$xl=$null
$book=$null
try {
 $xl=New-Object -ComObject Excel.Application
 $xl.Visible=$false
 $xl.DisplayAlerts=$false
 $book=$xl.Workbooks.Add()
 Write-Output "LIST_SEPARATOR=$($xl.International(5))"
 try {
   $book.Worksheets.Item(1).Range('A1').Formula='=IF(1=1,2,3)'
   Write-Output "COMMA_FORMULA_OK=$($book.Worksheets.Item(1).Range('A1').Value2)"
 } catch {Write-Output "COMMA_ERROR=$($_.Exception.Message)"}
 try {
   $book.Worksheets.Item(1).Range('A2').Formula='=IF(1=1;2;3)'
   Write-Output "SEMICOLON_FORMULA_OK=$($book.Worksheets.Item(1).Range('A2').Value2)"
 } catch {Write-Output "SEMICOLON_ERROR=$($_.Exception.Message)"}
 $book.SaveAs('C:\Users\User\.codex\tmp\nomexp_20261020\formula_diagnostic.xlsx',51)
} finally {
 if($null -ne $book){$book.Close($false)}
 if($null -ne $xl){$xl.Quit();[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)}
}
