$source=Get-Content -LiteralPath 'C:\Users\User\Documents\Codex\2026-09-07\pr\work\build_documents.ps1' -Raw -Encoding UTF8
& ([scriptblock]::Create($source.Substring(0,$source.IndexOf('$notice='))))
# Import the reusable functions into this script scope.
. ([scriptblock]::Create($source.Substring(0,$source.IndexOf('$notice='))))
$notice='PROIECT PENTRU COMPLETARE ȘI SEMNARE – datele efective de livrare, testare și recepție se completează pe baza operațiunilor realizate.'
$parties='Furnizor: INDUNOVA ROBOTICS S.R.L.; CUI 52786670; J2025082650004; sat Botești, oraș Zlatna, nr. 37, jud. Alba; administrator Pușcău Bogdan-Sebastian. IBAN / bancă: [___]. Beneficiar: INDUSTRY DEVELOPMENT PRINTER S.R.L.; CUI RO50436813; J2024016413007; mun. Călărași, str. Constantin Dobrogeanu Gherea nr. 39, jud. Călărași; administrator Cercel Paraschiva.'
$ref='Contract de furnizare nr. 9/29.07.2026. Proiect cod 334979: „Sistem integrat bazat pe inteligență artificială (AI) pentru monitorizarea în timp real a defectelor în procesul de imprimare 3D”. Contract de finanțare nr. 390064/16.09.2025.'
function Base($title){(Para $title $true)+(Para $notice)+(Para 'Nr. [___] / Data [___]')+(Para $parties)+(Para $ref)}
$items=@(
 @('Sistem video de securitate: 8 camere video, DVR/NVR, HDD și accesorii','sistem','1','[mărci, modele, SN și inventar componente]'),
 @('Camere industriale Machine-Vision – Luxonis OAK-D-PRO-AF, SKU A00546','buc.','6','Lot 2604TA; SN în anexa 06; corespondență cu oferta de verificat'),
 @('Suporturi pentru camere industriale','buc.','6','[producător/model]'),
 @('Cabluri de comunicație și alimentare','buc.','6','[tip, lungime, conectori]'),
 @('Sisteme de iluminare industrială','buc.','6','[producător/model/SN sau lot]'),
 @('Controler de iluminare cu sursă de alimentare','buc.','6','[producător/model/SN sau lot; sursă inclusă]'),
 @('Interfețe hardware USB 3.0 sau echivalent','buc.','6','[producător/model/SN sau lot]'),
 @('Toate accesoriile necesare funcționării complete a sistemului','[UM]','[inventar]','[listă, cantități și legătura cu echipamentele]')
)
function Inventory { $r=@();$r+=,@('Bun conform art. 5 alin. (2)','UM / cant. contract','Identificare / cant. efectivă');foreach($x in $items){$r+=,@($x[0],($x[1]+' / '+$x[2]),($x[3]+'; predat: [___]'))};Table $r }
$warranty='Garanție: minimum 24 de luni de la semnarea procesului-verbal de recepție finală fără obiecțiuni, sau durata mai mare prevăzută în oferta tehnică (art. 20). Durata exactă: [de verificat în ofertă]; data de început: [___].'
$sign='Furnizor: Pușcău Bogdan-Sebastian, administrator / împuternicit [___]; semnătură [___]. Beneficiar: Cercel Paraschiva, administrator / reprezentanți desemnați [___]; semnături [___].'
$b=Base 'FACTURĂ – MACHETĂ PENTRU EMITERE'
$b+=(Para 'Serie / număr: [___]. Data emiterii: [___]. Moneda: RON. IBAN furnizor / bancă: [___]. Cod TVA furnizor / regim aplicabil: [de confirmat].')
$r=@();$r+=,@('Denumire','UM / cant.','Preț unitar fără TVA','Valoare fără TVA');foreach($x in $items){$r+=,@($x[0],($x[1]+' / '+$x[2]),'[conform ofertei]','[conform ofertei]')};$b+=Table $r
$b+=(Para 'Total contractual pentru întregul obiect: 57.851,24 lei fără TVA (art. 6). Totalul liniilor facturate trebuie reconciliat cu oferta financiară. Accesoriile se evidențiază în poziția contractuală corespunzătoare, fără dublarea valorii.')+(Para 'TVA: [cotă aplicabilă / sumă]. Total cu TVA: [___]. Facturi anterioare / eventuale sume deja facturate sau încasate: [___].')+(Para 'Transportul, manipularea, instalarea, configurarea, testarea, punerea în funcțiune și instruirea de bază sunt incluse în preț (art. 7); nu se adaugă costuri suplimentare.')+(Para 'Conform art. 8 alin. (2), factura se emite după livrare, instalare, configurare, testare și punere în funcțiune, confirmate prin proces-verbal semnat de ambele părți. PV nr. [___] / [___]. Plata integrală prin virament bancar la data semnării PV, conform art. 8 alin. (3). Scadența calendaristică: [___].')+(Para 'Macheta acoperă obiectul integral. Defalcarea se completează după oferta financiară, iar pozițiile se corelează cu livrarea și facturarea efective.')
SaveDoc '01_Factura_macheta.docx' $b
$b=Base 'CERTIFICAT DE CONFORMITATE AL FURNIZORULUI'
$b+=(Inventory)+(Para 'Cerințe de referință: art. 5 și 18 din contract; caiet de sarcini [nr./dată]; oferta tehnică acceptată [nr./dată]; clarificări / acte adiționale [___].')+(Para 'Documente suport pentru fiecare model: declarația producătorului [emitent, nr., dată, model acoperit]; fișă tehnică [___]; raport de verificare [___]. Lista documentelor se completează în anexa 08.')+(Para 'Declarație de validat prin documente și verificări: INDUNOVA ROBOTICS S.R.L. confirmă că produsele efectiv identificate și predate sunt noi, originale, neutilizate, corespund cerințelor contractuale și specificațiilor documentelor de referință și sunt compatibile pentru funcționarea ca sistem integrat. Rezultate și eventuale abateri: [___].')+(Para 'Acest proiect de certificat al furnizorului nu reprezintă o declarație UE emisă de producător. Standardele și cerințele de conformitate se preiau numai din documentele aplicabile modelului exact.')+(Para 'Emitent: INDUNOVA ROBOTICS S.R.L. Responsabil autorizat: [nume, funcție]. Data / semnătură: [___].')
SaveDoc '02_Certificat_conformitate_proiect.docx' $b
$b=Base 'CERTIFICAT DE CALITATE'
$b+=(Inventory)+(Para 'Document suplimentar solicitat de beneficiar în pregătirea dosarului; art. 11 nu enumeră separat certificatul de calitate. Cerințele suplimentare din caietul de sarcini rămân de verificat.')+(Para 'Documente de calitate / trasabilitate: [___]. Raport de verificare și testare: anexa 08 nr. [___]/[___].')+(Para 'Se consemnează starea fizică, integritatea, identificarea, completitudinea, corespondența tehnică și rezultatele probelor funcționale pentru toate pozițiile. Concluzie privind calitatea: [___]. Neconformități / măsuri: [___].')+(Para $warranty)+(Para 'Responsabil verificări: [nume, funcție, semnătură]. Emitent: INDUNOVA ROBOTICS S.R.L.; reprezentant autorizat [___]; semnătură [___].')
SaveDoc '03_Certificat_calitate_proiect.docx' $b
$b=Base 'AVIZ DE ÎNSOȚIRE A MĂRFII / EXPEDIȚIE'
$b+=(Para 'Loc încărcare: [___]. Destinație: sediul beneficiarului din Călărași, str. Constantin Dobrogeanu Gherea nr. 39, sau locația indicată de acesta: [confirmare/adresă]. Data / ora expedierii: [___].')+(Inventory)+(Para 'Cantitățile din coloana contractuală sunt repere; în aviz se confirmă exclusiv cantitățile efectiv expediate. Componentele sistemului de securitate și accesoriile se individualizează în inventarul 09.')+(Para 'Transportator/delegat: [___]. Auto / AWB: [___]. Colete: [___]. Ambalaje originale și protecție pentru transport: [verificat de ___].')+(Para 'Motiv: livrare conform contractului nr. 9/29.07.2026. Factura asociată: [nr./dată, dacă este emisă după îndeplinirea art. 8 alin. (2)]. Documente însoțitoare: [lista și numerele din anexa 08].')+(Para 'Predat de: [___]. Preluat pentru transport de: [___]. Primit de: [___]. Data/ora și semnături: [___]. Diferențe: [___].')
SaveDoc '04_Aviz_expeditie_proiect.docx' $b
$b=Base 'PROCES-VERBAL DE PREDARE-PRIMIRE ȘI RECEPȚIE'
$b+=(Para 'Tip: [finală / constatare intermediară – se selectează în funcție de operațiunile efectiv încheiate]. Loc: [___]. Data: [___]. Reprezentanți/comisie beneficiar: [nume, funcții]. Reprezentanți furnizor: [___].')+(Inventory)+(Para 'Referințe: aviz [___]; oferta tehnică [___]; caiet de sarcini [___]; oferta financiară [___]; inventar detaliat 09; SN camere în anexa 06; raport de probe și documente în anexa 08.')+(Para 'Conform art. 14–16, recepția se realizează după livrare, instalare, configurare și testare și cuprinde verificarea cantitativă, calitativă și funcțională. Rezultatele reale sunt consemnate în anexa 08.')+(Para 'Instalarea tuturor echipamentelor, montarea DVR/NVR și suporturilor, conectarea cablurilor, iluminării și interfețelor, configurarea, verificarea comunicației, testarea sistemului și punerea în funcțiune: [date, executanți, rezultate]. Instruirea de bază inclusă în preț potrivit art. 7: [data, participanți, conținut, confirmări].')+(Para 'Bunuri și documente lipsă: [___]. Neconformități / rezerve: [___]. Termene și responsabili: [___]. Decizia beneficiarului: [recepție finală fără obiecțiuni / recepție cu rezerve / refuz total sau parțial / remediere și reverificare]. Se selectează și se motivează după verificări.')+(Para 'Îndeplinirea integrală a obiectului contractual: [confirmare numai după verificarea tuturor pozițiilor, serviciilor și documentelor]. Recepția doar a celor șase camere nu dovedește recepția finală a întregului contract.')+(Para $warranty)+(Para 'Valoare contractuală integrală: 57.851,24 lei fără TVA. Facturarea și plata se corelează cu art. 8. Data semnării de ambele părți: [___].')+(Para $sign)
SaveDoc '05_Proces_verbal_receptie_proiect.docx' $b
$b=Base 'CERTIFICAT DE GARANȚIE'
$b+=(Para 'Produse acoperite: inventarul detaliat 09, cu modelele, seriile/loturile și cantitățile efectiv livrate. Cele șase camere Luxonis sunt individualizate în anexa 06. Aviz [___]; PV final fără obiecțiuni [___]; factură [___].')+(Para $warranty)+(Para 'Garanția acoperă defectele de fabricație și material, neconformitățile tehnice și deficiențele de funcționare apărute în condiții normale de utilizare (art. 20 alin. (2)).')+(Para 'Fără costuri suplimentare: diagnosticare, reparare, înlocuirea componentelor defecte, înlocuirea produsului dacă repararea nu este posibilă într-un termen rezonabil și suport tehnic privind utilizarea echipamentelor (art. 21).')+(Para 'Primirea sesizării se confirmă într-o zi lucrătoare. Intervenția începe în maximum 5 zile lucrătoare de la notificarea beneficiarului. Dacă produsul nu poate fi reparat în maximum 10 zile lucrătoare, se înlocuiește cu unul nou, cu caracteristici tehnice cel puțin echivalente (art. 22).')+(Para 'Sesizări și suport: INDUNOVA ROBOTICS S.R.L.; persoană de contact [___]; telefon [___]; e-mail [___]; adresă service [___]. Beneficiarul comunică identificarea produsului, descrierea defecțiunii și datele de contact.')+(Para 'Data începerii: [___]. Durata finală conform ofertei, minimum 24 luni: [___]. Data expirării: [___]. Emitent / reprezentant: [___]. Semnătură: [___].')
SaveDoc '07_Certificat_garantie_proiect.docx' $b
$b=Base 'ANEXA 08 – RAPORT DE INSTALARE, PROBE, INSTRUIRE ȘI DOCUMENTE PREDATE'
$r=@();$r+=,@('Verificare conform art. 12 și 15','Rezultat / dovadă / responsabil');foreach($x in @('Corespondență cu oferta tehnică și caietul de sarcini','Existența accesoriilor și integritatea echipamentelor','Instalarea camerelor video și montarea DVR/NVR','Instalarea camerelor Machine-Vision și a suporturilor','Conectarea cablurilor, instalarea iluminării și interfețelor','Configurarea echipamentelor și verificarea comunicației','Funcționarea sistemului video și DVR/NVR; calitatea imaginilor','Funcționarea celor șase camere Machine-Vision','Funcționarea iluminării și a interfețelor USB','Transmiterea imaginilor și compatibilitatea componentelor','Funcționarea aplicațiilor software','Acces local și de la distanță, dacă este prevăzut în ofertă','Testarea întregului sistem și punerea în funcțiune','Instruirea de bază: data, formator, participanți, subiecte')){$r+=,@($x,'[de completat; neaplicabil numai cu justificare]')};$b+=Table $r
$b+=(Para 'Documente de predat conform art. 11 și 18 – se înscriu identificatorul, data și confirmarea predării: factura (cu respectarea momentului emiterii din art. 8); aviz dacă este cazul; certificat de garanție; certificat de conformitate; fișe tehnice; manuale de utilizare; licențe software dacă este cazul; alte documente din caietul de sarcini. Suplimentar: certificatul de calitate solicitat, inventarul complet și SN. Situație: [___].')+(Para 'Observații, probe nereușite și măsuri: [___].')+(Para $sign)
SaveDoc '08_Raport_probe_documente_instruire.docx' $b
$b=Base 'ANEXA 09 – INVENTAR COMPLET PENTRU LIVRARE ȘI RECEPȚIE'
$b+=(Inventory)+(Para 'Detalierea sistemului video de securitate: 8 camere [marcă/model/SN pentru fiecare]; DVR/NVR [model/SN/cantitate conform ofertei]; HDD [model/capacitate/SN/cantitate conform ofertei]; accesorii [denumire/cantitate].')+(Para 'Detalierea celorlalte poziții: [model, specificații, SN sau lot dacă există, cantitate efectivă]. Pentru bunurile fără serie se consemnează „fără SN” numai după verificare.')+(Para 'Iluminarea, controlerele cu sursă și interfețele USB sunt poziții distincte în art. 5. Dacă sunt implementate prin componente integrate în camere, corespondența trebuie documentată față de oferta tehnică și caietul de sarcini; fotografiile ambalajelor nu demonstrează această corespondență.')+(Para $sign)
SaveDoc '09_Inventar_complet_livrare.docx' $b
$check=@'
# Dosarul de livrare – contract nr. 9/29.07.2026

Au fost citite cele 11 pagini transmise ca imagini. Caietul de sarcini, oferta tehnică, oferta financiară și eventualele clarificări/acte adiționale nu sunt incluse. Documentele Word au fost actualizate pe baza contractului și fotografiilor; rămân proiecte până la completarea faptelor și datelor lipsă.

## Obiectul de livrat – art. 5, pagina 4

| Poziție | Cantitate contractuală |
|---|---:|
| Sistem video de securitate cu 8 camere video, DVR/NVR, HDD și accesorii | 1 sistem |
| Camere industriale Machine-Vision | 6 buc. |
| Suporturi pentru camere industriale | 6 buc. |
| Cabluri de comunicație și alimentare | 6 buc. |
| Sisteme de iluminare industrială | 6 buc. |
| Controlere de iluminare cu sursă de alimentare | 6 buc. |
| Interfețe hardware USB 3.0 sau echivalent | 6 buc. |
| Toate accesoriile necesare funcționării complete | inventar de completat |

Prețul total este 57.851,24 lei fără TVA (art. 6). Include transport, manipulare, instalare, configurare, testare, punere în funcțiune și instruire de bază (art. 7). Contractul nu oferă prețuri unitare sau modelele concrete ale produselor.

## Informațiile care mai trebuie

1. **Oferta financiară acceptată**: prețurile pe poziții și modul de includere a accesoriilor/serviciilor, pentru reconcilierea cu 57.851,24 lei fără TVA.
2. **Oferta tehnică și caietul de sarcini**, plus eventuale clarificări/acte adiționale: modele, specificații, configurație, documente suplimentare și garanție dacă depășește 24 luni. Trebuie verificată corespondența Luxonis OAK-D-PRO-AF cu oferta acceptată.
3. **Inventarul real al celorlalte bunuri**: marca/modelul și seriile celor 8 camere de securitate, DVR/NVR și HDD; modelele și cantitățile suporturilor, cablurilor, iluminării, controlerelor cu surse, interfețelor USB și accesoriilor. Dacă unele funcții sunt integrate, trebuie documentată corespondența cu pozițiile contractuale, fără a presupune că cele șase camere acoperă automat aceste poziții.
4. **Stadiul efectiv**: se predă întregul obiect acum? Ce s-a predat/facturat anterior? Sunt terminate instalarea, configurarea, testarea, punerea în funcțiune și instruirea? Rezultatele reale, eventualele lipsuri și rezerve.
5. **Date documente și transport**: seriile/numerele și datele facturii, avizului, certificatelor și PV; adresa efectivă de livrare; data/ora expedierii; delegat/transportator, auto/AWB, colete și persoanele de predare/primire.
6. **Date fiscale și bancare lipsă**: IBAN și bancă INDUNOVA; statut/cod TVA la emitere și cota/regimul aplicabil. Contractul înscrie CUI 52786670 fără prefix RO; nu se presupune din acest fapt statutul fiscal actual. Eventuale facturi/plăți anterioare.
7. **Conformitate și documentație**: declarațiile și certificatele producătorilor pentru modelele exacte, fișele tehnice, manualele, eventualele licențe și documentele suplimentare din caietul de sarcini. Responsabilul autorizat pentru certificate și contactul service.
8. **Recepție**: persoanele/comisia și funcțiile, data/locul, raportul probelor, participanții la instruire și semnatarii efectivi. Administratorii sunt deja identificați în contract; se precizează dacă semnează alte persoane împuternicite.

## Reguli preluate din contract pentru documente

- Art. 8, pagina 5: factura se emite după livrare, instalare, configurare, testare și punere în funcțiune confirmate prin PV semnat de ambele părți; plata integrală este prevăzută la data semnării PV. Art. 11 enumeră factura între documentele însoțitoare; dosarul corelează emiterea cu momentul stabilit expres în art. 8.
- Art. 10: termen de livrare maximum 45 zile calendaristice de la semnare; destinație sediul beneficiarului sau locația indicată; ambalaje originale.
- Art. 11, pagina 6: factură, aviz dacă este cazul, certificat de garanție, certificat de conformitate, fișe tehnice, manuale, licențe dacă este cazul și alte documente din caietul de sarcini. Certificatul de calitate este pregătit suplimentar la cererea utilizatorului.
- Art. 12 și 14–16: instalare/configurare/testare pentru întregul sistem; recepție cantitativă, calitativă și funcțională, semnată de ambele părți.
- Art. 20–22, pagina 9: minimum 24 luni garanție de la PV final fără obiecțiuni, sau mai mult conform ofertei; confirmare sesizare într-o zi lucrătoare; începere intervenție în maximum 5 zile lucrătoare; înlocuire dacă repararea nu este posibilă în maximum 10 zile lucrătoare.

## Date preluate

Furnizor: INDUNOVA ROBOTICS S.R.L., CUI 52786670, J2025082650004, sat Botești, oraș Zlatna, nr. 37, jud. Alba; administrator Pușcău Bogdan-Sebastian.

Beneficiar: INDUSTRY DEVELOPMENT PRINTER S.R.L., CUI RO50436813, J2024016413007, Călărași, str. Constantin Dobrogeanu Gherea nr. 39, jud. Călărași; administrator Cercel Paraschiva.

Proiect 334979; contract de finanțare 390064/16.09.2025. Titlu: „Sistem integrat bazat pe inteligență artificială (AI) pentru monitorizarea în timp real a defectelor în procesul de imprimare 3D”.

Camerele fotografiate: Luxonis OAK-D-PRO-AF, SKU A00546, lot 2604TA. Seriile sunt în anexa 06 și trebuie confruntate cu dispozitivele la predare. Fotografiile identifică produsele, dar nu demonstrează singure conformitatea tehnică sau funcționarea.
'@
[System.IO.File]::WriteAllText((Join-Path $outDir '00_Informatii_necesare.md'),$check,[System.Text.UTF8Encoding]::new($false))
$b=Base 'LISTĂ DE COMPLETARE A DOSARULUI'
foreach($line in ($check -split "`r?`n")){$b+=Para $line}
SaveDoc '00_Informatii_necesare.docx' $b
$zipPath=Join-Path $outDir 'Dosar_livrare_camere_PROIECT.zip'
$fs=[System.IO.File]::Open($zipPath,[System.IO.FileMode]::Create);$zip=[System.IO.Compression.ZipArchive]::new($fs,[System.IO.Compression.ZipArchiveMode]::Create)
Get-ChildItem -LiteralPath $outDir -File | Where-Object {$_.Extension -in '.docx','.md'} | ForEach-Object {[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$_.FullName,$_.Name) | Out-Null}
$zip.Dispose();$fs.Dispose()
# Verify that each generated Word document contains well-formed XML.
Get-ChildItem -LiteralPath $outDir -Filter '*.docx' | ForEach-Object {$z=[System.IO.Compression.ZipFile]::OpenRead($_.FullName);$reader=[System.IO.StreamReader]::new($z.GetEntry('word/document.xml').Open());$xml=[xml]$reader.ReadToEnd();$reader.Dispose();$z.Dispose();[pscustomobject]@{Document=$_.Name;XMLValid=($null -ne $xml.DocumentElement);Bytes=$_.Length}}
