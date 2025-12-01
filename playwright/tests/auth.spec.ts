import { test, expect } from "@playwright/test";

const TEST_PASSWORD = "SuperSecret1";

test("Positive: register with valid data", async ({ page }) => {
  const now = Date.now();
  const email = `user_${now}@example.com`;
  const username = `user_${now}`;

  await page.goto("/static/register.html");

  await page.fill("#username", username);
  await page.fill("#email", email);
  await page.fill("#password", TEST_PASSWORD);
  await page.fill("#confirmPassword", TEST_PASSWORD);

  await page.click("button[type=submit]");

  await expect(page.locator("#message")).toHaveText("Registration successful!");
});

test("Positive: login with correct credentials", async ({ page }) => {
  const now = Date.now();
  const email = `login_${now}@example.com`;
  const username = `login_${now}`;

  // First create the user via API
  const res = await page.request.post("/auth/register", {
    data: {
      username,
      email,
      password: TEST_PASSWORD,
    },
  });
  expect(res.ok()).toBeTruthy();

  await page.goto("/static/login.html");

  await page.fill("#email", email);
  await page.fill("#password", TEST_PASSWORD);
  await page.click("button[type=submit]");

  await expect(page.locator("#message")).toContainText("Login successful");

  const token = await page.evaluate(() => localStorage.getItem("jwt"));
  expect(token).not.toBeNull();
});

test("Negative: register with short password shows front-end error", async ({ page }) => {
  const now = Date.now();
  const email = `short_${now}@example.com`;
  const username = `short_${now}`;

  await page.goto("/static/register.html");

  await page.fill("#username", username);
  await page.fill("#email", email);
  await page.fill("#password", "123");
  await page.fill("#confirmPassword", "123");

  await page.click("button[type=submit]");

  await expect(page.locator("#message")).toHaveText(
    "Password must be at least 8 characters."
  );
});

test("Negative: login with wrong password shows invalid credentials", async ({ page }) => {
  const now = Date.now();
  const email = `wrong_${now}@example.com`;
  const username = `wrong_${now}`;

  // Create user with correct password
  const res = await page.request.post("/auth/register", {
    data: {
      username,
      email,
      password: TEST_PASSWORD,
    },
  });
  expect(res.ok()).toBeTruthy();

  await page.goto("/static/login.html");

  await page.fill("#email", email);
  await page.fill("#password", "WrongPassword1");
  await page.click("button[type=submit]");

  await expect(page.locator("#message")).toContainText("Invalid email or password");
});