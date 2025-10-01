Write-Host "Sprint 9b Validation Started"

Set-Location "$PSScriptRoot\..\.."

Write-Host "Running database migration..."
Set-Location backend
alembic upgrade head

Write-Host "Backend: repository tests"
python -m pytest tests/unit/test_repositories.py -v
Write-Host "Backend: persistence service integration"
python -m pytest tests/integration/test_persistence_service.py -v
Write-Host "Backend: persistence E2E"
python -m pytest tests/e2e/test_persistence_e2e.py -v
Write-Host "Backend: export service + route"
python -m pytest tests/unit/test_export_service.py -v
python -m pytest tests/integration/test_export_route.py -v
Write-Host "Backend: DTO parity + error handling"
python -m pytest tests/unit/test_dto_parity.py -v
python -m pytest tests/integration/test_api_error_handling.py -v

Set-Location ../frontend

Write-Host "Frontend: persistence + history tests"
npm test -- analysis.test.ts
npm test -- useHistory.test.ts

Write-Host "Frontend: persistence E2E workflow"
npx playwright test persistence-pipeline.spec.ts

Write-Host "Sprint 9b Validation Complete - all tests executed"
