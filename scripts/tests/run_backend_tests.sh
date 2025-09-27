#!/bin/bash
# HealthIQ AI v5 - Backend Test Runner (Bash)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

echo "🧪 HealthIQ AI v5 - Backend Test Suite"
echo "======================================="

# Change to backend directory
cd backend

echo ""
echo "📍 Running Backend Tests..."

# Run unit tests
echo ""
echo "🔬 Unit Tests:"
python -m pytest tests/unit/ -v --tb=short

# Run integration tests  
echo ""
echo "🔗 Integration Tests:"
python -m pytest tests/integration/ -v --tb=short

# Run E2E tests
echo ""
echo "🎯 E2E Tests:"
python -m pytest tests/e2e/ -v --tb=short

# Run enforcement tests
echo ""
echo "🛡️ Enforcement Tests:"
python -m pytest tests/enforcement/ -v --tb=short

# Run all tests with coverage
echo ""
echo "📊 All Tests with Coverage:"
python -m pytest tests/ -v --cov=app --cov=core --cov-report=term-missing --tb=short

echo ""
echo "✅ Backend Test Suite Complete!"
echo "======================================="

# Return to root directory
cd ..
