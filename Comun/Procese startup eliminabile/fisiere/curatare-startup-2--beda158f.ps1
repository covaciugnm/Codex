# Curatare startup runda 2 - 30.10.2026. Ruleaza ca administrator.
$log = 'C:\Users\User\Documents\Backup-Startup-2026-10-30\curatare-log-2.txt'
Start-Transcript -Path $log -Force | Out-Null

"=== SERVICII ==="
$servicii = 'Autodesk Access Service Host','Autodesk CER Service',
            'EasyTuneEngineService','GBTECService','OCButtonService','GigabyteUpdateService',
            'Wms','WmsRepair'
foreach ($s in $servicii) {
    try {
        Set-Service -Name $s -StartupType Disabled -ErrorAction Stop
        Stop-Service -Name $s -Force -ErrorAction SilentlyContinue
        "OK   $s -> Disabled ($((Get-Service $s).Status))"
    } catch { "EROARE $s : $($_.Exception.Message)" }
}
Get-Process -Name 'AdskAccessService*','GCC','LiquidSensord','GraphicsCardEngine*','browser_assistant','Weixin' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

"=== TASK-URI PROGRAMATE ==="
$tasks = Get-ScheduledTask | Where-Object {
    $_.TaskName -like 'Opera scheduled*' -or
    $_.TaskPath -eq '\cFos\Registration Tasks\' -or
    $_.TaskName -in 'GCC','GraphicsCardEngine','GBTECService' -or
    $_.TaskName -like 'OneDrive *'
}
foreach ($t in $tasks) {
    try { Disable-ScheduledTask -TaskName $t.TaskName -TaskPath $t.TaskPath -ErrorAction Stop | Out-Null; "OK   $($t.TaskPath)$($t.TaskName)" }
    catch { "EROARE $($t.TaskPath)$($t.TaskName) : $($_.Exception.Message)" }
}

"=== RUN (Autodesk sters din HKLM) ==="
$k = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
foreach ($n in 'Autodesk Access Service') {
    if (Get-ItemProperty -Path $k -Name $n -ErrorAction SilentlyContinue) { Remove-ItemProperty -Path $k -Name $n; "OK   sters $n" } else { "--   $n nu exista" }
}
$ka = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run'
if (Get-ItemProperty -Path $ka -Name 'Autodesk Access Service' -ErrorAction SilentlyContinue) { Remove-ItemProperty -Path $ka -Name 'Autodesk Access Service'; "OK   sters StartupApproved Autodesk" }

"=== APLICATII UTILIZATOR (dezactivate ca in Task Manager, reversibil) ==="
$sa = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run'
$off = [byte[]](3,0,0,0,0,0,0,0,0,0,0,0)
foreach ($n in 'Opera Stable','Opera Browser Assistant','Weixin','Discord','Teams') {
    try { New-ItemProperty -Path $sa -Name $n -PropertyType Binary -Value $off -Force -ErrorAction Stop | Out-Null; "OK   $n -> dezactivat la startup" }
    catch { "EROARE $n : $($_.Exception.Message)" }
}

"=== APLICATII STORE (WhatsApp, iCloud, Widgets, Teams) ==="
$base = 'HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData'
$uwp = 'AppleInc.iCloud_nzyj5cx40ttqa\iCloudHomeStartupTask',
       '5319275A.WhatsAppDesktop_cv1g1gvanyjgm\WhatsAppStartupTask',
       '48405AmbientSoftware.WidgetsFree_agy8jafheqhng\WidgetsDesktopTask',
       'MSTeams_8wekyb3d8bbwe\TeamsTfwStartupTask'
foreach ($u in $uwp) {
    $p = Join-Path $base $u
    if (Test-Path $p) {
        $st = (Get-ItemProperty $p).State
        if ($st -eq 2 -or $st -eq 4) { Set-ItemProperty -Path $p -Name State -Value 1 -Type DWord; "OK   $u -> dezactivat (era $st)" } else { "--   $u deja dezactivat ($st)" }
    } else { "--   $u nu exista" }
}
Stop-Transcript | Out-Null
