import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.js"],
    coverage: {
      provider: "v8",
      include: ["src/App.jsx", "src/api.js"],
      reporter: ["text", "json-summary"],
      thresholds: { statements: 75, branches: 65, functions: 75, lines: 75 },
    },
  },
});
