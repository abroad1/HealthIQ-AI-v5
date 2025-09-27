# TEST_LEDGER.md Update Check Hook (PowerShell)
# Ensures TEST_LEDGER.md is updated when code changes are made

Write-Host "📝 Checking TEST_LEDGER.md update..." -ForegroundColor Cyan

# Check if any non-test files were changed
$changedFiles = git diff --cached --name-only --diff-filter=AM | Where-Object { $_ -match "\.(py|ts|tsx)$" -and $_ -notmatch "(test|spec)" }

if (-not $changedFiles) {
    Write-Host "✅ No implementation files changed, skipping TEST_LEDGER.md check" -ForegroundColor Green
    exit 0
}

# Check if TEST_LEDGER.md was updated
$ledgerUpdated = git diff --cached --name-only | Where-Object { $_ -eq "TEST_LEDGER.md" }

if ($ledgerUpdated) {
    Write-Host "✅ TEST_LEDGER.md was updated" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ TEST_LEDGER.md was not updated for code changes" -ForegroundColor Red
    Write-Host "Changed files:" -ForegroundColor Yellow
    foreach ($file in $changedFiles) {
        Write-Host "  $file" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please update TEST_LEDGER.md with test results before committing." -ForegroundColor Yellow
    exit 1
}
