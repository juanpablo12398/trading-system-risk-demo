import asyncio
import json
import os
import unittest
from datetime import datetime, timedelta, timezone

import httpx

from agent_sample.api_app import create_app
from agent_sample.audit import MemoryAuditStore, PostgresAuditStore
from agent_sample.evaluation import Observation, evaluate_holdout, replay_paper_decisions
from agent_sample.exchange import collect_quotes, parse_quote, rest_quote, websocket_quote
from agent_sample.fixtures import sample_rest, sample_websocket
from agent_sample.pipeline import Scenario, run_demo


def run(coro):
    return asyncio.run(coro)


class ExchangeTests(unittest.TestCase):
    def test_quote_normalizes_symbol_and_price(self):
        quote = parse_quote(
            {"symbol": " demo ", "price": "101.2", "event_time": "2024-01-01T00:00:00Z"},
            "rest",
        )
        self.assertEqual((quote.symbol, quote.price, quote.source), ("DEMO", 101.2, "rest"))

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            parse_quote({"symbol": "DEMO", "price": 0, "event_time": "2024-01-01T00:00:00Z"}, "rest")

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            parse_quote({"symbol": "DEMO", "price": 1, "event_time": "2024-01-01T00:00:00"}, "rest")

    def test_both_read_only_sources_collected(self):
        result = run(collect_quotes(sample_rest, sample_websocket))
        self.assertEqual(result["sources"], ["rest", "websocket"])
        self.assertEqual(result["price"], 101.3)
        self.assertTrue(result["complete"])

    def test_one_source_failure_marks_incomplete(self):
        async def broken():
            raise RuntimeError("offline")

        result = run(collect_quotes(sample_rest, broken))
        self.assertFalse(result["complete"])
        self.assertEqual(result["sources"], ["rest"])

    def test_both_sources_failure_rejected(self):
        async def broken():
            raise RuntimeError("offline")

        with self.assertRaises(RuntimeError):
            run(collect_quotes(broken, broken))

    def test_symbol_disagreement_rejected(self):
        async def different():
            return parse_quote(
                {"symbol": "OTHER", "price": 1, "event_time": "2024-01-01T00:00:00Z"},
                "websocket",
            )

        with self.assertRaises(ValueError):
            run(collect_quotes(sample_rest, different))

    def test_rest_adapter_uses_get_only(self):
        async def scenario():
            calls = []

            def handler(request):
                calls.append(request.method)
                return httpx.Response(200, json={
                    "symbol": "DEMO", "price": 10, "event_time": "2024-01-01T00:00:00Z"
                })

            async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
                result = await rest_quote("https://example.invalid/quote", client)
            return calls, result

        calls, quote = run(scenario())
        self.assertEqual(calls, ["GET"])
        self.assertEqual(quote.price, 10)

    def test_websocket_adapter_reads_one_frame(self):
        class Socket:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *_):
                return False

            async def recv(self):
                return json.dumps({
                    "symbol": "DEMO", "price": 11, "event_time": "2024-01-01T00:00:00Z"
                })

        result = run(websocket_quote("wss://example.invalid/stream", lambda _: Socket()))
        self.assertEqual((result.price, result.source), (11, "websocket"))


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.t = datetime(2024, 1, 1, tzinfo=timezone.utc)

    def row(self, probability=0.8, outcome=1, paper_return=0.02, approved=True,
            event_time=None, available_at=None):
        return Observation(event_time or self.t, available_at or self.t,
                           probability, outcome, paper_return, approved)

    def test_brier_and_accuracy_on_holdout(self):
        result = evaluate_holdout([self.row(), self.row(0.2, 0)])
        self.assertEqual(result, {"samples": 2, "brier_score": 0.04, "accuracy": 1.0})

    def test_future_information_rejected(self):
        future = self.row(available_at=self.t + timedelta(seconds=1))
        with self.assertRaises(ValueError):
            evaluate_holdout([future])
        with self.assertRaises(ValueError):
            replay_paper_decisions([future])

    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_holdout([self.row(probability=1.1)])

    def test_paper_replay_ignores_unapproved_row(self):
        result = replay_paper_decisions([
            self.row(approved=True),
            self.row(paper_return=-0.9, approved=False),
        ])
        self.assertEqual(result["paper_decisions"], 1)
        self.assertEqual(result["paper_return"], 0.02)

    def test_drawdown_is_measured(self):
        result = replay_paper_decisions([
            self.row(paper_return=0.1, event_time=self.t),
            self.row(paper_return=-0.1, event_time=self.t + timedelta(days=1)),
        ])
        self.assertEqual(result["max_drawdown"], 0.1)

    def test_empty_paper_replay(self):
        self.assertEqual(replay_paper_decisions([])["paper_decisions"], 0)


class PipelineTests(unittest.TestCase):
    def test_full_paper_cycle_includes_every_claimed_layer(self):
        async def scenario():
            store = MemoryAuditStore()
            result = await run_demo(Scenario(), store)
            return result, await store.recent()

        result, history = run(scenario())
        self.assertEqual(result["market"]["sources"], ["rest", "websocket"])
        self.assertEqual(result["agents"]["ok_count"], 2)
        self.assertEqual(result["review"]["kept_ids"], ["FICTIONAL-CANDIDATE"])
        self.assertEqual(result["evaluation"]["samples"], 4)
        self.assertEqual(result["backtest"]["paper_decisions"], 2)
        self.assertTrue(result["controls"]["allowed"])
        self.assertFalse(result["controls"]["live_orders"])
        self.assertEqual(result, history[0])

    def test_reviewer_veto_blocks_paper_path(self):
        result = run(run_demo(Scenario(veto=True), MemoryAuditStore()))
        self.assertFalse(result["controls"]["allowed"])
        self.assertEqual(result["review"]["kept_ids"], [])

    def test_stale_data_blocks_paper_path(self):
        result = run(run_demo(Scenario(fresh=False), MemoryAuditStore()))
        self.assertFalse(result["controls"]["allowed"])

    def test_missing_authority_blocks_paper_path(self):
        result = run(run_demo(Scenario(authority=False), MemoryAuditStore()))
        self.assertFalse(result["controls"]["allowed"])

    def test_exposure_cap_blocks_paper_path(self):
        result = run(run_demo(Scenario(exposure=61), MemoryAuditStore()))
        self.assertFalse(result["controls"]["allowed"])

    def test_partial_feed_blocks_paper_path(self):
        async def broken():
            raise RuntimeError("offline")

        result = run(run_demo(Scenario(), MemoryAuditStore(), websocket=broken))
        self.assertFalse(result["market"]["complete"])
        self.assertFalse(result["controls"]["allowed"])

    def test_bad_exposure_rejected(self):
        with self.assertRaises(ValueError):
            Scenario(exposure=101)

    def test_model_error_cannot_approve_candidate(self):
        async def broken_model(*_):
            raise RuntimeError("offline")

        result = run(run_demo(Scenario(), MemoryAuditStore(), llm_transport=broken_model))
        self.assertFalse(result["controls"]["allowed"])
        self.assertEqual(result["review"]["reviews"][0]["verdict"], "manual_review")


class ApiTests(unittest.TestCase):
    def test_http_cycle_and_history_use_same_result(self):
        async def scenario():
            app = create_app(MemoryAuditStore())
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://test"
            ) as client:
                mode = (await client.get("/api/demo/mode")).json()
                result = (await client.post("/api/demo/cycle", json={
                    "fresh": True, "authority": True, "exposure": 35, "veto": False
                })).json()
                history = (await client.get("/api/demo/history")).json()
            return mode, result, history

        mode, result, history = run(scenario())
        self.assertEqual(mode["storage"], "memory")
        self.assertEqual(result, history[0])

    def test_http_rejects_out_of_range_exposure(self):
        async def scenario():
            app = create_app(MemoryAuditStore())
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://test"
            ) as client:
                return await client.post("/api/demo/cycle", json={"exposure": 101})

        self.assertEqual(run(scenario()).status_code, 422)

    def test_no_order_route_exists(self):
        async def scenario():
            app = create_app(MemoryAuditStore())
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://test"
            ) as client:
                return await client.post("/api/orders")

        self.assertEqual(run(scenario()).status_code, 404)


@unittest.skipUnless(os.environ.get("TEST_POSTGRES_DSN"), "requires CI PostgreSQL")
class PostgresAuditTests(unittest.TestCase):
    def test_audit_round_trip(self):
        async def scenario():
            store = PostgresAuditStore(os.environ["TEST_POSTGRES_DSN"])
            saved = await store.append({"kind": "fictional-test"})
            return saved, await store.recent()

        saved, recent = run(scenario())
        self.assertTrue(any(item["id"] == saved["id"] for item in recent))
