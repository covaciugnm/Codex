import json,hashlib,pathlib,datetime,collections
r=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
e=r/'executie'
o=e/'A11_reproduceri_lot1'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rub=read(r/'A11_rubrica_control.json')
i=read(o/'rapoarte_integritate.json')
l=e/'A11_ledger_651_fise.json'
led=read(l)
scores=read(pathlib.Path('C:/Users/User/AppData/Local/Temp/a11_lot1_matrix.json'))
ids=list(scores)
v={'schema':'eva.audit.a11.independent-control.lot1.v1','reviewer':'A11','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_bundle_sha256':'df251d54425833e941ddf85ddf0e376ed7f2fb20312702919956a0b582f3b397','cutoff_git_sha':'6df998aee0e514d30856c461962afe99ebd0d113','rubric_sha256':sha(r/'A11_rubrica_control.json'),'decision':'REVENIRE_OBLIGATORIE_R2','accepted_reports':0,'reviewed_reports':len(ids),'product_quality_score':None,'score_rule':'Câte 0,2 exclusiv pentru fiecare subcontrol satisfăcut integral în aria declarată, exact 50 pe raport. QC01-R4 apreciază registrul comun A12 verificat pentru toate zonele. Lipsa probelor nu dă punctaj, chiar când este raportată corect. Scorul acoperă probarea și calitatea raportului, nu calitatea software. Scorul global A12 măsoară procedura pentru 651 fișe; nu este media scorurilor fișelor.','reports':{},'task_ledger':{'file':l.name,'sha256':sha(l),'records':len(led['records']),'accepted_fully':led['accepted_fully'],'scores':led['score_histogram'],'semantic_and_integrity_results':led['totals'],'control_states':led['status_counts'],'details':'Toate fișele au dispoziție PARTIAL_DE_RELUAT. Toate cele 4004 fragmente au clasificare individuală în ledger; clasificarea conservatoare nu pretinde că fragmentele normative candidate sunt automat cerințe probate. 1953 PASS documentare înseamnă 3 controale de proveniență/structură per fișă. T227 este cazul cu 2,2/10, nu un flux de achiziție demonstrat.'}}
for z in ids:
 p=e/(z+'_raport.json'); rr=read(p); s=scores[z]; integ=i.get(z,{}); ref=integ.get('hash',led['source_sha256']); assert sha(p)==ref
 cc=[]
 for t,mask,note in zip(rub['criteria'],s['m'],s['n']):
  assert len(mask)==5
  q=[{'id':x['id'],'requirement':x['text'],'earned':int(b)*0.2} for x,b in zip(t['report_subchecks'],mask)]
  cc.append({'id':t['id'],'title':t['title'],'score':mask.count('1')/5,'subchecks':q,'adjudication':note,'evidence':([p.name+'#/controls',p.name+'#/findings',p.name+'#/pipelines','A11_reproduceri_lot1/rapoarte_integritate.json#/'+z] if z!='A12' else [p.name+'#/records',l.name+'#/records',l.name+'#/totals'])})
 n=sum(mask.count('1') for mask in s['m'])
 v['reports'][z]={'sha256':sha(p),'source_file':p.name,'quality_verdict':'PARȚIAL_DE_RELUAT','quality_score_10':n/5,'verified_subchecks':n,'of':50,'product_score':None,'integrity_and_coverage':(integ if z!='A12' else {'all_records_hashed':651,'source_admin_links_checked':1609,'historical_quotes_checked':2805}),'criterion_scores':cc,'mandatory_reaudit':s['a']}
v['independent_results']=[
 ['A01.F01','CONFIRMAT_FIXTURE','Înregistrare anonimă la cabinet existent: 201, apartenență manager persistată.','A01_P0_independent.json'],
 ['A01.F02','CONFIRMAT_FIXTURE','Membru A nu poate citi utilizatorii B (403); grant pe firma B persistat (201), can false→true, un rând activ.','A01_P0_independent.json'],
 ['A01.F04','CONFIRMAT_FIXTURE','Ordine inversată B apoi A, firmă/CUI comun, corp diferit și cheie identică: ambele 201, aceeași identitate, conținut B accesibil din A; CUI terț 403.','A01_P0_independent.json'],
 ['A01.F05','CONFIRMAT_FIXTURE','Pe același cabinet: read 200, logout-all 200, auth/me 401, read cu tokenul vechi 200, semnătură invalidă 401.','A01_P0_independent.json'],
 ['A01 suite','REPLAY_CORESPUNZĂTOR','62 aserțiuni, 28 divergente de la oracol, 11 scenarii FE; outputuri independente și fără efect extern. Nicio concluzie privind exploatarea efectivă în producție.','A01_rerun/fixture_results.json','A01_rerun/dom_fixture.json'],
 ['A02.F01/F02','CONFIRMATE_SQL','Extrase SQL reale executate în SQLite: 19+13 și rezervă globală 5 → 22 în loc de 27; fără rezervă 32. Stoc 19, comandă vânzare 2 și cumpărare 6 → 11 în loc de 17. Nu probează locking/plan PostgreSQL sau un rezultat E2E.','A02_A03_SQL_independent.json'],
 ['A03-F01','CONFIRMAT_SQL','Două scheme 125 și 29 în același client→un rezultat 154; control o singură schemă 125.','A02_A03_SQL_independent.json'],
 ['A03-F02','CONFIRMAT_NET_PARCIAL','Reconstrucție SQL pe aceleași clause ale metodei net: 97 și 31 produc -128 agregat în loc de -97 și -31. Alegerea și emiterea efectivă a jurnalului de către proces nu au fost executate.','A03_A05_supplemental.json'],
 ['A03-F04','CONFIRMAT_STOREFRONT_FIXTURE','Patru comenzi persistate în fixture Flask; 0,19 utilizat la separarea net în traseul testat. Regulă generală fiscală / întreg ERP / deploy necertificate.','A03_checkout_replay.json'],
 ['A04-F01','CONFIRMAT_CLASĂ_ȘI_JAR','Linii 8@31 și 6@53; 8/2→354, zero/2→106. Linie goală ori bad urmată de 2→2/6 și 380. Nu a fost creată o recepție / mișcare de stoc.','A04_NIR_frozen.log','A04_NIR_installed_JAR.log','A11Nir.java'],
 ['A04-F02/F03','CONFIRMATE_HELPER','Fixture auxiliar: coliziuni în reconciliere, DATE COMPLETE cu 1 sau 100 diferențe sau la eroare citire partener; la 101 false, control curat true. Nu este o constatare despre nucleul ERP.','A04_recon_fixture.json','A04_recon_verdict.json'],
 ['A04-F04/F05','CONFIRMATE_COMPONENTĂ','Poll fixture 401/404 și coliziune nume ZIP normalizate; rămâne browser/operator/deploy neexecutat.','A04_archive_fixture.json','A04_poll.jsonl'],
 ['A05-F01/F02/F03','CONFIRMATE_JAR_SEGMENT','JAR instalat, compilare proaspătă probe J02/J03/J04/J09/J10/J11: lot, tip PK și cantitate fracționară refuzate; aceeași notă 20→19→18 și 8 mișcări față de 4. Nu extrapolați la toate modurile native de producție/consum.','A05_WmsProbe_replay.txt'],
 ['A05-F08','REPRODUS_MODEL_CHEIE','În modelul constrângerii: arhivarea blochează duplicatul, redenumirea permite reutilizarea de alt ID. Executorul a observat rezultatul și cu REST seed; A11 a repetat doar modelul SQL.','A03_A05_supplemental.json'],
 ['A05-F10','DEZECHILIBRU_SEED_PROBAT_CAUZĂ_NEREPRODUSĂ','18/20 la activare suprapusă și 13/15→12/14 cu pereche stabilă, după evidența executorului. Timestamp de creare și -2 la +12 ms nu stabilesc ordinea commiturilor, nu identifică singure mecanismul cauzal.','../A05_raport.json#/findings'],
 ['A12','651_INDIVIDUAL','651 fișe, toate hashurile, pointerii și citările verificate. Criteriile generate din fragmente/metadate au fost respinse ca substitut al cerințelor probate.', '../A11_ledger_651_fise.json']]
v['independent_results_path_base']='executie/A11_reproduceri_lot1'
v['independent_evidence_manifest']={p.relative_to(o).as_posix():sha(p) for p in sorted(o.rglob('*')) if p.is_file()}
v['hard_blocker_assessment']=[
 ['HB01','A03 pointerul A05 este depășit; hashul vechi s-a identificat la A05/raport-r1.json. Versiunea este reconciliată de A11, corecție de raport R2 necesară. Nicio substituție tăcută.'],
 ['HB02','Registrul este reconciliat la 651/651. Nu se confundă exhaustivitatea registrului cu execuția tuturor cerințelor.'],
 ['HB03','Responsabilitățile există în plan. Acceptările bilaterale ale fluxurilor nu sunt complete în acest lot.'],
 ['HB04','ACTIV pentru toate cele șase rapoarte: dovezi obligatorii de UX, stări, persistență, rezultate interzone sau criterii individuale lipsesc.'],
 ['HB05','A12 trebuie să separe proveniența de criteriu atomic; nu s-au transformat cele 1953 controale documentare PASS în confirmări funcționale. Restul separă explicit nivelurile.'],
 ['HB06','Nicio contradicție ascunsă probată în aceste rapoarte; deciziile de politică multi-G1 și locatori din A05 sunt condiționale și se rejudecă pe cerință.'],
 ['HB07','Probele arată defecte A01 și A05. Defectul demonstrat nu descalifică singur auditul; rămân neprobate alte căi, roluri și scenarii concurente obligatorii.'],
 ['HB08','T227 și F09 seed nu sunt dovezi ale absenței generale din iDempiere; concluziile au fost limitate la corpusul/instalarea observate.'],
 ['HB09','ACTIV pentru A12: niciunul dintre cele 4004 fragmente nu are simultan statut și dovezi per criteriu; lipsesc legături semantice task→rezultat.'],
 ['HB10','Gate al planului precede execuția, executorii nu au acordat 10/10.'],
 ['HB11','Nicio închidere globală; controlele obligatorii neexecutate împiedică 10/10.'],
 ['HB12','A11 a rulat local, cu date sintetice. Capturi operaționale A05 sunt de tenant seed autorizat. Nu a fost identificată o scriere de producție în această revizie.'],
 ['HB13','2.805 citări verificate exact; problemă semantică de clasificare A12, nu probă de fabricare deliberată. A11 nu acceptă citarea ca dovadă funcțională.']]
v['retest_order']=['Prioritatea imediată a riscului produs: A01.F01/F02/F04/F05 – păstrați probele și supuneți responsabilului autorizat. Auditul nu a modificat codul sau configurația producției.','R2 executori: înghețați versiunile anterioare, închideți corecțiile de probă per raport, testați condițiile contrare.','R2 A12: 651 revizuiri semantice, integrarea nominală a A01–A10 și confirmarea diferențelor.','A11: rescorați aceleași 50 subcontroale pe fiecare hash nou, publicați diferențele și mențineți deschis orice rezultat obligatoriu neprobat.']
v['conclusion']='0/6 rapoarte și 0/651 fișe aprobate integral. Cele patru defecte P0 A01 au fost reproduse independent în mediu sintetic. Produsul nu primește scor global. Lotul acesta nu evaluează rapoartele A06–A10.'
assert len(led['records'])==651 and len(set(x['source_id'] for x in led['records']))==651
assert all(x['of']==50 and 0<x['quality_score_10']<10 for x in v['reports'].values())
file=e/'A11_control_lot1.json'
file.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('sha=',sha(file),'ledger=',sha(l),'scores=',[(z,x['quality_score_10']) for z,x in v['reports'].items()])
