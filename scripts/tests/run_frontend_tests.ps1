# HealthIQ AI v5 - Frontend Test Runner (PowerShell)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

Write-Host "🧪 HealthIQ AI v5 - Frontend Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Change to frontend directory
Set-Location -Path "frontend"

Write-Host "`n📍 Running Frontend Tests..." -ForegroundColor Yellow

# Run Jest unit tests
Write-Host "`n🔬 Jest Unit Tests:" -ForegroundColor Green
npm test

# Run Jest tests with coverage
Write-Host "`n📊 Jest Tests with Coverage:" -ForegroundColor Green
npm run test:coverage

# Run type checking
Write-Host "`n🔍 TypeScript Type Checking:" -ForegroundColor Green
npm run type-check

# Run linting
Write-Host "`n🧹 ESLint Linting:" -ForegroundColor Green
npm run lint

Write-Host "`n✅ Frontend Test Suite Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Return to root directory
Set-Location -Path ".."
