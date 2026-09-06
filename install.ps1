# ==============================================================================
# PyHawk — Automated Windows Installer (PowerShell)
# «Sharp as a hawk, fast as math»
# ==============================================================================

Write-Host ""
Write-Host "    __   __  _______  _     _  ___   _ " -ForegroundColor Cyan
Write-Host "   |  | |  ||   _   || | _ | ||   | | |" -ForegroundColor Cyan
Write-Host "   |  |_|  ||  |_|  || || || ||   |_| |" -ForegroundColor Cyan
Write-Host "   |       ||       ||       ||      _|" -ForegroundColor Cyan
Write-Host "   |       ||       ||       ||     |_ " -ForegroundColor Cyan
Write-Host "   |   _   ||   _   ||   _   ||    _  |" -ForegroundColor Cyan
Write-Host "   |__| |__||__| |__||__| |__||___| |_|" -ForegroundColor Cyan
Write-Host "  PyHawk Installer — Windows Edition" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
Write-Host "Checking requirements..." -ForegroundColor Yellow

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py -3"
}

if (-not $pythonCmd) {
    Write-Host "[ERROR] Python 3 was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/ or Windows Store."
    exit 1
}

$pyVer = & ($pythonCmd.Split()[0]) --version 2>&1
Write-Host "   [OK] Found $pyVer" -ForegroundColor Green

# 2. Setup directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$InstallDir = Join-Path $env:USERPROFILE ".pyhawk"
$BinDir = Join-Path $InstallDir "bin"

Write-Host "`nInstalling PyHawk to $InstallDir..." -ForegroundColor Yellow

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

# Copy files
if ($ScriptDir -ne $InstallDir) {
    Copy-Item -Path (Join-Path $ScriptDir "hawk") -Destination $InstallDir -Recurse -Force
    if (Test-Path (Join-Path $ScriptDir "examples")) {
        Copy-Item -Path (Join-Path $ScriptDir "examples") -Destination $InstallDir -Recurse -Force
    }
    if (Test-Path (Join-Path $ScriptDir "vscode-hawk")) {
        Copy-Item -Path (Join-Path $ScriptDir "vscode-hawk") -Destination $InstallDir -Recurse -Force
    }
    Copy-Item -Path (Join-Path $ScriptDir "hawk_cli.py") -Destination $InstallDir -Force
    if (Test-Path (Join-Path $ScriptDir "README.md")) {
        Copy-Item -Path (Join-Path $ScriptDir "README.md") -Destination $InstallDir -Force
    }
}

# 3. Create Windows batch launcher wrappers in $BinDir
$cliPath = Join-Path $InstallDir "hawk_cli.py"

$batContent = @"
@echo off
$pythonCmd "$cliPath" %*
"@

Set-Content -Path (Join-Path $BinDir "pyhawk.cmd") -Value $batContent -Encoding Ascii
Set-Content -Path (Join-Path $BinDir "hawk.cmd") -Value $batContent -Encoding Ascii

Write-Host "   [OK] Created commands: pyhawk.cmd and hawk.cmd in $BinDir" -ForegroundColor Green

# 4. Add to User PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$PathEntries = $UserPath -split ';'

if ($PathEntries -notcontains $BinDir) {
    Write-Host "`nConfiguring PATH in Windows Environment Variables..." -ForegroundColor Yellow
    $NewUserPath = if ([string]::IsNullOrWhiteSpace($UserPath)) { $BinDir } else { "$UserPath;$BinDir" }
    [Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
    $env:Path += ";$BinDir"
    Write-Host "   [OK] PATH updated successfully in Windows Environment Variables!" -ForegroundColor Green
} else {
    Write-Host "   [OK] $BinDir is already in User PATH." -ForegroundColor Green
}

# 5. Install VS Code Extension if installed
$vsixFiles = Get-ChildItem -Path (Join-Path $InstallDir "vscode-hawk") -Filter "hawk-language-*.vsix" -ErrorAction SilentlyContinue | Sort-Object Name
$vsixPath = if ($vsixFiles) { $vsixFiles[-1].FullName } else { $null }

if (Get-Command code -ErrorAction SilentlyContinue) {
    if ($vsixPath -and (Test-Path $vsixPath)) {
        Write-Host "`nInstalling VS Code extension (PyHawk)..." -ForegroundColor Yellow
        & code --install-extension $vsixPath --force | Out-Null
        Write-Host "   [OK] VS Code extension installed!" -ForegroundColor Green
    }
}

Write-Host "`nPyHawk installed successfully!" -ForegroundColor Green
Write-Host "Try it in Command Prompt or PowerShell:"
Write-Host "  pyhawk version" -ForegroundColor Cyan
Write-Host "  pyhawk repl" -ForegroundColor Cyan
Write-Host "  pyhawk run <file.hwk>" -ForegroundColor Cyan
Write-Host "  pyhawk build <file.hwk>" -ForegroundColor Cyan
Write-Host "`nSharp as a hawk, fast as math.`n"
