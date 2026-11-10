"""One synthetic, paper-only path through ingest, agents, evaluation and audit."""

from dataclasses import dataclass
from typing import Any

from .agents import NewsReviewAgent
from .brain import SharedBrain
from .evaluation import evaluate_holdout, replay_paper_decisions
from .exchange import QuoteSource, collect_quotes
from .fixtures import sample_holdout, sample_news, sample_rest, sample_websocket
from .llm import ClaudeClient, Transport
from .orchestrator import run_agents
from .predictive import evaluate_chronological_holdout
from .reviewer import ReviewGuardAgent
from .risk import evaluate_demo_gates


@dataclass(frozen=True)
class Scenario:
    fresh: bool = True
    authority: bool = True
    exposure: int = 35
    veto: bool = False

    def __post_init__(self):
        if not 0 <= self.exposure <= 100:
            raise ValueError("fictional exposure must be between 0 and 100")


async def run_demo(
    scenario: Scenario,
    audit_store: Any,
    *,
    rest: QuoteSource = sample_rest,
    websocket: QuoteSource = sample_websocket,
    llm_transport: Transport | None = None,
) -> dict[str, Any]:
    market = await collect_quotes(rest, websocket)
    brain = SharedBrain()
    await brain.init_cycle()

    async def fictional_llm(prompt: str, system: str, model: str) -> str:
        if "Review fictional item" in prompt:
            return '{"verdict":"veto"}' if scenario.veto else '{"verdict":"allow"}'
        return '{"summary":"Fictional context reviewed"}'

    client = ClaudeClient(llm_transport or fictional_llm, timeout=2, attempts=2)
    news = NewsReviewAgent(brain, client, [sample_news])

    async def quality_agent():
        await brain.store("sample/quality", {"complete": market["complete"]})
        return {"status": "ok" if market["complete"] else "error", "complete": market["complete"]}

    orchestrated = await run_agents(
        {"news": news.run, "data_quality": quality_agent}, timeout=3
    )
    reviewer = await ReviewGuardAgent(brain, client).run([
        {"id": "FICTIONAL-CANDIDATE", "preapproved": True},
        {"id": "PRE-REJECTED", "preapproved": False},
    ])

    holdout = sample_holdout()
    evaluation = evaluate_holdout(holdout)
    backtest = replay_paper_decisions(holdout)
    prediction = evaluate_chronological_holdout(
        [10.0, 10.9, 11.4, 12.3, 12.9, 13.8, 14.5, 15.2], train_size=5
    )
    controls = evaluate_demo_gates(
        fresh=scenario.fresh,
        authority=scenario.authority,
        exposure=scenario.exposure,
        complete_data=market["complete"],
        review_kept="FICTIONAL-CANDIDATE" in reviewer["kept_ids"],
        model_validated=(
            prediction["holdout_samples"] >= 3
            and prediction["mae"] <= prediction["persistence_mae"]
        ),
    )
    trace = [
        {"kind": "Input", "message": "Fictional REST and WebSocket snapshots normalized"},
        {"kind": "Agents", "message": f"{orchestrated['ok_count']} of {orchestrated['total_count']} parallel agents completed"},
        {"kind": "Review", "message": reviewer["reviews"][0]["verdict"]},
        {"kind": "Evaluation", "message": f"{evaluation['samples']} synthetic holdout rows replayed"},
        {"kind": "Prediction", "message": f"{prediction['training_pairs']} fictional training pairs; {prediction['holdout_samples']} later predictions"},
        {"kind": "Control", "message": "Paper path eligible" if controls["allowed"] else "Paper path blocked"},
    ]
    saved = await audit_store.append({
        "market": market,
        "agents": orchestrated,
        "review": reviewer,
        "evaluation": evaluation,
        "prediction": prediction,
        "backtest": backtest,
        "controls": controls,
        "trace": trace,
    })
    return saved
