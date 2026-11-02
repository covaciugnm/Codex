from pathlib import Path
import json,gzip,hashlib,datetime,collections,subprocess as sp,os,io,tarfile
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); E=B/'executie';P=E/'R11_plan_delta'; O=E/'R11_fisiere'; A=O/'A12';A.mkdir(exist_ok=True); W=Path('D:/CodexWork/a12-r11-p01'); W.mkdir(exist_ok=True);LOCAL=W/'repo';LOCAL.mkdir(exist_ok=True); head='2fe90ed3f128c33dff7cf9f8674e664a70679390'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return sha_bytes(p.read_bytes())
def rel(p):return p.relative_to(B).as_posix()
def ref(p):return {'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
def save(p,j):
 if p.exists():raise Exception('immutable '+str(p))
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def lines(p):
 with gzip.open(p,'rt',encoding='utf8')as f:return [json.loads(x)for x in f]
dispatch=P/'Dispatch_tehnic_integral.jsonl.gz';whole=P/'Catalog_Git_integral_per_fisier.jsonl.gz';rows=lines(dispatch);d={r['path']:r for r in rows};catalog={r['path']:r for r in lines(whole)}
gate=P/'A11_verdict_plan_delta_R11_v3.json';plan=P/'Plan_delta_R11_v3.json'
assert len(rows)==len(d)==6709 and len({r['id']for r in rows})==6709 and sha(plan)=='676bb5437b47c66835c842b6909e288ccd916388272d69d541d823b36a887edd'and sha(gate)=='57b63643abcea8fcb1c716465a9dcb86e9f89a59ec3940d42035df940db2dd14'and read(gate)['eligible_to_execute_candidate_audit'] is True
axes=['inspected','static','exercised','bindingVerified','reproduced','blocked']

