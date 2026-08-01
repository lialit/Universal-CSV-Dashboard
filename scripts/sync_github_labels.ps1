param(
    [string]$Repository = "lialit/Universal-CSV-Dashboard",
    [string]$ConfigPath = ".github/labels.yml"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Label configuration not found: $ConfigPath"
}

function Get-LabelsFromSimpleYaml {
    param([string]$Path)

    $labels = @()
    $current = $null

    foreach ($line in Get-Content $Path) {
        $trimmed = $line.Trim()

        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }

        if ($trimmed -match '^- name:\s*"(.*)"\s*$') {
            if ($null -ne $current) {
                $labels += [PSCustomObject]$current
            }

            $current = [ordered]@{
                name = $Matches[1]
                color = ""
                description = ""
            }
            continue
        }

        if ($null -eq $current) {
            continue
        }

        if ($trimmed -match '^color:\s*"([0-9A-Fa-f]{6})"\s*$') {
            $current.color = $Matches[1]
            continue
        }

        if ($trimmed -match '^description:\s*"(.*)"\s*$') {
            $current.description = $Matches[1]
            continue
        }
    }

    if ($null -ne $current) {
        $labels += [PSCustomObject]$current
    }

    return $labels
}

gh auth status | Out-Null

$labels = Get-LabelsFromSimpleYaml -Path $ConfigPath

if (-not $labels -or $labels.Count -eq 0) {
    throw "No labels were parsed from $ConfigPath."
}

foreach ($label in $labels) {
    $name = [string]$label.name
    $color = [string]$label.color
    $description = [string]$label.description

    if ([string]::IsNullOrWhiteSpace($name) -or [string]::IsNullOrWhiteSpace($color)) {
        throw "Invalid label entry in $ConfigPath. Each label requires name and color."
    }

    Write-Host "Syncing label: $name"

    gh api "/repos/$Repository/labels/$([uri]::EscapeDataString($name))" *> $null

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

Write-Host "Label synchronization completed for $Repository. Parsed $($labels.Count) labels."
