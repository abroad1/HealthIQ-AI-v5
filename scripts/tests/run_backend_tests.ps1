# HealthIQ AI v5 - Backend Test Runner (PowerShell)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

Write-Host "🧪 HealthIQ AI v5 - Backend Test Suite" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Change to backend directory
Set-Location -Path "backend"

Write-Host "`n📍 Running Backend Tests..." -ForegroundColor Yellow

# Run unit tests
Write-Host "`n🔬 Unit Tests:" -ForegroundColor Green
python -m pytest tests/unit/ -v --tb=short

# Run integration tests  
Write-Host "`n🔗 Integration Tests:" -ForegroundColor Green
python -m pytest tests/integration/ -v --tb=short

# Run E2E tests
Write-Host "`n🎯 E2E Tests:" -ForegroundColor Green
python -m pytest tests/e2e/ -v --tb=short

# Run enforcement tests
Write-Host "`n🛡️ Enforcement Tests:" -ForegroundColor Green
python -m pytest tests/enforcement/ -v --tb=short

# Run all tests with coverage
Write-Host "`n📊 All Tests with Coverage:" -ForegroundColor Green
python -m pytest tests/ -v --cov=app --cov=core --cov-report=term-missing --tb=short

Write-Host "`n✅ Backend Test Suite Complete!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan

# Return to root directory
Set-Location -Path ".."
