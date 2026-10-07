$ErrorActionPreference = 'Stop'
$sourcesToFetch = @(
 @('wikdict-sqlite-2.html','https://download.wikdict.com/dictionaries/sqlite/2/'),
 @('wikdict-tei-recommended.html','https://download.wikdict.com/dictionaries/tei/recommended/'),
 @('indic-readme.txt','https://raw.githubusercontent.com/AI4Bharat/Indic-Glossaries/master/README.md'),
 @('kaikki-list.html','https://kaikki.org/dictionary/'),
 @('yaitron-readme.txt','https://raw.githubusercontent.com/veer66/Yaitron/master/README.md')
)
$kaikkiNames = @('English','German','French','Spanish','Romanian','Bengali','Urdu','Cantonese','Hausa','Marathi','Telugu','Wu','Tamil','Persian','Egyptian Arabic','Moroccan Arabic','Najdi Arabic','Vietnamese','Kannada','Gujarati','Amharic','Burmese','Central Atlas Tamazight','Tarifit','Tashelhit','Kabyle','Malayalam','Odia','Sudanese Arabic','Punjabi','Western Punjabi','Uzbek','Igbo','Yoruba','Thai','Nepali','Hokkien','Kazakh','Sinhalese','Khmer','Azerbaijani')
foreach ($kaikkiName in $kaikkiNames) { $sourcesToFetch += ,@(('kaikki-' + $kaikkiName.Replace(' ','_') + '.html'),('https://kaikki.org/dictionary/' + [uri]::EscapeDataString($kaikkiName) + '/index.html')) }
$wikiCodes = @('en','de','fr','es','ro','bn','ur','yue','ha','mr','te','wuu','ta','fa','arz','ary','vi','kn','gu','am','my','shi','kab','ml','or','pa','pnb','uz','ig','yo','th','ne','zh_min_nan','kk','si','km','az')
foreach ($wikiCode in $wikiCodes) { $sourcesToFetch += ,@(('wiki-' + $wikiCode + '.html'),('https://dumps.wikimedia.org/' + $wikiCode + 'wiktionary/latest/')) }
$archiveIds = @('dictionaryofhaus02robiuoft','vocabularyofyoru00crow','englishchinesevo00shan','vocabularyofshan00edkirich','cu31924026888481','judsonburmeseeng00judsrich')
foreach ($archiveId in $archiveIds) { $sourcesToFetch += ,@(('archive-' + $archiveId + '.json'),('https://archive.org/metadata/' + $archiveId)) }
$result = @()
foreach ($sourceToFetch in $sourcesToFetch) {
 try {
  Invoke-WebRequest -UseBasicParsing -Uri $sourceToFetch[1] -OutFile $sourceToFetch[0] -TimeoutSec 12
  $result += [pscustomobject]@{ file=$sourceToFetch[0]; url=$sourceToFetch[1]; status='OK' }
 } catch { $result += [pscustomobject]@{ file=$sourceToFetch[0]; url=$sourceToFetch[1]; status=$_.Exception.Message } }
}
$result | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath 'fetch-log.json' -Encoding UTF8
$result | Group-Object status | Select-Object Count,Name | Format-Table -AutoSize
