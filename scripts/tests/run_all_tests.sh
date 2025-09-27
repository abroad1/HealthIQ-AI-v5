#!/bin/bash
# HealthIQ AI v5 - Complete Test Suite Runner (Bash)
# Created: 2025-01-27 - Sprint 1-2 Prerequisites Implementation

echo "🧪 HealthIQ AI v5 - Complete Test Suite"
echo "========================================="

start_time=$(date +%s)

# Run backend tests
echo ""
echo "🔧 Running Backend Tests..."
bash "$(dirname "$0")/run_backend_tests.sh"

# Run frontend tests
echo ""
echo "🎨 Running Frontend Tests..."
bash "$(dirname "$0")/run_frontend_tests.sh"

# Run E2E tests
echo ""
echo "🎯 Running E2E Tests..."
bash "$(dirname "$0")/run_e2e_tests.sh"

end_time=$(date +%s)
duration=$((end_time - start_time))

echo ""
echo "🎉 Complete Test Suite Finished!"
echo "⏱️ Total Duration: $(printf '%02d:%02d:%02d' $((duration/3600)) $((duration%3600/60)) $((duration%60)))"
echo "========================================="
