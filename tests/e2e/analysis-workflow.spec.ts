import { test, expect } from '@playwright/test';

test.describe('Health Analysis Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the upload page
    await page.goto('/upload');
  });

  test('complete biomarker analysis workflow', async ({ page }) => {
    // Test the complete user journey from upload to results
    
    // 1. Verify upload page loads
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
    await expect(page.getByText('Biomarker Data Entry')).toBeVisible();
    
    // 2. Add biomarker data
    await page.getByText('Add Biomarker').click();
    
    // Fill in glucose biomarker
    await page.getByDisplayValue('Select biomarker').selectOption('glucose');
    await page.getByDisplayValue('').fill('100');
    await page.getByDisplayValue('Select unit').selectOption('mg/dL');
    
    // Add another biomarker
    await page.getByText('Add Biomarker').click();
    
    // Fill in HbA1c biomarker
    const biomarkerSelects = page.getByDisplayValue('Select biomarker');
    await biomarkerSelects.nth(1).selectOption('hba1c');
    const valueInputs = page.getByDisplayValue('');
    await valueInputs.nth(1).fill('5.5');
    const unitSelects = page.getByDisplayValue('Select unit');
    await unitSelects.nth(1).selectOption('%');
    
    // 3. Submit the analysis
    await page.getByText('Submit 2 Biomarkers').click();
    
    // 4. Verify success state
    await expect(page.getByText('Analysis Started!')).toBeVisible();
    await expect(page.getByText('Your health analysis is being processed')).toBeVisible();
    
    // 5. Wait for redirect to results page
    await page.waitForURL('/results', { timeout: 10000 });
    
    // 6. Verify results page loads
    await expect(page.getByText('Your Health Analysis Results')).toBeVisible();
    await expect(page.getByText('Overall Health Score')).toBeVisible();
    
    // 7. Check biomarker dials are displayed
    await expect(page.getByText('Biomarker Analysis')).toBeVisible();
    await expect(page.getByText('Glucose')).toBeVisible();
    await expect(page.getByText('HbA1c')).toBeVisible();
    
    // 8. Check health clusters tab
    await page.getByText('Health Clusters').click();
    await expect(page.getByText('Health Clusters')).toBeVisible();
    
    // 9. Check AI insights tab
    await page.getByText('AI Insights').click();
    await expect(page.getByText('Health Insights')).toBeVisible();
  });

  test('questionnaire analysis workflow', async ({ page }) => {
    // Test questionnaire-based analysis
    
    // 1. Switch to questionnaire tab
    await page.getByText('Health Questionnaire').click();
    
    // 2. Fill out questionnaire form
    await page.getByLabel('Full Name').fill('John Doe');
    await page.getByLabel('Email Address').fill('john@example.com');
    await page.getByLabel('Phone Number').fill('555-1234');
    await page.getByDisplayValue('Select an option').selectOption('United States');
    await page.getByLabel('Date of Birth').fill('1990-01-01');
    await page.getByDisplayValue('Select an option').nth(1).selectOption('Male');
    
    // Fill height
    await page.getByLabel('Feet').fill('6');
    await page.getByLabel('Inches').fill('0');
    
    // Fill weight
    await page.getByLabel('Weight (lbs)').fill('180');
    
    // Fill lifestyle questions
    await page.getByDisplayValue('Select an option').nth(2).selectOption('7-8 hours');
    await page.getByDisplayValue('Select an option').nth(3).selectOption('None');
    await page.getByDisplayValue('Select an option').nth(4).selectOption('Never used');
    
    // 3. Submit questionnaire
    await page.getByText('Complete Assessment').click();
    
    // 4. Verify success and redirect
    await expect(page.getByText('Analysis Started!')).toBeVisible();
    await page.waitForURL('/results', { timeout: 10000 });
    
    // 5. Verify results page
    await expect(page.getByText('Your Health Analysis Results')).toBeVisible();
  });

  test('combined analysis workflow', async ({ page }) => {
    // Test combined biomarker + questionnaire analysis
    
    // 1. Switch to combined analysis tab
    await page.getByText('Combined Analysis').click();
    
    // 2. Add biomarker data (Step 1)
    await page.getByText('Add Biomarker').click();
    await page.getByDisplayValue('Select biomarker').selectOption('glucose');
    await page.getByDisplayValue('').fill('100');
    await page.getByDisplayValue('Select unit').selectOption('mg/dL');
    
    // Proceed to questionnaire
    await page.getByText('Next').click();
    
    // 3. Fill questionnaire (Step 2)
    await page.getByLabel('Full Name').fill('Jane Doe');
    await page.getByLabel('Email Address').fill('jane@example.com');
    await page.getByLabel('Phone Number').fill('555-5678');
    await page.getByDisplayValue('Select an option').selectOption('United States');
    await page.getByLabel('Date of Birth').fill('1985-05-15');
    await page.getByDisplayValue('Select an option').nth(1).selectOption('Female');
    
    // Fill height and weight
    await page.getByLabel('Feet').fill('5');
    await page.getByLabel('Inches').fill('6');
    await page.getByLabel('Weight (lbs)').fill('140');
    
    // Fill lifestyle questions
    await page.getByDisplayValue('Select an option').nth(2).selectOption('7-8 hours');
    await page.getByDisplayValue('Select an option').nth(3).selectOption('None');
    await page.getByDisplayValue('Select an option').nth(4).selectOption('Never used');
    
    // Proceed to review
    await page.getByText('Complete Assessment').click();
    
    // 4. Review and submit (Step 3)
    await expect(page.getByText('Review and Submit')).toBeVisible();
    await expect(page.getByText('1 biomarkers entered')).toBeVisible();
    await expect(page.getByText('Health questionnaire completed')).toBeVisible();
    
    await page.getByText('Start Combined Analysis').click();
    
    // 5. Verify success and redirect
    await expect(page.getByText('Analysis Started!')).toBeVisible();
    await page.waitForURL('/results', { timeout: 10000 });
    
    // 6. Verify results page
    await expect(page.getByText('Your Health Analysis Results')).toBeVisible();
  });

  test('CSV upload functionality', async ({ page }) => {
    // Test CSV file upload
    
    // 1. Switch to CSV upload tab
    await page.getByText('CSV Upload').click();
    
    // 2. Create a test CSV file
    const csvContent = 'glucose,100,mg/dL,2024-01-01\nhba1c,5.5,%,2024-01-01\ntotal_cholesterol,220,mg/dL,2024-01-01';
    
    // 3. Upload the CSV file
    const fileInput = page.getByLabel('Choose CSV File');
    await fileInput.setInputFiles({
      name: 'test-biomarkers.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent)
    });
    
    // 4. Verify CSV was processed
    await expect(page.getByText('CSV file processed. 3 biomarkers loaded.')).toBeVisible();
    
    // 5. Submit the analysis
    await page.getByText('Submit 3 Biomarkers').click();
    
    // 6. Verify success and redirect
    await expect(page.getByText('Analysis Started!')).toBeVisible();
    await page.waitForURL('/results', { timeout: 10000 });
    
    // 7. Verify results page shows uploaded data
    await expect(page.getByText('Your Health Analysis Results')).toBeVisible();
    await expect(page.getByText('Glucose')).toBeVisible();
    await expect(page.getByText('HbA1c')).toBeVisible();
    await expect(page.getByText('Total Cholesterol')).toBeVisible();
  });

  test('results page functionality', async ({ page }) => {
    // Navigate directly to results page (assuming analysis exists)
    await page.goto('/results');
    
    // 1. Verify results page loads
    await expect(page.getByText('Your Health Analysis Results')).toBeVisible();
    
    // 2. Test tab navigation
    await page.getByText('Biomarkers').click();
    await expect(page.getByText('Biomarker Analysis')).toBeVisible();
    
    await page.getByText('Health Clusters').click();
    await expect(page.getByText('Health Clusters')).toBeVisible();
    
    await page.getByText('AI Insights').click();
    await expect(page.getByText('Health Insights')).toBeVisible();
    
    // 3. Test show/hide details toggle
    await page.getByText('Show Details').click();
    await expect(page.getByText('Hide Details')).toBeVisible();
    
    await page.getByText('Hide Details').click();
    await expect(page.getByText('Show Details')).toBeVisible();
    
    // 4. Test export functionality
    await page.getByText('Export').click();
    // Note: In a real test, you'd verify the file download
    
    // 5. Test new analysis button
    await page.getByText('Start New Analysis').click();
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
  });

  test('error handling', async ({ page }) => {
    // Test error states and handling
    
    // 1. Try to submit empty form
    await page.getByText('Submit 0 Biomarkers').click();
    // Should not submit (button should be disabled)
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
    
    // 2. Add biomarker but don't fill required fields
    await page.getByText('Add Biomarker').click();
    await page.getByText('Submit 1 Biomarkers').click();
    // Should show validation errors
    await expect(page.getByText('Please select a biomarker')).toBeVisible();
    
    // 3. Navigate to results without analysis
    await page.goto('/results');
    await expect(page.getByText('No Analysis Found')).toBeVisible();
    await expect(page.getByText('Please complete an analysis first')).toBeVisible();
  });

  test('responsive design', async ({ page }) => {
    // Test responsive behavior on different screen sizes
    
    // 1. Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/upload');
    
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
    await expect(page.getByText('Biomarker Data Entry')).toBeVisible();
    
    // 2. Test tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
    
    // 3. Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.reload();
    
    await expect(page.getByText('Health Analysis Upload')).toBeVisible();
  });
});
