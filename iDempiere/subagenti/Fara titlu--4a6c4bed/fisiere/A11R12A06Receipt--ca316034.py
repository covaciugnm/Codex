import json,hashlib,zipfile,re,datetime,shutil
from pathlib import Path
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';D=B/'A06_T343_instrumente_lot03';O=B/'A11/Val03_loturi'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
checks=[]
def ck(label,ok,detail=None):checks.append({'check':label,'ok':bool(ok),'detail':detail})
def save(n,obj):
 p=O/n;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':h(p)}
mf=D/'MANIFEST_A06_lot03.json';ck('manifest SHA',h(mf)=='5743839e4a93c1cb2d7e61b010081668693ea1ae4f4fcae388876b96d1a319fe');m=read(mf)
for e in m['files']:ck('artifact '+e['path'],h(D/e['path'])==e['sha256'] and (D/e['path']).stat().st_size==e['bytes'])
ck('82 artifacts unique',len(m['files'])==len({e['path'] for e in m['files']})==82)
report=read(D/'Raport_A06_lot03.json');ck('report SHA',h(D/'Raport_A06_lot03.json')=='c702618cdc4b3fb50da9886cb24bf7407553446a28ea9efd17a4f6e92d3b37b8')
for s in read(D/'Sources.json'):
 raw=(D/'sources'/Path(s['path']).name).read_bytes();ck('source '+s['path'],hashlib.sha256(raw).hexdigest()==s['sha256'] and blob(raw)==s['git_object'])
rows=read(D/'Results.json');supp=read(D/'Supplement_case.json');rows2=rows+[supp];cases={x['id']:x for x in rows2};ck('all records unique',len(cases)==len(rows2))
for ident,count in [('I14',18),('I15',8),('I16',10)]:
 expected=[x for x in cases if x.startswith(ident+'_')];ck(ident+' count',len(expected)==count)
 claimed=next(x['case_ids'] for x in report['files'] if x['control'].endswith(ident));ck(ident+' exact membership',set(claimed)==set(expected))
ck('two boundary cases',len([x for x in cases if x.startswith('BOUNDARY_')])==2)
for name in ['I16_complete','I16_only_control','I16_stale_fail']:ck(name+' accepted comparator',cases[name]['rc']==0 and 'mutanti=OK' in cases[name]['stdout'])
for name in ['I16_duplicate_control','I16_empty','I16_no_log_fail','I16_unknown_live','I16_not_run']:ck(name+' negative',cases[name]['rc']!=0)
ck('I15 setup classified UCIS ERROR',cases['I15_setup']['rc']==0 and 'UCIS (ERROR' in cases['I15_setup']['stdout'])
phase=read(D/'Pytest_phase_oracles.json');ck('pytest phase rc', {k:v['rc'] for k,v in phase.items()}=={'pass':0,'assert':1,'setup':1,'collect':2,'empty':5})
ck('setup never reached body', 'ERROR at setup' in phase['setup']['stdout'] and 'synthetic setup error' in phase['setup']['stdout'])
ck('supplement aggregate consumes setup',supp['rc']==0 and 'mutanti=OK' in supp['stdout'] and 'UCIS (ERROR' in supp['stdout'])
ck('supplement JSON log equals producer JSON',supp['output_logs']['clasa_bl.aud.txt']==cases['I15_setup']['logs']['probe.aud.txt'])
script_originals={n:(D/'sources'/n).read_text(encoding='utf-8') for n in ['rulare_aud_b_r1.sh','test_clasa_lot_b_r1.sh']}
raw_setup=[]
with zipfile.ZipFile(D/'Fixture_and_harness.zip') as z,zipfile.ZipFile(D/'Supplement_fixture.zip') as zs:
 for arch in [z,zs]:
  for name in arch.namelist():
   if name.endswith('/suite/rulare_aud_b_r1.sh') and name.startswith('runner_'):
    actual=arch.read(name).decode('utf-8');normalized=re.sub(r'^CB=.*$', 'CB=/home/saga-server/Documents/EvA-Contab/tools/status/coada_builduri.sh',actual,flags=re.M)
    ck('I15 only CB remapped '+name,normalized==script_originals['rulare_aud_b_r1.sh'])
   if name.endswith('/suite/test_clasa_lot_b_r1.sh'):
    actual=arch.read(name).decode('utf-8');normalized=re.sub(r'^R=[^;]+;', 'R=/home/saga-server/Documents/EvA-Contab;',actual,flags=re.M)
    ck('I16 only R remapped '+name,normalized==script_originals['test_clasa_lot_b_r1.sh'])
   if name.endswith('runner_setup/work/out/probe.aud.txt') or name.endswith('class_setup_from_original/work/out/clasa_bl.aud.txt'):raw_setup.append((name,hashlib.sha256(arch.read(name)).hexdigest()))
 ck('setup fixture intrinsic raise',b'raise RuntimeError("synthetic setup error")' in z.read('pytest_setup/test_witness.py'))
 ck('stale runner explicit rc10',b'exit 10' in z.read('class_stale_fail/suite/rulare_aud_b_r1.sh'))
ck('raw producer-consumer log identity',len(raw_setup)==2 and len({x[1] for x in raw_setup})==1 and raw_setup[0][1]==supp['input_original_I15_log_sha256'],raw_setup)
own=O/'Proba_A11_mutator_lot03_v1.json';ow=read(own);ck('A11 four own witnesses',len(ow['cases'])==4 and ow['cases'][1]['changed_function_names']==['unrelated'] and ow['cases'][1]['rc']==0)
qa=save('QA_A11_receptie_A06_lot03_v1.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'issues':[x for x in checks if not x['ok']],'product_execution_in_this_verifier':False})
print(json.dumps({'qa':qa,'checks':len(checks),'issues':[x for x in checks if not x['ok']]},ensure_ascii=False))
