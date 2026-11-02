from a12_r6_exec import *
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
import html
from concurrent.futures import ThreadPoolExecutor
R=E/'R6';R5=E/'R5';Prep=E/'R6_pregatire';R.mkdir(exist_ok=True)
for fld in ['taskuri','fise_html','probe','metoda']:(R/fld).mkdir(exist_ok=True)
sha5=sha(R5/'A12_raport.json');assert sha5=='ec00d36e6ee2eb4755981e22c0c332279b8319cb58080f535e6879de44de97cd';assert sha(E/'A11_control_A12_R5.json')=='8c88ca705968761dd0217a887462a76df906561a7aceff9e284ed3d2a9a5813c'
parent=rd(R5/'A12_raport.json');ced=rd(R5/'Dovezi_criterii.json');ev=ced['evidence'];reverse=defaultdict(list);cases=defaultdict(list)
@lru_cache(maxsize=4096)
def sh(p):return sha(p)
@lru_cache(maxsize=256)
def read(p):return rd(p)
def digbytes(bb):return hashlib.sha256(bb).hexdigest()
def jc(v):return digbytes(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def ptr(v,t):
 for a in t[1:].split('/') if t else []:
  k=a.replace('~1','/').replace('~0','~');v=v[int(k)]if isinstance(v,list)else v[k]
 return v
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def add(cid,file,point,expected,actual,scope,layer,disp='SUBCAZ_MĂSURAT',hist=False,textline=False,datum=None):
 p=Path(file);rel=p.relative_to(B).as_posix();loc=({'kind':'text-line','line':point,'line_sha256':digbytes(p.read_text(encoding='utf-8-sig',errors='replace').splitlines()[point-1].encode())}if textline else {'kind':'json-pointer','pointer':point,'canonical_value_sha256':jc(ptr(read(p),point))});key='EV6-'+jc([rel,point,layer])[:22];assert expected is not None
 ev[key]={'level':layer,'source':rel,'sha_or_oid':sh(p),'pointer':point if not textline else None,'line':point if textline else None,'strict_primary_locators':[loc],'content_or_observation':actual,'limit':scope}
 cases[cid].append({'evidence':key,'layer':layer,'asserted_expected':expected,'measured':actual,'data_or_actor':datum,'result':disp,'remaining_scope':scope,'closure_phase':hist});return key
OR=Prep/'A12/Oracole_487_EV5.json';orows=rd(OR)['rows'];om={q['r5_id']:(i,q)for i,q in enumerate(orows)}
for eid,(i,d)in om.items():
 ev[eid]['R6_oracle_locator']={'source':OR.relative_to(B).as_posix(),'sha256':sh(OR),'pointer':'/rows/'+str(i),'canonical_value_sha256':jc(d),'status':d['numeric_basis'],'automatic_conformity':False}
comparison=Prep/'A12/Contraste_108_R5.json';contr={q['criterion']:(i,q)for i,q in enumerate(rd(comparison)['records'])}
an=Prep/'Anexe/Anexe_nominale_R5.json';anr=rd(an)['rows']; ax={r['criterion']:r for r in anr}
@lru_cache(maxsize=768)
def blob(oid):
 for p in [D/'blobs'/(oid+'.gz'),Path('D:/CodexWork/p01-r6-annex')/(oid+'.gz')]:
  if p.is_file():
   b=gzip.decompress(p.read_bytes());assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;return b.decode('utf-8-sig',errors='replace').splitlines()
 raise KeyError(oid)
ind=[]
for a in anr:
 row=[]
 for v in a['anchors']:
  oid=v['blob_oid'];n=v['line'];ls=blob(oid);lit=ls[n-1];assert digbytes(lit.encode())==v['line_text_sha256'],(a['criterion'],oid,n)
  row.append({**v,'original_nominal_line':lit,'nearby_delineation_if_material':ls[max(0,n-2):min(len(ls),n+1)],'read_as':'Există combinația de entitate/control din anexă la linia reprodusă. Afirmația ori scorul istoric nu constituie execuție actuală.'})
 ind.append({'criterion':a['criterion'],'task':a['task'],'search_result':a['status_search_only'],'original_source':a['original_source'],'historical_controls':row,'no_runtime_credit_from_annex':True})
wr(R/'probe/Anexe_1611_pentru_fisa.json',{'source_hash':sh(an),'records':ind});ar={x['criterion']:(i,x)for i,x in enumerate(ind)}
aux=Prep/'A12';hp=Prep/'Istoric/T110_T111_documentar.json';hp2=Prep/'Istoric/Provenienta_si_evenimente_nominale.json'
add('T110-R3-001',hp,'/T110','524 funcții iDempiere, corespondent SAGA și decizie individuală.', '524 rânduri ale foii confruntate cu CSV A73; 524/524 identități, nume și tipuri în exportul q31 și în citirea GardenWorld.','Corespondența documentară și găurile din planul implementării se păstrează separat de execuția ERP.','DOCUMENT_PRIMARY','DOMENIU_DOCUMENTAR_CONFIRMAT',True)
add('T111-R3-001',hp,'/T111','378 funcții, 227 module, fiecare cu beneficiu explicat.','378 perechi unice și 227 module, până la 244 lacune/partial din care 152 au toate trei câmpurile planificate completate peste o liniuță. Alte 92 au cel puțin un câmp barem fără conținut.','Catalogul nu are o coloană beneficiu separată, iar G254, G301, G376 descriu doar inactivitatea/nefolosirea. Nu se demonstrează 378 explicații de beneficiu.','DOCUMENT_PRIMARY','ARITMETICĂ_CONFIRMATĂ_SEMANTICĂ_INCOMPLETĂ',True)
for i,f in enumerate(rd(hp2)['new_nominal_observations']):
 add(f['technical']+'-R2-002',hp2,'/new_nominal_observations/'+str(i),'Eveniment nominal de anulare și legătură de lineage, separat de oră exactă a portalului.',f['event_time']+' · '+f['related_predecessor_or_successor_named']+' · linia '+str(f['event_row']),'Limita superioară a primei constatări, nu data exactă a tranziției.','REGISTRU_ISTORIC','LIMITĂ_TEMPORALĂ_STRÂNSĂ',True)
jp=aux/'T03_concurenta_JobFundal.json'
for i,q in enumerate(rd(jp)['rows']):
 expect='1 acceptat / 1 rând ulterior' if 'bypass'not in q['scenario']and 'rollback'not in q['scenario']else ('2 acceptați / 2 rânduri pe mutant'if'bypass'in q['scenario']else '0 după rollback, 1 după reluare')
 add('T03-R2-039',jp,'/rows/'+str(i),expect,{'target':q['target'],'scenario':q['scenario'],'decision':q['simultaneous_after_barrier'],'after':q['witness_rows_after_first_two_trx'],'final':q['final_rows']},q['limit'],'GUARDĂ_PRODUS_ȘI_DOUĂ_TRANZACȚII','MARTOR_CONCURENȚĂ'if'bypass'not in q['scenario']else'MUTANT_DETECTAT',datum=q['two_pg_sessions_before'])
for n,cycle in [('T06_proces_direct_GardenWorld.json','inițială'),('T06_proces_direct_GardenWorld_schema_completa.json','schema corectată')]:
 q=aux/n;d=rd(q);assert all(v['removed']for v in d['removed'])
 for i,f in enumerate(d['runs']):
  nm=f['case'];ex={'range_invalid':'Parametrii incompatibili refuzați și delta 0','unknown_bank':'Cont inexistent/neaparținând firmei refuzat și delta 0','missing_summary':'REZUMAT_11 lipsă și delta 0','foreign_archive':'CUI diferit → refuz specific cui_diferit fără scriere','unreadable_archive':'Fișier nevizitabil SQLite → refuz de arhivă ilizibilă cu clasa excepției și fără scriere'}[nm];limit='La momentul probei existau 0 rânduri în GardenWorld; nu se reconstituie populația istorică de 168. În varianta CUI străin s-a oprit la o precondiție anterioară: niciuna dintre probe nu a observat cui_diferit.'
  for cid in {'range_invalid':['T06-R2-008'],'unknown_bank':['T06-R2-008'],'missing_summary':['T06-R2-009'],'foreign_archive':['T06-R2-008','T06-R2-020'],'unreadable_archive':['T06-R2-008','T06-R2-021']}[nm]:
   add(cid,q,'/runs/'+str(i),ex,f['response'],limit,'PROCES_NATIV_REST_GARDENWORLD','PRECONDIȚIE_NESATISFĂCUTĂ'if nm=='foreign_archive'else 'REFUZ_NATIV_ȘI_DELTA_ZERO',datum={'actor':'GardenAdmin/102, GardenWorld 11','state':cycle,'before':f['client11_before'],'after':f['client11_after']})
def attach_mtags(cid,fname,query,target,limit,rel,count=None):
 p=aux/fname if not isinstance(fname,Path)else fname;ls=p.read_text(encoding='utf-8-sig',errors='replace').splitlines();hits=[(i,ln.strip())for i,ln in enumerate(ls,1)if re.search(query,ln,re.I)]
 if count is not None:assert len(hits)==count,(cid,fname,query,len(hits),count)
 for i,line in hits:add(cid,p,i,target,line,limit,rel,textline=True)
jcal=aux/'JVM_calibrat_r6_final.json';job=rd(jcal)
for z in ('git','instalat'):
 for cid,rx,exp in [('T159-R2-007',r'^\s*OK\s+refuz: 44 chei','44 chei inexistente → ParametruFiscalLipsa'),('T159-R2-013',r'^\s*OK\s+an fiscal: (?:luna 12|exercițiul încheiat)','Luna 12 ca pe revizia inițială; luna 6 → 25 decembrie.'),('T159-R2-007',r'^\s*OK\s+LC-1: 61 mutanți','61 variații registru; detectare prin cel puțin un caz de paritate')]:attach_mtags(cid,z+'_TestT159LotA.log',rx,exp,'Unitate țintă cu registru injectat, fără declarație fiscală transmisă.','JVM_COLECTAT')
 attach_mtags('T159-R2-056',z+'_TestT159LotE.log',r'^\s*OK\s+.*(?:refuz|registru|paritate|ValidFrom)','Lotul E verifică rata/registrul și refuzul la lipsă prin teste, iar HTTP backend se probează separat.','Fixtura Java folosește sursa fiscală injectată; nu răspunde rețelei fiscale.','JVM_WEBSHOP')
 attach_mtags('T06-R2-010',z+'_TestComparatieSagaEcran.log',r'^\s*OK\s+E-[1-8]:','8 din 8 controale statice ale formei.','Test sursă și modele de prezentare; nu este navigare în ecran.','JVM_VERIFICARE_STATICĂ',8)
 attach_mtags('T323-R2-002',z+'_TestLocatiiMultiple.log',r'^\s*OK\s+L[1-7](?:\s|[.:])','Fiecare dintre L1–L7 trebuie să transporte locatorul ales; ASI și documentul persistent necesită și dovadă nativă.','Probe pe bytecode și căi declarate din JAR; nu înseamnă șapte documente scrise în ERP.','JVM_TRASABILITATE_LOCATOR')
 attach_mtags('T314-R2-006','final_'+z+'_TestT314Meniu_martor.log',r'^\s*OK\s+T314-inlucru(?:\s|\.d15)','14 frunze în lucru; țintele 24, 25 și 43 au ecran.','Test original cu normalizare Windows a locației pentru javap, fără schimbare de predicat. Meniul este compilat din sursa Git.','JVM_THEME')
 attach_mtags('T204-R2-005','final_'+z+'_TestT204Ecrane_martor.log',r'^OK C-2: 19/19 situri','19/19 surse de grilă vizibilă.','Același predicate original cu jurnalizare a reușitelor; fără browser.','JVM_UI_COMPONENT')
 attach_mtags('T204-R2-016','final_'+z+'_TestT204Ecrane_martor.log',r'^OK C-13.*(?:dreptul fals|dreptul permis)','Refuz t29.tip.drept_raport, iar rolul permis generează CSV.','Metoda de imprimare și rol injectat; captura de dialog rămâne separată.','JVM_UI_ROL')
 for m in ['M01','M02','M03']:attach_mtags('T204-R2-005','final_'+z+'_TestT204Ecrane_'+m+'.log',r'^FAIL C-2: 18/19','Mutantul original '+m+' este detectat.','18/19 față de 19/19 pe martor. Aceleași trei mutații pe două JAR-uri, nu șase mutații distincte.','MUTANT_UI_COMPONENT',1)
 attach_mtags('T190-R2-007',R5/('calibrare/'+z+'_TestReges.log'),r'^\s*OK\s+T190 lărgire','Fiecare din cele 8 valori din tabelul C-4 are efectul determinat în sursa testului.','Extinderea acoperă cele șapte ramuri nelegate în R5. 8 vectori × două JAR-uri; sursa logurilor este anterioară R6.','JVM_8_VECTORI',8)
 for cid,fn,regex,exp in [('T325-R2-016','TestPutaway','T27 procesele prin fabrica','Clasele de proces prin fabrică; instanța ERP este cerută separat.'),('T326-R2-039','TestListaPicking','T13 deGenerat|T34 legătura','true/true/false și ordinea apelului privind livrarea.'),('T330-R2-021','TestFefo','t329.refuz.tenant|firma nedeterminată|două firme|client 0','Două firme izolate și cheia exactă t329.refuz.tenant.')]:
  attach_mtags(cid,R5/('calibrare/'+z+'_'+fn+'.log'),regex,exp,'R5 păstrează și eșecurile de mediu inițiale; rezultatul acestei reluări nu produce o tranzacție ERP.','RELECTURĂ_LOG_ORIGINAL')
 for nm,rx in [('TestT29Catalog','REZULTAT'),('TestT29Acoperire','REZULTAT'),('TestAjutor','REZULTAT'),('TestT28Meniu','REZULTAT')]:attach_mtags('T163-R2-029',z+'_'+nm+'.log',rx,'0 FAIL în suita nominală; numărul istoric de ecrane verificat separat.','Git și JAR instalat au rezultate diferite la două suite. Nu transfera un rezultat global de Git la instalare sau la montarea istorică.','JVM_SUITA_NOMINALĂ')
loc=aux/'T323_nou_vector_alegere.json'
for i,x in enumerate(rd(loc)['results']):add('T323-R2-002',loc,'/results/'+str(i),'4 alegeri (a doua locație, altă gestiune, 0, negativ) și 5 refuzuri/permisiuni pe tenant/activitate.',str(x['target'])+' exit='+str(x['exit']),rd(loc)['claim'],'JVM_REGULĂ_INDEPENDENTĂ',datum=x['raw'])
fisc=aux/'T159_test_matrice.json'
for i,x in enumerate(rd(fisc)['mutations']):add('T159-R2-056',fisc,'/mutations/'+str(i),'Martor 0 cod; variantele silent-fallback și prioritate inversată trebuie ucise de testele originale.',{'variant':x['variant'],'rc':x['returncode'],'observation':x['observations']},'TestClient FastAPI, SQLite sintetic și sursă fiscală injectată. Fără tranzacție iDempiere.','TEST_BACKEND_FISCAL')
attach_mtags('T159-R2-056',aux/'T159_backend_pytest.log',r'::(?:test_ruta_get_si_refuz_422|test_ruta_doar_citire|test_valoare_registru_alt_decat_seed_si_refuz).*PASSED','GET 200 pentru CAS 0,25, GET 422 pentru cheia lipsă; scrierile POST/PUT/PATCH/DELETE sunt refuzate.','Este conftest-ul oficial pe SQLite; nu certifică autorizarea sau disponibilitatea partenerilor în instalarea reală.','PYTEST_SUITĂ_NOMINALĂ')
p=aux/'T204_T330_citire_documentara_exacta.json'
for cid in rd(p):add(cid,p,'/'+cid,'T204 intersecție în cele 26 = 0' if cid.startswith('T204')else 'O linie în COORDONARE_SESIUNI.md.',rd(p)[cid],rd(p)[cid]['limit'],'GIT_DOCUMENTAR_ACTUAL','ȚINTĂ_DOCUMENTARĂ_OBSERVATĂ')
p=aux/'Probe_istorice_recalibrate.json'
for k in ['T191_baseline','T191_remove_mapping']:add('T191-R2-014',p,'/'+k,'48 chei și 0/0 pe martor; eliminarea unui rând produce 1/1 și exit 1.',rd(p)[k],'Validează matricea documentară caz+mutant; zero scrieri de produs pentru fiecare dintre cele 48 chei rămâne separat.','SCRIPT_DOCUMENTAR_MARTOR_MUTANT')
for cid,fields in [('T329-R2-016',['K1','K15','K17'])]:
 for z in ('git','instalat'):attach_mtags(cid,z+'_TestLoturi.log',r'^\s*OK\s+.*(?:K15|K17|K1[^0-9])','Căile K1–K17 trebuie purtate sau refuzate; K15 cere verificarea nativă cu/bazat pe ASI.','Metoda de test nu dovedește documentul contabil la 10,00 pentru interfața nativă.','JVM_APELURI_LOT')
# Scope of native chain never credited to T337 disabled. The physical chain is attached to explicitly matching verbs, not to whole WMS.
native=E/'Reverificare_Flux_S1_aviz_retur_R6.json'
if native.is_file():
 assert sh(native)=='1a2e23d14bd8a85105153e2ca951290f712bea83b6a6936bdbfcf7122d026033'
 w=rd(native)
 for i,row in enumerate(w['stages']):
  if 'before pick; dismantled CPP' in row['stage']:add('T338-R2-004',native,'/stages/'+str(i),'Pregătirea comenzii presupune pick pe locator, după desfacerea setului dacă este nevoie.',{'stage':row['stage'],'g2':row['g2_lot_locator_recipe']},'Context nativ operațional, fără a confirma ecranele Android A9–A11. T337 oprit în această configurație; nota G2 nu are o legătură SO demonstrată, fără dovadă pentru manoperă.','ERP_TRASABILITATE_CONTEXT','CONTEXT_NATIV')
p=aux/'Metadate_13_selectii.json'
for i,z in enumerate(rd(p)['rows']):
 add(z['criterion'],p,'/rows/'+str(i),z['expected_subcontrol'],z['actual'],'Un SELECT pe clona restaurată nu substituie procesul sau ecranul cerut. Pentru EVA_StarePornire, relația exactă și înregistrarea dicționarului sunt absente din bază.','METADATE_NOMINALE','SONDĂ_DICTȚIONAR')
for target in ('git','instalat'):
 attach_mtags('T27.36-R4-001',R5/('calibrare/'+target+'_TestT27eHarta.log'),r'^\s*(?:OK\s+H4\.[145]|FAIL\s+H5 D(?:101|112|300))','Harta publică categorii, iar validatoarele nominale trebuie prezente în locul prevăzut în plan.','Datele proiectului și clasele sunt testate; DUK în /duk/lib era absent în mediul local. Nu descrie ce vede utilizatorul în ZK.','JVM_HARTA_DECLARAȚII')
pgext=Prep/'Calibrare_SQL/Reluare_T22_T155.json'
if pgext.is_file():
 assert sh(pgext)=='242778c6376a5977ca129c54516392f00d5f51c45bb2ea1951ebccd66ae6aaf7'
 for i,s in enumerate(rd(pgext)['runs']):
  if s['suite']=='TestT22MetaSql':cid='T22-R2-001';parts=[4,5];expect='Uniqueness în cadrul firmei și păstrarea istoricului comenzii. Verificarea funcției de corelare trebuie urmărită la succesorul T216.';lim='Regulile unice de staging nu dovedșc conversia în C_Order, factura, plata sau execuția la data administrativă de agregare.'
  else:cid='T155-R2-002';parts=[6,7,8,9,10];expect='Detectorul distinge note existente/neechilibrate, documentele nemarcate și stările din fixtura de 18 tabele.';lim='Detectarea unui document fără notă nu îl postează. Balanța debitor/creditor la deschidere și tratarea tuturor operațiunilor ERP nu rezultă din această probă.'
  for j in parts:add(cid,pgext,'/runs/'+str(i)+'/pg/markers/'+str(j),expect,s['pg']['markers'][j],lim,'SQL_TEST_ORIGINAL',datum=s['target'])
wr(R/'probe/Cazuri_noi.json',{'rows':dict(cases),'count':sum(map(len,cases.values()))})

