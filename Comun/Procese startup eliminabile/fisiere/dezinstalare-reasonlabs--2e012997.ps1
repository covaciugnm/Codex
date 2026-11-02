$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\dezinstalare-reasonlabs-log.txt'
Start-Transcript -Path $log -Force | Out-Null
$svc = 'rsClientSvc','rsEngineSvc','rsSyncSvc','rsDNSResolver','rsDNSSvc','rsVPNSvc'
foreach ($s in $svc) { Set-Service $s -StartupType Manual -ErrorAction SilentlyContinue }
foreach ($s in 'rsEngineSvc','rsClientSvc') { Start-Service $s -ErrorAction SilentlyContinue; "$s : $((Get-Service $s).Status)" }
Start-Sleep -Seconds 5
$p = Start-Process 'C:\Program Files\ReasonLabs\EPP\Uninstall.exe' -ArgumentList '/uninstall' -Wait -PassThru
"Uninstall exit: $($p.ExitCode)"
# asteapta procesele copil ale dezinstalarii
for ($i=0; $i -lt 60; $i++) {
    $c = Get-Process | Where-Object { $_.Path -like '*ReasonLabs*' -or $_.Path -like '*\Temp\*' -and $_.Name -match 'uninst|^Au_' }
    if (-not $c) { break }; Start-Sleep -Seconds 5
}
"Folder ramas: $(Test-Path 'C:\Program Files\ReasonLabs\EPP')"
Stop-Transcript | Out-Null
