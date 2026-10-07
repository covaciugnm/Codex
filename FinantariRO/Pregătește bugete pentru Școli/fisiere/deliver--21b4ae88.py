from pathlib import Path
import shutil, json, hashlib, html
from urllib.parse import quote

root=Path('Z:/00. Proiecte 2026/2026.11.27 - SCOLI ISJ CJRAE ONG PARTENER - PEO P7 7.e.3 Scoli pentru viitor')
out=Path(__file__).parent/'output'
analysis=root/'2. ANALIZA SI CLARIFICARI'
manifest=[]
for key,eur in [('minim','700000'),('maxim','1000000')]:
    dest=root/f'5.1 Buget {key} eligibil - {eur} EUR'
    dest.mkdir(exist_ok=True)
    source=out/f'Buget_{key}_doua_scenarii_contributie.xlsx'
    target=dest/source.name
    shutil.copy2(source,target)
    manifest.append({'file':str(target.relative_to(root)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (dest/'CITESTE_MA.txt').write_text('PROIECTARE IDEALA CONDITIONATA — 07.10.2026\n'
        'Bugetul este al intregului parteneriat. ONG-ul este partener, nu lider eligibil.\n'
        'Doua scenarii in Sinteza si selector in Parametri B22: minim acceptat / optimizare punctaj.\n'
        'Cotele coincid deoarece contributia suplimentara nu primeste puncte in grila. ONG 0%; lider 2% numai pentru categoria juridica modelata. Alte categorii impun alte cote.\n'
        'Alocarile pentru bunuri/servicii sunt anvelope de planificare, nu preturi de piata confirmate. Introduceti oferta unitara in Buget M si sursa/data in N; completati personalul extern eligibil inclus in serviciu in P.\n'
        'Salarizare permite calcul distinct pentru personal public. Selectia regimului si procentului necesita documente.\n'
        'Toate cele cinci activitati A1–A5 sunt incluse. Verificari distinge calculele de probele ramase deschise.\n'
        'Consultati raportul central, fisele de selectie, matricea de evaluare si auditul. 10/10 priveste proiectarea in perimetrul cunoscut, nu eligibilitatea certificata ori punctajul acordat.\n',encoding='utf-8')
    for name in [f'verification_{key}.json',f'errors_{key}.txt']:
        shutil.copy2(out/name,analysis/name)
(analysis/'Manifest_bugete_finale_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

items=[
('Lider eligibil si contributie','Selectarea unei scoli/ISJ/CJRAE eligibile; verificarea categoriei de finantare publica.','Fisa juridica, acreditare, sursa de finantare si declaratia contributiei. Cota 2% este ipoteza, nu regula universala.','Manager + jurist'),
('Scenariu teritorial si punctaj','Pentru tinta100: parteneriat ITI Delta Dunarii real, contributie SIDD si aviz ADI. Pentru alte teritorii: plafon99.','Nu se inventeaza localizarea. Selectia urmeaza fisa scolilor si nevoile reale.','Manager + evaluator'),
('Scoli, elevi si diagnostic','Selectati scoli pentru480/720 elevi unici si nevoi demonstrate; rezerve de recrutare motivate.','Fisa scolilor, acorduri, date anonimizate, evaluare initiala si inventar dotari.','Educatie'),
('Experienta relevanta ONG','Selectati proiectele finalizate relevante din ultimii3ani, apoi probele distincte pentru3.6 si3.7.','Contracte, rapoarte finale, acceptari, indicatori si documentele statutare; experienta sociala cu varstnici nu este suficienta singura.','Scriere + ONG'),
('Oferte si justificarea costurilor','Obtineti surse comparabile pentru13linii; recalculati cantitati si valori dupa diagnostic.','Foaia Achizitii propune specificatii; trei surse este recomandare a echipei, nu obligatie universala atribuita ghidului.','Economist + achizitii'),
('Salarizare individuala','Stabiliti regimul fiecarui post, baza legala, salariul de baza, majorarea si orele reale.','Grilele generale sunt arhivate; grilele individuale ale institutiilor se obtin dupa alegerea liderului. Modelul nu acorda automat40%.','Economist + jurist'),
('Finante ONG actuale','Documentati fondurile suficiente declarate si absenta altor proiecte PEO; elaborati fluxul lunar.','Extrase actuale, balanta, buget cash-flow, explicatia capitalurilor negative2025; capacitatea calculata nu certifica toate conditiile financiare.','Economist'),
('Bilanturi complete2016–2025','Obtineti situatiile semnate si recipisele de la contabil/ONG, mai ales2016–2018.','API ANAF furnizeaza indicatori2019–2025; raspunsurile goale2016–2018 nu dovedesc nedepunerea.','ONG + contabil'),
('Lipsuri documentare si actualizari legislative','Inchideti referintele marcate lipsa/esec in registre, verificati forma in vigoare la depunere si actele scanate.','Biblioteca si extragerile nu inseamna ca toate referintele au fost recuperate sau citite integral. Pastrati versiunea, emitentul si sursa.','Jurist + documentarist'),
('Clarificari AM','Clarificati regulile concursurilor si referintele necorelate; validati orice interpretare neacoperita.','Intrebarile sunt redactate in raportul specialistului. Nu au fost transmise extern.','Manager'),
('Implementare si dubla finantare','Confirmati orarul, competentele, protectia minorilor/GDPR, sustenabilitatea si evitarea suprapunerii cu PNRR/masa/transport/formare.','Proceduri, inventare si declaratii distincte, proiecte relevante selectate pentru punctaj.','Educatie + jurist'),
]
open_text='LISTA DESCHISA SI PROPUNERI — 07.10.2026\nPerimetru: proiectare ideala pe ipotezele acceptate. Dovezile viitoare raman deschise.\n\n'
for i,(topic,proposal,proof,owner) in enumerate(items,1):
    open_text+=f'{i}. {topic}\nPropunere: {proposal}\nProba / limita: {proof}\nResponsabil: {owner}\nStatus: DESCHIS — de inchis inaintea validarii finale/depunerii, dupa caz.\n\n'
(analysis/'Lista_deschisa_si_propuneri.txt').write_text(open_text,encoding='utf-8')
def link(path,label=None):
    p=Path(path)
    return '<a href="'+quote(p.as_posix(),safe='/')+'">'+html.escape(label or p.name)+'</a>'
sections=[]
for name in ['Raport_agent_auditor_independent.txt','Rubrica_audit_10_dimensiuni.txt','Fisa_selectie_scoli_ideale.txt','Fisa_conditii_minime_ROSE.txt','Lista_deschisa_si_propuneri.txt','SWOT.txt','Evaluare_actualizata_cost_eficienta.txt','Raport_agent_evaluator_matrice_completa.txt','Matrice_audit_cerinte_dovezi.txt','Raport_specialist_educatie.txt','Raport_specialist_scriere_si_intrebari.txt','Raport_agent_jurist.txt','Raport_agent_manager_proiect.txt']:
    p=analysis/name
    if p.exists():sections.append('<details><summary>'+html.escape(name.replace('_',' '))+'</summary><p>'+link(p.relative_to(root),'Deschide fisierul sursa')+'</p><pre>'+html.escape(p.read_text(encoding='utf-8-sig'))+'</pre></details>')
rows=''.join('<tr>'+''.join('<td>'+html.escape(t)+'</td>' for t in item)+'</tr>' for item in items)
budgets=''.join('<li>'+link(x['file'])+'</li>' for x in manifest)
sections.append('<section><h3>Dosarul financiar ANAF</h3><p>'+link('10.1 ROSE/Raport_economist_ROSE_eligibilitate_financiara_preliminara.txt','Raport economist — capacitate și condiții financiare')+'</p><p>'+link('10.1 ROSE/Sinteza_indicatori_ANAF_2016_2025.csv','Sinteza indicatorilor ANAF 2016–2025')+'</p><p>'+link('10.1 ROSE/Registru_descarcari_ANAF_2016_2025.csv','Registrul răspunsurilor ANAF și al limitelor datelor')+'</p></section>')
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Școli pentru viitor — dosar de proiectare</title><style>body{font:16px/1.6 system-ui;background:#f1f5f8;color:#19364f;margin:0}main{max-width:1120px;margin:auto;padding:40px}h1{font-size:38px;line-height:1.15}h2{margin-top:36px}a{color:#1259a4}section,details{background:white;padding:22px;border-radius:12px;margin:15px 0}summary{cursor:pointer;font-weight:700}pre{white-space:pre-wrap;font:14px/1.6 system-ui;color:#263849}table{border-collapse:collapse;width:100%;background:white}td,th{padding:12px;border:1px solid #dbe2e8;text-align:left;vertical-align:top}th{background:#19364f;color:white}.note{border-left:5px solid #db9c23;padding:16px;background:#fff8e7}.tag{color:#176343;font-weight:700}@media print{details{display:block}main{padding:0}summary{break-after:avoid}}</style><main>
<p class="tag">DOSAR DE PROIECTARE • 07.10.2026 • ROMANIAN SOUL ENTITY / ROSE</p><h1>Școli pentru viitor</h1>
<section><p>Proiectul pornește de la condițiile ideale: școlile și probele de experiență vor fi selectate după fișele de mai jos. Fondurile suficiente și lipsa altor proiecte PEO aprobate sunt declarații ale utilizatorului, folosite ca ipoteze de lucru.</p>
<p class="note"><strong>10/10 privește calitatea proiectării în perimetrul cunoscut și ipotezele declarate.</strong> Verdictul independent și limitele sale sunt în raportul auditorului de mai jos. Punctajul oficial nu este acordat: ținta condiționată este100/100 cu criteriul ITI îndeplinit sau99/100 în afara lui. Necunoscutele rămân deschise, cu propuneri.</p>
<p><strong>ONG-ul poate participa ca partener, nu ca lider eligibil.</strong> Sunt necesare un lider eligibil și experiență relevantă, dovedită conform ghidului și clarificărilor. Activitatea de îngrijire a vârstnicilor nu demonstrează singură experiența educațională.</p></section>
<h2>Bugete și contribuție</h2><ul>'''+budgets+'''</ul>
<table><tr><th>Indicator</th><th>Minim</th><th>Maxim</th></tr><tr><td>Total eligibil</td><td>700.000 EUR /3.680.880 lei</td><td>1.000.000 EUR /5.258.400 lei</td></tr><tr><td>Buget ONG partener</td><td>178.638,93 lei</td><td>243.406,13 lei</td></tr><tr><td>Elevi / luni</td><td>480 /24</td><td>720 /30</td></tr><tr><td>Contribuție lider la ipoteza2%</td><td>70.044,82 lei</td><td>100.299,88 lei</td></tr><tr><td>Contribuție ONG</td><td>0%</td><td>0%</td></tr></table>
<p>Fiecare fișier are două scenarii de contribuție și opt foi de lucru. Cotele coincid: grila nu acordă puncte suplimentare pentru o contribuție mai mare. Cota liderului depinde de categoria juridică;2% este ipoteza categoriei modelate. Toate activitățile A1–A5 sunt incluse, inclusiv alfabetizare și STEAM.</p>
<p>Prețurile bunurilor și serviciilor sunt plafoane de planificare rezultate din alocarea bugetului, nu oferte validate. Fișele de achiziții și câmpurile editabile permit înlocuirea lor cu prețuri documentate. Personalul este propus cu timp parțial;15/19 persoane dacă rolurile sunt distincte. Necesarul final rezultă din orarul școlilor și competențele personalului.</p>
<h2>Capacitate financiară și documente</h2><p>Veniturile2022–2025 însumează2.013.707 lei și acoperă numeric finanțarea ONG din ambele modele. Aceasta nu certifică întreaga eligibilitate financiară. Capitalurile proprii2025 sunt negative; fondurile actuale declarate se documentează separat. Dosarul10.1 ROSE conține răspunsurile ANAF pentru2016–2025: indicatori disponibili2019–2025 și răspunsuri goale2016–2018. Nu sunt situațiile financiare complete, semnate.</p>
<p>Biblioteca reunește documentele apelului, clarificări, condiții generale, legislație și surse programatice. Registrele păstrează eșecurile și referințele nerecuperate; extragerea documentelor nu echivalează cu lectura integrală a fiecărei pagini. Grilele generale sunt arhivate; încadrarea salarială individuală se validează după alegerea instituțiilor.</p>
<h2>Lista deschisă și propuneri</h2><table><tr><th>Aspect</th><th>Propunere</th><th>Probe / limite</th><th>Responsabil</th></tr>'''+rows+'''</table><h2>Rapoarte și fișe detaliate</h2>'''+''.join(sections)+'''<section><p>Echipa de agenți: manager de proiect, specialist scriere, economist, jurist, specialist educație, evaluator, auditor independent și documentarist. Rapoartele de specialitate păstrează sursele și condițiile specifice. Manifestul SHA256 identifică exact cele două bugete livrate.</p></section></main></html>'''
(root/'00 RAPORT CENTRAL - SCOLI PENTRU VIITOR.html').write_text(page,encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
