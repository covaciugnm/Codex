from pathlib import Path
import json,hashlib,shutil,re,zipfile,xml.etree.ElementTree as ET,concurrent.futures,requests,os
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie\BI_iDempiere');L=Path(__file__).parent
# Reproducible generators; no credentials or credential-search logs are copied.
gen=R/'08_Administrare/generatoare';gen.mkdir(exist_ok=True)
for name in ['report_content.txt','build_report.py','prepare_excel.py','build_excel.mjs','build_annexes.py','excel_data.json']:
 t=(L/name).read_text(encoding='utf-8')
 t=t.replace("Path(r'\\\\192.168.100.169\\Comun\\00.Roboti\\iDempiere\\Documentatie\\BI_iDempiere')","Path(__file__).resolve().parents[2]")
 if name.endswith('.mjs'):t=t.replace("const root='//192.168.100.169/Comun/00.Roboti/iDempiere/Documentatie/BI_iDempiere';","const root=new URL('../../',import.meta.url).pathname.replace(/^\\/([A-Za-z]:)/,'$1');")
 (gen/name).write_text(t,encoding='utf-8')
(gen/'README.md').write_text('''# Generatoare

Sursele raportului, matricei și anexelor sunt păstrate pentru mentenanță. Python necesită python-docx; Excel folosește @oai/artifact-tool din runtime-ul de documente. Ordine: build_report.py, prepare_excel.py, build_annexes.py, build_excel.mjs. PDF-ul este exportat din DOCX cu Microsoft Word. Nu sunt incluse chei sau credențiale. Modificările documentare cer reverificarea surselor, regenerarea și controlul vizual.
''',encoding='utf-8')
versions=json.loads((R/'06_Surse_oficiale/versiuni_identificate.json').read_text(encoding='utf-8'))
def get_release(v):
 u=v[3];r=requests.get(u,timeout=60);p=R/'06_Surse_oficiale/Releases';p.mkdir(exist_ok=True);name=re.sub('[^A-Za-z0-9_]','_',v[0])+'.html'
 o=dict(product=v[0],version=v[1],url=u,http_status=r.status_code)
 if r.ok:(p/name).write_bytes(r.content);o.update(local='06_Surse_oficiale/Releases/'+name,sha256=hashlib.sha256(r.content).hexdigest())
 return o
releaseproof=list(concurrent.futures.ThreadPoolExecutor(5).map(get_release,versions[:5]));(R/'06_Surse_oficiale/Releases/provenienta.json').write_text(json.dumps(releaseproof,indent=2),encoding='utf-8')
# Check exported workbook XML: sheet counts, frozen headers/columns and auto-filters.
with zipfile.ZipFile(R/'02_Matrice/Comparatie_BI_iDempiere_Eva.xlsx') as z:
 ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 wb=ET.fromstring(z.read('xl/workbook.xml'));names=[n.attrib['name'] for n in wb.findall('s:sheets/s:sheet',ns)]
 assert len(names)==7,names
 panes=[]
 for i,n in enumerate(names,1):
  node=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));pane=node.find('s:sheetViews/s:sheetView/s:pane',ns);panes.append({'sheet':n,'pane':pane.attrib if pane is not None else None});assert pane is not None
 assert len([n for n in z.namelist() if re.match(r'xl/tables/table\d+.xml$',n)])==7
check={'date':'2026-10-08','xlsx_sheets':names,'frozen_panes':panes,'matrix_functions':64,'idempiere_components':37,'profile_examples_structurally_validated':3,'proposed_pilot_tests_not_executed':16,'renderer':'Microsoft Word PDF export; all 35 PDF pages visually reviewed; Artifact Tool sheet preview','native_excel_read_only_open':'Success: all 7 sheets loaded without repair','limitations':['No production DB accessed','No integration/runtime tests executed','Canonical DOCX renderer unavailable because soffice.exe is absent; Word export used']}
(R/'08_Administrare/verificari_livrare.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
# Credential patterns only on authored/audited material; report filenames, never matched contents.
patterns=[rb'-----BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{25,}',rb'github_pat_[A-Za-z0-9_]{35,}']
findings=[]
files=[Path(base)/name for base,dirs,names in os.walk(R) for name in names]
print('Enumerated',len(files),'files',flush=True)
for p in files:
 if '07_Manuale_complete' in p.parts or '06_Surse_oficiale' in p.parts or p.suffix.lower() not in ['.txt','.json','.md','.java','.py','.mjs','.sql','.html']:continue
 b=p.read_bytes()
 if any(re.search(q,b) for q in patterns):findings.append(str(p.relative_to(R)))
assert not findings,'Credential-pattern findings: '+str(findings)
dest=L/'eva-bi-docs/Documentatie/BI_iDempiere';dest.mkdir(parents=True,exist_ok=True)
def hashcopy(p):
 b=p.read_bytes();rel=p.relative_to(R);target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 return {'path':rel.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(24) as pool:manifest=list(pool.map(hashcopy,[p for p in files if p.name!='manifest_fisiere_sha256.json']))
(R/'08_Administrare/manifest_fisiere_sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(x['bytes']<100*1024*1024 for x in manifest)
shutil.copyfile(R/'08_Administrare/manifest_fisiere_sha256.json',dest/'08_Administrare/manifest_fisiere_sha256.json')
print('Packaged',len(manifest),'files',round(sum(x['bytes'] for x in manifest)/1024/1024,1),'MiB; credential-pattern scan clean; sheets',len(names))
