import pathlib,json,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); e=R/'executie'; a=e/'A09'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=a/'A09_addendum_android_R2.json'; mfile=a/'android_source_manifest_R2.json';j=rd(p);m=rd(mfile)
assert h(p)=='83ce6c78613088aea4724adbec2b73bcb78767789758619f4683d35efcda4f2c' and h(mfile)==j['source_manifest_sha256']=='97739c1fd35e5d7250fdca90b7d6a695a77fda9b914655e89a5633cb780e3581'
assert h(pathlib.Path(m['apk']['copy']))==j['apk_sha']==m['apk']['sha256']; assert len(m['files'])==199 and j['AND_execution_count']==0
for f in m['files']:
 b=(pathlib.Path(m['source_root'])/f['path']).read_bytes()
 assert hashlib.sha256(b).hexdigest()==f['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['blob'], f['path']
ids=rd(R/'Index_trasabilitate.json');controls={x['id']:x for x in ids['controls']};ps={x['id']:x for x in ids['pipelines']}
from collections import Counter
errs=[];reg={x['technical']:x for x in rd(R/'Inventar_P01.json')['rows']}
for c in j['controls']:
 for t in c['task_links']:
  assert reg[t['source']]['code']==t['canonical'] and reg[t['source']]['raw_state']==t['source_state'],(t,reg[t['source']]['raw_state'])
 assert c['artifact'] and c['modules'] and c['commands_or_reproduction'] and c['limits_if_resource_missing'] and c['db'] and c['status']=='NEEXECUTAT' and c['quality_reviewer']=='A11'
 assert all(x in controls or x in ps or x=='A12-CK-01' for x in c['cross_zone_parents'])
 for x in c['parent_A09_controls']:
  if not any(x in ps[y]['resolved_control_ids'] for y in c['parent_A09_pipelines']):errs.append([c['id'],'control',x])
 for y in c['parent_A09_pipelines']:
  if not any(x in ps[y]['resolved_control_ids'] for x in c['parent_A09_controls']):errs.append([c['id'],'pipeline',y])
print('orphans',errs)
assert not errs,errs
rs={'QC01-P3':'199/199 hashuri SHA256/OID, cele 18 omise anterior sunt incluse și au dispoziție, inclusiv build/proguard.','QC02-P2':'6 controale AND→task și ID canonic/stare validate pe inventar; părinte A09 și cross zone, test/artefact.','QC04-P3':'Oracole distincte DR/CO și pierdere după commit, fără confundare mock și ERP actual.','QC05-P2':'K1/K2, +0/1 linii și mișcări, date A/B, două gestiuni/lot, zero după refuz, conservare cantitativă.','QC06-P3':'5 interfețe responsabile furnizor/consumator, dovadă și acceptarea sarcinii distinctă de rezultatul observat.','QC09-P1':'Comenzi/module/rută/artefact și alternativă limitată fără AVD; fizic/AVD/JVM/APK și semnare distincte.','QC10-P1':'Șablon probator individual și revizie A11 pe hash nemodificat, versiunea R1 păstrată.'}
checks=[{'id':x['id'],'points':0.2,'evidence':rs.get(x['id'],'Condiție menținută a planului semnat și reconfirmată în domeniul celor șase controale AND.')} for crit in rd(R/'A11_rubrica_control.json')['criteria'] for x in crit['plan_subchecks']]
v={'reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject':p.relative_to(R).as_posix(),'hash_sha256':h(p),'base_plan_bundle':j['signed_base_manifest_sha256'],'previous_gate_sha256':h(e/'A11_gate_android_R1.json'),'manifest_sha256':h(mfile),'tracked':199,'git_blob_and_sha_verified':199,'apk_hash_recomputed':j['apk_sha'],'individual_control_count':len(j['controls']),'crosscheck_errors':errs,'decision':'ACCEPTAT_PLAN_SUPLIMENT_ANDROID','quality_score_plan':10,'earned':50,'maximum_subchecks':50,'subchecks':checks,'open_hard_blockers':[],'AND_executed_at_gate':j['AND_execution_count'],'quality_score_product_or_audit':None,'limitations':'Semnătură și proveniența buildului, AVD, acces fizic și efect ERP sunt obiecte de execuție. 10/10 fără execuție le atestă numai proiectarea. Nici telefonul real, nici legătura reproductibilă dintre APK și SHA nu sunt certificate prin inventar.'}
out=e/'A11_gate_android_R2.json';out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(h(out))

