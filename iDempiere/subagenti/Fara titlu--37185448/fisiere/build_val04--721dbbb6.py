from pathlib import Path
import json,gzip,hashlib,datetime,copy,collections
from concurrent.futures import ThreadPoolExecutor
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=B/'executie/R11_fisiere';V=O/'A12/Val_04';PREV=O/'A12/Val_03'
HEAD='2fe90ed3f128c33dff7cf9f8674e664a70679390';inputs={};cache={};events=[];manifest_receipts=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(B).as_posix()
def ref(p,pt=None):
 r={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if pt is not None:r['pointer']=pt
 return r
def source(p,h=None):
 p=Path(p);k=rel(p)
 if k not in cache:
  data=p.read_bytes();inputs[k]={'path':k,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
  cache[k]=json.loads(data.decode('utf-8-sig'))if p.suffix=='.json'else data
 if h:assert inputs[k]['sha256']==h,(k,h,inputs[k]['sha256'])
 return cache[k]
def ptr(j,p):
 if p=='':return j
 assert p.startswith('/')
 for t in p[1:].split('/'):
  t=t.replace('~1','/').replace('~0','~');j=j[int(t)]if isinstance(j,list)else j[t]
 return j
def save(n,j):
 p=V/n;assert not p.exists(),p;p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return p
def manifest(p,h):
 j=source(p,h)
 fs=j.get('files',j.get('artifact_hashes'))
 for f in fs:
  target=B/f['path']if 'path'in f else p.parent/f['file']
  assert sha(target)==f['sha256'],str(target)
 manifest_receipts.append({'manifest':ref(p),'members_verified':len(fs)})
 return j
manifest(PREV/'MANIFEST_val_03.json','2847558d5416f9c2c2f032e81da37163627498cd56aeda38716ce18bf49f1579')
prior=source(PREV/'Handoff_val_03.json','9758e95a4ff7d84b0fe384b48b5af3f3a2b640ff9cf6afcdba8bb6418ccbd02e')
reg=B/prior['register']['path'];raw=source(reg,prior['register']['sha256'])
R={r['path']:r for r in map(json.loads,gzip.decompress(raw).decode().splitlines())};assert len(R)==6709
matrix=copy.deepcopy(source(B/prior['task_matrix']['path'],prior['task_matrix']['sha256']))
contracts=copy.deepcopy(source(B/prior['contracts']['path'],prior['contracts']['sha256']))
prev_suites=source(B/prior['suites']['path'],prior['suites']['sha256'])
previous_A11=O/'A11/Verdict_A11_R11_val03_v1.json';source(previous_A11,'95593bbc0888f0963ae25c7cb93077565749be3ee75c5320702f7ef910219d57')
ui_file=O/'Triaj_fixture_UI_Val03/Raport_triaj_UI_config.json';ui=source(ui_file,'1883de0e10f2df684b01a533a06e312dd419e9563e4ca35b1a1d1cc06a427c91')
err_file=O/'Triaj_fixture_UI_Val03/Erata_metoda_V12_V13.json';err=source(err_file,'a8494f398054f834098cf55f5746454c75fe3102cd73ff6a7b293c6164cd57c7')
be_file=O/'Backend_extindere_Val04/Raport_8_suite_backend.json';be=source(be_file,'ae5b78278759cbfafe2b16540fcb25557613059d7bd691b2cbc2cb70eb47e297')
hr_file=O/'HR_izolare_Val03/Raport_A01_HR_Val03.json';hr=source(hr_file,'74c131c5dc149f380910759655afd16299018c8e40b175eb56011afe67e0a629')
manifest(hr_file.parent/'Manifest_HR_Val03.json','3f864b9d65d40a96c368b78627634af0930710859aa43ce8c05390b0454773fc')
for k in ['suite_receipt','source_manifest','help_receipt','help_screenshot']:
 q=ui[k];source(B/q['path'],q['sha256'])
for k in ['source_receipts','source_manifests']:
 for q in be[k]:source(B/q['path'],q['sha256'])
source(O/'HR_izolare_Val03/actors.json',hr['results']['independent_auth_matrix']['sha256'])
origf=hr_file.parent/hr['results']['original_tests']['file'];orig=source(origf,hr['results']['original_tests']['sha256'])
assert len(orig['cases'])==3 and all(c['outcome']=='passed'for c in orig['cases'])
def add(path,f,pt,executor,axes,scope,observed,limit):
 assert path in R,path;ptr(source(f),pt)
 event={'executor':executor,'source_file':rel(f),'source_sha256':inputs[rel(f)]['sha256'],'pointer':pt,'scope':scope,'result':observed,'axes':axes,'limits_and_own_axis_values':limit,'candidate':HEAD}
 event['event_id']='R11V4-'+hashlib.sha256(json.dumps(event,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]
 assert not any(e.get('event_id')==event['event_id']for e in R[path]['evidence'])
 R[path]['evidence'].append(event)
 for a in axes:R[path]['axis'][a]='OBSERVED_ONLY_AT_LINKED_SCOPE'
 R[path]['qualifying_executor']=sorted({x['executor']for x in R[path]['evidence']})
 events.append({**event,'path':path,'file_id':R[path]['id'],'git_oid':R[path]['git_oid']})
selected={}
for i,s in enumerate(prev_suites['rows']):
 selected[s['file']]={'file':s['file'],'git_oid':s['git_oid'],'sha256':s['source_sha256'],'prior_val03':ref(B/prior['suites']['path'],'/rows/'+str(i)),'current_origin':s['original_receipt'],
 'selected_events':[{'event':copy.deepcopy(e),'provenance':{**s['original_receipt'],'pointer':s['original_receipt']['pointer']+'/cases/'+str(n)}}for n,e in enumerate(s['reported_events_original'])],
 'latest_whole_program_exit':s['exit'],'whole_program_snapshot_provenance':s['original_receipt'],'mixed_selective_rerun':False,'new_program':False,
 'effective_scope':s['effective_classification'],'semantic_limit':s['limit'],'history':[s['original_receipt']],'whole_functional_acceptance':False}
def newrow(file,f,idx,r,new,limit):
 assert file in R
 cases=r.get('cases',[])
 out={'file':file,'git_oid':R[file]['git_oid'],'sha256':r.get('source_sha256'),'current_origin':ref(f,'/rows/'+str(idx)),
 'selected_events':[{'event':copy.deepcopy(e),'provenance':ref(f,'/rows/'+str(idx)+'/cases/'+str(n))}for n,e in enumerate(cases)],
 'latest_whole_program_exit':r['returncode'],'whole_program_snapshot_provenance':ref(f,'/rows/'+str(idx)),
 'mixed_selective_rerun':False,'new_program':new,'effective_scope':'OBSERVATIE_COMPONENTA_ORIGINALA','semantic_limit':limit,
 'history':selected[file]['history']+[ref(f,'/rows/'+str(idx))]if file in selected else[ref(f,'/rows/'+str(idx))],
 'whole_functional_acceptance':False}
 if file in selected:out['prior_val03']=selected[file]['prior_val03']
 return out
uif=B/ui['suite_receipt']['path'];uir=source(uif,ui['suite_receipt']['sha256'])
assert len(uir['rows'])==7
for i,r in enumerate(uir['rows']):
 name=r['file'];assert name in selected
 selected[name]=newrow(name,uif,i,r,False,'Auth și backend țintă simulate; configurare JSON sintetică. '+err['correct_method'])
 add(name,uif,'/rows/'+str(i),'COORDONATOR',['exercised'],'Suita originală reluată pe fixture explicită; înlocuiește observația anterioară, nu se cumulează.',{'exit':r['returncode'],'events':r.get('cases',[])},err['correct_method'])
newfiles=[]
for i,rec in enumerate(be['records']):
 name=rec['file'];assert name not in selected and R[name]['git_oid']==rec['git_oid'];newfiles.append(name)
 f=B/rec['receipt']['path'];rr=source(f,rec['receipt']['sha256'])
 matches=[(k,x)for k,x in enumerate(rr['rows'])if x['file']==name];assert len(matches)==1
 k,r=matches[0];selected[name]=newrow(name,f,k,r,True,rec['limit']+' '+err['correct_method'])
 selected[name]['sha256']=rec['sha256']
 add(name,f,'/rows/'+str(k),'COORDONATOR',['exercised'],'Sursă test nouă în corpusul celor63 suite; aserțiuni originale pe componentă.',rec['result'],{'native_boundary':rec['normal_path_and_native_boundary'],'limit':rec['limit'],'method':err['correct_method']})
assert len(newfiles)==8 and len(selected)==63
# Replace exactly three old failing event observations; never pretend the two HR suites were fully rerun.
hr_substitutions=[]
for i,c in enumerate(orig['cases']):
 name='backend/'+c['id'].split('::')[0];s=selected[name]
 match=[(k,x)for k,x in enumerate(s['selected_events'])if x['event']['id']==c['id']and x['event']['stage']==c['stage']]
 assert len(match)==1
 k,old=match[0];assert old['event']['outcome']=='failed'
 current={'event':copy.deepcopy(c),'provenance':ref(origf,'/cases/'+str(i))}
 s['selected_events'][k]=current;s['mixed_selective_rerun']=True;s['history'].append(ref(origf,'/cases/'+str(i)))
 s['effective_scope']='COMPOZIT_V7_CU_REPROBA_A_3_CAZURI_HR;FARA_RERULARE_INTEGRALA'
 s['selective_rerun_limit']='Cel mai recent exit al întregii suite rămâne cel V7; trei semnale sunt înlocuite nominal cu proba HR. Cele27 cereri ASGI sunt separat, nu aici.'
 hr_substitutions.append({'file':name,'before':old,'after':current,'unchanged_remaining_suite_observations':True})
 add(name,origf,'/cases/'+str(i),'A01',['exercised'],'Numai proba originală HR nominală reluată, nu întreaga suită.',c,hr['limits'])
# UI source attribution: CSS/KB are consumed/read, not executable business logic.
ui_dynamic={'frontend/app.py','frontend/static/eva-help.js','frontend/storefront/app/cms.py','frontend/storefront/app/factory.py','frontend/storefront/templates/themes/generic/product.html'}
for i,r in enumerate(ui['file_records']):
 name=r['path'];assert R[name]['git_oid']==r['git_oid']
 ax=['inspected']+(['exercised']if name in ui_dynamic else[])
 add(name,ui_file,'/file_records/'+str(i),'COORDONATOR',ax,'Numai rutele/fragmentele și efectele descrise în fișă; nu întreg fișierul.',{'observations':r['observations'],'result':r['result'],'persistent_effect':r['persistent_effect']},r['limit'])
hr_dynamic={'backend/app/routers/hr.py','backend/app/routers/hr_payroll.py','backend/app/hr_payroll/service.py','backend/app/idempiere/tenant_authz.py','backend/app/idempiere/readdb.py','backend/app/idempiere/perms.py','backend/app/auth.py'}
for i,r in enumerate(hr['sources']):
 name=r['path'];assert R[name]['git_oid']==r['oid']
 add(name,hr_file,'/sources/'+str(i),'A01',['inspected'],'Identitate sursă HR la commit, fără a considera orice import executat.',r,'Funcțiile exercitate sunt legate separat la cele trei pipeline-uri; celelalte surse sunt suport.')
 if name in hr_dynamic:
  pidx=0 if name in {'backend/app/idempiere/tenant_authz.py','backend/app/idempiere/readdb.py','backend/app/auth.py','backend/app/routers/hr.py'}else 1 if name in {'backend/app/routers/hr_payroll.py','backend/app/hr_payroll/service.py'}else 2
  add(name,hr_file,'/pipelines/'+str(pidx),'A01',['exercised'],'Funcția/ruta nominală ASGI cu context real și PG sintetic; mirror ERP rămâne mock.',hr['pipelines'][pidx],hr['limits'])
for o in ui['observations']:
 matrix['unassigned_or_context_only'].append({'case':o['id'],'proof':ref(ui_file,'/observations/'+str(ui['observations'].index(o))),'disposition':'Legătură funcțională demonstrată; ID de criteriu contractual al taskului nu este demonstrat prin nume/tema fișierului.','whole_task_credit':False})
matrix['unassigned_or_context_only'].append({'case':'A01.HR.Val03','proof':ref(hr_file,'/nominal_requirement'),'disposition':hr['nominal_requirement']['canonical_caution'],'whole_task_credit':False})
# Existing criterion C67: all four named suite sources observed, separately.
criteria={c['criterion']:c for c in matrix['criterion_rows']};c67=criteria['T58-R2-077']
names=['backend/tests/test_t58_close_month.py','backend/tests/test_t32_l6j_rute.py','backend/tests/test_t32_l6h_citiri.py','backend/tests/test_error_catalog.py']
c67rows=[]
for n in names:
 s=selected[n];evs=s['selected_events']
 assert all(e['event']['outcome']=='passed'for e in evs)and s['latest_whole_program_exit']==0
 c67rows.append({'file':n,'program':s['current_origin'],'observed_call_passed_events':len(evs),'native_execution':False})
assert [r['observed_call_passed_events']for r in c67rows]==[36,29,234,11]
caseid='R11V4.T58.C67.FOUR_SUITES'
case={'case':caseid,'criteria':['T58-R2-077'],'proofs':[ref(be_file,'/T58_C67')]+[r['program']for r in c67rows],
 'files':[{'path':n,'id':R[n]['id'],'git_oid':R[n]['git_oid'],'owner':R[n]['owner'],'peer':R[n]['peer']}for n in names],
 'actor':'Actorii sintetici ai fiecărei suite originale; contexte/SQLite independente.',
 'entry_native_or_adapter':'Patru suite originale rulate separat în fixture noi; clientul/contextul ERP dublate în originale.',
 'expected_for_this_case':c67['requirement_original'],'observed':{'suite_rows':c67rows,'call_passed_events':310,'call_failed_events':0},
 'positive':'Succes/refuz/idempotency/AuditEvent în T58,29 rute l6j,234 citiri l6h și11 catalog erori.',
 'negative':'Contraexemplele originale pentru token lipsă/firmă străină/refuz păstrate. Unele citiri l6h acceptă500; nu se transferă drept succes ERP.',
 'limitation':['Nu a fost rulată comanda comună cu patru suite în aceeași instanță; sursele/fixturele și execuțiile separate sunt păstrate.','Nu certifică procesul nativ, ZK, Fact_Acct sau contractul D16.','Asocierea nouă este la același criteriu C67, nu creează criteriu/task suplimentar.'],
 'result_at_scope':'PATRU_SUITE_NOMINALE_OBSERVATE_SEPARAT','whole_task_verdict':None,'complete_pipeline':False}
matrix['cases'].append(case);c67['R11_cases'].append(caseid);c67['Val04_gap_update']='Suita l6j_rute anterior lipsă are acum29/29. Toate4 sursele cerute au execuții separate; comanda comună nu a fost reprodusă.'
matrix['nominal_links'].append({'case':caseid,'task':'T58','canonical':None,'criterion':'T58-R2-077','expected_original':c67['requirement_original'],'normative_record':c67['baseline'],'proofs':case['proofs'],'result_in_R11':case['result_at_scope'],'claim':'Componentele tuturor celor4 suite originale, executate separat.','limit':case['limitation'],'previous_R10_result':c67['R10_result_historical'],'R10_is_current_verdict':False})
for old in matrix['cases']:
 if old['case']=='R11V3.T58.C-67':old['Val04_successor_scope_note']='Afirmația lipsei l6j era valabilă la Val03; vezi R11V4.T58.C67.FOUR_SUITES pentru completarea probei, fără rescrierea istoriei.'
print('PREPARED',len(selected),'suite files',len(events),'file events',len(hr_substitutions),'HR case substitutions')
a05f=O/'A05/Val_04/Raport_A05_native_Val04_v2.json';a05=source(a05f,'59d93db99e533308dac179e60218d6add0b0c775497804edc037b305f20ea6f7')
manifest(a05f.parent/'MANIFEST_A05_Val04_v2.json','97a25752bd69ddefe96faf17c6a19cf1bb6b35277edaaa1acd7b4dfc68168af3')
cont='idempiere/plugins/com.eva.ro.contab/'
for i,r in enumerate(a05['source_trace']):
 name=cont+'src/com/eva/ro/contab/'+r['file'];assert R[name]['id']==r['file_id']and R[name]['git_oid']==r['oid']
 q=r['source_artifact'];data=source(B/q['path'],q['sha256']);assert hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==r['oid']
 lines=data.decode('utf8').splitlines();assert all(0<n<=len(lines)for n in r['anchor_lines'])
 add(name,a05f,'/source_trace/'+str(i),'A05',['inspected'],'Lectura traseului nativ și a ancorei; fără PO complet sau nouă execuție concurentă.',r['result'],r['limit'])
compfile=a05f.parent/'Comparatie_clase_montate.json';comp=source(compfile,'35e243a64ddbaf5fd92aa9f898ed9d7bf0c17c4f5b186db80614dd405ef14308')
for i,r in enumerate(comp['rows']):
 name=cont+'src/'+r['class'].split('$')[0].replace('.class','')+'.java'
 assert r['identical']and r['git_jar_class_sha256']==r['mounted_jar_class_sha256']
 add(name,compfile,'/rows/'+str(i),'A05',['bindingVerified'],'Identitate bytecode între JAR Git și JAR montat pentru clasa precisă.',r,comp['scope'])
native_refs=a05['native_source_records'];assert len(native_refs)==7
for ca in matrix['cases']:
 if ca['case']=='A05.G2.BOM.CONCURRENCY':
  ca['Val04_binding_and_source_only']=[ref(a05f,'/source_trace'),ref(compfile),ref(a05f,'/native_findings')]
  ca['Val04_native_limit']='4 cazuri beforeSave numai cu gettere sintetice; nu PO.saveEx, UI, Fact_Acct ori cursă persistentă nouă. Cele7 surse native sunt inventar suplimentar separat.'
for link in matrix['nominal_links']:
 if link['case']=='A05.G2.BOM.CONCURRENCY':link['Val04_binding_only']=[ref(a05f,'/source_trace'),ref(compfile)]
phase=collections.Counter();typed=collections.Counter()
for s in selected.values():
 for e in s['selected_events']:
  r=e['event'];phase[r['stage']+'|'+r['outcome']]+=1;typed[r.get('report_type','UNKNOWN_LEGACY')+'|'+r['outcome']]+=1
print('CURRENT_EVENT_COUNTS',dict(phase),'TYPED',dict(typed),'WHOLE_PROGRAM_SNAPSHOTS',dict(collections.Counter(s['latest_whole_program_exit']for s in selected.values())))
sm=source(B/ui['source_manifest']['path'],ui['source_manifest']['sha256']);smmap={r['file']:r for r in sm['rows']}
for name,s in selected.items():
 assert smmap[name]['git_blob']==s['git_oid']==R[name]['git_oid']
 s['sha256']=smmap[name]['sha256']
 s['source_manifest']=ref(B/ui['source_manifest']['path'],'/rows/'+str(sm['rows'].index(smmap[name])))

