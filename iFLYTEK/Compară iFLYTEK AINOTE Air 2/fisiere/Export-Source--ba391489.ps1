[CmdletBinding()]
param(
    [string]$DecodedDirectory='D:\CodexWork\iflytek-build-work\decoded-full',
    [string]$Jdk='C:\Program Files\Java\jdk-21',
    [string]$OutputDirectory=(Join-Path $PSScriptRoot 'dist'),
    [string]$ReportFile=(Join-Path $PSScriptRoot 'reports/source-export.json')
)
$ErrorActionPreference='Stop'
if (!(Test-Path -LiteralPath (Join-Path $DecodedDirectory '.input-sha256'))) { throw 'Missing verified source stamp.' }
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$destination=Join-Path $OutputDirectory 'iflytek-1.0.3899-editable-source.zip'
$arguments=@('--create','--file',$destination,'--no-manifest')
foreach ($entry in @('apktool.yml','.input-sha256','AndroidManifest.xml','assets','lib','res','smali','smali_classes2','smali_classes3','smali_classes4','smali_classes5','smali_classes6','unknown','original')) {
    if (Test-Path -LiteralPath (Join-Path $DecodedDirectory $entry)) { $arguments+=@('-C',$DecodedDirectory,$entry) }
}
& (Join-Path $Jdk 'bin/jar.exe') @arguments
if ($LASTEXITCODE -ne 0) { throw 'Source archive failed.' }
$entries=@(& (Join-Path $Jdk 'bin/jar.exe') --list --file $destination)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read source archive.' }
$files=@($entries | Where-Object {$_ -notmatch '/$'})
$smali=@($files | Where-Object {$_ -match '^smali(?:_classes\d+)?/.*\.smali$'}).Count
$native=@($files | Where-Object {$_ -match '^lib/.*\.so$'}).Count
$assets=@($files | Where-Object {$_ -match '^assets/'}).Count
# Only root build/cache directories are forbidden: org/apache/commons/io/build is application code.
$forbidden=@($files | Where-Object {$_ -match '^(build|tmp|private)/|\.(p12|jks|pass)$'})
if ($smali -ne 47219 -or $native -ne 80 -or $assets -ne 1046 -or $forbidden.Count -ne 0) { throw 'Source archive inventory mismatch.' }
$hash=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
"$hash  $([IO.Path]::GetFileName($destination))" | Set-Content -LiteralPath ($destination+'.sha256') -Encoding ascii
$report=[ordered]@{status='PASS';file='dist/iflytek-1.0.3899-editable-source.zip';sha256=$hash;bytes=(Get-Item -LiteralPath $destination).Length;totalFiles=$files.Count;smaliFiles=$smali;nativeLibraries=$native;assets=$assets;privateKeyOrCacheFiles=$forbidden.Count}
New-Item -ItemType Directory -Path (Split-Path -Parent $ReportFile) -Force | Out-Null
$report | ConvertTo-Json | Set-Content -LiteralPath $ReportFile -Encoding utf8
Write-Host "Exported editable Smali/resources plus preserved native/Flutter binaries: $destination"
