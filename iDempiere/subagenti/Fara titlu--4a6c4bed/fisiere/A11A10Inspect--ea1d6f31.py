import pathlib,json,hashlib,zipfile,collections
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A10_Instrumente_ramase_lot03')
def load(n):return json.loads((B/n).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
m=load('Manifest_lot03.json'); issues=[]
for n,v in m['files'].items():
 b=(B/n).read_bytes()
 if sha(b)!=v['sha256'] or len(b)!=v['bytes']:issues.append(n)
print('MANIFEST',len(m['files']),sha((B/'Manifest_lot03.json').read_bytes()),'ISSUES',issues)
for n in ['Rezultate_I17_pure_28.json','Rezultate_I17_DOM_18.json','Rezultate_shell_27_cazuri.json']:
 a=load(n);print(n,type(a).__name__,len(a));print(json.dumps(a[-1],ensure_ascii=False)[:2300])
print('INV',str(load('Inventar_final_fixture.json'))[:1500])
print('MANIFEST PATHS',list(m['files']))
with zipfile.ZipFile(B/'Dovezi_complete_lot03.zip') as z:
 ns=z.namelist();print('ZIP',len(ns),'DUP',len(ns)-len(set(ns)),'BAD',z.testzip());print('ZIP_SAMPLE',ns[:20]);print('RUNNERS',[x for x in ns if x.endswith('.py') and '/' not in x][:30]);print('ZIP_PREP',[x for x in ns if x.endswith('Preparation_manifest.json')])
print('CASES')
for a in load('Rezultate_shell_27_cazuri.json'):print(json.dumps(a,ensure_ascii=False)[:600])
