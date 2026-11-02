[CmdletBinding()]
param([string]$ToolDirectory = 'D:\CodexWork\iflytek-build-tools')
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $ToolDirectory -Force | Out-Null
$packages = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'tools.lock.json') -Raw | ConvertFrom-Json
foreach ($package in $packages) {
    $destination = Join-Path $ToolDirectory $package.name
    if (!(Test-Path -LiteralPath $destination)) {
        Write-Host "Downloading $($package.name)"
        Invoke-WebRequest -Uri $package.url -OutFile $destination
    }
    if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $package.sha256) {
        throw "Checksum mismatch: $destination. The file will not be executed."
    }
}
if (!(Test-Path -LiteralPath (Join-Path $ToolDirectory 'android-build-tools/android-16/zipalign.exe'))) {
    Expand-Archive -LiteralPath (Join-Path $ToolDirectory 'build-tools_r36_windows.zip') -DestinationPath (Join-Path $ToolDirectory 'android-build-tools')
}
if (!(Test-Path -LiteralPath (Join-Path $ToolDirectory 'platform-tools/adb.exe'))) {
    Expand-Archive -LiteralPath (Join-Path $ToolDirectory 'platform-tools_r37.0.1-win.zip') -DestinationPath $ToolDirectory
}
Write-Host "Verified toolchain: $ToolDirectory"
