#!/usr/bin/env powershell
<#
.SYNOPSIS
    Push MTG Draft Rater to GitHub
.DESCRIPTION
    This script automates pushing the project to GitHub
.PARAMETER RepoName
    GitHub repository name (will be created if not exists)
.PARAMETER GitUser
    Your GitHub username
.EXAMPLE
    .\push-to-github.ps1 -RepoName "mtg-draft-rater" -GitUser "adamd613"
#>

param(
    [string]$RepoName = "mtg-draft-rater",
    [string]$GitUser = "adamd613"
)

$gitPath = "C:\Program Files\Git\bin\git.exe"
$projectPath = "c:\Users\Adam\Desktop\Hobbies and Things\Rate_This_Card"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   GitHub Push Configuration Helper     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  GitHub User: $GitUser"
Write-Host "  Repository: $RepoName"
Write-Host "  Local Path: $projectPath"
Write-Host ""

# Navigate to project
Set-Location $projectPath

# Confirm branch name
Write-Host "Current branch:" -ForegroundColor Yellow
& $gitPath branch

Write-Host ""
Write-Host "Instructions to complete the push:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Go to https://github.com/new"
Write-Host "2. Create repository: $RepoName"
Write-Host "3. Do NOT initialize with README"
Write-Host "4. Click 'Create repository'"
Write-Host ""
Write-Host "5. Then run these commands in PowerShell:" -ForegroundColor Green
Write-Host ""
Write-Host "`$gitPath = `"$gitPath`"" -ForegroundColor White
Write-Host "cd `"$projectPath`"" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "# Add GitHub as remote" -ForegroundColor Gray
Write-Host "& `$gitPath remote add origin https://github.com/$GitUser/$RepoName.git" -ForegroundColor White
Write-Host "" -ForegroundColor Gray
Write-Host "# Rename to main branch (optional but recommended)" -ForegroundColor Gray
Write-Host "& `$gitPath branch -M main" -ForegroundColor White
Write-Host "" -ForegroundColor Gray
Write-Host "# Push to GitHub" -ForegroundColor Gray
Write-Host "& `$gitPath push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Note: You'll be prompted for GitHub credentials (use Personal Access Token)" -ForegroundColor Yellow
Write-Host ""

$createNow = Read-Host "Create repository now on GitHub? (y/n)"
if ($createNow -eq 'y' -or $createNow -eq 'Y') {
    Write-Host ""
    Write-Host "Opening GitHub in browser..." -ForegroundColor Cyan
    Start-Process "https://github.com/new"
    Write-Host "Once created, come back and run the commands above" -ForegroundColor Green
}
