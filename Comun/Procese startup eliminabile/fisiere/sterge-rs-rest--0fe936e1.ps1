$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\rs-cleanup.txt'
& C:\Windows\System32\sc.exe delete rsSyncSvc *>&1 | Out-File $log
Remove-Item 'C:\ProgramData\ReasonLabs' -Recurse -Force -ErrorAction SilentlyContinue
"ProgramData ReasonLabs ramas: $(Test-Path 'C:\ProgramData\ReasonLabs')" | Out-File $log -Append
