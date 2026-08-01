param(
    [string]$Owner = "lialit",
    [string]$Repository = "Universal-CSV-Dashboard",
    [string]$ConfigPath = ".github/project-board.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed or is not available in PATH."
}

if (-not (Test-Path $ConfigPath)) {
    throw "Project configuration not found: $ConfigPath"
}

gh auth status | Out-Null

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$title = [string]$config.title

$projectListJson = gh project list --owner $Owner --limit 100 --format json
$projectList = $projectListJson | ConvertFrom-Json
$projects = if ($null -ne $projectList.projects) { $projectList.projects } else { $projectList }
$project = $projects | Where-Object { $_.title -eq $title } | Select-Object -First 1

if ($null -eq $project) {
    Write-Host "Creating project: $title"
    $createdJson = gh project create --owner $Owner --title $title --format json
    $project = $createdJson | ConvertFrom-Json
}
else {
    Write-Host "Using existing project: $title"
}

$projectNumber = [int]$project.number
if ($projectNumber -le 0) {
    throw "Could not determine the project number."
}

gh project edit $projectNumber --owner $Owner `
    --description ([string]$config.description) `
    --readme ([string]$config.readme) `
    --visibility ([string]$config.visibility) | Out-Null

$linkOutput = gh project link $projectNumber --owner $Owner --repo $Repository 2>&1
if ($LASTEXITCODE -ne 0 -and ($linkOutput -notmatch "already")) {
    throw ($linkOutput -join [Environment]::NewLine)
}

$fieldListJson = gh project field-list $projectNumber --owner $Owner --limit 100 --format json
$fieldList = $fieldListJson | ConvertFrom-Json
$existingFields = if ($null -ne $fieldList.fields) { $fieldList.fields } else { $fieldList }

foreach ($field in $config.fields) {
    $fieldName = [string]$field.name
    $exists = $existingFields | Where-Object { $_.name -eq $fieldName } | Select-Object -First 1

    if ($null -ne $exists) {
        Write-Host "Field already exists: $fieldName"
        continue
    }

    Write-Host "Creating field: $fieldName"

    if ([string]$field.type -eq "SINGLE_SELECT") {
        $options = ($field.options -join ",")
        gh project field-create $projectNumber --owner $Owner `
            --name $fieldName `
            --data-type SINGLE_SELECT `
            --single-select-options $options | Out-Null
    }
    else {
        gh project field-create $projectNumber --owner $Owner `
            --name $fieldName `
            --data-type ([string]$field.type) | Out-Null
    }
}

$itemListJson = gh project item-list $projectNumber --owner $Owner --limit 200 --format json
$itemList = $itemListJson | ConvertFrom-Json
$existingItems = if ($null -ne $itemList.items) { $itemList.items } else { $itemList }

foreach ($itemUrl in $config.initial_items) {
    $itemUrl = [string]$itemUrl
    $exists = $existingItems | Where-Object {
        $_.content.url -eq $itemUrl -or $_.url -eq $itemUrl
    } | Select-Object -First 1

    if ($null -ne $exists) {
        Write-Host "Item already exists: $itemUrl"
        continue
    }

    Write-Host "Adding item: $itemUrl"
    gh project item-add $projectNumber --owner $Owner --url $itemUrl | Out-Null
}

Write-Host "Project board synchronization completed. Project number: $projectNumber"
Write-Host "Open with: gh project view $projectNumber --owner $Owner --web"
