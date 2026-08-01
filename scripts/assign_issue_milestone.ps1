param(
    [string]$Repository = "lialit/Universal-CSV-Dashboard",
    [int]$IssueNumber = 14,
    [string]$MilestoneTitle = "v1.1 - Polish & Adoption"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

gh auth status | Out-Null

$milestonesJson = gh api "/repos/$Repository/milestones?state=all&per_page=100"
$milestones = $milestonesJson | ConvertFrom-Json
$milestone = $milestones | Where-Object { $_.title -eq $MilestoneTitle } | Select-Object -First 1

if ($null -eq $milestone) {
    throw "Milestone not found: $MilestoneTitle"
}

gh api --method PATCH "/repos/$Repository/issues/$IssueNumber" `
    -F milestone=$($milestone.number) | Out-Null

Write-Host "Assigned issue #$IssueNumber to milestone '$MilestoneTitle' (number $($milestone.number))."
