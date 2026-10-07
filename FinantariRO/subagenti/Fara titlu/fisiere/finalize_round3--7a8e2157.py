from pathlib import Path
import json,hashlib,html,re
base=Path('2.1 Legislatie si eligibilitate'); out=base/'Recuperari Runda3'
op=json.loads((out/'Registru_op_Runda3.json').read_text(encoding='utf-8'))
alt=json.loads((out/'Registru_alternative_Runda3.json').read_text(encoding='utf-8'))
records=[x for x in op+alt if x['status']=='DESCARCAT_DE_VALIDAT' and x['nume']!='Plan_educatie_digitala_COM2020_624']
archive=out/'Carta_tratate_2016_RO_original.download'
archive.rename(out/'Carta_tratate_2016_RO_original.zip')
cm=json.loads((out/'Manifest_Carta_2016.json').read_text(encoding='utf-8'))
records.append({'nume':'Carta_drepturi_UE','url_sursa':'https://op.europa.eu/o/opportal-service/download-handler?identifier=1194001c-c811-11e6-a6db-01aa75ed71a1&format=pdf&language=ro&productionSystem=cellar&part=','data':'2026-10-07','status':'DESCARCAT','fisier':'Carta_tratate_2016_1.pdf',**{k:cm[0][k] for k in ('sha256','pagini','octeti')},'arhiva_originala':'Carta_tratate_2016_RO_original.zip','coperta':'Carta_tratate_2016_2.pdf'})
details={
'Regulament2021_1057':('RO; act inițial JO L231/30.06.2021, 39 pagini; NU consolidat 2025. EUR-Lex indică o formă consolidată la20.09.2025, care nu este această copie.','Art.4(1)(f),6,8,17; PDF pp17,19–21,23. Acces egal la educație, nediscriminare/accesibilitate, Carta, indicatori și monitorizare.'),
'Regulament2024_2509':('RO; act inițial JO L2024/2509,26.09.2024,239 pagini. NU certifică toate rectificările ulterioare. În sursa EUR-Lex FR apare o rectificare11.08.2026; aplicabilitatea ei versiunii RO nu este certificată.','Art.33 pp52–53; art.61 p71; art.63 pp72–73. Economie/eficiență/eficacitate, conflicte inclusiv percepute și gestiune partajată. Nu se importă automat regulile granturilor în gestiune directă în apelul PEO.'),
'Regulament2023_1676':('RO; act inițial JO L216/01.09.2023,28 pagini, cu anexă. Nu este certificat drept ultimă consolidare.','Art.1–3 p2 și anexa pct1.1–1.4 pp3–4: domeniu educație formală, participare verificată, categorii acoperite, proporționalizare și ajustare. Aplicarea concretă ED01/ED02 rămâne conform GSCS, fără înlocuirea unilaterală a baremelor.'),
'Recomandare2022_C476_01':('RO; recomandare8.12.2022,JO C476/15.12.2022,11 pagini. Privește îngrijirea pe termen lung, exact cum este citată în GSCS; nu este recomandarea obiectivelor Barcelona pentru educație timpurie.','Punctele6–10 pp6–8 și anexa principiilor de calitate pp10–11: calitate, prevenirea abuzului, condiții de muncă, competențe și guvernanță. Relevanța pentru acest apel nu extinde activitățile eligibile la serviciul de vârstnici al ONG.'),
'Agenda_competente_COM2020_274':('EN; COM(2020)274final/01.07.2020,26 pagini, copie oficială transmisă Parlamentului Austriei. Nu include automat documentele de lucru SWD separate.','Introducere pp2–4 și acțiunile6/8 pp14,17: competențe pentru tranziția verde/digitală, învățare pe parcursul vieții. Educația timpurie este baza traseului; relevanță pentru formarea personalului și resurse pedagogice.'),
'Plan_educatie_digitala_COM2020_624_RO':('RO; COM(2020)624final/30.09.2020,23 pagini. Separat există publicația editorială oficială EN de20pagini; aceasta nu înlocuiește COM în registrul principal. SWD(2020)209 nu este inclus automat.','Secțiunile4.1/4.2 pp12,15; acțiunile4–6 p15 și siguranță/etică/drepturile copiilor p18. Conținut digital accesibil și pregătirea profesorilor; nu creează drept independent de finanțare pentru echipamente.'),
'Pact_verde_COM2019_640':('RO; COM(2019)640final/11.12.2019, transmis prin Consiliu15051/19,28 pagini. Anexa de calendar a COM nu este declarată recuperată separat.','Secțiunea2.2.4 și pasajele despre educație: implicarea elevilor/părinților/comunității, competențe climatice, materiale și formarea profesorilor. Sprijină justificarea temelor de mediu, nu inventează punctaj sau eligibilitate nouă.'),
'Carta_drepturi_UE':('RO; text2016 în volumul oficial Tratate consolidate,408pagini+copertă2pagini; Carta la pp393–405. Descărcarea oficială este ZIP cu fișiere.pdfx4, păstrate integral caPDF; textul extras poate conține duplicări de planșe din ediția de tipar.','Art.1,7–8,14,20–26,31,51–54, pp393–405; demnitate/date, educație, nediscriminare, interes superior al copilului, incluziune dizabilități, muncă și domeniul de aplicare. Nu s-au citit integral tratatele din cele408pagini.')}
for r in records:
 r['status']='DESCARCAT_VALIDAT_IDENTITATE_SI_TEXT'
 r['versiune_si_limite'],r['pasaje_consultate']=details[r['nume']]
 r['limita_lecturii']='Au fost consultate pasajele indicate, nu se afirmă lectura juridică integrală a întregului document.'
(out/'Registru_validat_Runda3.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
mapping={'Regulament2021_1057_FSE':'Regulament2021_1057','Regulament2024_2509_financiar':'Regulament2024_2509','Regulament2023_1676_costuri_unitare':'Regulament2023_1676','Recomandare2022_C476_01_ingrijire_lunga':'Recomandare2022_C476_01','Carta_drepturi_UE':'Carta_drepturi_UE'}
reg=json.loads((base/'Registru_final_legislatie.json').read_text(encoding='utf-8-sig'))
for x in reg:
 if x['nume'] in mapping:
  r=next(z for z in records if z['nume']==mapping[x['nume']]);x.update(status='DESCARCAT',fisier='Recuperari Runda3/'+r['fisier'],url_descarcare=r['url_sursa'],octeti=r['octeti'],sha256=r['sha256'],pagini=r['pagini'],data_verificarii='2026-10-07',observatie=r['versiune_si_limite'],pasaje_consultate=r['pasaje_consultate'])
(out/'Registru_legislatie_actualizat_35_surse.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
rows=[]
for r in records:rows.append('<tr>'+''.join('<td>'+html.escape(str(r.get(k,'')))+'</td>' for k in ('nume','fisier','pagini','versiune_si_limite','pasaje_consultate','url_sursa','sha256'))+'</tr>')
(out/'Registru_validat_Runda3.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Recuperare documentară — Runda3</title><style>body{font:15px Arial;margin:24px}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:9px;vertical-align:top;overflow-wrap:anywhere}th{background:#e5eef7}</style><h1>Recuperare documentară — 07.10.2026</h1><p>8/8 documente vizate recuperate. Registrul legislativ de 35 surse are acum copii pentru35/35. Aceasta confirmă existența fișierelor, nu consolidarea actuală sau analiza juridică exhaustivă. Formele inițiale și limitele sunt precizate mai jos.</p><table><tr>'+''.join('<th>'+x+'</th>' for x in ('Document','Fișier','Pagini','Versiune și limite','Pasaje consultate','Sursă','SHA256'))+'</tr>'+''.join(rows)+'</table></html>',encoding='utf-8')
print('documente',len(records),'registru',len(reg),'descarcate',sum(x['status']=='DESCARCAT' for x in reg))
