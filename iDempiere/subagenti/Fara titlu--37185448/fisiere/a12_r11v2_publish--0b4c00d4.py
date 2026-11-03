from a12_r11v2_review import *
import shutil,html
from concurrent.futures import ThreadPoolExecutor
def check0(e):
 f=B/e['source_file'];j=source(f,e['source_sha256']);assert ptr(j,e['pointer'])is not None
for r in R.values():
 assert r['candidate']==head and r['git_oid']==d[r['path']]['git_object']and r['file_verdict']is None
 for e in r['evidence']:check0(e)
eligible=[x for x in tasks['rows']if x['in_R10']];assert len(eligible)==652 and len(cr)==2619
def check_task(row):
 p=B/row['R10_file'];assert sha(p)==row['R10_file_sha256'],row['technical'];return row['technical']
with ThreadPoolExecutor(max_workers=8)as ex:verified=list(ex.map(check_task,eligible))
by_crit=collections.defaultdict(list);by_task=collections.defaultdict(list)
for x in links:by_crit[x['criterion']].append(x['case']);by_task[x['task']].append(x['case'])
cm=[]
for i,r in enumerate(br['rows']):
 cm.append({'task':r['task'],'canonical':r['canonical'],'criterion':r['criterion'],'requirement_original':r['text'],'owner_prior':r['owner'],'baseline':{**ref(baseline),'pointer':'/rows/'+str(i)},'R10_result_historical':r['R10'],'R11_cases':sorted(set(by_crit[r['criterion']])),'R11_oracle_complete':r['criterion']in ['T201-R2-013','T201-R2-014'],'R11_task_closure':False,'R11_status':'OBSERVATIE_LA_SUBCONDITIA_EXPLICITA'if by_crit[r['criterion']]else'RECEPTIE_NOMINALA_R11_DESCHISA'})
tm=[]
chapters={}
for r in eligible:
 name=r['technical'];criteria=[x for x in cm if x['task']==name];assert len(criteria)==r['R10_criterion_count']
 tm.append({'task':name,'canonical':r['canonical'],'chapter':r['chapter'],'title':r['title'],'alias':r['alias_declared'],'tracker_snapshot':{'state':r['current_state'],'last_edit_as_declared':r['last_edit_as_declared'],'source':ref(ri),'pointer':'/rows/'+str(tasks['rows'].index(r))},'historical_dossier':{'file':r['R10_file'],'sha256':r['R10_file_sha256']},'R10_criteria_count':len(criteria),'R11_direct_cases':sorted(set(by_task[name])),'R11_linked_criteria':[c['criterion']for c in criteria if c['R11_cases']],'whole_task_current_verdict':None,'remaining':'Verificarea tuturor condițiilor și efectelor la versiunea R11.'})
 ch=chapters.setdefault(r['chapter'],{'chapter':r['chapter'],'tasks':0,'criteria':0,'with_R11_direct_observation':0,'linked_criteria':0,'fully_accepted_tasks':0})
 ch['tasks']+=1;ch['criteria']+=len(criteria);ch['with_R11_direct_observation']+=bool(by_task[name]);ch['linked_criteria']+=sum(bool(c['R11_cases'])for c in criteria)
plan12=P/'A12_inventar_si_receptie_v2.json';contracts=source(plan12)['bidirectional_transactional_cases'];exmap={'D01':['A01','A09'],'D02':['A08'],'D03':['A05'],'D04':[],'D05':['A06'],'D06':['A07'],'D07':['A04'],'D08':[],'D09':['A10'],'D10':['A08'],'D11':['A02','A09','A10'],'D12':['A07'],'D13':['A12'],'D14':[],'D15':['A03'],'D16':[],'D17':[]}
open_limits={'D01':'Ruta nativă cu doi utilizatori, două cabinete și sesiuni ZK, receptorul pe eroare și dreptul la firmă.','D02':'Cheia unică M_Product_ID CPP/CPA, două G1 și două G2 până la documente; persistența defectului magazinului este JSON.','D03':'MPPProductBOM/PO cu două sesiuni native, locatorul, cutia și 0,5h în G1 o singură dată, stornare și G3.','D04':'Combinații împărțite între canale și două G1, ordine persistente, rezervări și rollback la candidatul R11.','D05':'Roluri, proces Validez/EXCLUS/ROȘU nativ; același ID până la aviz și zero efect cross-client.','D06':'Document nativ pe aceeași comandă, AWB, încasare și confirmare pe canal; lotul A07 începe TRIMIS în fixture.','D07':'Selectarea/confirmarea SPV în ZK și PO, NIR, cost și restul importurilor; proba izolată măsoară afișarea și garda.','D08':'T329/T366 cu două scheme, Fact_Acct.ASI, rollback și concurență pe noul candidat.','D09':'Toate clasele oficiale T330 și sesiunea §61, build/OSGi complet; gărzile CLI au Docker și ceas simulate.','D10':'Canal eMAG/Trendyol, comisionar, administrare exclusiv ERP și intrarea normală până la starea serverului.','D11':'AD/schema pe upgrade nativ, client bootstrap cu rol, revizie bundle activă și restaurare.','D12':'Volum integral1/100/1000 și resurse; A07 măsoară selectarea lotului la2000/2001, cu identitate structurală.','D13':'Import SAGA real și balanță nativă la noul candidat; A12 validează comparatorul pe date sintetice.','D14':'Retur parțial simultan, RMA, recepție, credit și restituire pe aceeași cheie.','D15':'Proces complet GeneratorDeclaratie, stare EVA_Declaratie/AD_Attachment, date salariale și validarea legală.','D16':'Închidere lunară și balanță în două scheme, notă și drepturi la stornare pe candidat.','D17':'Dispozitiv WMS, scanare și roluri până la efectul persistent.'}
pipeline=[]
for i,c in enumerate(contracts):
 pipeline.append({'id':c['id'],'objective':c['objective'],'owner':c['owner'],'peer':c['peer'],'approved_contract':{**ref(plan12),'pointer':'/bidirectional_transactional_cases/'+str(i)},'available_executor_lots':exmap[c['id']],'scope':'PROBE_PARTIALE_ASOCIATE'if exmap[c['id']]else'PROBA_LANT_R11_DE_EXECUTAT','gap':open_limits[c['id']],'accepted_complete':False,'score':None})
stages={o:{'assigned_files':sum(r['owner']==o for r in R.values()),'static_scope_files':sum(r['owner']==o and r['axis']['static']!='UNVERIFIED'for r in R.values()),'content_inspected_files':sum(r['owner']==o and r['axis']['inspected']!='UNVERIFIED'for r in R.values()),'exercise_scope_files':sum(r['owner']==o and r['axis']['exercised']!='UNVERIFIED'for r in R.values()),'own_executor_distinct_files':len({r['path']for r in R.values()for e in r['evidence']if e['executor']==o}),'sealed_zone_received':True,'remaining':'Restul ramurilor și metodele native, frontend/rol și toate contractele complete.'}for o in sorted({r['owner']for r in R.values()})}
axis_counts={a:sum(r['axis'][a]!='UNVERIFIED'for r in R.values())for a in axes}
methods=V/'metoda';methods.mkdir(exist_ok=True)
for n in ['buildbase','ingest','tasklinks','review','publish']:
 src=Path(os.environ['TEMP'])/('a12_r11v2_'+n+'.py');dest=methods/src.name
 if not dest.exists():shutil.copyfile(src,dest)
rawout=V/'Registru_6709_val_02.jsonl.gz';assert not rawout.exists()
with rawout.open('wb')as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0)as out:
  for r in R.values():out.write((json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n').encode())
taskf=V/'Matrice_criterii_task_probe.json';save(taskf,{'utc':now(),'head':head,'task_population':652,'criterion_population':2619,'task_rows':tm,'criterion_rows':cm,'nominal_links':links,'cases':cases,'unassigned_or_context_only':unassigned,'notes':['R10 este etalon istoric și rămâne la propriul commit. R11 nu închide automat taskuri prin o probă componentă.','Nici stările API/task tracker, nici codul produsului nu au fost modificate.','Cheia comercială a taskului este numai cea din registrul capturat. Un ID canonic lipsă rămâne null.']})
pipe=V/'Contracte_17_si_capitole.json';save(pipe,{'utc':now(),'head':head,'contracts':pipeline,'chapters':list(chapters.values()),'ten_zones':stages,'unreviewed_task_associations':unassigned,'A11_partial_reviews':reviewcases})
ev=V/'Evenimente_val_02.json';save(ev,{'utc':now(),'head':head,'prior':ref(init),'events':events,'file_event_count':len(events),'distinct_file_count':len({e['file_id']for e in events}),'result':'Evenimentele de sintaxă, lectură, suite și efecte se numără pe axe distincte; nu sunt defecte diferite.'})
report=V/'Handoff_val_02.json';save(report,{'utc':now(),'head':head,'plan':ref(plan),'gate':ref(gate),'previous_handoff':ref(A/'Handoff_registru_val_01.json'),'register':ref(rawout),'task_matrix':ref(taskf),'contracts_and_chapters':ref(pipe),'events':ref(ev),'counts':{'technical_files':6709,'structure_or_format_checks':6683,'readable_text_without_formal_contract':26,'first_observation':sum(bool(r['evidence'])for r in R.values()),'files_by_axis':axis_counts,'fully_audited_files':0,'tasks':652,'criteria':2619,'criteria_with_direct_partial_observation':len(by_crit),'tasks_with_direct_observation':len(by_task),'new_events':len(events),'new_event_files':len({e['file_id']for e in events})},'zones':stages,'suite_v7':{'proof':ref(O/'Suite_originale_API_portal_v7/Rezultate_suite_originale.json'),'suite_count':55,'entries':suite_states,'call_passed':sum(x['stage_outcomes'].get('call::passed',0)for x in suite_states),'call_failed':sum(x['stage_outcomes'].get('call::failed',0)for x in suite_states),'diagnostic':'Fiecare nonzero/skip rămâne nominal; trierea erorilor de mediu/fixtură va avea recepție separată. Rularea suitei nu promite intrarea ERP nativă.'},'independent_lots':reviews,'whole_audit_score':None,'product_score':None,'manifest_receipts':manifest_receipts,'sources':[v for k,v in sorted(inputs.items())],'source_methods':[ref(f)for f in methods.glob('*.py')],'pipeline_complete':False,'remaining':'17 contracte complete sunt urmărite individual; 2.619 criterii păstrează etalonul și proba nominală. R11 este în curs, cu recepție independentă parțială.','scope':'Toate cele zece zone au predare sigilată. Fiecărui fișier îi sunt păstrate titularul, peer, executorul efectiv, proba, metoda și limitarea. Artefactele vechi sunt surse imuabile.'})
# Readback, pointer verification, identity and source preservation.
q=lines(rawout);assert len(q)==6709 and len({r['id']for r in q})==6709 and len({r['path']for r in q})==6709
assert sum(c['tasks']for c in chapters.values())==652 and sum(c['criteria']for c in chapters.values())==2619
for r in q:
 for e in r['evidence']:check0(e)
for v in inputs.values():assert sha(B/v['path'])==v['sha256'],v['path']
qa=V/'Verificare_val_02.json';save(qa,{'utc':now(),'register':ref(rawout),'report':ref(report),'input_manifest_members':sum(x['verified_members']for x in manifest_receipts),'task_sha_verified':len(verified),'evidence_edges_resolved':sum(len(r['evidence'])for r in q),'unique_files':len(q),'unique_tasks':len({r['task']for r in tm}),'unique_criteria':len({r['criterion']for r in cm}),'raw_sources_reverified':len(inputs),'issues':[],'scope':'Integritate/trasabilitate. Concluzia independentă asupra auditului rămâne la A11.'})
man=V/'MANIFEST_val_02.json';save(man,{'utc':now(),'head':head,'files':[ref(f)for f in sorted(V.rglob('*'))if f.is_file()and f!=man],'algorithm':'SHA256','self_reference':False})
print('REPORT',ref(report),'REG',ref(rawout),'MANIFEST',ref(man),'QA',ref(qa));print('counts',read(report)['counts'])

