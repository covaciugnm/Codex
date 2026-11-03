import pathlib,tempfile,shutil,subprocess,hashlib,json,datetime,sys,zipfile,os,copy
sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A11/T240_lot01';P=R/'executie/R12_plan_delta'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
proof=O/'Control_independent_T240_v1.json';assert h(proof)=='72a8bd764bbbbe45863dcee78faad1aa56f02ef8757a65cec24d54e3f4bb9c3d'
j=json.loads(proof.read_text(encoding='utf8'));archive=O/'Fixture_si_iesiri_independente_T240_v1.zip';assert h(archive)==j['artifacts'][0]['sha256']
scratch=pathlib.Path(tempfile.mkdtemp(prefix='a11-r12-t240-title-',dir='D:/CodexWork')).resolve();assert scratch.parent==pathlib.Path('D:/CodexWork').resolve()
dest=O/'Control_independent_T240_titlu_E_v1.json';assert not dest.exists()
res=[]
try:
 with zipfile.ZipFile(archive) as z:
  source=z.read('verifica_proba.py');child=z.read('child.py');baseline={x:z.read(x) for x in z.namelist() if x.startswith('positive/') and not x.endswith('/')}
 (scratch/'verifica_proba.py').write_bytes(source);(scratch/'child.py').write_bytes(child)
 assert h(scratch/'verifica_proba.py')=='8352ebf2afa6175ae77582efc77166a0c071d2c3806926b7e0ae63da6fde6413'
 for name,expected in [('baseline',0),('display_only',1),('report_title_triple_forged',0),('inventory_second_column_changed',0)]:
  d=scratch/name;d.mkdir()
  for rel,raw in baseline.items():
   if rel.endswith(('stdout.txt','stderr.txt')):continue
   f=d/pathlib.PurePosixPath(rel).relative_to('positive');assert f.resolve().is_relative_to(d.resolve());f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
  e_lines=(d/'ecrane.tsv').read_text(encoding='utf8').splitlines();lines=(d/'raport.tsv').read_text(encoding='utf8').splitlines();header=lines[0].split('\t');rows=[dict(zip(header,x.split('\t'))) for x in lines[1:]]
  target=rows[0]
  if name=='display_only':target['titlu_afisat']='Ajutor — TITLU DIFERIT'
  if name=='report_title_triple_forged':target['titlu_afisat']=target['titlu_asteptat']='Ajutor — TITLU DIFERIT';target['titlu_inventar']='TITLU DIFERIT'
  if name=='inventory_second_column_changed':e_lines[0]=e_lines[0].split('\t')[0]+'\tNUME REAL DIN INVENTAR'
  (d/'ecrane.tsv').write_text('\n'.join(e_lines)+'\n',encoding='utf8');(d/'raport.tsv').write_text('\t'.join(header)+'\n'+'\n'.join('\t'.join(r[k] for k in header) for r in rows)+'\n',encoding='utf8')
  names={x.split('\t')[0]:x.split('\t')[1] for x in e_lines}
  independent_mismatch=[{'screen':r['ecran'],'language':r['limba'],'inventory_name':names[r['ecran']],'report_inventory_name':r['titlu_inventar'],'displayed':r['titlu_afisat']} for r in rows if not r['titlu_afisat'].endswith(' — '+names[r['ecran']])]
  args=[sys.executable,'-I','-X','utf8',str(scratch/'child.py'),str(scratch),str(scratch/'verifica_proba.py'),str(d),'--ecrane',str(d/'ecrane.tsv')]
  cp=subprocess.run(args,cwd=scratch,capture_output=True,text=True,encoding='utf8',timeout=20,env={**os.environ,'TEMP':str(scratch),'TMP':str(scratch),'PYTHONDONTWRITEBYTECODE':'1'})
  assert cp.returncode==expected,(name,cp.returncode,cp.stderr)
  assert ('GUARD_OK socket' in cp.stderr and 'GUARD_OK outside_write' in cp.stderr)
  if name=='baseline':assert not independent_mismatch
  else:assert independent_mismatch
  (d/'stdout.txt').write_text(cp.stdout,encoding='utf8');(d/'stderr.txt').write_text(cp.stderr,encoding='utf8')
  res.append({'id':name,'component_exit':cp.returncode,'independent_inventory_oracle_accepts':not bool(independent_mismatch),'inventory_mismatches':independent_mismatch,'stdout':cp.stdout,'stderr':cp.stderr,'report_sha256':h(d/'raport.tsv'),'inventory_sha256':h(d/'ecrane.tsv')})
 outzip=O/'Fixture_titlu_E_independent_v1.zip';assert not outzip.exists()
 with zipfile.ZipFile(outzip,'x',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(scratch.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(scratch).as_posix())
finally:
 assert scratch.parent==pathlib.Path('D:/CodexWork').resolve() and scratch.name.startswith('a11-r12-t240-title-')
 shutil.rmtree(scratch)
out={'schema':'A11.R12.T240.inventory_title.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480','subject':'R12-I19 / R3 compararea cu E coloana2','source':j['preflight']['source'],'originals_unchanged':True,'method':'CLI original, 4 fixture independente, fără importul generatorului original. Oracolul A11 citește E col.2 și compară suffixul titlului raportat, spre deosebire de judecător.','input_fixture_archive':ref(archive),'cases':res,'finding':{'id':'A11.R12.T240.R3.E2','statement':'Judecătorul poate raporta13/13 conforme și rc0 deși titlul afișat contrazice numele din E col.2. Schimbarea numai a col.2 în E nu îi afectează verdictul; falsificarea coerentă a celor3 coloane din raport este acceptată.','requirement':'Docstring verifica_proba.py R3: titlul trebuie să se termine cu numele ecranului din inventar E col.2.','mechanism':'citeste_e păstrează numai prima coloană; motive folosește titlu_inventar din raport.','scope':'Defect al corelării judecătorului CLI cu inventarul, probat pe date sintetice; nu demonstrează un titlu greșit în UI reală.','suggestion':'Păstrează maparea ID→nume din E și validează atât titlu_inventar din raport, cât și titlul afișat împotriva sursei E, cu excepția REGES explicită și probe pozitive/negative.','native_priority':'Această corecție aparține uneltei de verificare; nu solicită un mecanism UI nativ paralel.','whole_task_accepted':False},'cleanup':{'scratch_absent':not scratch.exists(),'services':0,'operational_writes':0},'artifacts':[ref(outzip)],'method_source':{'path':str(pathlib.Path(__file__)),'sha256':h(pathlib.Path(__file__))}}
assert out['cleanup']['scratch_absent'];dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(ref(dest),ensure_ascii=False))
