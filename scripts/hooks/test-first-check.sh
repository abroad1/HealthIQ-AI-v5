#!/bin/bash
# Test-First Development Enforcement Hook
# Ensures every implementation file has a corresponding test file

set -e

echo "🔍 Checking for test-first compliance..."

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=AM)

MISSING_TESTS=()

for file in $STAGED_FILES; do
  # Skip test files themselves
  if [[ $file == *".test."* ]] || [[ $file == *".spec."* ]] || [[ $file == *"test_"* ]]; then
    continue
  fi

  # Check backend Python files
  if [[ $file == backend/app/*.py ]] || [[ $file == backend/core/*.py ]] || [[ $file == backend/services/*.py ]]; then
    dir=$(dirname "$file")
    filename=$(basename "$file" .py)
    test_file="$dir/test_$filename.py"
    
    if [[ ! -f "$test_file" ]]; then
      MISSING_TESTS+=("$file -> $test_file")
    fi
  fi

  # Check frontend TypeScript files
  if [[ $file == frontend/app/services/*.ts ]] || [[ $file == frontend/app/state/*.ts ]] || [[ $file == frontend/app/components/*.tsx ]]; then
    dir=$(dirname "$file")
    filename=$(basename "$file" .ts)
    filename=$(basename "$filename" .tsx)
    test_file="$dir/$filename.test.ts"
    
    if [[ ! -f "$test_file" ]]; then
      MISSING_TESTS+=("$file -> $test_file")
    fi
  fi
done

# Report results
if [ ${#MISSING_TESTS[@]} -eq 0 ]; then
  echo "✅ All implementation files have corresponding test files"
  exit 0
else
  echo "❌ Missing test files for the following implementation files:"
  for missing in "${MISSING_TESTS[@]}"; do
    echo "  $missing"
  done
  echo ""
  echo "Please create the missing test files before committing."
  echo "Use templates in templates/tests/ for reference."
  exit 1
fi
