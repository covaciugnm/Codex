import json, pathlib, ssl, sys, urllib.request, urllib.error
w=pathlib.Path('/tmp/codex-a05.ObWQES')
ip=(w/'ip').read_text().strip()
context=ssl._create_unverified_context() # synthetic internal self-signed HTTPS, isolated GardenWorld only
base='https://'+ip+':8443/api/v1'
session=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=context))
def req(path,method,body=None,token=None):
    headers={'Content-Type':'application/json','Accept':'application/json'}
    if token:headers['Authorization']='Bearer '+token
    r=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers=headers)
    try:
        with session.open(r,timeout=15) as v: return v.status,json.load(v)
    except urllib.error.HTTPError as e:
        try:return e.code,json.load(e)
        except Exception:return e.code,{}
def public(res):
    if isinstance(res,dict):return {k:public(v) for k,v in res.items() if k.lower() not in {'token','accesstoken','refreshtoken','password','secret'}}
    if isinstance(res,list):return [public(v) for v in res]
    return res
user='GardenAdmin'
auth={'userName':user,'password':user};s,b=req('/auth/tokens','POST',auth);print('AUTH status',s,'response',str(public(b))[:900])
if s==200:
    auth['parameters']={'clientId':11,'roleId':102,'organizationId':11,'warehouseId':103,'language':'en_US'}
    s,b=req('/auth/tokens','POST',auth);print('ROLE login',s, 'auth issued',bool(b.get('token')));token=b.get('token')
    if token:
        (w/'garden-token').write_text(token);(w/'garden-token').chmod(0o600)
        for route in ['/windows?$top=1','/models/m_product?$top=1','/models/m_inventory?$top=1','/processes/eva_notasetwms']:
            st,d=req(route,'GET',token=token);print('GET',route,'status',st,'keys',list(d)[:8])
