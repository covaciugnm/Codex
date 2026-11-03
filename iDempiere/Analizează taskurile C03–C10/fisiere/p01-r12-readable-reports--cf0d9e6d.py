from pathlib import Path
import json,hashlib,datetime
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
pairs=[('executie/R12_fisiere/A08_Helper_rapoarte_lot02/Raport_A08.html','Raport_A08_lectura.html'),('executie/R12_fisiere/A09_Helper_corpus_lot02/Raport_A09_Helper_corpus_lot02.html','Raport_A09_Helper_corpus_lot02_lectura.html')]
style='<style id="readability-only">html,body{max-width:100%;box-sizing:border-box}body{overflow-wrap:anywhere}pre{max-width:100%;overflow-x:auto;white-space:pre-wrap}code{overflow-wrap:anywhere}table{display:block;max-width:100%;overflow-x:auto}th,td{min-width:120px;overflow-wrap:anywhere}@media(max-width:600px){body{padding:14px!important;margin:0!important}h1{font-size:25px!important}}</style>'
entries=[]
for origin,name in pairs:
 p=R/origin;q=p.with_name(name);assert not q.exists();s=p.read_text(encoding='utf-8');assert '</style>' in s
 n=s.replace('</style>','</style>'+style,1);assert n.replace(style,'',1)==s;q.write_text(n,encoding='utf-8')
 entries.append({'source':p.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'view':q.relative_to(R).as_posix(),'view_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'change':'Only additional CSS; removing the added style yields original bytes decoded as UTF-8. Original signed file unchanged.'})
o=R/'executie/Publicare_R12_Val02/Manifest_vizualizare_rapoarte.json';assert not o.exists();o.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entries':entries},ensure_ascii=False,indent=2),encoding='utf-8');print(o)
