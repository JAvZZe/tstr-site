import { test, expect } from '@playwright/test';

test('simple test', async ({ page }) => {
    await page.goto('https://google.com');
    const title = await page.title();
    console.log('Title:', title);
    expect(title).toBeTruthy();
});
