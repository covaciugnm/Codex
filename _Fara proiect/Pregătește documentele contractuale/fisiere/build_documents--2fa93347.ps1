$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$outDir='C:\Users\User\Documents\Codex\2026-09-07\pr\outputs'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$serials=@('194430100193975A00','1944301031DF985A00','194430107134995A00','19443010910C985A00','19443010414B995A00','19443010E1E1975A00')
function Esc([string]$s){[System.Security.SecurityElement]::Escape($s)}
function Para([string]$s,[bool]$bold=$false){$r='';if($bold){$r='<w:rPr><w:b/></w:rPr>'};'<w:p><w:r>'+$r+'<w:t xml:space="preserve">'+(Esc $s)+'</w:t></w:r></w:p>'}
function Table($rows){$s='<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>';foreach($row in $rows){$s+='<w:tr>';foreach($cell in $row){$s+='<w:tc><w:tcPr><w:tcW w:w="2400" w:type="dxa"/></w:tcPr>'+(Para $cell)+'</w:tc>'};$s+='</w:tr>'};$s+'</w:tbl>'}
function SaveDoc($name,$body){
 $path=Join-Path $outDir $name
 $fs=[System.IO.File]::Open($path,[System.IO.FileMode]::Create)
 $zip=[System.IO.Compression.ZipArchive]::new($fs,[System.IO.Compression.ZipArchiveMode]::Create)
 $entries=@{
 '[Content_Types].xml'='<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>';
 '_rels/.rels'='<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>';
 'word/document.xml'='<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+$body+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000"/></w:sectPr></w:body></w:document>'
 }
 foreach($key in $entries.Keys){$entry=$zip.CreateEntry($key);$writer=[System.IO.StreamWriter]::new($entry.Open(),[System.Text.UTF8Encoding]::new($false));$writer.Write($entries[$key]);$writer.Dispose()};$zip.Dispose();$fs.Dispose()
}
$notice='PROIECT – DE COMPLETAT ȘI VALIDAT. Contractul nu a putut fi consultat. Nu confirmă emiterea facturii, livrarea, testarea sau recepția.'
$parties='Furnizor: [denumire, CUI, nr. registrul comerțului, sediu, IBAN, bancă]. Beneficiar: [denumire, CUI, nr. registrul comerțului, sediu].'
$ref='Contract: [număr și dată de verificat în PDF; numele fișierului indică nr. 9]. Anexe/acte adiționale: [de completat].'
$product='Cameră Luxonis OAK-D-PRO-AF; SKU A00546; lot 2604TA; cantitate identificată în fotografii: 6 bucăți.'
function Base($title){(Para $title $true)+(Para $notice)+(Para 'Nr. [___] / Data [___]')+(Para $parties)+(Para $ref)}
$rows=@();$rows+=,@('Nr.','Model / SKU','Serie (SN)','Fotografie')
for($i=0;$i -lt 6;$i++){$photo=if($i -eq 5){'12.52.17.jpeg'}else{'12.52.17 '+($i+1)+'.jpeg'};$rows+=,@(($i+1).ToString(),'OAK-D-PRO-AF / A00546',$serials[$i],$photo)}
$annex=(Para 'ANEXĂ – IDENTIFICAREA CELOR 6 CAMERE' $true)+(Para 'Transcriere din fotografiile furnizate. Seriile de pe ambalaje se confruntă cu echipamentele la predare.')+(Para $product)+(Table $rows)+(Para 'Fișierele foto au prefixul „WhatsApp Image 2026-09-07 at ”. Codul comun 0096718607556 nu reprezintă seria individuală SN.')+(Para 'Anexă la factura [___], avizul [___], certificatele [___] și procesul-verbal [___].')
SaveDoc '06_Anexa_serii_camere.docx' $annex
$b=Base 'FACTURĂ – MACHETĂ PENTRU EMITERE'
$b+=(Para 'Serie/număr fiscal: [___]. Data emiterii: [___]. Data livrării: [___]. Monedă: [___]. Scadență: [conform contractului].')
$r=@();$r+=,@('Denumire','UM','Cant.','Preț fără TVA','Valoare fără TVA','TVA');$r+=,@('Luxonis OAK-D-PRO-AF, SKU A00546; serii în anexa 06','buc.','6','[___]','[___]','[cotă / sumă]');$r+=,@('[Alte bunuri conform contractului – de identificat]','[___]','[___]','[___]','[___]','[___]');$r+=,@('[Servicii contractate – de identificat]','[___]','[___]','[___]','[___]','[___]')
$b+=Table $r
$b+=(Para 'Total fără TVA: [___]. TVA: [___]. Total cu TVA: [___]. Avansuri de regularizat, facturi de referință și sold: [___].')+(Para 'Denumirile, defalcarea prețurilor și regimul TVA se completează după contract și datele fiscale. Dacă prețul este pentru un sistem/set, liniile se adaptează; nu se inventează prețuri separate.')
SaveDoc '01_Factura_macheta.docx' $b
$b=Base 'CERTIFICAT DE CONFORMITATE AL FURNIZORULUI – PROIECT'
$b+=(Para $product)+(Para 'Identificare individuală: anexa 06. Alte produse acoperite: [denumire, model, cantitate, serie/lot – după contract].')+(Para 'Documente suport: [declarația de conformitate a producătorului: emitent, număr, dată, modele acoperite]; [fișe tehnice]; [alte documente relevante].')+(Para 'Cerințe contractuale verificate: [anexă/articol și caracteristici]. Rezultatul verificării și eventualele abateri: [___].')+(Para 'Text de validat de emitent: Furnizorul confirmă conformitatea produselor identificate mai sus cu cerințele contractuale enumerate și documentele suport anexate, în limitele verificărilor consemnate.')+(Para 'Documentul furnizorului nu înlocuiește declarația UE de conformitate a producătorului. Nu se completează standarde sau declarații de conformitate fără documentele aferente.')+(Para 'Responsabil autorizat: [nume, funcție]. Data și semnătura: [___].')
SaveDoc '02_Certificat_conformitate_proiect.docx' $b
$b=Base 'CERTIFICAT DE CALITATE – PROIECT'
$b+=(Para $product)+(Para 'Serii: anexa 06. Alte bunuri: [lista de completat după contract].')+(Para 'Documente de calitate ale producătorului/furnizorului de origine: [___]. Raport de verificare: [nr./dată/responsabil].')
$r=@();$r+=,@('Verificare propusă','Rezultat / dovadă');foreach($x in @('Identificare model, SN și lot','Stare fizică și integritate','Completitudinea accesoriilor contractate','Pornire, conectare și funcționare','Alte probe prevăzute în contract')){$r+=,@($x,'[de efectuat / completat]')};$b+=Table $r
$b+=(Para 'Concluzie privind calitatea: [se completează exclusiv pe baza verificărilor]. Neconformități și măsuri: [___].')+(Para 'Garanție: [durată, moment de început, condiții și contact service conform contractului]. Certificat de garanție separat: [dacă este prevăzut].')+(Para 'Responsabil verificare: [nume, funcție, semnătură]. Emitent: [nume, funcție, semnătură].')
SaveDoc '03_Certificat_calitate_proiect.docx' $b
$b=Base 'AVIZ DE ÎNSOȚIRE A MĂRFII / EXPEDIȚIE – PROIECT'
$b+=(Para 'Loc încărcare: [___]. Destinație exactă: [___]. Data/ora expedierii: [___]. Motivul expedierii: [___]. Factură asociată, dacă există: [___].')
$r=@();$r+=,@('Bun','UM','Cantitate expediată','Observații');$r+=,@('Luxonis OAK-D-PRO-AF, SKU A00546','buc.','[6 – de confirmat la expediere]','Serii: anexa 06');$r+=,@('[Alte bunuri/accesorii din contract]','[___]','[___]','[model/serie/lot]');$b+=Table $r
$b+=(Para 'Număr colete / ambalare: [___]. Transportator/delegat: [___]. Mijloc de transport / număr auto sau AWB: [___].')+(Para 'Documente însoțitoare: [factură, certificate, declarații producător, manuale, garanție și alte documente contractuale].')+(Para 'Predat de: [nume, semnătură]. Transport preluat de: [___]. Primit de: [nume, funcție, data/ora, semnătură]. Diferențe constatate: [___].')
SaveDoc '04_Aviz_expeditie_proiect.docx' $b
$b=Base 'PROCES-VERBAL DE RECEPȚIE – PROIECT'
$b+=(Para 'Locul și data recepției: [___]. Reprezentant furnizor: [___]. Reprezentant/comisie beneficiar: [nume, funcții].')+(Para 'Documente de referință: contract și anexe [___]; aviz [___]; factură [___]; documente tehnice și certificate [___].')
$r=@();$r+=,@('Poziție','Cant. contractuală','Cant. primită','Rezultat');$r+=,@('6 camere identificate în anexa 06','[de verificat]','[___]','[___]');$r+=,@('[Alte bunuri și accesorii contractate]','[___]','[___]','[___]');$r+=,@('[Instalare/configurare/instruire, dacă sunt contractate]','[___]','[executat: ___]','[___]');$b+=Table $r
$b+=(Para 'Verificări cantitative, vizuale, documentare și probe funcționale efectuate: [metodă, dată, rezultate, raport anexat].')+(Para 'Documente efectiv predate: [listă cu numere/date]. Bunuri sau documente lipsă: [___]. Neconformități / rezerve: [___]. Termene de remediere și responsabili: [___].')+(Para 'Decizia comisiei: [admisă / admisă cu rezerve / amânată / respinsă – se selectează după verificări]. Îndeplinirea integrală a obligațiilor contractuale: [se stabilește după verificarea tuturor pozițiilor și serviciilor].')+(Para 'Începutul și durata garanției: [conform clauzei contractuale]. Anexe: inventar SN, rapoarte de probe, documente predate [___].')+(Para 'Furnizor: [nume, funcție, semnătură]. Beneficiar/comisie: [nume, funcții, semnături].')
SaveDoc '05_Proces_verbal_receptie_proiect.docx' $b
$check=@'
# Informații necesare pentru finalizarea dosarului

Stadiu: cinci machete Word și o anexă cu șase serii sunt pregătite. Nu sunt documente emise sau semnate. PDF-ul contractului nu a fost disponibil: unitatea Z: lipsește în mediul sesiunii. Lista completă a obligațiilor contractuale rămâne de stabilit.

1. **Contractul integral, anexele tehnice/financiare și eventualele acte adiționale** – încărcate direct în conversație. Din acestea se vor prelua părțile, lista bunurilor, prețurile, serviciile, documentele obligatorii, garanția, termenele și condițiile recepției. Nu este necesară retranscrierea datelor deja existente în contract.
2. **Livrarea efectivă:** ce se predă acum și ce s-a predat anterior; alte echipamente, accesorii, cabluri, alimentatoare sau servicii numai dacă sunt contractate; cantități, modele și serii pentru fiecare. Fotografii de etichete nu confirmă singure predarea sau funcționarea.
3. **Facturare:** seria și numărul, data emiterii/livrării, moneda, statutul TVA și cota/regimul aplicabil, eventuale avansuri/facturi anterioare și regularizări. Confirmarea datelor fiscale și bancare dacă s-au schimbat față de contract.
4. **Expediere:** adresa exactă, data/ora, persoana care predă și cea care primește, transportator/delegat, auto sau AWB, număr colete; seria/numărul avizului.
5. **Recepție:** data și locul, persoanele/comisia și funcțiile, verificările și probele efectuate, rezultatele, lipsurile sau rezervele, stadiul instalării/configurării/instruirii dacă sunt contractate; numărul procesului-verbal.
6. **Conformitate și calitate:** declarația de conformitate a producătorului pentru modelul exact, fișele tehnice, certificatele/documentele de calitate disponibile, raportul real de verificare/testare; emitentul și semnatarul autorizat, numerele și datele certificatelor. Nu sunt deduse standarde tehnice din siglele de pe ambalaj.
7. **Garanție și documentație:** documentele de garanție, contactul service, manualele și orice alte documente cerute prin contract. Durata și începutul garanției se preiau din contract.

## Date deja preluate din fotografii

Producător/marcă: Luxonis. Model etichetă: OAK-D-PRO-AF. SKU: A00546. Batch ID: 2604TA. Șase serii distincte:

| Fotografie | SN |
|---|---|
| 12.52.17 1.jpeg | 194430100193975A00 |
| 12.52.17 2.jpeg | 1944301031DF985A00 |
| 12.52.17 3.jpeg | 194430107134995A00 |
| 12.52.17 4.jpeg | 19443010910C985A00 |
| 12.52.17 5.jpeg | 19443010414B995A00 |
| 12.52.17.jpeg | 19443010E1E1975A00 |

Seriile sunt transcrise de pe ambalajele fotografiate și trebuie confruntate cu dispozitivele. Codul comun 0096718607556 nu este SN individual.
'@
[System.IO.File]::WriteAllText((Join-Path $outDir '00_Informatii_necesare.md'),$check,[System.Text.UTF8Encoding]::new($false))
$zipPath=Join-Path $outDir 'Dosar_livrare_camere_PROIECT.zip'
$fs=[System.IO.File]::Open($zipPath,[System.IO.FileMode]::Create);$zip=[System.IO.Compression.ZipArchive]::new($fs,[System.IO.Compression.ZipArchiveMode]::Create)
Get-ChildItem -LiteralPath $outDir -File | Where-Object {$_.Extension -in '.docx','.md'} | ForEach-Object {[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$_.FullName,$_.Name) | Out-Null}
$zip.Dispose();$fs.Dispose()
Get-ChildItem -LiteralPath $outDir -File | Select-Object Name,Length
