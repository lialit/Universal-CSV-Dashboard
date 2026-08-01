param(
    [string]$Repository = "lialit/Universal-CSV-Dashboard",
    [int]$IssueNumber = 14,
    [string]$MilestonePrefix = "v1.1"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

gh auth status | Out-Null

$endpoint = "/repos/$Repository/milestones?state=all`&per_page=100"
$milestonesJson = gh api $endpoint
$milestones = $milestonesJson | ConvertFrom-Json
$matches = @($milestones | Where-Object { $_.title -like "$MilestonePrefix*" })

if ($matches.Count -eq 0) {
    throw "No milestone found with prefix: $MilestonePrefix"
}

if ($matches.Count -gt 1) {
    $titles = ($matches | ForEach-Object { $_.title }) -join ", "
    throw "Multiple milestones found with prefix '$MilestonePrefix': $titles"
}

$milestone = $matches[0]

gh api --method PATCH "/repos/$Repository/issues/$IssueNumber" `
    -F milestone=$($milestone.number) | Out-Null

Write-Host "Assigned issue #$IssueNumber to milestone '$($milestone.title)' (number $($milestone.number))."
