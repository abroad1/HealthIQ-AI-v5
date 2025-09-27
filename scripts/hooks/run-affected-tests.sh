#!/bin/bash
# Run Tests for Changed Files Hook
# Runs tests for files that were changed

set -e

echo "🧪 Running tests for changed files..."

# Get list of changed files
CHANGED_FILES="$@"

if [ -z "$CHANGED_FILES" ]; then
  echo "No files to test"
  exit 0
fi

# Track test results
TEST_FAILED=false

for file in $CHANGED_FILES; do
  echo "Testing $file..."
  
  # Skip test files themselves
  if [[ $file == *".test."* ]] || [[ $file == *".spec."* ]] || [[ $file == *"test_"* ]]; then
    continue
  fi

  # Run backend tests
  if [[ $file == backend/*.py ]]; then
    cd backend
    if ! python -m pytest tests/unit/ -v --tb=short; then
      TEST_FAILED=true
    fi
    cd ..
  fi

  # Run frontend tests
  if [[ $file == frontend/app/*.ts ]] || [[ $file == frontend/app/*.tsx ]]; then
    cd frontend
    if ! npm run test -- --watchAll=false; then
      TEST_FAILED=true
    fi
    cd ..
  fi
done

if [ "$TEST_FAILED" = true ]; then
  echo "❌ Some tests failed"
  exit 1
else
  echo "✅ All tests passed"
  exit 0
fi
