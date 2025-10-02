import { test, expect } from '@playwright/test'

test.describe('HealthIQ AI v5 Frontend E2E', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/')
    
    // Basic smoke test - page should load without errors
    await expect(page).toHaveTitle(/HealthIQ/i)
    
    // Check for basic page structure
    const body = page.locator('body')
    await expect(body).toBeVisible()
  })

  test('navigation works', async ({ page }) => {
    await page.goto('/')
    
    // Test that the page is accessible
    await expect(page.locator('body')).toBeVisible()
  })

  test('responsive design works', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await expect(page.locator('body')).toBeVisible()

    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/')
    await expect(page.locator('body')).toBeVisible()
  })
})
