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
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI authentication failed. Run: gh auth login"
}

$labels = Get-LabelsFromSimpleYaml -Path $ConfigPath

if (-not $labels -or $labels.Count -eq 0) {
    throw "No labels were parsed from $ConfigPath."
}

# Fetch all current labels once. This avoids treating an expected 404 for a
# missing label as a fatal PowerShell error.
$existingJson = gh api "/repos/$Repository/labels?per_page=100"
if ($LASTEXITCODE -ne 0) {
    throw "Could not read existing labels from $Repository."
}

$existingLabels = $existingJson | ConvertFrom-Json
$existingByName = @{}
foreach ($existingLabel in $existingLabels) {
    $existingByName[[string]$existingLabel.name] = $true
}

$created = 0
$updated = 0

foreach ($label in $labels) {
    $name = [string]$label.name
    $color = [string]$label.color
    $description = [string]$label.description

    if ([string]::IsNullOrWhiteSpace($name) -or [string]::IsNullOrWhiteSpace($color)) {
        throw "Invalid label entry in $ConfigPath. Each label requires name and color."
    }

    if ($existingByName.ContainsKey($name)) {
        Write-Host "Updating label: $name"
        $encodedName = [uri]::EscapeDataString($name)
        gh api --method PATCH "/repos/$Repository/labels/$encodedName" `
            -f new_name="$name" `
            -f color="$color" `
            -f description="$description" | Out-Null

        if ($LASTEXITCODE -ne 0) {
            throw "Failed to update label: $name"
        }

        $updated++
    }
    else {
        Write-Host "Creating label: $name"
        gh api --method POST "/repos/$Repository/labels" `
            -f name="$name" `
            -f color="$color" `
            -f description="$description" | Out-Null

        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create label: $name"
        }

        $existingByName[$name] = $true
        $created++
    }
}

Write-Host "Label synchronization completed for $Repository. Created: $created. Updated: $updated. Total configured: $($labels.Count)."
