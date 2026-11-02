# Curatare startup - 30.10.2026. Ruleaza ca administrator. Backup in acelasi folder.
$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\curatare-log.txt'
Start-Transcript -Path $log -Force | Out-Null

"=== SERVICII ==="
$servicii = 'rsClientSvc','rsEngineSvc','rsSyncSvc','rsDNSResolver','rsDNSSvc','rsVPNSvc',
            'QMEmulatorService','simptcp','cFosSpeedS','DSAService','DSAUpdateService'
foreach ($s in $servicii) {
    try {
        Set-Service -Name $s -StartupType Disabled -ErrorAction Stop
        Stop-Service -Name $s -Force -ErrorAction SilentlyContinue
        $st = (Get-Service $s).Status
        "OK   $s -> Disabled ($st)"
    } catch { "EROARE $s : $($_.Exception.Message)" }
}

"=== TASK-URI PROGRAMATE ==="
$tasks = Get-ScheduledTask | Where-Object {
    $_.TaskName -like 'AVGBrowserProtect*' -or
    $_.TaskName -eq 'Adobe Acrobat Update Task' -or
    $_.TaskPath -eq '\GoogleUserPEH\' -or
    $_.TaskName -like 'Firefox Default Browser Agent*' -or
    $_.TaskPath -like '\SoftLanding\*' -or
    $_.TaskName -eq 'RevoHelperFreeStartup'
}
foreach ($t in $tasks) {
    try { Disable-ScheduledTask -TaskName $t.TaskName -TaskPath $t.TaskPath -ErrorAction Stop | Out-Null; "OK   $($t.TaskPath)$($t.TaskName)" }
    catch { "EROARE $($t.TaskPath)$($t.TaskName) : $($_.Exception.Message)" }
}

"=== INTRARI RUN ==="
$run = @{
  'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' = 'Gigabyte Speed','AdobeAAMUpdater-1.0','Logi Download Assistant'
  'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' = 'Adobe CCXProcess','CheckNDISPort58ac13','CancelAutoPlay_df','Acrobat Assistant 8.0','TeamsMachineUninstallerLocalAppData','TeamsMachineUninstallerProgramData'
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run' = 'Gigabyte Speed','Logitech Download Assistant','AdobeAAMUpdater-1.0','AdobeGCInvoker-1.0'
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run32' = 'Adobe CCXProcess','TeamsMachineInstaller','CancelAutoPlay_df','CheckNDISPort58ac13','Acrobat Assistant 8.0'
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run' = 'GoogleUpdaterTaskUser128.0.6537.0','GoogleUpdaterTaskUser128.0.6597.0','GoogleUpdaterTaskUser129.0.6651.0','GoogleUpdaterTaskUser136.0.7079.0','GoogleUpdaterTaskUser138.0.7156.0','GoogleUpdaterTaskUser148.0.7730.0','Logitech Download Assistant'
}
foreach ($k in $run.Keys) {
    foreach ($n in $run[$k]) {
        if (Get-ItemProperty -Path $k -Name $n -ErrorAction SilentlyContinue) {
            try { Remove-ItemProperty -Path $k -Name $n -ErrorAction Stop; "OK   $n  ($k)" } catch { "EROARE $n : $($_.Exception.Message)" }
        } else { "--   $n nu exista ($k)" }
    }
}
Stop-Transcript | Out-Null
