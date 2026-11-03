import pathlib,json,hashlib,gzip,datetime,sys
sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');P=R/'executie/R12_plan_delta'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
src=P/'A12/Supliment_populatie_2315.json';assert h(src)=='13950bb8cf068eaac963b1bc9693315e127cdc00670e90aa2cc24527853c1408'
data=j(src);refs=[]
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and 'sha256' in x:
   f=R/x['path'];assert f.is_file() and h(f)==x['sha256'],x
   if 'pointer' in x:
    z=j(f)
    for part in x['pointer'].strip('/').split('/'):
     key=part.replace('~1','/').replace('~0','~');z=z[int(key)] if isinstance(z,list) else z[key]
   refs.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(data)
with gzip.open(P/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz','rt',encoding='utf8') as f:catalog={x['path']:x for x in map(json.loads,f)}
for x in data['source_documents_read_only']:
 raw=(R/x['path']).read_bytes();oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 assert oid==x['git_blob']==catalog[x['git_path']]['git_object']
criterion=data['normative_comparison']['frozen_criterion'];line=(R/criterion['path']).read_text(encoding='utf8').splitlines()[106]
assert line==criterion['text'] and hashlib.sha256(line.encode()).hexdigest()==criterion['line_sha256']
assert 'CO \\| CO \\| CO' in line
prefix='Documentatie/echipa-2026-10-09/T343-comenzi-site-mutate-in-program/'
assert not any(x.startswith(prefix+'14e') for x in catalog)
assert 'D-343-60' not in (P/'Sources_lues'/prefix/'01b_decizii_orchestrator.md').read_text(encoding='utf8')
out={
 'schema':'A11.R12.T343.nominal_oracle_intake.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':data['head'],
 'source':{'path':src.relative_to(R).as_posix(),'sha256':h(src)},'checks':{'references_rehashed':len(refs),'source_documents_SHA_and_Git_blob':4,'criterion_line107_exact':True,'14e_absent_in_fixed_catalog':True,'D34360_absent_in_fixed_decision_document':True,'product_executions':0},
 'decision':'ADMIS ca supliment documentar, cu recepția nominală C-2.2 rămasă deschisă. Nu modifică poarta lotului T240 și nu validează revendicările de teste din observații.',
 'criterion_preserved':criterion,
 'oracle_rule':'C-2.2 la df85 cere CO|CO|CO|număr de linii legate. IP este o stare diferită; nu se transformă în PASS al acestei formulări. Observația registrului nu amendă singură oracolul.',
 'native_first':'Nu calificăm IP drept defect fără traseul și contractul complet. Se documentează drumul nativ T22/T216, DocAction/DocStatus/Processed, motivul stării și condițiile de continuare. Normalizarea suplimentară trebuie justificată prin capabilitatea nativă verificată.',
 'pending_actions':[
  'A06/A07: fixează D-343-60 și 14e cu autor/data/commit, recepție și aplicabilitate la SHA; absența constatată este limitată la sursele fixate.',
  'A06/A08: propune amendamentul nominal cu vechi/nou, justificare, actor și oracle înainte/după pentru C_Order/Line, M_InOut/Line și C_Invoice/Line; A11 recepționează înainte de promovarea rezultatului în noua formulare.',
  'D05 rămâne deschis; D06 păstrează separat efectele aval aviz/factură/încasare; D01/D10 păstrează rol/context/stare UI.',
  'A12: păstrează numerele declarate56/0,26/0,306 ca afirmații neprimite; nu creează un task canonic din textul T-NOU și nu închide LR-urile lotului B.'
 ],
 'scoring':{'plan_gate_changed':False,'new_plan_score':None,'execution_score':None,'global_product_score':None,'contracts_closed':0},
 'method':{'path':str(pathlib.Path(__file__)),'sha256':h(pathlib.Path(__file__))},
 'resources':{'new_services':0,'operational_writes':0,'created_files':'Documente de audit numai'}
}
dest=P/'Receptie_A11_supliment_T343_2315_v1.json';assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
seal=P/'Sigiliu_A11_supliment_T343_2315_v1.json';assert not seal.exists();seal.write_text(json.dumps({'artifact':{'path':dest.relative_to(R).as_posix(),'sha256':h(dest)},'utc':out['utc'],'method':out['method']},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'output':str(dest),'sha256':h(dest),'seal_sha256':h(seal),'refs':len(refs)},ensure_ascii=False))
