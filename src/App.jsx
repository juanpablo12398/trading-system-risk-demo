import React, { useMemo, useState } from "react";

const sampleEvents = [
  {
    id: "SIM-401",
    label: "Synthetic cycle received",
    kind: "Input",
    time: "09:00:00",
  },
  {
    id: "SIM-402",
    label: "Data quality checked",
    kind: "Validation",
    time: "09:00:02",
  },
  {
    id: "SIM-403",
    label: "Risk gates evaluated",
    kind: "Control",
    time: "09:00:03",
  },
  {
    id: "SIM-404",
    label: "Dry-run audit recorded",
    kind: "Audit",
    time: "09:00:04",
  },
];

// Generic visualization logic. It is not a trading strategy or the private system's risk engine.
function evaluateDemo({ fresh, lease, exposure }) {
  const checks = [
    { name: "Recent market data", passed: fresh, note: "Reject stale inputs" },
    {
      name: "Exclusive cycle authority",
      passed: lease,
      note: "Single active operator",
    },
    {
      name: "Illustrative exposure cap",
      passed: exposure <= 60,
      note: "Demo threshold only",
    },
  ];
  return { checks, allowed: checks.every((check) => check.passed) };
}

export default function App() {
  const [fresh, setFresh] = useState(true);
  const [lease, setLease] = useState(true);
  const [exposure, setExposure] = useState(35);
  const [showTrace, setShowTrace] = useState(false);
  const result = useMemo(
    () => evaluateDemo({ fresh, lease, exposure }),
    [fresh, lease, exposure],
  );
  return (
    <div className="layout">
      <aside>
        <div className="identity">
          <span className="glyph">◇</span>
          <div>
            <strong>TRADING SYSTEM</strong>
            <small>RISK CONSOLE / DEMO</small>
          </div>
        </div>
        <nav>
          <span className="selected">▦ &nbsp; Control plane</span>
          <span>◷ &nbsp; Cycle history</span>
          <span>▤ &nbsp; Audit trail</span>
        </nav>
        <div className="safety">
          <span>● &nbsp; SANDBOX ONLY</span>
          <p>
            No market connection. No order execution. No proprietary strategy
            code.
          </p>
        </div>
      </aside>
      <main>
        <header>
          <div>
            <span className="eyebrow">
              PUBLIC REACT CASE STUDY · SYNTHETIC SCENARIO
            </span>
            <h1>Risk before execution</h1>
            <p>
              A focused illustration of fail-closed controls and observable
              decisions in an experimental multi-agent system.
            </p>
          </div>
          <div className="mode">
            DRY RUN
            <br />
            <strong>Always on</strong>
          </div>
        </header>
        <section className="topline">
          <div>
            <small>System mode</small>
            <strong>Simulation</strong>
          </div>
          <div>
            <small>Cycle authority</small>
            <strong>{lease ? "Acquired" : "Missing"}</strong>
          </div>
          <div>
            <small>Decision</small>
            <strong className={result.allowed ? "pass" : "block"}>
              {result.allowed ? "Eligible for simulation" : "Blocked"}
            </strong>
          </div>
          <div>
            <small>Live orders</small>
            <strong>Disabled</strong>
          </div>
        </section>
        <section className="grid">
          <article className="panel">
            <div className="panel-head">
              <div>
                <span className="eyebrow">CONTROL SURFACE</span>
                <h2>Change the scenario</h2>
              </div>
              <span className="demo-tag">Synthetic inputs</span>
            </div>
            <div className="toggle-row">
              <div>
                <strong>Market data is fresh</strong>
                <small>A stale feed should stop the cycle.</small>
              </div>
              <input
                type="checkbox"
                checked={fresh}
                onChange={(event) => setFresh(event.target.checked)}
                aria-label="Market data is fresh"
              />
            </div>
            <div className="toggle-row">
              <div>
                <strong>Exclusive authority held</strong>
                <small>Only one cycle may own this simulation.</small>
              </div>
              <input
                type="checkbox"
                checked={lease}
                onChange={(event) => setLease(event.target.checked)}
                aria-label="Exclusive authority held"
              />
            </div>
            <div className="slider-row">
              <div>
                <strong>Illustrative exposure</strong>
                <small>Demo cap: 60 units, unrelated to real settings.</small>
              </div>
              <strong>{exposure} units</strong>
            </div>
            <input
              className="slider"
              type="range"
              min="0"
              max="100"
              value={exposure}
              onChange={(event) => setExposure(Number(event.target.value))}
              aria-label="Illustrative exposure"
            />
            <div className="hint">
              Adjust a control to see why the decision changes. This panel
              cannot trade.
            </div>
          </article>
          <article className="panel">
            <div className="panel-head">
              <div>
                <span className="eyebrow">EXPLAINABLE RESULT</span>
                <h2>Safety gates</h2>
              </div>
            </div>
            <div className="gates">
              {result.checks.map((check) => (
                <div className="gate" key={check.name}>
                  <span className={check.passed ? "check" : "cross"}>
                    {check.passed ? "✓" : "×"}
                  </span>
                  <div>
                    <strong>{check.name}</strong>
                    <small>{check.note}</small>
                  </div>
                  <em className={check.passed ? "ok" : "bad"}>
                    {check.passed ? "PASS" : "BLOCK"}
                  </em>
                </div>
              ))}
            </div>
            <div
              className={`decision ${result.allowed ? "allowed" : "denied"}`}
            >
              <strong>
                {result.allowed
                  ? "Demo path can continue"
                  : "Fail closed: demo path stopped"}
              </strong>
              <p>
                {result.allowed
                  ? "The scenario is eligible for a simulated audit record only."
                  : "At least one control failed; no simulated action can proceed."}
              </p>
            </div>
          </article>
        </section>
        <section className="panel trace">
          <div className="panel-head">
            <div>
              <span className="eyebrow">OBSERVABILITY</span>
              <h2>Example cycle trace</h2>
            </div>
            <button onClick={() => setShowTrace((value) => !value)}>
              {showTrace ? "Hide" : "Show"} sample trace
            </button>
          </div>
          {showTrace ? (
            <div className="events">
              {sampleEvents.map((event) => (
                <div key={event.id}>
                  <span>{event.time}</span>
                  <strong>{event.label}</strong>
                  <em>{event.kind}</em>
                </div>
              ))}
            </div>
          ) : (
            <p className="placeholder">
              Open the static sample trace to inspect the simulated control
              flow.
            </p>
          )}
        </section>
        <footer>
          Public demo by Juan Pablo Verdondoni · Private collectors,
          orchestration, models, strategies and exchange adapters are excluded.
        </footer>
      </main>
    </div>
  );
}
