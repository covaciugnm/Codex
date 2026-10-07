param([Parameter(Mandatory=$true)][string]$DestinationPath)
$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path -Parent $PSScriptRoot
$expectedLeaf = 'Cercetare_si_arhitectura_robotica_2026-10-02'
if ((Split-Path -Leaf $DestinationPath) -ne $expectedLeaf) { throw 'Unexpected destination leaf' }
$manifestPath = Join-Path $sourceRoot 'MANIFEST_SHA256.json'
$manifest = Get-Content -LiteralPath $manifestPath -Encoding UTF8 -Raw | ConvertFrom-Json
foreach($entry in $manifest.files) {
  $sourceFile = Join-Path $sourceRoot $entry.path
  if ((Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { throw "Source changed: $($entry.path)" }
}
New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
Get-ChildItem -LiteralPath $sourceRoot | Copy-Item -Destination $DestinationPath -Recurse -Force
$mismatches = @()
foreach($entry in $manifest.files) {
  $destFile = Join-Path $DestinationPath $entry.path
  if (!(Test-Path -LiteralPath $destFile) -or (Get-FileHash -LiteralPath $destFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { $mismatches += $entry.path }
}
$tracked = @{}
foreach($entry in $manifest.files){ $tracked[$entry.path] = $true }
foreach($excluded in $manifest.excludes){ $tracked[$excluded] = $true }
$extra = @()
Get-ChildItem -LiteralPath $DestinationPath -File -Recurse | ForEach-Object {
  $relative = $_.FullName.Substring($DestinationPath.TrimEnd('\').Length + 1).Replace('\','/')
  if (!$tracked.ContainsKey($relative)) { $extra += $relative }
}
$manifestHash = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ((Get-FileHash -LiteralPath (Join-Path $DestinationPath 'MANIFEST_SHA256.json') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $manifestHash) { $mismatches += 'MANIFEST_SHA256.json' }
$proof = [ordered]@{at=[DateTime]::UtcNow.ToString('o'); status=$(if($mismatches.Count -eq 0 -and $extra.Count -eq 0){'verified'}else{'failed'}); source=$sourceRoot; destination=$DestinationPath; files_checked=$manifest.files.Count; manifest_sha256=$manifestHash; mismatches=$mismatches; extra=$extra; scope='File identity and complete copy; not physical or application validation'}
$proofText = $proof | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText((Join-Path $sourceRoot 'LIVRARE_CONFIRMATA.json'),$proofText,[System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $DestinationPath 'LIVRARE_CONFIRMATA.json'),$proofText,[System.Text.UTF8Encoding]::new($false))
$proofText
if($proof.status -ne 'verified'){throw 'Delivery verification failed'}
