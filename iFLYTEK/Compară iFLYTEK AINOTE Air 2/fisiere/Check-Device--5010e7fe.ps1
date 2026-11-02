[CmdletBinding()]
param(
    [string]$ToolDirectory='D:\CodexWork\iflytek-build-tools',
    [string]$Serial,
    [string]$ReportFile=(Join-Path $PSScriptRoot 'reports/device-status.json')
)
$ErrorActionPreference='Stop'
$adb=Join-Path $ToolDirectory 'platform-tools/adb.exe'
if (!(Test-Path -LiteralPath $adb)) { throw 'Run Setup-Tools.ps1 first.' }
$list=@(& $adb devices)
if ($LASTEXITCODE -ne 0) { throw 'ADB device listing failed.' }
$ready=@($list | Where-Object {$_ -match '^\S+\s+device$'})
$unauthorized=@($list | Where-Object {$_ -match '^\S+\s+unauthorized$'})
$result=[ordered]@{authorizedDevices=$ready.Count;unauthorizedDevices=$unauthorized.Count;deviceInstallationTested=$false;deviceLaunchTested=$false}
if ($Serial) {
    if (!($ready | Where-Object {($_ -split '\s+')[0] -eq $Serial})) { throw 'Requested device is not authorized.' }
} elseif ($ready.Count -eq 1) {
    $Serial=($ready[0] -split '\s+')[0]
}
if ($Serial) {
    $result.model=((& $adb -s $Serial shell getprop ro.product.model) -join '').Trim()
    $result.androidVersion=((& $adb -s $Serial shell getprop ro.build.version.release) -join '').Trim()
    $result.apiLevel=((& $adb -s $Serial shell getprop ro.build.version.sdk) -join '').Trim()
    $result.abis=((& $adb -s $Serial shell getprop ro.product.cpu.abilist) -join '').Trim()
    $app=@(& $adb -s $Serial shell pm path com.iflytek.translateapp)
    $result.originalPackageInstalled=[bool]($app -match '^package:')
    $result.status='ADB_READY'
} else {
    $result.status=if ($ready.Count -gt 1) {'SELECT_DEVICE'} elseif ($unauthorized.Count) {'AUTHORIZE_ON_PHONE'} else {'NO_ADB_DEVICE'}
}
# Device serials, accounts, phone numbers and IMEIs are deliberately not saved.
New-Item -ItemType Directory -Path (Split-Path -Parent $ReportFile) -Force | Out-Null
$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $ReportFile -Encoding utf8
$result | ConvertTo-Json -Depth 4
