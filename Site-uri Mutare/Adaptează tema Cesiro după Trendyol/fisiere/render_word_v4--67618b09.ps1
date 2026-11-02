$ErrorActionPreference = 'Stop'
$cesiroOut = 'Z:\00.Roboti\MutareSite\output\cesiro-proiect'
$cesiroQa = Join-Path $cesiroOut 'qa-v4'
New-Item -ItemType Directory -Path $cesiroQa -Force | Out-Null
$cesiroWord = New-Object -ComObject Word.Application
$cesiroWord.Visible = $false
$cesiroWord.DisplayAlerts = 0
try {
    foreach ($cesiroName in @('Proiect_CESIRO_Design_React_Python_V4','Matrice_Raspuns_Audituri_CESIRO_V4')) {
        $cesiroDocument = $cesiroWord.Documents.Open((Join-Path $cesiroOut ($cesiroName + '.docx')), $false, $true)
        try {
            $cesiroDocument.Repaginate()
            $cesiroDocument.ExportAsFixedFormat((Join-Path $cesiroQa ($cesiroName + '.pdf')), 17)
            Write-Output ($cesiroName + ': ' + $cesiroDocument.ComputeStatistics(2) + ' pagini')
        } finally { $cesiroDocument.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($cesiroDocument) }
    }
} finally { $cesiroWord.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($cesiroWord) }
