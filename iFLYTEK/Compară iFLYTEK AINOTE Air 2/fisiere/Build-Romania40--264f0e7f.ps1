[CmdletBinding()]
param(
    [string]$BaselineApk = (Join-Path $PSScriptRoot '../../dist/iflytek-1.0.3899-full-rebuilt.apk'),
    [string]$OriginalLibrary = 'D:\CodexWork\iflytek-build-work\decoded-full\lib\arm64-v8a\libapp.so',
    [string]$WorkDirectory = 'D:\CodexWork\iflytek-romania40-work',
    [string]$ToolDirectory = 'D:\CodexWork\iflytek-build-tools',
    [string]$SigningDirectory = 'D:\CodexWork\iflytek-build-private',
    [string]$Jdk = 'C:\Program Files\Java\jdk-21',
    [string]$Python = 'C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe',
    [string]$Distribution = 'Codex-iFLYTEK-Analysis'
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
function Wsl-Path([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    if ($full -notmatch '^([A-Za-z]):[\\/]') { throw 'Build from a local drive.' }
    '/mnt/' + $Matches[1].ToLowerInvariant() + '/' + $full.Substring(3).Replace('\','/')
}
function Run([string]$Exe,[string[]]$Arguments,[string]$Log) {
    & $Exe @Arguments *> $Log
    if ($LASTEXITCODE -ne 0) { Get-Content -LiteralPath $Log -Tail 30; throw "Failed: $Log" }
}
$patch = Join-Path $WorkDirectory 'patch'
$reports = Join-Path $PSScriptRoot 'reports'
$dist = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../dist'))
foreach ($dir in @($WorkDirectory,$patch,$reports,$dist)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$library = Join-Path $WorkDirectory 'libapp.so'
$nativeReport = Join-Path $patch 'native-patch.json'
$wsl = Join-Path $env:SystemRoot 'System32/wsl.exe'
Run $wsl @('-d',$Distribution,'-u','root','--cd','/root','--exec','python3',
    (Wsl-Path (Join-Path $PSScriptRoot 'patch_native.py')),(Wsl-Path $OriginalLibrary),
    (Wsl-Path $library),'--work',(Wsl-Path $patch)) (Join-Path $reports 'assemble.log')
$env:PYTHONPATH = Join-Path $ToolDirectory 'pydeps'
Run $Python @((Join-Path $PSScriptRoot 'test_native.py'),$library,(Join-Path $patch 'native-tests.json')) (Join-Path $reports 'native-tests.log')
$unsigned = Join-Path $WorkDirectory 'romania40-unsigned.apk'
$aligned = Join-Path $WorkDirectory 'romania40-aligned.apk'
$signed = Join-Path $dist 'iflytek-1.0.3899-romania40.apk'
Run $Python @((Join-Path $PSScriptRoot 'package_variant.py'),$BaselineApk,$library,$nativeReport,$unsigned) (Join-Path $reports 'package.log')
$android = Join-Path $ToolDirectory 'android-build-tools/android-16'
$java = Join-Path $Jdk 'bin/java.exe'
$signer = Join-Path $android 'lib/apksigner.jar'
$store = Join-Path $SigningDirectory 'iflytek-local.p12'
$pass = Join-Path $SigningDirectory 'signing.pass'
if (!(Test-Path -LiteralPath $store) -or !(Test-Path -LiteralPath $pass)) { throw 'Existing local signing key required.' }
Run (Join-Path $android 'zipalign.exe') @('-P','16','-f','4',$unsigned,$aligned) (Join-Path $reports 'align.log')
Run $java @('-jar',$signer,'sign','--ks',$store,'--ks-key-alias','iflytek-local','--ks-pass',"file:$pass",
    '--v1-signing-enabled','false','--v2-signing-enabled','true','--v3-signing-enabled','true',
    '--v4-signing-enabled','false','--out',$signed,$aligned) (Join-Path $reports 'sign.log')
Run $java @('-jar',$signer,'verify','--verbose','--print-certs',$signed) (Join-Path $reports 'signature.txt')
Run (Join-Path $android 'zipalign.exe') @('-c','-P','16','4',$signed) (Join-Path $reports 'alignment.txt')
Run $Python @((Join-Path $PSScriptRoot 'package_variant.py'),$BaselineApk,$library,$nativeReport,$signed,
    '--verify','--report',(Join-Path $reports 'archive-audit.json')) (Join-Path $reports 'audit.log')
foreach ($name in @('native-patch.json','native-tests.json','patch-disassembly.txt')) {
    Copy-Item -LiteralPath (Join-Path $patch $name) -Destination (Join-Path $reports $name) -Force
}
$hash = (Get-FileHash -LiteralPath $signed -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText($signed + '.sha256',$hash + '  ' + [IO.Path]::GetFileName($signed) + "`n")
Write-Output "Verified APK: $signed"
Write-Output "SHA-256: $hash"
