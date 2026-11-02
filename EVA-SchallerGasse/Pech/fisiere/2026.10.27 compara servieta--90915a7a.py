from pathlib import Path
import json,zipfile,hashlib,collections,shutil,os,re
R=Path.cwd();Q=R/'folder map/2026.10.27 QA autorizare'; Z=Q/'Servieta';Z.mkdir(exist_ok=True)
I=json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'));old={x['cale']:x for x in I}
names=['P1 - Unternehmen & Eigentum.zip','P2 - Baubewilligung – Einreichplanung P2041.zip','P3 - Archiv – Unterlagen zur Baubewilligung.zip','P4 - Baugrund & Tragwerk (Geotechnik, Statik).zip','P5 - Architektur – Ausführungsplanung (Planstand 08.09.2026).zip','P6 - Heizung, Gas & Lüftung.zip','P7 - Wasser & Kanal (Sanitär).zip','P8 - Dachgeschoss (Dachgeschossausbau).zip','P9 - Elektro & Schwachstrom.zip','P11 - Bestand – Bestandspläne & Fotodokumentation.zip','P12 - Ausschreibung Generalunternehmer.zip']
files=[];pages=[]
for name in names:
 src=Path('C:/Users/User/Downloads')/name;p=Z/('2026.10.27 '+name);shutil.copy2(src,p);pg=name.split(' - ')[0];rows=[]
 with zipfile.ZipFile(p) as z:
  for m in z.infolist():
   if m.is_dir():continue
   data=z.read(m);dest=Z/pg/m.filename
   if not dest.resolve().is_relative_to((Z/pg).resolve()):raise ValueError(m.filename)
   dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   item={'page':pg,'name':m.filename,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'downloaded':dest.relative_to(R).as_posix()};files.append(item);rows.append(item)
 pages.append({'page':pg,'url':'https://www.ac-wohnart.at/'+pg.lower(),'count':len(rows),'zip':p.relative_to(R).as_posix()})
for pg in ['P10','P13','P14','P15','P16','P17']:pages.append({'page':pg,'url':'https://www.ac-wohnart.at/'+pg.lower(),'count':0,'observed':'Noch keine Dateien vorhanden.'})
local=[];changed=[]
exclude={'folder map','.git','.codex','.agents','Acasa','Website'}
exts={'.pdf','.docx','.doc','.xlsx','.xls','.csv','.txt','.eml','.ics','.dwg','.dxf','.jpg','.jpeg','.png','.tif','.tiff','.md','.zip','.rar','.7z','.pptx'}
for base,dirs,fs in os.walk(R):
 dirs[:]=[x for x in dirs if x not in exclude]
 for name in fs:
  p=Path(base)/name;rel=p.relative_to(R).as_posix()
  if p.suffix.lower() not in exts or name.startswith('~$') or name=='desktop.ini':continue
  if '/Alte proiecte/' in rel:continue
  st=p.stat();prior=old.get(rel);same=bool(prior and prior.get('octeti')==st.st_size and prior.get('modificat_ns')==st.st_mtime_ns)
  dig=prior['sha256'] if same else hashlib.sha256(p.read_bytes()).hexdigest()
  if not same:changed.append(rel)
  local.append({'cale':rel,'sha256':dig,'size':st.st_size,'unchanged_metadata':same})
by=collections.defaultdict(list)
for r in local:by[r['sha256']].append(r['cale'])
for row in files:row['local_matches']=by.get(row['sha256'],[])
webhash={x['sha256'] for x in files}
groups=collections.defaultdict(list)
for row in local:
 if row['sha256'] not in webhash:groups[row['sha256']].append(row['cale'])
stats={'data':'2026.10.27','account':'office@zt-pech.at','scope':'P1–P17 accesibile; P18–P20 blocate, neinspectate','online_files':len(files),'online_unique':len(webhash),'online_exact_local':sum(bool(x['local_matches']) for x in files),'online_no_exact_local':sum(not x['local_matches'] for x in files),'local_files':len(local),'local_unique':len(by),'local_unique_not_online':len(groups),'new_or_changed_metadata':len(changed),'local_excluded':sorted(exclude),'exts':sorted(exts),'pages':sorted(pages,key=lambda p:int(p['page'][1:]))}
(Q/'2026.10.27 Comparatie servieta.json').write_text(json.dumps({'stats':stats,'files':files,'local':local,'missing_online_by_hash':groups,'new_or_changed_paths':changed},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2));print('NO_EXACT_MATCH');print(json.dumps([r for r in files if not r['local_matches']],ensure_ascii=False,indent=2))
