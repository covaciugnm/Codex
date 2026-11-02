"""Independent A11 variant, cloned ASGI fixture harness with different controls. No external network."""
import pathlib,os,json,sys,hashlib
B=pathlib.Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie')
OUT=B/'A11_reproduceri_lot1'
os.environ['A01_OUTPUT']=str(OUT)
h=(B/'A01/a01_probe.py').read_text(encoding='utf-8')
exec(compile(h[:h.index("request('T01'")],str(B/'A01/a01_probe.py')+'#safe-fixture-setup','exec'))
cases=[]
def call(method,url,token=None,body=None,extra=None):
 hdr=extra.copy() if extra else {}
 if token: hdr['Authorization']='Bearer '+token
 return cli.request(method,pref+url,json=body,headers=hdr)
def item(fid,steps,expected,actual,conditions):
 cases.append(dict(id=fid,steps=steps,expected=expected,observed=actual,scope=conditions))
# F01: same cabinet vs unknown unique code, new email and persisted identity assessed separately.
reg=call('POST','/auth/register',body={'name':'A11 probe person','email':'a11-independent@example.invalid','password':'A11-Only-local-Pass!','cui':'RO71000002'})
with SessionLocal() as se:
 result=se.query(IamUser).filter_by(email='a11-independent@example.invalid').one_or_none()
 account=[result.managing_uuid,result.role] if result else None
item('A01.F01',['anonymous POST existing cabinet from synthetic fixture','SELECT account.email and cabinet membership'],['deny join without invitation',None],[reg.status_code,account],'ASGI app at frozen SHA, A/B synthetic, enforcement enabled; invite absent')
# F02: before/after checks for unrelated company; protected negative read.
before=call('GET','/auth/can?tenant_cui=RO81919192&perm=write',member)
peer=call('GET','/managing-firms/cabB/users',member)
grant=call('POST','/users/Amem/access',member,{'managed_firm_uuid':'B1','app':'both','permission':'write'})
after=call('GET','/auth/can?tenant_cui=RO81919192&perm=write',member)
with SessionLocal() as se:
 persisted=se.query(FirmAccess).filter_by(iam_user_uuid='Amem',managed_firm_uuid='B1').count()
item('A01.F02',['member A cannot read cabinet B users','auth/can before','grant own write on managed firm B1','auth/can after, SELECT grant'],[403,False,'403/404',False,0],[peer.status_code,before.json().get('allowed'),grant.status_code,after.json().get('allowed'),persisted],'Role member with valid A team lead; negative control: unrelated users list.')
# F04 reverse creation direction B → A plus replay and control distinct idempotency.
base={'X-Tenant-Cui':'RO91919191'}
hkey={**base,'X-Idempotency-Key':'A11-replay-key-B-to-A-00042'}
bdoc=call('POST','/office/documents',bm,{'filename':'B-private.txt','content':'A11 synthetic marker','mime':'text/plain'},hkey)
adoc=call('POST','/office/documents',am,{'filename':'A-private.txt','content':'different A','mime':'text/plain'},hkey)
alist=call('GET','/office/documents',am,extra=base)
nonshared=call('GET','/office/documents',am,extra={'X-Tenant-Cui':'RO81919192'})
with SessionLocal() as se:
 n=se.query(OfficeDocument).count()
item('A01.F04',['manager B creates office canary on shared firm CUI','manager A submits distinct payload with same idempotency key','manager A lists docs, non-shared tenant as negative'],['do not disclose another cabinet record','refuse wrong context'],dict(Bcode=bdoc.status_code,Acode=adoc.status_code,replayed_first_id=bool(bdoc.json().get('eva_uuid')) and bdoc.json().get('eva_uuid')==adoc.json().get('eva_uuid'),canary_read_by_A='B-private.txt' in [x.get('filename') for x in alist.json().get('documents',[])],nonshared_status=nonshared.status_code,row_count=n),'Two independent cabinets manage identical firm CUI; no claim incident in production.')
# F05: avoid cross-cabinet write confound. Use own cabinet read before/after logout + refresh negative.
pre=call('GET','/managing-firms/cabA/users',am)
rev=call('POST','/auth/logout-all',am)
me=call('GET','/auth/me',am)
leak=call('GET','/managing-firms/cabA/users',am)
bad=call('GET','/managing-firms/cabA/users',am+'x')
item('A01.F05',['valid manager accesses own cabinet','logout-all','old token auth/me','old token same own-cabinet read','invalid signature same read'],[200,200,401,401,401],[pre.status_code,rev.status_code,me.status_code,leak.status_code,bad.status_code],'Own cabinet read deliberately avoids combining revocation and separate foreign-store PUT finding.')
cli.close();engine.dispose();tmp.cleanup()
(OUT/'A01_P0_independent.json').write_text(json.dumps(dict(code='6df998aee0e514d30856c461962afe99ebd0d113',harness_sha256=hashlib.sha256(h.encode()).hexdigest(),time_utc=datetime.datetime.now(datetime.UTC).isoformat(),cases=cases,external_attempts=attempted,cleanup=not wd.exists()),ensure_ascii=False,indent=2),encoding='utf-8')
print([(i['id'],i['observed']) for i in cases])
