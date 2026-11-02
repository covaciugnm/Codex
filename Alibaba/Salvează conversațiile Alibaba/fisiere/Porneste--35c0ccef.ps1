$ErrorActionPreference = 'Stop'
$taskConfig = Get-Content (Join-Path $PSScriptRoot 'config.json') -Raw | ConvertFrom-Json
$taskPython = 'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$taskRunning = $false
try { $taskStatus = Invoke-RestMethod 'http://127.0.0.1:8766/control/status' -Headers @{'X-Archive-Key'=$taskConfig.token} -TimeoutSec 4; $taskRunning = $null -ne $taskStatus.running } catch {}
if (-not $taskRunning) {
    $taskProcess = Start-Process -FilePath $taskPython -ArgumentList ('"'+(Join-Path $PSScriptRoot 'launcher.py')+'"') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $PSScriptRoot 'launcher-output.log') -RedirectStandardError (Join-Path $PSScriptRoot 'launcher-error.log') -PassThru
    $taskProcess.Id | Set-Content (Join-Path $PSScriptRoot 'launcher.pid')
    for ($taskAttempt=0; $taskAttempt -lt 15; $taskAttempt++) {
        Start-Sleep -Milliseconds 400
        try { $taskStatus = Invoke-RestMethod 'http://127.0.0.1:8766/control/status' -Headers @{'X-Archive-Key'=$taskConfig.token} -TimeoutSec 4; $taskRunning = $null -ne $taskStatus.running; if ($taskRunning) { break } } catch {}
    }
}
if (-not $taskRunning) { throw 'Lansatorul nu a pornit. Vezi launcher-error.log.' }
try { Invoke-RestMethod 'http://127.0.0.1:8766/control/start' -Method Post -Headers @{'X-Archive-Key'=$taskConfig.token} -TimeoutSec 20 | Out-Null } catch { Write-Warning 'Serverul de comunicare nu a pornit. Poti reincerca din pagina arhivei.' }
if (-not $env:ALIBABA_NO_BROWSER) { Start-Process 'http://127.0.0.1:8766/' }
