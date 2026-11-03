$ErrorActionPreference = 'Stop'
$lab = [System.IO.Path]::GetFullPath('D:\CodexWork\a05-r12-native-lab-n05-20261103')
$expectedParent = [System.IO.Path]::GetFullPath('D:\CodexWork')
if ((Split-Path -Parent $lab) -ne $expectedParent -or (Split-Path -Leaf $lab) -ne 'a05-r12-native-lab-n05-20261103') { throw 'Unexpected cleanup target' }
$resolved = (Resolve-Path -LiteralPath $lab).Path
if ($resolved -ne $lab) { throw 'Resolved cleanup target mismatch' }
$out = 'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\R12_fisiere\A05_N05_lot03'
$reparse = @(Get-ChildItem -LiteralPath $lab -Recurse -Force -Attributes ReparsePoint)
if ($reparse.Count -ne 0) { throw 'Reparse points require inspection; nothing removed' }
$jvm = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'java.exe' -and $_.CommandLine -like '*A05N05Launcher*' })
if ($jvm.Count -ne 0) { throw 'Own JVM remains active; no removal' }
$listenersBefore = @(Get-NetTCPConnection -LocalPort 56455 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess)
& 'D:\CodexWork\p01-local-pg16\pgsql\bin\pg_ctl.exe' -D (Join-Path $lab 'pgdata') -m fast -w stop
if ($LASTEXITCODE -ne 0) { throw 'Owned PG failed to stop' }
$listenersAfter = @(Get-NetTCPConnection -LocalPort 56455 -State Listen -ErrorAction SilentlyContinue)
if ($listenersAfter.Count -ne 0) { throw 'Port still listening; no removal' }
Copy-Item -LiteralPath (Join-Path $lab 'postgres.log') -Destination (Join-Path $out 'postgres_final.log')
$fileCount = @(Get-ChildItem -LiteralPath $lab -Recurse -File -Force).Count
Remove-Item -LiteralPath $lab -Recurse -Force
[ordered]@{
 utc = [DateTime]::UtcNow.ToString('o')
 target = $lab
 verifiedParent = $expectedParent
 reparsePoints = $reparse.Count
 ownJvmProcesses = $jvm.Count
 listenersBefore = $listenersBefore
 listenersAfter = $listenersAfter.Count
 pgStopped = $true
 filesRemoved = $fileCount
 targetExistsAfter = (Test-Path -LiteralPath $lab)
 operationalWrites = 0
 scope = 'Only A05 N05 synthetic lab. Other labs, retained Masini scratch and shared p01-local-pg16/data untouched. Runtime caches/harness preserved as passive reproducible evidence.'
} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $out 'Cleanup_final_v1.json') -Encoding utf8
Get-Content -LiteralPath (Join-Path $out 'Cleanup_final_v1.json')
