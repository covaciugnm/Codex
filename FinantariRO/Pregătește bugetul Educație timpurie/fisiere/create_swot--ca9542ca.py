from pathlib import Path
from html import escape
import csv,json
out=Path('7.4 SWOT si plan de optimizare');out.mkdir(exist_ok=True)
rows=[
('S1','Punct forte','Lider UAT și ONG cu roluri complementare','Liderul Sebeș este confirmat de utilizator; separarea funcțiilor este proiectată. Selecția formală nu este încă probată.','Ambele','Valorificare: UAT operează componenta publică, ONG intervenția familială în limita experienței dovedite.','1.2;3.4','4.1 Concept'),
('S2','Punct forte','Fonduri proprii disponibile','Declarație explicită a utilizatorului. Nu presupune CAF pozitiv ori hotărâri bugetare adoptate.','Ambele','Transformarea disponibilității în angajamente și deviz anual de sustenabilitate.','4.2','Instrucțiunea utilizatorului;10.1 ROSE'),
('S3','Punct forte','Toate familiile de activități au alocare','Matrice A1.1–A1.5,A2.1–A2.4,A3.1–A3.6; costurile exemplelor alternative se activează după nevoie.','Ambele','Păstrarea acoperirii relevante, eliminarea oricăror cantități fără justificare locală.','2.1;3.2','4.1;5.1;5.2'),
('S4','Punct forte','Modelul financiar se reconciliază','Audit independent al celor 4 XLSX:172 formule/fișier, zero erori de calcul memorate.','Ambele','Înghețarea versiunii auditate; la modificări, regenerare și control independent.','3.2','6.1 Audit'),
('S5','Punct forte','Contribuție ONG minimă compatibilă cu punctajul','Grila nu acordă bonus contribuției voluntare; 0% ONG este minimul folosit.','Ambele','Fondurile suplimentare se orientează spre continuitate sau nevoi reale, fără simularea unui bonus.','Grila integrală','6.2;GSCG'),
('S6','Punct forte','Separarea baremelor de costurile reale','Modelul nu adaugă salariile și hrana standard deja acoperite de ED01/ED02.','Ambele','Registru unic copil-lună-cost-sursă înainte de prima decontare.','3.1;3.2','5.1;5.2;GSCS5.3'),
('W1','Punct slab','Experiența relevantă ONG nu este încă documentată','EcoWarriors și existența contractului/raportului final sunt confirmate de beneficiar. Datele exacte și documentele necesită verificare; lista este în8.1.','Ambele','Verificarea dosarului EcoWarriors pentru alternativa resurse educaționale/metode inovatoare; se păstrează statutul declarat până la analizarea actelor.','Eligibilitate;3.6;3.7','2.1;10.1'),
('W2','Punct slab','Volumul și rețeaua sunt ipoteze','65/1650copii și unitățile nu sunt susținute de o listă operațională validată.','Critic extins','Bază agregată pe unități și cohorte; dimensionarea bugetului după capacitate demonstrată.','1.3;2.4;3.2','4.1;6.1'),
('W3','Punct slab','Spațiile și operatorii nu sunt nominalizați','1/5servicii complementare noi sunt scenarii, nu autorizări existente.','Ambele','Matrice spațiu-operator-capacitate-avize-calendar-inventar.','2.1;3.5;4.1','6.1'),
('W4','Punct slab','CES și normarea completă nu sunt reconciliate','224copii pentru sprijin itinerant în extins; suprapunerea cu logopedie și grupe trebuie stabilită. Reducerile efectivelor se verifică pe legea curentă.','Critic extins','Unicitate copii CES, repartiție pe grupe/vârste, norme legale, personal și înlocuiri.','1.6;3.4','5.2;7.1;7.2;7.3'),
('W5','Punct slab','Prețurile reale sunt estimări','Nu există două oferte comparabile pe fiecare cost fără barem.','Ambele','Specificare funcțională după inventar și minimum două justificări de piață comparabile.','3.1;3.2','Buget!Fundamentare'),
('W6','Punct slab','Sustenabilitatea nu are deviz aprobat','Disponibilitatea fondurilor este confirmată de utilizator, dar lipsesc volumele anuale și angajamentele entităților.','Ambele','Calcul cost anual integral și buget pentru minimum3ani; finanțarea lunilor neacoperite de grant.','4.2','4.1;6.1'),
('W7','Punct slab','Marjă redusă peste pragul minim','Pilotul este cu1.703,40lei peste minim; tăierea unor costuri poate coborî proiectul sub prag.','Pilot','La fiecare ajustare, revalidarea plafonului minim și celui pe copil; nu se introduc cheltuieli artificiale.','Eligibilitate financiară','5.1'),
('W8','Punct slab','Arhiva are limite de actualitate și exhaustivitate','Unele copii legislative sunt forme de bază, iar anumite documente europene/atașamente nu sunt recuperate integral.','Ambele','Registru de versiuni cu dată de aplicabilitate și verificarea amendamentelor relevante.','Conformitate transversală','2.1;3.1'),
('O1','Oportunitate','Infrastructură publică deja existentă','Posibilitate de utilizare verificabilă numai după inventar și aprobări.','Ambele','Reutilizare dotări și spații adecvate pentru reducerea costului incremental.','3.2;3.5','De confirmat prin UAT'),
('O2','Oportunitate','Integrarea educație-social-sănătate','A3.6 permite cooperare pe caz și reducerea barierelor de participare.','Ambele','Protocol cu responsabili, circuitul cazurilor și termene de răspuns.','2.4;2.5;4.1','GSCS A3.6'),
('O3','Oportunitate','Metodă alternativă de capacitate financiară','ONG are vechime; utilizarea regulii40%AFN rămâne condiționată de portofoliu și celelalte cerințe.','Ambele','Verificare proiecte contractate și alegerea metodei aplicabile în acord.','Eligibilitate','GSCG;10.1'),
('O4','Oportunitate','Extindere justificată a parteneriatului','Posibilitate de analizat dacă Sebeș nu susține volumul maxim; nu este o decizie deja aprobată.','Extins','Evaluarea altor membri numai după răspunsul utilizatorului și verificarea regulilor apelului.','1.3;2.4','Clarificare în așteptare'),
('O5','Oportunitate','Transferul metodologiei către operatori','Strategia, formarea și studiul de impact pot susține continuitatea în instituțiile implicate.','Ambele','Proceduri și instrumente reutilizabile, cu aprobări, instruire și responsabil permanent.','4.1','GSCS A1'),
('T1','Amenințare','Respingere la etapa preliminară','O condiție obligatorie neîndeplinită nu poate fi compensată cu buget mare ori scor teoretic bun.','Ambele','Verificare eliminatorie înainte de optimizarea punctajului; veto la experiență/parteneriat/capacitate.','Anexa2','6.2'),
('T2','Amenințare','Dublă finanțare','Servicii standard, PNRR și finanțări locale pot acoperi aceeași prestație ori același activ.','Ambele','Reconcilierea surselor și a beneficiului suplimentar pe fiecare cost și perioadă.','Eligibilitate;2.4','6.1'),
('T3','Amenințare','Ținte demografice sau de retenție nerealiste','Țintele romi35/850 și rezultate58/1452 sunt ipoteze. Extinsul are marjă de49rezultate peste minimul matematic pentru punctajul superior.','Ambele','Date reale, desegregare, plan de acces/frecvență și intervenții timpurii; fără atribuirea etniei prin presupunere.','1.5;2.6','6.2'),
('T4','Amenințare','Întârzierea aprobărilor și autorizărilor','Proiect24luni, final absolut31.12.2029; calendarul exact nu este stabilit.','Ambele','Drum critic al aprobărilor; servicii deschise numai după îndeplinirea condițiilor.','2.1;2.2','GSCS;4.1'),
('T5','Amenințare','Costuri reale de personal peste estimări','Salariile publice, calificarea, concediile și înlocuirile pot schimba necesarul.','Ambele','Normare integrală și simulare cost total angajator în regimul juridic corect.','3.4','7.2;7.3'),
('T6','Amenințare','Interpretări greșite ale versiunii legislative','Forma de bază nu certifică regula în vigoare la implementare.','Ambele','Comparare text consolidat, acte modificatoare și data intrării în vigoare; clarificare AM când normele se intersectează.','Conformitate transversală','2.1;7.2'),
('T7','Amenințare','Neasigurarea protecției copiilor și datelor','Date sociale, etnie, sănătate/CES și evidențe individuale necesită temei și acces limitat.','Ambele','Proceduri de protecție a copilului și date, minimizare, personal competent și circuit de sesizare.','1.6;2.7;legal','7.2'),
]
headers=['ID','Categorie','Aspect','Dovada_sau_limita','Scenariu','Actiune','Criterii','Sursa_in_dosar']
with (out/'SWOT.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(headers);w.writerows(rows)
intro='''ANALIZĂ SWOT ȘI PLAN DE OPTIMIZARE – RUNDA 2
07.10.2026 | Sebeș – ROMANIAN SOUL ENTITY
Analiza compară scenariul pilot cu65copii și cel extins cu1650copii. Afirmațiile sunt clasificate ca dovezi disponibile, declarații ale utilizatorului sau ipoteze de verificat. Nu atribuie beneficii confirmate unor resurse încă neidentificate.
Concluzie: disponibilitatea banilor nu este blocajul de proiectare. Experiența eligibilă, capacitatea educațională, evitarea dublei finanțări și sustenabilitatea documentată determină dimensiunea și punctajul maxim posibil.
'''
actions='''
STRATEGII REZULTATE DIN SWOT
SO: folosește capacitatea administrativă a liderului și fondurile disponibile pentru servicii necesare, cu cooperare socială și continuitate formalizată.
WO: completează inventarul, analiza de nevoi și dovezile de experiență înainte de alegerea dimensiunii; reutilizează infrastructura și extinde parteneriatul numai dacă necesitatea și eligibilitatea sunt dovedite.
ST: menține registrul copil-lună-cost-sursă, controlul versiunilor legislative și separarea funcțiilor; rezervă timp suficient pentru autorizări și intervenții împotriva abandonului.
WT: blochează validarea finală dacă există o condiție eliminatorie nerezolvată; ajustează numărul de copii, servicii și costuri după probe, fără a inventa beneficiari sau cheltuieli pentru plafon.

ORDINEA DE OPTIMIZARE
1. Eligibilitate și experiență ONG/parteneriat: condiții obligatorii înaintea punctajului.
2. Rețea reală: copii unici, CES, unități, grupe, operatori și capacitate pe perioade.
3. Legalitate operațională: autorizări, personal, protecția copilului, date și achiziții.
4. Buget justificat: cantități, prețuri, salarii, TVA, surse și lipsa dublei finanțări.
5. Punctaj: probe pentru fiecare subcriteriu, limite istorice documentate și maximum posibil fără promisiuni fictive.
6. Audit nou după fiecare modificare relevantă: dovada închiderii fiecărei constatări; hashuri noi pentru bugete modificate.

REGULA AVIZULUI FINAL
10/10 în audit este distinct de100/100 în grila apelului. Un plafon de punctaj mai mic poate fi maximul posibil numai dacă limitele sunt documentate și toate condițiile obligatorii sunt îndeplinite. Fără experiență dovedită, operatori, capacitate, oferte și angajamente, 10/10 nu poate fi acordat onest. Repetarea calculelor nu înlocuiește dovezile lipsă.
'''
body=intro+'\n\n'+'\n\n'.join(' | '.join(r) for r in rows)+actions
(out/'SWOT_si_plan_de_optimizare.txt').write_text(body,encoding='utf-8')
tables=''
for category in ['Punct forte','Punct slab','Oportunitate','Amenințare']:
 tables+='<h2>'+category+'</h2><table><tr><th>Aspect și dovadă</th><th>Efect / acțiune</th></tr>'
 for r in rows:
  if r[1]!=category:continue
  tables+='<tr><td><b>'+escape(r[0]+' '+r[2])+'</b><p>'+escape(r[3])+'</p></td><td>'+escape(r[5])+'<p><small>'+escape('Scenariu: '+r[4]+' · Criterii: '+r[6]+' · Sursă: '+r[7])+'</small></p></td></tr>'
 tables+='</table>'
html='<!doctype html><html lang="ro"><meta charset="utf-8"><title>SWOT și optimizare</title><style>body{font:16px/1.5 Segoe UI,Arial;max-width:1120px;margin:36px auto;color:#17364a}table{border-collapse:collapse;width:100%}td,th{border:1px solid #cbd9e2;padding:14px;vertical-align:top;width:50%}th{background:#17364a;color:white}h2{margin-top:38px}pre{white-space:pre-wrap;font:inherit}small{color:#526d7d}</style><h1>SWOT · Educație timpurie Sebeș / ROSE</h1><pre>'+escape(intro)+'</pre>'+tables+'<pre>'+escape(actions)+'</pre></html>'
(out/'SWOT_si_plan_de_optimizare.html').write_text(html,encoding='utf-8')
print('SWOT: '+str(len(rows))+' constatari, TXT/HTML/CSV.')
