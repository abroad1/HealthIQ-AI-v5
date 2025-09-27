#!/bin/bash
# HealthIQ AI v5 - Frontend Test Runner (Bash)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

echo "🧪 HealthIQ AI v5 - Frontend Test Suite"
echo "========================================"

# Change to frontend directory
cd frontend

echo ""
echo "📍 Running Frontend Tests..."

# Run Jest unit tests
echo ""
echo "🔬 Jest Unit Tests:"
npm test

# Run Jest tests with coverage
echo ""
echo "📊 Jest Tests with Coverage:"
npm run test:coverage

# Run type checking
echo ""
echo "🔍 TypeScript Type Checking:"
npm run type-check

# Run linting
echo ""
echo "🧹 ESLint Linting:"
npm run lint

echo ""
echo "✅ Frontend Test Suite Complete!"
echo "========================================"

# Return to root directory
cd ..
