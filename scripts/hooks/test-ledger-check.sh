#!/bin/bash
# TEST_LEDGER.md Update Check Hook
# Ensures TEST_LEDGER.md is updated when code changes are made

set -e

echo "📝 Checking TEST_LEDGER.md update..."

# Check if any non-test files were changed
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=AM | grep -E "\.(py|ts|tsx)$" | grep -v -E "(test|spec)")

if [ -z "$CHANGED_FILES" ]; then
  echo "✅ No implementation files changed, skipping TEST_LEDGER.md check"
  exit 0
fi

# Check if TEST_LEDGER.md was updated
if git diff --cached --name-only | grep -q "TEST_LEDGER.md"; then
  echo "✅ TEST_LEDGER.md was updated"
  exit 0
else
  echo "❌ TEST_LEDGER.md was not updated for code changes"
  echo "Changed files:"
  echo "$CHANGED_FILES"
  echo ""
  echo "Please update TEST_LEDGER.md with test results before committing."
  exit 1
fi
