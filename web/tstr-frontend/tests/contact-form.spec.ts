import { test, expect } from '@playwright/test';

test.describe('Contact Form Auto-Selection', () => {

  test('should auto-select inquiry type from URL parameter', async ({ page }) => {
    // Navigate with query param
    await page.goto('http://localhost:4322/contact?inquiry=sales');
    
    // Wait for and check the select element
    const select = page.locator('select[name="inquiryType"]');
    await expect(select).toHaveValue('sales');
  });

  test('should pre-fill subject from URL parameter', async ({ page }) => {
    // Navigate with query param
    await page.goto('http://localhost:4322/contact?subject=Priority%20Support%20Request');
    
    // Wait for and check the textarea
    const textarea = page.locator('textarea[name="message"]');
    await expect(textarea).toHaveValue(/Subject: Priority Support Request/);
  });

  test('should handle invalid inquiry type parameter gracefully', async ({ page }) => {
    // Navigate with invalid query param
    await page.goto('http://localhost:4322/contact?inquiry=hacked_string');
    
    // Select should still be empty/default
    const select = page.locator('select[name="inquiryType"]');
    await expect(select).toHaveValue('');
  });

  test('should handle combination of inquiry and subject parameters', async ({ page }) => {
    // Navigate with query params
    await page.goto('http://localhost:4322/contact?inquiry=partnership&subject=Collaboration');
    
    // Verify both
    const select = page.locator('select[name="inquiryType"]');
    await expect(select).toHaveValue('partnership');
    
    const textarea = page.locator('textarea[name="message"]');
    await expect(textarea).toHaveValue(/Subject: Collaboration/);
  });

});
