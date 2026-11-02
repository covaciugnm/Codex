$ErrorActionPreference='Stop'
$root=(Get-Item '.\iFLYTEK_XF-AIGlasses-01_Documentatie').FullName
$dest=Join-Path $root 'Software/Biblioteca_Glasses'
$rows=@(Get-Content (Join-Path $dest 'manifest.json') -Raw | ConvertFrom-Json)
foreach($name in @('manifest-aplicatii.json','manifest-extra.json')) {if(Test-Path (Join-Path $dest $name)){$rows+=@(Get-Content (Join-Path $dest $name) -Raw | ConvertFrom-Json)}}
function Enc($s){[Net.WebUtility]::HtmlEncode([string]$s)}
$reading=Join-Path $dest 'Lectura';New-Item -ItemType Directory -Force $reading | Out-Null
$urlMap=@{};foreach($r in $rows){if($r.status -eq 'descarcat' -and $r.category -eq 'Documentatie'){$urlMap[$r.url]='../Lectura/'+[IO.Path]::GetFileName($r.file)}}
foreach($r in $rows | Where-Object {$_.category -eq 'Documentatie' -and $_.status -eq 'descarcat'}){
 $html=[IO.File]::ReadAllText((Join-Path $dest $r.file))
 $main=[regex]::Match($html,'(?is)<main\b[^>]*>(.*?)</main>');if($main.Success){$html=$main.Groups[1].Value}else{$body=[regex]::Match($html,'(?is)<body\b[^>]*>(.*?)</body>');if($body.Success){$html=$body.Groups[1].Value}}
 $html=[regex]::Replace($html,'(?is)<(script|style|svg|iframe|noscript)\b[^>]*>.*?</\1>','')
 $html=[regex]::Replace($html,'(?is)<(?:link|meta|img|input)\b[^>]*>','')
 $html=[regex]::Replace($html,'(?is)\s(?:style|class|on\w+)\s*=\s*(?:"[^"]*"|''[^'']*'')','')
 $origin=[uri]$r.url
 $html=[regex]::Replace($html,'href="([^"]*)"',{param($m) try{$u=[uri]::new($origin,[Net.WebUtility]::HtmlDecode($m.Groups[1].Value)).AbsoluteUri;if($urlMap.ContainsKey($u)){$u=$urlMap[$u]};'href="'+(Enc $u)+'"'}catch{''}})
 $title=Enc $r.title
 $page='<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+ $title +'</title><style>body{font:17px/1.65 system-ui;max-width:1000px;margin:30px auto;padding:0 20px;color:#193342}pre{overflow:auto;background:#f0f4f6;padding:16px}table{border-collapse:collapse}td,th{border:1px solid #ccd;padding:8px}a{color:#075ca6}</style><p><a href="../INDEX.html">← Biblioteca</a> · <a href="'+(Enc $r.url)+'">Sursa online</a> · <a href="../'+$r.file+'">HTML original</a></p><h1>'+$title+'</h1><p>Copie de lectură, 30.10.2026. Scripturile și elementele interactive sunt eliminate. Legăturile fără copie locală necesită internet. Conținutul rămâne în limba originală.</p><hr>'+$html+'</html>'
 [IO.File]::WriteAllText((Join-Path $reading ([IO.Path]::GetFileName($r.file))),$page)
}
$good=@($rows | Where-Object status -eq 'descarcat');$gb=[math]::Round(($good | Measure-Object bytes -Sum).Sum/1GB,2)
$out=[Text.StringBuilder]::new()
[void]$out.Append('<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>iFLYTEK — aplicații, documentații și Bluetooth</title><style>body{font:16px/1.6 system-ui;background:#f3f6f8;color:#173745;max-width:1250px;margin:30px auto;padding:0 20px}h1{font-size:32px}h2{margin-top:36px}a{color:#075da8}section,.intro{background:white;padding:22px;border-radius:12px;margin:18px 0}.scroll{overflow:auto}table{border-collapse:collapse;width:100%}th,td{padding:12px;border-bottom:1px solid #d8e2e8;text-align:left;vertical-align:top}th{background:#e9f1f6}small{display:block;color:#526876}input{font:inherit;padding:12px;width:min(90%,600px)}.ok{color:#17683b}.missing{color:#9b4816}code{overflow-wrap:anywhere}nav a{margin-right:18px}</style></head><body><nav><a href="../../INDEX.html">Arhiva principală</a><a href="../INDEX.html">128 arhive SDK existente</a><a href="manifest-complet.json">Inventar și SHA-256</a></nav><p id="sdk-experimental"><a href="../SDK_Experimental/INDEX.html"><strong>SDK experimental extras din APK — JAR, surse, protocol și teste</strong></a></p><h1>iFLYTEK — aplicații și documentații</h1><div class="intro"><p>Biblioteca cercetării pentru ochelari, AINOTE și Loomy. Actualizată la 30 octombrie 2026.</p><p><strong>'+ $good.Count +' fișiere arhivate · '+$gb+' GiB</strong>. Descărcările sunt originale și nu au fost instalate. Arhivele de cod includ documentația din depozite; dependențele externe nu sunt incluse automat.</p><p>Componenta <code>com.iflytek.easytrans.headset.bluetooth</code> a fost identificată în APK-ul oficial. Un SDK separat pentru dezvoltatori nu a fost găsit. Compatibilitatea proiectelor altor producători cu XF-AIGlasses-01 nu este confirmată.</p><label>Caută în bibliotecă <input id="filter" type="search" placeholder="Android, Bluetooth, AINOTE, Loomy…"></label></div>')
foreach($cat in @('Aplicatii','Documentatie','Cod_sursa','Cercetare')){
 [void]$out.Append('<section><h2>'+(Enc $cat.Replace('_',' '))+'</h2><div class="scroll"><table><thead><tr><th>Resursă</th><th>Fișiere locale</th><th>Proveniență și compatibilitate</th></tr></thead><tbody>')
 foreach($r in $rows | Where-Object category -eq $cat | Sort-Object title){
 $local='<span class="missing">'+(Enc $r.status)+'</span>'
 if($r.status -eq 'descarcat'){$local='<a class="ok" href="'+(Enc $r.file)+'">Deschide / descarcă</a><small>'+[math]::Round($r.bytes/1MB,2)+' MiB</small>';if($cat -eq 'Documentatie'){$local='<a href="Lectura/'+[IO.Path]::GetFileName($r.file)+'">Citește local</a><br>'+$local}}
 if($r.error){$local+='<small>'+(Enc $r.error)+'</small>'}
 $src=Enc $r.scope;if($r.url){$src+='<br><a href="'+(Enc $r.url)+'">Sursa online</a>'}
 [void]$out.Append('<tr data-resource><td><strong>'+(Enc $r.title)+'</strong></td><td>'+$local+'</td><td>'+$src+'</td></tr>')
 }
 [void]$out.Append('</tbody></table></div></section>')
}
[void]$out.Append('<p>Acoperire: materialele identificate în cercetare și disponibile public. Fișierele restricționate la cont, SDK-urile private și aplicațiile disponibile exclusiv în magazine nu sunt prezentate ca descărcate. Unele pagini dinamice necesită site-ul online.</p><script>document.getElementById("filter").addEventListener("input",e=>{const q=e.target.value.toLocaleLowerCase();document.querySelectorAll("[data-resource]").forEach(r=>r.hidden=!r.textContent.toLocaleLowerCase().includes(q));});</script></body></html>')
[IO.File]::WriteAllText((Join-Path $dest 'INDEX.html'),$out.ToString())
$rows | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $dest 'manifest-complet.json') -Encoding utf8
foreach($entry in @(@('INDEX.html','Software/Biblioteca_Glasses/INDEX.html'),@('Software/INDEX.html','Biblioteca_Glasses/INDEX.html'),@('Software/APLICATII_ECHIPAMENTE.html','Biblioteca_Glasses/INDEX.html'))){
 $p=Join-Path $root $entry[0];$s=[IO.File]::ReadAllText($p);$banner='<p id="biblioteca-glasses" style="padding:18px;background:#e7f4ec;border:1px solid #8bbda0"><a href="'+$entry[1]+'"><strong>Aplicații și documentații — iFLYTEK Glasses, Bluetooth, AINOTE și Loomy</strong></a></p>'
 if($s -match 'id="biblioteca-glasses"'){$s=[regex]::Replace($s,'(?s)<p id="biblioteca-glasses".*?</p>',$banner)}elseif($s -match '(?i)<body[^>]*>'){$s=[regex]::Replace($s,'(?i)(<body[^>]*>)',('$1'+$banner))}else{$s=$s.Replace('<h1>',$banner+'<h1>')}
 [IO.File]::WriteAllText($p,$s)
}
$fail=@();foreach($r in $good){if(!(Test-Path -LiteralPath (Join-Path $dest $r.file))){$fail+=$r.file}}
$check=[ordered]@{date='2026-10-30';downloaded=$good.Count;GiB=$gb;missingFiles=$fail;notDownloaded=@($rows | Where-Object status -ne 'descarcat' | Select-Object title,status,error)}
$check | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $dest 'validare.json') -Encoding utf8
$check | ConvertTo-Json -Depth 5
