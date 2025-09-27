#!/bin/bash
# HealthIQ AI v5 - E2E Test Runner (Bash)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

echo "🧪 HealthIQ AI v5 - E2E Test Suite"
echo "===================================="

# Change to frontend directory (Playwright tests are here)
cd frontend

echo ""
echo "📍 Running E2E Tests..."

# Install Playwright browsers if not already installed
echo ""
echo "🌐 Ensuring Playwright Browsers are Installed:"
npx playwright install

# Run Playwright tests in headed mode (visible browser)
echo ""
echo "🎯 Playwright E2E Tests (Headed):"
npx playwright test --headed

# Run Playwright tests in headless mode (faster)
echo ""
echo "🎯 Playwright E2E Tests (Headless):"
npx playwright test

# Run Playwright tests with UI mode (interactive)
echo ""
echo "🎯 Playwright E2E Tests (UI Mode - Interactive):"
echo "   Note: UI mode opens interactive test runner"
# npx playwright test --ui  # Uncomment to run interactive mode

echo ""
echo "✅ E2E Test Suite Complete!"
echo "===================================="

# Return to root directory
cd ..
