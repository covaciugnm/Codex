$ErrorActionPreference='Stop'
$taskDir=Join-Path (Split-Path -Parent $PSScriptRoot) '08. Corespondenta\2026.10.05 Actualizare comunicari'
$taskItems=Get-Content -LiteralPath (Join-Path $taskDir '2026.10.05 Descarcari originale.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskOut=Join-Path $taskDir '2026.10.05 Atasamente'
New-Item -ItemType Directory -Path $taskOut -Force | Out-Null
foreach($taskItem in $taskItems){
 $taskPath=Join-Path $taskOut ('2026.10.05 '+$taskItem.id.Substring(0,8)+' '+$taskItem.filename)
 if(!(Test-Path -LiteralPath $taskPath)){Invoke-WebRequest -Uri $taskItem.url -OutFile $taskPath -UseBasicParsing}
 if((Get-Item -LiteralPath $taskPath).Length -ne $taskItem.size){throw ('Dimensiune incorecta: '+$taskItem.id)}
 Write-Output ('Salvat '+$taskItem.id+' '+$taskItem.size+' octeti')
}
