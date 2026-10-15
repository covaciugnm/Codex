import json,pathlib,hashlib,sys
from decimal import Decimal,ROUND_HALF_UP
sys.stdout.reconfigure(encoding='utf-8')
W=pathlib.Path(__file__).parent
O=W.parent/'2026.10.13 Baza comuna negociere BERGER PECH'
matrix=O/'2026.10.13 Cerinte comune negociere matrice.json'
assert hashlib.sha256(matrix.read_bytes()).hexdigest()=='73b45b4c8a18908f6f30bcea9400a4506de02de3719ede324750ca6afe76aa0f'
legal=json.loads((O/'2026.10.13 Obiectii negociere reformulate.json').read_text(encoding='utf-8'))
points=next(x['repere_facturare_comune']for x in legal['puncte_negociere']if x['id']=='P09')
D=Decimal
def amount(x):return D(str(x)).quantize(D('.01'),rounding=ROUND_HALF_UP)
def disp(x):return f'{amount(x):,.2f}'.replace(',','_').replace('.',',').replace('_','.')
def bundle(net):
    net=amount(net);vat=amount(net*D('.20'));gross=net+vat;ret=amount(net*D('.05'))
    return {'net_eur':str(net),'tva_20_eur':str(vat),'brut_eur':str(gross),'retentie_5_net_eur':str(ret),'net_dupa_retentie_eur':str(net-ret),'plata_bruta_dupa_retentie_eur':str(gross-ret),'afisare':{'net':disp(net),'tva_20':disp(vat),'brut':disp(gross),'retentie_5_net':disp(ret),'plata_bruta_dupa_retentie':disp(gross-ret)}}
base={'BERGER':D('45000'),'PECH':D('69300')};pc=[10,20,25,15,10,10,10]
rows=[]
for k,(point,pct)in enumerate(zip(points,pc),1):
    rows.append({'id':f'E{k}','reper':point['id'],'procent_pachet':pct,'livrabil_comun':point['livrabil_comun'],'termen_trigger':point['termen_propusa'],'berger':bundle(base['BERGER']*D(pct)/100),'pech':bundle(base['PECH']*D(pct)/100)})

bcols=['Calcul / Ausführungsstatik','Planuri constructive și de execuție','Asistență statică','Prüfingenieur']
pcols=['01 Ausführungsstatik','02 Durchbruchsplanung Bestand','03 Baugrubensicherung','04 Untergrundbeschau','05 Baubegleitung / 12 Abnahmen','06 Schlussunterlagen']
ba=[['1500','3000','0','0'],['2500','6000','0','500'],['4500','5750','0','1000'],['3000','2250','0','1500'],['1500','3000','0','0'],['0','0','2000','2500'],['0','0','0','4500']]
pa=[['6930','0','0','0','0','0'],['8453.33','0','5000','0','406.67','0'],['10511.67','6000','0','0','813.33','0'],['9175','0','0','0','1220','0'],['6930','0','0','0','0','0'],['0','0','0','800','6130','0'],['0','0','0','0','5430','1500']]
alloc={}
for v,cols,grid,totals in [('BERGER',bcols,ba,['13000','20000','2000','10000']),('PECH',pcols,pa,['42000','6000','5000','800','14000','1500'])]:
    table=[]
    for k,line in enumerate(grid,1):
        values=list(map(D,line));assert sum(values)==D(rows[k-1][v.lower()]['net_eur'])
        table.append({'reper':f'E{k}','valori_net_eur':[str(amount(x))for x in values],'valori_net_afisate':[disp(x)for x in values],'total_net_eur':str(amount(sum(values)))})
    for c,expected in enumerate(totals):assert sum(D(r[c])for r in grid)==D(expected)
    alloc[v.lower()]={'coloane_originale':cols,'totaluri_originale_net_eur':[str(amount(x))for x in totals],'randuri':table,'statut':'Alocare AG pentru facturarea pachetului neschimbat. Coloanele păstrează toate valorile originale ca Kalkulationsgliederung; nu sunt oferte noi pentru servicii, tarife unitare sau limite ale scopului comun.'}

pi=[]
for k,(bv,pv)in enumerate(zip(['0','500','1000','1500','0'],['0','406.67','813.33','1220','0']),1):
    pi.append({'reper':f'E{k}','berger_parte_planificare_net_eur':str(amount(D(rows[k-1]['berger']['net_eur'])-D(bv))),'berger_parte_PI_net_eur':str(amount(bv)),'pech_parte_planificare_net_eur':str(amount(D(rows[k-1]['pech']['net_eur'])-D(pv))),'pech_parte_PI_net_eur':str(amount(pv))})

options=[]
for n in range(7):
    bn=amount(D(n)*D('2000')/12);pn=amount(D(n)*450)
    options.append({'numar_vizite_suplimentare':n,'berger':bundle(bn),'pech':bundle(pn),'total_cu_baza_berger':bundle(base['BERGER']+bn),'total_cu_baza_pech':bundle(base['PECH']+pn)})

checks={'procente':sum(pc),'berger':{},'pech':{}}
assert sum(pc)==100
for v in base:
    for field in ['net_eur','tva_20_eur','brut_eur','retentie_5_net_eur','plata_bruta_dupa_retentie_eur']:
        total=sum(D(r[v.lower()][field])for r in rows);expect=D(bundle(base[v])[field]);assert total==expect
        checks[v.lower()][field]=str(amount(total))
    checks[v.lower()]['D1_D5_net_eur']=str(amount(sum(D(r[v.lower()]['net_eur'])for r in rows[:5])))
assert sum(D(r['berger_parte_PI_net_eur'])for r in pi)==3000
assert sum(D(r['pech_parte_PI_net_eur'])for r in pi)==2440
assert sum(D(r['berger_parte_planificare_net_eur'])for r in pi)==33000
assert sum(D(r['pech_parte_planificare_net_eur'])for r in pi)==53000

obj={'data':'2026.10.13','titlu':'Propunere economică comună pentru negocierea R06 BERGER PECH','statut':'PROPUNERE AG de evaluat înainte de integrare. NETRIMISĂ / NESEMNATĂ; nu ofertă acceptată. Nu modifică R05 sau PDF-urile existente.','principii':['Aceleași 7 repere E1–E7 și aceeași repartizare procentuală 10/20/25/15/10/10/10 pentru ambii. Procentele sunt preluate din propunerea R05 BERGER și propuse acum ca regulă AG comună, nu atribuite ofertelor originale.','Totalurile de bază rămân 45.000 EUR net BERGER și 69.300 EUR net PECH; TVA oferită 20%. Retenția este 5% din net, fără micșorarea onorariului. În exemplul numeric TVA se calculează înainte de retenție; tratamentul efectiv al facturilor urmează legea aplicabilă.','Cele 4 poziții BERGER și 6 PECH rămân numai Kalkulationsgliederung cu valorile originale intacte. Nicio coloană nu restrânge proiectarea, PI, ZT/Fertigstellung sau BWB comun și nu exclude specialiștii profesioniști previzibili.','Ratele nu sunt scadențe calendaristice și nu dau avans pentru simpla numire, rezervare de resurse sau predare a propriului plan. Facturarea curentă privește rezultatul efectiv prestat; decontul legal justificat al împiedicării/încetării rămâne separat.'],
'repere_plati':rows,'totaluri':{'berger':bundle(base['BERGER']),'pech':bundle(base['PECH'])},'alocare_interna_propusa':alloc,
'control_80_procente':{'constatare':'E1–E5 însumează 80% la ambii. BERGER 36.000 EUR net depășește calculul+planurile originale 33.000 cu 3.000. PECH 55.440 depășește Pos. 01–03 de 53.000 cu 2.440. Această comparație de alocare economică nu stabilește singură valoarea legală a pachetului extins, dar arată de ce numai predarea planurilor nu justifică automat toate cele 80%.','berger':{'80_procente_net_eur':'36000.00','planificare_originala_net_eur':'33000.00','partea_PI_propusa_net_eur':'3000.00'},'pech':{'80_procente_net_eur':'55440.00','planificare_originala_net_eur':'53000.00','partea_PI_propusa_net_eur':'2440.00'},'evaluare':'Modelul este încărcat spre faza de planificare. Poate fi acceptat numai cu toate produsele de proiectare și control PI efectiv livrate și cu documentare verificabilă. Alocarea convențională nu dovedește, prin ea însăși, prestarea sau valoarea reală a unui control. AG trebuie să valideze alocarea cu fiecare ofertant înainte de semnare.','fara_avans_PI':{'repartizare_early_PI':pi,'provenienta':'BERGER folosește alocarea AG deja propusă în R05, nu o ofertă originală pe rapoarte. PECH 2.440 EUR este alocare AG nouă în Pos. 05 de 14.000, împărțită în raportul 1:2:3, cu rotunjire cumulativă; nu preț suplimentar și nu tarif primit.','regula':'E2/E3/E4 cer aceleași rapoarte profesionale PI pentru ambii. Partea PI se facturează numai după raportul efectiv al persoanei eligibile în funcția PI; simpla livrare a propriului calcul/plan ori controlul intern al proiectantului nu este dovada serviciului PI distinct. Când raportul PI lipsește, suma sa se amână; partea de planificare separabilă efectiv livrată rămâne facturabilă după regula comună.','rapoarte':[{'reper':'E2','livrabil':'Beschau-/Haltepunkteplan PI, luare la cunoștință a bazelor și evaluare profesională documentată.'},{'reper':'E3','livrabil':'Raport PI distinct asupra predimensionării, bazelor existentului și concordanței plan–statică pentru elementele etapei.'},{'reper':'E4','livrabil':'Verificare și freigabe PI documentate ale planurilor complete de lemn/oțel/îmbinări pentru etapa D4.'}],'limita':'Calificarea și independența se probează după funcție. Nu afirmăm o interdicție legală generică a cumulului proiectant–PI; contractul cere performanța de control distinctă și verificabilă, nu o substituire formală prin planul propriu.'}},
'E6_facturare_pe_prestatie':{'berger':'4.500 EUR net: 2.000 asistență + 2.500 PI, alocare internă a pachetului. Facturare proporțională pentru cele 12 vizite fizice și controale/befunde aferente efectiv realizate, nu integral după prima prezență.','pech':'6.930 EUR net: Pos. 04 teren 800 + Pos. 05 vizite/PI 6.130. Cei 800 se facturează o singură dată după Befund de teren complet; vizita comună intră o dată în cele 12 și nu produce o nouă taxă de drum. Restul se decontează proporțional după prestațiile fazei.','metoda_propusa':'Înainte de semnare se confirmă registrul celor 12 faze și alocarea proporțională. Dacă se folosește numărul fizic ca repartizare simplă: BERGER cumul k × 4.500/12; PECH componenta vizite cumul k × 6.130/12, plus 800 numai dacă Befund Pos. 04 este complet. Se folosește raportul exact, se rotunjește cumulativ la cent și se deduc facturile anterioare. Aceste raporturi sunt repartizare de rată inclusă, nu tarife pentru vizita suplimentară. Dacă obligații PI ale etapei rămân neprestate, partea lor convenită se amână.','distinctie_T0':'Inspecțiile profesionale inițiale T0 pentru baze/BWB sunt incluse în pachet și nu consumă cele 12 vizite B0; nu se taxează încă o dată aceeași prestație. Tarifele 13–18 rămân cele din fișa de opțiuni.'},
'E7_BWB_existenta_inainte_final':{'regula':'E7 include as-built, dosar final ZT/Fertigstellung complet, coordonarea de închidere și BWB întregul existent/nou cu înregistrarea aplicabilă. Termenul legal pentru existent poate preceda E7 final și nu se amână până la sfârșitul construcției.','decont_separabil':'Numai prestația BWB de existent efectiv completă și, când se cere, înregistrată poate fi decontată anticipat ca parte separabilă din E7. Înainte de factură se identifică exact conținutul și suma A_BWB_E7 alocată în E7, în scris, fără preț nou suplimentar. Nu se presupune că întregul E7 sau toată Pos. 06 PECH reprezintă exclusiv cartea existentului.','camp_de_negociere':{'berger':'A_BWB_E7 = ______ EUR net, parte din E7 de 4.500 EUR net, nu în plus.','pech':'A_BWB_E7 = ______ EUR net, parte din E7 de 6.930 EUR net, nu în plus.','motiv':'Nu există preț original separat verificabil pentru această subprestație; cuantumul nu se inventează. Se completează bilateral înainte de decontul anticipat.'},'reconciliere':'Soldul final E7 = rata E7 − sumele E7 deja corect facturate, inclusiv A_BWB_E7. Actualizarea cărții pentru intervențiile noi și restul dosarului rămân de predat. Fără dublă facturare și fără plata integrală a finalului pentru o carte încă incompletă.','probe':'BWB existent complet, calificări/Erstprüfung, registre/termene, înregistrare aplicabilă, proces de predare și alocarea acceptată a sumei.'},
'optiuni_0_6':options,'regie_originala_net_ora':{'berger':[{'rol':'Baumeister / Ziviltechniker','eur':'150.00'},{'rol':'Qualifizierter Techniker','eur':'135.00'},{'rol':'Techniker','eur':'95.00'},{'rol':'Sekretariat','eur':'75.00'}],'pech':[{'rol':'Ziviltechniker','eur':'195.00'},{'rol':'Projektleiter','eur':'145.00'},{'rol':'Techniker','eur':'125.00'},{'rol':'Technischer Zeichner','eur':'95.00'}],'regula':'Numai schimbare reală concretă aprobată, cu rol/prestație/plafon și dovezi; fără dublare cu pachetul sau tariful vizitei. Compensațiile și decontul legal justificat sunt distincte.'},
'text_propus_DE':[
'Für beide Anbieter werden dieselben Leistungs- und Abrechnungspunkte E1 bis E7 mit den Anteilen 10/20/25/15/10/10/10 Prozent des jeweiligen unveränderten Gesamtnettohonorars vorgeschlagen. Die Originalpositionen bleiben ausschließlich als Kalkulationsgliederung mit unveränderten Beträgen erhalten; sie begrenzen den gemeinsamen Leistungsumfang nicht.',
'Die laufende Meilensteinabrechnung setzt tatsächlich erbrachte, prüffähige und dem jeweiligen Leistungspunkt zuordenbare Leistungen voraus. Bei E2 bis E4 werden die ausdrücklich zugeordneten PI-Anteile erst mit dem tatsächlichen fachlichen PI-Bericht der geeigneten Person abrechenbar. Eine Planlieferung oder die interne Kontrolle des Planverfassers allein macht den PI-Anteil nicht fällig. Noch nicht erbrachte PI-Anteile werden zurückgestellt; vollständig gelieferte, sinnvoll abtrennbare Planungsanteile bleiben nach den vereinbarten Prüf- und Zahlungsregeln abrechenbar. Gesondert zu begründende gesetzliche Ansprüche aus Behinderung oder Beendigung bleiben unberührt.',
'E6 wird nach dem tatsächlichen, dokumentierten Leistungsfortschritt der zwölf enthaltenen physischen Ortstermine und zugehörigen PI-Befunde abgerechnet. Die PECH-Untergrundposition von EUR 800,00 netto ist im Grundhonorar enthalten und wird nur einmal nach vollständigem Befund abgerechnet. Ein gemeinsamer Termin zählt als ein physischer Termin; keine doppelte Reise-, PI- oder Statikabrechnung entsteht. Die wirtschaftliche Ratenaufteilung ist kein zusätzlicher Besuchstarif.',
'Eine gesetzlich früher fällige vollständige Bestands-Bauwerksbuchleistung wird rechtzeitig erbracht. Ihr gesondert abrechenbarer Betrag wird vor einer Teilrechnung ausdrücklich als Teil des E7-Budgets bezeichnet, nicht als zusätzlicher Preis. Der spätere E7-Restbetrag vermindert sich um sämtliche bereits auf E7 verrechneten Beträge. Fortschreibung für neue Eingriffe und die übrigen Abschlussleistungen bleiben geschuldet; eine noch unvollständige Gesamtleistung löst nicht die gesamte Schlussrate aus.'
],
'surse':[{'id':'MATRIX','cale':str(matrix),'sha256':hashlib.sha256(matrix.read_bytes()).hexdigest(),'rol':'Cerințele comune și metadatele reparate, sursă de negociere.'},{'id':'NEG_LEGAL','cale':str(O/'2026.10.13 Obiectii negociere reformulate.json'),'sha256':hashlib.sha256((O/'2026.10.13 Obiectii negociere reformulate.json').read_bytes()).hexdigest(),'rol':'Reperele comune E1–E7 din P09; text exact păstrat.'}],
'control_numeric':checks,'limite':['Nu confirmă acceptarea celor 80% sau a noilor alocări de către prestatori.','PECH alocarea PI timpurie și distribuția pe poziții sunt AG noi; nu sunt tarife/prețuri individuale primite. BERGER aceeași repartizare este preluată din draftul R05, nu din oferta originală.','Opțiunile necomandate nu se facturează. Pentru cele comandate și apoi împiedicate/anulate se analizează separat decontul legal justificat; nu se promite anulare gratuită în orice situație.','Retenția, înlocuirea prin garanție și dreptul legal la Sicherstellung sunt clauze distincte; această propunere numerică nu le modifică.','Nu s-au creat contracte/PDF și nu s-au modificat R05 sau sursele originale.']}

for v in ['BERGER','PECH']:
    f=W/f'2026.10.13 Werkvertrag {v} R05.json'
    obj['surse'].append({'id':v+'_R05','cale':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'rol':'Valori originale și alocare precedentă BERGER; R05 nemodificat.'})
file=W/'2026.10.13 Propunere economica comuna R06.json';file.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['2026.10.13 — PROPUNERE ECONOMICĂ COMUNĂ R06','BAZĂ AG DE EVALUAT ÎNAINTE DE INTEGRARE. NETRIMISĂ / NESEMNATĂ. R05 și PDF-urile existente nemodificate.']+obj['principii']+['','RATE COMUNE — valori EUR; TVA 20%, retenție 5% din net','Reper | Procent | BERGER net / TVA / brut / retenție / plată brută după retenție | PECH net / TVA / brut / retenție / plată brută după retenție']
for r in rows:
    line=[r['id'],str(r['procent_pachet'])+' %']
    for v in ['berger','pech']:line.append(' / '.join(r[v]['afisare'][x]for x in ['net','tva_20','brut','retentie_5_net','plata_bruta_dupa_retentie']))
    lines.append(' | '.join(line));lines.append(r['livrabil_comun']);lines.append('Termen: '+r['termen_trigger'])
for v in ['berger','pech']:lines.append('TOTAL '+v.upper()+': '+' / '.join(obj['totaluri'][v]['afisare'][x]for x in ['net','tva_20','brut','retentie_5_net','plata_bruta_dupa_retentie']))
lines+=['','CONTROLUL CELOR 80% PÂNĂ LA D5',obj['control_80_procente']['constatare'],obj['control_80_procente']['evaluare'],obj['control_80_procente']['fara_avans_PI']['provenienta'],obj['control_80_procente']['fara_avans_PI']['regula']]
for v,a in alloc.items():
    lines+=['','ALOCARE '+v.upper()+' — PROPUNERE AG, NU PREȚURI NOI','Reper | '+' | '.join(a['coloane_originale'])+' | TOTAL NET']
    for r in a['randuri']:lines.append(r['reper']+' | '+' | '.join(r['valori_net_afisate'])+' | '+disp(r['total_net_eur']))
    lines.append('SUMĂ | '+' | '.join(disp(x)for x in a['totaluri_originale_net_eur'])+' | '+disp(base[v.upper()]));lines.append(a['statut'])
for section in ['E6_facturare_pe_prestatie','E7_BWB_existenta_inainte_final']:
    lines+=['',section]
    for k,v in obj[section].items():lines.append(k+': '+(json.dumps(v,ensure_ascii=False)if isinstance(v,dict)else v))
lines+=['','OPȚIUNI ȘI REGIE','Maximum 6: BERGER 1.000 EUR net / 1.200 brut, total condiționat 46.000 net / 55.200 brut; PECH 2.700 net / 3.240 brut, total 72.000 net / 86.400 brut.','BERGER raport exact n × 2.000/12, rotunjire cumulativă; PECH 450 net per vizită. Fără dublare PI/statik, corecții proprii/documente normale și prestații deja remunerate.',json.dumps(obj['regie_originala_net_ora'],ensure_ascii=False),'','CLAUZE GERMANE PROPUSE']+obj['text_propus_DE']+['','CONTROL: procente 100%; sumele, TVA, retenția și toate coloanele originale reconciliate exact.']+obj['limite']
txt=file.with_suffix('.txt');txt.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('PASS: 7 repere, 100%, valori originale 4/6 intacte, net/TVA/brut/retenție exact; PI înainte D5 3.000/2.440, fără cost nou.')
print('JSONSHA',hashlib.sha256(file.read_bytes()).hexdigest());print('TXTSHA',hashlib.sha256(txt.read_bytes()).hexdigest())
