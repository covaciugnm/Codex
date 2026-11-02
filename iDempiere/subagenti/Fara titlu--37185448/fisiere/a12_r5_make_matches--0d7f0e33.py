from a12_r3_survey import *
import collections,re,unicodedata,hashlib
R=E/'R5';o=R/'probe';o.mkdir(exist_ok=True);r4=E/'R4';pc=E/'R5_pregatire';cal=rd(R/'calibrare/executii.json');sq1=rd(R/'sql_batch/executii.json');sq2=rd(R/'sql_batch/recalibrare/executii.json');rootj=rd(pc/'JVM/Executii_JVM_R5.json')['runs'];roots2=rd(pc/'JVM/Calibrare_JVM_R5_2.json')
def tidy(a):return ''.join(c for c in unicodedata.normalize('NFD',a.lower())if unicodedata.category(c)!='Mn')
def kws(s):return {a for a in re.findall(r'[a-z0-9_]{3,}',tidy(s))if a not in set('care dupa tabel prin cele fiecare daca sunt doar exist exista ului nici test teste nivel dintre toate simplu valoarea cazul articol pentru compara tehnic randului valida aceeasi listei target audit cerinta metodei aceasta atunci automat pare initial pozitiv numeric asertiune executie operatie codul sursa valoare antet proba testul numarul clasa pentru runde serie coduri valoarea citeste contine posibil verifica termen procedura vizibil asteptat rezultat actual doua acesta subiect mai fara alt tabel model suma baza decizie proces portare care codul astept precizat cazuri verificari utilizator regula aceeasi prima numarul intre tipul grup integral articolul'.split())}
src=rd(r4/'Dovezi_criterii.json')['evidence'];patt=re.compile(r'\bTest[A-Z][A-Za-z0-9_]{2,}')
# Reviewed associations. A suite not in the case's nominal plan is a search lead only unless this direct task/fixture map applies.
allow={'T325':['TestPutaway','TestListaAmplasare'],'T326':['TestListaPicking','TestListaPickingEcran'],'T329':['TestLoturi','TestLoturiEcrane'],'T330':['TestFefo'],'T190':['TestReges','TestT190StudiiSql'],'T159':['TestT159LotA','TestT159LotB','TestT159LotC','TestT159LotD','TestT159DSql'],'T58':['TestT58Inchidere','TestT58Alarma','TestT58Sql'],'T03':['TestT03Lot5','TestT03Front','TestT03r1SponsSql'],'T217':['TestT217FiltruSql','TestT217Filtru'],'T220':['TestT220CorelezSql'],'T331':['TestT331Sql'],'T354':['TestT354Sql','TestT354Set','TestT354Disponibil'],'T179':['TestT179OssSql','TestT179ImpactSql'],'T256':['TestT256D394Sql'],'T155':['TestT155NepostateSql'],'T182':['TestT182D107Sql'],'T189':['TestT189SalarizareSql'],'T227':['TestT227VerificareImportSql'],'T22':['TestT22CitiriSql','TestT22TrimitereSql','TestT22MetaSql'],'T06':['TestComparatieSaga'],'T40':['TestT40L2Sql','TestT40L3Sql','TestT40L4Sql','TestT40PCfgSql'],'T42':['TestT42L2Sql','TestT42L34Sql','TestT42L5Sql','TestT42L6Sql'],'T39':['TestT29Acoperire'],'T224':['TestT224IdSpvSql'],'T21':['TestT21R2Sql'],'T323':['TestT323Productie'],'T334':['TestApiMobilInventar'],'T41':['TestT41L7Sql']}
series=collections.defaultdict(list);allunits=[]
def add(nm,tag,source,rel,rc,typ):
 if not source.exists():return
 ll=source.read_text(encoding='utf8',errors='replace').splitlines();ctx='';yst=[];group=None;desc=source.suffix
 for i,l in enumerate(ll,1):
  if re.match('^\\s*==',l):ctx=l.strip()[:380]
  if not re.match(r'^\s*(ok|fail|pass|nok)\b',l,re.I):continue
  plain=l.strip();words=kws(plain);yst.append((i,plain,ctx,words))
 record={'suite':nm,'target':tag,'source':rel,'log_sha':sha(source),'run_exit':rc,'tier':typ};idx=len(allunits);allunits.append(record);series[nm].append((idx,yst))
for x in rootj:add(x['suite'],x['target'],pc/'JVM'/Path(x['log']).name if '/'not in x['log']else pc/'JVM'/x['log'], 'R5_pregatire/JVM/'+x['log'],x.get('run_rc'),'JVM_initial_all')
rs2=(roots2.get('runs')or roots2.get('results')or [])+(rd(pc/'JVM/Calibrare_JVM_R5_3.json').get('results')or []); 
for x in rs2:
 if not isinstance(x,dict)or not x.get('log'):continue
 logpath=(pc/'JVM'/x['log']); 
 if logpath.is_file():add(x['suite'],x['target'],logpath,'R5_pregatire/JVM/'+x['log'],x.get('rc',x.get('run_rc',x.get('run'))),'JVM_calibrated_root')
for x in cal:add(x['suite'],x['target'],R/'calibrare'/x['verified_log'],'R5/calibrare/'+x['verified_log'],x['run'],'JVM_calibrated_A12')
for parent,rs in [('sql_batch',sq1),('sql_batch/recalibrare',sq2)]:
 for x in rs:
  if x.get('pglog'):add(x['task_suite'],x['target'],R/parent/x['pglog'],'R5/'+parent+'/'+x['pglog'],x['psql_exit'],'PG_actual_project_SQL')
rows=[];found=collections.defaultdict(list);used=set();lead={};caseplan={}
def matches(k,c,su,info):
 norm=c['normative_content'];keypat=re.match(r'^([KCR])[-.]0*(\d+)([a-z]?)(?=\b|\s)',norm,re.I)
 label=keypat[1].upper()+'-'+keypat[2]+keypat[3]if keypat else None
 kw=kws(norm+' '+c['expected_oracle']);label_rx=(r'(?<![A-Za-z0-9])'+keypat[1]+r'[-.]0*'+keypat[2]+keypat[3]+r'(?![a-z0-9])')if keypat else r'(?!)'
 # The product test must be explicitly named in the source row, or in a hand-checked task mapping and explicitly label the same criterion.
 explicit=su in info; keyed=re.findall(r'[A-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_]+|[A-Z]+_[A-Z][A-Z_0-9]+',info);keyed=[z for z in keyed if len(z)>5 and not z.startswith('Test')]
 by=[]
 for si,ls in series.get(su,[]):
  srec=allunits[si];q=[]
  for j,l,h,words in ls:
   overlap=kw&words;precise=re.search(label_rx,l,re.I) is not None;ctxflag=re.search(label_rx,h,re.I)is not None;symbol=next((sy for sy in keyed if sy.lower()in l.lower()),None)
   # Explicit same fixture ID is meaningful; require actual words in the assertion/label, not just a passing suite.
   if len(overlap)<2:continue
   if precise and (explicit or su in allow.get(k,[])):rtype='ID_CONTROL_ȘI_ASERȚIUNE'
   elif ctxflag and (explicit or su in allow.get(k,[])) and len(overlap)>=3:rtype='SECȚIUNE_CONTROL_ȘI_ASERȚIUNE'
   elif explicit and symbol and len(overlap)>=3:rtype='SUITĂ_ȘI_SIMBOL_NOMINAL'
   elif explicit and len(overlap)>=5 and ('→'in l or '⇒'in l or re.search(r'\b\d+/\d+\b',l)):rtype='SUITĂ_EXPLICITĂ_ȘI_ORACOL_CONCRET'
   else:continue
   score=(12 if precise else 7 if ctxflag else 6 if symbol else 3)+len(overlap)
   q.append((score,si,j,l,h,rtype,sorted(overlap)))
  if q:by.extend(sorted(q,key=lambda z:-z[0])[:2])
 return by
for z in rd(r4/'A12_raport.json')['records']:
 k=z['task'];w=rd(r4/z['file'])
 for c in [*w['operative_criteria_and_audit_criteria'],*w['R3_new_criteria'],*w['R4_new_criteria']]:
  if c['current']['status']!='NEEXECUTAT':continue
  ev=src[c['source_evidence_id']]['content_or_observation'];sinfo=(ev.get('row')or ev.get('literal')or '')if isinstance(ev,dict)else ''
  info=c['normative_content']+' '+c['expected_oracle']+' '+str(sinfo);suites=set(allow.get(k,[]))|set(patt.findall(info));cand=[]
  for su in suites:cand+=matches(k,c,su,info)
  if cand:found[c['id']]=cand
# Assign a concrete observation only once per (suite,target,line/tier), preserving secondary hits as uncredited leads.
# Calibrated/SQL observations outrank environment-failed runs for the same testcase.
owners={};citems=[]
for cid,li in found.items():
 for score,si,no,txt,head,rule,kws0 in li:
  sr=allunits[si];key=(sr['suite'],sr['target'],tidy(txt));score+= 3 if sr['tier']in ('PG_actual_project_SQL','JVM_calibrated_A12') else 1 if 'calibrated' in sr['tier'] else 0
  cur=owners.get(key)
  if cur is None or score>cur[0]:owners[key]=(score,cid,si,no,txt,head,rule,kws0)
for key,(_,cid,si,no,txt,head,rule,overlap) in owners.items():
 su=allunits[si];lk='OBS-'+hashlib.sha256((su['suite']+'|'+su['target']+'|'+tidy(txt)).encode()).hexdigest()[:18];citems.append({'criterion':cid,'unique_observation':lk,'suite':su['suite'],'target':su['target'],'tier':su['tier'],'source':su['source'],'source_sha256':su['log_sha'],'line':no,'header':head,'literal':txt[:530],'actual_marker':txt.split()[0].upper(),'matching_contract':rule,'overlap_used_only_to_select_the_line':overlap,'suite_rc':su['run_exit']})
wr(o/'executii_corelate.json',{'source_runs':allunits,'records':sorted(citems,key=lambda r:(r['criterion'],r['target'],r['line'])),'constraints':'O aserțiune specifică primește un singur ID și este atribuită la un singur criteriu în fiecare țintă. Nu se acordă PASS de implementare din potrivire de text sau din exit-code-ul suitei. Semnificația subsetului observat trebuie păstrată împreună cu rândul original și regiunea de cod/fixtură.'});print('runs',len(allunits),'candidates',len(found),'claimed',len(set(i['criterion'] for i in citems)),'assertions',len(citems))

