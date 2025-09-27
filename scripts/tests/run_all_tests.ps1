# HealthIQ AI v5 - Complete Test Suite Runner (PowerShell)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

Write-Host "🧪 HealthIQ AI v5 - Complete Test Suite" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta

$startTime = Get-Date

# Run backend tests
Write-Host "`n🔧 Running Backend Tests..." -ForegroundColor Yellow
& "$PSScriptRoot\run_backend_tests.ps1"

# Run frontend tests
Write-Host "`n🎨 Running Frontend Tests..." -ForegroundColor Yellow
& "$PSScriptRoot\run_frontend_tests.ps1"

# Run E2E tests
Write-Host "`n🎯 Running E2E Tests..." -ForegroundColor Yellow
& "$PSScriptRoot\run_e2e_tests.ps1"

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n🎉 Complete Test Suite Finished!" -ForegroundColor Green
Write-Host "⏱️ Total Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Magenta
