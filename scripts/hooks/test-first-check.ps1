# Test-First Development Enforcement Hook (PowerShell)
# Ensures every implementation file has a corresponding test file

Write-Host "🔍 Checking for test-first compliance..." -ForegroundColor Cyan

# Get list of staged files
$stagedFiles = git diff --cached --name-only --diff-filter=AM

$missingTests = @()

foreach ($file in $stagedFiles) {
    # Skip test files themselves
    if ($file -match "\.test\." -or $file -match "\.spec\." -or $file -match "test_") {
        continue
    }

    # Check backend Python files
    if ($file -match "^backend/(app|core|services)/.*\.py$") {
        $dir = Split-Path $file
        $filename = [System.IO.Path]::GetFileNameWithoutExtension($file)
        $testFile = Join-Path $dir "test_$filename.py"
        
        if (-not (Test-Path $testFile)) {
            $missingTests += "$file -> $testFile"
        }
    }

    # Check frontend TypeScript files
    if ($file -match "^frontend/app/(services|state|components)/.*\.(ts|tsx)$") {
        $dir = Split-Path $file
        $filename = [System.IO.Path]::GetFileNameWithoutExtension($file)
        $testFile = Join-Path $dir "$filename.test.ts"
        
        if (-not (Test-Path $testFile)) {
            $missingTests += "$file -> $testFile"
        }
    }
}

# Report results
if ($missingTests.Count -eq 0) {
    Write-Host "✅ All implementation files have corresponding test files" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Missing test files for the following implementation files:" -ForegroundColor Red
    foreach ($missing in $missingTests) {
        Write-Host "  $missing" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please create the missing test files before committing." -ForegroundColor Yellow
    Write-Host "Use templates in templates/tests/ for reference." -ForegroundColor Yellow
    exit 1
}
