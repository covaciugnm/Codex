$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$root=Split-Path $PSScriptRoot -Parent
$software=Split-Path $root -Parent
$dest=Join-Path $root 'documentatie/arhive-sdk'
New-Item -ItemType Directory -Force $dest | Out-Null
$records=[System.Collections.Generic.List[object]]::new()
$archives=Get-ChildItem -LiteralPath $software -Filter '*.zip' -Recurse | Where-Object { $_.FullName -notlike "$root*" -and $_.FullName -notlike "$(Join-Path $software 'SDK_Experimental')*" }
$counter=0
foreach($archive in $archives){
  $zip=[IO.Compression.ZipFile]::OpenRead($archive.FullName)
  try {
    foreach($entry in $zip.Entries){
      if(!$entry.Name -or $entry.FullName -notmatch '(?i)(\.(md|markdown|rst|txt|html?|pdf|docx?)$|(^|/)(README|LICENSE|NOTICE|CHANGELOG)$)'){continue}
      $counter++
      $ext=[IO.Path]::GetExtension($entry.Name).ToLowerInvariant()
      $binary=$ext -in @('.pdf','.doc','.docx')
      $file=('{0:D6}' -f $counter)+$(if($binary){$ext}else{'.txt'})
      $status='extracted-text'
      if($entry.Length -gt 20971520){$status='indexed-only-over-20MiB';$file=$null}
      else {
        $stream=$entry.Open()
        try {
          if($binary){$output=[IO.File]::Create((Join-Path $dest $file));try{$stream.CopyTo($output)}finally{$output.Dispose()};$status='extracted-binary-not-text-read'}
          else {$reader=[IO.StreamReader]::new($stream);try{$body=$reader.ReadToEnd()}finally{$reader.Dispose()};if($ext -in @('.html','.htm')){$body=[regex]::Replace($body,'(?is)<(script|style)\b[^>]*>.*?</\1>',' ');$body=[Net.WebUtility]::HtmlDecode([regex]::Replace($body,'<[^>]+>',' '))};[IO.File]::WriteAllText((Join-Path $dest $file),$body,[Text.UTF8Encoding]::new($false))}
        } finally {$stream.Dispose()}
      }
      $records.Add([pscustomobject]@{archive=[IO.Path]::GetRelativePath($software,$archive.FullName);entry=$entry.FullName;bytes=$entry.Length;file=$file;status=$status})
    }
  } finally {$zip.Dispose()}
}
$records | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $dest 'index.json') -Encoding utf8
[pscustomobject]@{archives=$archives.Count;documents=$records.Count;textExtracted=@($records|Where-Object status -eq 'extracted-text').Count;binaryExtracted=@($records|Where-Object status -eq 'extracted-binary-not-text-read').Count;oversize=@($records|Where-Object status -eq 'indexed-only-over-20MiB').Count} | ConvertTo-Json | Tee-Object -FilePath (Join-Path $dest 'summary.json')
