import ast,json,re,hashlib,requests,zipfile,io,unicodedata,shutil,time
from pathlib import Path
from urllib.parse import urlparse
BASE=Path(__file__).parent;BIN=BASE/'download_cache';OUT=BASE/'F'
# Reuse only validated document-download functions, without rerunning catalogue generation.
ns=globals()
tree=ast.parse((BASE/'downloads.py').read_text(encoding='utf8'))
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['download','clean']:exec(compile(ast.Module(body=[node],type_ignores=[]),'download_functions','exec'),ns)
manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf8'));cat=json.loads((BASE/'catalogue.json').read_text(encoding='utf8'));byid={r['id']:r for r in cat}
todo=[d for d in manifest if not d['ok'] and ('429 ' in d.get('error','') or 'Serverul nu a furnizat PDF original' in d.get('error',''))]
print('RECOVERY',len(todo),flush=True)
for i,d in enumerate(todo,1):
 result=download(d['url'],True)
 if result['ok']:
  d.update(result);sub='0.ARHIVA' if d['archive'] else '1.DOCUMENTE OFICIALE';folder=OUT/byid[d['program']]['folder']/sub;folder.mkdir(parents=True,exist_ok=True)
  mx=max(12,244-len(str(folder))-10-len(d['ext']));target=folder/(clean(d['label'],min(60,mx))+'_'+d['sha256'][:8]+d['ext']);shutil.copy2(d['file'],target);d['relative_path']=target.relative_to(OUT).as_posix()
 else:d['error']=result.get('error','')
 print('RECOVERED',i,result['ok'],d['url'],flush=True)
 time.sleep(1)
# Preserve versions explicitly in the archive; recent WP 2026–27 decisions are current.
for d in manifest:
 if d['program']=='JUCA' and d['ok'] and re.search(r'WPB[- _]2026[- _]27',d['url'],re.I) and d['archive']:
  old=OUT/d['relative_path'];folder=OUT/byid['JUCA']['folder']/'1.DOCUMENTE OFICIALE';folder.mkdir(parents=True,exist_ok=True);new=folder/old.name;shutil.copy2(old,new);d['archive']=False;d['relative_path']=new.relative_to(OUT).as_posix()
 if d['program']=='SMP' and d['ok'] and any('C_'+str(y)+'_' in d['url'] or 'c-'+str(y)+'-' in d['url'] for y in [2022,2023,2024]) and not d['archive']:
  old=OUT/d['relative_path'];folder=OUT/byid['SMP']['folder']/'0.ARHIVA';folder.mkdir(parents=True,exist_ok=True);new=folder/old.name;shutil.copy2(old,new);d['archive']=True;d['relative_path']=new.relative_to(OUT).as_posix();d['label']='[VERSIUNE ANTERIOARĂ] '+d['label']
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('RECOVERY_DONE',flush=True)
