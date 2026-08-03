param(
    [string]$Owner = "lialit",
    [string]$Repository = "Universal-CSV-Dashboard",
    [string]$ProjectTitle = "Universal CSV Dashboard Roadmap",
    [string]$ConfigPath = ".github/project-items.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Project item configuration not found: $ConfigPath"
}

gh auth status | Out-Null

$projectList = (gh project list --owner $Owner --limit 100 --format json | ConvertFrom-Json)
$projects = if ($null -ne $projectList.projects) { $projectList.projects } else { $projectList }
$project = $projects | Where-Object { $_.title -eq $ProjectTitle } | Select-Object -First 1

if ($null -eq $project) {
    throw "Project not found: $ProjectTitle"
}

$projectNumber = [int]$project.number
$projectView = gh project view $projectNumber --owner $Owner --format json | ConvertFrom-Json
$projectId = [string]$projectView.id

if ([string]::IsNullOrWhiteSpace($projectId)) {
    throw "Could not determine the project node ID."
}

$fieldList = gh project field-list $projectNumber --owner $Owner --limit 100 --format json | ConvertFrom-Json
$fields = if ($null -ne $fieldList.fields) { $fieldList.fields } else { $fieldList }

$itemList = gh project item-list $projectNumber --owner $Owner --limit 200 --format json | ConvertFrom-Json
$items = if ($null -ne $itemList.items) { $itemList.items } else { $itemList }

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$updated = 0

foreach ($entry in $config) {
    $issueNumber = [int]$entry.issue
    $issueUrl = "https://github.com/$Owner/$Repository/issues/$issueNumber"

    $item = $items | Where-Object {
        $_.content.url -eq $issueUrl -or $_.url -eq $issueUrl
    } | Select-Object -First 1

    if ($null -eq $item) {
        Write-Host "Adding missing issue #${issueNumber} to the project"
        gh project item-add $projectNumber --owner $Owner --url $issueUrl | Out-Null
        $itemList = gh project item-list $projectNumber --owner $Owner --limit 200 --format json | ConvertFrom-Json
        $items = if ($null -ne $itemList.items) { $itemList.items } else { $itemList }
        $item = $items | Where-Object {
            $_.content.url -eq $issueUrl -or $_.url -eq $issueUrl
        } | Select-Object -First 1
    }

    if ($null -eq $item) {
        throw "Could not find project item for issue #${issueNumber}"
    }

    $fieldValues = @{
        "Workflow" = [string]$entry.workflow
        "Priority" = [string]$entry.priority
        "Area" = [string]$entry.area
        "Release" = [string]$entry.release
        "Effort" = [string]$entry.effort
    }

    foreach ($fieldName in $fieldValues.Keys) {
        $field = $fields | Where-Object { $_.name -eq $fieldName } | Select-Object -First 1
        if ($null -eq $field) {
            throw "Project field not found: $fieldName"
        }

        $value = $fieldValues[$fieldName]
        $option = $field.options | Where-Object { $_.name -eq $value } | Select-Object -First 1
        if ($null -eq $option) {
            throw "Option '$value' not found in field '$fieldName'"
        }

        gh project item-edit `
            --id ([string]$item.id) `
            --project-id $projectId `
            --field-id ([string]$field.id) `
            --single-select-option-id ([string]$option.id) | Out-Null
    }

    Write-Host "Configured issue #${issueNumber}: $($entry.workflow), $($entry.priority), $($entry.area), $($entry.release), $($entry.effort)"
    $updated++
}

Write-Host "Project workflow synchronization completed. Updated: $updated."
Write-Host "Open with: gh project view $projectNumber --owner $Owner --web"
