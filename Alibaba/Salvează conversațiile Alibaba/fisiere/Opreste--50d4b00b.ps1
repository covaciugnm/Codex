$ErrorActionPreference = 'Stop'
$taskPidFile = Join-Path $PSScriptRoot 'server.pid'
if (-not (Test-Path -LiteralPath $taskPidFile)) { return }
$taskServerPid = [int](Get-Content -LiteralPath $taskPidFile)
$taskProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $taskServerPid"
$taskScript = Join-Path $PSScriptRoot 'server.py'
if ($taskProcess -and $taskProcess.CommandLine.Contains($taskScript)) {
    Stop-Process -Id $taskServerPid
}
