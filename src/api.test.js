import { beforeEach, expect, test, vi } from "vitest";
import { demoApi } from "./api";

beforeEach(() => vi.unstubAllGlobals());

test("cycle posts scenario to Python API", async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ id: "demo" }) });
  vi.stubGlobal("fetch", fetchMock);
  const scenario = { fresh: true, authority: false, exposure: 35, veto: false };
  await demoApi.cycle(scenario);
  expect(fetchMock).toHaveBeenCalledWith("/api/demo/cycle", expect.objectContaining({
    method: "POST",
    body: JSON.stringify(scenario),
  }));
});

test("HTTP error is surfaced", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
    ok: false, status: 503, json: async () => ({ detail: "Service unavailable" }),
  }));
  await expect(demoApi.history()).rejects.toThrow("Service unavailable");
});

test("mode and history use read-only endpoints", async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => [] });
  vi.stubGlobal("fetch", fetchMock);
  await demoApi.mode();
  await demoApi.history();
  expect(fetchMock.mock.calls.map(([url]) => url)).toEqual([
    "/api/demo/mode", "/api/demo/history",
  ]);
});
