export const meta = {
  name: 'analiza-planse-schallergasse',
  description: 'Echipa de specialisti analizeaza plansele si documentele proiectului Schallergasse 35 Viena',
  phases: [{ title: 'Analiza planse', detail: 'arhitect, instalatii, structura, documente' }],
}

const DIR = String.raw`D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)`
const P29 = DIR + String.raw`\Arhitectura Madalina\2026.07.29`

const SCHEMA = {
  type: 'object',
  required: ['sinteza', 'constatari'],
  properties: {
    sinteza: { type: 'string', description: 'Sinteza analizei in romana, 1-2 paragrafe' },
    constatari: { type: 'array', items: { type: 'string' }, description: 'Constatari importante pentru lista de materiale si documentele descriptive' },
    incaperi: { type: 'array', items: { type: 'object', properties: {
      nivel: { type: 'string' }, unitate: { type: 'string' }, denumire: { type: 'string' },
      arie_mp: { type: 'number' }, finisaj: { type: 'string' }, perimetru_m: { type: 'number' },
      inaltime_m: { type: 'number' }, obs: { type: 'string' } } } },
    materiale: { type: 'array', items: { type: 'object', properties: {
      material: { type: 'string' }, cantitate: { type: 'string' }, um: { type: 'string' },
      zona: { type: 'string' }, obs: { type: 'string' } } } },
    note_tehnice: { type: 'array', items: { type: 'string' } }
  }
}

phase('Analiza planse')

const COMMON = `Esti membru intr-o echipa de super-specialisti care pregateste lista completa de materiale (achizitie de la Dedeman) si documentatia tehnica pentru renovarea imobilului Schallergasse 35, 1120 Wien (demisol + parter + 3 etaje + mansarda pe 2 niveluri). Proiect: recompartimentari interioare si mansardare. Citeste FIECARE plansa PDF indicata cu tool-ul Read (sunt PDF-uri de 1 pagina, lizibile vizual si textual). Raspunde in limba romana. Fii exhaustiv si precis: extrage cote, arii, straturi, adnotari, legende, tabele de arii utile. Returneaza datele prin StructuredOutput.`

const tasks = [
  {
    label: 'arhitect:planuri-noi',
    prompt: COMMON + `

ROL: Arhitect sef. Citeste plansele PROPUSE (varianta finala 2026.07.29):
1. "${P29}\\A,01 Plan demisol - Yoga.pdf"
2. "${P29}\\A.02 Plan parter.pdf"
3. "${P29}\\A.03 Plan etaj I-III.pdf"
4. "${P29}\\Sectiunea AA.pdf"

EXTRAGE pentru fiecare nivel:
- Tabelele "ARIE UTILA" complete: fiecare incapere cu denumire, arie mp, finisaj pardoseala (F:), perimetru (P:), inaltime (H:)
- Tipurile de pereti noi (Z.1, Z.2 etc.) cu stratificatia exacta scrisa in legenda
- Adnotarile cu finisaje: inaltimi faianta (ex. "faianta pana la +2.40m"), caramizi de sticla (pozitii, randuri, cote montaj), inaltari de pardoseala, cazi ingropate, inchideri cu zidarie
- Usile: dimensiuni si tipuri (din cotele de goluri, ex. 90/210, glisante)
- Elemente speciale: lift, scari, balustrade (ABSTURZSICHERUNG), platforme
- Din Sectiunea AA: inaltimi de nivel, cote, structura planseelor vizibile
Completeaza campul "incaperi" cu TOATE incaperile din toate tabelele de arii.`
  },
  {
    label: 'arhitect:detalii+existent',
    prompt: COMMON + `

ROL: Arhitect de detalii + releveu. Citeste plansele:
1. "${P29}\\D-01 Detaliu streasina.pdf"
2. "${P29}\\D-02 Detaliu lucarna.pdf"
3. "${P29}\\D-03 Detaliu lucarna_atic.pdf"
4. "${P29}\\A.04 Plan parter_existent.pdf"
5. "${P29}\\A.05 Plan etaj I-III_existent.pdf"
6. "${P29}\\A.06 Plan demisol_existent.pdf"

EXTRAGE:
- Din detaliile D-01..D-03: stratificatiile COMPLETE ale invelitorii, streasinii, lucarnei si aticului (fiecare strat cu grosime si material, de ex. tabla faltuita, astereala, contrasipci, folie anticondens, vata, bariera vapori, gips-carton), sisteme de jgheaburi/burlane, sorturi de tabla, racorduri
- Din planurile existente vs. propuse: ce pereti se demoleaza, ce goluri noi se creeaza, ce zidarie se inchide - pentru capitolul demolari/reparatii
- Orice specificatie de material scrisa pe detalii (ex. tip tabla, tip membrana)
Completeaza "materiale" cu fiecare strat/material identificat pe detalii, cu zona si grosimea.`
  },
  {
    label: 'inginer:electrice',
    prompt: COMMON + `

ROL: Inginer instalatii electrice. Citeste plansele:
1. "${P29}\\instalatii\\IE01_Plan demisol.pdf"
2. "${P29}\\instalatii\\IE02_Plan parter.pdf"
3. "${P29}\\instalatii\\IE03_Plan etaj curent.pdf"
4. "${P29}\\instalatii\\IE04_Plan mansarda 1.pdf"
5. "${P29}\\instalatii\\IE05_Plan mansarda 2.pdf"

CONTEXT: o extractie anterioara (2026.05.28, aceleasi planse) a numarat: prize duble 116, prize simple 72, intrerupatoare 121, iluminat tavan IP20 40, suspendate 53, IP44/IP65 47, senzori PIR 16, tablouri 14 (11 TE-TOP + TE-SC + TE-YOGA + FDCP); cabluri estimate 4500 m; copex 4650 m. IE03 se multiplica x3 (etaje 1-3).

SARCINA:
- Citeste legenda fiecarei planse si valideaza/corecteaza numaratoarea pe fiecare nivel (raporteaza per plansa: iluminat tavan, suspendat, IP44, liniar, aplice, senzori, intrerupatoare pe tipuri daca legenda le distinge, prize duble/simple/IP44, tablouri, trasee)
- Noteaza specificatiile scrise pe planse: tipuri de circuite, sectiuni de cablu daca sunt notate, cote de montaj, note tehnice (ex. protectii la treceri)
- Completeaza "materiale" cu lista de materiale electrice rezultata (cu cantitati recomandate de achizitie, +10% rezerva).`
  },
  {
    label: 'inginer:sanitare-termice',
    prompt: COMMON + `

ROL: Inginer instalatii sanitare si termice. Citeste plansele:
1. "${P29}\\instalatii\\IT01_Plan demisol.pdf"
2. "${P29}\\instalatii\\IT02_Plan parter.pdf"
3. "${P29}\\instalatii\\IT03_Plan etaj curent.pdf" (se multiplica x3 pentru etajele 1-3)
4. "${P29}\\instalatii\\IT04_Plan mansarda 1.pdf"
5. "${P29}\\instalatii\\IT05_Plan mansarda 2.pdf"

EXTRAGE:
- Legenda completa a fiecarei planse (simboluri obiecte sanitare, radiatoare, incalzire in pardoseala, centrale/boilere, coloane, ventilatie)
- Numara obiectele sanitare pe nivel: WC (suspendate cu rezervor incastrat Geberit?), lavoare, cazi, dusuri, chiuvete bucatarie, masini spalat, sifoane pardoseala
- Sisteme de incalzire: radiatoare (numar, pozitii sub ferestre), incalzire in pardoseala (zone), centrale termice / surse
- Trasee: coloane de scurgere (pozitii ghene), alimentari apa rece/calda, ventilare bai peste acoperis
- Note tehnice scrise pe planse (numerotate)
- Completeaza "materiale" cu lista estimata de materiale sanitare+termice pentru achizitie (tevi PPR/PEX cu metraje estimate pe baza traseelor si numarului de consumatori, canalizare PP pe diametre, rezervoare incastrate, obiecte sanitare premium, radiatoare, sistem incalzire pardoseala cu placa tacker+teava+distribuitori, izolatie tevi), cu cantitati si rezerva 10%.`
  },
  {
    label: 'structurist:statica+bauphysik',
    prompt: COMMON + `

ROL: Inginer structurist + fizica constructiilor. Surse:
1. Foloseste Glob pe "${DIR}\\Statik\\**\\*" si citeste fisierele text/PDF traduse din "${DIR}\\Statik\\OCR\\Tradus" (daca sunt multe, pe cele mai relevante: rezumate, memorii tehnice)
2. Citeste paginile 7-17 din "${DIR}\\12S35_EinrBPH_2022-03-22+2022-09-06_Abgabe.pdf" (catalogul Bauphysik cu tipurile de pereti/plansee aprobate: AW01, AW03, AW05, AW06, WTW01-05, IW01-04, SW01, VS01-04, DA01-04, FB02-04, AD01-02)
3. Citeste "${P29}\\Sectiunea AA.pdf"

EXTRAGE:
- Pentru FIECARE tip de element din catalogul Bauphysik (AW*, WTW*, IW*, SW*, VS*, DA*, FB*, AD*): stratificatia completa cu grosimi si cerintele (REI/EI, Rw dB, U W/m2K) - acestea sunt fundamentul documentului descriptiv
- Din statica: concluziile studiului geotehnic, interventiile structurale (planseu nou peste etajul 3, grinzi metalice, buiandrugi, groapa lift, scari metalice yoga: 7 trepte L=1.50m + podest 1.65x1.50m), clase de beton/otel specificate
- Constrangeri pentru executie: greutati admise pe planseele existente din lemn (Dippelbaum), sape usoare vs. grele
- Completeaza "materiale" cu materialele structurale necesare (beton, armatura, profile metalice, grinzi lemn, OSB, buiandrugi) cu cantitatile din centralizator unde le recunosti.`
  },
  {
    label: 'consultant:documente-proiect',
    prompt: COMMON + `

ROL: Consultant tehnic documentatie. Analizeaza folderele de documente ale proiectului:
1. Foloseste Glob pe "${DIR}\\00.Proiect\\**\\*" si listeaza structura
2. Citeste documentele-cheie gasite in "00.Proiect\\01. Behoerden + Eigentum\\01. Baubescheid + genehmigte Plaene" (autorizatia/bescheid daca exista PDF), "00.Proiect\\03. Einreichplanung - Planwechsel\\02. Baubeschreibung" si "00.Proiect\\07. Kosten + Ausschreibung" (Leistungsverzeichnisse, Materiallisten)
3. Citeste "${DIR}\\00.Claude\\01. Roadmap si Pasi Legali" si "02. Echipa si Roluri" (fisierele din ele) daca exista
4. Citeste "${DIR}\\Arhitectura Madalina\\2026.05.28\\Specificatii Ziduri + Planse Adnotate\\SPECIFICATII_Pereti_pe_Niveluri.docx" - foloseste python-docx prin Bash/PowerShell daca Read nu il poate citi direct

EXTRAGE:
- Cerintele legale/tehnice care conditioneaza materialele: clase de reactie la foc (A2, EI90/EI30), cerinte acustice (Rw 63-70 dB), cerinte termice (valori U), norme ÖNORM mentionate
- Ce liste de materiale/caiete de sarcini exista deja in proiect (denumiri fisiere + continut pe scurt)
- Restrictii de patrimoniu/fatada (§ 69, fatada stradala se pastreaza integral)
- Orice decizie de proiect relevanta pentru achizitii (lift Schindler 3300, usi EI2 30-C, numerotare Top-uri)
NU inventa: daca un document nu exista sau nu e lizibil, spune explicit.`
  },
]

const results = await parallel(tasks.map(t => () =>
  agent(t.prompt, { label: t.label, phase: 'Analiza planse', schema: SCHEMA })
))

log(`Analiza completa: ${results.filter(Boolean).length}/${tasks.length} specialisti au raportat`)
return { rapoarte: tasks.map((t, i) => ({ specialist: t.label, raport: results[i] })) }