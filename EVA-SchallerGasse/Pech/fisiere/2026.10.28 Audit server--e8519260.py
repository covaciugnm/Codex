from pathlib import Path
import json,hashlib,re,datetime,collections,sys,zipfile,shutil
sys.stdout.reconfigure(encoding='utf-8')
S=Path(r'\\192.168.100.151\site-uri\schallergasse35')
R=Path.cwd();Q=R/'folder map/2026.10.28 QA server';Q.mkdir(exist_ok=True)
print('ROOT',str(S))
for folder in ['public','data/uploads']:
 p=S/folder;print('DIR',folder)
 for x in p.iterdir():print(x.name,'DIR' if x.is_dir() else x.stat().st_size)
app=(S/'backend/app.py').read_text(encoding='utf-8')
for i,line in enumerate(app.splitlines()):
 if any(k in line for k in ['@app.get','StaticFiles','DOCS_DIR','DOCUMENTS_DIR','PAGE','page_files','page_docs','def list','ROOT_DIR','PUBLIC_DIR','UPLOAD_DIR']):
  print('APP',i+1,line)
docs=(S/'DOCUMENTATIE.md').read_text(encoding='utf-8')
for line in docs.splitlines():
 if any(k.lower() in line.lower() for k in ['document','map','p18','p19','p20','ser','fișier','fisier','upload','pagina','pagină']) and not any(k in line.lower() for k in ['password','parol','secret','token','credential']):print('DOC',line)
exts={'.pdf','.doc','.docx','.xls','.xlsx','.csv','.txt','.json','.dwg','.dxf','.zip','.rar','.7z','.jpg','.jpeg','.png','.webp','.tif','.tiff'}
old_path=Q/'2026.10.28 Inventar server.json';old={x['path']:x for x in json.loads(old_path.read_text(encoding='utf-8'))} if old_path.exists() else {}
files=[]
for folder in ['public','data/uploads']:
 for p in (S/folder).rglob('*'):
  if not p.is_file() or (folder=='public' and p.suffix.lower() not in exts):continue
  if any(x in p.parts for x in ['fonts']):continue
  st=p.stat();rel=p.relative_to(S).as_posix();mt=datetime.datetime.fromtimestamp(st.st_mtime).isoformat();prior=old.get(rel);same=prior and prior['size']==st.st_size and prior['modified']==mt
  files.append({'path':rel,'size':st.st_size,'modified':mt,'sha256':prior['sha256'] if same else hashlib.sha256(p.read_bytes()).hexdigest()})
(Q/'2026.10.28 Inventar server.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print('HASHED',len(files));print(collections.Counter(x['path'].split('/')[1] for x in files))
print('PAGE_DIRS',[(x.name,len(list(x.iterdir()))) for x in (S/'data/uploads/pages').iterdir() if x.is_dir()])
oldweb=json.loads((R/'folder map/2026.10.27 QA autorizare/2026.10.27 Comparatie servieta.json').read_text(encoding='utf-8'));webhash={x['sha256'] for x in oldweb['files']};extra=[]
for row in files:
 if not row['path'].startswith('data/uploads/pages/') or row['sha256'] in webhash:continue
 src=S/row['path'];dest=Q/('2026.10.28 Server '+src.parent.name+' '+src.name);shutil.copy2(src,dest)
 item=dict(row);item['local_copy']=dest.relative_to(R).as_posix()
 if src.suffix=='.zip':
  with zipfile.ZipFile(src) as z:item['members']=[x.filename for x in z.infolist()]
 elif src.suffix in ['.txt','.csv']:item['excerpt']=src.read_text(encoding='utf-8-sig',errors='replace')[:800]
 extra.append(item)
(Q/'2026.10.28 Fisiere suplimentare.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf-8')
print('EXTRAS',json.dumps(extra,ensure_ascii=False,indent=2))
