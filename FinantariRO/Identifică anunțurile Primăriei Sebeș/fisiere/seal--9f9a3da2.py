import json,sqlite3,csv,gzip,hashlib,html,shutil,re
from pathlib import Path
from lxml import etree
B=Path(r'D:\Codex\iFLYTEK-audit');P=B/'deliverable';C=sqlite3.connect(P/'02_Functii_variabile/catalog.sqlite');checks=[]
def ck(name,ok,detail=''):
 checks.append({'check':name,'pass':bool(ok),'detail':detail});assert ok,(name,detail)
ck('SQLite integrity_check',C.execute('pragma integrity_check').fetchone()[0]=='ok')
ck('36 DEX / 188 ELF',C.execute("select count(*) from artifacts where kind='dex'").fetchone()[0]==36 and C.execute("select count(*) from artifacts where kind='elf'").fetchone()[0]==188)
ck('ELF debug verification coverage',C.execute('select count(*) from elf_validation').fetchone()[0]==188)
ck('No parser errors',C.execute('select count(*) from errors').fetchone()[0]==0)
ck('No concrete methods missing code',C.execute('select count(*) from methods where defined=1 and code_offset=0 and (flags & 1280)=0').fetchone()[0]==0)
for table in ['methods','fields','classes','variables','aot_functions','aot_field_offsets','evidence','key_candidates','protocol_constants','native_symbols','native_dependencies']:
 files=list(P.rglob(table+'.csv.gz'));ck('Export exists '+table,len(files)==1)
 with gzip.open(files[0],'rt',encoding='utf-8-sig',newline='') as f:n=sum(1 for _ in csv.reader(f))-1
 count=C.execute('select count(*) from '+table).fetchone()[0];ck('Export row count '+table,n==count,str(count))
prior=json.loads((P/'05_Comparatii/prior-catalog-comparison.json').read_text());ck('Prior methods and fields exact match',all(prior[k]==0 for k in ['methods_only_prior','methods_only_current','fields_only_prior','fields_only_current']))
v=json.loads((P/'06_Audit/independent-validation.json').read_text());ck('Independent parser covers every DEX',set(v)=={r[0] for r in C.execute("select hash from artifacts where kind='dex'")})
sampled=sum(x.get('sampled_code_methods',0) for x in v.values());ck('Independent instruction sample nonempty',sampled>0,str(sampled))
for f in (P/'00_Raport').glob('*.html'):
 doc=etree.HTML(f.read_text(encoding='utf-8'));bad=[]
 for a in doc.xpath('//a[@href]'):
  target=a.get('href')
  if not target.startswith(('http:','https:','#')) and not (f.parent/target).exists():bad.append(target)
 ck('Local report links '+f.name,not bad,str(bad))
ck('Manifest coverage',len(list((P/'01_Inventar/manifests').glob('*.xml')))==36)
for f in (P/'01_Inventar/manifests').glob('*.xml'):
 x=etree.parse(str(f));ns='{http://schemas.android.com/apk/res/android}'
 for e in x.iter('meta-data'):
  if re.search('key|secret|token|password',e.get(ns+'name',''),re.I) and e.get(ns+'value') is not None:ck('Metadata credential redaction '+f.name,e.get(ns+'value')=='[REDACTAT]')
htmlp=P/'00_Raport/index.html';s=htmlp.read_text(encoding='utf-8');extra='''<div class="card"><h2>Dovezi suplimentare</h2><p><a href="dovezi-si-verificari.html">Conectare, resurse de limbă, manifest și planul de verificare</a> · <a href="../02_Functii_variabile/data-dictionary.json">Dicționarul datelor și unitățile offseturilor</a> · <a href="../06_Audit/delivery-reaudit.json">Reauditul fișierelor livrate</a></p><p>Față de APK-ul oficial, canalele FY10030001/FY10030002 au aceleași semnături și hashuri brute ale instrucțiunilor DEX, iar cinci căi de fișiere au hashuri diferite. Acest rezultat nu înseamnă identitate integrală a aplicațiilor. Pentru versiunile cu multe nume obfuscate diferite, numărul mare de diferențe nu demonstrează un număr egal de funcții noi.</p></div>'''
if 'Dovezi suplimentare' not in s:s=s.replace('</nav>','</nav>'+extra)
htmlp.write_text(s,encoding='utf-8')
for file in ['supplement.py','seal.py']:shutil.copy2(B/file,P/'07_Reproducere'/file)
shutil.copy2(B/'supplement.log',P/'07_Reproducere/supplement.log')
js=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
js(P/'07_Reproducere/toolchain-availability.json',{'checked':'2026-11-01','installed_cpp_toolchain':'Visual Studio Build Tools 2019 16.11 (vswhere verified)','modern_cpp_tools_in_path':False,'wsl_docker_in_path':False,'available_prior_blutter_binary':'Linux toolchain bundle for Dart 3.10.9 arm64; no compatible Windows executable recovered from bundle','upstream':'https://github.com/worawit/blutter','upstream_scope':'Android libapp.so arm64 only; recent Dart; compatible tool build required per Dart version','important_limit':'Bavvo 1.0.1222 delivered split is armeabi-v7a. Its AOT analysis is not covered by the prior arm64 tool. Windows support exists upstream but modern C++ build prerequisites are not installed here. No system-wide compiler/VM installation attempted.'})
js(P/'06_Audit/delivery-reaudit.json',{'result':'PASS for delivered static artifacts; AOT across all versions and runtime validation remain OPEN','checks':checks,'sampled_code_methods':sampled,'aot_symbol_entries':C.execute('select count(*) from aot_functions').fetchone()[0],'aot_unique_addresses':C.execute('select count(distinct address) from aot_functions').fetchone()[0]})
C.close()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
files=[{'path':str(f.relative_to(P)).replace('\\','/'),'bytes':f.stat().st_size,'sha256':sha(f)} for f in P.rglob('*') if f.is_file() and f.name!='SHA256SUMS.json'];js(P/'SHA256SUMS.json',files)
print('REAUDIT PASS',len(checks),'checks',len(files),'files',sum(x['bytes'] for x in files),'bytes',flush=True)
