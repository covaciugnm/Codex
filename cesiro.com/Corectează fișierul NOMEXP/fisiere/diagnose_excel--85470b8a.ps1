$ErrorActionPreference='Stop'
$xl=$null
$book=$null
try {
 $xl=New-Object -ComObject Excel.Application
 $xl.Visible=$false
 $xl.DisplayAlerts=$false
 $xl.AskToUpdateLinks=$false
 Write-Output "VERSION=$($xl.Version) READY=$($xl.Ready)"
 try {
  $book=$xl.Workbooks.Add()
  Write-Output "ADD_OK count=$($xl.Workbooks.Count)"
  $book.Close($false)
  $book=$null
 } catch {Write-Output "ADD_ERROR=$($_.Exception.Message)"}
 $f='C:\Users\User\.codex\tmp\nomexp_20261020\NOMEXP_SKU_5900_corectat.xlsx'
 Write-Output "EXISTS=$(Test-Path -LiteralPath $f) LENGTH=$((Get-Item -LiteralPath $f).Length)"
 try {
  $book=$xl.Workbooks.Open($f,0,$true,5,'','',$true,2,"`t",$false,$false,0,$false,$true,1)
  Write-Output "RECOVERY_OPEN_OK sheets=$($book.Worksheets.Count)"
  $book.SaveCopyAs('C:\Users\User\.codex\tmp\nomexp_20261020\recovery_diagnostic.xlsx')
  $book.Close($false)
  $book=$null
 } catch {Write-Output "RECOVERY_ERROR=$($_.Exception.Message) HRESULT=$($_.Exception.HResult)"}
} finally {
 if($null -ne $book){$book.Close($false)}
 if($null -ne $xl){$xl.Quit();[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)}
 [GC]::Collect()
 [GC]::WaitForPendingFinalizers()
}
