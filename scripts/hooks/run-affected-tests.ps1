# Run Tests for Changed Files Hook (PowerShell)
# Runs tests for files that were changed

Write-Host "🧪 Running tests for changed files..." -ForegroundColor Cyan

# Get list of changed files from arguments
$changedFiles = $args

if (-not $changedFiles) {
    Write-Host "No files to test" -ForegroundColor Yellow
    exit 0
}

# Track test results
$testFailed = $false

foreach ($file in $changedFiles) {
    Write-Host "Testing $file..." -ForegroundColor Cyan
    
    # Skip test files themselves
    if ($file -match "\.test\." -or $file -match "\.spec\." -or $file -match "test_") {
        continue
    }

    # Run backend tests
    if ($file -match "^backend/.*\.py$") {
        Push-Location backend
        try {
            $result = python -m pytest tests/unit/ -v --tb=short
            if ($LASTEXITCODE -ne 0) {
                $testFailed = $true
            }
        } finally {
            Pop-Location
        }
    }

    # Run frontend tests
    if ($file -match "^frontend/app/.*\.(ts|tsx)$") {
        Push-Location frontend
        try {
            $result = npm run test -- --watchAll=false
            if ($LASTEXITCODE -ne 0) {
                $testFailed = $true
            }
        } finally {
            Pop-Location
        }
    }
}

if ($testFailed) {
    Write-Host "❌ Some tests failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ All tests passed" -ForegroundColor Green
    exit 0
}
