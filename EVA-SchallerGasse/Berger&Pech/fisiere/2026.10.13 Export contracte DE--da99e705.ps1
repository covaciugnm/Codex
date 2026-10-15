$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)'
$taskWord = $null
$taskOwned = $false
try {
    $taskWord = New-Object -ComObject Word.Application
    if ($taskWord.Documents.Count -ne 0) { throw 'Word instance has open documents; no documents modified.' }
    $taskOwned = $true
    $taskWord.Visible = $false
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskWord.Options.UpdateLinksAtOpen = $false
    $taskRecords = Get-Content -LiteralPath (Join-Path $taskRoot '00.Proiect\09. Vertraege\2026.10.13 Versiuni contracte numai germana.json') -Raw | ConvertFrom-Json
    foreach ($taskRecord in $taskRecords.documente) {
        $taskDocPath = [IO.Path]::GetFullPath((Join-Path $taskRoot $taskRecord.docx))
        $taskPdfPath = [IO.Path]::ChangeExtension($taskDocPath, '.pdf')
        if (-not $taskDocPath.StartsWith($taskRoot + '\') -or -not $taskPdfPath.StartsWith($taskRoot + '\')) { throw 'Export target outside authorized workspace' }
        if (Test-Path -LiteralPath $taskPdfPath) { throw 'PDF already exists; no overwrite performed' }
        $taskDoc = $null
        try {
            $taskDoc = $taskWord.Documents.Open($taskDocPath,$false,$true,$false)
            $taskDoc.Fields.Update() | Out-Null
            $taskDoc.Repaginate()
            $taskDoc.ExportAsFixedFormat($taskPdfPath,17)
            Write-Output "$($taskRecord.prestator): $($taskDoc.ComputeStatistics(2)) pages"
        } finally {
            if ($null -ne $taskDoc) { $taskDoc.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc) }
        }
    }
} finally {
    if ($taskOwned -and $null -ne $taskWord) { $taskWord.Quit(0) }
    if ($null -ne $taskWord) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) }
}

