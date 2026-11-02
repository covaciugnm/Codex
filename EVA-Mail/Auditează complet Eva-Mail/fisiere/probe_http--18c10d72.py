import concurrent.futures,json,pathlib,time,urllib.request,urllib.error
root=pathlib.Path(__file__).resolve().parent
urls=['https://mail.eva-org.com'+p for p in ['/','/api/v1/auth/me','/api/v1/contacts','/api/v1/probleme','/api/v1/eva-chat/status/00000000-0000-0000-0000-000000000000','/api/v1/openapi.json','/tts-lab/','/tts-lab/openapi.json','/download/android.json','/.well-known/assetlinks.json']]+['http://192.168.100.166:11435/api/tags','http://192.168.100.166:11436/api/tags','http://192.168.100.166:3000/api/v1/auth/me']
def probe(url):
    start=time.monotonic()
    try:
        try: r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'EVA-release-audit/2026-10-30'}),timeout=15)
        except urllib.error.HTTPError as e:r=e
        b=r.read(200000)
        row={'url':url,'status':r.status,'seconds':round(time.monotonic()-start,3),'content_type':r.headers.get('Content-Type'),'bytes_read':len(b),'headers':{k:v for k,v in r.headers.items() if k.lower() in ['content-security-policy','strict-transport-security','permissions-policy','x-frame-options','cache-control']}}
        try:
            data=json.loads(b)
            if isinstance(data,dict):
                row['keys']=list(data)
                if 'items' in data: row['items_count']=len(data['items'])
                if 'paths' in data: row['api_paths']={k:list(v) for k,v in data['paths'].items()};row['security']=data.get('security');row['security_schemes']=data.get('components',{}).get('securitySchemes')
                if 'models' in data:row['models_count']=len(data['models'])
                if url.endswith('android.json'):row['metadata']=data
            elif url.endswith('assetlinks.json'):row['metadata']=data
        except Exception: pass
        return row
    except Exception as e:return {'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: rows=list(ex.map(probe,urls))
(root/'http-probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
