import json,hashlib,gzip,zipfile,datetime
from pathlib import Path
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
B=R/'executie/R12_fisiere'
O=B/'A11/Val03_preflight'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 p=Path(p); assert not p.exists(),str(p)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(label,ok,details=None):
 checks.append({'check':label,'ok':bool(ok),'details':details})
def resolve(s):
 p=Path(s)
 return p if p.is_absolute() else R/p
ref_count=0
def refs(d):
 global ref_count
 if isinstance(d,dict):
  if isinstance(d.get('path'),str) and isinstance(d.get('sha256'),str) and len(d['sha256'])==64:
   p=resolve(d['path']); ref_count+=1
   check('reference '+d['path'],p.exists() and sha(p)==d['sha256'])
   if 'pointer' in d:
    try:
     q=read(p)
     for part in d['pointer'].strip('/').split('/'):
      part=part.replace('~1','/').replace('~0','~'); q=q[int(part)] if isinstance(q,list) else q[part]
     check('pointer '+d['path']+d['pointer'],True)
    except Exception as e: check('pointer '+d['path']+d['pointer'],False,str(e))
  for v in d.values(): refs(v)
 elif isinstance(d,list):
  for x in d:refs(x)
M=B/'A12/Val_03/MANIFEST_preflight_Val03_0039.json'
S=B/'A12/Val_03/Supliment_populatie_0039.json'
check('manifest exact',sha(M)=='c7e4cfa0bd47cf692be7be08f71b2e0427d19151d4b5d662c3bdfe6640c0aa5b')
check('supplement exact',sha(S)=='cac08725a0ba8790ccccf8c8e373039006ecb1aed3bb82a9828110da81f241e9')
s=read(S); refs(read(M)); refs(s)
refs(read(B/'A12/Val_03/Continuitate_sigilii_Val02_dupa_preflight.json'))
old=read(resolve(s['captures'][0]['files'][0]['path'])); new=read(resolve(s['captures'][1]['files'][0]['path']))
check('996 rows',len(old)==len(new)==996)
changes=[(i,{k for k in set(a)|set(b) if a.get(k)!=b.get(k)}) for i,(a,b) in enumerate(zip(old,new)) if a!=b]
check('only two changed rows',len(changes)==2,[(i,sorted(k)) for i,k in changes])
check('only observations progress dates',all(k<={'observatii','procent','ultima_actualizare'} for _,k in changes))
check('693 P01',sum(x.get('proiect')=='P01' for x in new)==693)
for f in s['focus_requirement_equality']:
 a=old[int(f['before']['pointer'][1:])]; b=new[int(f['after']['pointer'][1:])]
 check('normative '+f['alias'],all(a.get(x['field'])==b.get(x['field']) and x['equal'] for x in f['normative_fields']))
 check('whole row equality '+f['alias'],(a==b)==f['all_fields_equal'])
check('18 focus tasks',len(s['focus_requirement_equality'])==18)
for a,b in zip(s['captures'][0]['files'][1:],s['captures'][1]['files'][1:]):check('auxiliary '+Path(a['path']).name,resolve(a['path']).read_bytes()==resolve(b['path']).read_bytes())
inv=read(R/'executie/R12_plan_delta/Manifest_A12_receptie_R12_v2.json')
want={x['path']:x['fixed_R12_oid'] for x in s['N05_source_identity_continuity']}
found={}
with gzip.open(resolve(inv['authoritative']['catalog']['path']),'rt',encoding='utf-8') as z:
 for line in z:
  d=json.loads(line)
  if d.get('path') in want:found[d['path']]=d
for p,oid in want.items():check('N05 catalog '+p,p in found and oid in str(found[p]),found.get(p))
# Independently bind the 21 protocol source copies and original JAR entries; no product execution.
idpath=B/'A05_N05_lot03/Identitati_sursee_bundle_v1.json'; ident=read(idpath)
for x in ident['source_files']:
 rel=x['path'].split('/src/com/eva/ro/contab/')[1]
 p=B/'A05_N05_lot03/surse_df85'/rel; data=p.read_bytes()
 check('N05 copied source '+rel,hashlib.sha256(data).hexdigest()==x['sha256'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['oid'])
j=ident['jar']; jp=Path(j['path']); data=jp.read_bytes()
check('N05 JAR identity',hashlib.sha256(data).hexdigest()==j['sha256'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==j['oid'])
with zipfile.ZipFile(jp) as z:
 for c in ident['classes']:check('N05 JAR entry '+c['entry'],hashlib.sha256(z.read(c['entry'])).hexdigest()==c['sha256'])
qa={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'A11 independent metadata and bytes; no product execution','reference_instances':ref_count,'checks':checks,'issues':[x for x in checks if not x['ok']]}
out=O/'QA_A11_receptie_supliment_0039_v1.json';write(out,qa)
print(json.dumps({'path':str(out),'sha256':sha(out),'checks':len(checks),'refs':ref_count,'issues':qa['issues']},ensure_ascii=False))
