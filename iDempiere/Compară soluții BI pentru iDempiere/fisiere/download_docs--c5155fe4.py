from research_bi import ROOT,S
import zipfile,io,json,hashlib,concurrent.futures,pathlib
repos=[('Superset','apache/superset',['docs/','superset-embedded-sdk/README.md']),('Metabase','metabase/metabase',['docs/']),('Knowage','KnowageLabs/Knowage-Documentation',['']),('Redash','getredash/website',['src/pages/kb/','src/pages/help/','src/content/','_kb/']),('Lightdash','lightdash/mintlify-docs',['']),('iDempiere','idempiere/idempiere.github.io',['docs/']),('BX_Metabase','bxservice/de.bxservice.metabase',['']),('CashForecast','pshepetko/org.idempiere.cashforecasting',['README.md','COPYING','downloads/'])]
def run(item):
 name,repo,prefixes=item;out=ROOT/'07_Manuale_complete'/name;out.mkdir(parents=True,exist_ok=True);rec={'name':name,'repository':repo,'date':'2026-10-08'}
 try:
  m=S.get('https://api.github.com/repos/'+repo,timeout=30);m.raise_for_status();meta=m.json();branch=meta['default_branch']
  c=S.get('https://api.github.com/repos/'+repo+'/commits/'+branch,timeout=30);c.raise_for_status();sha=c.json()['sha'];rec.update(branch=branch,commit=sha,license=meta.get('license'))
  u=f'https://codeload.github.com/{repo}/zip/{sha}';r=S.get(u,timeout=240);r.raise_for_status();z=zipfile.ZipFile(io.BytesIO(r.content));files=[]
  for n in z.namelist():
   if n.endswith('/'):continue
   rel=n.split('/',1)[-1]
   if not (any(rel.startswith(p) for p in prefixes) or pathlib.PurePosixPath(rel).name.lower().startswith(('license','notice','copying','readme')) and '/' not in rel):continue
   if '..' in pathlib.PurePosixPath(rel).parts:continue
   p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n));files.append(rel)
  rec.update(download_url=u,files=len(files),archive_sha256=hashlib.sha256(r.content).hexdigest(),paths=files)
  if len(files)<10:rec['warning']='Verifica structura documentatiei; selectie posibil incompleta'
 except Exception as e:rec['error']=str(e)[:200]
 (out/'PROVENIENTA.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False),encoding='utf-8')
 print(name,rec.get('files',0),rec.get('error',''),flush=True)
 return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(run,repos))
 (ROOT/'07_Manuale_complete'/'manifest.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
