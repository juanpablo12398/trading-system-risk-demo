import React, { useEffect, useState } from "react";
import { demoApi } from "./api";

export default function App() {
  const [scenario, setScenario] = useState({
    fresh: true,
    authority: true,
    exposure: 35,
    veto: false,
  });
  const [mode, setMode] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    demoApi.mode().then((value) => active && setMode(value))
      .catch((failure) => active && setError(failure.message));
    demoApi.history().then((items) => active && setHistory(items)).catch(() => {});
    return () => { active = false; };
  }, []);

  function update(key, value) {
    setScenario((current) => ({ ...current, [key]: value }));
    setResult(null);
  }

  async function runCycle() {
    setBusy(true);
    setError("");
    try {
      const next = await demoApi.cycle(scenario);
      setResult(next);
      setHistory(await demoApi.history());
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(false);
    }
  }

  const checks = result?.controls?.checks ?? [];
  return (
    <div className="layout">
      <aside>
        <div className="identity">
          <span className="glyph">◇</span>
          <div><strong>TRADING SYSTEM</strong><small>PUBLIC ENGINEERING SAMPLE</small></div>
        </div>
        <nav>
          <span className="selected">▦ &nbsp; Paper cycle</span>
          <span>◷ &nbsp; Holdout replay</span>
          <span>▤ &nbsp; Audit trail</span>
        </nav>
        <div className="safety">
          <span>● &nbsp; SYNTHETIC DATA</span>
          <p>Read-only data adapters. No account connection, order endpoint or private strategy.</p>
        </div>
      </aside>
      <main>
        <header>
          <div>
            <span className="eyebrow">REACT → PYTHON API → AGENTS → AUDIT</span>
            <h1>Inspect a paper-only cycle</h1>
            <p>
              This connected sample runs fictional REST and WebSocket snapshots
              through agents, model evaluation, paper replay and risk gates.
              The full experimental system remains private.
            </p>
          </div>
          <div className="mode">PAPER ONLY<br /><strong>Orders disabled</strong></div>
        </header>
        {error && <p className="api-error" role="alert">{error}</p>}
        <section className="topline">
          <div><small>Storage</small><strong>{mode?.storage ?? "Connecting"}</strong></div>
          <div><small>Market inputs</small><strong>{result?.market?.sources?.join(" + ") ?? "Not run"}</strong></div>
          <div><small>Decision</small>
            <strong className={result?.controls?.allowed ? "pass" : "block"}>
              {!result ? "Not run" : result.controls.allowed ? "Paper path eligible" : "Blocked"}
            </strong>
          </div>
          <div><small>Live orders</small><strong>Disabled</strong></div>
        </section>
        <section className="grid">
          <article className="panel">
            <div className="panel-head">
              <div><span className="eyebrow">FICTIONAL INPUTS</span><h2>Run a scenario</h2></div>
              <span className="demo-tag">No live API calls</span>
            </div>
            <div className="toggle-row">
              <div><strong>Market data is fresh</strong><small>Stale inputs block the paper path.</small></div>
              <input type="checkbox" checked={scenario.fresh}
                onChange={(event) => update("fresh", event.target.checked)}
                aria-label="Market data is fresh" />
            </div>
            <div className="toggle-row">
              <div><strong>Exclusive authority held</strong><small>One cycle owns the sample decision.</small></div>
              <input type="checkbox" checked={scenario.authority}
                onChange={(event) => update("authority", event.target.checked)}
                aria-label="Exclusive authority held" />
            </div>
            <div className="toggle-row">
              <div><strong>Context reviewer veto</strong><small>Exercise the bounded LLM verdict.</small></div>
              <input type="checkbox" checked={scenario.veto}
                onChange={(event) => update("veto", event.target.checked)}
                aria-label="Context reviewer veto" />
            </div>
            <div className="slider-row">
              <div><strong>Illustrative exposure</strong><small>Demo cap: 60 units; unrelated to private rules.</small></div>
              <strong>{scenario.exposure} units</strong>
            </div>
            <input className="slider" type="range" min="0" max="100"
              value={scenario.exposure}
              onChange={(event) => update("exposure", Number(event.target.value))}
              aria-label="Illustrative exposure" />
            <button className="run-button" onClick={runCycle} disabled={busy}>
              {busy ? "Running…" : "Run paper cycle"}
            </button>
          </article>
          <article className="panel">
            <div className="panel-head"><div><span className="eyebrow">BACKEND RESULT</span><h2>Safety gates</h2></div></div>
            {checks.length ? (
              <>
                <div className="gates">
                  {checks.map((check) => (
                    <div className="gate" key={check.name}>
                      <span className={check.passed ? "check" : "cross"}>{check.passed ? "✓" : "×"}</span>
                      <div><strong>{check.name}</strong></div>
                      <em className={check.passed ? "ok" : "bad"}>{check.passed ? "PASS" : "BLOCK"}</em>
                    </div>
                  ))}
                </div>
                <div className={`decision ${result.controls.allowed ? "allowed" : "denied"}`}>
                  <strong>{result.controls.allowed ? "Paper path eligible" : "Fail closed: paper path blocked"}</strong>
                  <p>No code in this repository can place an order.</p>
                </div>
              </>
            ) : <p className="placeholder">Run the backend cycle to see evaluated gates.</p>}
          </article>
        </section>
        {result && (
          <section className="grid result-grid">
            <article className="panel">
              <div className="panel-head"><div><span className="eyebrow">AGENT SYSTEM</span><h2>Orchestration and review</h2></div></div>
              <p>{result.agents.ok_count}/{result.agents.total_count} parallel agents completed.</p>
              <p>News agent: {result.agents.results.news.status} · Data quality: {result.agents.results.data_quality.status}</p>
              <p>Reviewer: {result.review.reviews[0].verdict} · Previously rejected input: {result.review.reviews[1].verdict}</p>
              <p>Shared context: {result.agents.results.news.data?.summary ?? "No summary"}</p>
            </article>
            <article className="panel">
              <div className="panel-head"><div><span className="eyebrow">MODEL EVIDENCE</span><h2>Holdout and paper replay</h2></div></div>
              <p>Holdout observations: {result.evaluation.samples}</p>
              <p>Brier score: {result.evaluation.brier_score} · Accuracy: {result.evaluation.accuracy}</p>
              <p>Paper decisions: {result.backtest.paper_decisions}</p>
              <p>Paper return: {result.backtest.paper_return} · Max drawdown: {result.backtest.max_drawdown}</p>
              <small>Fixed fictional observations; no model training, live prices or strategy disclosed.</small>
            </article>
          </section>
        )}
        <section className="panel trace">
          <div className="panel-head"><div><span className="eyebrow">OBSERVABILITY</span><h2>Cycle trace</h2></div></div>
          {result ? <div className="events">
            {result.trace.map((event, index) => (
              <div key={index}><span>{String(index + 1).padStart(2, "0")}</span>
                <strong>{event.message}</strong><em>{event.kind}</em></div>
            ))}
          </div> : <p className="placeholder">A backend generated trace appears after a paper cycle.</p>}
        </section>
        <section className="panel trace">
          <div className="panel-head"><div><span className="eyebrow">PERSISTENCE</span><h2>Audit history</h2></div></div>
          {history.length ? <div className="events">
            {history.map((event) => (
              <div key={event.id}><span>{event.id.slice(0, 8)}</span>
                <strong>{event.controls.allowed ? "Paper path eligible" : "Blocked"}</strong>
                <em>{event.market.symbol}</em></div>
            ))}
          </div> : <p className="placeholder">No cycles recorded in this demo session.</p>}
        </section>
        <footer>
          Public sample by Juan Pablo Verdondoni · Synthetic inputs and adapted
          architecture. Private collectors, models, strategies and exchange
          operations are excluded.
        </footer>
      </main>
    </div>
  );
}
