import pathlib,json,hashlib,sys,re
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path(__file__).parent;O=R.parent;W=O.parent/'2026.10.13 Reorganizare juridica si audit'
M=json.loads((O/'2026.10.13 Cerinte comune negociere matrice.json').read_text(encoding='utf-8'))
A=json.loads((W/'2026.10.13 Audit comercial comparativ R05 final.json').read_text(encoding='utf-8'))
E=json.loads((W/'2026.10.13 Propunere economica comuna R06.json').read_text(encoding='utf-8'))
assert hashlib.sha256((O/'2026.10.13 Cerinte comune negociere matrice.json').read_bytes()).hexdigest()=='73b45b4c8a18908f6f30bcea9400a4506de02de3719ede324750ca6afe76aa0f'
assert hashlib.sha256((W/'2026.10.13 Propunere economica comuna R06.json').read_bytes()).hexdigest()=='37fef92d28a852ecd2520c130d283e2d4a0dbbd61aa9882be0c0c16a1f62410d'
expected={'BERGER':'b2a5254c4806e4067eadd6d17613b815bcb5d7d85020f672cc32b1964a420d56','PECH':'edf8d2831118f5137cb5e616df0a96172ff4aa3781617ded5291668bda84e101'}
C={};SRC={};sources=[]
snap=R/'2026.10.13 Snapshot audit comercial independent';snap.mkdir(exist_ok=True)
for v in expected:
    p=R/f'2026.10.13 Werkvertrag {v} R06 Entwurf.json';data=p.read_bytes();h=hashlib.sha256(data).hexdigest();assert h==expected[v]
    (snap/f'2026.10.13 Snapshot {v} R06 final.json').write_bytes(data);C[v]=json.loads(data);s={}
    for sec in C[v]['sections']:
        for k,tx in enumerate(sec['paragraphs'],1):s[f"§ {sec['number']}({k})"]=tx
    for an in C[v]['annexes']:
        for k,tx in enumerate(an.get('paragraphs',[]),1):s[f"Anexa {an['number']}, alineat {k}"]=tx
        for t,tab in enumerate(an.get('tables',[]),1):
            for k,row in enumerate(tab['rows'],1):s[f"Anexa {an['number']}, tabel {t}, rând {k}"]=' | '.join(map(str,row))
    SRC[v]=s;sources.append({'prestator':v,'cale':str(p),'sha256':h,'sectiuni':len(C[v]['sections']),'anexe':len(C[v]['annexes']),'componente':len(s),'statut':'R06 Entwurf, negociere AG, nu acceptare prestator'})

routes='''
N001|§ 2(1);§ 11(1);Anexa 1, alineat 1
N002|§ 2(2);§ 2(5);Anexa 2, alineat 1
N003|§ 1(1);§ 1(2);§ 1(3);Anexa 6, tabel 1, rând 1
N004|§ 2(3);§ 2(4);§ 16(1);Anexa 5, alineat 1
N005|§ 3(1);§ 11(1)
N006|§ 3(2);Anexa 1, tabel 1, rând 5;Anexa 3, tabel 1, rând 7
N007|§ 3(2);§ 2(5);Anexa 1, tabel 1, rând 4
N008|§ 3(3);Anexa 1, tabel 1, rând 3;Anexa 3, tabel 1, rând 9
N009|§ 3(3);§ 3(4);Anexa 1, tabel 1, rând 7
N010|§ 3(4);Anexa 1, tabel 1, rând 6
N011|§ 3(5)
N012|§ 4(1);Anexa 1, tabel 1, rând 1
N013|§ 4(2);Anexa 1, tabel 1, rând 2
N014|§ 4(3);Anexa 3, alineat 5;§ 7(6)
N015|§ 4(4);§ 4(5)
N016|§ 4(1);§ 4(5);§ 5(7)
N017|§ 3(6)
N018|§ 5(1);Anexa 3, tabel 1, rând 11
N019|§ 5(2);§ 5(4)
N020|§ 5(3);§ 5(7);§ 7(4);§ 7(5)
N021|§ 5(4)
N022|§ 5(5)
N023|§ 5(6)
N024|§ 5(7);§ 8(4)
N025|§ 5(8);§ 11(2)
N026|§ 6(1);Anexa 1, tabel 1, rând 9
N027|§ 6(2)
N028|§ 6(3)
N029|§ 6(3);§ 6(4)
N030|§ 6(4);§ 2(2)
N031|§ 6(5);Anexa 3, alineat 6;Anexa 3, tabel 1, rând 17
N032|§ 6(6);Anexa 3, alineat 6;Anexa 3, tabel 1, rând 16
N033|§ 6(7)
N034|§ 7(1);§ 7(2);§ 7(3);§ 8(2);Anexa 3, alineat 2
N035|Anexa 3, tabel 2, rând 1;Anexa 3, tabel 2, rând 2;Anexa 3, tabel 2, rând 3;Anexa 3, tabel 2, rând 4;Anexa 3, tabel 2, rând 5;Anexa 3, tabel 2, rând 6;Anexa 3, tabel 2, rând 7;Anexa 3, tabel 2, rând 8;Anexa 3, tabel 2, rând 9;Anexa 3, tabel 2, rând 10;Anexa 3, tabel 2, rând 11;Anexa 3, tabel 2, rând 12
N036|§ 5(3);§ 7(4);§ 11(1)
N037|§ 7(4);§ 7(5);Anexa 3, alineat 4;Anexa 4, alineat 7
N038|Anexa 4, alineat 5;Anexa 4, alineat 6;Anexa 4, tabel 6, rând 1;Anexa 4, tabel 6, rând 2
N039|Anexa 4, alineat 6
N040|§ 7(5);§ 9(7);§ 11(5)
N041|§ 7(6);§ 9(8)
N042|§ 7(2);Anexa 3, tabel 2, rând 1;Anexa 4, alineat 9;Anexa 4, tabel 3, rând 6
N043|§ 8(1);Anexa 2, alineat 1
N044|§ 8(2);Anexa 3, alineat 2;Anexa 3, tabel 1, rând 5
N045|§ 8(2);§ 8(3);§ 6(1);§ 8(6)
N046|§ 8(6);§ 5(4)
N047|§ 8(4)
N048|§ 8(5)
N049|§ 9(1);Anexa 3, tabel 1, rând 1;Anexa 3, tabel 1, rând 2
N050|§ 9(2);§ 9(7);§ 11(1);Anexa 3, tabel 1, rând 12;Anexa 3, tabel 1, rând 13;Anexa 3, tabel 1, rând 14;Anexa 3, tabel 1, rând 15
N051|§ 9(6);Anexa 3, tabel 1, rând 6;Anexa 3, tabel 1, rând 7;Anexa 3, tabel 1, rând 8;Anexa 3, tabel 1, rând 9;Anexa 3, tabel 1, rând 10
N052|Anexa 3, alineat 3;§ 12(2);§ 9(6)
N053|§ 9(3);§ 9(8);§ 7(3)
N054|§ 9(4);§ 9(5);§ 15(2)
N055|§ 9(7);§ 15(1)
N056|§ 10(1)
N057|§ 10(2)
N058|§ 10(3)
N059|§ 10(4)
N060|§ 10(5);§ 15(5)
N061|§ 10(6);Anexa 4, tabel 2, rând 7
N062|§ 11(1);Anexa 4, tabel 2, rând 8
N063|Anexa 4, tabel 3, rând 8
N064|§ 11(2);§ 2(5)
N065|§ 11(3);§ 11(4)
N066|§ 11(5);Anexa 4, tabel 5, rând 1;Anexa 4, tabel 5, rând 2;Anexa 4, tabel 5, rând 3;Anexa 4, tabel 5, rând 4
N067|§ 11(2);§ 7(1)
N068|§ 12(2)
N069|§ 12(1);Anexa 4, alineat 1;Anexa 4, alineat 2;Anexa 4, alineat 8
N070|Anexa 4, alineat 3;Anexa 4, alineat 9;Anexa 4, tabel 3, rând 2;Anexa 4, tabel 3, rând 3;Anexa 4, tabel 3, rând 4
N071|§ 12(1);§ 12(2);§ 12(3)
N072|§ 12(3);§ 12(4)
N073|§ 12(4)
N074|§ 12(5);§ 13(3)
N075|§ 12(6);Anexa 6, tabel 1, rând 7
N076|§ 12(7);§ 15(3)
N077|§ 13(1)
N078|§ 13(2)
N079|§ 13(3);§ 15(6)
N080|§ 13(4)
N081|§ 13(5);§ 13(6);Anexa 6, tabel 2, rând 8
N082|§ 14(1);Anexa 6, tabel 1, rând 2;Anexa 6, tabel 1, rând 5;Anexa 6, tabel 1, rând 9
N083|§ 14(2);§ 5(2);Anexa 6, tabel 1, rând 3;Anexa 6, tabel 1, rând 4;Anexa 6, tabel 1, rând 5
N084|§ 14(3);§ 14(4);§ 14(5);Anexa 6, tabel 1, rând 6;Anexa 6, tabel 2, rând 10
N085|§ 14(5);§ 8(5)
N086|§ 15(1);§ 15(2)
N087|§ 15(3)
N088|§ 15(4)
N089|§ 15(5)
N090|§ 15(6)
N091|§ 16(1);§ 16(2);Anexa 6, tabel 1, rând 8
N092|§ 16(3)
N093|§ 16(4)
N094|§ 16(5)
N095|§ 2(5);Anexa 6, alineat 3;Anexa 6, tabel 1, rând 9
N096|§ 10(7)
N097|Anexa 6, alineat 3;Anexa 6, tabel 1, rând 2;Anexa 6, tabel 1, rând 9
N098|§ 3(7);§ 11(1);§ 11(3)
N099|§ 2(5);Anexa 1, alineat 2;Anexa 2, tabel 1, rând 9
N100|Anexa 5, alineat 1;Anexa 6, alineat 2
'''
routes={i:refs.split(';')for i,refs in (line.split('|',1)for line in routes.strip().splitlines())}
assert set(routes)=={x['id']for x in M['matrice']}
special={'N034':'T0 profesional separat, digital zero; 12 B0 fizice și prima Untergrund/Fundierung sunt explicite la ambii.','N035':'Cele 12 faze sunt identice, fără transfer tacit al unei faze la digital ori diminuarea verificării reale.','N036':'Aceeași regulă 12+6 la ambii, inclusiv PI fizic; documentele normale și corecturile/dublarea sunt excluse din supliment.','N038':'Diferența economică este păstrată: BERGER tarif AG derivat n × 2.000/12, PECH 450 EUR net.','N042':'PECH 800 este în bază, facturabil o singură dată după Befund; o vizită comună se numără o dată. BERGER același rezultat de teren în pachet, fără falsă poziție separată 800.','N050':'18 luni de la B0 real, T0 înainte distinct, închidere obișnuită inclusă; formularea ambiguă § 9(2) a fost clarificată.','N051':'D1–D5 aceleași 3/6/8/10/12 săptămâni, obligatorii relativ T0; nu calendar PECH rămas nedeterminat.','N062':'Totalurile proprii net/TVA/brut sunt păstrate; fără BWB/PI supliment implicit.','N063':'Toate 4/6 valori originale și fiecare coloană economică sunt reconciliate, fără limitarea scopului prin poziție.','N069':'Aceleași 7 repere și procente 10/20/25/15/10/10/10; numai rezultate prestate, cu decont legal separat pentru împiedicare/încetare.','N070':'PI E2/E3/E4 profesional efectiv, fără facturarea planului propriu ca PI; 3.000 BERGER/2.440 PECH în alocarea economică, nu cost nou.','N081':'Aceeași penalitate 0,1% din netul etapei/zi culpabilă, max5% din netul pachetului; diferența plafonului este economică, nu de clauză.','N084':'O singură regulă administrativă neutră, fără prag numeric nou sau 2× anual; nu mai există avantaj/minim diferit impus unui ofertant.','N088':'§ 1168 decont corect: economii, venit alternativ efectiv și omis intenționat; nu anulare gratuită automată sau plată numai a orelor efectuate.','N095':'Nicio reînnoire a ofertei vechi prin draft AG; răspuns comercial/resurse/calendar înainte de semnare.','N100':'Bază de negociere AG, NETRIMISĂ/NESEMNATĂ; extinderile sunt propuneri explicite, nu pretinse acceptări istorice.'}
criteria=[]
for r in M['matrice']:
    line={'id':r['id'],'tema':r['criteriu'],'capitol_faza':r['capitol_faza'],'cerinta_comuna_verificata':r['cerinta_comuna'],'rezultat':'PASS pentru redactarea propunerii comune','constatare':special.get(r['id'],'Conținutul, livrabilul, declanșarea, dovada și delimitarea cerinței comune sunt acoperite în textele R06 citate. Nu se afirmă prestarea sau acceptarea lor.'),'teme_originale':r['teme_60']}
    for v in SRC:
        refs=list(routes[r['id']])
        if r['id']=='N063':refs +=[f'Anexa 4, tabel 1, rând {k}'for k in range(1,5 if v=='BERGER' else 7)]
        line[v.lower()]={'original':r[v.lower()]['original'],'surse_originale':r[v.lower()]['surse_original'],'referinte_r06':[{'referinta':x,'citat':SRC[v][x]}for x in refs]}
    criteria.append(line)

def num(x):return Decimal(str(x).replace('.','').replace(',','.'))
numeric=[]
for v in C:
    tables=C[v]['annexes'][3]['tables'];base=Decimal('45000'if v=='BERGER'else'69300')
    original=[num(row[1])for row in tables[0]['rows'][:-1]];assert original==list(map(Decimal,['13000','20000','2000','10000']if v=='BERGER'else['42000','6000','5000','800','14000','1500']))
    rate=tables[1]['rows'][:-1];assert[len(rate),sum(num(row[3])for row in rate)]==[7,base]
    for k,row in enumerate(rate):assert row[2]==str(E['repere_plati'][k]['procent_pachet'])+' %'and num(row[3])==Decimal(E['repere_plati'][k][v.lower()]['net_eur'])
    allocation=tables[2]['rows'];want=E['alocare_interna_propusa'][v.lower()]['randuri']
    for k,row in enumerate(allocation[:-1]):
        vals=list(map(num,row[1:-1]));assert vals==list(map(Decimal,want[k]['valori_net_eur']));assert sum(vals)==num(row[-1])
    for k,a in enumerate(original):assert sum(num(row[k+1])for row in allocation[:-1])==a
    actual=tables[3]['rows']
    for k,row in enumerate(actual[:-1]):
        w=E['repere_plati'][k][v.lower()];assert list(map(num,row[1:]))==[Decimal(w[key])for key in ['net_eur','tva_20_eur','brut_eur','retentie_5_net_eur','plata_bruta_dupa_retentie_eur']]
    for k in range(1,6):assert sum(num(row[k])for row in actual[:-1])==num(actual[-1][k])
    rates=tables[4]['rows'];expected_rates=E['regie_originala_net_ora'][v.lower()];assert[num(r[1])for r in rates]==[Decimal(x['eur'])for x in expected_rates]
    opt=tables[5]['rows'];assert num(opt[0][2])==Decimal('1000'if v=='BERGER'else'2700')and num(opt[1][2])==base+num(opt[0][2])
    numeric.append({'prestator':v,'rezultat':'PASS exact Decimal','pozitii_originale':list(map(str,original)),'rate_net':list(map(lambda r:str(num(r[3])),rate)),'total_net':str(base),'TVA_20':str(num(actual[-1][2])),'brut':str(num(actual[-1][3])),'retentie_5_net':str(num(actual[-1][4])),'plata_dupa_retentie':str(num(actual[-1][5])),'suma_procente':100,'max_optiuni_net':str(num(opt[0][2])),'total_cu_6_net':str(num(opt[1][2]))})

actual_diffs=[]
for bs,ps in zip(C['BERGER']['sections'],C['PECH']['sections']):
    assert bs['number']==ps['number']and len(bs['paragraphs'])==len(ps['paragraphs'])
    for k,(b,p)in enumerate(zip(bs['paragraphs'],ps['paragraphs']),1):
        if b!=p:
            assert(bs['number'],k)in[(1,2),(11,1)]
            actual_diffs.append({'referinta':f"§ {bs['number']}({k})",'tip':'identitate prestator'if bs['number']==1 else'valoare economică permisă','berger':b,'pech':p})
for n in [1,2,3,6]:assert C['BERGER']['annexes'][n-1]==C['PECH']['annexes'][n-1],n
bt=C['BERGER']['annexes'][3]['tables'];pt=C['PECH']['annexes'][3]['tables']
assert[(r[0],r[1],r[2])for r in bt[1]['rows']]==[(r[0],r[1],r[2])for r in pt[1]['rows']]
assert len(actual_diffs)==2

# Invers: fiecare alineat/rând din propriul R06 are cel puțin un criteriu comercial adecvat.
inverse=[]
for v,s in SRC.items():
    for ref,tx in s.items():
        ids=[c['id']for c in criteria if ref in[x['referinta']for x in c[v.lower()]['referinte_r06']]]
        if not ids:
            if ref.startswith('Anexa 1, alineat 1'):ids=['N001']
            elif ref=='Anexa 1, tabel 1, rând 8':ids=['N021','N023','N061']
            elif ref.startswith('Anexa 2, tabel'):ids=['N002']
            elif ref=='Anexa 3, alineat 1':ids=['N049','N051']
            elif ref.startswith('Anexa 3, tabel 1, rând '):ids={'3':['N043'],'4':['N051']}[ref.rsplit(' ',1)[1]]
            elif ref.startswith('Anexa 4, tabel 1'):ids=['N062']
            elif ref.startswith('Anexa 4, tabel 2'):ids=['N069']
            elif ref.startswith('Anexa 4, tabel 3'):ids=['N063','N069']
            elif ref.startswith('Anexa 4, tabel 4'):ids=['N074','N069']
            elif ref=='Anexa 4, alineat 4':ids=['N014','N061']
            elif ref=='Anexa 4, alineat 10':ids=['N069','N074']
            elif ref=='Anexa 6, alineat 1':ids=['N003','N083','N084']
            elif ref.startswith('Anexa 6, tabel 1, rând 10'):ids=['N002','N049','N051']
            elif ref.startswith('Anexa 6, tabel 2, rând '):ids={'1':['N001'],'2':['N020','N026'],'3':['N050','N051'],'4':['N034','N038'],'5':['N014','N046'],'6':['N064','N065'],'7':['N069','N074'],'9':['N058','N088']}[ref.rsplit(' ',1)[1]]
            else:raise ValueError('R06 fără asociere: '+v+' '+ref)
        assert all(i in routes for i in ids)
        inverse.append({'prestator':v,'referinta_r06':ref,'criterii':ids,'text_r06':tx,'statut':'Cerință AG comună explicită sau alocare/identitate economică proprie; nu acceptare istorică.'})
assert len(criteria)==100
original=[]
for r in A['checklist']:
    ids=[c['id']for c in criteria if r['id']in c['teme_originale']];assert ids
    original.append({'id':r['id'],'tema':r['tema'],'berger_original':r['berger']['oferta'],'pech_original':r['pech']['oferta'],'surse_originale':[r['berger']['sursa'],r['pech']['sursa']],'criterii_r06':ids,'concluzie':'Valorile/tarifele originale sunt păstrate când sunt aplicabile; condițiile și scopul comun mai amplu sunt explicit propuși prin R06 și ierarhia § 2, nu pretinse ca acceptate de ofertant. Abaterea de la original prin propunere AG nu este un defect în sine.'})
closed={'id':'F01','tema':'§ 9(2), durata cadrului','severitate':'clarificare editorială comună','snapshot_initial':{'berger':'d6eaa839dad7ff8ed54ff09b13dfe23b22f5bae5d69563d7edc575758418ccb3','pech':'033f030e1a49f2d8a0e89227740bddc306b21d6224efc4c63a3179ff01a04a07'},'observatie_initiala':'Sintagma über achtzehn Monate putea fi citită drept depășire a duratei, în loc de execuție în cadrul acesteia.','rezultat_final':'ÎNCHIS la ambii: innerhalb dieses achtzehnmonatigen Rahmens, fără schimbarea prețului, B0 sau regulilor de depășire/compensație.'}
for v in C:assert'innerhalb dieses achtzehnmonatigen Rahmens'in C[v]['sections'][8]['paragraphs'][1]
obj={'data':'2026.10.13','titlu':'Audit comercial independent bidirecțional R06','rol':'Audit independent al textului/scopului/comparabilității și cifrelor; auditul normativ juridic este efectuat separat.','statut':'R06 este propunere AG pentru negociere, NETRIMISĂ/NESEMNATĂ. Nu este contract acceptat, executat sau atribuit.','rezultat':'PASS pentru comparabilitatea propunerilor și reconcilierea exactă a cifrelor. Nu au fost identificate omisiuni de scop sau diferențe operative nepermise după închiderea F01.','criterii_100':criteria,'original_catre_r06_60':original,'r06_catre_cerinte':inverse,'diferente_operative':actual_diffs,'control_numeric':numeric,'observatii_inchise':[closed],'observatii_deschise':[],'puncte_de_negociere':['80% până la D5 este o alocare AG spre faza de proiectare, nu datorie automată pe simplul plan. PI timpuriu 3.000/2.440 EUR este condiționat de controlul profesional efectiv; părțile neprestate se amână.','Durata18 luni, 12 fizice+T0 separat, extinderile PI/BWB, formatele, drepturile, garanția/retenția și penalitatea comună sunt cerințe explicite de negociere la valorile proprii; răspunsul ofertantului, echipa și bazele exacte rămân de confirmat.','Alocarea BWB de existent facturabil mai devreme trebuie identificată exact în E7 înaintea facturii, fără preț nou și cu deducere din soldul E7. Acesta este parametru de negociere viitoare, nu onorariu suplimentar inventat.','Originalul PECH trimite generic la LB AG; nu se afirmă că nicio componentă PI există în original, nici că întregul pachet R06 ar fi fost deja acceptat prin acea trimitere.','Ofertele originale rămân copii nemodificate în folderele de livrare; propunerea nu le reînnoiește unilateral valabilitatea.'], 'surse_r06':sources,'surse_originale':E['surse'][-2:],'repere_comune_sha256':'73b45b4c8a18908f6f30bcea9400a4506de02de3719ede324750ca6afe76aa0f','economic_sha256':'37fef92d28a852ecd2520c130d283e2d4a0dbbd61aa9882be0c0c16a1f62410d','acoperire':{'criterii':100,'teme_originale':60,'sectiuni_per_firma':16,'alineate_principale_per_firma':96,'anexe_per_firma':6,'componente_R06':len(inverse),'referinte_inexistente':0,'anexe_tehnice_si_conditii_identice':[1,2,3,6],'original_position_counts':[4,6]},'limite':['Nu este certificat de abilitare, registru live, poliță actuală, acceptare a prețului sau început de șantier.','Fidelitatea și comparabilitatea textului sunt distincte de oportunitatea comercială și aprobarea cifrelor noi de către ofertanți.','Auditul nu modifică documentele R06/R05, nu trimite emailuri și nu creează contracte sau PDF.','Înaintea livrării PDF este necesară verificarea vizuală a tuturor paginilor de către echipa QA; această verificare nu este inclusă în prezentul audit de JSON.']}
p=R/'2026.10.13 Audit comercial independent R06.json';p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['2026.10.13 — AUDIT COMERCIAL INDEPENDENT R06',obj['statut'],obj['rezultat'],'Acoperire: 100 criterii; 60 teme originale; 16 secțiuni, 96 alineate și 6 anexe per firmă; '+str(len(inverse))+' componente R06.','Surse finale: BERGER '+expected['BERGER']+'; PECH '+expected['PECH'],'F01 închis: § 9(2) clarifică cadrul de18 luni; fără alte diferențe operative de scop.','Diferențele § 1(2) și § 11(1) sunt numai identitatea firmei și prețul. Anexele1/2/3/6 sunt identice; Anexa4 are aceleași rezultate/procente cu valorile proprii, Anexa5 păstrează originalul propriu.','']
for r in criteria:
    lines +=[r['id']+' — '+r['tema'],r['constatare']]
    for v in SRC:lines.append(v+': '+', '.join(x['referinta']for x in r[v.lower()]['referinte_r06']))
    lines.append('')
lines+=['CONTROL NUMERIC']+[json.dumps(x,ensure_ascii=False)for x in numeric]+['','PUNCTE DE NEGOCIERE']+obj['puncte_de_negociere']+['','LIMITE']+obj['limite']
p.with_suffix('.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('PASS',len(criteria),'criterii',len(inverse),'componente',len(original),'teme originale; sume reconciliate exact, anexe1/2/3/6 identice, numai2 diferențe operative permise.')
print('REPORTSHA',hashlib.sha256(p.read_bytes()).hexdigest())
