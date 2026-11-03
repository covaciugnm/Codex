from pathlib import Path
import json,hashlib,gzip,collections,zipfile,datetime,subprocess,tempfile,shutil
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';O=B/'A11/Val02_loturi'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
checks=[]
def ck(name,ok,detail=None):
 checks.append({'check':name,'ok':bool(ok),'detail':detail});assert ok,(name,detail)
specs=[('A09_Helper_corpus_lot02/MANIFEST_SHA256.json','23f5fa497a8f07b3b7654ccdd8de3227a6657a149cf94ce3aff3172d17de5018'),('A08_Helper_rapoarte_lot02/MANIFEST_A08_lot02.json','3dc9c882d755754b6ab7982d32dd8fb5f7e965d0fec99e10f242e82668012141'),('A09_Date_Masini_lot02/MANIFEST_SHA256.json','ff071b46603712874805c53a024d5d4f8fccf7fedd5fb988dfb338d17f5059db'),('A05_Nativ_lot02/MANIFEST_A05_Nativ_lot02.json','96d157f5b85a6eaab9aa99aa895931eebb88118789271db5cdc1068ef9eb2add'),('A05_Nativ_lot02/MANIFEST_reproducere_v1.json','3458ac7087d803a865400e4b8f4fbe1467e8e44683d00483be5a1014b8f1294e')]
manifest_counts={};manifests=[]
for rel,expected in specs:
 p=B/rel;ck(rel+' seal',h(p)==expected);o=j(p);rows=o.get('files') if isinstance(o.get('files'),list) else o.get('entries');ck(rel+' unique',len(rows)==len({x['path'] for x in rows}));manifest_counts[rel]=len(rows)
 for x in rows:
  target=p.parent/x['path'];ck(rel+' / '+x['path'],target.is_file() and h(target)==x['sha256'] and ('bytes' not in x or target.stat().st_size==x['bytes']))
 manifests.append(ref(p))
with gzip.open(R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf8') as f:catalog={x['path']:x for x in map(json.loads,f)}
sources={}
for rel in ['A09_Helper_corpus_lot02/sources','A08_Helper_rapoarte_lot02/Sources']:
 base=B/rel
 for p in base.rglob('*.py'):
  path=p.relative_to(base).as_posix();raw=p.read_bytes();ck('Git source '+rel+'/'+path,blob(raw)==catalog[path]['git_object'])
  if path in sources:ck('shared source same '+path,sources[path]['sha256']==h(p))
  sources[path]={'path':path,'git_object':blob(raw),'sha256':h(p),'local':str(p),'whole_file_acceptance':False}
a09=B/'A09_Helper_corpus_lot02';r09=j(a09/'results.json')['results']+j(a09/'results_supplement01.json')['results'];ids09=[x['case'] for x in r09]
ck('A09 67 unique case records',len(r09)==67 and len(set(ids09))==67)
for x in r09:
 p=a09/'cases'/x['case']/'result.json';ck('A09 result identity '+x['case'],j(p)==x)
 ck('A09 stable inputs '+x['case'],not x['changed_inputs'] and all(x['checks'].values()))
 with zipfile.ZipFile(p.parent/'synthetic_repository.zip') as z:
  for path in sources:
   if path in z.namelist():ck('A09 archive source '+x['case']+'/'+path,hashlib.sha256(z.read(path)).hexdigest()==sources[path]['sha256'])
a08=B/'A08_Helper_rapoarte_lot02';r08=sum([j(a08/f)['cases'] for f in ['Results.json','Results_supplement01.json','Results_supplement02.json']],[]);ids08=[x['id'] for x in r08]
ck('A08 54 unique case records',len(r08)==54 and len(set(ids08))==54)
invocations=0
for x in r08:
 p=a08/'Cases'/x['id']/'result.json';ck('A08 result identity '+x['id'],j(p)==x)
 if 'steps' in x:invocations+=len(x['steps'])
 else:invocations+=1
 for side in ['fixture_before.zip','fixture_after.zip']:
  zpath=p.parent/side
  if zpath.exists():
   with zipfile.ZipFile(zpath) as z:
    for path in sources:
     if path in z.namelist():ck('A08 '+side+' source '+x['id']+'/'+path,hashlib.sha256(z.read(path)).hexdigest()==sources[path]['sha256'])
ck('A08 58 top-level CLI',invocations==58,invocations)
children=[]
for case,expected in [('C14_manual_child_observed',2),('C15_fisa_child_observed',0)]:
 with zipfile.ZipFile(a08/'Cases'/case/'fixture_after.zip') as z:
  matches=[x for x in z.namelist() if x.endswith('_audit_child_results.jsonl')];ck(case+' child log exists',len(matches)==1)
  rows=[json.loads(x) for x in z.read(matches[0]).decode('utf8').splitlines()];children.append({'case':case,'rows':rows})
  ck(case+' child failure direct',len(rows)==1 and 'FileNotFoundError' in str(rows) and any(v==1 for v in rows[0].values()))
  report=[x for x in z.namelist() if x.endswith('81_audit_texte_lot1.md')];ck(case+' report persists',len(report)==1)
  ck(case+' OK count',z.read(report[0]).decode('utf8').count('| OK |')==expected)
mas=B/'A09_Date_Masini_lot02'
for name in ['WSagaMasiniForm.java','WSagaCrudForm.java']:
 p=mas/name;path='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/form/'+name;ck('Mașini source '+name,blob(p.read_bytes())==catalog[path]['git_object']);sources[path]={'path':path,'git_object':blob(p.read_bytes()),'sha256':h(p),'whole_file_acceptance':False}
ck('Mașini Git installed class identical',(mas/'Git_WSagaMasiniForm.class').read_bytes()==(mas/'Installed_WSagaMasiniForm.class').read_bytes())
native=B/'A05_Nativ_lot02';stdout=(native/'bootstrap_attempt5_po.stdout.txt').read_text();po=j(native/'Recitire_independenta_PO.json');q={x['name']:x for x in po['queries']}
ck('Native exact duplicate cause','AdempiereException' in stdout and 'm_product_value' in stdout and 'already exists' in stdout)
ck('Native rows semantic',len(q['products']['rows'])==2 and {r[0] for r in q['products']['rows']}=={'1000001','1000002'} and all(r[-2:]==['11','11'] for r in q['products']['rows']))
ck('Native rollback and duplicate',q['rollback']['rows']==[[0]] and q['duplicate']['rows']==[[1]])
ck('Native retry and prefix',q['products']['rows'][0][2]=='A05 retry after rollback succeeded' and po['prefix'] in stdout)
ck('Native permissive build explicit',q['build']['rows']==[['2026-03-09','${env.ADEMPIERE_VERSION} 20080428-1232','N']])
ann=j(native/'Anexa_reproducere_v1.json');active={l.split('|')[1] for l in stdout.splitlines() if l.startswith('ACTIVE_END|')};ck('Native 19 active vs 6 explicit',active=={x['symbolic_name'] for x in ann['actual_active_bundles']} and len(active)==19 and len(ann['minimum_explicit_start_sequence'])==6)
for x in ann['actual_active_bundles']:
 p=Path(x['path']);ck('Native active binary '+x['symbolic_name'],p.is_file() and h(p)==x['sha256'] and blob(p.read_bytes())==x['oid_computed'])
# Exact native source anchor; no native Java execution inferred from this read.
manual=Path('D:/CodexWork/a12-r11-p01/repo/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/ajutor/ManualEvA.java');path='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/ajutor/ManualEvA.java';ck('Native chapter invariant OID',blob(manual.read_bytes())==catalog[path]['git_object']);lines=manual.read_text(encoding='utf8').splitlines();anchor={'path':path,'git_object':blob(manual.read_bytes()),'sha256':h(manual),'lines':[{'line':i+1,'text':l} for i,l in enumerate(lines) if 'un singur capitol pe ecran' in l]};ck('Native chapter invariant exists',any(x['line']==2821 for x in anchor['lines']))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','manifest_counts':manifest_counts,'manifests':manifests,'source_identities':list(sources.values()),'A09':{'cases':67,'by_instrument':dict(collections.Counter(x['instrument'] for x in r09))},'A08':{'cases':54,'top_level_cli':invocations,'case_ids':ids08,'direct_failed_children':children},'native_chapter_invariant':anchor,'checks':checks,'check_count':len(checks),'all_ok':all(x['ok'] for x in checks),'meaning':'Rehash/reconciliere ale probelor, nu număr de teste de produs ori criterii îndeplinite.'}
p=O/'Reconciliere_A11_loturi_Val02_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'path':str(p),'sha256':h(p),'checks':len(checks),'manifests':manifest_counts},ensure_ascii=False))
