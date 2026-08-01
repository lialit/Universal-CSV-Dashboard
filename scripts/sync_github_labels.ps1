param(
    [string]$Repository = "lialit/Universal-CSV-Dashboard",
    [string]$ConfigPath = ".github/labels.yml"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Get-Command ConvertFrom-Yaml -ErrorAction SilentlyContinue)) {
    throw "ConvertFrom-Yaml is unavailable. Run this script in PowerShell 7.4+ or install a YAML module that provides it."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Label configuration not found: $ConfigPath"
}

gh auth status | Out-Null

$labels = Get-Content $ConfigPath -Raw | ConvertFrom-Yaml

foreach ($label in $labels) {
    $name = [string]$label.name
    $color = [string]$label.color
    $description = [string]$label.description

    Write-Host "Syncing label: $name"

    $existing = gh api "/repos/$Repository/labels/$([uri]::EscapeDataString($name))" 2>$null

    if ($LASTEXITCODE -eq 0) {
        gh api --method PATCH "/repos/$Repository/labels/$([uri]::EscapeDataString($name))" `
            -f new_name="$name" `
            -f color="$color" `
            -f description="$description" | Out-Null
    }
    else {
        gh api --method POST "/repos/$Repository/labels" `
            -f name="$name" `
            -f color="$color" `
            -f description="$description" | Out-Null
    }
}

Write-Host "Label synchronization completed for $Repository."
