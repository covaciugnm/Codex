from a03_r8_base import *
import collections,shutil
base=out.parents[2]; qr=base/'Coada_reverificari_P01.json'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):
 p=P(p)
 if not p.is_absolute():p=out/p
 return {'file':str(p.relative_to(base)).replace('\\','/'),'sha256':H(p.read_bytes())}
states={'P':'CONFORM_ORACOL_EXECUTAT','F':'ABATERE_ORACOL_EXECUTAT','L':'PARȚIAL_EXERCITAT','H':'RECALCUL_PE_INSTANTANEU_ISTORIC','D':'DOAR_DOCUMENT_INDEXAT','N':'NEEXECUTAT','X':'EXERCITAT_SEPARAT_T191'}
rows=read(qr)['rows'];search={r['criterion']:r for r in rows if r['owner']=='A03' and r['category'].startswith('FIX')};assert len(search)==239
ar=read(out/'Index_istoric.json')['relatii'];cases={};
def add(t,i,state,claim,links,limit='',sub=None):
 k=t+'-R2-'+str(i).zfill(3);assert k in search,(t,i);assert k not in cases,k
 cases[k]={'status':states[state],'mesurat':claim,'limita':limit,'dovezi':[ref(x) for x in links],'subprobe':sub or []}
def l(n):return 'log/'+n+'.txt'
for i,lot,cmd in [(4,'A','ramase'),(5,'A','chei-lipsa'),(16,'B','ramase'),(17,'B','chei-lipsa'),(22,'C','ramase'),(54,'E','ramase'),(55,'E','chei-lipsa')]:add('T159',i,'P',f'Generatorul Git {cmd} pe lotul {lot} întoarce 0 la SHA fix, rc 0.',[l('159-'+cmd+'-'+lot)])
for i,desc in [(14,'grupul anaf/AcoperireDeclaratii, FirmaInfo, GenBilant, GenD394'),(20,'grupul GenD112, MotorSalariiRO, WSagaConfigSalariiForm'),(25,'anaf/GenD101')]:add('T159',i,'P','Niciun rezultat pentru '+desc+' după normalizarea prefixului Git al fișierului, controlul global are doi alți candidați.',[l('159-readers'),l('159-readers-groups')])
add('T159',23,'L','Zero chei C lipsă. Sursa seed are câte un rând pentru REZERVA_LEGALA_COTA și REZERVA_LEGALA_PLAFON.',[l('159-chei-lipsa-C'),l('159-keys-seeds')],'SELECT din firma reală de laborator cerut explicit lipsește.')
add('T159',27,'P','TestT29ImportSetari rulează 52 verificări, 0 FAIL inclusiv import/migrare. Aceeași sursă Saga din Git în ambele rulări, cu contab Git și instalat.',[l('retry-git-TestT29ImportSetari'),l('retry-installed-TestT29ImportSetari')],'Fixtura scriitorului este sintetică.')
add('T159',29,'F','Oracolul cere 0, scriptul listează 2, rc 1.',[l('159-readers'),l('159-frozen-diagnostic')],'Prima linie raportată formatează «sector» și nu citește o setare. A doua pasează o cheie de arhivă către amanaCheieArhiva. Verificarea eșuează, o deficiență de migrare a firmei nu se deduce de aici.')
add('T159',30,'P','Comanda literală din §3.6 cu cele 19 chei și verbele de scriere are 0 rezultate.',[l('159-writes')])
add('T159',39,'F','Triaj înghețat b7e563428c, 3321 locuri, 570 diferențe etichetate, rc 1.',[l('159-central'),l('159-frozen-diagnostic')],'Include decalaje de linie și elemente devenite orfane. Nu sunt 570 valori fiscale greșite.')
add('T159',49,'P','57 fișiere text în dosarul de probă față de minimul 17.',[l('159-doc')],'Rezultatul măsoară inventarul solicitat, nu succesul operațiilor documentate.')
add('T159',50,'P','Compararea triajului înghețat cu cel curent: reclasificate 0, rc 0. Obiectele TSV nu sunt identice octet cu octet.',[l('159-reclass'),l('159-frozen-diagnostic')])
add('T159',51,'F','Regenerarea triajului la 6df998a cu 3174 rânduri raportează 136 netriate/conflicte, rc 1.',[l('159-rules')],'Este deriva față de regulile înghețate, nu o concluzie asupra sumelor declarate.')
reg4=base/'executie/R4_zone/A03/dovezi';race=reg4/'T58_race_native.json';nat=reg4/'T58_positive_and_reverse.json';rg4=reg4/'Registru_subcriterii_R4.json'
for i in (13,14):add('T58',i,'P','Restituire exactă R4: 10 perechi cu autentificări native independente, 5 în fiecare ordine preferată, 0 perechi lăsate cu VC activă și AMORT inactivă. LR-2 pe SHA fix rc 0.',[race,nat,rg4],'Proba ERP este R4; ordinea expedierii nu impune ordinea commiturilor.')
add('T58',16,'L','Închidere AMORT și VC reale și gărzi repetate. TestA83Butoane 79/0 pe ambele JAR.',[nat,l('retry-git-TestA83Butoane'),l('retry-installed-TestA83Butoane')],'Procesul nominal R-REINCH și mesajul său nu au fost reexecutate.')
for i,log,state,text in [(55,'055','P','12 tabele-document, 0 netratate, rc 0.'),(59,'059','F','25 ecrane, două neclasificate – ValidareProdusInventar și WSagaPreluareDateForm, rc 1.'),(60,'060','P','Zero porți după deschiderea tranzacției sau în metodă cu Trx primit, rc 0.'),(61,'061','F','70 ecrane candidate și 18 neclasificate, rc 1.'),(62,'062','F','Generatorul de inventar întoarce rc 1 și 8 verificări căzute la SHA fix. Mutanții M1–M3 nu au fost rulați, deoarece oracolul pozitiv însuși cade.')]:add('T58',i,state,text,[l('58-'+log)],'Inventar structural al versiunii curente; efectul în UI sau înregistrările contabile necesită probă proprie.' if state=='F' else '')
add('T58',77,'P','310 cazuri ale celor patru module în JUnit-ul auditului la același SHA, toate fără skip/failure/error. Repetarea întregului lot în Windows a atins 160 s fără verdict.', ['T58_JUnit_recitire.json'],'Testele au registru SQLite și iDempiere simulat. Nu validează o sesiune de cabinet.')
for i,tag in [(72,'refuz_pas_nefacut_registrul_neatins'),(73,'succes_inchide_luna_si_audit'),(74,'indisponibil_refuz_503'),(76,'portofoliu'),(78,'portal_refuz_arata_mesajul'),(83,'firma')]:
 ev=read(out/'T58_JUnit_recitire.json')['tests'];matches=[r['name'] for r in ev if r['class'].endswith('test_t58_close_month') and tag in r['name']]
 add('T58',i,'L','Intrarea FastAPI sau logica portalului executată în testele nominale: '+', '.join(matches),['T58_JUnit_recitire.json'],'iDempiere simulat; scenariul de cabinet R-B și captura UI solicitate nu au fost refăcute integral în R8.',matches)
add('T58',79,'L','Comentariul distinct apare exact o dată. TestPornireContab se oprește la javap Windows după verificări parțiale.',[l('58-079'),l('retry-git-TestPornireContab')],'Suita nativă integrală a acestui criteriu nu are verdict în această execuție.')
add('T156',4,'P','C-1a 1 și C-1b 7/7 pe codul înghețat.',[l('156-core')])
j156=[l('git-TestT156MutareCont'),l('installed-TestT156MutareCont')];jj=(out/j156[0]).read_text(encoding='utf8',errors='replace').splitlines()
for i,pt,desc in [(11,'C-8','Lunile intervalului inclusiv trecerea anului și cazurile inversate.'),(12,'C-9','Refuzurile de validare cont identic, interval invers, cont din altă firmă, inactiv sau sintetic.'),(13,'C-9b','TipCod diferit de CONT în cinci variante.'),(14,'C-10','Firma nedeterminată și filtrele client ale scrierilor/citirilor.'),(15,'C-11','Reaplicarea în ordine a lanțului A–B–C.'),(16,'C-12','Amprentă identică după rescalare; alt contor, sumă, max ID schimbă amprenta.'),(18,'C-13b','Condus în memorie prin modelul nativ al mutării/stornării.'),(19,'C-13c','Cârligul de eroare testat structural prin addErrorMessage.'),(20,'C-14','Testul verifică UPDATE-ul sursei notei, inclusiv combinația contabilă.'),(21,'C-15','Exact D100 pentru 4418 și niciuna pentru 401, cu controale semestru, recipisă și altă firmă.'),(26,'C-20','Semnalarea copiilor refăcuți și câmpurile separate sunt verificate în cod.'),(28,'C-22','Idempotența declarativă a celor trei indexuri și ruta ensure* sunt verificate în cod.')]:
 relevant=[x.strip() for x in jj if 'OK ' in x and pt in x];add('T156',i,'L',desc,j156,'98 verificări pozitive pe fiecare JAR. Fixtura e pură/structurală, fără SQL înainte/după, clic, conflict între tranzacții sau postare reală.',relevant[:6])
add('T156',24,'F','Testul nominal 98/0, C-18a=2 în loc de 1, C-18b=1 și C-18c=130 în loc de 120 în catalogul curent.',[l('156-core')]+j156,'Suita completă și mutanții nu au fost rulați; creșterea catalogului integrat nu este o eroare a mutării conturilor.')
pair='T186_detectori_independenti.json'
add('T186',5,'P','Reconstituit exportul T0 1b9a18466d: cele 338 perechi din inventarul înghețat și cele 338 ale detectorului sunt identice.',[pair],'După integrare detectorul mai găsește 21, iar acum 17. Compararea cere T0.')
add('T186',6,'L','0 motive scurte/șablon, în 30 rânduri d în inventarul capturat acum; numitorul istoric specificat era 29.',[l('186-006')],'Confirmă proprietatea motivului, nu și eșantionul literal 29.')
add('T186',7,'P','Ambele gărzi originale LR-3 au produs exact 18/0 și 3/0.',[l('186-32_test_clasa_r1'),l('186-36_test_clasa_r2')])
add('T186',12,'P','Exact un fișier/un rezultat în detector: jurnal/AvertismentUnic.java.',[l('186-012')])
for i,lot in [(13,'LA'),(14,'LA'),(17,'LB'),(18,'LB'),(22,'LB2'),(34,'all')]:
 a={'LA':'57 fișiere / 19 cu abateri','LB':'52 / 40','LB2':'1 / 1','all':'110 / 60'}[lot]
 sc='K-CLS/K-INV dif în exportul actual, '+a+'.'
 if i==18:
  add('T186',i,'L','Verificatorul întreg LB este roșu. Nu separă în rezumat c-ecran; testele de propagare LB au 26/0. Nu atribui tuturor notificărilor abaterile amprentei.',[l('186-KCLS-'+lot),l('git-TestT186PropagareLB')],'Mutantul exact M-A6 și UX lipsesc.')
 else:add('T186',i,'F',sc,[l('186-KCLS-'+lot)]+([l('186-kinv')] if i in (14,34) else []),'Modificările legitime ulterioare și deplasările de ordinale sunt incluse. Nu traduce numărul în defecte de produs; trialul mutantului pe sursa deja deplasată poate fi neinterpretabil.')
add('T186',24,'P','Java și Python produc aceleași 338 perechi pe exportul T0. Repetate pe integrarea T186: 21/21. La SHA fix: 17/17; diferența simetrică este 0 în fiecare export.',[pair],'338 este numărul de pe T0, nu numărul de pe HEAD.')
add('T186',35,'P','MD5 JAR Git exportat identic cu git show; etichete.tsv extras din JAR 26ad66d0c6b92b50a52baa96d0807988, identic cu sursa de la același SHA.',[l('256-JAR-resource')])
add('T256',2,'L','40 rânduri din grep și 0 LIPSA pentru bucla nominală; acoperirea semantică/justificarea fiecărui rând nou nu este stabilită doar prin numele fișierului.',[l('256-inventory')])
add('T256',3,'F','K-S1=0 și K-S2=3; verificarea suplimentară a expresiei substring pe fișierul întreg numără 1 în loc de 0; apelul găsit este în calculul steagului din_docno din GenD394:1849.',[l('256-kstatic-explicit'),l('256-raw-BRE'),l('256-raw'),'T256_SQL_din_JAR.json'],'Cele 15 verificări SQL/JAR sunt corecte; acest test static nu dovedește numărarea greșită a facturilor.')
add('T256',4,'L','SQL obținut prin reflecție din GenD394 în fiecare JAR: F01–F10, ambele liste de vânzări și stornări, steagurile și izolarea firmei reproduc 15/15 oracole, fără FAIL.', ['T256_SQL_din_JAR.json','T256_SQL.json'],'Nu s-au creat facturile din scenariul nominal în ZK, iar T1/S1/S2 nu sunt aceleași date.')
add('T256',15,'P','Diff de la baza 1ba1029296 pe clasele D394Reguli cu predicatele specificate: 0. Diff de statistică al fixturilor t180: gol.',[l('256-015')],'Comparație la SHA actual; nu echivalează cu semnarea originală.')
add('T256',16,'L','Mutantul M-A pierde filtrul OSS și întoarce X 8 în lista de vânzări: ROSU. M-B și M-C nu sunt în aceeași campanie SQL.', ['T256_SQL.json'],'Nu echivalează cu 3/3 mutanți uciși.')
add('T256',18,'P','Au fost parcurse celulele Punct și Observat pe fiecare rând M. Regula :număr apare în ambele celule în toate cele 34/34 rânduri.',[l('256-018')])
add('T256',19,'L','Mutantul M16 produce 200013 de la firma 2; rularea SQL din JAR la firma 1 exclude firma B. Extrasul izolat al firmei 2 readuce numai 200013.', ['T256_SQL_din_JAR.json','T256_SQL.json'],'Nu a fost postată o ARI F-L1 într-un cabinet în timpul măsurării.')
add('T256',24,'P','Există 22 artefacte în directorul cerut față de minimum 20.',[l('256-024')])
add('T254',1,'L','Din TestT254EroriInchidere: 550 metode, 112 catch-uri evaluate, 0 tăcute nemarcate la ambele JAR.',[l('git-TestT254EroriInchidere'),l('installed-TestT254EroriInchidere')],'Inventarul INV cu formula N_L+N_C nu a fost reconciliat complet.')
add('T254',2,'F','Scriptul original inventar_fara_catch găsește 122 citiri, 117 SUB și 5 AFARA față de oracolul 0 (2 getSQLValue*, 3 MSysConfig).',[l('254-afara')],'Acoperirea statică a grafului s-a schimbat; cazurile semantice trebuie reproduse înaintea unei atribuiri financiare.')
add('T254',3,'P','Garda native: 3 chei în surse, aceleași 3 în test; 0 fără motiv.',[l('git-TestT254EroriInchidere'),l('installed-TestT254EroriInchidere')])
add('T254',16,'P','Metoda citiri() din TestT254EroriInchidere a executat null, gol, 2026-1 și x. Valorile invalide poartă numele cheii, cele absente nu reclamă cheia; întregul test 67/0 pe fiecare JAR.',[l('git-TestT254EroriInchidere'),l('installed-TestT254EroriInchidere')],'Independent de existența bazei, scopul este garda parametrului. Simularea nu atestă închiderea lunii.')
for i in (7,22):add('T11',i,'P','grep pe formularul REGES și clasele directorului, 39 fișiere, toate 0 apariții setStyle(.', [l('11-style')],'grep rc 1 când nu există potriviri este rezultatul așteptat.')
ns=read(out/'T196_recalcul_arhiva.json')['results']
for i in [4,5,7,8,9,11,12,15]:
 k='T196-R2-'+str(i).zfill(3);z=[r for r in ns if r['criterion']==k];dv={4:'Instantaneele A1/B1 din iunie 2023 sunt identice.',5:'A2/B2 februarie 2023 sunt identice, FISE|2|2.',7:'Șase concepte × doi salariați, 12 rânduri nominale.',8:'A3/B3 sunt identice iar AJUSTARE_MANUALA_V crește exact 0→100.00.',9:'A0/A0b sunt identice. Nu reproducesc în această comparație instanța procesului, nota și mesajul.',11:'O notă CO, 10 linii; recomputarea independentă debit=credit 4601.00 și fotografia FACT|10|4601.00|4601.00.',12:'Cele două instantanee de note A4/B4 sunt identice octet cu octet.',15:'Pe ambele trasee, ieșirile de izolare înainte/după sunt identice.'}[i];add('T196',i,'H',dv,['T196_recalcul_arhiva.json'],'Am refăcut operația de comparație pe artefactele sursă; nu am rulat într-o clonă nouă clicurile sau butoanele originare.',z)
coord=out.parent/'T191/Dispozitii_T191.json'; assert H(coord.read_bytes())=='3677c4991dc18cc2e0bd4db3ac530c15cebb18df90072bce761cd95da057a6a8'
for r in read(coord)['rows']:
 k=r['criterion']; assert k in search
 cases[k]={'status':states['X'],'mesurat':r.get('actual'),'limita':r.get('scope_limit'),'subprobe':[r['scope_disposition']],'dovezi':[ref(coord)]}
def output():
 for k,r in search.items():
  if k not in cases:
   cases[k]={'status':states['D' if k in ar else 'N'],'mesurat':'A fost identificat obiectul Git original al raportului.' if k in ar else 'Nu există în acest lot o rulare exactă a scenariului.','limita':'Cazul rămâne deschis pentru intrarea și oracolul nominal de mai jos.','dovezi':[]}
  c=cases[k];c.update({'criterion':k,'task':r['task'],'canonical':r['project_task'],'historical_requirement':r['source']['text'],'entry_oracle_working_queue':r.get('next'),'historical_documents':ar.get(k,[]),'source_evidence_id':r['source'].get('source_evidence_id'),'source_position':r['source'].get('source_position')})
  if c['status']==states['D']:c['dovezi']=[ref('Index_istoric.json')]
 rr=[cases[k] for k in search]; counts=dict(collections.Counter(r['status'] for r in rr)); tasks={t:dict(collections.Counter(r['status'] for r in rr if r['task']==t)) for t in sorted({r['task'] for r in rr})}
 d={'utc':UTC(),'agent':'A03','sha':sha,'base_queue':ref(qr),'roster':len(rr),'summary':counts,'counts_by_task':tasks,'separated_T191':{'covered_by_coordinator':len(read(coord)['rows']),'total_in_queue':sum(r['task']=='T191' for r in rr),'evidence':ref(coord)},'source_readback':ref('Index_istoric.json'),'R4_unchanged':ref(rg4),'limits':['P reprezintă numai oracolul nominal din rând. F înseamnă că observația curentă nu satisface pragul nominal, fără atribuire automată ca defect de produs sau defect istoric.','Recalculul de instantaneu confirmă egalități și totaluri istorice, fără să reexecute intrarea ERP. Doar un fișier numit după un criteriu nu constituie test.','Cazurile T191 sunt preluate din raportul coordonatorului, 19/24 cazuri măsurate, niciun caz contabilizat încă o dată.','Nu a fost efectuată transmitere fiscală. Nu au fost rulate scripturi de test pe date ale unei firme productive.','Native SQL T256 și JAR pe fixture sunt distincte de generarea unei declarații din documente reale. Cele două cabinte folosite pentru instantaneele T196 aparțin dovezilor istorice.'],'r8':rr}
 return d
if __name__=='__main__':
 result=output();J(out/'Registru_A03_R8.json',result);f=out/'Registru_A03_R8.json';print(len(cases),result['summary'],H(f.read_bytes()))

