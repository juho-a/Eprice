const { test, expect } = require("@playwright/test");

test('Home page loads successfully', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  // Check if the page title is correct
  await expect(page).toHaveTitle("Home - Market Electricity Prices Today");
});

test('Home page has the chart visible.', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  // wait for a second for the page to load
  await page.waitForTimeout(1000);
  const canvas = page.locator("#priceChart");
  await expect(canvas).toBeVisible();
});
