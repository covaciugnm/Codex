$ErrorActionPreference='Stop'
$taskDir=Split-Path -Parent $MyInvocation.MyCommand.Path
$jobs=Get-Content -LiteralPath "$taskDir\jobs.json" -Raw | ConvertFrom-Json
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
$word.AutomationSecurity=3
$results=@()
$stage=Join-Path $taskDir 'word_stage'
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$idx=0
try {
 foreach($j in $jobs){
  $idx++
  if((Test-Path -LiteralPath $j.pdf) -and (Get-Item -LiteralPath $j.pdf).LastWriteTimeUtc -ge (Get-Item -LiteralPath $j.docx).LastWriteTimeUtc){
   $results += [PSCustomObject]@{docx=$j.docx;pdf=$j.pdf;result='OK';reused=$true}
   continue
  }
  $pdfDir=Split-Path -Parent $j.pdf
  New-Item -ItemType Directory -Force -Path $pdfDir | Out-Null
  try {
   $localDoc=Join-Path $stage ("doc_"+$idx+'.docx')
   $localPdf=Join-Path $stage ("doc_"+$idx+'.pdf')
   Copy-Item -LiteralPath $j.docx -Destination $localDoc -Force
   $doc=$word.Documents.Open($localDoc,$false,$false)
   if($null -eq $doc){throw 'Word did not open the staged document'}
   $doc.Fields.Update() | Out-Null
   $doc.Repaginate()
   $pages=$doc.ComputeStatistics(2)
   $doc.Save()
   $doc.ExportAsFixedFormat($localPdf,17)
   $doc.Close(0)
   Copy-Item -LiteralPath $localDoc -Destination $j.docx -Force
   Copy-Item -LiteralPath $localPdf -Destination $j.pdf -Force
   $results += [PSCustomObject]@{docx=$j.docx;pdf=$j.pdf;pages=$pages;result='OK'}
   Write-Output ([System.IO.Path]::GetFileName($j.docx)+' '+$pages+'p')
  } catch {
   $results += [PSCustomObject]@{docx=$j.docx;pdf=$j.pdf;result=$_.Exception.Message}
  }
 }
} finally {
 $word.Quit()
 $results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$taskDir\conversion.json" -Encoding utf8
}
