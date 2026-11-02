$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $env:TEMP
$sourcePath = 'C:\Users\User\Documents\Codex'
$destinationPath = 'D:\ChatGPT_local\Codex'
$backupPath = 'C:\Users\User\Documents\Codex-before-move'
try {
    $sourceItem = Get-Item -LiteralPath $sourcePath
    if ($sourceItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Codex is already a link. No changes made.' }
    if ($sourceItem.FullName -ne $sourcePath) { throw 'Unexpected source path.' }
    if (Test-Path -LiteralPath $backupPath) { throw 'Backup path already exists.' }
    if (Test-Path -LiteralPath $destinationPath) { throw 'Destination already exists. No changes made.' }
    $links = @(Get-ChildItem -LiteralPath $sourcePath -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
    if ($links.Count) { throw 'Source contains symbolic links; manual inspection required.' }
    New-Item -ItemType Directory -Path $destinationPath | Out-Null
    & robocopy $sourcePath $destinationPath /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ
    if ($LASTEXITCODE -ge 8) { throw 'Copy failed. Original files retained.' }
    $sourceFiles = @(Get-ChildItem -LiteralPath $sourcePath -Recurse -Force -File)
    $destinationFiles = @(Get-ChildItem -LiteralPath $destinationPath -Recurse -Force -File)
    if ($sourceFiles.Count -ne $destinationFiles.Count) { throw 'File counts differ. Original files retained.' }
    foreach ($file in $sourceFiles) {
        $relativePath = $file.FullName.Substring($sourcePath.Length + 1)
        $targetPath = Join-Path $destinationPath $relativePath
        if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $targetPath).Hash) { throw "Verification failed: $relativePath" }
    }
    Rename-Item -LiteralPath $sourcePath -NewName 'Codex-before-move'
    try {
        New-Item -ItemType Junction -Path $sourcePath -Target $destinationPath | Out-Null
    } catch {
        Rename-Item -LiteralPath $backupPath -NewName 'Codex'
        throw
    }
    $junction = Get-Item -LiteralPath $sourcePath
    if ($junction.LinkType -ne 'Junction' -or $junction.Target -ne $destinationPath) { throw 'Link verification failed. Backup retained.' }
    if ((Get-Item -LiteralPath $backupPath).FullName -ne 'C:\Users\User\Documents\Codex-before-move') { throw 'Unexpected backup path.' }
    Remove-Item -LiteralPath $backupPath -Recurse -Force
    Write-Host "Done. $($sourceFiles.Count) files verified. Codex now uses $destinationPath through the original path." -ForegroundColor Green
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host 'Stopped. Do not delete retained original or backup folders.'
}
Read-Host 'Press Enter to close'
