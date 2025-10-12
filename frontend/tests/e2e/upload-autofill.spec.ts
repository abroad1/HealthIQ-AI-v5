import { test, expect } from '@playwright/test';

test('Auto-populate questionnaire and reach results', async ({ page }) => {
  await page.goto('/upload?autofill=true');
  
  // Wait for mock biomarkers to load
  await page.waitForTimeout(1000);
  
  // Verify mock biomarkers are loaded
  await expect(page.getByText(/Review Parsed Results/i)).toBeVisible({ timeout: 5000 });
  
  // Click "Confirm All" button to confirm biomarkers
  await page.getByRole('button', { name: /confirm all/i }).click();
  
  // Wait for questionnaire to appear
  await page.waitForTimeout(1000);
  
  // Verify questionnaire form is visible
  await expect(page.getByText(/Health Assessment Questionnaire/i)).toBeVisible({ timeout: 5000 });
  
  // Verify email field is auto-filled
  const emailInput = page.getByRole('textbox', { name: /email/i });
  await expect(emailInput).toHaveValue('test@example.com', { timeout: 5000 });
  
  // Submit the questionnaire
  await page.getByRole('button', { name: /complete assessment/i }).click();
  
  // Wait for navigation to results
  await page.waitForURL(/results/, { timeout: 10000 });
  
  // Verify we're on results page
  expect(page.url()).toContain('/results');
});

test('Mock biomarkers are displayed when autofill=true', async ({ page }) => {
  await page.goto('/upload?autofill=true');
  
  // Wait for mock biomarkers to load
  await page.waitForTimeout(1000);
  
  // Verify biomarkers table is visible
  await expect(page.getByText(/Review Parsed Results/i)).toBeVisible({ timeout: 5000 });
  
  // Verify specific biomarkers are present
  await expect(page.getByText(/glucose/i)).toBeVisible();
  await expect(page.getByText(/hdl/i)).toBeVisible();
  await expect(page.getByText(/ldl/i)).toBeVisible();
  await expect(page.getByText(/triglycerides/i)).toBeVisible();
});

test('Questionnaire form is pre-filled when autofill=true', async ({ page }) => {
  await page.goto('/upload?autofill=true');
  
  // Wait for mock biomarkers to load
  await page.waitForTimeout(1000);
  
  // Confirm biomarkers
  await page.getByRole('button', { name: /confirm all/i }).click();
  
  // Wait for questionnaire to appear
  await page.waitForTimeout(1000);
  
  // Verify Demographics fields are pre-filled
  const nameInput = page.getByRole('textbox', { name: /full name/i });
  await expect(nameInput).toHaveValue('John Smith', { timeout: 5000 });
  
  const emailInput = page.getByRole('textbox', { name: /email/i });
  await expect(emailInput).toHaveValue('test@example.com', { timeout: 5000 });
  
  const phoneInput = page.getByRole('textbox', { name: /phone/i });
  await expect(phoneInput).toHaveValue('07123456789', { timeout: 5000 });
  
  // Verify date of birth is filled
  const dobInput = page.locator('input[type="date"]').first();
  await expect(dobInput).toHaveValue('1978-05-15', { timeout: 5000 });
  
  // Verify weight is filled
  const weightInput = page.getByRole('spinbutton', { name: /weight/i });
  await expect(weightInput).toHaveValue('165', { timeout: 5000 });
});

