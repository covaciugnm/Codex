from readgit import *
from datetime import datetime,timezone
out=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R8_pregatire/A06_oracole');out.mkdir(exist_ok=True);assert not list(out.iterdir()),'Preserve immutable supplement'
audit=out.parents[2];idx=out.parent/'Index_883_relectura_surse.json';queue=json.loads(idx.read_text(encoding='utf8'))['records']
reg=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/Documentatie/echipa-2026-10-09/00_STATUS_TASKURI.json')
srcroot=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102');pr='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab'
regb=reg.read_bytes();assert hashlib.sha1(b'blob '+str(len(regb)).encode()+b'\0'+regb).hexdigest()=='2c022d178bb94f0a52d74ab16172f0aa59474c6c'
cap=audit/'capturi/00_STATUS_TASKURI.json'; capjd=json.loads(cap.read_text(encoding='utf-8-sig'));jd=json.loads(regb);lst=listing(roots);ats=json.loads((w/'actual.json').read_text(encoding='utf8'))
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def linesrec(folder,name,lines,quote=None):
 path,oid=next((p,o) for p,o in lst if p.endswith('/'+name) and folder in p and p.count('/')==3);data=get(path,oid);assert data is not None,path
 source=data.decode('utf-8-sig').splitlines()
 cuts=[]
 for n in lines:
  l=source[n-1]
  if quote and quote in l:
   i=l.index(quote); excerpt=l[max(0,i-15):i+265]
  else:excerpt=l[:510]
  cuts.append({'line':n,'line_sha256':hashlib.sha256(l.encode()).hexdigest(),'excerpt':excerpt})
 return {'path':path,'git_oid':oid,'sha256':hashlib.sha256(data).hexdigest(),'lines':cuts}
def anch(rel,pattern):
 path=srcroot/rel;lines=path.read_text(encoding='utf8').splitlines()
 return dict(path=rel,line=next(i for i,v in enumerate(lines,1) if pattern in v),pattern=pattern,sha256=H(path))
t22='T22-flux-';t35='T35-cadru-'
family={
 'K07':('T22.07-R2-001',103,'Bulinele operaționale la începutul și închiderea reconcilierii',[linesrec(t22,'00_cerinta_proprietar.md',[4],'bulina rosie'),linesrec(t22,'06_manager_plan_v2.md',[25,563,566,567]),linesrec(t22,'09_auditor_verdict_plan_v2.md',[28])],[anch(pr+'/corelare/CazFlux.java','static String bulinaInceput('),anch(pr+'/corelare/CazFlux.java','static String bulinaFinal(')],'C05/C18 trebuie să fie roșii la început chiar dacă baza este verde; C26 este martor verde. Pentru un caz configurat ca închis cu încasări legate se admite |DIF|≤0,01; peste 0,01 sau dacă lipsește legătura rămâne roșu.','Au fost exercitate codul de culoare și condiția de închidere, nu tabelul redat pe ecran, toate cele 26 de cazuri, agregările sau culorile vizuale/etichetele accesibile.'),
 'K09':('T22.09-R2-001',105,'Identificatorul documentului și legătura pe pagina individuală',[linesrec(t22,'00_cerinta_proprietar.md',[4],'pagina de comanda individuala'),linesrec(t22,'06_manager_plan_v2.md',[64,65,145,596,597],'fereastră nouă')],[anch(pr+'/corelare/RaportFluxComenzi.java','static Legatura zoom('),anch(pr+'/corelare/RaportFluxComenzi.java','Record_UU="+') if False else anch(pr+'/corelare/RaportFluxComenzi.java','&Record_UU='),anch(pr+'/corelare/RaportFluxComenzi.java','target=\\"_blank\\"'),anch(pr+'/form/PanouFluxComenzi.java','window.open(')],'Factura validă are link iDempiere Zoom către C_Invoice și Record_UU corect. UUID absent sau malformed nu generează legătură. HTML-ul paginii trebuie să trimită într-o fereastră nouă; suitei actuale îi corespunde o factură FV-77, 121,00 și un link URL distinct.','Autorul istoric cere pagina pentru operator; «client web»/comisionar nu e un rol documentat în acea propoziție. Helperul validează forma UUID, nu apartenența la cabinet ori permisiunea pentru document. Nu s-a făcut click și nu s-a demonstrat autorizarea la destinație.'),
 'K08':('T22.08-R2-001',104,'Proveniența prețului din fișa pe canal',[linesrec(t22,'74k_arhitect_spec_v3_faza_K.md',[569,571,574],'valoarea efectivă'),linesrec(t22,'66g_auditor_verdict_plan_addendum_K_erata.md',[92],'EFECTIVĂ')],[anch(pr+'/corelare/TabelaFisaCanal.java','static ValoareEfectiva valoareEfectiva('),anch(pr+'/corelare/FisaCanalCalcul.java','static String valoareModificata(')],'Câmp PRET_VANZARE. Baza iDempiere 121,00; aplicarea −10% dă 108,90. Nicio suprascriere → IDEMPIERE; suprascriere de platformă fără valoare de canal → PLATFORMA; valoare explicită 100,00 pe canal → CANAL; spațiile albe pe canal lasă activă valoarea platformei.','Cerința inițială solicită analiză mai amplă de câmpuri, fotografii, dimensiuni, certificate și proprietari. Această subprobă privește un singur câmp și calculul în memorie; nu dovedește fișa UI sau publicarea externă.'),
 'K35':('T35-R2-001',230,'Activare, permisiune de scriere și izolare firmă',[linesrec(t35,'00_cerinta_proprietar.md',[6],'bifa de activare'),linesrec(t35,'04_manager_plan.md',[590],'altă firmă')],[anch(pr+'/corelare/PlatformeVanzari.java','static String scrierePermisa(RandPoarta')],'Fișă proprie activă+Scriere permisă Y+capabilitate FISA → fără motiv de refuz. Aceeași fișă citită ca alt client → alta_firma; fișa dezactivată → inactiva; N → scriere_nepermisa. Este poarta unității înainte de expeditor.','Nu s-au apelat servicii, nici nu s-a citit/introdus o cheie. Nu sunt probate UI pentru setări, toate platformele, criptarea secretului, transportul, autorizarea unui utilizator real sau izolarea a două baze fizice.')}
records=[]
for k,(criterion,n,title,historical,anchors,oracle,limit) in family.items():
 pos=next(r for r in queue if r['criterion']==criterion);assert pos['position']==f'/{n}/cerere_proprietar';assert jd[n]['id']==pos['task'] and capjd[n]['cerere_proprietar']==jd[n]['cerere_proprietar'] and capjd[n]['id']==pos['task']
 probes=[]
 for run in [rr for rr in ats if rr['suite']=='OracleProbe']:
  ss=[dict(input=z[1],expected=z[2],actual=z[3],matched=z[4]=='true') for z in run['observations'] if z[0]==k]
  assert ss and all(z['matched'] for z in ss)
  probes.append({'jar':run['jar'],'jar_sha256':run['jar_sha256'],'producer_source_sha256':run['source_sha256'],'jvm_exit':run['run_return'],'rows':ss})
 rec={'case_id':k,'criterion_id':criterion,'task':pos['task'],'title':title,'original_R7/R8_queue_record':pos,'registry_source':{'path':'Documentatie/echipa-2026-10-09/00_STATUS_TASKURI.json','git_oid':'2c022d178bb94f0a52d74ab16172f0aa59474c6c','sha256':H(reg),'json_pointer':pos['position'],'captured_registry_sha256':H(cap),'captured_pointer_matches_criterion':True,'literal':jd[n]['cerere_proprietar']},'historical_support_at_frozen_sha':historical,'historical_evidence_class':'Cerință și documentație istorică (nu probe de execuție la data închiderii).','recoverable_expected':oracle,'product_sources':anchors,'production_tests_here':'none','actual_component_runs':probes,'classification':'ETALON_RECUPERAT_PENTRU_SUBCONDIȚIE; COMPONENTĂ_EXERCITATĂ; CRITERIUL_TOTAL_PARȚIAL','unrecovered_or_unexecuted':limit}
 if k=='K09':
  rec['fixture_page']=[{x:r[x] for x in ['jar','jar_sha256','suite','source_sha256','compile_return','run_return','stdout_sha256','ok_lines','fail_lines','observations']} for r in ats if r['suite']=='TestT22Pagina']
  assert all(y['ok_lines']==33 and y['run_return']==0 and any('target="_blank"' in t for t in y['observations']) for y in rec['fixture_page'])
 records.append(rec)
date=datetime.now(timezone.utc).isoformat()
report={'schema':'A06.R8.independent_recovered_suboracles.v1','date_utc':date,'code_sha':sha,'parent_queue_sha256':H(idx),'scope':'Exact 4 criterii din coada nominală 883, trei din capitolul T22 și unul T35. Etalon recuperat și exercitat doar pentru subcondițiile enumerate. Nu se modifică înregistrările R1–R8 sau verdictele A12/A11.','archive_protocol':'Recuperare locală fără rețea: tree Git la SHA fixat, bloburi din arhivă gzip sau preexistente în Git, SHA-1 blob Git = hash(header blob+octeți). S-au verificat rândurile de registru și contexte de plan/spec primare. Fragmentele sunt scurte, rândul complet este identificat prin SHA-256.','runtime_protocol':'JDK 21, cele două JAR concrete cu aceeași suită offline. Driverul nominal e inclus integral. TestT22Pagina și dependența sa TestT22Flux din copia de cod au fost compilate pentru fiecare JAR; TestT22Flux nu a fost executat ca suită independentă. Nu se atestă zero modificări istorice prin trecerea unei aserțiuni actuale.','contracts':records,'raw_run_evidence':ats,'harness_source':(w/'OracleProbe.java').read_text(encoding='utf8'),'run_recipe':(w/'exec-tests.py').read_text(encoding='utf8'),'input_gloss':'K07 6, K09 3, K08 5, K35 4 aserțiuni nominale pe JAR. TestT22Pagina are 33 verificări pe JAR, din care sunt izolate probele de HTML/link. Acestea nu devin 33 criterii noi și nici 8 cazuri funcționale.','case_count':len(records),'unique_R7_criteria':len({r['criterion_id'] for r in records}),'whole_criteria_promoted':0,'user_interfaces_or_ERPs_modified':0,'score':None,'independent_reviewer':'A11'}
fn=out/'Raport_oracole_A06.json'; fn.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
manifest={'schema':'A06.R8.oracle_manifest.v1','date_utc':date,'git':sha,'signed_file':fn.name,'sha256':H(fn),'file_bytes':fn.stat().st_size,'nominal_case_ids':[x['case_id'] for x in records],'case_count':4,'primary_queue_sha256':H(idx),'r1_to_r8_unchanged':True,'scope':'Manifestul semnează raportul final cu tot codul și rezultatele incluse. Manifestul nu își include propriul hash.'}
mf=out/'Manifest_oracole_A06.json';mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(fn,H(fn),mf,H(mf))

