import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

describe("Trading System public risk demo", () => {
  test("defaults to simulated eligibility with live orders disabled", () => {
    render(<App />);
    expect(screen.getByText("Eligible for simulation")).toBeInTheDocument();
    expect(screen.getByText("Demo path can continue")).toBeInTheDocument();
    expect(screen.getByText("Disabled")).toBeInTheDocument();
    expect(screen.getAllByText("PASS")).toHaveLength(3);
  });

  test("stale data fails closed", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Market data is fresh" }));
    expect(screen.getByText("Blocked")).toBeInTheDocument();
    expect(screen.getByText("Fail closed: demo path stopped")).toBeInTheDocument();
    expect(screen.getAllByText("BLOCK")).toHaveLength(1);
  });

  test("missing exclusive authority blocks the path", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Exclusive authority held" }));
    expect(screen.getByText("Missing")).toBeInTheDocument();
    expect(screen.getByText("Blocked")).toBeInTheDocument();
  });

  test("the illustrative cap passes at 60 and blocks above 60", () => {
    render(<App />);
    const slider = screen.getByRole("slider", { name: "Illustrative exposure" });
    fireEvent.change(slider, { target: { value: "60" } });
    expect(screen.getByText("Eligible for simulation")).toBeInTheDocument();
    fireEvent.change(slider, { target: { value: "61" } });
    expect(screen.getByText("Blocked")).toBeInTheDocument();
    fireEvent.change(slider, { target: { value: "0" } });
    expect(screen.getByText("Eligible for simulation")).toBeInTheDocument();
  });

  test("sample trace can be opened and closed without an execution action", async () => {
    const user = userEvent.setup();
    render(<App />);
    expect(screen.queryByText("Synthetic cycle received")).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Show sample trace" }));
    expect(screen.getByText("Synthetic cycle received")).toBeInTheDocument();
    expect(screen.getByText("Dry-run audit recorded")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Hide sample trace" }));
    expect(screen.queryByText("Synthetic cycle received")).not.toBeInTheDocument();
    expect(screen.getByText(/cannot trade/)).toBeInTheDocument();
  });

  test("multiple failed controls are all shown while decision remains blocked", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Market data is fresh" }));
    await user.click(screen.getByRole("checkbox", { name: "Exclusive authority held" }));
    fireEvent.change(screen.getByRole("slider", { name: "Illustrative exposure" }), {
      target: { value: "100" },
    });
    expect(screen.getAllByText("BLOCK")).toHaveLength(3);
    expect(screen.getByText("Fail closed: demo path stopped")).toBeInTheDocument();
    expect(screen.getByText("Disabled")).toBeInTheDocument();
  });

  test("restoring controls returns to simulation eligibility", async () => {
    const user = userEvent.setup();
    render(<App />);
    const freshness = screen.getByRole("checkbox", { name: "Market data is fresh" });
    await user.click(freshness);
    expect(screen.getByText("Blocked")).toBeInTheDocument();
    await user.click(freshness);
    expect(screen.getByText("Eligible for simulation")).toBeInTheDocument();
    expect(screen.getAllByText("PASS")).toHaveLength(3);
  });

  test("opening a static trace does not change a blocked decision", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("checkbox", { name: "Market data is fresh" }));
    await user.click(screen.getByRole("button", { name: "Show sample trace" }));
    expect(screen.getByText("Synthetic cycle received")).toBeInTheDocument();
    expect(screen.getByText("Blocked")).toBeInTheDocument();
    expect(screen.getByText("Disabled")).toBeInTheDocument();
  });
});
