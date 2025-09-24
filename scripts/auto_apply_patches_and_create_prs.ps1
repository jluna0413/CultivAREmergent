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

Get-ChildItem -Path $PatchDir -Filter "*.patch" | Sort-Object Name | ForEach-Object {
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

    # Copy patch to a stable temp location so it remains accessible across checkouts
    $tmpRoot = if ($env:RUNNER_TEMP) { $env:RUNNER_TEMP } elseif ($env:TEMP) { $env:TEMP } else { Join-Path (Get-Location) ".gitpatchtmp" }
    if (-not (Test-Path $tmpRoot)) { New-Item -ItemType Directory -Force -Path $tmpRoot | Out-Null }
    $tmpPatch = Join-Path $tmpRoot ("$patchName.patch")
    Get-Content -Raw -Path $patch | Set-Content -Path $tmpPatch -NoNewline:$false

    try {
        git apply --index -- "$tmpPatch"
    } catch {
        Write-Warning "Patch failed to apply cleanly: $patchName. Aborting branch and leaving patch for manual review."
        git checkout $BaseBranch
        git branch -D $branch
        return
    }

    # Stage only modified/deleted tracked files, avoid committing the .patch files themselves
    git add -u

    # If nothing changed, skip commit/PR
    $status = git status --porcelain
    if (-not $status) {
        Write-Host "No file changes detected after applying $patchName; skipping commit/PR."
        git checkout $BaseBranch
        git branch -D $branch
        return
    }

    $checkSucceeded = $true
    # If CheckCmd is a simple script path like 'python scripts/check_all_jinja.py' try to validate the script exists
    $checkParts = $CheckCmd -split '\s+'
    if ($checkParts.Length -ge 2) {
        $checkPath = $checkParts[1]
        if (Test-Path (Resolve-Path -Path $checkPath -ErrorAction SilentlyContinue)) {
            Write-Host "Running checks: $CheckCmd"
            try {
                pwsh -NoProfile -Command $CheckCmd
            } catch {
                $checkSucceeded = $false
                Write-Warning "Checks failed for $patchName. Leaving branch $branch for manual fix."
            }
        } else {
            Write-Warning "Check script not found at $checkPath; skipping checks for $patchName."
        }
    } else {
        Write-Host "No check command provided; skipping checks for $patchName."
    }

    if (-not $checkSucceeded) {
        return
    }

    git commit -m "chore: apply suggested patch $patchName" --no-verify
    git push -u $Remote $branch

    $title = "Automated: apply patch $patchName"
    $body = "Auto-generated patch application for $patchName\n\nThis branch was created by scripts/auto_apply_patches_and_create_prs.ps1.\nPlease review and merge via normal workflow."

    # Build gh arguments safely to avoid command injection
    $ghArgs = @('pr','create','--title',$title,'--body',$body,'--base',$BaseBranch,'--head',$branch)
    if ($Label) { $ghArgs += @('--label',$Label) }
    if ($Reviewer) { $ghArgs += @('--reviewer',$Reviewer) }
    if (Test-Path $PrTemplatePath) { $ghArgs += @('--body-file',$PrTemplatePath) }

    try {
        $proc = Start-Process -FilePath 'gh' -ArgumentList $ghArgs -NoNewWindow -Wait -PassThru -ErrorAction Stop
        if ($proc.ExitCode -ne 0) { Write-Warning "gh returned exit code $($proc.ExitCode) while creating PR for $branch" }
        else { Write-Host "PR created for $branch" }
    } catch {
        Write-Warning "Failed to create PR via gh for $branch: $_"
    }
}
Write-Host "All patches processed."
