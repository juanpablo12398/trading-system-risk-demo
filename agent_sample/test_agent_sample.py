import asyncio
import unittest

from agent_sample.agents import NewsReviewAgent
from agent_sample.brain import SharedBrain
from agent_sample.llm import ClaudeClient, InvalidResponseError, RetryableLLMError, parse_object
from agent_sample.orchestrator import run_agents


def run(coro):
    return asyncio.run(coro)


class ParseTests(unittest.TestCase):
    def test_plain_json(self):
        self.assertEqual(parse_object('{"summary":"ok"}'), {"summary": "ok"})

    def test_fenced_json(self):
        self.assertEqual(parse_object('```json\n{"summary":"ok"}\n```'), {"summary": "ok"})

    def test_invalid_json_rejected(self):
        with self.assertRaises(InvalidResponseError):
            parse_object("not JSON")

    def test_array_rejected(self):
        with self.assertRaises(InvalidResponseError):
            parse_object("[]")


class ClientTests(unittest.TestCase):
    def test_success(self):
        async def transport(prompt, system, model):
            self.assertEqual((prompt, system, model), ("p", "s", "haiku"))
            return '{"summary":"done"}'

        result = run(ClaudeClient(transport).ask(prompt="p", system="s"))
        self.assertEqual(result["summary"], "done")

    def test_retries_transient_error(self):
        calls = []

        async def transport(*_):
            calls.append(1)
            if len(calls) < 3:
                raise RetryableLLMError()
            return '{"summary":"done"}'

        self.assertEqual(run(ClaudeClient(transport).ask(prompt="p", system="s"))["summary"], "done")
        self.assertEqual(len(calls), 3)

    def test_retry_limit(self):
        calls = []

        async def transport(*_):
            calls.append(1)
            raise RetryableLLMError()

        with self.assertRaises(RetryableLLMError):
            run(ClaudeClient(transport, attempts=2).ask(prompt="p", system="s"))
        self.assertEqual(len(calls), 2)

    def test_timeout(self):
        async def transport(*_):
            await asyncio.sleep(0.04)
            return "{}"

        with self.assertRaises(TimeoutError):
            run(ClaudeClient(transport, timeout=0.001, attempts=1).ask(prompt="p", system="s"))

    def test_invalid_json_not_retried(self):
        calls = []

        async def transport(*_):
            calls.append(1)
            return "bad"

        with self.assertRaises(InvalidResponseError):
            run(ClaudeClient(transport).ask(prompt="p", system="s"))
        self.assertEqual(len(calls), 1)


class BrainTests(unittest.TestCase):
    def test_store_and_recall_copies_values(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()
            data = {"nested": {"x": 1}}
            await brain.store("sample/news", data)
            data["nested"]["x"] = 2
            restored = await brain.recall("sample/news")
            restored["nested"]["x"] = 3
            return await brain.recall("sample/news"), await brain.snapshot()

        recalled, snapshot = run(scenario())
        self.assertEqual(recalled["nested"]["x"], 1)
        self.assertEqual(snapshot["sample/news"]["nested"]["x"], 1)

    def test_cycle_isolation_between_tasks(self):
        async def scenario():
            brain = SharedBrain()

            async def task(value):
                await brain.init_cycle()
                await brain.store("same", {"value": value})
                await asyncio.sleep(0)
                return await brain.recall("same")

            return await asyncio.gather(task("a"), task("b"))

        self.assertEqual(run(scenario()), [{"value": "a"}, {"value": "b"}])

    def test_uninitialized_task_cannot_read(self):
        with self.assertRaises(RuntimeError):
            run(SharedBrain().recall("sample/news"))

    def test_bad_value_rejected(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()
            await brain.store("", {})

        with self.assertRaises(ValueError):
            run(scenario())


class AgentTests(unittest.TestCase):
    def test_news_agent_calls_llm_and_stores_result(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()

            async def source():
                return [{"title": "Example headline"}, {"title": "example headline"}]

            async def transport(prompt, system, model):
                self.assertIn("Example headline", prompt)
                return '{"summary":"Public example"}'

            agent = NewsReviewAgent(brain, ClaudeClient(transport), [source])
            result = await agent.run()
            return result, await brain.recall(agent.namespace)

        result, stored = run(scenario())
        self.assertEqual(result, stored)
        self.assertEqual(result["story_count"], 1)
        self.assertEqual(result["status"], "ok")

    def test_partial_source_failure(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()

            async def fail():
                raise RuntimeError("offline")

            async def good():
                return [{"title": "Fictional story"}]

            async def transport(*_):
                return '{"summary":"ok"}'

            return await NewsReviewAgent(brain, ClaudeClient(transport), [fail, good]).run()

        result = run(scenario())
        self.assertEqual((result["status"], result["source_failures"]), ("ok", 1))

    def test_no_data_does_not_call_llm(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()

            async def source():
                return []

            async def transport(*_):
                raise AssertionError("must not call LLM")

            return await NewsReviewAgent(brain, ClaudeClient(transport), [source]).run()

        self.assertEqual(run(scenario())["status"], "no_data")

    def test_invalid_llm_result_fails_closed(self):
        async def scenario():
            brain = SharedBrain()
            await brain.init_cycle()

            async def source():
                return [{"title": "Fictional story"}]

            async def transport(*_):
                return '{"wrong_field":1}'

            return await NewsReviewAgent(brain, ClaudeClient(transport), [source]).run()

        self.assertEqual(run(scenario())["status"], "error")


class OrchestratorTests(unittest.TestCase):
    def test_parallel_execution(self):
        async def scenario():
            started = 0
            barrier = asyncio.Event()

            async def agent():
                nonlocal started
                started += 1
                if started == 2:
                    barrier.set()
                await barrier.wait()
                return {"status": "ok"}

            return await run_agents({"a": agent, "b": agent}, timeout=0.05)

        self.assertEqual(run(scenario())["ok_count"], 2)

    def test_failure_isolated(self):
        async def good():
            return {"status": "ok"}

        async def bad():
            raise ValueError("sensitive message")

        result = run(run_agents({"good": good, "bad": bad}))
        self.assertEqual(result["ok_count"], 1)
        self.assertEqual(result["results"]["bad"]["error_type"], "ValueError")
        self.assertNotIn("sensitive message", str(result))

    def test_timeout_isolated(self):
        async def slow():
            await asyncio.sleep(0.04)
            return {"status": "ok"}

        self.assertEqual(run(run_agents({"slow": slow}, timeout=0.001))["results"]["slow"]["status"], "timeout")

    def test_non_dict_is_error(self):
        async def bad():
            return "bad"

        self.assertEqual(run(run_agents({"bad": bad}))["results"]["bad"]["error_type"], "TypeError")


if __name__ == "__main__":
    unittest.main()
