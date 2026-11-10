import React from "react";
import { beforeEach, describe, expect, test, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";
import { demoApi } from "./api";

vi.mock("./api", () => ({
  demoApi: { mode: vi.fn(), history: vi.fn(), cycle: vi.fn() },
}));

const result = {
  id: "12345678-demo",
  market: { symbol: "DEMOUSD", price: 101.3, sources: ["rest", "websocket"], complete: true },
  agents: {
    ok_count: 2, total_count: 2,
    results: {
      news: { status: "ok", data: { summary: "Fictional context reviewed" } },
      data_quality: { status: "ok" },
    },
  },
  review: { reviews: [{ verdict: "allow" }, { verdict: "skipped" }] },
  evaluation: { samples: 4, brier_score: 0.2325, accuracy: 0.5 },
  backtest: { paper_decisions: 2, paper_return: -0.0106, max_drawdown: 0.03 },
  controls: {
    allowed: true, live_orders: false,
    checks: [
      { name: "Recent market data", passed: true },
      { name: "Bounded context review", passed: true },
    ],
  },
  trace: [
    { kind: "Input", message: "Fictional REST and WebSocket snapshots normalized" },
    { kind: "Control", message: "Paper path eligible" },
  ],
};

beforeEach(() => {
  vi.clearAllMocks();
  demoApi.mode.mockResolvedValue({ storage: "PostgreSQL", orders: "disabled" });
  demoApi.history.mockResolvedValue([]);
  demoApi.cycle.mockResolvedValue(result);
});

describe("Trading System connected sample", () => {
  test("identifies the sample as paper only and loads backend mode", async () => {
    render(<App />);
    expect(await screen.findByText("PostgreSQL")).toBeInTheDocument();
    expect(screen.getByText("Orders disabled")).toBeInTheDocument();
    expect(screen.getByText(/No account connection, order endpoint/)).toBeInTheDocument();
  });

  test("runs backend cycle and shows agents, feeds, evaluation and controls", async () => {
    const user = userEvent.setup();
    demoApi.history.mockResolvedValueOnce([]).mockResolvedValueOnce([result]);
    render(<App />);
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    expect(demoApi.cycle).toHaveBeenCalledWith({
      fresh: true, authority: true, exposure: 35, veto: false,
    });
    expect(await screen.findByText("2/2 parallel agents completed.")).toBeInTheDocument();
    expect(screen.getByText(/News agent: ok/)).toBeInTheDocument();
    expect(screen.getByText(/Brier score: 0.2325/)).toBeInTheDocument();
    expect(screen.getByText(/Paper decisions: 2/)).toBeInTheDocument();
    expect(screen.getByText("rest + websocket")).toBeInTheDocument();
    expect(screen.getAllByText("Paper path eligible").length).toBeGreaterThan(0);
    expect(screen.getByText("Fictional REST and WebSocket snapshots normalized")).toBeInTheDocument();
    expect(screen.getByText("12345678")).toBeInTheDocument();
  });

  test("control change clears stale result and sends the changed scenario", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    await screen.findByText("2/2 parallel agents completed.");
    await user.click(screen.getByRole("checkbox", { name: "Market data is fresh" }));
    expect(screen.queryByText("2/2 parallel agents completed.")).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    expect(demoApi.cycle).toHaveBeenLastCalledWith(expect.objectContaining({ fresh: false }));
  });

  test("vetoed result is shown as blocked", async () => {
    const user = userEvent.setup();
    demoApi.cycle.mockResolvedValue({
      ...result,
      review: { reviews: [{ verdict: "veto" }, { verdict: "skipped" }] },
      controls: {
        allowed: false, live_orders: false,
        checks: [{ name: "Bounded context review", passed: false }],
      },
      trace: [{ kind: "Control", message: "Paper path blocked" }],
    });
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Context reviewer veto" }));
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    expect(await screen.findByText("Fail closed: paper path blocked")).toBeInTheDocument();
    expect(screen.getByText(/Reviewer: veto/)).toBeInTheDocument();
  });

  test("API failure is visible and does not invent a result", async () => {
    const user = userEvent.setup();
    demoApi.cycle.mockRejectedValue(new Error("Demo API offline"));
    render(<App />);
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Demo API offline");
    expect(screen.queryByText("2/2 parallel agents completed.")).not.toBeInTheDocument();
  });

  test("history from backend is visible on initial load", async () => {
    demoApi.history.mockResolvedValue([result]);
    render(<App />);
    expect(await screen.findByText("12345678")).toBeInTheDocument();
  });

  test("exposure and authority controls reach the backend request", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Exclusive authority held" }));
    fireEvent.change(screen.getByRole("slider", { name: "Illustrative exposure" }), {
      target: { value: "61" },
    });
    await user.click(screen.getByRole("button", { name: "Run paper cycle" }));
    expect(demoApi.cycle).toHaveBeenCalledWith(expect.objectContaining({
      authority: false, exposure: 61,
    }));
  });

  test("unavailable backend mode is reported", async () => {
    demoApi.mode.mockRejectedValue(new Error("Mode API offline"));
    render(<App />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Mode API offline");
  });
});
