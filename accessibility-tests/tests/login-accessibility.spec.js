const { test, expect } = require('@playwright/test');
const { runAxeScan } = require('../helpers/axe-helper');

test.describe('Makanify Login Page Accessibility Audit', () => {
  test('login page should have no accessibility violations', async ({ page }) => {
    // Navigate to the target login page (baseURL is configured in playwright.config.js)
    await page.goto('/login', { waitUntil: 'networkidle' });

    // Wait for the form email input to ensure components are loaded
    await page.waitForSelector('#email', { state: 'visible' });
    // Run the accessibility scan using the reusable helper
    // Run the accessibility scan using the reusable helper
    await runAxeScan(page);
  });
});
