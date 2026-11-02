import pathlib,json,ssl,urllib.request,urllib.error,sys,os
w=pathlib.Path('/tmp/codex-a05.ObWQES')
ip=w.joinpath('ip').read_text().strip()
assert ip.startswith('10.250.')
op=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=ssl._create_unverified_context()))
def request(m,r,body=None,token=None):
    h={'Content-Type':'application/json','Accept':'application/json'}
    if token:h['Authorization']='Bearer '+token
    rr=urllib.request.Request('https://'+ip+':8443/api/v1/'+r,data=json.dumps(body).encode() if body is not None else None,headers=h,method=m)
    try:
        with op.open(rr,timeout=60) as v:return v.status,json.loads(v.read() or '{}')
    except urllib.error.HTTPError as e:
        try:return e.code,json.loads(e.read() or '{}')
        except Exception:return e.code,{}
def auth(user,pwd,cl,role,org):
    s,d=request('POST','auth/tokens',{'userName':user,'password':pwd}); assert s==200,(s,'login')
    s,d=request('PUT','auth/tokens',{'clientId':cl,'roleId':role,'organizationId':org},d['token'])
    assert s==200,(s,'select role');return d['token']
def main():
    t=auth('GardenAdmin','GardenAdmin',11,102,11)
    print('authenticated synthetic tenant=11 org=11 role=102')
    for r in ['models/m_product?$top=1','models/m_inventory?$top=1','processes/eva_notasetwms','models/eva_perechewms?$top=1']:
        s,d=request('GET',r,token=t);print('GET',r,s,'summary',d.get('title',d.get('message','')),'fields',list(d.keys())[:5])
    try:
        st=auth('SuperUser','System',0,0,0)
    except Exception as e:
        print('no synthetic System role',str(e))
        return
    st0,read=request('GET','models/ad_entitytype?$filter=EntityType%20eq%20%27EVASAGA%27',token=st)
    print('read entity type',st0,'rows',len(read.get('records',[])))
    if st0==200 and not read.get('records'):
        resp,rec=request('POST','models/ad_entitytype',{'EntityType':'EVASAGA','Name':'EVA Saga synthetic audit','Description':'Scoped audit fixture, type required by installed plugin','Version':'13.0.0'},st)
        print('instantiate required entity type using native PO REST',resp,rec.get('id'),rec.get('title',rec.get('detail','')))
if __name__=='__main__':main()

