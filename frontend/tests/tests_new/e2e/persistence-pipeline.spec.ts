import { test, expect } from '@playwright/test';

test.describe('Persistence Pipeline E2E', () => {
  test('should complete full analysis pipeline with persistence', async ({ page }) => {
    // Navigate to the analysis page
    await page.goto('/');

    // Wait for the page to load
    await expect(page.locator('h1')).toContainText('HealthIQ AI');

    // Mock the analysis API responses
    await page.route('**/api/analysis/start', async (route) => {
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          analysis_id: analysisId,
          status: 'completed',
          result_version: '1.0.0',
          biomarkers: [
            {
              biomarker_name: 'glucose',
              value: 95.0,
              unit: 'mg/dL',
              score: 0.75,
              percentile: 65.0,
              status: 'normal',
              reference_range: { min: 70, max: 100 },
              interpretation: 'Within normal range',
              confidence: 0.9,
              health_system: 'metabolic',
              critical_flag: false
            }
          ],
          clusters: [
            {
              id: '456e7890-e89b-12d3-a456-426614174001',
              name: 'metabolic',
              biomarkers: ['glucose'],
              description: 'Metabolic health cluster',
              severity: 'normal',
              confidence: 0.9
            }
          ],
          insights: [
            {
              id: '789e0123-e89b-12d3-a456-426614174002',
              title: 'Good glucose control',
              content: 'Your glucose levels are well controlled',
              category: 'metabolic',
              confidence: 0.9,
              severity: 'normal',
              biomarkers_involved: ['glucose'],
              recommendations: ['Continue current diet']
            }
          ],
          recommendations: ['Continue current diet'],
          overall_score: 0.85,
          meta: {
            result_version: '1.0.0',
            confidence_score: 0.9,
            processing_metadata: { test: 'data' }
          },
          created_at: new Date().toISOString()
        })
      });
    });

    // Mock the history API response
    await page.route('**/api/analysis/history*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          analyses: [
            {
              analysis_id: '123e4567-e89b-12d3-a456-426614174000',
              created_at: new Date().toISOString(),
              overall_score: 0.85,
              status: 'completed',
              processing_time_seconds: 5.0
            }
          ],
          total: 1,
          limit: 10,
          offset: 0
        })
      });
    });

    // Mock the result API response
    await page.route('**/api/analysis/result*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          analysis_id: '123e4567-e89b-12d3-a456-426614174000',
          result_version: '1.0.0',
          biomarkers: [
            {
              biomarker_name: 'glucose',
              value: 95.0,
              unit: 'mg/dL',
              score: 0.75,
              percentile: 65.0,
              status: 'normal',
              reference_range: { min: 70, max: 100 },
              interpretation: 'Within normal range',
              confidence: 0.9,
              health_system: 'metabolic',
              critical_flag: false
            }
          ],
          clusters: [
            {
              id: '456e7890-e89b-12d3-a456-426614174001',
              name: 'metabolic',
              biomarkers: ['glucose'],
              description: 'Metabolic health cluster',
              severity: 'normal',
              confidence: 0.9
            }
          ],
          insights: [
            {
              id: '789e0123-e89b-12d3-a456-426614174002',
              title: 'Good glucose control',
              content: 'Your glucose levels are well controlled',
              category: 'metabolic',
              confidence: 0.9,
              severity: 'normal',
              biomarkers_involved: ['glucose'],
              recommendations: ['Continue current diet']
            }
          ],
          recommendations: ['Continue current diet'],
          overall_score: 0.85,
          meta: {
            result_version: '1.0.0',
            confidence_score: 0.9,
            processing_metadata: { test: 'data' }
          },
          created_at: new Date().toISOString()
        })
      });
    });

    // Mock the export API response
    await page.route('**/api/analysis/export', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          export_id: '789e0123-e89b-12d3-a456-426614174002',
          status: 'pending',
          message: 'Export request submitted successfully'
        })
      });
    });

    // Step 1: Start analysis
    await page.click('button:has-text("Start Analysis")');
    
    // Wait for analysis to complete
    await expect(page.locator('text=Analysis completed')).toBeVisible({ timeout: 10000 });

    // Step 2: Check that results are displayed
    await expect(page.locator('text=Good glucose control')).toBeVisible();
    await expect(page.locator('text=Overall Score: 85%')).toBeVisible();

    // Step 3: Navigate to history (if there's a history button)
    const historyButton = page.locator('button:has-text("History")');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      
      // Wait for history to load
      await expect(page.locator('text=Analysis History')).toBeVisible();
      
      // Check that the analysis appears in history
      await expect(page.locator('text=123e4567-e89b-12d3-a456-426614174000')).toBeVisible();
      await expect(page.locator('text=85%')).toBeVisible();
    }

    // Step 4: Test result retrieval (if there's a view result button)
    const viewResultButton = page.locator('button:has-text("View Result")');
    if (await viewResultButton.isVisible()) {
      await viewResultButton.click();
      
      // Wait for result to load
      await expect(page.locator('text=Analysis Result')).toBeVisible();
      
      // Check that the result details are displayed
      await expect(page.locator('text=Good glucose control')).toBeVisible();
      await expect(page.locator('text=Overall Score: 85%')).toBeVisible();
    }

    // Step 5: Test export (if there's an export button)
    const exportButton = page.locator('button:has-text("Export")');
    if (await exportButton.isVisible()) {
      await exportButton.click();
      
      // Wait for export to complete
      await expect(page.locator('text=Export request submitted successfully')).toBeVisible();
    }

    // Verify that all API calls were made
    const requests = [];
    page.on('request', request => {
      if (request.url().includes('/api/analysis/')) {
        requests.push(request.url());
      }
    });

    // Check that the analysis was persisted by verifying API calls
    expect(requests).toContain(expect.stringContaining('/api/analysis/start'));
    expect(requests).toContain(expect.stringContaining('/api/analysis/history'));
    expect(requests).toContain(expect.stringContaining('/api/analysis/result'));
    expect(requests).toContain(expect.stringContaining('/api/analysis/export'));
  });

  test('should handle persistence failures gracefully', async ({ page }) => {
    // Navigate to the analysis page
    await page.goto('/');

    // Mock the analysis API to return an error
    await page.route('**/api/analysis/start', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          error: 'Internal server error',
          message: 'Failed to persist analysis'
        })
      });
    });

    // Start analysis
    await page.click('button:has-text("Start Analysis")');
    
    // Wait for error message
    await expect(page.locator('text=Failed to persist analysis')).toBeVisible({ timeout: 10000 });

    // Verify that the error is displayed to the user
    await expect(page.locator('text=Error')).toBeVisible();
  });

  test('should handle history API failures', async ({ page }) => {
    // Navigate to the analysis page
    await page.goto('/');

    // Mock successful analysis start
    await page.route('**/api/analysis/start', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          analysis_id: '123e4567-e89b-12d3-a456-426614174000',
          status: 'completed',
          result_version: '1.0.0',
          biomarkers: [],
          clusters: [],
          insights: [],
          recommendations: [],
          overall_score: 0.85,
          meta: {},
          created_at: new Date().toISOString()
        })
      });
    });

    // Mock history API to return an error
    await page.route('**/api/analysis/history*', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          error: 'Internal server error',
          message: 'Failed to fetch analysis history'
        })
      });
    });

    // Start analysis
    await page.click('button:has-text("Start Analysis")');
    
    // Wait for analysis to complete
    await expect(page.locator('text=Analysis completed')).toBeVisible({ timeout: 10000 });

    // Try to access history
    const historyButton = page.locator('button:has-text("History")');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      
      // Wait for error message
      await expect(page.locator('text=Failed to fetch analysis history')).toBeVisible();
    }
  });
});
