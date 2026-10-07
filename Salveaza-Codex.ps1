param(
    [string]$Destinatie = (Join-Path $PSScriptRoot 'salvari'),
    [string]$CodexData = (Join-Path $env:USERPROFILE '.codex'),
    [string]$PythonExe = ''
)
$ErrorActionPreference = 'Stop'
if (-not $PythonExe) {
    $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) {
        $PythonExe = $bundledPython
    } else {
        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonCommand) { throw 'Python 3.11+ este necesar. Specificati -PythonExe cu calea executabilului.' }
        $PythonExe = $pythonCommand.Source
    }
}
$snapshotName = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$snapshotPath = Join-Path $Destinatie $snapshotName
& $PythonExe (Join-Path $PSScriptRoot 'export_codex.py') --codex-home $CodexData --output $snapshotPath
if ($LASTEXITCODE -ne 0) { throw 'Exportul nu s-a finalizat. Directorul partial este pastrat pentru diagnostic.' }
& $PythonExe (Join-Path $PSScriptRoot 'verifica_arhiva.py') $snapshotPath
if ($LASTEXITCODE -ne 0) { throw 'Verificarea arhivei a esuat. Nu marcati salvarea drept completa.' }
Write-Host "Salvare verificata: $snapshotPath"
Write-Host 'Cititi manifest.json pentru fisiere indisponibile. Salvarea nu incarca automat date in GitHub.'
