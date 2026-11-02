from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,sqlite3,csv,collections,importlib.util,re
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font,PatternFill,Alignment
from urllib.parse import quote
root=Path.cwd();base=root/'folder map';stamp=datetime.now(ZoneInfo('Europe/Bucharest')).isoformat(timespec='seconds')
spec=importlib.util.spec_from_file_location('archive_index',base/'actualizeaza_index.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rows={r['cale']:r for r in json.loads((base/'inventar.json').read_text(encoding='utf-8-sig'))};changed=json.loads((base/'2026.10.31 Fisiere actualizate verificare generala.json').read_text(encoding='utf-8'))
oldhash={r['sha256']:r['cale'] for r in reversed(list(rows.values()))};updated=[]
for rel in changed:
 if rel.startswith('folder map/'):continue
 p=root/rel;st=p.stat();sha=hashlib.sha256(p.read_bytes()).hexdigest();text,status,info=module.extract(p)
 cp=base/'texte'/(sha+'.txt');cp.write_text(text,encoding='utf-8');(base/'texte'/(sha+'.json')).write_text(json.dumps(dict(info,status=status),ensure_ascii=False,indent=2),encoding='utf-8')
 desc,excerpt=module.describe(rel,text,status)
 row={'cale':rel,'folder':p.parent.relative_to(root).as_posix(),'extensie':p.suffix.lower(),'octeti':st.st_size,'modificat':datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':oldhash.get(sha,'') if oldhash.get(sha)!=rel else '','ce_reprezinta':desc,'baza_descrierii':'Actualizare incrementala 2026.10.31; tip din nume si text extras','extras_continut':excerpt,'stare_citire':status,'text_cache':cp.relative_to(root).as_posix(),'detalii':info,'rezumat_verificat':'','ocr_cache':''}
 rows[rel]=row;updated.append(row);oldhash.setdefault(sha,rel)
ordered=sorted(rows.values(),key=lambda r:r['cale'].lower());assert len({r['cale'] for r in ordered})==len(ordered)
(base/'inventar.json').write_text(json.dumps(ordered,ensure_ascii=False,indent=2),encoding='utf-8')
with (base/'inventar.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=[k for k in ordered[0] if k!='detalii'];w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(ordered)
# Refresh folder counts from the canonical inventory without re-reading unchanged document contents.
folders=json.loads((base/'foldere.json').read_text(encoding='utf-8-sig'));dirmap={r['cale']:r for r in folders}
for r in ordered:
 path=Path(r['folder'])
 for p in [path,*path.parents]:
  rel=p.as_posix()
  if rel!='.' and rel not in dirmap:dirmap[rel]={'cale':rel,'fisiere_directe':0,'fisiere_recursive':0,'rol':'Corespondenta si actualizare proiect Schallergasse 35','baza':'Actualizare incrementala a structurii'}
for folder,r in dirmap.items():
 sub=[x for x in ordered if x['cale'].startswith(folder+'/')];r['fisiere_directe']=sum(x['folder']==folder for x in sub);r['fisiere_recursive']=len(sub)
folders=sorted(dirmap.values(),key=lambda r:r['cale'].lower());(base/'foldere.json').write_text(json.dumps(folders,ensure_ascii=False,indent=2),encoding='utf-8')
stats=json.loads((base/'statistici.json').read_text(encoding='utf-8-sig'));stats.update({'generat':stamp,'fisiere':len(ordered),'foldere':len(folders),'continuturi_unice':len({r['sha256'] for r in ordered}),'copii_identice':len(ordered)-len({r['sha256'] for r in ordered}),'stari':dict(collections.Counter(r['stare_citire'] for r in ordered)),'mod_actualizare':'Incremental: numai documentele salvate la verificarea generala 2026.10.31; textele si hashurile documentelor neschimbate sunt reutilizate.'});(base/'statistici.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
# Rebuild the derivative workbook in streaming mode, preserving readable columns and hyperlinks.
wb=Workbook(write_only=True)
def sheet(name,headers,widths):
 ws=wb.create_sheet(name);ws.freeze_panes='A2'
 for i,width in enumerate(widths,1):
  from openpyxl.utils import get_column_letter
  ws.column_dimensions[get_column_letter(i)].width=width
 cells=[]
 for h in headers:
  c=WriteOnlyCell(ws,h);c.font=Font(bold=True,color='FFFFFF');c.fill=PatternFill('solid',fgColor='24486B');cells.append(c)
 ws.append(cells);return ws
cols=['cale','ce_reprezinta','extras_continut','stare_citire','duplicat_al','octeti','modificat','sha256','text_cache','ocr_cache','rezumat_verificat'];ws=sheet('Fișiere',cols,[55,55,55]+[30]*8)
for r in ordered:
 cells=[]
 for col in cols:
  c=WriteOnlyCell(ws,re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',str(r.get(col,'')))[:32700]);c.data_type='s';c.alignment=Alignment(vertical='top',wrap_text=True)
  if col in ('cale','text_cache','ocr_cache') and r.get(col):c.hyperlink=(root/r[col]).as_uri()
  cells.append(c)
 ws.append(cells)
ws.auto_filter.ref='A1:K'+str(len(ordered)+1)
ds=sheet('Foldere',['Cale','Fișiere directe','Fișiere recursive','Rol conform structurii'],[55,30,30,55])
for r in folders:ds.append([r['cale'],r['fisiere_directe'],r['fisiere_recursive'],r['rol']])
ds.auto_filter.ref='A1:D'+str(len(folders)+1)
ss=sheet('Acoperire',['Indicator','Valoare'],[55,80])
for k,v in stats.items():
 if k not in ('stari','erori'):ss.append([k,str(v)])
for k,v in stats['stari'].items():ss.append([k,v])
wb.save(base/'Folder map.xlsx')
byfolder=collections.defaultdict(list)
for r in ordered:byfolder[r['folder']].append(r)
lines=['# Harta documentelor Schallergasse 35','',f'Generat: {stamp}. {len(ordered)} fișiere, {len(folders)} foldere.','','Actualizare incrementala; descrierile de tip sunt deduse din nume, iar extrasele provin din textele arhivate.','']
for folder in ['.']+[r['cale'] for r in folders]:
 lines+=['## '+folder,'']
 if folder in dirmap:lines+=[dirmap[folder]['rol'],'']
 for r in byfolder[folder]:
  link='../'+quote(r['cale'],safe='/');lines.append(f"- [{Path(r['cale']).name}]({link}) — {r['ce_reprezinta']}. Stare: {r['stare_citire']}."+(f" Copie identică: "+r['duplicat_al'] if r['duplicat_al'] else ''))
  if r['extras_continut']:lines.append('  Extras: '+r['extras_continut'].replace('\n',' '))
  if r['ocr_cache']:lines.append('  OCR automat neverificat: '+r['ocr_cache'])
  if r.get('rezumat_verificat'):lines.append('  Situație documentată: '+r['rezumat_verificat'].replace('\n',' '))
 if not byfolder[folder]:lines.append('Fără fișiere directe; consultați subfolderele.')
 lines.append('')
(base/'HARTA_COMPLETA.md').write_text('\n'.join(lines),encoding='utf-8')
# One transaction, with only changed rows; never replace a live database.
db=sqlite3.connect(base/'cautare.sqlite',timeout=120);db.execute('PRAGMA busy_timeout=120000');db.execute('BEGIN IMMEDIATE')
current={path:(rid,sha) for rid,path,sha in db.execute('select rowid,cale,sha256 from documente')}
updates=0
for r in ordered:
 prev=current.get(r['cale'])
 if prev and prev[1]==r['sha256']:continue
 if prev:db.execute('DELETE FROM documente WHERE rowid=?',(prev[0],))
 tx=(root/r['text_cache']).read_text(encoding='utf-8')
 if r.get('ocr_cache'):tx+='\n\nOCR AUTOMAT NEVERIFICAT\n'+(root/r['ocr_cache']).read_text(encoding='utf-8')
 db.execute('INSERT INTO documente VALUES (?,?,?,?)',(r['cale'],r['ce_reprezinta']+'\n'+r.get('rezumat_verificat',''),tx,r['sha256']));updates+=1
db.commit();db.close()
print(json.dumps({'index_incremental':True,'files':len(ordered),'changed_files':len(updated),'sqlite_updates':updates,'workbook_refreshed':True,'existing_errors':len(stats.get('erori',[]))},ensure_ascii=False))

