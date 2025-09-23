<#
PowerShell script: apply patch files (git apply) one-by-one, run checks, commit, push, create PR via gh
Usage (PowerShell):
  pwsh .\scripts\auto_apply_patches_and_create_prs.ps1 -PatchDir .\scripts\patches -BaseBranch main -CheckCmd "python scripts/check_all_jinja.py"
#>
param(
    [Parameter(Mandatory=$true)][string]$PatchDir,
    [string]$BaseBranch = "main",
    [string]$CheckCmd = "python scripts/check_all_jinja.py",
    [string]$Remote = "origin",
    [switch]$DryRun,
    [string]$Label = "automated",
    [string]$Reviewer = "",
    [string]$PrTemplatePath = ".github/PULL_REQUEST_TEMPLATE.md"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git not on PATH." }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "gh (GitHub CLI) not on PATH. Run 'gh auth login' first." }

$PatchDir = (Resolve-Path $PatchDir).Path
Write-Host "Scanning patches in $PatchDir"

Get-ChildItem -Path $PatchDir -Filter "*.patch" | ForEach-Object {
    $patch = $_.FullName
    $patchName = $_.BaseName
    $branch = "auto/patch/$patchName"
    Write-Host "=== Processing patch: $patchName ==="

    if ($DryRun) {
        Write-Host "DRY RUN: would create branch $branch from $BaseBranch and attempt to apply $patch"
        return
    }

    git fetch $Remote
    git checkout $BaseBranch
    git pull $Remote $BaseBranch

    git checkout -b $branch

    try {
        git apply --index $patch
    } catch {
        Write-Warning "Patch failed to apply cleanly: $patchName. Aborting branch and leaving patch for manual review."
        git checkout $BaseBranch
        git branch -D $branch
        return
    }

    # Stage any changes from the patch explicitly (defensive add for CI envs)
    git add -A

    $checkSucceeded = $true
    if (Test-Path (Join-Path (Get-Location) $CheckCmd.Split(' ')[1])) {
        Write-Host "Running checks: $CheckCmd"
        try {
            pwsh -NoProfile -Command $CheckCmd
        } catch {
            $checkSucceeded = $false
            Write-Warning "Checks failed for $patchName. Leaving branch $branch for manual fix."
        }
    } else {
        Write-Warning "Check script not found; skipping checks for $patchName."
    }

    if (-not $checkSucceeded) {
        return
    }

    git commit -m "chore: apply suggested patch $patchName" --no-verify
    git push -u $Remote $branch

    $title = "Automated: apply patch $patchName"
    $body = "Auto-generated patch application for $patchName\n\nThis branch was created by scripts/auto_apply_patches_and_create_prs.ps1.\nPlease review and merge via normal workflow."

    $ghCmd = "gh pr create --title `"$title`" --body `"$body`" --base $BaseBranch --head $branch"
    if ($Label) { $ghCmd += " --label `"$Label`"" }
    if ($Reviewer) { $ghCmd += " --reviewer $Reviewer" }
    if (Test-Path $PrTemplatePath) { $ghCmd += " --body-file $PrTemplatePath" }

    Invoke-Expression $ghCmd

    Write-Host "PR created for $branch"
}
Write-Host "All patches processed."
