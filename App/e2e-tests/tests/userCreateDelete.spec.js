const { test, expect } = require('@playwright/test');
const fetch = require('node-fetch');

test.describe('User Creation and Deletion', () => {
    let email;
    let password;
    let mailToken;

    test.beforeAll(async () => {
        // Create temp account
        const domainRes = await fetch('https://api.mail.tm/domains');
        const domainData = await domainRes.json();
        const domain = domainData['hydra:member'][0].domain;
        username = `test${Date.now()}@${domain}`;

        await fetch('https://api.mail.tm/accounts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: email, password }),
        });

        // Get mail.tm token for fetching emails
        const tokenRes = await fetch('https://api.mail.tm/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: email, password }),
        });
        const tokenData = await tokenRes.json();
        mailToken = tokenData.token;
        });

    test('Register user', async ({ page }) => {
        await page.goto('http://localhost:5173/auth/register');
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Verification has been sent to your email. Please verify your account to continue.')).toBeVisible();
    });

    test('Verify user', async ({ page }) => {
        // 4. Poll for verification email and extract link
        let verificationLink;
        for (let i = 0; i < 10; i++) {
            await new Promise(r => setTimeout(r, 2000));
            const messagesRes = await fetch('https://api.mail.tm/messages', {
                headers: { Authorization: `Bearer ${mailToken}` },
            });
            const messages = await messagesRes.json();
            if (messages['hydra:member'].length > 0) {
                const msgId = messages['hydra:member'][0].id;
                const msgRes = await fetch(`https://api.mail.tm/messages/${msgId}`, {
                    headers: { Authorization: `Bearer ${mailToken}` },
                });
                const msg = await msgRes.json();
                // Extract the verification link (adjust regex if needed)
                const match = msg.text.match(/http:\/\/localhost:5173\/auth\/verify\?email=[^&]+&code=[A-Z0-9-]+/);
                if (match) {
                    verificationLink = match[0];
                    break;
                }
            }
        }
        expect(verificationLink).toBeTruthy();


        // 5. Visit the verification link
        await page.goto(verificationLink);

        // 6. Click the verify button
        const verifyButton = page.locator('button[type="submit"]');
        await verifyButton.click();

         // 7. Check verification success message and the URL
        await expect(page.locator('text=Your email has been verified. You can now login.')).toBeVisible();
        await expect(page).toHaveURL(/\/auth\/login\?is_verified=true/);

    });

    test('Login user', async ({ page }) => {
        await page.goto('http://localhost:5173/auth/login');
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await expect(page.locator(`Logged in as: ${email}`)).toBeVisible();
        
    });

    test('Remove user', async ({ page }) => {
        await page.goto('http://localhost:5173/auth/remove');
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', password);
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Your account has been removed.')).toBeVisible();
        await page.click('button[type="submit"]');
    });

});

