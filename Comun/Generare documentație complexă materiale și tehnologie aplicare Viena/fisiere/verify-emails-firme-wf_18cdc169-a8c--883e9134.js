export const meta = {
  name: 'verify-emails-firme',
  description: 'Verifica/gaseste adresele de email oficiale pentru cele 11 firme (Prüfingenieur + BauKG) Schallergasse',
  phases: [{ title: 'Cautare email-uri' }],
}

const SCHEMA = {
  type: 'object',
  required: ['firma', 'email_gasit', 'confidenta', 'sursa_url'],
  properties: {
    firma: { type: 'string' },
    email_candidat: { type: 'string', description: 'emailul presupus initial (poate fi gol)' },
    email_gasit: { type: 'string', description: 'emailul OFICIAL gasit pe site (sau gol daca nu s-a gasit)' },
    coincide_cu_candidatul: { type: 'boolean' },
    website_oficial: { type: 'string' },
    sursa_url: { type: 'string', description: 'URL-ul paginii Impressum/Kontakt de unde s-a extras' },
    confidenta: { type: 'string', enum: ['inalta', 'medie', 'scazuta'] },
    telefon_confirmat: { type: 'string' },
    nota: { type: 'string', description: 'observatii: alt email de contact, formular in loc de email, etc.' },
  },
}

phase('Cautare email-uri')

const COMMON = `Esti asistent de verificare a datelor de contact. Sarcina: gaseste adresa de e-mail OFICIALA de contact a firmei de mai jos, de pe SITE-UL EI OFICIAL (pagina Impressum sau Kontakt). Foloseste WebSearch (allowed_domains poate ajuta) si WebFetch pe pagina de contact/impressum a firmei. NU inventa. Daca gasesti mai multe (office@, kontakt@), alege-o pe cea de contact general. Verifica sa se potriveasca cu numele si adresa firmei (ca sa nu confunzi cu alta firma). Daca nu gasesti un email pe site (doar formular de contact), spune asta in 'nota' si lasa email_gasit gol. Returneaza prin StructuredOutput. Raspunde in romana la nota.`

const FIRME = [
  { firma: 'PCD ZT-GmbH (Ziviltechniker)', adr: 'Schoenbrunner Strasse 297, 1120 Wien', tel: '+43 1 877 34 25', cand: '(lipsa)', hint: 'birou de ingineri/Ziviltechniker, Prüfingenieur, 1120 Wien. Cauta domeniul oficial (posibil pcd.at sau similar).' },
  { firma: 'DI Janka Neid (Ziviltechniker/Prüfingenieur)', adr: 'Aichholzgasse 26/2, 1120 Wien', tel: '+43 676 633 78 15', cand: 'office@neid.co.at', hint: 'site probabil neid.co.at' },
  { firma: 'Toms Ziviltechniker GmbH', adr: 'Margaretenstrasse 93, 1050 Wien', tel: '+43 1 310 07 07', cand: 'office@toms.at', hint: 'site toms.at' },
  { firma: 'POTYKA & Partner ZT GmbH', adr: 'Altmannsdorfer Strasse 76A/9, 1120 Wien', tel: '+43 1 877 25 71', cand: 'office@potyka-partner.at', hint: 'site potyka-partner.at' },
  { firma: 'DI Remzi Avunduk (Ziviltechniker)', adr: '1220 Wien', tel: '+43 1 202 19 75', cand: 'office@zt-avunduk.at', hint: 'site zt-avunduk.at; gaseste si adresa exacta din 1220 Wien' },
  { firma: 'KPPK Ziviltechniker GmbH', adr: 'Gumpendorfer Strasse 132, 1060 Wien', tel: '+43 1 535 21 23', cand: 'office@kppk.at', hint: 'site kppk.at' },
  { firma: 'SSB Technisches Buero GmbH', adr: 'Liechtensteinstrasse 143-145/4, 1090 Wien', tel: '+43 1 952 18 78', cand: 'kontakt@ssb.wien', hint: 'site ssb.wien' },
  { firma: 'Baumeister DI Paknehad & Partner GmbH', adr: 'Erdbergstrasse 10/62, 1030 Wien', tel: '+43 670 19 84636', cand: 'office@paknehad-bau.at', hint: 'site paknehad-bau.at' },
  { firma: 'BAU-WERTE - Baumeister DI Stefan Lechner', adr: 'Gertrude-Froehlich-Sandner-Strasse 2, 1100 Wien', tel: '+43 664 22 41 591', cand: 'baumeister@bau-werte.biz', hint: 'site bau-werte.biz' },
  { firma: 'BK Baumanagement GmbH (DI Bernhard Kazda)', adr: 'Reisberggasse 6, 1230 Wien', tel: '+43 676 9128084', cand: 'kazda@bk-b.at', hint: 'site bk-b.at' },
  { firma: 'Themis Baumanagement GmbH', adr: 'Paulanergasse 15, 1040 Wien', tel: '+43 463 931 860', cand: 'office@themis.co.at', hint: 'site themis.co.at; tel 0463 = Klagenfurt, verifica birou Wien' },
]

const results = await parallel(FIRME.map(f => () =>
  agent(COMMON + `\n\nFIRMA: ${f.firma}\nADRESA: ${f.adr}\nTELEFON: ${f.tel}\nEMAIL CANDIDAT (de verificat): ${f.cand}\nINDICIU: ${f.hint}`,
    { label: 'email:' + f.firma.slice(0, 24), schema: SCHEMA })
))

const ok = results.filter(Boolean)
log(`Verificate: ${ok.length}/${FIRME.length}`)
return { rezultate: FIRME.map((f, i) => ({ firma: f.firma, candidat: f.cand, rezultat: results[i] })) }