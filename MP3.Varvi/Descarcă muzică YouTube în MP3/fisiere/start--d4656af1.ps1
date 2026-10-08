$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonExe = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    $pyCommand = Get-Command py -ErrorAction SilentlyContinue
    if ($pythonCommand) { & $pythonCommand.Source -m venv .venv }
    elseif ($pyCommand) { & $pyCommand.Source -3 -m venv .venv }
    else { throw 'Instalează Python 3.11 sau mai nou, apoi pornește din nou.' }
    if ($LASTEXITCODE -ne 0) { throw 'Crearea mediului Python a eșuat.' }
}
& $pythonExe -m pip install -r requirements.txt --disable-pip-version-check --no-cache-dir
if ($LASTEXITCODE -ne 0) { throw 'Instalarea dependențelor a eșuat. Verifică internetul.' }
Write-Host 'Deschide http://127.0.0.1:8765 în browser. Pentru oprire: Ctrl+C.'
& $pythonExe app.py
