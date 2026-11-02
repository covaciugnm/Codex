import pathlib,json,hashlib,datetime,collections
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
base=rd(E/'A11_control_lot1.json'); rubric=rd(R/'A11_rubrica_control.json');integ=rd(O/'zone_integrity.json');m=rd(O/'assessment_matrix.json')
def compact(v,n=330):return str(v or '')[:n]
def score(c):
 return [{'id':x['id'],'name':x['title'],'earned':mask.count('1')/5,'rationale':notes,'subchecks':[{'id':y['id'],'criterion':y['text'],'earned':int(bit)/5}for y,bit in zip(x['report_subchecks'],mask)]}for x,mask,notes in zip(rubric['criteria'],c['m'],c['n'])]
p={'reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_git_sha':'6df998aee0e514d30856c461962afe99ebd0d113','base_plan_manifest':'df251d54425833e941ddf85ddf0e376ed7f2fb20312702919956a0b582f3b397','rubric_sha256':h(R/'A11_rubrica_control.json'),'scores_for_reports_not_product':True,'decision':'RAPOARTE_PARȚIALE_PENTRU_REAUDITARE','reports':{}}
for z,v in m.items():
 ig=integ[z];q=rd(E/ig['path']);assert h(E/ig['path'])==ig['sha256']; c=score(v); n=sum(ms.count('1') for ms in v['m']);assert len(c)==10 and all(len(x['subchecks'])==5 for x in c)
 controls=[{'id':x.get('control_id') or x['id'],'reported_state':x.get('verdict_integral') or x.get('status'),'fully_accepted':(z=='A02' and x.get('verdict_integral')=='PASS'),'scope':compact(x.get('R2_coverage') or x.get('execution_coverage')or x.get('observed')),'remaining':compact(x.get('open_checks')or x.get('remaining_or_scope')or x.get('remaining'))}for x in q['controls']]
 pipes=[{'id':x.get('pipeline_id')or x['id'],'complete_business_chain_accepted':False,'scope':compact(x.get('steps_verified')or x.get('observed')or x.get('state_trace')),'remaining':compact(x.get('open_checks')or x.get('remaining')or x.get('bilateral_verdict'))}for x in q['pipelines']]
 f=[{'id':x.get('finding_id')or x.get('id'),'declared':x.get('disposition')or x.get('status'),'A11':t,'evidence':x.get('evidence')or x.get('evidence_ids')or []}for x,t in zip(q['findings'],v['f'])]; assert len(f)==len(q['findings'])
 p['reports'][z]={'report':ig['path'],'report_sha256':ig['sha256'],'previous_score':base['reports'][z]['quality_score_10'],'quality_score':n/5,'accepted_subchecks':n,'out_of':50,'criteria':c,'individual_controls':controls,'individual_pipelines':pipes,'findings':f,'replies_to_R1_review':v['q'],'mandatory_reaudit':v['actions'],'full_safer_assessment':'Existența unui segment sau a unei metode native nu echivalează cu toate stările terminale, toate rolurile sau toate taskurile istorice.','hash_checks':ig['sources_checked'],'hash_issues':ig['errors'],'implementation_score':None}
p['independent_reproduction']={'folder':'A11_reproduceri_zone_R2_B/','native_PG':{'proof':'pg_independent.json','findings':['A02.F08','A03-F01'],'observed':'Migratorul original alege 3 sau 17 după ordinea fizică de inserție; 54 din celălalt cabinet rămâne constant. Balanță nativă pentru 21101: 7802,38 agregat versus 4217,50 USD și 3584,88 EUR în scheme separate; baza clonată a fost ștearsă.'},'precision':['A11Precision.java','precision_git.txt','precision_installed.txt'],'zip':'a04_zip_recomputed.json: dry-run original FastAPI pe Linux-glob. Perechi de nume distincte: 2 rânduri; coliziune în ambele sensuri: 1 rând cu 200/dry_run_valid; traversal:400. Identitatea ERP/preflight și registrul sunt fixture, nu postare reală.','cross_file':'cross.json','saga_secondary_scope':'A03-F05 și A04-F06 provin din aceleași L8 și L12. Un efect tehnic demonstrat în sandbox; politica tratamentului schemei secundare rămâne decizie.','GL_scope':'Mesaj cu lei pentru EUR se referă la textul rezumatului și nu dovedește singur schimbarea monedei jurnalului.'}
p['hard_gates']={'HB01':'A03: 3 referințe dereferențiază astăzi alt SHA; nu se transferă drept credit la R2.','HB04':'Toate: probe necesare de rol, E2E și interfețe incomplete împiedică 10/10.','HB09':'Trasabilitatea către fișele A12 pe draft R4 trebuie reconciliată distinct în A03.','scope_external':'A02 necesită topologia comercială reală doar pentru impact live; majoritatea testelor de tranzacție/rol sunt sintetice și executabile. A03 necesită decizia de contabilitate și data/regimul aplicabil pentru o concluzie legală sau contabilă extrapolată. A04 are teste locale reale de recepții/plată/import, dar eficiența unui furnizor/curier real rămâne separată.'}
p['summary']={'reports':len(m),'score_table':{z:v['quality_score']for z,v in p['reports'].items()},'full_reports_accepted':0,'total_controls':sum(len(v['individual_controls'])for v in p['reports'].values()),'pipelines':sum(len(v['individual_pipelines'])for v in p['reports'].values()),'findings':sum(len(v['findings'])for v in p['reports'].values())}
out=E/'A11_control_zone_R2_lotB.json';wr(out,p);print(h(out),p['summary'])
p0=rd(E/'A11_control_zone_R2_lotA.json');sha={'A05':'3986fd91b4f4f5d5079fa0002c23f3e05b63b11ca1233e719f9af7ed0b6c27af','A06':'cc96c88240823f7a87c428f1ee8489a2377a094e8d6607613bc91ece2b0bc944','A09':'713657960dbd4bf998d4bab49de05213b4e665b01453b1c1baF5f6bfc0b70e91'.lower()}
out3={}
for z,bind in sha.items():
 file=E/'R3_zone'/z/(z+'_raport.json');assert h(file)==bind
 j=rd(file);rev=j['revision_consolidated'];assert h(E/rev['source'])==rev['source_sha256']==p0['frozen_reports'][z]['sha256'] and rev['independent_review_sha256']==h(E/'A11_control_zone_R2_lotA.json')
 for ef in rev['evidence']:
  f=ef.get('path')or ef.get('file');assert h(E/f)==ef['sha256'],f
 good=True
 if z in ['A05','A06']:
  needed={'A05-R2-F11':['A05-C15','A05-C20','A05-C24']} if z=='A05' else {'A06-F09':['A06-C09'],'A06-F10':['A06-C07']}
  for fid,nodes in needed.items():
   ff=next(x for x in j['findings'] if (x.get('finding_id')or x.get('id'))==fid)
   assert set(ff.get('controls') or ff.get('control_ids'))>=set(nodes)
   for node in nodes:
    cc=next(x for x in j['controls'] if (x.get('control_id')or x.get('id'))==node); assert fid in (cc.get('findings')or cc.get('finding_ids')or [])
 old=p0['frozen_reports'][z]; criteria=old['criteria'];inc=0
 if z in ['A05','A06']:
  target=next(x for x in criteria if x['id']=='QC10');sub=next(x for x in target['subchecks'] if x['id']=='QC10-R1'); assert sub['earned']==0;sub['earned']=0.2;target['earned']+=0.2;inc=1
  target['assessment']='R3 a închis corecția nominală de trasabilitate a constatărilor. Evaluarea reprodusă în R2 rămâne evaluarea segmentului funcțional.'
 out3[z]={'source':file.relative_to(E).as_posix(),'sha256':bind,'r2_sha':rev['source_sha256'],'R2_quality':old['quality_score_10'],'R3_quality':(old['quality_subchecks_awarded']+inc)/5,'criteria':criteria,'extra_evidence_file_count':len(rev['evidence']),'crosswalk_fixed':True,'new_full_business_chain_confirmed':False,'residual':rev['remaining'],'implementation_score':None}
out=E/'A11_control_consolidari_A05_A06_A09_R3.json';wr(out,{'reviewer':'A11','scope':'Consolidări R3 separate pe hash, recenzate în raport cu 50 subcontroale deja punctate. Nicio extindere la un flux nou integral validat.','reports':out3});print(h(out),[(z,v['R3_quality'])for z,v in out3.items()])

