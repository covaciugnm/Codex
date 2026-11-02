$ErrorActionPreference='Stop'
$destinationFile='Z:\00.Roboti\cesiro.com\outputs\nomexp_5900_20261020\NOMEXP_SKU_5900_corectat.xlsx'
$file='C:\Users\User\.codex\tmp\nomexp_20261020\NOMEXP_SKU_5900_corectat.xlsx'
Copy-Item -LiteralPath $destinationFile -Destination $file -Force
$reportPath='Z:\00.Roboti\cesiro.com\work_nomexp\native_excel_checks.json'
$excel=$null
$book=$null
try {
    $excel=New-Object -ComObject Excel.Application
    $excel.Visible=$false
    $excel.DisplayAlerts=$false
    $excel.AskToUpdateLinks=$false
    $excel.AutomationSecurity=3
    $nativeNormalization=$false
    try {
        $book=$excel.Workbooks.Open($file,0,$false)
    } catch {
        # Excel rejects the exporter's multiargument formulas. Restore the exact
        # authored formulas through Excel before using its native serialization.
        $book=$excel.Workbooks.Open($file,0,$false,5,'','',$true,2,"`t",$false,$false,0,$false,$true,1)
    }
    $blocks=Get-Content -LiteralPath 'Z:\00.Roboti\cesiro.com\work_nomexp\formula_restore.json' -Raw -Encoding utf8 | ConvertFrom-Json
    foreach($block in $blocks){
        $matrix=New-Object 'object[,]' $block.formulas.Count,1
        for($i=0;$i -lt $block.formulas.Count;$i++){$matrix[$i,0]=[string]$block.formulas[$i][0]}
        $targetRange=$book.Worksheets.Item($block.sheet).Range($block.range)
        if($targetRange.NumberFormat -eq '@'){$targetRange.NumberFormat='General'}
        $targetRange.Formula=$matrix
    }
    $nativeFile='C:\Users\User\.codex\tmp\nomexp_20261020\NOMEXP_SKU_5900_native.xlsx'
    $book.SaveAs($nativeFile,51)
    $book.Close($false)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($book)
    $book=$null
    $file=$nativeFile
    $book=$excel.Workbooks.Open($file,0,$false)
    $nativeNormalization=$true
    $excel.CalculateFullRebuild()
    $sku=$book.Worksheets.Item('SKU_5900')
    $export=$book.Worksheets.Item('NOMEXP02_5900')
    $catalog=$book.Worksheets.Item('Cataloage')
    $audit=$book.Worksheets.Item('Corectii')
    $values=$sku.Range('A7:U372').Value2
    $codes=@()
    $badStatuses=@()
    $unknown=0
    for($r=1;$r -le 366;$r++){
        $codes += [string]$values[$r,1]
        if($values[$r,19] -ne 'Cod valid'){$badStatuses += $r+6}
        if($values[$r,6] -eq 'Descriere lipsă: 324L'){$unknown++}
    }
    $unique=($codes | Sort-Object -Unique).Count
    if($unique -ne 366 -or $badStatuses.Count -ne 0 -or $unknown -ne 14){throw "Validare nativă eșuată: unique=$unique bad=$($badStatuses.Count) unknown=$unknown"}
    $expectedControl=Get-Content -LiteralPath 'Z:\00.Roboti\cesiro.com\work_nomexp\audit_date\sku5900_expected_control.json' -Raw -Encoding utf8 | ConvertFrom-Json
    $codeDiff=@(Compare-Object -ReferenceObject $expectedControl.expected_sku_sorted -DifferenceObject ($codes | Sort-Object))
    if($codeDiff.Count -ne 0){throw "Codurile calculate nu corespund listei independente: $($codeDiff.Count) diferențe"}
    $exportCodes=$export.Range('A2:A367').Value2
    for($r=1;$r -le 366;$r++){
        if($codes[$r-1] -notmatch '^5900_\d{4}_\d{4}_[A-Z0-9]{4}$'){throw "SKU nevalid la rândul $($r+6): $($codes[$r-1])"}
        if($exportCodes[$r,1] -ne $codes[$r-1]){throw "Cod diferit în export la rândul $($r+1)"}
    }
    $sku.Range('L7').Value2=12.34
    $excel.CalculateFull()
    if([math]::Abs($export.Range('K2').Value2-12.34) -gt 0.000001){throw 'Prețul nu se propagă în export în Excel'}
    $sku.Range('L7').ClearContents() | Out-Null
    # A known zero is a populated input and must not be treated as missing.
    $sku.Range('L7').Value2=0
    $excel.CalculateFull()
    if($sku.Range('T7').Value2 -match 'Preț;'){throw 'Un preț explicit zero este tratat ca lipsă'}
    $sku.Range('L7').ClearContents() | Out-Null
    $catValues=$catalog.Range('G7:H49').Value2
    $unknownRow=0
    for($r=1;$r -le 43;$r++){if($catValues[$r,1] -eq '324L'){$unknownRow=$r+6}}
    $catalog.Range("H$unknownRow").Value2='Descriere test'
    $excel.CalculateFull()
    if($audit.Range('B13').Value2 -ne 0){throw 'Contorul descrierilor lipsă nu se actualizează'}
    $catalog.Range("H$unknownRow").Value2='De completat'
    $excel.CalculateFullRebuild()
    if($audit.Range('B13').Value2 -ne 14 -or $audit.Range('B14').Value2 -ne 366){throw 'Restaurare date după test eșuată'}
    $errorCells=@()
    foreach($sheet in $book.Worksheets) {
        try {
            $errors=$sheet.UsedRange.SpecialCells(-4123,16)
            if($null -ne $errors){$errorCells += "$($sheet.Name)!$($errors.Address())"}
        } catch {
            if($_.Exception.Message -notmatch 'No cells were found|Nu s-au găsit celule|Nicio celulă găsită|0x800A03EC') {throw}
        }
    }
    if($errorCells.Count -ne 0){throw "Erori formule Excel: $($errorCells -join ',')"}
    $sku.Activate()
    $excel.ActiveWindow.ScrollRow=1
    $excel.ActiveWindow.ScrollColumn=1
    $excel.ActiveWindow.Zoom=85
    $sku.Range('A1').Select() | Out-Null
    $book.CheckCompatibility=$false
    $book.Save()
    $result=[ordered]@{opened_in_excel=$true;native_serialization=$nativeNormalization;excel_version=$excel.Version;unique_sku=$unique;exact_expected_sku_match=$true;export_sku_match=$true;invalid_sku=$badStatuses.Count;missing_glaze_descriptions=$unknown;formula_errors=$errorCells;price_propagation=$true;zero_price_not_missing=$true;glaze_recalculation=$true;temporary_inputs_restored=$true;sheets=$book.Worksheets.Count;saved=$book.Saved}
    $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding utf8
    $result | ConvertTo-Json -Depth 5
    $book.Close($false)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($book)
    $book=$null
    Copy-Item -LiteralPath $file -Destination $destinationFile -Force
} finally {
    if($null -ne $book){$book.Close($false);[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($book)}
    if($null -ne $excel){$excel.Quit();[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
