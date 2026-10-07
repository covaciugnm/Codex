$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath 'S:\dracula-design').Path.TrimEnd('\')
$local = 'C:\Users\User\Documents\Codex\2026-09-25\cre\outputs\dracula-design-office\dist\assets'
$items = @(
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35.jpeg';Folder='01-brand';Name='dracula-design-logo-auriu.jpeg';Web='brand'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (4).jpeg';Folder='02-produse';Name='dracula-design-rucsac-business.jpeg';Web='produse'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (5).jpeg';Folder='02-produse';Name='dracula-design-servieta-business.jpeg';Web='produse'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (6).jpeg';Folder='02-produse';Name='dracula-design-portofel.jpeg';Web='produse'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (7).jpeg';Folder='02-produse';Name='dracula-design-geanta-tote.jpeg';Web='produse'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (8).jpeg';Folder='02-produse';Name='dracula-design-esarfa-signature.jpeg';Web='produse'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (9).jpeg';Folder='04-atmosfera';Name='dracula-design-editorial-feminin.jpeg';Web='atmosfera'},
 @{Old='dracula-design-bags.jpeg';Folder='03-colectii';Name='dracula-design-colectie-business.jpeg';Web='colectii'},
 @{Old='WhatsApp Image 2026-09-25 at 16.38.35 (3).jpeg';Folder='99-duplicate';Name='dracula-design-colectie-business-duplicat.jpeg';Web=$null}
)
$inventory = foreach($item in $items){
 $source = Join-Path $root $item.Old
 $folder = Join-Path $root $item.Folder
 $target = [IO.Path]::GetFullPath((Join-Path $folder $item.Name))
 if(-not $target.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Destination outside project'}
 if(-not (Test-Path -LiteralPath $source)){throw "Missing source: $source"}
 if(Test-Path -LiteralPath $target){throw "Destination already exists: $target"}
 New-Item -ItemType Directory -Path $folder -Force | Out-Null
 $before = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
 Move-Item -LiteralPath $source -Destination $target
 $after = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
 if($before -ne $after){throw 'Hash mismatch'}
 if($item.Web){$webFolder=Join-Path $local $item.Web;New-Item -ItemType Directory -Path $webFolder -Force | Out-Null;Copy-Item -LiteralPath $target -Destination (Join-Path $webFolder $item.Name)}
 [PSCustomObject]@{NumeInitial=$item.Old;CaleNoua=$item.Folder+'/'+$item.Name;SHA256=$after}
}
$inventory | Export-Csv -LiteralPath (Join-Path $root 'inventar-imagini.csv') -NoTypeInformation -Encoding UTF8
$inventory | Export-Csv -LiteralPath 'C:\Users\User\Documents\Codex\2026-09-25\cre\outputs\dracula-design-office\inventar-imagini.csv' -NoTypeInformation -Encoding UTF8
Write-Output "Organized $($inventory.Count) images; originals preserved byte for byte; duplicate retained."
