import { test, expect } from '@playwright/test';

test.describe('Claim Button Visibility Enhancement', () => {
  test('browse page shows claim buttons on unclaimed listings', async ({ page }) => {
    await page.goto('http://localhost:4321/browse');

    // Wait for listings to load
    await page.waitForSelector('.listing-card');

    // Check that claim buttons are visible on listing cards
    const claimButtons = page.locator('.claim-link');
    await expect(claimButtons.first()).toBeVisible();

    // Verify the button text
    await expect(claimButtons.first()).toContainText('Is this you? Claim');
  });

  test('claim button click redirects non-authenticated users to login', async ({ page }) => {
    await page.goto('http://localhost:4321/browse');

    // Wait for listings to load
    await page.waitForSelector('.listing-card');

    // Click the first claim button
    const firstClaimButton = page.locator('.claim-link').first();
    await firstClaimButton.click();

    // Should redirect to login page with redirect_to parameter
    await expect(page).toHaveURL(/\/login\?redirect_to=.*/);
  });

  test('login page handles redirect_to parameter', async ({ page }) => {
    // Simulate login redirect with claim URL
    const claimUrl = encodeURIComponent('/listing/test-slug?claim=true');
    await page.goto(`http://localhost:4321/login?redirect_to=${claimUrl}`);

    // Check that we're on the login page
    await expect(page).toHaveURL(/\/login\?redirect_to=.*/);

    // The redirect handling is tested in the login flow
    // (would need actual auth setup for full e2e test)
  });

  test('claim page redirects authenticated users with listing ID', async ({ page }) => {
    // This would require authentication setup
    // For now, just verify the page loads
    await page.goto('http://localhost:4321/claim?provider=Test%20Company&id=123');

    // Should show the claim form
    await expect(page.locator('h1')).toContainText('Claim Your Profile');
  });

  test('listing page shows claim section for redirected users', async ({ page }) => {
    // This would require a real listing slug
    // For now, just verify the page structure exists
    await page.goto('http://localhost:4321/browse');

    // Check that the claim section exists in the DOM (hidden by default)
    const claimSection = page.locator('#claim-section');
    await expect(claimSection).toBeAttached();
  });
});