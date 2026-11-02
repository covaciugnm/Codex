from pathlib import Path, PurePosixPath
import subprocess,os,json,hashlib,datetime
E=Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie');W=Path(r'D:\CodexWork\a01-r11-frozen');repo=Path(r'D:\CodexWork\eva-audit-p01-src-20261101');deps=Path(r'D:\CodexWork\eva-a01-fixture-deps');out=E/'R11_fisiere/A01';out.mkdir(parents=True,exist_ok=True);W.mkdir(exist_ok=True);env={**os.environ,'GIT_NO_LAZY_FETCH':'1'};git=lambda *a:subprocess.check_output(['git','-C',str(repo),*a],env=env);h=lambda b:hashlib.sha256(b).hexdigest();old='6df998aee0e514d30856c461962afe99ebd0d113';new='2fe90ed3f128c33dff7cf9f8674e664a70679390';plan=E/'R11_plan_delta/Plan_delta_R11_v3.json';approval=E/'R11_plan_delta/A11_verdict_plan_delta_R11_v3.json'
assert h(plan.read_bytes())=='676bb5437b47c66835c842b6909e288ccd916388272d69d541d823b36a887edd' and h(approval.read_bytes())=='57b63643abcea8fcb1c716465a9dcb86e9f89a59ec3940d42035df940db2dd14';
def materialize(which,rev):
 rows=[];files=git('ls-tree','-r','-z',rev,'--','frontend','proxy/traefik/propuneri-t232');root=W/which
 for line in files.split(b'\0'):
  if not line:continue
  meta,s=line.split(b'\t',1);m,t,oid=meta.decode().split();f=s.decode();
  if not (f.startswith(('proxy/traefik/propuneri-t232/','frontend/themes/','frontend/portal/')) or f in ('frontend/tests/test_t232_aud_portal_ocolire.py','frontend/tests/test_t232_l1_cale_webui.py') or (len(PurePosixPath(f).parts)==2 and f.endswith('.py'))):continue
  oldroot=Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102'); ref=oldroot/f; blob=ref.read_bytes() if ref.is_file() else b''
  if hashlib.sha1(('blob '+str(len(blob))+'\0').encode()+blob).hexdigest()!=oid:blob=git('cat-file','blob',oid)
  assert hashlib.sha1(('blob '+str(len(blob))+'\0').encode()+blob).hexdigest()==oid
  dst=root/f;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(blob);rows.append({'path':f,'git_oid':oid,'sha256':h(blob)})
 return rows
records={rev:materialize(label,rev) for label,rev in [('old',old),('new',new)]};(out/'manifest_original_git.json').write_text(json.dumps({'plan_sha256':h(plan.read_bytes()),'approval_sha256':h(approval.read_bytes()),'sources':records},indent=2),encoding='utf8');print([(k,len(v)) for k,v in records.items()]);
