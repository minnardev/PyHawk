# PyHawk Uninstaller (Windows)
Write-Host "🗑  Uninstalling PyHawk..." -ForegroundColor Yellow

$InstallDir = Join-Path $env:USERPROFILE ".pyhawk"
$BinDir = Join-Path $InstallDir "bin"

# Remove from User PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$NewPath = ($UserPath -split ';' | Where-Object { $_ -ne $BinDir }) -join ';'
[Environment]::SetEnvironmentVariable("Path", $NewPath, "User")

# Remove folder
if (Test-Path $InstallDir) {
    Remove-Item -Recurse -Force $InstallDir
}

Write-Host "✓ PyHawk successfully uninstalled." -ForegroundColor Green
