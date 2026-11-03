$ErrorActionPreference='Stop'
$releasedPaths=@(
 'D:\CodexWork\a05-r12-native-lab-order-20261103',
 'D:\CodexWork\a05-r12-native-lab-g3-20261103',
 'D:\CodexWork\a05-r12-native-lab-n05-20261103'
)
$retainedPaths=@(
 'D:\CodexWork\p01-r12-masini-dates',
 'D:\CodexWork\a11-r12-mutator-20261103',
 'D:\CodexWork\a11-r12-mutator-20261103-v2',
 'D:\CodexWork\p01-r12-t343-tools-l03',
 'D:\CodexWork\p01-r12-t343-tools-l03-v2',
 'D:\CodexWork\a10-r12-l03',
 'D:\CodexWork\a11-catalog-oracle-l05-20261103',
 'D:\CodexWork\a08-catalog-json-l05-20261103'
)
$listeners=@(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object {$_.LocalPort -eq 56455} | Select-Object LocalAddress,LocalPort,OwningProcess)
$auditProcesses=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^(java|javaw|postgres|pg_ctl)\.exe$' -and $_.CommandLine -match 'a05-r12-native-lab|a08-catalog-json-l05|a11-catalog-oracle-l05'} | Select-Object ProcessId,Name,CommandLine)
$resourceReport=[ordered]@{
 utc=(Get-Date).ToUniversalTime().ToString('o')
 mode='Read-only local resource verification; no deletion or service operation'
 released_labs=@($releasedPaths | ForEach-Object {[ordered]@{path=$_;exists=(Test-Path -LiteralPath $_)}})
 listeners_56455=$listeners
 audit_lab_processes=$auditProcesses
 retained_after_automatic_rejection=@($retainedPaths | ForEach-Object {[ordered]@{path=$_;exists=(Test-Path -LiteralPath $_);reason='Earlier automatic deletion review: blocked by policy; not retried'}})
}
$resourceReport | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath 'D:\CodexWork\p01-r12-val05-resource-check.json' -Encoding utf8
$resourceReport | ConvertTo-Json -Depth 6
