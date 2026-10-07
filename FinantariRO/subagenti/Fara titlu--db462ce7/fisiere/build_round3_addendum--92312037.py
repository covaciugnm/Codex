from pathlib import Path
import csv,json,html,hashlib,collections
r=Path(__file__).resolve().parent;o=r/'7.1 Audit iterativ';e=r/'7.6 Reevaluare punctaj'
grid=list(csv.DictReader((e/'Runda2.csv').open(encoding='utf-8-sig'),delimiter=';'))
changes={
'1.1':(1,'7.8/02: legea198, strategiile și relația obiective–activități–rezultate sunt explicite; documentele UE suplimentare au identitate validată.','Transpunere înCF; completarea exactă a formei strategiei locale/aprobării și actualizarea versiunilor la depunere.'),
'1.6c':(1,'7.8/03: măsuri ecologice pe bunuri/servicii, cerințe verificabile, recepție și costurile liniilor existente identificate.','Piață, specificații finale, ponderea atelierelor de mediu; creditul privește proiectarea financiară, nu cumpărări deja făcute.'),
'1.7b':(1,'7.8/02 mapează100% operațiunea la provocările Semestrului. Auditorul a verificat independent ConsiliuST10400/26ADD1, România pp16–17.','Documentul este opinieEMCO/SPC, nu recomandare finală. Grila cere provocările identificate în Semestru; nu adăugăm obligația exclusivă a recomandării finale. Transpunere înCF/MySMIS.'),
'3.2d':(1,'7.8/03: criterii pe ciclul de viață, durabilitate/reparabilitate/consum, dovezi echivalente și metodă comparabilă36luni.','Justificarea pieței și cerințe proporționale înaintea achiziției; nu inventăm o economie de emisii ori preț.'),
'3.3':(2,'7.8/01:13profiluri acoperă16linii de personal; atribuții, studii, experiență minimă propusă, livrabile și limite. Auditor:ore/tarife reconciliate fără diferențe.','Nominalizările și calificările reale se verifică separat;3.4b rămâne0din lipsa normării integrale. Managementul este intern.'),
'4.2':(0,'7.8OPEX:șablon503formule și metodologie pentru36luni plusdecalaj; costurile integrale și sursele necompletate suntn.a.','Fondurile sunt confirmate; sunt necesare alocarea, devizul integral și acte peoperator/perioadă. Nu acordăm2puncte pentru un șablon.')}
for x in grid:
 if x['Cod']in changes:
  score,why,left=changes[x['Cod']]
  for k in ['Pilot_inferior','Pilot_superior','Extins_inferior','Extins_superior']:x[k]=str(score)
  x['Dovada_si_apreciere']=why;x['Conditie_ramasa']=left
totals={k:sum(int(x[k])for x in grid)for k in ['Pilot_inferior','Pilot_superior','Extins_inferior','Extins_superior']}
categories={c:{k:sum(int(x[k])for x in grid if x['Categorie']==c)for k in totals}for c in dict.fromkeys(x['Categorie']for x in grid)}
with(e/'Runda3.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(grid[0]),delimiter=';');w.writeheader();w.writerows(grid)
gtext='''REEVALUARE INDEPENDENTĂ — RUNDA 3
07.10.2026 | Lectură internă a conținutului disponibil; nu punctaj oficial și nu nota auditului din10.

Interval actual:36–67/100 pilot;36–53/100 extins. Runda2era30–65, respectiv30–51. Cele46elemente sunt păstrate înCSV; au fost reevaluate independent numai criteriile afectate de7.8. Limita inferioară crește cu6, cea superioară cu2. Creditul recunoaște conținutul efectiv redactat, sub condiția adaptării și anexării în cererea finală. Nu cere efectuarea anticipată a achizițiilor pentru a recunoaște un plan de achiziții, dar nici nu presupune existența resurselor/datelelor lipsă.

Modificări:1.1=1/1,1.6c=1/1,1.7b=1/1,3.2d=1/1,3.3=2/2.4.2rămâne0/2. Restul aprecierilor Rundei2nu se modifică fără probe noi. Documentele de experiență nu au fost încă examinate, deși existența lor și implementareaEcoWarriors sunt confirmate de utilizator.

'''
gtext+='\n'.join(f"{c}: pilot {v['Pilot_inferior']}–{v['Pilot_superior']}; extins {v['Extins_inferior']}–{v['Extins_superior']}"for c,v in categories.items())
gtext+='''

Cele8puncte pentru țintele numerice1.5/2.6 rămân separate până la validarea populației și fezabilității. Dacă se validează fără altă schimbare:44–75pilot,44–61extins. Încă0–4puncte istorice3.6/3.7 depind de actele examinate; adăugarea tuturor celor12ar produce48–79pilot și48–65extins. Acestea sunt scenarii aritmetice, nu punctaje câștigate. Chiar în acel scenariu favorabil, eficiența ar fi maximum20/30pilot și12/30extins, sub pragul21. Sunt necesare inventare, prețuri, normare și resurse reale.
Praguri:21/30relevanță,21/30eficacitate,21/30eficiență,7/10sustenabilitate și70/100total; orice condiție preliminară neîndeplinită rămâne eliminatorie. Maximul teoretic100nu este plafon real demonstrat. Un plafon97poate fi optim dacă istoria probată justifică lipsa3puncte, dar nu este încă o concluzie despre acest solicitant.

Motivarea temei10: Anexa3cere abordarea provocărilor identificate în Semestrul European. Documentul primar Consiliu din19.06.2026 constată pentru România participarea insuficientă la educația timpurie și accesul inegal;7.8leagă A1/A2/A3 și costurile de sprijin exclusiv de această intervenție. Este opinieEMCO/SPC, nu se atribuie fraudulos statutul de recomandare finală. Recomandarea finală poate întări dosarul, dar nu introducem un filtru mai restrictiv decât textul grilei.
Sursa verificată independent: https://data.consilium.europa.eu/doc/document/ST-10400-2026-ADD-1/en/pdf , pp16–17, secțiunea România. Nu se pretinde arhivareaPDFîn urma lecturii web.

DETALIEREA CRITERIILOR MODIFICATE
'''
gtext+='\n\n'.join(f'{k}: {s} punct(e). {why}\nRămâne: {left}'for k,(s,why,left)in changes.items())
(e/'Runda3.txt').write_text(gtext,encoding='utf-8')
style='<style>body{font:16px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 20px;color:#142b34}table{border-collapse:collapse;font-size:13px}td,th{border:1px solid #aac;padding:8px;vertical-align:top}p{margin:1.2em 0}</style>'
render=lambda t:'<!doctype html><html lang="ro"><meta charset="utf-8">'+style+''.join('<p>'+html.escape(p).replace('\n','<br>')+'</p>'for p in t.split('\n\n'))+'</html>'
(e/'Runda3.html').write_text(render(gtext)[:-7]+'<table><tr>'+''.join('<th>'+k+'</th>'for k in grid[0])+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(v)+'</td>'for v in x.values())+'</tr>'for x in grid)+'</table></html>',encoding='utf-8')
delta=[
('A01','PARȚIAL REMEDIAT','Cele5surseUE restante sunt recuperate:35/35în lista inventariată; plus3COM.','Nu înseamnă toate trimiterile/anexele și modificările din întregul corpus.'),
('A02','PARȚIAL REMEDIAT','Contract2041consolidat17.04.2025 este separat și verificat; registreleUE precizează formele inițiale și lectura punctuală.','Consolidările actuale ale unor acteUE și verificarea completă a trimiterilor rămân sarcină echipă.'),
('A19','FIȘE REDACTATE','13profiluri complete; criteriul3.3primește2puncte interne.','Nominalizări,CV/diplome/autorizații și angajatorul real sunt de primit/verificat.'),
('A20','REPER SALARIAL ADĂUGAT','ListaSebeș31.03.2026 recuperată; auditorul a citit nota coordonatorului, fără a pretinde propria lectură vizualăPDF.','Nu înlocuiește statele actuale sau grila operatorilorPJ/ONG; tarifele nu sunt drepturi salariale aprobate.'),
('A17/A29','SENSIBILITATE CLARIFICATĂ','F06MAX:1840ore inițiale nu încap la o persoană înM1–M8; propunerea mută720ore în actualizări ulterioare, cu livrabile explicite.','Validarea sfereiA1.1/A1.2și a jaloanelor înaintea deschiderii; dacă nu permite actualizări, calendarul/resursele se refac fără pontaje fictive.'),
('A31','TEMĂ10DETALIATĂ','Corelarea cu Semestrul verificată direct,100%argumentat;1.7bprimește1punctintern.','AdaptareCF/MySMIS și versiuni strategice; păstrează separat cheiletemei05.'),
('A42','CRITERII ECOLOGICE REDACTATE','Specificații, alternative echivalente, ciclul de viață și costurile existente;1.6c/3.2dprimeștecâte1punct.','Piață, proporționalitate, prețuri, procedură și recepție încă de validat.'),
('A33','ȘABLON INTEGRAL, DATE INCOMPLETE','OPEX503formule, subtotal938880lei/36luni/serviciu, restn.a.; decalajulplatăfinală separat.','Devizreal integral/operator și surse/alocări/acte;4.2nu primește puncte acum.'),
('A44','NUCLEU DOCUMENTAR RECUPERAT ȘI MAPAT','Manualv5,Instr10/11/12,contractconsolidat și matrice20controale; lipsa acestor documente ca atare este remediată.','Transpunerea pe contractul semnat, diferența5/15zile recuperare și referința finalimplementare/platăfinală sunt de reconciliat.')]
with(o/'Runda3_Modificari_registru.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Constatare','Stare_Runda3','Dovada_noua','Ramas_deschis']);w.writerows(delta)
text='''ADDENDUM AUDIT — RUNDA 3
07.10.2026 | Municipiul Sebeș și ROMANIAN SOUL ENTITY

NOTA PREGĂTIRII ȘI CONFORMITĂȚII DOCUMENTARE A DOSARULUI PENTRU DEPUNERE:4,0/10. VETO DE VALIDARE FINALĂ:ACTIV.
Aceasta nu este nota calității calculelor, nu este punctajul grantului și nu diagnostichează entitățile ca neeligibile. Utilizatorul a confirmat implementareaEcoWarriors, produsele, existența actelor și fondurile necesare. Rămân examinarea documentelor și datele reale de proiectare. Lipsa examinării nu este dovada inexistenței sau neeligibilității.

Runda3analizează numai probele noi. Runda2și rubricile sale sunt păstrate. Descărcările, fișele și șabloanele sunt progres real; subtestele externe încă deschise nu sunt punctate artificial. A01nu mai are5surseUE lipsă din lista35; rămâne verificarea exhaustivității trimiterilor și consolidărilor. A44nu mai este lipsă de manual/contract; are acum20controale și două diferențe de aplicare explicite. Nota4,0rămâne pentru dosarul complet deoarece nu s-a închis un nou subtest integral din rubrica stabilită.

PUNCTAJUL INTERN ACTUALIZAT
Reevaluarea independentă după7.8 acordă credit real pentru redactare:3.3=2puncte;1.1,1.6c,1.7b,3.2d=câte1.4.2rămâne0din lipsa devizului și alocărilor complete. Intervalul actual este36–67pilot și36–53extins, fațăde30–65/30–51anterior. Nu este prognoză probabilistică sau punctaj oficial. CSVcomplet46elemente și justificările sunt în7.6/Runda3.csv/txt/html. Cele8puncte ale țintelor și0–4aleistoricului rămân separate; nici adăugarea tuturor nu închide pragurile de categorie.

VERIFICĂRI INDEPENDENTE NOI
Cele4bugete eligibile au exact hashurile Rundei2; nu au fost recalculate inutil și nu au fost modificate. Avizul numeric anterior se păstrează la aceleași fișiere.
OPEX_36_luni.xlsx:503formule, fără eroriExcelmemorate și fără neconcordanțe în controalele efectuate. Auditorul a verificat în regimfărămodificare produsele lunare, subtotalurile, însumările și menținerean.a.pentru costuri/surse/decalajnecunoscute.938880lei/36luni pentru1serviciu este numai subsetul celor5componente;5servicii dau4694400lei. OPEXintegral și necesarulcu decalaj rămânn.a. Testelelimită sunt reproduceri aritmetice independente și inspecțiaformulelor; nu sunt pretinse teste interactiveExcel executate de auditor. Autorul a raportat separat testele cu motorul de calcul.
13fișe,16linii de personal:orele și tarifele comparate independent cuXLSXMIN/MAX nu prezintă diferențe. Calificarea, numirea, salariullegal și capacitateareală rămân de validat. SensibilitateaF06MAXși propunerea condiționată de actualizări sunt consemnate, fără a transforma pontaje viitoare în dovezi.
8documenteUE/COM:hashurile și numărul de pagini din registrulvalidat corespund copiilor locale. Auditorul a citit registrul și nota juridică; lectura articolelor strategice este documentată de jurist, nu atribuită fals auditorului ca lectură integrală.35/35este lista inventariată, nu întreg universul documentelor aplicabile. Formele inițialeFSE+2021/financiar2024nu sunt declarate consolidări actuale. Carta este în volumul408pagini, cu lectura juridică limitată la pasajele declarate.

A44—REZULTATE MATERIALE
Contractul2041inițial270845este separat de consolidarea296187din17.04.2025; cea din urmă conține notelemodificării714/2025. Instr10aprobămanualv5șiînlocuiește9; Instr11precizează moduleleMySMISșiînlocuiește4/2024. Instr12privește universitățile și nu este temei salarial pentruSebeș/ONG.
Matricea1.2/Matrice_A44_contract_manual_GSCS.csv/txt/html tratează20controale:RPmax3luni, termen30ziledupăperioadă și10zilelucrătoare înainteCR;CRfinalămax90zile;CPutilizatămax5zilelucrătoare/CRCPmax10zilelucrătoare; reconciliere pânăla20; dosareachiziții înainteCR/CP; acteadiționale și notificări;FSE+modificăriînaceeașicategoriecuaprobare; personalpublic; recuperări; arhivare; continuitate; vizibilitate.
Două diferențe rămân de reconciliat peclauza aplicabilă:art12(5)general spune5zile pentruCPnejustificate/neeligibile, în timp ceAnexa4specifică descrie15zileînainteadeciziei; nu se promite universal15zile. Pentru continuitate,GSCS/manualraportează începutul lafinalimplementare, contractulFSE+art2(6)la platafinală; șablonulOPEXinclude intervalulintermediar și36lunifărăgol, subrezerva clauzeisemnate. Arhivarea este separatminimum5ani dela31decembrie anulultimeiplăți și poate dura mai mult.
Au fost citite integral textele de aprobareInstr10șiInstr11/12, secțiunile relevante dinmanual/contract/GSCS; nu pretindem lectura integrală a209pagini cu toateanexele. Documentarea acestei matrice nu confirmă executarea obligațiilor beneficiarului.

CE POATE CONTINUA ECHIPA ȘI CE TREBUIE PRIMIT
Echipa:certificarea formelor aplicabile, trierea trimiterilor rămase, integrarea tuturor textelor înCF, verificarea strategicălocală și actualizarea calendarului pe jaloane reale. Cererile de interpretareAMrămân proiecte, nu mesaje trimise extern.
Beneficiar/UAT/operatori:documentele8.1pentruEcoWarriors/lider, selecțiapartenerului/acorduri, portofoliu/CAF, dateGT/SIIIR/cohorte/CES, operatori/grupe/spații/autorizări, inventarePNRR și nevoi suplimentare, oferte/TVA, CV/încadrări/salarii, devizul integral și acte de alocare. Se cere depunerea/verificarea actelor existente, nu reconfirmarea existenței experienței sau fondurilor.
Nici această rundă nu autorizează depunerea și nu acordă10/10condiționat. După probele noi se închid punctual constatările; nu se repetă auditul identic pentru a fabrica nota finală.
'''
# Improve numeric word boundaries without altering decimal commas or reference IDs.
import re
def clean(t):
 t=re.sub(r'(?<=[a-zăâîșț])(?=\d)',' ',t);t=re.sub(r'(?<=\d)(?=[A-Za-zăâîșț])',' ',t);t=re.sub(r'(?<=[:;])(?=[A-Za-zăâîșț0-9])',' ',t)
 return t
text=clean(text);gtext=clean(gtext)
(o/'Runda3_Addendum.txt').write_text(text,encoding='utf-8');(o/'Runda3_Addendum.html').write_text(render(text),encoding='utf-8')
(e/'Runda3.txt').write_text(gtext,encoding='utf-8')
manifest=[]
for folder,pattern in [(o,'Runda3*'),(e,'Runda3*')]:
 for p in folder.glob(pattern):
  if p.is_file()and p.name!='Runda3_Manifest.json':manifest.append({'file':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(o/'Runda3_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'elements':len(grid),'totals':totals,'categories':categories,'audit_score':4},ensure_ascii=True))
