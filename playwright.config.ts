import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./playwright/tests",
  use: {
    baseURL: "http://127.0.0.1:8000",
    headless: true,
  },
  webServer: {
    command: "uvicorn app.main:app --host 0.0.0.0 --port 8000",
    url: "http://127.0.0.1:8000/docs",
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});