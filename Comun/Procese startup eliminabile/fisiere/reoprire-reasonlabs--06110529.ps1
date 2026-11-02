$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\reoprire-reasonlabs-log.txt'
Start-Transcript -Path $log -Force | Out-Null
$svc = 'rsClientSvc','rsEngineSvc','rsSyncSvc','rsDNSResolver','rsDNSSvc','rsVPNSvc'
foreach ($s in $svc) { Set-Service $s -StartupType Disabled -ErrorAction SilentlyContinue }
foreach ($s in $svc) { Stop-Service $s -Force -ErrorAction SilentlyContinue }
Get-Process | Where-Object { $_.Path -like '*ReasonLabs*' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
foreach ($s in $svc) { $g = Get-Service $s; "$s = $($g.Status) / $($g.StartType)" }
"Procese ramase: " + ((Get-Process | Where-Object { $_.Path -like '*ReasonLabs*' }).Name -join ', ')
Stop-Transcript | Out-Null
