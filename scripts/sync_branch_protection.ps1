param(
    [string]$Owner = "lialit",
    [string]$Repository = "Universal-CSV-Dashboard",
    [string]$ConfigPath = ".github/branch-protection.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Branch protection configuration not found: $ConfigPath"
}

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$branch = [string]$config.branch

if ([string]::IsNullOrWhiteSpace($branch)) {
    throw "The branch field is missing from $ConfigPath."
}

Write-Host "Validating GitHub authentication..."
gh auth status | Out-Null

$endpoint = "repos/$Owner/$Repository/branches/$branch/protection"
$tempFile = [System.IO.Path]::GetTempFileName()

try {
    $payload = @{
        required_status_checks = @{
            strict = [bool]$config.required_status_checks.strict
            contexts = @($config.required_status_checks.contexts)
        }
        enforce_admins = [bool]$config.enforce_admins
        required_pull_request_reviews = @{
            dismiss_stale_reviews = [bool]$config.required_pull_request_reviews.dismiss_stale_reviews
            require_code_owner_reviews = [bool]$config.required_pull_request_reviews.require_code_owner_reviews
            required_approving_review_count = [int]$config.required_pull_request_reviews.required_approving_review_count
            require_last_push_approval = [bool]$config.required_pull_request_reviews.require_last_push_approval
        }
        restrictions = $null
        required_linear_history = [bool]$config.required_linear_history
        allow_force_pushes = [bool]$config.allow_force_pushes
        allow_deletions = [bool]$config.allow_deletions
        block_creations = [bool]$config.block_creations
        required_conversation_resolution = [bool]$config.required_conversation_resolution
        lock_branch = [bool]$config.lock_branch
        allow_fork_syncing = [bool]$config.allow_fork_syncing
    }

    $payload | ConvertTo-Json -Depth 10 | Set-Content -Path $tempFile -Encoding UTF8

    Write-Host "Applying protection to $Owner/$Repository branch '$branch'..."
    gh api --method PUT $endpoint `
        --header "Accept: application/vnd.github+json" `
        --input $tempFile | Out-Null

    Write-Host "Branch protection applied successfully."

    $resultJson = gh api $endpoint --header "Accept: application/vnd.github+json"
    $result = $resultJson | ConvertFrom-Json

    $contexts = @($result.required_status_checks.contexts) -join ", "
    Write-Host "Required checks: $contexts"
    Write-Host "Require pull request: $($null -ne $result.required_pull_request_reviews)"
    Write-Host "Enforce for administrators: $($result.enforce_admins.enabled)"
    Write-Host "Require conversation resolution: $($result.required_conversation_resolution.enabled)"
    Write-Host "Allow force pushes: $($result.allow_force_pushes.enabled)"
    Write-Host "Allow deletions: $($result.allow_deletions.enabled)"
}
finally {
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}
