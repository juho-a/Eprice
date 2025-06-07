const { test, expect } = require("@playwright/test");
const baseUrl = "http://localhost:5173";

test.describe("Authentication", () => {
    test("Shows error on login with invalid credentials", async ({ page }) => {
        await page.goto(`${baseUrl}/auth/login`);
        await page.fill('input[name="email"]', "notarealuser@example.com");
        await page.fill('input[name="password"]', "wrongpassword");
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
        await expect(page.locator("text=Incorrect email or password")).toBeVisible();
    });

    test("Registers a new user successfully and removes the account after", async ({ page }) => {
        const email = `testuser${Date.now()}@example.com`;
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Verification has been sent to your email")).toBeVisible();
        
        // remove the user after test to avoid conflicts
        await page.goto(`${baseUrl}/auth/remove`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(`${baseUrl}/logout?removed=true`);
        await expect(page.locator("text=Your account has been removed")).toBeVisible();
        // press the button to confirm account removal
        await page.click('button[type="submit"]');
        // you should be redirected to the home page
        await expect(page).toHaveURL(`${baseUrl}/`);
    });

    test("Shows error on register with existing email", async ({ page }) => {
        const existingEmail = "test@test.com";
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', existingEmail);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Email already registered.")).toBeVisible();
    });


    // This test assumes you have a verified user for login success
    test("Logs in successfully with valid credentials", async ({ page }) => {
        const email = "test@test.com";
        const password = "secret";
        await page.goto(`${baseUrl}/auth/login`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Welcome")).toBeVisible();
    });

    // after login successfully, the user's email should be visible via id user-info
    test("Shows user email after login", async ({ page }) => {
        const email = "test@test.com";
        const password = "secret";
        await page.goto(`${baseUrl}/auth/login`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        // Now check for the user info
        await expect(page.locator("#user-info")).toHaveText('Logged in as: test@test.com');
    });

    // This test assumes you have a verified user for logout success
    test("Logs out successfully", async ({ page }) => {
        const email = "test@test.com";
        const password = "secret";
        await page.goto(`${baseUrl}/auth/login`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await page.goto(`${baseUrl}/`);
        // expect logout-link id to be visible
        await expect(page.locator("#logout-link")).toBeVisible();
        // click the logout link
        await page.click('#logout-link');
        await expect(page).toHaveURL(`${baseUrl}/logout`);
        // press the button to confirm logout-button
        await page.click('button[type="submit"]');
        // expect redirect to home page
        await expect(page).toHaveURL(`${baseUrl}/`);
        // expect user-info to not be visible
        await expect(page.locator("#user-info")).toHaveCount(0);
    });

    test("Shows register prompt when not logged in", async ({ page }) => {
        await page.goto(`${baseUrl}/`);
        await page.waitForTimeout(1000);
        const prompt = page.locator("text=Want to see more features and get the full functionality of the app?");
        await expect(prompt).toBeVisible();
        const registerLink = page.locator("#register-link");
        await expect(registerLink).toBeVisible();
        await expect(registerLink).toHaveText(/Register/i);
    });
});