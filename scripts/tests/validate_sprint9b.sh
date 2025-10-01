#!/usr/bin/env bash
set -euo pipefail

echo "Sprint 9b Validation Started"

cd "$(dirname "$0")/../.."

echo "Running database migration..."
cd backend
alembic upgrade head

echo "Backend: repository tests"
python -m pytest tests/unit/test_repositories.py -v

echo "Backend: persistence service integration"
python -m pytest tests/integration/test_persistence_service.py -v

echo "Backend: persistence E2E"
python -m pytest tests/e2e/test_persistence_e2e.py -v

echo "Backend: export service + route"
python -m pytest tests/unit/test_export_service.py -v
python -m pytest tests/integration/test_export_route.py -v

echo "Backend: DTO parity + error handling"
python -m pytest tests/unit/test_dto_parity.py -v
python -m pytest tests/integration/test_api_error_handling.py -v

cd ../frontend

echo "Frontend: persistence + history tests"
npm test -- analysis.test.ts
npm test -- useHistory.test.ts

echo "Frontend: persistence E2E workflow"
npx playwright test persistence-pipeline.spec.ts

echo "Sprint 9b Validation Complete - all tests executed"
