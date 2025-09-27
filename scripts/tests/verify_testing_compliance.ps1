# Test Compliance Verification Script (PowerShell)
# Verifies that all testing requirements from TESTING_STRATEGY.md
# and CURSOR_RULES.md are properly implemented and documented.

param(
    [string]$ProjectRoot = "."
)

Write-Host "🧪 Test Compliance Verification Report" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

$Issues = @()
$TotalIssues = 0

# Check if TEST_LEDGER.md exists
$TestLedgerPath = Join-Path $ProjectRoot "TEST_LEDGER.md"
if (-not (Test-Path $TestLedgerPath)) {
    $Issues += "❌ TEST_LEDGER.md does not exist"
    $TotalIssues++
} else {
    $Content = Get-Content $TestLedgerPath -Raw
    
    # Check for required elements
    $RequiredElements = @(
        @{Pattern = "Run Command"; Error = "Missing run command documentation"},
        @{Pattern = "Execution time"; Error = "Missing execution time documentation"},
        @{Pattern = "Coverage percentage"; Error = "Missing coverage percentage documentation"},
        @{Pattern = "Test counts"; Error = "Missing test count documentation"},
        @{Pattern = "Individual test methods"; Error = "Missing individual test method documentation"}
    )
    
    foreach ($Element in $RequiredElements) {
        if ($Content -notmatch $Element.Pattern) {
            $Issues += "❌ $($Element.Error)"
            $TotalIssues++
        }
    }
    
    # Check for proper test count format
    if ($Content -notmatch '\d+/\d+\s+tests') {
        $Issues += "❌ Missing proper test count format (e.g., 10/10 tests)"
        $TotalIssues++
    }
    
    # Check for run command format
    if ($Content -notmatch 'python -m pytest.*-v') {
        $Issues += "❌ Missing proper run command format"
        $TotalIssues++
    }
    
    # Check for coverage percentage format
    if ($Content -notmatch '\d+%') {
        $Issues += "❌ Missing coverage percentage documentation"
        $TotalIssues++
    }
    
    # Check for code block formatted commands
    if ($Content -notmatch '```bash' -and $Content -notmatch '```powershell') {
        $Issues += "❌ Missing code block formatted commands"
        $TotalIssues++
    }
}

# Check test archive compliance
$TestsArchivePath = Join-Path $ProjectRoot "tests_archive"
if (-not (Test-Path $TestsArchivePath)) {
    $Issues += "❌ tests_archive directory does not exist"
    $TotalIssues++
} else {
    $RecentArchives = Get-ChildItem -Path $TestsArchivePath -Recurse -Filter "*.py" | Where-Object { $_.FullName -match "2025-01-27" }
    if ($RecentArchives.Count -eq 0) {
        $Issues += "❌ No recent test archives found for 2025-01-27"
        $TotalIssues++
    }
}

# Check backend test structure
$BackendTestsPath = Join-Path $ProjectRoot "backend\tests"
if (Test-Path $BackendTestsPath) {
    $TestFiles = Get-ChildItem -Path $BackendTestsPath -Recurse -Filter "test_*.py"
    foreach ($TestFile in $TestFiles) {
        if (-not $TestFile.Name.StartsWith("test_")) {
            $Issues += "❌ Backend test file $($TestFile.Name) does not follow naming convention"
            $TotalIssues++
        }
    }
}

# Check frontend test structure
$FrontendTestsPath = Join-Path $ProjectRoot "frontend\tests"
if (Test-Path $FrontendTestsPath) {
    $TestFiles = Get-ChildItem -Path $FrontendTestsPath -Recurse -Filter "*.test.ts"
    foreach ($TestFile in $TestFiles) {
        if (-not $TestFile.Name.EndsWith(".test.ts")) {
            $Issues += "❌ Frontend test file $($TestFile.Name) does not follow naming convention"
            $TotalIssues++
        }
    }
}

# Print results
Write-Host "`n📋 Compliance Check Results:" -ForegroundColor Yellow
if ($Issues.Count -eq 0) {
    Write-Host "  ✅ All compliance requirements met!" -ForegroundColor Green
} else {
    foreach ($Issue in $Issues) {
        Write-Host "  $Issue" -ForegroundColor Red
    }
}

Write-Host "`n📊 Summary:" -ForegroundColor Yellow
if ($TotalIssues -eq 0) {
    Write-Host "  ✅ All compliance requirements met!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "  ❌ $TotalIssues compliance issues found" -ForegroundColor Red
    Write-Host "  🔧 Please fix issues before completing testing tasks" -ForegroundColor Yellow
    exit 1
}
