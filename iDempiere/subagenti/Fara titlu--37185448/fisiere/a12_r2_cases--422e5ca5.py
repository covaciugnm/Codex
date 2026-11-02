from pathlib import Path
from collections import defaultdict,Counter
from functools import lru_cache
import json,re,gzip,hashlib,datetime,html,shutil,sys
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');D=Path(r'D:\CodexWork\A12_evidence_20261102');E=B/'executie';R=E/'R2';T=R/'taskuri';T.mkdir(exist_ok=True)
def rd(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def hs(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
def uniq(i):return list(dict.fromkeys(i))
def norm(t):return ' '.join(str(t or '').lower().split())
def tidy(t):return re.sub(r'\s+',' ',str(t or '')).strip()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
P=rd(D/'map.json')['target_paths'];PP=rd(D/'map_r2_plans.json');rootmanifest=rd(B/'capturi/MANIFEST.json');snapshot=rootmanifest['ended_utc'];sha=rootmanifest['repo_sha']
@lru_cache(maxsize=800)
def blob(o):return gzip.decompress((D/'blobs'/(o+'.gz')).read_bytes()).decode('utf-8-sig','replace')
def pathending(s):return next(p for p in P if p.endswith(s))
def readp(p):return json.loads(blob(P[p]))
p99=pathending('/99_PROPUNERE_PAS3.json');p99a=pathending('/99a_DECIZII_PROPRIETAR_PAS3.md');p30=pathending('/30_decizii_P01.json');p32=pathending('/32_RASPUNSURI_PROPRIETAR.md');p285=pathending('/T285-toate-proiectele-pe-capitole/plan.json');pr285=pathending('/T285-toate-proiectele-pe-capitole/10_raport.md');pold=pathending('/00_DECIZIE_PROPRIETAR_APLICATIA_VECHE_20261023.md');pcard={Path(p).stem:p for p in P if '/cartele_pas3/' in p and p.endswith('.json')}
d99=readp(p99);d30={x['id']:(i,x)for i,x in enumerate(readp(p30)['decizii'])};d285={x['id']:(i,x)for i,x in enumerate(readp(p285)['proiecte']['P01']['strange'])};group=rd(B/'A12_index_taskuri.json'); ix={x['source_id']:x for x in group['rows']};queued={k for k,x in ix.items() if x['individual_review']};rr=rd(B/'capturi/00_STATUS_TASKURI.json');reg={x['id']:(i,x) for i,x in enumerate(rr)};led=rd(E/'A11_ledger_651_fise.json');review={v['source_id']:v for v in led['records']};hist=rd(E/'A12_istoric_git_stari.json');histidx={x['id']:(i,x) for i,x in enumerate(hist['rows'])};first=rd(E/'R1/A12_raport.json');firstrows={f['id']:f for f in first['records']};a11=rd(E/'A11_control_lot1.json')
manual=B.parent/'2026.10.22 Task C03-C10/Manual_arhitectura_2026-10-25';cm=rd(manual/'Date_manual_C03.json');vm=rd(manual/'Date_manual_C10.json');rz=defaultdict(list);fiches=defaultdict(list)
for i,x in enumerate(cm['rz_mapping']):rz['P01.'+x['old_task_id']].append((i,x))
for i,x in enumerate(vm['source_fiche_mapping_59']):
 m=re.search(r'\bP01\.C10\.T\d{4}(?:\.\d+)?\b',x['source_title']); 
 if m:fiches[m[0]].append((i,x))
zone_reports={};fi={};mhsi={};ae=[]
for n in range(1,11):
 p=E/f'A{n:02d}_raport.json'
 if not p.exists():continue
 z='A%02d'%n; zone_reports[z]=rd(p);mhsi[z]=hs(p)
 for j,f in enumerate(zone_reports[z].get('findings',[])):
  if isinstance(f,dict):fi[f.get('id') or f.get('finding_id')]=(z,j,f)
for name,v in [('A11/independent_results',a11['independent_results'])]:
 for j,f in enumerate(v):ae.append((j,f))
evidence={};inverse=defaultdict(list);rev_dir=R/'inputs';rev_dir.mkdir(exist_ok=True)
def ev(typ,source,pointer,content,hash_,limit,date=None):
 key=typ+'|'+source+'|'+str(pointer)+'|'+str(hash_);code='EV2-'+hashlib.sha256(key.encode()).hexdigest()[:22]
 val={'level':typ,'source':source,'pointer':pointer,'sha_or_oid':hash_,'dated_when_known':date,'content_or_observation':content,'limit':limit}
 if code not in evidence:evidence[code]=val
 return code
def mdev(path,ptr,content,reason,typ='HISTORICAL_REFERENCE'):
 return ev(typ,path,ptr,content,P[path],reason)
def json_ev(file,ptr,val,lim,typ='AUDIT_EXECUTION'):
 path=E/file
 return ev(typ,'executie/'+file,ptr,val,hs(path),lim)
def add_req(reqs,k,cat,text,sourceev,expected=None,actor=None,pre=None,layer=None,action=None,uncertain=None,entire=None):
 if not str(text).strip():return None
 key=(cat,src:=str(sourceev),norm(text));slot=len(reqs)+1
 if any(v['_k']==key for v in reqs):return None
 v={'_k':key,'id':k+'-R2-'+f'{slot:03d}','kind':cat,'normative_content':text,'source_evidence_id':sourceev,'actor_or_role':actor or 'Rolul de afaceri trebuie stabilit din sursă; responsabil de verificare: '+ix[k]['chapter_owner'],'preconditions':pre or ('Execută controlul asociat pe versiunea '+sha+' în mediu izolat, cu rol autorizat și date dedicate. Nu se inventează precondiții istorice nescrise.'),'layers':layer or ['funcție de afaceri','probă pe rol','persistență conform sursei'],'expected_oracle':expected or text,'current':{'status':'NEEXECUTAT','observed':None,'evidence_ids':[]},'closure':{'status':'INCONCLUDENT','observed':None,'evidence_ids':[]},'constraint':uncertain or 'Nu există încă probă independentă specifică pentru rezultatul integral la închidere și astăzi.','next_action':action or ('Pregătește fixtura pentru '+ix[k]['display_title']+', apoi compară rezultatul persistent cu criteriul citat. Documentează versiunea, rolul, înainte/după și contraexemplul.'),'source_provenance_limit':entire}
 reqs.append(v);return v
def exec_obs(req,status,observed,ids,domain='current'):
 req[domain]={'status':status,'observed':observed,'evidence_ids':uniq(ids)}
def originals(t):
 s=(t.get('cerere_proprietar') or '').strip();orig=t.get('origine') or {}
 if not s or re.match(r'^\s*[\[(]?(?:(?:cererea\s+)?nescris|reconstituit|necunoscut|fără cerere|nu e scris)',s,re.I):return None,None,None
 if re.search(r'nu e citat direct|nu este citat direct|nescrisă la înregistrare',s,re.I):return None,None,None
 # Quotes are selected from the field actually carrying the request. Narration by an orchestrator (origine.text)
 # and an unlabelled retrospective log must not silently become a verbatim owner requirement.
 quotes=re.findall(r'«([^«»]+)»',s)
 if quotes:
  words=' '.join(quotes).strip()
  if len(words)<18 or words.lower() in ('avem softul nostru, eva-accounting','ok corecteaza eva'):return None,None,None
  return words,'cerere_proprietar',orig.get('data') if isinstance(orig,dict) else None
 return None,None,None
def roleby(t):
 return 'operator de probă cu dreptul documentat (istoric nedeterminat dacă sursa nu îl numește); responsabil de verificare '+ix[t]['chapter_owner']
def relevantplans(k):
 pp=PP.get(k,[]);main=[p for p in pp if re.fullmatch(r'\d+[a-z]?_plan\.md',Path(p).name,re.I)]
 if main:return main
 # Distinct approved versions are not merged blindly. Prefer a named manager plan or specification directly in the task folder; ambiguous revisions stay candidates.
 return [p for p in pp if re.fullmatch(r'\d+_(?:manager_plan(?:_v\d+)?|spec(?:ificatie)?)\.md',Path(p).name,re.I)]
def cells(l):return [re.sub(r'\\\|','|',x.strip()) for x in re.split(r'(?<!\\)\|',l.strip().strip('|'))]
def historical_owner_doc(k,reqs,other):
 for p in PP.get(k,[]):
  if not p.lower().endswith('/00_cerinta_proprietar.md'):continue
  ln=blob(P[p]).splitlines();heads=[];sections=[];oldcl=0
  for j,line in enumerate(ln,1):
   st=line.strip()
   if st.startswith('#'):heads.append(st);oldcl=j;continue
   # Direct quotation only. A quoted status, a title, an actor's assertion, or a bare name does not define an acceptance criterion.
   if not st.startswith(('>','«')) or len(st)<25:continue
   if st.startswith('>'):qt=st[1:].strip()
   else:
    ma=re.match(r'«([^»]{24,})»',st)
    if not ma:continue
    qt=ma[1]
   if len(qt)<24 or re.search(r'VERIFICAT DE MINE|cod de securitate|token[\s:=]|\bparol[aă]\s*[=:]',qt,re.I):continue
   eid=mdev(p,j,{'literal':qt,'section':heads[-1] if heads else None},'Citat din dosarul exact al taskului; poate defini un obiectiv comun. Prezența documentului nu înseamnă acceptarea programului.')
   if re.search(r'(?i)\baudit|\bechip|\bplan|\bagent|10/10',qt) and not re.search(r'(?i)\bstoc|\bfactur|\bimport|\bmeni|\bpl[aă]ti|\bsold|\bcontab|\braport|\baplica',qt):
    other.append({'type':'ORDIN_DE_ORGANIZARE_CITAT_DIN_DOSAR','evidence_id':eid,'meaning':'Păstrează ordinul pentru proces și metode; nu constituie oracol funcțional al aplicației.'});continue
   if not re.search(r'(?i)\b(trebuie|vreau|s[ăa] (se |fie|avem|fac|aib|putem|rule|implem)|verific|compar|implemen|ad[aă]ug|afi[șs]|cite[șs]t|calcule|porne[șs]t|urm[aă]r|propune|inventar|controleaz|refuz|permite)',qt):
    other.append({'type':'CONTEXT_CITAT_DIN_DOSAR','evidence_id':eid,'meaning':'Nu s-a identificat în acest text o obligație verificabilă autonomă.'});continue
   if any(norm(qt)==norm(q['normative_content']) for q in reqs):continue
   add_req(reqs,k,'OBIECTIV_CITAT_DOSAR_PROPRIU',qt,eid,qt,actor=roleby(k),pre='În limitele secțiunii '+str(heads[-1] if heads else 'cerere proprietar')+' a dosarului '+k+'.',layer=['activitate nominală','criteriu funcțional de calibrat'],action='Confruntă linia '+str(j)+' cu baremul și probele proprii taskului; separă obiectivele comune de subpunctul individual.',entire='Sursă nominală, nu dovadă că programul execută cerința.')
def task_adjudication(k,reqs,doc,other,src):
 t=reg[k][1];state=t['stare_generala'];v=ix[k];target=v['aggregate_target']
 if state=='agregat':
  to=reg.get(target,(None,{}))[1];tc=to.get('cod_capitol');before=t.get('cerere_proprietar');after=to.get('cerere_proprietar');ins=[];ok=False;basis=None
  if k in d99['corespondenta']:
   mapping=d99['corespondenta'][k];ins=[mdev(p99,'/corespondenta/'+k,mapping,'Corespondență nominală propusă înainte de execuția transferului.'),mdev(p99a,8,blob(P[p99a]).splitlines()[7],'Aprobare în bloc a listei; nu probează implementarea.')];ok=bool(tc==mapping);basis='Corespondență 99 + aprobare 99a.'
  elif k in d285:
   i,r=d285[k];ins=[mdev(p285,f'/proiecte/P01/strange/{i}',r,'Rândul nominal fixează subtaskul și părintele; dovada aprobării este independentă de execuția funcției.'),mdev(pr285,2,blob(P[pr285]).splitlines()[1],'Raport de reorganizare sub ordinul proprietarului, nu test al obiectivelor.')];ok=target==r['parinte'];basis='Reorganizare T285.'
  elif k in d30 and d30[k][1]['decizie'] in ('AGREGAT','UNIT','UNIT/AGREGAT'):
   i,r=d30[k];ins=[mdev(p30,f'/decizii/{i}',{j:r.get(j)for j in ('id','decizie','tinta','motiv','dovezi')},'Lista nominală a fazei 1.'),mdev(p32,2,blob(P[p32]).splitlines()[1],'Aprobarea listei, cu amendamentele ulterioare care au prioritate.')];ok=(str(r.get('tinta','')).split('.')[-1]==target or r.get('tinta')==target);basis='Decizie T139 aprobată, cu verificare a țintei.'
  if v['split_into']:
   ins+=[mdev(p99,'/inchise_prin_impartire/'+k,d99['inchise_prin_impartire'].get(k),'Împărțirea nominală, distinctă de simpla relație parent.'),ev('LIVE_READ_ONLY','capturi/00_CORESPONDENTA_COD_CAPITOL.json','/inchise_prin_impartire/'+k,v['split_into'],next(x['live']for x in rootmanifest['files'] if x['file']=='00_CORESPONDENTA_COD_CAPITOL.json'),'Țintele finale declarate; obiectivele fiecărei destinații sunt separate.')];basis=(basis or '')+' Împărțire explicită.'
  n=add_req(reqs,k,'DISPOZIȚIE_ADMINISTRATIVĂ','Transferul declarat pentru '+k+' este autoritativ, identifică destinația și păstrează obligațiile inițiale.',src,'Decizia nominală aprobă exact '+str(target)+' sau destinațiile separate '+str(v['split_into'])+'; sursa și ținta rămân auditabile.','proprietar/gestionarul registrului','Registrul și actul de reorganizare sunt comparate la identitate, nu numai la titlu.',['registru','decizie','istoric'],'Recitește toate destinațiile și confruntă obiectivele, subpunctele și amendamentele; nu folosi starea părintelui ca probă a funcției.')
  verdict='PASS_DOVEDIT' if ok else 'INCONCLUDENT'; note=(basis or 'Nu s-a identificat un act nominal aprobat cu țintă concordantă.')+' Transfer efectiv în registru către '+str(target)+'; stare țintă '+str(to.get('stare_generala'))+'. Acest rezultat privește strict dispoziția, nu îndeplinirea cerințelor.'
  # Transfer can pass only for the administrative identity, not preservation of the functional obligations.
  n['normative_content']='Transferul administrativ al rândului '+k+' are decizie nominală aprobată și ținta înregistrată corect.';n['expected_oracle']='Ținta decisă coincide cu ținta din registru; verificare separată a obligațiilor funcționale ale destinației.'
  exec_obs(n,verdict,note,[src]+ins);doc['administrative_decision']=note
  dif=norm(before)==norm(after) if before and after else None
  n2=add_req(reqs,k,'CONTROL_TRANSFER_OBLIGAȚII','Cererea funcțională a sursei trebuie urmărită la destinație, fără moștenirea automată a verdictului.',src,'Se identifică pentru fiecare obligație o dispoziție explicită în țintă și probă de implementare; simpla identitate de text nu este suficientă.','A12 / titularul sursei și destinației','Identitățile tehnice și textele integrale sunt comparate.',['cerință','succesor','funcție'],'Pentru ținta '+str(target)+' citește cerința și criteriile funcționale; execută probele lipsă, indiferent de concordanța textuală.')
  nr=reg[target][0] if target in reg else None; tev=ev('LIVE_READ_ONLY','capturi/00_STATUS_TASKURI.json',f'/{nr}/cerere_proprietar',after,rootmanifest['files'][0]['live'],'Texte sursă și țintă pe aceeași fotografie, nu comportament.') if nr is not None else None
  exec_obs(n2,'INCONCLUDENT','Cerere literal identică după normalizarea spațiilor: '+str(dif)+'; ținta este '+str(to.get('stare_generala'))+'. Criteriile/probele succesorului nu devin probe ale sursei fără legătură semantică.',[i for i in [src,tev,*ins] if i])
  doc['successors']=[{'target':target,'state':to.get('stare_generala'),'canonical':tc,'literal_original_request':after,'origin_request_literal_equal':dif,'functional_verdict':'NEDETERMINAT_SEPARAT'}]+[{'canonical':c,'technical':next((key for key,(_,w) in reg.items() if w.get('cod_capitol')==c),None),'title':next((w['nume_sugestiv'] for _,w in reg.values() if w.get('cod_capitol')==c),None),'functional_verdict':'NEDETERMINAT_SEPARAT'} for c in v['split_into']]
 elif state=='anulat' or k=='T229':
  ins=[];ok=False;msg=[];hist_e=None
  if k in d30:
   ii,j=d30[k]
   if j['decizie']=='ANULAT':
    ins += [mdev(p30,f'/decizii/{ii}',{key:j.get(key)for key in ('id','decizie','motiv','dovezi','tinta')},'Decizie nominală de anulare, confruntată cu actul de aprobare.'),mdev(p32,2,blob(P[p32]).splitlines()[1],'Listele aprobate în bloc; amendamentele Q1–Q8 pot modifica dispoziția.')];ok=True;msg.append('Lista nominală T139, stare ANULAT și motiv explicit.')
  for path in [p32,pold]:
   for ii,line in enumerate(blob(P[path]).splitlines(),1):
    if re.search(r'(?<![\w.])(?:P01\.)?'+re.escape(k)+r'(?!\w|\.\d)',line) and ('anulat' in line.lower() or path==pold and line.startswith('|') and not re.search(r'nu se anul',line,re.I)):
     ins.append(mdev(path,ii,line,'Linie care menționează direct identitatea în secțiunea de anulări.'));msg.append('Act nominal de anulare: '+Path(path).name+':'+str(ii));ok=True
  q=add_req(reqs,k,'DISPOZIȚIE_ADMINISTRATIVĂ','Anularea a fost autorizată pentru această identitate; istoricul și starea actuală se disting.',src,'Actul datat numește taskul sau aprobă lista nominală în care acesta apare. Starea activă corespunde celei mai recente decizii.','proprietar / gestionar registru','Compară actele istorice cu registrul, lista finalizatelor și cea a rămase.',['registru','decizie','cronologie'],'Verifică dacă o decizie ulterioară reactivează cerința, apoi urmărește funcționalitatea numai pe calea activă.')
  if k=='T229':msg+=['Starea curentă «plan», 1%, motivul reactivării pe 31.10 și prezența în ambele liste confirmă că anularea veche nu este o închidere funcțională actuală.'];exec_obs(q,'FAIL_DOVEDIT',' '.join(msg)+' Contradicția privește clasificarea în lista curentă de finalizate, nu execuția codului.',[src,*ins]);q['closure']={'status':'PASS_DOVEDIT' if ok else 'INCONCLUDENT','observed':'Anulare istorică documentată; nu montare.','evidence_ids':ins}
  else:exec_obs(q,'PASS_DOVEDIT' if ok else 'INCONCLUDENT',' '.join(msg) if msg else 'Registrul declară anulare, dar nu am probat o decizie aprobată nominală pentru această identitate.',[src,*ins])
# References are read once, pinned to the report byte-level digest.
hs=__import__('functools').lru_cache(maxsize=4096)(hs)
def notes_for_test(r):
 s=str(r.get('log',''));t=r.get('lines') or [];l=s.splitlines() if s else t if isinstance(t,list) else []
 extract=[n.strip()[:490] for n in l if re.search(r'(?:FAIL|REZULTAT|compil|error:|Exception|RESULT|Summary)',n,re.I)]
 return {k:r[k] for k in ('id','test','source','test_path','test_sha256','target','jar_sha256','compile','compile_exit','run_exit','exit','rc','ok','fail','compiled','sha256') if k in r}|{'observed_diagnostics':extract[:15]}
testmap=defaultdict(list)
for zone,f,prop0 in [('A01','A01/java_results.json','tests'),('A02','A02/Java_suite.json','tests'),('A03','A03/java_retry2.json','runs'),('A06','A06/suite.json',None),('A07','A07/suite-installed.json',None),('A07','A07/suite-master.json',None)]:
 if not(E/f).exists():continue
 raw=rd(E/f); rows=raw.get(prop0,[]) if prop0 and isinstance(raw,dict) else raw
 if not isinstance(rows,list):continue
 for j,row in enumerate(rows):
  if not isinstance(row,dict):continue
  name=row.get('test') or row.get('id') or row.get('class')
  if not name:continue
  result=notes_for_test(row); eid=json_ev(f,('/'+prop0 if prop0 else '')+'/'+str(j),result,'Arie exactă a fixture-ului executorului '+zone+'; nu este execuție end-to-end sau dovadă retroactivă.','BUILD_OR_UNIT_TEST');testmap[name].append((eid,result))
native=rd(E/'Matrice_nativa_reutilizare.json')['rows']
def cite_test(req):
 body=str(req['expected_oracle'])+' '+str(req['normative_content']);matches=[]
 for symbol,samples in testmap.items():
  if re.search(r'\b'+re.escape(symbol)+r'\b',body):matches.extend(samples)
 if not matches:return
 ids=[q[0] for q in matches];obs='; '.join((q[1].get('test') or q[1].get('id') or '?')+': '+str({k:q[1].get(k) for k in ['target','compile','compile_exit','exit','run_exit','rc','ok','fail'] if k in q[1]}) for q in matches)
 exec_obs(req,'INCONCLUDENT','Testul este numit în criteriu și există execuție nominală: '+obs+'. Suita nu demonstrează automat toate clauzele criteriului. Rezultatele/diagnosticele sunt stocate exact în dovezi.',ids)
def pcrit(k,p,reqs):
 ll=blob(P[p]).splitlines();header=None;section=None
 for n,line in enumerate(ll,1):
  if line.lstrip().startswith('#'):section=tidy(line);header=None
  if not line.strip().startswith('|'):continue
  cs=cells(line);first=cs[0].strip('* \x60') if cs else ''
  if n<len(ll) and ll[n].strip().startswith('|') and ('----' in ll[n] or '---' in ll[n]):header=cs;continue
  m=re.fullmatch(r'(?:K[-.]\d+(?:[.-]\d+|[a-z])?|RZ[-.]\d+(?:[.-]\d+|[a-z])?|R[-.]\d+(?:[.-]\d+|[a-z])?|C[-.]\d+(?:[.-]\d+|[a-z])?)',first,re.I)
  if not m or not header or len(cs)<2:continue
  # Use structured table semantics, not every identifier: risks, test outcomes or narrative are not requirements.
  hd=norm(' '.join(header));sect=norm(section)
  if ('risc' in hd or 'risc' in sect or 'istoric' in sect or 'amendament' in sect or 'defect' in hd):continue
  if not any(word in hd+' '+sect for word in ['criter','rezultat','aștept','aştept','cerin','accept','țint','tinta','numeric','oracol','funcțion','verific','contract','comport','dovad','indicator']):continue
  oracle_parts=[s for h,s in zip(header,cs) if any(x in norm(h) for x in ('aștept','aştept','țint','tint','oracol','rezultat','expected','criteriu')) and len(s)>2 and s!=first]
  # Preserve complete row, including the columns adjacent to numeric targets.
  expected=' | '.join(oracle_parts) if oracle_parts else ' | '.join(cs[1:])
  cite=mdev(p,n,{'heading':section,'columns':header,'row':line},'Criteriu din tabelul formal al dosarului EXACT al taskului. Eticheta/versiunea planului rămâne distinctă de acceptarea istorică; nu este probă de funcționare.')
  rr=add_req(reqs,k,'CRITERIU_PLAN_NOMINAL',first+' — '+' | '.join(cs[1:]),cite,expected,actor=roleby(k),pre='Condiția completă din tabelul '+str(section)+' și rolul/versiunea dosarului; pe SHA actual trebuie confirmată aceeași configurație.',layer=['suprafață indicată de criteriu','oracol al planului'],action='Reexecută criteriul '+first+' din '+p+':'+str(n)+'; compară exact coloana țintă/rezultat cu proba de la versiunea auditată.',entire='Rândul de plan este identificat; veridicitatea unei aprobări sau execuții istorice se verifică separat.')
  if rr:cite_test(rr)
def current_policy(k,reqs):
 # Explicit scope: observed result is used ONLY for the specific requirement this fixture measures.
 def add_current(ident,text,expected,fid,idx,why):
  if fid not in fi:return
  z,j,ff=fi[fid];c=ev('USER_SCOPE','Manualul explicativ 25.10.2026 / idei și clarificări',ident,{'requirement':text},hs(manual/'Date_manual_Explicativ.json'),'Criteriu actual privind arhitectura comunicată; nu se proiectează retroactiv în definiția veche a taskului.','2026-10-25')
  cr=add_req(reqs,k,'CERINȚĂ_ACTUALĂ_AMENDATĂ',text,c,expected,actor='gestionar/operator autorizat WMS',pre='Separă în cabinet test fezabilitatea componentei de acceptarea completă UI/ERP. Se compară strict aceeași operație și granulație documentată.',layer=['backend','stoc fizic','persistență'],action='Reia într-un cabinet izolat cu același bundle, actori și fixtură. Verifică fiecare efect o singură dată, plus traseul complet până la documentul contabil.')
  if cr:
   zobs=ff.get('observed_fact') or ff.get('observed') or ff.get('reproduction');ze=json_ev(z+'_raport.json','/findings/'+str(j),{'id':fid,'actual':zobs,'title':ff.get('title')},'Domeniul exact al constatării executorului; nu se extinde la tot taskul.','INTEGRATION_TEST');ids=[ze]
   for ji,rec in ae:
    ids0=rec[0].split('/');match=(fid in rec[0] if len(ids0)==1 else fid in rec[0] or fid.split('-')[-1] in ids0[1:] and fid.startswith(ids0[0][:3]))
    if match:ids.append(json_ev('A11_control_lot1.json','/independent_results/'+str(ji),rec,'Reproducerea A11 se aplică numai segmentului declarat.','INTEGRATION_TEST'))
   exec_obs(cr,'FAIL_DOVEDIT_LA_NIVEL_COMPONENTĂ',why+' '+str(zobs),ids);cr['related_findings_only_for_this_requirement']=[fid]
 if k=='T355':
  add_current('U18 / C03 condiție de reluare','Repetarea aceleiași note de asamblare nu consumă din nou aceeași cantitate.','20 unități înainte și 19 după prima notă de 1; repetarea aceleiași note rămâne la 19, cu aceleași efecte.', 'A05-F01',0,'Reproducere pe nota din JAR, cu aceeași identitate: 20→19→18; dublare demonstrată în segmentul testat.')
  add_current('U17 și U18 / rețete','Nota trebuie să poată înregistra o cutie și 0,5 ore de muncă pentru ambalarea reală; costul se recunoaște o singură dată în G1.','Fixtura operațională permite o cutie și 0,5 ore. Efectul contabil singular necesită probă separată.','A05-F02',0,'Componenta refuză PK / 0,5 înainte de execuția efectelor; conformitatea contabilă G1 nu a fost demonstrată în această probă.')
 if k=='T354':
  add_current('U14 + U22','Stocul alternativ de canal nu scade aceeași rezervare globală de două ori când sunt eligibile două gestiuni G1.','10+10−7=13 disponibile global; nu 6. Nu se însumează alternativele S1 și S2 ca stoc distinct.','A02.F01',0,'Segmentul de agregare per gestiune este reprodus. Alternativa virtuală din task este afectată dacă folosește acest calculator; restul fluxului comercial nu este certificat.')
def retrieval(k,t):
 out=[]
 for p in PP.get(k,[]):
  if '/'+k+'-' in p or '/'+k+'_' in p:out.append(p)
 return out
def cases(v):
 k=v['source_id'];r1=rd(E/'R1'/firstrows[k]['file']);assert hs(E/'R1'/firstrows[k]['file'])==review[k]['sha256'];ad=review[k];rawno,t=reg[k];shadow=histidx[k];cats=Counter();frags=[]
 for f,g in zip(r1['atomic_requirements'],ad['fragment_records'],strict=True):
  # Preserve every old item and its position, never promote it by copying its classification.
  cat=g['kind_for_review'];cats[cat]+=1;frags.append({'ordinal':g['ordinal'],'category_A11':cat,'archived_text_verbatim':f['text'],'original_source':f['source'],'r1_hash_from_A11':g['text_sha256'],'is_operative_requirement':False})
 src=ev('LIVE_READ_ONLY','capturi/00_STATUS_TASKURI.json',f'/{rawno}',{'id':k,'title':t['nume_sugestiv'],'raw_state':t['stare_generala'],'original_code':t.get('cod_capitol'),'closure_date':t.get('finalizat_la')},rootmanifest['files'][0]['live'],'Registru declarat. Nu probează singur instalarea, testul sau execuția.',snapshot)
 ht=ev('HISTORICAL_REFERENCE','executie/A12_istoric_git_stari.json','/rows/'+str(shadow[0]),{'first_observation':shadow[1]['first_final_on_daily_sample_explicit_P01'],'declared_historical_dates':shadow[1]['historic_dates_declared'],'daily_changes':shadow[1]['observed_daily_changes']},hs(E/'A12_istoric_git_stari.json'),'Data commitului este o limită superioară a primei observații în eșantion, nu o dată exactă de terminare sau montare.')
 reqs=[];other=[];doc={};full=t.get('cerere_proprietar') or '';s,qk,qt=originals(t);raw_quote_ev=ev('HISTORICAL_REFERENCE','capturi/00_STATUS_TASKURI.json',f'/{rawno}/cerere_proprietar',full,rootmanifest['files'][0]['live'],'Textul integral al câmpului, inclusiv proveniență și eventuale citate.',qt)
 if s:
  srcq=ev('HISTORICAL_REFERENCE','capturi/00_STATUS_TASKURI.json',f'/{rawno}/'+qk,s,rootmanifest['files'][0]['live'],'Formulare atribuită proprietarului în registru; nu dovedește îndeplinirea ei.',qt)
  if re.search(r'(?:10/10|patru echipe|4 echipe|cu.*auditor|reverific.*sarcin|reia cu echipa)',s,re.I):
   add_req(reqs,k,'DIRECTIVĂ_DE_METODĂ',s,srcq,'Păstrează plan și audit independent, verificări și reluări pentru domeniul real al taskului; nu echivala această directivă de organizare cu o cerință funcțională ERP.','coordonator și auditor separat','Proiectul are o sarcină de judecat și dovadă independentă de acceptare.',['guvernanță','istoric'],'Verifică raportul și baremul istoric la commitul declarat; probează independent criteriile funcționale ale fișei.')
  elif re.search(r'(?:permis|permisiune|liber la montare|po.ti mont|poți mont|deploy fara probleme|actualizezi containere)',s,re.I):
   other.append({'type':'AUTORIZAȚIE_ISTORICĂ','evidence_id':srcq,'meaning':'Permisiunea nu definește singură release-ul, digestul, cabinetul ori acceptarea funcției; raportul montării se verifică separat.'})
  else:
   add_req(reqs,k,'DIRECTIVĂ_LITERALĂ_PROPRIETAR',s,srcq,'Rezultatul cerut textual: '+s+'; prag cantitativ sau decizie de acceptare neprecizate în acest citat, dacă nu sunt documentate separat.',actor=roleby(k),layer=['cerere proprietar','afacere'],entire='Nu se presupune că fiecare citat este un contract numeric sau o acceptare ulterioară.')
 else:other.append({'type':'CERERE_ORIGINALĂ_NESCRISĂ_SAU_NEIDENTIFICATĂ','evidence_id':raw_quote_ev,'meaning':'Identificatori de inventar, citate retrospective și LOG_ISTORIC sunt proveniență. Se caută obiective în cartela exactă, plan, RZ sau decizie; dacă lipsesc rămân necunoscute.'})
 canon=v['canonical'];card_path=pcard.get(canon)
 if card_path:
  c=readp(card_path);appr=mdev(p99a,8,blob(P[p99a]).splitlines()[7],'Aprobarea setului de cartele în bloc; nu validează funcționalitatea instalată.')
  for j,goal in enumerate(c.get('obiective',[])):
   if not isinstance(goal,dict):continue
   tx=goal.get('obiectiv')
   if tx:
    ee=mdev(card_path,f'/obiective/{j}/obiectiv',tx,'Câmp explicit obiectiv al cartelei canonice exacte, nu text liber al registrului.')
    n=add_req(reqs,k,'OBIECTIV_CARTELĂ_NOMINALĂ',tx,ee,tx,actor=roleby(k),pre='Aceeași cartela '+canon+' și domeniul aprobării 99a/D-A8-2; verifică amendamentele de după 18.10.2026.',layer=[k for k,d in c.get('tip',{}).items() if d],entire='Aprobare documentară în bloc; nu probă a implementării.')
    if n:n['authority_evidence_ids']=[appr]
   for j2,ac in enumerate(goal.get('activitati',[])):
    res=ac.get('rezultat') if isinstance(ac,dict) else None
    if not isinstance(res,dict) or not res.get('indicator') or not res.get('tinta'):continue
    ee=mdev(card_path,f'/obiective/{j}/activitati/{j2}/rezultat',res,'Criteriu de livrabil cu indicator și țintă explicite.')
    n=add_req(reqs,k,'LIVRABIL_CARTELĂ_NOMINALĂ',res['indicator'],ee,'Țintă: '+str(res['tinta'])+'; bază: '+str(res.get('T0'))+'; metodă: '+str(res.get('comanda')),actor=ac.get('rol') or roleby(k),pre='Activitatea '+str(ac.get('nr'))+' din cartela '+canon,layer=['livrabil','metodă','acceptare documentară'],entire='Ținta documentului nu atestă rezultatul software.')
 for pp in relevantplans(k):pcrit(k,pp,reqs)
 for j,z in rz.get(canon,[]):
  orig=z['original'];path=manual/'Date_manual_C03.json';cite=ev('HISTORICAL_REFERENCE',str(path),f'/rz_mapping/{j}/original',orig,hs(path),'Transcrierea RZ a sursei C03; păstrează condiția originală și dispoziția ulterioară distincte.','2026-10-25')
  n=add_req(reqs,k,'RZ_SURSĂ_C03',z['id']+' '+orig['indicator'],cite,'Țintă '+str(orig['target'])+'; probă: '+str(orig['proof']),actor=roleby(k),pre='Contextul și valoarea inițială ale sursei RZ: '+str(orig.get('T0')),layer=['flux WMS','oracol cantitativ','persistență'],action='Repetă '+z['id']+' în versiunea aplicabilă; dispoziția din manual este '+z['disposition']+'.',entire='Maparea se face pe old_task_id, nu pe codurile propuse pentru viitor.')
  if n:n['amendment_after_source']={'disposition':z['disposition'],'reason':z['reason']};cite_test(n)
 for j,z in fiches.get(canon,[]):
  body=z['source_body_exact'];lines=body.splitlines()
  for li,line in enumerate(lines):
   ma=re.match(r'^- \*\*(Rezultate cantitative|Rezultate calitative[^*]*):\*\*\s*(.*)',line)
   if not ma:continue
   path=manual/'Date_manual_C10.json';ee=ev('HISTORICAL_REFERENCE',str(path),f'/source_fiche_mapping_59/{j}/source_body_exact:line{li+1}',line,hs(path),'Rând exact al fișei originale; nu folosi noul cod propus drept cod vechi.','2026-10-25')
   n=add_req(reqs,k,'CRITERIU_FIȘĂ_C10',ma[2],ee,ma[2],actor=roleby(k),pre='Subcapitolul și identitatea istorică '+z['source_title'],layer=['contract de vânzări','probă cantitativă/calitativă conform sursei'],action='Verifică metoda și T0 istorice ale '+z['id']+' în mediul/versiunea corespunzătoare; separă amendamentul '+z['amendment']+'.')
   if n:cite_test(n)
 # Separate the original traced business specification from later renumbering proposals; never look up a proposed code as if registered.
 if canon:
  for fname,section,source,field,name_id in [('Date_manual_C03.json','old_task_mapping',cm.get('old_task_mapping',[]),'initial_requirement','old_task_id'),('Date_manual_C10.json','historical_task_mapping_33',vm.get('historical_task_mapping_33',[]),'initial_exact','old_id')]:
   for jj,row in enumerate(source):
    if row.get(name_id)!=canon.removeprefix('P01.') or row.get('legacy_id') not in (None,k,'P01.'+k):continue
    txt=row.get(field)
    if not isinstance(txt,str) or not txt.strip():continue
    ee=ev('HISTORICAL_REFERENCE',str(manual/fname),f'/{section}/{jj}/{field}',txt,hs(manual/fname),'Cerință inițială citită din sursa istorică prin ID vechi și legacy ID. Nu se presupune că data de acceptare sau montarea coincid cu data manualului.','2026-10-25')
    q=add_req(reqs,k,'OBIECTIV_INIȚIAL_TRASAT',txt,ee,txt,actor=roleby(k),pre='Identitatea în manualul istoric coincide cu codul ȘI ID-ul tehnic al taskului.',layer=['activitate de afaceri','frontend/backend unde sunt cerute','documente și date'],action='Confruntă cerința inițială și dispoziția următoare cu documentele și mediul propriu; nu echivala propunerea manualului cu o implementare.')
    if q:q['amendment_after_source']={'disposition':row.get('decision') or row.get('disposition'),'reason':row.get('why') or row.get('justification')}
 historical_owner_doc(k,reqs,other)
 task_adjudication(k,reqs,doc,other,src);current_policy(k,reqs)
 return k,v,r1,ad,frags,raw_quote_ev,ht,src,reqs,doc,other
def sourcecheck(path,kind,ptr,limit):
 return json_ev(path,ptr,kind,limit)
controls={}
for zz,p in zone_reports.items():
 for j,x in enumerate(p.get('controls',[])):
  if isinstance(x,dict):controls[(zz,x.get('control_id') or x.get('id'))]=(j,x)
def zone_control(zz,cid):
 j,x=controls[(zz,cid)]
 summary={k:x.get(k) for k in ('control_id','id','title','expected','observed','status','evidence_ids','evidence','findings','finding_ids') if k in x}
 return json_ev(zz+'_raport.json','/controls/'+str(j),summary,'Rezultatul executorului pe domeniul/fixture-ul declarat, nu verdictul integral al cerinței sau al taskului.')
def mount_coverage(k,reqs,doc,src):
 pths=[p for p in P if re.search(r'/'+re.escape(k)+r'[-_][^/]+/[^/]*raport[^/]*montare[^/]*\.md$',p,re.I)]
 if not pths:return
 obs={};docs=[]
 for pp in pths:
  ll=blob(P[pp]).splitlines()
  for j,s in enumerate(ll,1):
   if not s.startswith('|'):continue
   c=cells(s)
   if not c:continue
   firstcol=norm(c[0]).strip(' \x60*')
   if firstcol in ('q31','ses','asociatie','asociație','aride','cesiro') and len(c)>2:
    token=mdev(pp,j,s,'Constatare istorică a raportului de montare per cabinet; proba actuală nu a rerulat operația.');obs[firstcol]=token
  docs.append({'file':pp,'git_oid':P[pp],'total_lines':len(ll)})
 if not obs:return
 u=add_req(reqs,k,'CONTROL_DISPOZIȚIE_MONTARE','Afirmația istorică de montare este susținută de rânduri identificabile pentru cabinetele vizate.',src,'Câte un rezultat de montare cu identificare pentru q31, ses, asociatie, aride și cesiro; dacă scope-ul raportului este mai mic se documentează și se reanalizează ținta.','auditor de livrare','Versiunea istorică declarată și fișierele de release ale taskului; nu reprezintă drept de redeploy.',['livrare','proveniență'],action='Confruntă digests, manifestul registry și jurnalele per cabinet cu raportul; pentru comportament rulează smoke independent pe clonă dacă există.')
 exec_obs(u,'PASS_DOVEDIT_DOCUMENTAR' if len(obs)==5 else 'INCONCLUDENT','Raportul Git conține rânduri nominale pentru '+', '.join(sorted(obs))+'. Verificată existența și conținutul raportului istoric; nu starea de azi a aplicației.',list(obs.values()),'closure')
 doc['mount_reports']=docs
def specials(k,reqs,doc,src):
 if k=='T227':
  qr=rd(R.parent/'A12_T227_SQL_sintetic.json'); testp=rd(E/'A12_test_local_T227.json');db=rd(E/'A12_DB_metadate_CESIRO.json');jar=rd(E/'Diferente_bundle_CESIRO.json')
  ff=[(j,x)for j,x in enumerate(jar['rows']) if x['class'] in ('com/eva/ro/contab/form/VerificareImportSaga.class','com/eva/ro/contab/form/WSagaVerificareImportForm.class')]
  js=[json_ev('Diferente_bundle_CESIRO.json',f'/rows/{j}',v,'Compararea JAR instalat și JAR Git pentru clasa nominală.','LIVE_READ_ONLY')for j,v in ff]
  noform=json_ev('A12_DB_metadate_CESIRO.json','/rows/forms',{'count':len(db['rows']['forms']),'found':[q for q in db['rows']['forms']if 'VerificareImport' in str(q.get('classname') or '')]},'Interogare read only de dicționar CESIRO; numai cabinetul și classname verificate.','LIVE_READ_ONLY')
  for u in reqs:
   tx=u['normative_content'];id0=tx.split(' — ')[0]; z={'R-4':0,'R-9':2,'R-10':2,'R-14':1,'K-31':1}.get(id0)
   if z is not None:
    test=qr['tests'][z];test_e=json_ev('A12_T227_SQL_sintetic.json',f'/tests/{z}',test,'SQL din sursa fixată executat pe CTE sintetice în PostgreSQL, fără date reale; nu probează întreaga cerință UI/calcul.','INTEGRATION_TEST')
    exec_obs(u,'INCONCLUDENT','Segment măsurat: '+test['id']+'; așteptat '+str(test['expected'])+'; observat '+str(test['observed'])+', rc='+str(test['rc'])+'. Restul cerinței nu a fost demonstrat din ecran.',[test_e]);u['verified_segment']={'status':'PASS_DOVEDIT','expected':test['expected'],'observed':test['observed'],'evidence_id':test_e}
   elif id0 in ('K-21','K-22','K-23') or 'ecran' in tx.lower() and id0.startswith('R-'):
    exec_obs(u,'BLOCAT_ACCES','Testul vizual în CESIRO nu poate fi executat pentru această versiune: cele două clase lipsesc din JAR-ul montat și AD_Form nu are classname VerificareImport.',js+[noform])
   if 'test_bilant.py' in tx:
    te=json_ev('A12_test_local_T227.json','/',testp,'Testul harness-ului privind erorile/măștile; nu sold contabil.','LOCAL_ISOLATED_TEST');exec_obs(u,'INCONCLUDENT',testp['stdout']+' Numai segmentul de bilanț al harness-ului este probat.',[te])
 if k=='T224':
  j=rd(R/'T224_trei_referinte.json');u=add_req(reqs,k,'CONTROL_DISPOZIȚIE_REFERINȚE','Cele trei documente declarate trebuie să poată fi localizate la reviziile pe care le citează taskul.',src,'Fiecare blob istoric este recuperabil la SHA declarat; proveniența față de SHA GitHub de audit se evaluează separat.','auditor de proveniență','Diferențiază commitul declarat, SHA GitHub și checkoutul serverului.',['Git','documentare'],'Corectează referințele de consultare dacă se dorește vizibilitate pe GitHub; nu modifica taskul sau codul în acest audit.')
  ep=json_ev('R2/T224_trei_referinte.json','/rows',j['rows'],'Căutare după blob exact pe arborele Git congelat, plus git cat-file pe HEAD server.','STATIC_SOURCE')
  exec_obs(u,'PASS_DOVEDIT','3/3 bloburi identice la commiturile declarate și server f85086c5. 0/3 există cu același hash oriunde în arborele GitHub fixat. Neconcordanța este între versiuni, nu lipsă de document în general și nici defect al importului.',[ep])
 if k in ('T157','T214'):
  for u in reqs:
   if u['kind']!='OBIECTIV_CARTELĂ_NOMINALĂ':continue
   if k=='T157':
    ff=fi['A03-F02'];j,rec=next(q for q in ae if q[1][0]=='A03-F02')
    ee=[json_ev('A03_raport.json',f'/findings/{ff[1]}',{'id':'A03-F02','observed':ff[2]['observed_fact']},'Componentă folosită de nota de închidere; nu există comparație completă cu SAGA sau rulare finală a jurnalului.'),json_ev('A11_control_lot1.json',f'/independent_results/{j}',rec,'Reproducere independentă pe clauzele SQL, fără emiterea jurnalului.','INTEGRATION_TEST')];exec_obs(u,'INCONCLUDENT','Segment comparabil al calculului: '+rec[2]+' Nu a fost probată întreaga configurare de închidere pentru fiecare firmă sau paritatea cu SAGA.',ee)
   else:
    ss=testmap.get('TestT214VanzariPeCanal',[]);exec_obs(u,'INCONCLUDENT','Suita de clasă nominală a raportului T214 a fost executată: '+str([w[1].get('ok') for w in ss])+' aserțiuni trecute. Totalurile efectiv afișate pe canal/perioadă nu au fost reconciliate din ecran.',[w[0]for w in ss])
def extra_handoff(k,reqs,doc,src):
 def zproof(fid):
  if fid not in fi:return None
  zn,j,r=fi[fid];obs=r.get('observed') or r.get('observed_fact') or r.get('reproduction')
  return json_ev(zn+'_raport.json','/findings/'+str(j),{'id':fid,'title':r.get('title'),'observed':obs,'raw_evidence_refs':r.get('evidence_ids') or r.get('evidence'),'anchors':r.get('anchors')},'Dovadă limitată la ruta/forma/adaptorul exercitat de executor; nu se extinde la ansamblul taskului.','INTEGRATION_TEST'),str(obs)
 if k=='T216' and 'A07-F03'in fi:
  # Original T22 was aggregated into T216. Only T216 receives the amended operational criterion; links from T22 are disposition/history.
  path=manual/'Date_manual_Explicativ.json';cc=rd(path)
  for key,ref,test,exp in [('C10-EXT-01','A07-F03','Importul comercial păstrează distinct clientul și adresa de facturare față de destinația reală a comenzii.','Factura pe A, expediere pe B; ambele referințe distincte în C_Order.'),('U29','A07-F04','Pentru politica după livrarea reală, factura așteaptă livrarea curierului și lipsa incidentului conform configurației.','CO fără dovadă livrare nu declanșează facturare pe ramura amânată.')]:
   zr=zproof(ref)
   if not zr:continue
   coll=cc['audit_controls'] if key.startswith('C10') else cc['user_ideas_to_requirements']; ix0=next(j for j,z in enumerate(coll) if z.get('finding_id')==key or z.get('id')==key)
   ee=ev('USER_SCOPE',str(path),('/audit_controls/' if key.startswith('C10') else '/user_ideas_to_requirements/')+str(ix0),test,hs(path),'Cerință actuală separată de istoricul agregării T22→T216.','2026-10-25');u=add_req(reqs,k,'CERINȚĂ_ACTUALĂ_AMENDATĂ',test,ee,exp,actor='gestionar comenzi / responsabil vânzări',pre='Generatorul T22 din cod și JAR și politica comercială amânată; pentru emiterea imediată rezultatul legitim diferă.',layer=['comandă','backend','livrare','factură'],action='Reia în clonă cu Facturare A/Livrare B și cu politica amânată vs imediată; verifică documentele persistente.')
   exec_obs(u,'FAIL_DOVEDIT_LA_NIVEL_COMPONENTĂ',zr[1], [zr[0]]);u['related_findings_only_for_this_requirement']=[ref]
 if k=='T353' and 'A08-F01'in fi:
  eid,obs=zproof('A08-F01');doc['explicit_handoff_limit']={'id':'A08-F01','evidence':eid,'observed':obs,'boundary':'Importul CMS extern poate înlocui catalog altui canal. T353 privește textele/denumirile pe limbă; această probă nu a exercitat ecranul T353 ori importul lui nativ. Este risc în aval; nu se marchează FAIL T353.'}
 if k=='T227' and 'A09-F05' in fi:
  e,obs=zproof('A09-F05')
  for cr in reqs:
   if cr['normative_content'].startswith('K-23 —'):exec_obs(cr,'INCONCLUDENT',obs+' Pragul de 2 s din interfața ZK nu a fost măsurat; nu se poate afirma depășirea lui.',[e])
 if k=='T314' and 'A09-F02' in fi:
  e,obs=zproof('A09-F02')
  for cr in reqs:
   if cr['normative_content'].startswith('K-03 —'):
    exec_obs(cr,'INCONCLUDENT',obs+' Această probă arată coliziunea de etichete, nu infirmă singură obiectivul istoric distinct «zero diacritice» și nu testează fiecare intrare a meniului.',[e])

def finish_case(args):
 k,v,r1,ad,frags,qt,ht,src,reqs,doc,other=args; mount_coverage(k,reqs,doc,src);specials(k,reqs,doc,src);extra_handoff(k,reqs,doc,src)
 contexts=[];perzone=defaultdict(list)
 for cid in r1.get('planned_cross_controls',[]):
  zz=cid[:3]
  if (zz,cid) not in controls:continue
  eid=zone_control(zz,cid);perzone[zz].append(eid)
 # Native corroboration only where the named mechanism/SQL model is present literally in an objective OR in verified committed class/AD links. It is a candidate baseline, never behavioural proof.
 crit=' '.join(q['normative_content'] for q in reqs);associated_tables={t.casefold() for x in r1['static_code_and_live_dictionary'] for t in x.get('tables_bound_by_literal_sql_and_ad_catalog',[])};native_ev=[]
 for j,row in enumerate(native):
  sym=Path(row['native_source']).stem
  if re.search(r'\b'+re.escape(sym)+r'\b',crit) or sym.casefold() in associated_tables:
   native_ev.append(json_ev('Matrice_nativa_reutilizare.json','/rows/'+str(j),{x:row.get(x) for x in ['owner','capability','native_source','line','installed_class','bytecode_sha256']},'Mecanism nativ identificat nominal. Nicio dovadă automată de folosire sau testare în task.','STATIC_SOURCE'))
 oper=[x for x in reqs if x['kind'] not in ('DISPOZIȚIE_ADMINISTRATIVĂ','CONTROL_TRANSFER_OBLIGAȚII','CONTROL_DISPOZIȚIE_REFERINȚE','CONTROL_DISPOZIȚIE_MONTARE','DIRECTIVĂ_DE_METODĂ')]
 unknown=not oper
 if unknown:
  proc='Caută baremul aprobat pentru '+k+' ('+v['display_title']+').'
  if doc.get('successors'):proc+=' Prezintă separat cerințele destinației '+str(doc['successors'][0].get('target'))+' și măsurile funcționale; nu le atribui retroactiv.'
  if r1['source_identity_notes'].get('alias_to_frozen_inventory'):proc+=' Vechiul inventar descrie un rând de stare/proveniență, nu o cerință proprietar contemporană; caută brief-ul/decizia pe aliasul exact.'
  if v['source_state']=='anulat':proc+=' Nu se acordă calificativ funcțional pentru o anulare; confirmă individual că toate obligațiile au dispoziție.'
  other.append({'type':'CERINȚĂ_FUNCȚIONALĂ_NECUNOSCUTĂ','expected_oracle':None,'observed':None,'status':'INCONCLUDENT','reason':proc,'evidence_ids':[qt,ht,src],'source_search':{'own_plan_files_read':retrieval(k,reg[k][1]),'exact_card_exists':v['canonical'] in pcard,'known_legacy_proofs_and_paths':r1['source_identity_notes'].get('alias_to_frozen_inventory',[]),'referenced_git_documents':[(d['ref'],d['artifact']) for d in r1['artifacts_git_semantic_read']]}})
 for q in reqs:
  del q['_k']
  for when in ('current','closure'):
   state=q[when]
   if not state['evidence_ids'] and state['status'] in ('INCONCLUDENT','NEEXECUTAT'):
    state['blocking_reason']=('Acest task nu are probă funcțională individuală datată la închidere pentru acest criteriu; data unui commit nu constituie data montării.' if when=='closure' else 'Nu există încă execuție pentru oracolul indicat, cu actor/mediu/versiune și observația necesară. Se cere: '+q['next_action'])
   if state['evidence_ids']:assert state['observed'] is not None and all(i in evidence for i in state['evidence_ids'])
  ids=uniq([q['source_evidence_id'],*q.get('authority_evidence_ids',[]),*q['current']['evidence_ids'],*q['closure']['evidence_ids']])
  for rel,vals in [('source',[q['source_evidence_id']]),('authority',q.get('authority_evidence_ids',[])),('closure',q['closure']['evidence_ids']),('current',q['current']['evidence_ids'])]:
   for ii in uniq(vals):inverse[ii].append({'task':k,'criterion':q['id'],'relation':rel})
 ctrl={}
 risk_criteria={'A12-CK-03':reqs,'A12-CK-04':[q for q in reqs if q['kind'] in ('DISPOZIȚIE_ADMINISTRATIVĂ','CONTROL_TRANSFER_OBLIGAȚII','CONTROL_DISPOZIȚIE_MONTARE')],'A12-CK-06':[q for q in reqs if q['current']['evidence_ids']],'A12-CK-12':[q for q in reqs if k=='T227' and q.get('verified_segment')],'A12-CK-28':[q for q in reqs if q['kind']=='CONTROL_DISPOZIȚIE_MONTARE' or k=='T227' and q['current']['status']=='BLOCAT_ACCES'],'A12-CK-30':reqs}
 for entry in r1['control_results']:
  ck=entry['id'];ds=risk_criteria.get(ck,[]);prior=entry['status'];note=entry['result_or_next_probe']
  if ck in risk_criteria:
   if ck=='A12-CK-03':note='Au fost separate '+str(len(frags))+' fragmente inițiale, '+str(len(reqs))+' criterii/controale recuperate. Funcția normativă neidentificată: '+str(unknown)+'.'
   else:note='Criterii individuale aferente: '+str(len(ds))+'. Vezi rezultatele separate actual/istoric. '+note
   if ds:prior='INCONCLUDENT'
  ctrl[ck]={'status':prior,'rationale_or_next':note,'criterion_ids':[q['id'] for q in ds],'ids_derived_from_source_evidence':uniq([q['source_evidence_id'] for q in ds]),'r1_source':firstrows[k]['sha256']}
 # Scoring by A11 only; no generic task-level PASS from adjacent AD class, package or thematic finding.
 return {'schema':'eva.audit.A12.task.review-r2','task':k,'canonical':v['canonical'],'title':v['display_title'],'project':'P01','chapter':v['chapter'],'current_status_at_primary_cutoff':v['source_state'],'cutoff':snapshot,'source_git_sha':sha,'r1_immutable':{'path':'../../R1/'+firstrows[k]['file'],'sha256':firstrows[k]['sha256'],'A11_quality':ad['audit_quality_score'],'A11_actions':ad['actions'],'A11_issue':ad['primary_constraint']},'snapshot_evidence_id':src,'historical_timeline_evidence_id':ht,'known_closure_dates':v['source_closure_times'],'missing_exact_closure_date_at_cutoff':v['missing_source_closure_time'],'first_dated_final_registry_observation':shadow_of(k),'source_literal':{'raw_cerere':reg[k][1].get('cerere_proprietar'),'raw_descriere':reg[k][1].get('descriere'),'registry_pointer':reg[k][0],'original_request_evidence':qt,'principle':'Descrierea și notele de proveniență nu sunt criterii acceptate.'},'r1_fragments_reclassified':frags,'disposition_admin':doc,'operative_criteria_and_audit_criteria':reqs,'control_register_R2':ctrl,'functional_criteria_unidentified':unknown,'unknowns_and_supporting_context':other,'identified_task_files':[{'path':p,'git_oid':P[p]} for p in relevantplans(k)],'historical_sources_from_r1_ref':'../../R1/taskuri/Fisa_'+k+'.json#/historical_evidence','zone_related_controls_only':dict(perzone),'native_mechanisms_explicitly_referenced_only':native_ev,'zone_relation_limit':'Controalele de zonă asociate prin plan/capitol sunt pistă de predare. Doar referințele trecute în current.evidence_ids sunt utilizate ca probă a criteriului concret. Nu se propagă un finding de capitol către toate taskurile.','audit_review_status':'PARTIAL_CU_LIMITARI; R2 predată pentru reverificare A11, fără autocalificativ','quality_score_r2':None,'decision_at_closure':'Vezi separat rezultatele dispoziției și controalele funcționale. Fără probă datată individuală verdictul funcțional rămâne NEDETERMINAT.','decision_current':'Vezi rezultate individuale actuale și limitările declarate; niciun scor integral de implementare atribuit prin automatizare.'}
def shadow_of(k):
 row=histidx[k][1].get('first_final_on_daily_sample_explicit_P01')
 if not row:return None
 return {'observed_state':row.get('state'),'git_commit':row.get('sample_commit'),'registry_commit_time':row.get('latest_registry_commit_at_sample'),'request_hash':row.get('request_hash'),'note':'Moment maxim de observare a stării în instantaneul verificat, nu dată exactă a închiderii.'}
def run():
 groups=[];allkind=Counter();allstatus=Counter();ac=Counter();meta=Counter();refs=Counter();seen_area=Counter();quality_changes=[];mountn=0;rankrows=[]
 for k in ix:
  if k not in queued:continue
  case=finish_case(cases(ix[k]));criteria=case['operative_criteria_and_audit_criteria'];kinds=Counter(q['kind'] for q in criteria);statuses=Counter(q['current']['status'] for q in criteria)
  allkind.update(kinds);allstatus.update(statuses);meta.update(q['category_A11'] for q in case['r1_fragments_reclassified']);seen_area.update(case['zone_related_controls_only'].keys());mountn+=int(bool(case['disposition_admin'].get('mount_reports')))
  for q in criteria:
   for when in ('closure','current'):ac[(when,q[when]['status'])]+=1
  cr=[];overview=[]
  for q in criteria:
   if q['current']['observed'] is not None or q['closure']['observed'] is not None:cr.append(q['id'])
   if q['current']['status']=='FAIL_DOVEDIT_LA_NIVEL_COMPONENTĂ':overview.append(q['id'])
  if any('A11-CK' in q['source_evidence_id'] for q in criteria):raise ValueError(k)
  path=T/('Fisa_'+k+'.json');dump(path,case);groups.append({'task':k,'canonical':case['canonical'],'title':case['title'],'state':case['current_status_at_primary_cutoff'],'file':'taskuri/'+path.name,'sha256':hs(path),'R1_sha256':case['r1_immutable']['sha256'],'R1_A11_score':case['r1_immutable']['A11_quality'],'operative_and_audit_checks':len(criteria),'functional_source_unidentified':case['functional_criteria_unidentified'],'criteria_with_observations':cr,'component_failures':overview,'R2_score':None});rankrows.append((k,len(cr),len(criteria)))
  if len(groups)%100==0:print('R2',len(groups),flush=True)
 assert len(groups)==651==len(queued) and set(x['task']for x in groups)==queued and meta['METADATA_NU_CRITERIU']==906 and meta['DESCRIERE_DECLARATA_NU_DOVADA']==1961
 for id_,links in inverse.items():assert id_ in evidence and all(w['task'] in queued for w in links)
 dump(R/'Dovezi_criterii.json',{'schema':'eva.audit.criterion-evidence.v2','cutoff':snapshot,'source_git_sha':sha,'evidence':evidence,'inverse_task_requirement_links':dict(inverse),'method':'Chei determinate din nivel/sursă/pointer/hash. Inversă numai pentru dovezi legate unei cerințe; referințele din context/registru nu certifică comportamentul.'})
 summ={'schema':'eva.audit.A12.round2.v1','created_utc':now(),'primary_cutoff':snapshot,'code':sha,'scope':'651 originare. T352 nou și schimbarea T366 după această fotografie nu sunt clasificate prin acest lot; cer addendum separat.','disposition':'R2_PREDAT_PENTRU_REVERIFICARE; PARȚIAL_CU_LIMITĂRI','score_r2':None,'A11_r1_score':3.0,'A11_r1_report_sha256':hs(E/'A11_control_lot1.json'),'A11_ledger_r1_sha256':hs(E/'A11_ledger_651_fise.json'),'r1_archive':'../R1/A12_raport.json','r1_sha256':hs(E/'R1/A12_raport.json'),'counts':{'r2_case_records':651,'operational_and_audit_criteria':sum(allkind.values()),'functional_criteria_unidentified':sum(v['functional_source_unidentified']for v in groups),'operative_or_audit_checks_with_observed_segment':sum(len(v['criteria_with_observations'])for v in groups),'criteria_with_component_failure':sum(len(v['component_failures'])for v in groups),'cases_with_detailed_deployment_report':mountn,'r1_fragment_reclassified':dict(meta),'criteria_by_kind':dict(allkind),'current_status_counts':dict(allstatus),'closure_and_current_states':{'/'.join(k):v for k,v in ac.items()},'historical_missing_dates':244,'exact_dates_recovered_for_that_cohort':0,'bounded_from_daily_git_snapshot':244,'evidence_count':len(evidence),'sources_linked_to_task_criterion':len(inverse)},'evidence_catalog':{'file':'Dovezi_criterii.json','sha256':hs(R/'Dovezi_criterii.json')},'source_provenance':{'archive_plans_inspected_nominally':sum(len(retrieval(k,reg[k][1])) for k in queued),'original_plan_files_by_exact_folder':len({p for k in queued for p in retrieval(k,reg[k][1])}),'RZ_history':'C03 surse originale în matricea 25.10; criteriu și amendament distincte. C10 fișă originală: se folosesc numai rezultatele cantitative/calitative explicit etichetate.','registry_history':{'file':'../A12_istoric_git_stari.json','sha256':hs(E/'A12_istoric_git_stari.json'),'limitation':'Observație datată în commit, nu montare sau exact ora închiderii.'},'frozen_zone_reports':{k:{'file':'../'+k+'_raport.json','sha256':v,'linked_candidate_cases':seen_area[k]} for k,v in mhsi.items()},'zones_not_available_at_generation':[f'A{n:02d}'for n in range(1,11)if f'A{n:02d}' not in mhsi]},'fixed_examples':['T229: act nominal de anulare, reactivare curentă și contradicția dintre liste; indice distinct pentru istoric și prezent.','T224: 3/3 documente prezente la SHA declarat și server, 0/3 bloburi la SHA fixat. Nu este lipsă de document universală ori defect funcțional.','T227: se citește tabelul de criterii al planului propriu; sql nativ pe CTE leagă porțiuni R-4/R-9/R-10/R-14/K-31, cu restul cerinței neconcludent. Forma lipsă în CESIRO nu certifică interfața.','T355: duplicarea operației de ambalare și refuz PK/0,5 legate exclusiv la cerința de arhitectură actuală; nicio acuzație retroactivă.','T354: deducerea rezervării din două G1 în componenta relevantă. T157: segment SQL închidere multi-schemă dintr-un obiectiv mai larg, fără declarare E2E. T214: testul nominal al clasei nu dovedește reconcilierea din ecran.'],'limits':['Doar stările cu probă și domeniu explicit sunt revendicate; o dispoziție administrativă validă nu certifică funcția transferată.','Criteriile de plan sunt separabile de obiectivele aprobate. Pentru sarcini cu sursă ambiguă, funcția rămâne neidentificată; nu converti descrierea registrului în criteriu.','Nombre de cerințe este un numitor pentru cele recuperate, nu garanția că toate cerințele necunoscute au fost descoperite.','Dovezile zonelor sunt context până la legătură semantică strictă, nu se transferă un finding prin simpla apartenență la capitol.','Auditul integral al implementării, acceptarea independentă și probele pe restul interfețelor sunt încă deschise.'],'records':groups}
 summ['limits'][2]='Numărul cerințelor se referă la cele recuperate, fără a pretinde că cerințele istorice necunoscute au fost identificate.'
 dump(R/'A12_raport.json',summ)
 print('DONE',summ['counts'],flush=True)
 return summ
if __name__=='__main__':run()




