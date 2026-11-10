async function request(path, options) {
  const response = await fetch("/api/demo" + path, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Demo API returned ${response.status}`);
  return body;
}

export const demoApi = {
  mode: () => request("/mode"),
  history: () => request("/history"),
  cycle: (scenario) =>
    request("/cycle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(scenario),
    }),
};
