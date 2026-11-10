# Trading System · public risk demo

![Public demo preview](docs/preview.png)

An isolated **React + Vite** case study that visualizes fail-closed controls, exclusive cycle authority, dry-run behavior and an audit trace in an experimental agent-based trading project. Every event and parameter in this repository is fictional. The `evaluateDemo` function is generic teaching code, **not** the private risk engine or trading logic.

The private project uses Python orchestration, a market-data collector, PostgreSQL, an exchange adapter, agent components and an operational dashboard. In its documented Railway configuration, Railway runs the **collector and dashboard only**; trading and shadow cycles run locally against the same database. This public UI is a new presentation sample and does not claim to be the private dashboard or a production trading deployment.

No exchange API, model, strategy, order endpoint, real credential, market feed or proprietary parameter is present. **Live order execution is impossible** from this repository.

## Run

```bash
npm install
npm run dev
```

Run `npm test` for the published React behavior and `npm run build` for a production bundle check. The [documentation index](docs/00-indice/INDICE.md) contains the public specification, SDD, decisions, walkthrough and test strategy. These tests do not verify the private engine, market data or exchange adapters.

## What to inspect

- `src/App.jsx`: pure illustrative control evaluation, state driven gates and conditional trace.
- `src/styles.css`: responsive monitoring interface.
- The UI explains failed controls instead of quietly proceeding.

**Scope:** Limited public sample of engineering principles, not financial advice and not a deployable trading system. Designed and implemented by Juan Pablo Verdondoni.

Copyright © Juan Pablo Verdondoni. No reuse license is granted for this public sample.
