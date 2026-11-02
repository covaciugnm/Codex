import urllib.request,urllib.error,urllib.parse,ssl,json,pathlib,re
exec(pathlib.Path('/tmp/codex-a05.ObWQES/fixture.py').read_text().split('if __name__')[0])
st,x=request('POST','auth/tokens',{'userName':'GardenAdmin','password':'[CREDENTIAL_REDACTED]'}); t=x['token']
def get(m,route,data=None):
 h={'Authorization':'Bearer '+t,'Content-Type':'application/json','Accept':'application/json'}
 r=urllib.request.Request('https://'+ip+':8443/api/v1/'+route,data=json.dumps(data).encode() if data is not None else None,method=m,headers=h)
 try:
    with op.open(r,timeout=20) as f: d=f.read().decode();code=f.status
 except urllib.error.HTTPError as e: d=e.read().decode('utf8','replace');code=e.code
 d=re.sub(r'(?i)"(?:token|password|refresh_token)"\s*:\s*"[^"]+"','"[redacted]"',d)
 d=d.replace(t,'[redacted]');print(route,code,re.sub('<[^>]+>',' ',d)[:380])
get('GET','auth/roles?client=11');get('GET','auth/organizations?client=11&role=102');get('GET','auth/warehouses?client=11&role=102&organization=11')
get('PUT','auth/tokens',{'clientId':11,'roleId':102,'organizationId':11,'warehouseId':103,'language':'en_US'})

