[CmdletBinding()]
param(
    [string]$InputApk = (Join-Path $PSScriptRoot '../Biblioteca_Glasses/Aplicatii/iflytranslate-official.apk'),
    [string]$Jdk = 'C:\Program Files\Java\jdk-21',
    [string]$ToolDirectory = 'D:\CodexWork\iflytek-build-tools',
    [string]$WorkDirectory = 'D:\CodexWork\iflytek-build-work',
    [string]$SigningDirectory = 'D:\CodexWork\iflytek-build-private',
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'dist'),
    [ValidateSet('Full','BinaryResources')][string]$Mode = 'Full',
    [switch]$VerifyRoundTrip,
    [switch]$AllowCodeChanges
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$InputApk = (Resolve-Path -LiteralPath $InputApk).Path
$ToolDirectory = [IO.Path]::GetFullPath($ToolDirectory)
$WorkDirectory = [IO.Path]::GetFullPath($WorkDirectory)
$SigningDirectory = [IO.Path]::GetFullPath($SigningDirectory)
$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
$java = Join-Path $Jdk 'bin/java.exe'
$keytool = Join-Path $Jdk 'bin/keytool.exe'
if (!(Test-Path -LiteralPath $java)) { throw "Missing JDK: $Jdk" }
& (Join-Path $PSScriptRoot 'Setup-Tools.ps1') -ToolDirectory $ToolDirectory
$expected = '73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2'
$inputHash = (Get-FileHash -LiteralPath $InputApk -Algorithm SHA256).Hash.ToLowerInvariant()
if ($inputHash -ne $expected) { throw 'This project is pinned to the verified official APK 1.0.3899. Unexpected input hash.' }
$variant = if ($Mode -eq 'Full') { 'full' } else { 'binary-resources' }
$decoded = Join-Path $WorkDirectory "decoded-$variant"
$logs = Join-Path $WorkDirectory 'logs'
$tmp = Join-Path $WorkDirectory 'tmp'
$framework = Join-Path $WorkDirectory 'framework'
$reports = Join-Path $PSScriptRoot "reports/$variant"
foreach ($dir in @($WorkDirectory,$logs,$tmp,$framework,$OutputDirectory,$reports)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
$apktool = Join-Path $ToolDirectory 'apktool_3.0.3.jar'
$android = Join-Path $ToolDirectory 'android-build-tools/android-16'
$signer = Join-Path $android 'lib/apksigner.jar'
$javaArgs = @('-Xmx4g',"-Djava.io.tmpdir=$tmp")
function Run-Logged {
    param([string]$Exe,[string[]]$Arguments,[string]$Log)
    & $Exe @Arguments *> $Log
    $result = $LASTEXITCODE
    if ($result -ne 0) {
        Get-Content -LiteralPath $Log -Tail 45 | Write-Host
        throw "Command failed with exit code $result. See $Log"
    }
}
if (!(Test-Path -LiteralPath $decoded)) {
    $decodeArgs = $javaArgs + @('-jar',$apktool,'d',$InputApk,'-o',$decoded,'-p',$framework,'-j','4')
    if ($Mode -eq 'BinaryResources') { $decodeArgs += '-r' }
    Run-Logged -Exe $java -Arguments $decodeArgs -Log (Join-Path $logs "decode-$variant.log")
    Set-Content -LiteralPath (Join-Path $decoded '.input-sha256') -Value $inputHash -Encoding ascii
} else {
    $stamp = Join-Path $decoded '.input-sha256'
    if (!(Test-Path -LiteralPath $stamp) -or (Get-Content -LiteralPath $stamp -Raw).Trim() -ne $inputHash) {
        throw 'Existing decoded folder has no matching source stamp. Choose a fresh WorkDirectory; existing edits are preserved.'
    }
}
$unsigned = Join-Path $WorkDirectory "iflytek-$variant-unsigned.apk"
$aligned = Join-Path $WorkDirectory "iflytek-$variant-aligned.apk"
$signed = Join-Path $OutputDirectory "iflytek-1.0.3899-$variant-rebuilt.apk"
Run-Logged -Exe $java -Arguments ($javaArgs + @('-jar',$apktool,'b',$decoded,'-p',$framework,'-j','4','-o',$unsigned)) -Log (Join-Path $logs "build-$variant.log")
Run-Logged -Exe (Join-Path $android 'zipalign.exe') -Arguments @('-P','16','-f','4',$unsigned,$aligned) -Log (Join-Path $logs "align-$variant.log")
# A private local development key is kept outside the repository and distribution folder.
$projectPath = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\') + '\'
if ($SigningDirectory.StartsWith($projectPath,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'SigningDirectory must be outside the distributable project.'
}
New-Item -ItemType Directory -Path $SigningDirectory -Force | Out-Null
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
& (Join-Path $env:SystemRoot 'System32/icacls.exe') $SigningDirectory /inheritance:r /grant:r "*$($sid):(OI)(CI)F" '*S-1-5-18:(OI)(CI)F' *> (Join-Path $logs 'key-directory-acl.log')
if ($LASTEXITCODE -ne 0) { throw 'Could not restrict permissions on the private signing directory.' }
$store = Join-Path $SigningDirectory 'iflytek-local.p12'
$passfile = Join-Path $SigningDirectory 'signing.pass'
if (!(Test-Path -LiteralPath $store)) {
    if (Test-Path -LiteralPath $passfile) { throw 'Incomplete key state. Preserve it and choose a new SigningDirectory.' }
    $bytes = New-Object byte[] 32
    $rng = [Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    $rng.Dispose()
    [IO.File]::WriteAllText($passfile,[Convert]::ToBase64String($bytes),[Text.UTF8Encoding]::new($false))
    Run-Logged -Exe $keytool -Arguments @('-genkeypair','-alias','iflytek-local','-keyalg','RSA','-keysize','3072','-validity','3650','-storetype','PKCS12','-keystore',$store,'-storepass:file',$passfile,'-keypass:file',$passfile,'-dname','CN=iFLYTEK Local Research, OU=Rebuild, O=Local, C=RO') -Log (Join-Path $logs 'generate-local-key.log')
}
if (!(Test-Path -LiteralPath $passfile)) { throw 'Missing password file for the existing local signing key.' }
Run-Logged -Exe $java -Arguments @('-jar',$signer,'sign','--ks',$store,'--ks-key-alias','iflytek-local','--ks-pass',"file:$passfile",'--v1-signing-enabled','false','--v2-signing-enabled','true','--v3-signing-enabled','true','--v4-signing-enabled','false','--out',$signed,$aligned) -Log (Join-Path $logs "sign-$variant.log")
Run-Logged -Exe $java -Arguments @('-jar',$signer,'verify','--verbose','--print-certs',$signed) -Log (Join-Path $reports 'signature.txt')
Run-Logged -Exe (Join-Path $android 'zipalign.exe') -Arguments @('-c','-P','16','4',$signed) -Log (Join-Path $reports 'alignment.txt')
Run-Logged -Exe (Join-Path $android 'aapt2.exe') -Arguments @('dump','badging',$InputApk) -Log (Join-Path $reports 'original-badging.txt')
Run-Logged -Exe (Join-Path $android 'aapt2.exe') -Arguments @('dump','badging',$signed) -Log (Join-Path $reports 'rebuilt-badging.txt')
Run-Logged -Exe (Join-Path $android 'aapt2.exe') -Arguments @('dump','xmltree',$InputApk,'--file','AndroidManifest.xml') -Log (Join-Path $reports 'original-manifest-tree.txt')
Run-Logged -Exe (Join-Path $android 'aapt2.exe') -Arguments @('dump','xmltree',$signed,'--file','AndroidManifest.xml') -Log (Join-Path $reports 'rebuilt-manifest-tree.txt')
& node (Join-Path $PSScriptRoot 'Audit-APK.cjs') $InputApk $signed (Join-Path $reports 'archive-audit.json')
if ($LASTEXITCODE -ne 0) { throw 'Archive audit failed.' }
$badgingIdentical = (Get-FileHash -LiteralPath (Join-Path $reports 'original-badging.txt')).Hash -eq (Get-FileHash -LiteralPath (Join-Path $reports 'rebuilt-badging.txt')).Hash
$manifestIdentical = (Get-FileHash -LiteralPath (Join-Path $reports 'original-manifest-tree.txt')).Hash -eq (Get-FileHash -LiteralPath (Join-Path $reports 'rebuilt-manifest-tree.txt')).Hash
$manifestOriginal = (Get-Content -LiteralPath (Join-Path $reports 'original-manifest-tree.txt') -Raw) -replace '\(line=\d+\)',''
$manifestRebuilt = (Get-Content -LiteralPath (Join-Path $reports 'rebuilt-manifest-tree.txt') -Raw) -replace '\(line=\d+\)',''
$manifestEquivalent = $manifestOriginal -ceq $manifestRebuilt
$badgingOriginal = (Get-Content -LiteralPath (Join-Path $reports 'original-badging.txt') -Raw) -replace "res/[^'\r\n]+",'RESOURCE_PATH'
$badgingRebuilt = (Get-Content -LiteralPath (Join-Path $reports 'rebuilt-badging.txt') -Raw) -replace "res/[^'\r\n]+",'RESOURCE_PATH'
$badgingEquivalent = $badgingOriginal -ceq $badgingRebuilt
if (!$manifestEquivalent) { throw 'Manifest values changed. Inspect the two manifest-tree reports.' }
if (!$badgingEquivalent) { throw 'Android package metadata changed. Inspect the badging reports.' }
$outputHash = (Get-FileHash -LiteralPath $signed -Algorithm SHA256).Hash.ToLowerInvariant()
if ($VerifyRoundTrip) {
    & node (Join-Path $PSScriptRoot 'test-verifier.cjs')
    if ($LASTEXITCODE -ne 0) { throw 'Equivalence verifier self-check failed.' }
    $proof = Join-Path $WorkDirectory ("proof-" + $outputHash.Substring(0,12))
    if (!(Test-Path -LiteralPath $proof)) {
        $proofArgs = $javaArgs + @('-jar',$apktool,'d',$signed,'-o',$proof,'-p',$framework,'-j','4')
        if ($Mode -eq 'BinaryResources') { $proofArgs += '-r' }
        Run-Logged -Exe $java -Arguments $proofArgs -Log (Join-Path $logs "proof-$variant.log")
    }
    & node (Join-Path $PSScriptRoot 'Compare-Decoded.cjs') $decoded $proof (Join-Path $reports 'roundtrip.json')
    if ($LASTEXITCODE -ne 0 -and !$AllowCodeChanges) { throw 'Smali or resources differ after rebuild. Inspect the roundtrip report.' }
}
$report = [ordered]@{
    schemaVersion=1; variant=$variant; package='com.iflytek.translateapp';version='1.0.3899';
    inputSha256=$inputHash;outputSha256=$outputHash;outputApk=$signed;decodedProject=$decoded;
    bytecodeReassembled=$true; resourcesRecompiled=($Mode -eq 'Full');
    signatureVerified=$true;zipAlignmentVerified=$true;badgingIdentical=$badgingIdentical;manifestTreeIdentical=$manifestIdentical;
    manifestValuesEquivalent=$manifestEquivalent;badgingEquivalentExceptResourcePaths=$badgingEquivalent;
    roundTripRequested=[bool]$VerifyRoundTrip; deviceInstallationTested=$false; deviceLaunchTested=$false;
    loginTested=$false; glassesTested=$false; nativeAndFlutterSourcesRecovered=$false;
    signing='Local research key; not the manufacturer signature.';
    tools=@{apktool='3.0.3';androidBuildTools='36.0.0';platformTools='37.0.1';java=(& $java -version 2>&1 | Out-String).Trim()}
}
$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $reports 'build-result.json') -Encoding utf8
"$outputHash  $([IO.Path]::GetFileName($signed))" | Set-Content -LiteralPath ($signed + '.sha256') -Encoding ascii
Write-Host "Built and signed: $signed"
Write-Host "SHA256: $outputHash"
Write-Host 'Runtime, login and glasses compatibility require separate testing.'
