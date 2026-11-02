param([string[]]$Providers = @('BERGER','PECH'))
$ErrorActionPreference = 'Stop'
$taskDirectory = $PSScriptRoot
$taskWord = $null
$taskOwned = $false
try {
    $taskWord = New-Object -ComObject Word.Application
    if ($taskWord.Documents.Count -ne 0) { throw 'Word instance already has open documents; export stopped without modifying them.' }
    $taskOwned = $true
    $taskWord.Visible = $false
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskWord.Options.UpdateLinksAtOpen = $false
    foreach ($taskProvider in $Providers) {
        $taskDocPath = [IO.Path]::GetFullPath((Join-Path $taskDirectory "2026.10.12 Propunere contract $taskProvider.docx"))
        $taskPdfPath = [IO.Path]::GetFullPath((Join-Path $taskDirectory "2026.10.12 Propunere contract $taskProvider.pdf"))
        if (-not $taskDocPath.StartsWith($taskDirectory + '\') -or -not $taskPdfPath.StartsWith($taskDirectory + '\')) {throw 'Export target outside contract workspace'}
        $taskDoc = $null
        try {
            $taskDoc = $taskWord.Documents.Open($taskDocPath,$false,$true,$false)
            $taskDoc.Fields.Update() | Out-Null
            $taskDoc.Repaginate()
            $taskDoc.ExportAsFixedFormat($taskPdfPath,17)
            Write-Output "$taskProvider PDF: $($taskDoc.ComputeStatistics(2)) pages"
        } finally {
            if ($null -ne $taskDoc) { $taskDoc.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc) }
        }
    }
} finally {
    if ($taskOwned -and $null -ne $taskWord) { $taskWord.Quit(0) }
    if ($null -ne $taskWord) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) }
}
