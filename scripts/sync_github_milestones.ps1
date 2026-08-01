param(
    [string]$Repository = "lialit/Universal-CSV-Dashboard",
    [string]$ConfigPath = ".github/milestones.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Milestone configuration not found: $ConfigPath"
}

gh auth status | Out-Null

$milestones = Get-Content $ConfigPath -Raw | ConvertFrom-Json
if (-not $milestones -or $milestones.Count -eq 0) {
    throw "No milestones were parsed from $ConfigPath."
}

$existingMilestones = gh api --paginate "/repos/$Repository/milestones?state=all&per_page=100" | ConvertFrom-Json
$created = 0
$updated = 0

foreach ($milestone in $milestones) {
    $title = [string]$milestone.title
    $description = [string]$milestone.description
    $state = [string]$milestone.state

    if ([string]::IsNullOrWhiteSpace($title)) {
        throw "Invalid milestone entry in $ConfigPath. Each milestone requires a title."
    }

    if ([string]::IsNullOrWhiteSpace($state)) {
        $state = "open"
    }

    $existing = $existingMilestones | Where-Object { $_.title -eq $title } | Select-Object -First 1

    if ($null -ne $existing) {
        Write-Host "Updating milestone: $title"
        gh api --method PATCH "/repos/$Repository/milestones/$($existing.number)" `
            -f title="$title" `
            -f description="$description" `
            -f state="$state" | Out-Null
        $updated++
    }
    else {
        Write-Host "Creating milestone: $title"
        gh api --method POST "/repos/$Repository/milestones" `
            -f title="$title" `
            -f description="$description" `
            -f state="$state" | Out-Null
        $created++
    }
}

Write-Host "Milestone synchronization completed for $Repository. Created: $created. Updated: $updated. Total configured: $($milestones.Count)."
