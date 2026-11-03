import copy,gzip,hashlib,json,pathlib
from datetime import datetime,timezone
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
R=B/'executie/R12_fisiere';P=R/'A12/Val_04';O=R/'A12/Val_05'
H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p,pointer=None):
    b=p.read_bytes();r={'path':p.relative_to(B).as_posix() if p.is_relative_to(B) else p.as_posix(),'sha256':sha(b),'bytes':len(b)}
    if pointer is not None:r['pointer']=pointer
    return r
def point(d,p):
    for k in p.removeprefix('#').lstrip('/').split('/') if p not in ('','#') else []:
        k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
    return d
def refs(x):
    if isinstance(x,dict):
        if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:yield x
        for v in x.values():yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)
def resolve(p,s):
    q=pathlib.Path(s)
    if q.is_absolute():return q
    if s.startswith('executie/'):return B/q
    options=[p.parent/q,p.parent/'Sources'/q,p.parent/'surse_df85'/q,R/q,B/q]
    hits=list(dict.fromkeys(z for z in options if z.exists()))
    assert len(hits)==1,('Referință ambiguă/lipsă',p,s,hits)
    return hits[0]
def verify(p,expected=None):
    rr=ref(p)
    if expected:assert rr['sha256']==expected,(p,rr['sha256'],expected)
    checks=[]
    for r in refs(load(p)):
        if r['path'].startswith(('idempiere/','frontend/')) and isinstance(r.get('source'),dict):
            q=B/r['source']['path'];b=q.read_bytes();assert sha(b)==r['sha256']==r['source']['sha256']
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_oid']
            checks.append(r);continue
        q=resolve(p,r['path']);got=ref(q);assert got['sha256']==r['sha256'],(q,got['sha256'],r['sha256'])
        if 'bytes' in r:assert got['bytes']==r['bytes'],q
        if r.get('pointer') is not None:point(load(q),r['pointer'])
        checks.append(r)
    return load(p),checks
def read_prior():
    rows=[json.loads(x) for x in gzip.decompress((P/'Registru_6728_R12_Val04.jsonl.gz').read_bytes()).decode().splitlines()]
    assert len(rows)==len({r['path'] for r in rows})==6728
    return rows,{r['path']:r for r in rows}
def save(p,x):
    assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
