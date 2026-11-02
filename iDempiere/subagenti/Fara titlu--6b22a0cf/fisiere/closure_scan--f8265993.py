import datetime,hashlib,json,pathlib,re,subprocess
base=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');out=base/'executie/R6_pregatire/Istoric';tasks=[]
for f in (base/'executie/R5/taskuri').glob('Fisa_*.json'):
 t=json.loads(f.read_text(encoding='utf8')); 
 if t.get('missing_exact_closure_date_at_cutoff'):tasks.append({'task':t['task'],'canonical':t.get('canonical'),'first_registry_observed':t.get('first_dated_final_registry_observation',{}).get('registry_commit_time')})
assert len(tasks)==244
ssh_script=r'''
import datetime,json,subprocess,hashlib,re,unicodedata,collections,io,zipfile,xml.etree.ElementTree as ET
NAMES=__TASKS__; sha='6df998aee0e514d30856c461962afe99ebd0d113'; repo='/home/saga-server/Documents/EvA-Contab';g=lambda *args:subprocess.check_output(['git','-C',repo,*args]); roots=['Log-Istoric/LOG_ISTORIC.md','Log-Istoric/LOG_ISTORIC.xlsx','Documentatie/echipa-2026-10-09/00_LOG_OCUPARE_TASKURI.jsonl','Documentatie/echipa-2026-10-09/00_LOG_PROBLEME_CALITATE.jsonl','Documentatie/echipa-2026-10-09/00i_LOG_MODIFICARI_TOATE.md','Documentatie/echipa-2026-10-09/00d_STATUS_ECHIPE.md'];ids={x['task'] for x in NAMES}; alias={x['canonical']:x['task'] for x in NAMES if x['canonical']}; norm=lambda s:''.join(c for c in unicodedata.normalize('NFD',str(s).lower()) if unicodedata.category(c)!='Mn');rex=re.compile(r'(?<![\w.])(?:P(?P<proj>\d+)[.-](?:C\d+[.-])?)?T\d+(?:\.\d+)*(?![\w.])',re.I);cls=re.compile(r'\b(?:incheiat(?:a|e)?|inchis(?:a|e)?|finalizat(?:a|e)?|rezolvat(?:a|e)?|anulat(?:a|e)?|montat(?:a|e)?)\b');direct_grammar=re.compile(r'^\s*(?:[:;,—–-]\s*)?(?:a fost\s+|este\s+|e\s+)?(?:inchis|finalizat|anulat|montat|rezolvat|incheiat)(?:\b|$)');before_grammar=re.compile(r'\b(?:am (?:inchis|finalizat|anulat|montat|rezolvat|incheiat)|(?:inchiderea|finalizarea|anularea))\s+(?:taskului\s+)?$');results=[];sources=[]
def matches(s):
 out=[]
 for a in rex.finditer(s):
  txt=a.group().upper();pr=a.group('proj');
  if pr and int(pr)!=1:continue
  n=alias.get(txt) if '.C' in txt else re.search(r'T\d+(?:\.\d+)*$',txt).group();
  if n in ids:out.append((n,a.start(),a.end()))
 return out
def lineev(s,lno,source,ts=None,ss=None):
 mm=matches(s);most=norm(s); markers=list(cls.finditer(most));
 if not mm:return
 for name,start,end in mm:
  if not markers:continue
  la=most[end:end+75];lb=most[max(0,start-55):start];d=direct_grammar.match(la);b=before_grammar.search(lb);exact=bool(d or b);mtype='NOMINAL_CUVÂNT_ADIACENT' if exact else 'COAPARIȚIE_FĂRĂ_ATRIBUIRE';
  results.append({'source':source,'row':lno,'sha256_selected_line_or_virtual_row':hashlib.sha256(s.encode()).hexdigest(),'technical':name,'time_text':ts,'kind':mtype,'marker':(d.group().strip() if d else b.group().strip() if b else None),'event_type':'TEXT_DOCUMENTAR','sheet':ss})
def sdate(s):
 m=re.search(r'\b(?:\d{1,2}[./-]\d{1,2}[./-]20\d{2}|20\d{2}-\d{2}-\d{2})(?:[ T]\d{1,2}:\d{2}(?::\d{2})?)?',s[:90]);return m.group()if m else None
for fn in roots:
 oid=g('rev-parse',sha+':'+fn).decode().strip();blob=g('cat-file','blob',oid);md={'path':fn,'git_oid':oid,'sha256':hashlib.sha256(blob).hexdigest(),'bytes':len(blob)};sources.append(md)
 if fn.endswith('.xlsx'):
  ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','p':'http://schemas.openxmlformats.org/package/2006/relationships','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};md['sheet_row_counts']={}
  with zipfile.ZipFile(io.BytesIO(blob))as z:
   strings=[''.join(q.itertext())for q in ET.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml'in z.namelist()else [];wb=ET.fromstring(z.read('xl/workbook.xml'));rels={q.get('Id'):q.get('Target')for q in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
   for sh in wb.find('s:sheets',ns):
    target=rels[sh.get('{'+ns['r']+'}id')];x=ET.fromstring(z.read(target.lstrip('/')if target.startswith('/')else 'xl/'+target));rr=x.findall('s:sheetData/s:row',ns);md['sheet_row_counts'][sh.get('name')]=len(rr)
    for r in rr:
     cols=[]
     for c in r.findall('s:c',ns):
      v=c.findtext('s:v','',ns);cols.append(strings[int(v)]if c.get('t')=='s'else ''.join(c.find('s:is',ns).itertext())if c.get('t')=='inlineStr'and c.find('s:is',ns)is not None else v)
     l=' | '.join(cols);lineev(l,int(r.get('r')),fn,sdate(l),sh.get('name'))
 elif fn.endswith('.jsonl'):
  ll=blob.decode('utf8').splitlines();md['lines']=len(ll)
  for i,l in enumerate(ll,1):
   try:r=json.loads(l)
   except ValueError:continue
   project=str(r.get('proiect','')).upper();k=str(r.get('task','')).upper();code=str(r.get('cod','')).upper();mq=matches(code)
   if project and project!='P01':continue
   if k not in ids and len(mq)==1:k=mq[0][0]
   if k not in ids:continue
   if 'OCUPARE_'in fn and r.get('actiune')=='elibereaza':
    rs=norm(r.get('motiv',''));notes=norm(r.get('nota',''));m=cls.search(rs);notecls=cls.search(notes);sem='FĂRĂ_MARCAJ_FINAL' if not(m or notecls)else 'INDICIU_FINAL_ÎN_MOTIV' if m else 'INDICIU_FINAL_ÎN_NOTĂ';
    results.append({'source':fn,'row':i,'sha256_selected_line_or_virtual_row':hashlib.sha256(l.encode()).hexdigest(),'technical':k,'time_text':r.get('ora'),'kind':sem,'marker':m.group()if m else notecls.group()if notecls else None,'event_type':'ELIBERARE_SLOT','sheet':None})
   elif 'CALITATE' in fn and ('inchis'in norm(r.get('stare',''))or 'inchid' in norm(r.get('tip',''))):results.append({'source':fn,'row':i,'sha256_selected_line_or_virtual_row':hashlib.sha256(l.encode()).hexdigest(),'technical':k,'time_text':r.get('ora')or r.get('data'),'kind':'ÎNCHIDERE_INTRARE_CALITATE','marker':'închis','event_type':'CALITATE_DISTINCT_DE_TASK','sheet':None})
 else:
  ll=blob.decode('utf8').splitlines();md['lines']=len(ll)
  for i,l in enumerate(ll,1):lineev(l,i,fn,sdate(l))
# No notes, usernames, descriptions, customer data, or complete log lines leave the server.
out={};u=set()
for r in results:
 k=(r['source'],r['sheet'],r['row'],r['technical']);
 if k in u:continue
 u.add(k);out[k]=r
print(json.dumps({'sources':sources,'events':list(out.values())},ensure_ascii=False))
'''.replace('__TASKS__',repr(tasks))
r=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','python3 -'],input=ssh_script,encoding='utf8',capture_output=True,timeout=55);assert r.returncode==0,r.stderr[:370];scan=json.loads(r.stdout);counts={};per={};
for ev in scan['events']:
 counts[ev['kind']]=counts.get(ev['kind'],0)+1;per.setdefault(ev['technical'],[]).append(ev)
arr=[{**t,'documents_or_events':per.get(t['task'],[]),'disposition':'INDICIU_DOCUMENTAR_REEAUDIT_SEMANTIC' if per.get(t['task'])else 'NICIO_COINCIDENȚĂ_CU_MARCAJ_ÎN_CORPUSUL_SCANNAT'}for t in sorted(tasks,key=lambda t:t['task'])];doc={'schema':'eva.audit.r6.historical-date-candidates.v1','time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cutoff':'6df998aee0e514d30856c461962afe99ebd0d113','cohort_count':244,'intended':'Triaj nominal în jurnale istorice la cutoff. Un motiv de eliberare, o problemă de calitate închisă ori o coapariție nu constituie singure ora tranziției taskului P01.','privacy':'Căutarea în bloburi s-a făcut pe server. Nu s-au transferat linii de jurnal, comentarii private, conținutul notelor ori operațiuni în ERP. Numai ID, marker controlat, dată a înscrierii, număr rând și hash.','scanned':scan['sources'],'token_method':'Identificator tehnic exact și alias canonic dacă definit; niciun T36.46 atribuit din simplul T36, alți Pxx excluși la sintaxa nominală; documentele fără proiect specific necesită adjudecare. Markdown și XLSX pot fi oglinzi ale aceluiași jurnal și nu devin dovezi independente.','event_rows':len(scan['events']),'distinct_tasks_with_any_candidate_level':len(per),'by_event_kind':counts,'rows':arr,'exact_registry_closure_dates_promoted':0,'pending':'Validare semantică a markerelor nominale, cu scop, act și proiect. Timestamps de înregistrare nu devin automat date de închidere. În lipsă se păstrează intervalul sau NEDETERMINAT.'};target=out/'Cautare_evenimente_244.json';target.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:doc[k]for k in ['event_rows','distinct_tasks_with_any_candidate_level','by_event_kind']}));print('NOMINAL',[(r['technical'],r['time_text'],r['row'],r['marker']) for r in scan['events']if r['kind']=='NOMINAL_CUVÂNT_ADIACENT'][:36]);print('sha',hashlib.sha256(target.read_bytes()).hexdigest());
