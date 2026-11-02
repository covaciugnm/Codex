import os,sys,re,json,sqlite3,hashlib,html,unicodedata,collections,datetime,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
ROOT=Path(r'Z:\00. Persoane')
BASE=Path(__file__).resolve().parent
BASE.mkdir(parents=True,exist_ok=True)
CACHE=Path(r'C:\Users\User\AppData\Local\Temp\persoane-20261031')
OLD=ROOT/'00. Arhiva'/'00. Administrativ'/'Completare 2026-10-31'
REG=ROOT/'00. Registru persoane si documente.xlsx'
DB=BASE.parent/'inventar.sqlite'
TODAY=datetime.date(2026,11,1)
def norm(s):return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()).strip()
def keypath(s):return str(s).replace('/','\\').casefold()
def jsonread(p,default=None):
 try:return json.loads(p.read_text(encoding='utf-8-sig'))
 except Exception:return default
def linesread(p):
 if not p.exists():return []
 out=[]
 with p.open(encoding='utf-8-sig',errors='replace') as f:
  for l in f:
   try:out.append(json.loads(l))
   except Exception:pass
 return out
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def jsonl(p,rows):
 with p.open('w',encoding='utf-8') as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False,default=str)+'\n')
def scan_dir(path):
 dirs=[];fs=[];errs=[]
 try:
  with os.scandir(path) as it:
   for e in it:
    try:
     if e.is_dir(follow_symlinks=False):dirs.append(e.path)
     elif e.is_file(follow_symlinks=False):
      st=e.stat(follow_symlinks=False);fs.append({'path':e.path,'size':st.st_size,'mtime':st.st_mtime,'ext':Path(e.name).suffix.lower()})
    except Exception as ex:errs.append({'path':e.path,'error':str(ex)})
 except Exception as ex:errs.append({'path':str(path),'error':str(ex)})
 return dirs,fs,errs
def snapshot():
 started=datetime.datetime.now().isoformat();todo=[str(ROOT)];dirs=[];files=[];errors=[]
 with ThreadPoolExecutor(max_workers=12) as ex:
  while todo:
   futs=[ex.submit(scan_dir,p) for p in todo];todo=[]
   for f in as_completed(futs):
    ds,fs,es=f.result();dirs+=ds;todo+=ds;files+=fs;errors+=es
 result={'started':started,'finished':datetime.datetime.now().isoformat(),'directories':[str(ROOT)]+dirs,'files':files,'errors':errors}
 dump(BASE/'instantaneu_fizic.json',result);return result
def registry():
 import openpyxl
 w=openpyxl.load_workbook(REG,read_only=True,data_only=True)
 result={'source':str(REG),'mtime':REG.stat().st_mtime,'sheets':{}}
 for s in w:
  result['sheets'][s.title]=[list(r) for r in s.iter_rows(values_only=True)]
 w.close();dump(BASE/'registru_citit.json',result);return result
def grp(path):
 parts=Path(path).relative_to(ROOT).parts
 if not parts:return '00. RADACINA'
 if parts[0]=='00. Arhiva':return parts[1] if len(parts)>1 else '00. ARHIVA RADACINA'
 if len(parts)==1 and Path(path).suffix.lower() in ('.txt','.xlsx','.json','.jsonl','.log','.html','.md','.py'):return '00. RADACINA'
 return parts[0]
def cnpok(v):
 if not re.fullmatch('[1-9][0-9]{12}',v):return False
 n=sum(int(a)*int(b) for a,b in zip(v[:12],'279146358279'))%11
 if (1 if n==10 else n)!=int(v[-1]):return False
 try:datetime.date((1800 if v[0] in '34' else 2000 if v[0] in '56' else 1900)+int(v[1:3]),int(v[3:5]),int(v[5:7]))
 except ValueError:return False
 return True
def types(name):
 n=norm(name);out=[]
 pats={'CI / Buletin':r'\bCI\b|\bCEI\b|BULETIN|CARTE DE IDENTITATE','Pasaport':r'PASAPORT|PASSPORT','Permis conducere':r'PERMIS.*CONDUC|DRIV','Certificat nastere':r'NASTERE|NASTERTE','Certificat casatorie':r'CASATOR','CV':r'\bCV\b|CURRICULUM','Diploma bacalaureat':r'BACALAUREAT|DIPLOMA BAC\b','Diploma licenta':r'DIPLOM.*LICENT|LICENT.*DIPLOM','Diploma master':r'DIPLOM.*MASTER|MASTER.*DIPLOM','Certificat absolvire / formare':r'ABSOLV|FORMATOR|CERTIFICAT.*(CURS|FORMA|COMPETENT)','Contract individual de munca':r'\bCIM\b|CONTRACT.*MUNCA','Adeverinta':r'ADEVERINT','Raport Revisal / salariat':r'REVISAL|RAPORTSALARIAT|RAPORT SALARIAT','Documente multi-titular / dosar':r'DOSAR|ACTE COMUNE|CV SI DIPLOME'}
 for typ,pat in pats.items():
  if re.search(pat,n):out.append(typ)
 return out
def main():
 snap=jsonread(BASE/'instantaneu_fizic.json') if '--reuse-snapshot' in sys.argv else snapshot()
 reg=registry();sheets=reg['sheets'];files=snap['files'];pathset={keypath(x['path']) for x in files};groups=collections.defaultdict(list)
 for f in files:groups[grp(f['path'])].append(f)
 persons={norm(r[0]):{'row':i+1,'values':r} for i,r in enumerate(sheets['Persoane']) if i>=4 and r and r[0]}
 docs=[{'row':i+1,'values':r} for i,r in enumerate(sheets['Registru documente']) if i>=4 and r and r[0]]
 acts=[{'row':i+1,'values':r} for i,r in enumerate(sheets['Acte din dosare']) if i>=4 and r and r[0]]
 existingproblems=[{'row':i+1,'values':r} for i,r in enumerate(sheets['De verificat']) if i>=4 and r and r[0]]
 copies=linesread(OLD/'copies.jsonl');ocr=linesread(OLD/'ocr.jsonl');current_status=jsonread(OLD/'Stadiu.json',{})
 print('Jurnale si registru citite',flush=True)
 copybytarget=collections.defaultdict(list);sourcesbyperson=collections.defaultdict(list);hashes={};hashbasis={};textmeta={};texts={}
 for r in copies:
  if r.get('target'):
   copybytarget[keypath(r['target'])].append(r)
   if r.get('sha256'):hashes[keypath(r['target'])]=r['sha256'];hashbasis[keypath(r['target'])]='SHA-256 din jurnalul completarii, verificat la copiere'
  for p in r.get('persons',[]):sourcesbyperson[norm(p)].append(r)
 for r in ocr:
  if r.get('sha256'):textmeta[r['sha256']]=r
 try:
  con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True,timeout=60)
  for p,sha in con.execute('select path,sha256 from files where sha256 is not null'):hashes[keypath(p)]=sha;hashbasis[keypath(p)]='SHA-256 verificat de extractorul 2026-11-01'
  for sha,status,tp in con.execute('select sha256,status,text_path from documents'):
   if tp and status!='error':texts[sha]=DB.parent/tp
 except Exception:con=None
 for d in docs:
  r=d['values'];p=ROOT/str(r[12]);sha=str(r[14] or '')
  if sha:hashes.setdefault(keypath(p),sha);hashbasis.setdefault(keypath(p),'SHA-256 din registrul istoric')
 # Caches are read as evidence, never instructions. Missing text remains pending.
 needed={r.get('sha256') for r in copies if r.get('sha256')}
 needed|={v for v in hashes.values() if v}
 def load_text(sha):
  p=texts.get(sha,CACHE/'text'/(sha+'.txt'))
  try:return sha,p.read_text(encoding='utf-8-sig',errors='replace')
  except Exception:return sha,None
 with ThreadPoolExecutor(max_workers=12) as ex:
  loaded={k:v for k,v in ex.map(load_text,needed) if v is not None}
 print('Texte disponibile: '+str(len(loaded)),flush=True)
 issues=[];cnpcandidates=[];allrecords=[];allfileaudit=[]
 def issue(group,kind,certainty,detail,evidence,priority=2):
  v={'dosar':group,'tip':kind,'certitudine':certainty,'constatare':detail,'probe':evidence,'prioritate':priority};issues.append(v);return v
 for group,fs in sorted(groups.items()):
  name=group.split(' - ')[0];n=norm(name);person=persons.get(n);r=person['values'] if person else None;cnpmatch=re.search(r'(?<!\d)[1-9]\d{12}(?!\d)',group);foldercnp=cnpmatch.group() if cnpmatch else None
  isperson=not group.startswith(('00.','99.','.'))
  found=collections.defaultdict(list);sha_paths=collections.defaultdict(list);cover=collections.Counter();paths=[]
  for f in fs:
   p=f['path'];paths.append(p);sha=hashes.get(keypath(p));text=loaded.get(sha);meta=textmeta.get(sha,{})
   hints=types(Path(p).name)
   for t in hints:found[t].append(p)
   if sha:sha_paths[sha].append(p)
   status='text_disponibil' if text is not None else 'neextras_inca_sau_text_nepastrat'
   if meta.get('ocr_error'):status='eroare_ocr'
   elif meta.get('ocr_complete') and text is not None:status='ocr_disponibil_neverificat_manual'
   cover[status]+=1
   allfileaudit.append({'path':p,'dosar':group,'sha256':sha,'baza_amprentei':hashbasis.get(keypath(p)),'tipuri_indicate_de_nume':hints,'acoperire_continut':status,'marime':f['size'],'mtime':f['mtime'],'nota':'Tipurile deduse din nume sunt indicii, nu confirmari de titular sau continut.'})
  historical_docs=[d for d in docs if norm(d['values'][0])==n];historical_acts=[a for a in acts if norm(a['values'][0])==n]
  regproblems=[p for p in existingproblems if norm(p['values'][0])==n]
  source_records=sourcesbyperson[n];related=[];candidate_seen=set();name_tokens=set(n.split())
  if isperson:
   if not foldercnp:
    issue(group,'CNP necompletat in dosar','confirmat_in_evidenta','Dosarul nu are un CNP complet in denumire; nu rezulta ca CNP lipseste din toate actele.',[str(ROOT/group)],1)
   elif not cnpok(foldercnp):issue(group,'CNP cu control aritmetic neconform','necesita_verificare','CNP din numele dosarului nu trece controlul de lungime, data si cifra de control; verificati originalul.',[str(ROOT/group)],1)
   if not person:issue(group,'Persoana absenta din registrul istoric','confirmat_in_evidenta','Dosar fizic fara rand corespondent in registrul din 01.10.2026. Registrul este declarat istoric, deci actualizarea trebuie facuta in evidenta curenta.',[str(ROOT/group),str(REG)],2)
   if r:
    if str(r[2]).upper() in ('NEGASIT','DE VERIFICAT'):
     issue(group,'CI neidentificat in registrul istoric','negasit_in_verificarea_istorica','Registrul istoric nu identifica CI. Nu este o constatare de lipsa dupa verificarea integrala a tuturor surselor.',[f'{REG} | Persoane!C{person["row"]}']+found.get('CI / Buletin',[]),1)
    exp=r[6].date() if isinstance(r[6],datetime.datetime) else r[6] if isinstance(r[6],datetime.date) else None
    if exp and exp<TODAY:issue(group,'Termen CI inscris expirat','confirmat_din_registru_istoric',f'Termenul memorat in registru este {exp}; trebuie cautat actul mai nou. Nu deducem lipsa unui act nou.',[f'{REG} | Persoane!G{person["row"]}'],1)
   # Search the available associated source contents for CNP candidates. No assignment.
   possible=(list(source_records)+[{'source':f['path'],'sha256':hashes.get(keypath(f['path'])),'persons':[name]} for f in fs]) if not foldercnp else []
   for source in possible:
    sha=source.get('sha256');text=loaded.get(sha)
    if not text or sha in candidate_seen:continue
    candidate_seen.add(sha)
    candidates=sorted({x for x in (source.get('cnps') or textmeta.get(sha,{}).get('cnps') or re.findall(r'(?<!\d)[1-9]\d{12}(?!\d)',text)) if cnpok(x)})
    if not candidates:continue
    source_text_names={norm(x) for x in source.get('text_people',[])}|{norm(x) for x in textmeta.get(sha,{}).get('text_people',[])}
    if n not in source_text_names:
     normalized=norm(text)
     if not name_tokens or not name_tokens<=set(normalized.split()):continue
    if not foldercnp and candidates:
     for cnp in candidates:
      at=text.find(cnp);record={'dosar':group,'nume_dosar':name,'cnp_candidat':cnp,'cnp_in_document':len(candidates),'source':source.get('source'),'sha256':sha,'context':text[max(0,at-240):at+180],'statut':'CANDIDAT NECONFIRMAT - verificare titular si pagina obligatorie; nu se atribuie automat'};cnpcandidates.append(record);related.append(record)
   if related:issue(group,'CNP candidat in continut disponibil','candidat_neconfirmat',f'{len({x["cnp_candidat"] for x in related})} CNP-uri candidate apar in documente care mentioneaza numele. Verificati CI/CIM si contextul; documentele pot avea mai multi titulari.',list(dict.fromkeys(x['source'] for x in related)),1)
  broken=[];missingmeta=[]
  for d in historical_docs:
   v=d['values'];p=ROOT/str(v[12]);exists=keypath(p) in pathset
   if not exists:
    try:exists=p.is_file()
    except Exception:pass
   if not exists:broken.append({'source':str(p),'row':d['row']})
   miss=[]
   for idx,label in [(1,'CNP'),(4,'Serie'),(5,'Numar'),(6,'Emitere'),(7,'Valabilitate'),(8,'Emitent')]:
    if v[idx] is None or norm(v[idx]) in ('NEIDENTIFICAT','NEIDENTIFICATA','CNP DE COMPLETAT','DE VERIFICAT',''):
     miss.append(label)
   if miss:missingmeta.append({'source':str(p),'row':d['row'],'fields':miss,'type':v[2]})
  if broken:issue(group,'Referinta istorica fara fisier la calea memorata','confirmat_cale_neaccesibila',f'{len(broken)} referinte din registru nu au fisier la calea memorata; poate fi redenumire, mutare sau lipsa de acces, nu dovada stergerii.',[x['source'] for x in broken],1)
  duplicates=[{'sha256':sha,'paths':ps,'basis':hashbasis.get(keypath(ps[0]))} for sha,ps in sha_paths.items() if len(ps)>1]
  main_dups=[d for d in duplicates if sum('00. Arhiva' not in p for p in d['paths'])>1]
  if main_dups:issue(group,'Copii identice repetate in dosarul principal','sha256_jurnal_sau_extractor',f'{len(main_dups)} continuturi au mai multe cai in dosarul principal. Poate fi duplicare radacina/categorie; nu se sterge nimic automat.',[p for d in main_dups for p in d['paths']],3)
  if cover.get('neextras_inca_sau_text_nepastrat'):issue(group,'Acoperire continut incompleta','neextras_inca',f'{cover["neextras_inca_sau_text_nepastrat"]} fisiere nu au text integral disponibil in cache-urile citite. Lipsurile de acte nu pot fi confirmate pentru aceste fisiere.',[str(ROOT/group)],2)
  record={'dosar':group,'tip_grupare':'persoana' if isperson else 'administrativ_comun_neatribuit','fisiere':len(fs),'marime_totala':sum(f['size'] for f in fs),'cnp_din_dosar':foldercnp,'cnp_in_registru':r[1] if r else None,'rand_persoane':person['row'] if person else None,'tipuri_indicate_de_fisiere':dict(found),'documente_in_registru_istoric':historical_docs,'acte_in_dosare_istoric':historical_acts,'tipuri_negasite_istoric':list(dict.fromkeys(str(r[11]).split('; '))) if r and r[11] else [],'nota_tipuri_negasite':'Categorii istorice, nu lista obligatorie pentru fiecare persoana. Nu confirma lipsa din toate sursele.','date_necompletate_in_registru':missingmeta,'probleme_istorice':regproblems,'referinte_fara_cale':broken,'duplicate_hash':duplicates,'acoperire_continut':dict(cover),'cnp_candidati_neconfirmati':related,'dovezi_surproduse_externe':source_records,'surse':paths,'concluzie':'AUDIT INVENTAR SI EVIDENTE EFECTUAT; verificarea manuala a tuturor paginilor NU este incheiata.'}
  allrecords.append(record)
  print('Auditat '+group,flush=True)
 # Every physical directory, including empty categories, receives a record.
 folders=[]
 for directory in snap['directories']:
  pref=keypath(directory)+'\\';ff=[f for f in files if keypath(f['path']).startswith(pref)];direct=[f for f in ff if keypath(str(Path(f['path']).parent))==keypath(directory)]
  folders.append({'folder':directory,'grupare':grp(directory) if Path(directory)!=ROOT else '00. RADACINA','fisiere_directe':len(direct),'fisiere_inclusiv_subdosare':len(ff),'gol':not ff,'extensii':dict(collections.Counter(f['ext'] for f in ff)),'statut':'inventariat; continut partial verificat prin cache si registru'})
 known=[{'dosar':'BURIAN MARIANA SIMONA - CNP de completat','tip':'CNP si CI gasite in afara dosarului organizat','certitudine':'confirmat_vizual_de_agentul_principal_si_in_CIM','constatare':'CNP 2741207011091; CI AX512258; emitere 20.03.2013; termen 07.12.2023. Este disponibil un act vechi, nu dovada unui CI actual. Corectie in curs la agentul principal.','probe':[r'Z:\2019\SCANARI\Copii Buletine\Burian Mariana.JPG',r'Z:\00. Persoane\BURIAN MARIANA SIMONA - CNP de completat\05. Contracte personale\CNP de completat - BURIAN MARIANA SIMONA - Cim 307 - Burian Simona Mariana - modificat 2014.07.29 - 58c675ac9d.pdf'],'prioritate':1}, {'dosar':'COVACIU COSMIN-ADRIAN - 1721019120687','tip':'Continut diferit de titlul fisierului','certitudine':'confirmat_vizual_de_agentul_principal','constatare':'Diploma.Formator-Covaciu.Cosmin (ac559469cb.pdf) contine certificat auditor mediu. Nu confirma diploma de formator. In 99. De verificat au fost confirmate bacalaureat, licenta, doua masterate, INA si auditor mediu.','probe':[r'Z:\00. Persoane\COVACIU COSMIN-ADRIAN - 1721019120687\03. Diplome si Cursuri\1721019120687 - COVACIU COSMIN-ADRIAN - Diploma.Formator-Covaciu.Cosmin - modificat 2012.07.11 - ac559469cb.pdf'],'prioritate':1}]
 issues=known+issues
 summary={'as_of':str(TODAY),'snapshot_started':snap['started'],'snapshot_finished':snap['finished'],'files':len(files),'physical_directories':len(folders),'groups':len(groups),'person_groups':sum(x['tip_grupare']=='persoana' for x in allrecords),'historic_registry_persons':len(persons),'historic_registry_documents':len(docs),'historic_attached_acts':len(acts),'source_texts_available':len(loaded),'issues':len(issues),'issues_by_type':dict(collections.Counter(x['tip'] for x in issues)),'cnp_candidates_records':len(cnpcandidates),'groups_with_cnp_candidates':len({x['dosar'] for x in cnpcandidates}),'scan_errors':snap['errors'],'ongoing_existing_pipeline':current_status,'audit_scope':'Fiecare dosar/subfolder fizic si fiecare fisier din instantaneu; reconciliere cu evidenta istorica si jurnalul curent. Nu audit manual integral al tuturor paginilor.','absence_rule':'Nicio categorie generica nu este declarata act obligatoriu. NEGASIT ramane negasit in acoperirea indicata; lipsa absoluta nu este confirmata.'}
 dump(BASE/'sumar_audit.json',summary);jsonl(BASE/'audit_persoane.jsonl',allrecords);jsonl(BASE/'audit_fiecare_folder.jsonl',folders);jsonl(BASE/'audit_fiecare_fisier.jsonl',allfileaudit);jsonl(BASE/'probleme_si_probe.jsonl',issues);jsonl(BASE/'cnp_candidati_neconfirmati.jsonl',cnpcandidates)
 (BASE/'dosare').mkdir(exist_ok=True)
 for r in allrecords:
  fn=re.sub(r'[<>:"/\\|?*]','_',r['dosar'])+'.txt';lines=[r['dosar'],r['concluzie'],f'Fisiere: {r["fisiere"]}',f'CNP in dosar: {r["cnp_din_dosar"]}',f'Acoperire: {r["acoperire_continut"]}','\nACTE INDICATE DE NUMELE FISIERELOR (titularul/continutul necesita verificare):']
  for t,ps in r['tipuri_indicate_de_fisiere'].items():lines.append(t+'\n'+'\n'.join(ps))
  lines+=['\nCONSTATARI SI PROBE:']
  for i in issues:
   if i['dosar']==r['dosar']:lines += [i['tip']+' | '+i['certitudine'],i['constatare']]+i['probe']+['']
  lines+=['\nCATEGORII NEGASITE IN REGISTRUL ISTORIC (NU OBLIGATORII):','; '.join(r['tipuri_negasite_istoric'])]
  lines+=['\nCAMPURI ISTORICE NECOMPLETATE (unele neaplicabile):',json.dumps(r['date_necompletate_in_registru'],ensure_ascii=False,default=str)]
  (BASE/'dosare'/fn).write_text('\n'.join(lines),encoding='utf-8')
 body=[]
 for r in allrecords:
  pp=[i for i in issues if i['dosar']==r['dosar']];fn=re.sub(r'[<>:"/\\|?*]','_',r['dosar'])+'.txt'
  body.append('<tr><td><a href="dosare/'+html.escape(fn)+'">'+html.escape(r['dosar'])+'</a></td><td>'+str(r['fisiere'])+'</td><td>'+html.escape(str(r['cnp_din_dosar'] or 'NECOMPLETAT'))+'</td><td>'+html.escape(str(r['acoperire_continut']))+'</td><td>'+html.escape('; '.join(dict.fromkeys(i['tip'] for i in pp)))+'</td></tr>')
 report='<!doctype html><meta charset="utf-8"><title>Audit dosare persoane</title><style>body{font:15px system-ui;color:#162836;margin:32px;max-width:1600px}table{border-collapse:collapse;width:100%}th,td{padding:12px;text-align:left;border-bottom:1px solid #d3dce4;vertical-align:top}th{background:#edf2f5;position:sticky;top:0}input{font:inherit;padding:12px;width:75%;margin:20px 0}a{color:#18577e}p{max-width:1100px;line-height:1.5}.note{padding:16px;background:#fff4da}</style><h1>Audit dosare persoane</h1><p>'+html.escape(f'{summary["files"]} fisiere, {summary["physical_directories"]} directoare fizice, {summary["person_groups"]} dosare de persoana. Instantaneu {summary["snapshot_finished"]}.')+'</p><p class="note">Auditul inventarului si evidentelor acopera fiecare dosar. OCR-ul general continua. Nu declarăm lipsa absoluta a unui act pe baza numelui fisierului, a unui CV sau a registrului istoric. Categoriile NEGASIT nu sunt o lista de acte obligatorii.</p><p>Deschideti fiecare dosar pentru constatarile concrete si sursele sale. CNP-urile candidate sunt doar indicii si necesita confirmarea titularului in original. Mariana Burian si etichetarea diplomei lui Cosmin au constatari confirmate separat.</p><input id="q" placeholder="Cauta dosarul sau problema"><table><thead><tr><th>Dosar si fisa audit</th><th>Fisiere</th><th>CNP din dosar</th><th>Acoperire continut</th><th>Constatari</th></tr></thead><tbody>'+''.join(body)+'</tbody></table><script>const rows=[...document.querySelectorAll("tbody tr")];q.oninput=()=>{const s=q.value.toLowerCase();for(const r of rows)r.hidden=!r.textContent.toLowerCase().includes(s)}</script>'
 (BASE/'Audit dosare.html').write_text(report,encoding='utf-8')
 (BASE/'Sumar audit.txt').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str)+'\n\nConstatari confirmate prioritare:\n'+json.dumps(known,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2,default=str),flush=True)
if __name__=='__main__':main()
