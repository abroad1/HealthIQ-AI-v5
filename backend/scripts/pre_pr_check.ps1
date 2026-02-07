$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [string]$Name,
        [ScriptBlock]$Block
    )

    try {
        & $Block
        if ($LASTEXITCODE -ne $null -and $LASTEXITCODE -ne 0) {
            throw "Exit code $LASTEXITCODE"
        }
        Write-Host "PASS: $Name"
    } catch {
        Write-Host "FAIL: $Name - $($_.Exception.Message)"
        exit 1
    }
}

function Invoke-Python {
    param(
        [string]$Name,
        [string[]]$Args
    )

    Invoke-Step -Name $Name -Block { & python @Args }
}

Invoke-Python -Name "SSOT validate" -Args @("-m", "backend.core.ssot.validate")

if (Test-Path "backend/scripts/smoke_cluster_engine_v2.py") {
    Invoke-Python -Name "Smoke cluster engine v2" -Args @("backend/scripts/smoke_cluster_engine_v2.py")
} else {
    Write-Host "SKIP: Smoke cluster engine v2 (missing)"
}

if (Test-Path "backend/scripts/smoke_prompt_v2.py") {
    Invoke-Python -Name "Smoke prompt v2" -Args @("backend/scripts/smoke_prompt_v2.py")
} else {
    Write-Host "SKIP: Smoke prompt v2 (missing)"
}

Invoke-Step -Name "Upload parse smoke" -Block {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/upload/parse" -Method Post -Form @{
        text_content = "Hemoglobin 13.2 g/dL"
    }
    if (-not $response) {
        throw "Empty response"
    }
}

