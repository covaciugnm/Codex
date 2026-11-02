import json,csv,html,hashlib,shutil,sqlite3,datetime
from pathlib import Path
B=Path(r'D:\Codex\iFLYTEK-audit');P=B/'deliverable';R=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository');A=R/'apk-analysis-2026-11-01';D=R/'apk-protocol-audit-2026-11-01'
cat=json.loads((A/'catalog.json').read_text());db=sqlite3.connect(P/'02_Functii_variabile/catalog.sqlite');known={r[0] for r in db.execute('select distinct artifact from aot_functions')};rows=[];snapshots={}
for v in cat['versions']:
 m=json.loads((A/v['manifest']).read_text());dc=m.get('decompilation',{});details=[]
 for item in dc.get('components',[]):
  file=A/item['manifest'];data=json.loads(file.read_text());args=data.get('command',{}).get('args',[]);out=args[args.index('-d')+1] if '-d' in args else ''
  count=data.get('javaFiles')
  if count is None:count=sum(e['path'].endswith('.java') for e in data.get('entries',[]))
  details.append({'component':item['component'],'status':data.get('status'),'exit_code':data.get('exitCode'),'java_files':count,'count_basis':'javaFiles metadata' if data.get('javaFiles') is not None else 'Java entries in reused source manifest','known_jadx_errors':data.get('knownJadxErrors'),'source_manifest':str(file),'output_directory':out,'physical_output_exists':Path(out).exists() if out else None,'manifest_sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
  snapshots[str(file)]=details[-1]
 libs=[e for e in m['entries'] if e['path'].endswith('/libapp.so')];covered=[e for e in libs if e['sha256'] in known]
 row={'variant':v['variant'],'package':v['package'],'version':v['version'],'apk_sha256':v['sourceSha256'],'existing_decompilation_status':dc.get('status','not recorded'),'component_results':json.dumps(details,ensure_ascii=False),'java_files_reported':sum(x['java_files'] or 0 for x in details),'dart_aot_libraries':len(libs),'dart_aot_exact_hash_catalogued':len(covered),'aot_reuse_paths':'; '.join(e['path'] for e in covered),'remaining_work':'Review documented decompiler errors and protocol evidence; reuse existing outputs. '+('AOT recovery required for remaining distinct library hashes.' if len(covered)<len(libs) else 'Reuse exact-hash AOT catalog; runtime confirmation still open.'),'source_manifest':str(A/v['manifest'])}
 rows.append(row)
 print(row['variant'],row['existing_decompilation_status'],row['java_files_reported'],'AOT',len(covered),'/',len(libs),flush=True)
def js(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
with (P/'01_Inventar/existing-work-reconciliation.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
js(P/'01_Inventar/existing-work-reconciliation.json',{'checked_at':datetime.datetime.now().astimezone().isoformat(),'basis':'Current version manifests + decompiler manifests; exact libapp SHA256 match against recovered AOT catalog. No APK was decompiled again. Physical output existence is separate from reported source counts; not a fresh hash verification of every Java file.','versions':rows,'unique_decompiler_manifests':list(snapshots.values())})
versions=json.loads((P/'01_Inventar/versions.json').read_text());bysha={r['apk_sha256']:r for r in rows}
for v in versions:
 v['decompilation_status']=bysha[v['sha256']]['existing_decompilation_status'];v['existing_work_reference']='existing-work-reconciliation.csv'
js(P/'01_Inventar/versions.json',versions)
with (P/'01_Inventar/versions.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(versions[0]));w.writeheader();w.writerows(versions)
view=[{k:r[k] for k in ['variant','existing_decompilation_status','java_files_reported','dart_aot_libraries','dart_aot_exact_hash_catalogued','remaining_work']} for r in rows];cols=list(view[0]);tab='<table><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in cols)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in cols)+'</tr>' for r in view)+'</table>'
doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>Lucrări iFLYTEK existente</title><style>body{font:14px system-ui;margin:30px;color:#183c53}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border:1px solid #ccd9e1;padding:10px;text-align:left;overflow-wrap:anywhere}th{background:#e7eff5}p{line-height:1.6}</style><h1>Decompilări și documentație deja existente</h1><p><a href="index.html">Raport principal</a>. Am actualizat situația pe baza inventarelor curente. Rezultatele existente se reutilizează; nu au fost redecompilate pentru această corelare.</p><p>„complete-with-documented-limitations” înseamnă că etapa a fost efectuată cu limite consemnate. Rezultatele componentelor pot fi „partial-decompilation”, cu exit code 3 și fișiere Java disponibile. Aceasta nu înseamnă lipsă totală de cod. Numerele Java sunt cele raportate în manifestele de decompilare; nu au fost reverificate individual toate fișierele Java.</p><p>AOT se reutilizează oriunde biblioteca are exact același SHA256, inclusiv în variante derivate. Bibliotecile cu hash diferit necesită verificare distinctă; existența unei decompilări Java nu confirmă recuperarea codului Dart.</p>'+tab+'<p><a href="../01_Inventar/existing-work-reconciliation.json">Dovezi: directoare, manifeste, hashuri și stări pe componentă</a>.</p></html>'
(P/'00_Raport/lucrari-existente.html').write_text(doc,encoding='utf-8')
index=P/'00_Raport/index.html';s=index.read_text(encoding='utf-8');notice='<div class="card"><h2>Actualizare: lucrări deja existente</h2><p><a href="lucrari-existente.html">Situația actualizată a decompilărilor și documentației existente, pentru fiecare APK</a>. Rezultatele existente sunt reutilizate. Starea Java și starea recuperării Dart AOT sunt urmărite separat. Tabelul actualizat înlocuiește orice stare de decompilare mai veche din prima verificare.</p></div>'
if 'Actualizare: lucrări deja existente' not in s:s=s.replace('</nav>','</nav>'+notice)
index.write_text(s,encoding='utf-8')
check=P/'06_Audit/checklist-corecturi.csv'
with check.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;checks=list(reader)
for c in checks:
 if c['id']=='A09':c['observation']='Reconciliat cu manifestele curente, pe componente, inclusiv cod Java existent si exit codes. Vezi 01_Inventar/existing-work-reconciliation.csv. Nu se repeta decompilarea existenta.'
with check.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(checks)
audit=P/'06_Audit/audit.json';data=json.loads(audit.read_text());data['checks']=checks;data['existing_work_reconciliation']='../01_Inventar/existing-work-reconciliation.json';js(audit,data)
shutil.copy2(B/'reconcile_existing.py',P/'07_Reproducere/reconcile_existing.py')
old=json.loads((P/'SHA256SUMS.json').read_text());hashes={e['path']:e for e in old}
changed=['01_Inventar/existing-work-reconciliation.csv','01_Inventar/existing-work-reconciliation.json','01_Inventar/versions.csv','01_Inventar/versions.json','00_Raport/index.html','00_Raport/lucrari-existente.html','06_Audit/checklist-corecturi.csv','06_Audit/audit.json','07_Reproducere/reconcile_existing.py']
for rel in changed:
 f=P/rel;hashes[rel]={'path':rel,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()};target=D/rel;target.parent.mkdir(exist_ok=True);shutil.copy2(f,target);assert hashlib.sha256(target.read_bytes()).hexdigest()==hashes[rel]['sha256']
js(P/'SHA256SUMS.json',list(hashes.values()));shutil.copy2(P/'SHA256SUMS.json',D/'SHA256SUMS.json');print('UPDATED AND VERIFIED',len(changed),'files',flush=True)
