# HealthIQ AI v5 - E2E Test Runner (PowerShell)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

Write-Host "🧪 HealthIQ AI v5 - E2E Test Suite" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Change to frontend directory (Playwright tests are here)
Set-Location -Path "frontend"

Write-Host "`n📍 Running E2E Tests..." -ForegroundColor Yellow

# Install Playwright browsers if not already installed
Write-Host "`n🌐 Ensuring Playwright Browsers are Installed:" -ForegroundColor Green
npx playwright install

# Run Playwright tests in headed mode (visible browser)
Write-Host "`n🎯 Playwright E2E Tests (Headed):" -ForegroundColor Green
npx playwright test --headed

# Run Playwright tests in headless mode (faster)
Write-Host "`n🎯 Playwright E2E Tests (Headless):" -ForegroundColor Green
npx playwright test

# Run Playwright tests with UI mode (interactive)
Write-Host "`n🎯 Playwright E2E Tests (UI Mode - Interactive):" -ForegroundColor Green
Write-Host "   Note: UI mode opens interactive test runner" -ForegroundColor Yellow
# npx playwright test --ui  # Uncomment to run interactive mode

Write-Host "`n✅ E2E Test Suite Complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan

# Return to root directory
Set-Location -Path ".."
