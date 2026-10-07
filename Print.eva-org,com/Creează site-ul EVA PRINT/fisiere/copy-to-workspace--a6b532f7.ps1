$ErrorActionPreference = 'Stop'
$packageSource = 'C:\Users\User\.codex\visualizations\2026\10\02\01a0fbd7-f9a0-7df1-839f-a3792ebc6e66\EVA_PRINT_WEBSITE_BRIEF_2026-10-02'
$workspaceTarget = '\\192.168.100.151\site-uri\print.eva-org.com'
$packageTarget = [System.IO.Path]::GetFullPath((Join-Path $workspaceTarget 'EVA_PRINT_WEBSITE_BRIEF_2026-10-02'))
$resolvedWorkspace = (Resolve-Path -LiteralPath $workspaceTarget).ProviderPath.TrimEnd('\')
if (-not $packageTarget.StartsWith($resolvedWorkspace + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Destination is outside the intended workspace.' }
if (Test-Path -LiteralPath $packageTarget) {
    if (-not (Test-Path -LiteralPath (Join-Path $packageTarget '00_README\START_HERE_EN.txt'))) { throw 'Existing destination is not this generated package.' }
} else {
    New-Item -ItemType Directory -Path $packageTarget | Out-Null
}
# Install the package-level HTTP denial files before copying private reference resources.
foreach ($denialName in @('web.config','.htaccess')) {
    Copy-Item -LiteralPath (Join-Path $packageSource $denialName) -Destination (Join-Path $packageTarget $denialName) -Force
}
$copiedCount = 0
$copiedBytes = [long]0
foreach ($packageFile in (Get-ChildItem -LiteralPath $packageSource -Recurse -File -Force)) {
    $relativePackagePath = $packageFile.FullName.Substring($packageSource.Length).TrimStart('\')
    if ($relativePackagePath -match '(^|\\)(__MACOSX|python_libs|postgres-runtime)(\\|$)') { continue }
    $fileTarget = [System.IO.Path]::GetFullPath((Join-Path $packageTarget $relativePackagePath))
    if (-not $fileTarget.StartsWith($packageTarget + '\',[System.StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe destination file path.' }
    $parentTarget = [System.IO.Path]::GetDirectoryName($fileTarget)
    if (-not (Test-Path -LiteralPath $parentTarget)) { New-Item -ItemType Directory -Path $parentTarget | Out-Null }
    if (Test-Path -LiteralPath $fileTarget) {
        $existingPackageFile = Get-Item -LiteralPath $fileTarget -Force
        if ($existingPackageFile.Length -eq $packageFile.Length -and $existingPackageFile.LastWriteTimeUtc -eq $packageFile.LastWriteTimeUtc) { continue }
    }
    Copy-Item -LiteralPath $packageFile.FullName -Destination $fileTarget -Force
    $copiedCount++
    $copiedBytes += $packageFile.Length
    if ($copiedCount % 250 -eq 0) { Write-Output "Copied $copiedCount files" }
}
[pscustomobject]@{ Destination=$packageTarget; Files=$copiedCount; Bytes=$copiedBytes } | ConvertTo-Json
