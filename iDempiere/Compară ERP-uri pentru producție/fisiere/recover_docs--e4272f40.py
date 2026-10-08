from pathlib import Path
import requests,json,zipfile,io,hashlib,concurrent.futures
P=Path(__file__).parent; OUT=P/'package'
exec((P/'download_docs.py').read_text(encoding='utf-8-sig').split('with concurrent.futures.ThreadPoolExecutor(max_workers=10)')[0])
reg=json.loads((OUT/'registru_documentatii.json').read_text(encoding='utf8'))
failed=[x for x in reg if x.get('error') and x['id'].startswith('E') and x.get('status')!=404]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for r in pool.map(fetch,failed):
  if not r.get('error'):
   reg=[r if x['id']==r['id'] else x for x in reg]
   f=OUT/r['group']/(r['id']+'_INDISPONIBIL.txt')
   if f.exists():f.unlink()
url='https://codeload.github.com/odoo/documentation/zip/refs/heads/19.0'
try:
 r=requests.get(url,timeout=180);r.raise_for_status();z=zipfile.ZipFile(io.BytesIO(r.content));count=0
 for n in z.namelist():
  rel='/'.join(n.split('/')[1:])
  if n.endswith('/') or not (rel.startswith('content/applications/inventory_and_mrp/manufacturing') or rel in ['LICENSE','LICENSE.rst','COPYRIGHT']):continue
  f=OUT/'07_Odoo_Community/surse_documentatie'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(n));count+=1
 reg.append(dict(id='O_DOC_SOURCE',group='07_Odoo_Community',title='Documentație oficială Odoo 19: capitol Manufacturing, RST și imagini',url=url,status=200,local='07_Odoo_Community/surse_documentatie',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),files=count,note='Snapshot ramură 19.0; nu probă de disponibilitate Community pentru toate paginile.'))
 print('Odoo docs extracted',count,flush=True)
except Exception as e:print('Odoo fallback failed',str(e),flush=True)
(OUT/'registru_documentatii.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf8')
print('Sources',len(reg),'local',sum(bool(x.get('local')) for x in reg),'failed',sum(bool(x.get('error')) for x in reg),flush=True)
