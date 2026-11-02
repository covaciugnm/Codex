$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\opreste-procese-log.txt'
Stop-ScheduledTask -TaskName RevoHelperFreeStartup -ErrorAction SilentlyContinue
Get-Process AppMarket,cef_frame_render,RevoUninHelper,GameLoop* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
"Ramase: " + ((Get-Process AppMarket,cef_frame_render,RevoUninHelper -ErrorAction SilentlyContinue).Name -join ', ') | Out-File $log
