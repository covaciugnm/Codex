"""Build plan traceability only. Reads Git objects/diffs and signed registries. Executes no target code."""
import os,sys,re,json,hashlib,subprocess,collections,datetime
from pathlib import Path,PurePosixPath
B=Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');O=B/'executie/R11_plan_delta';G=Path(r'D:\CodexWork\eva-audit-p01-src-20261101');ENV={**os.environ,'GIT_NO_LAZY_FETCH':'1'};rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(G),*a],env=ENV);inv=rd(O/'Inventar_delta_1632.json');index=rd(B/'Index_trasabilitate.json');cv=rd(O/'A01_contributie_5_cai_si_A06.json');gate=rd(O/'A11_verdict_plan_delta_R11_v1.json');a=inv['base'];b=inv['new_head'];N=inv['rows'];assert len(N)==1632
raw=git('-c','core.quotepath=false','diff','--raw','--abbrev=40','-z','--no-renames',a,b);s=raw.strip(b'\0').split(b'\0');rr={s[i+1].decode('utf8'):s[i].decode('ascii').split() for i in range(0,len(s),2)};assert set(rr)=={r['path'] for r in N}; assert len(rr)==len(N); 
regdir='Documentatie/echipa-2026-10-09/';regf=regdir+'00_STATUS_TASKURI.json';mapf=regdir+'00_CORESPONDENTA_COD_CAPITOL.json';m=json.loads(git('show',b+':'+mapf));r=json.loads(git('show',b+':'+regf));status={v['id']:(i,v) for i,v in enumerate(r) if v.get('id')};codes={k:[(i,z) for i,z in enumerate(m['coduri']) if z.get('id_tehnic')==k] for k in status};edges={x['id']:(i,x) for i,x in enumerate(index['pipelines'])};ctrlindex={x['id']:(i,x) for i,x in enumerate(index['controls'])};seedby={r['path']:r for r in cv['registered_five_paths']};R12=rd(B/'A12_plan_taskuri.json');
def oneedge(c,p):
 i,row=edges[p]; j=row['resolved_control_ids'].index(c);assert c in ctrlindex;return {'control':c,'pipeline':p,'pointer':f'Index_trasabilitate.json#/pipelines/{i}/resolved_control_ids/{j}'}
def tlookup(k):
 if k not in status:return {'technical':k,'scope':'ABSENT_DIN_REGISTRUL_NOU','canonical_direct':[],'transitive':[]}
 n,row=status[k];pairs=codes.get(k,[]);seen=[]
 for i,z in pairs:
  if z['cod'] not in [v['code'] for v in seen]:seen.append({'code':z['cod'],'pointer':f'{mapf}#/coduri/{i}'})
 ds=seen;trans=[];owners=[]
 if not ds:
  target=row.get('agregat_in');
  if isinstance(target,str) and target!=k and target in status:
   for i,z in codes.get(target,[]):trans.append({'relation':'agregat_in','target_technical':target,'code':z['cod'],'pointer':f'{mapf}#/coduri/{i}','relation_pointer':f'{regf}#/{n}/agregat_in'})
  for x in m.get('inchise_prin_impartire',{}).get(k,[]):
   if x not in [t['code'] for t in trans]:trans.append({'relation':'split_not_direct','code':x,'pointer':f'{mapf}#/inchise_prin_impartire/{k}'})
  if not trans:
   for i,z in enumerate(m['coduri']):
    if z.get('origine')=='P01.'+k or 'P01.'+k in (z.get('id_vechi') or []):trans.append({'relation':'origine/alias, not same ID','target_technical':z.get('id_tehnic'),'code':z['cod'],'pointer':f'{mapf}#/coduri/{i}'})
 return {'technical':k,'registry_pointer':f'{regf}#/{n}','state_at_new_Git':row.get('stare_generala'),'scope':'P01_DIRECT' if ds and all(x['code'].startswith('P01.') for x in ds) else 'OTHER_PROJECT_DIRECT' if ds else 'LEGACY_OR_NO_DIRECT_CANONICAL_CODE','canonical_direct':ds,'transitive':trans}
group_defs={
 'AUTH_PROXY':('A01','A09','Garda consolei, separarea căilor și contextul de cabinet',[('A01.C16','A01.P03'),('A01.C08','A01.P03')]),
 'IAM':('A01','A09','Drepturi de rol/firma, grant și revocarea accesului',[('A01.C20','A01.P06'),('A01.C16','A01.P03')]),
 'PERSONAL':('A01','A09','Minimizarea datelor în clone și dovezi, mascare controlată',[('A01.C29','A01.P06'),('A01.C28','A01.P09')]),
 'HELP':('A09','A01','Manualul de ajutor, ecranele/ilustrațiile/rolurile, localizare și recuperare',[('A09-C25','A09-P6'),('A09-C26','A09-P6')]),
 'CHANNEL':('A06','A08','Canal/instanță și mapare ofertă, legături și operații în iDempiere',[('A08-C02','A08-P01'),('A06-C26','A06-P6')]),
 'CHANNEL_SETTINGS':('A08','A06','Rutare și configurație per site/canal, separare de funcțiile comisionarului',[('A08-C02','A08-P01'),('A08-C05','A08-P01')]),
 'ORDERIMPORT':('A06','A08','Import și actualizare comenzi, idempotency, administrarea exclusiv în ERP',[('A06-C18','A06-P4'),('A06-C19','A06-P4')]),
 'CRM':('A06','A08','Client/campanie și acces la operațiile proprii',[('A06-C23','A06-P6'),('A06-C30','A06-P6')]),
 'SAGA':('A04','A03','Pornirea firmei și import SAGA. Delimitare READ/WRITE, corelare și recuperare',[('A04-C11','A04-P4'),('A04-C12','A04-P4')]),
 'EFISCAL':('A03','A07','Document fiscal și coadă/recipisă; nicio transmitere externă',[('A03.CK22','A03.PL10')]),
 'G3MATRIX':('A06','A02','Produs × canal, preț/cantitate/termen și mapare CPP/CPA',[('A06-C15','A06-P3'),('A08-C06','A08-P02')]),
 'INVENTORY':('A05','A02','Document inventar și diferențe, trasabilitate cantitate și cost',[('A05-C18','A05-P05')]),
 'RET':('A07','A03','Retur comercial, logistic și financiar',[('A07.K21','A07.P5'),('A07.K22','A07.P5')]),
 'RELEASE':('A10','A01','Artefact distribuibil, configurație, hash Git vs binar instalat',[('A10-CK-01','A10-F01'),('A10-CK-03','A10-F01')]),
 'TOOLS':('A10','A01','Scripțuri/suite transversale, coadă, izolare, execuție fără efect operațional',[('A10-CK-07','A10-F02')]),
 'META':('A02','A06','Metadate/persistență partajată; revizuirea separată a fragmentelor DD, canal, ajutor și roluri',[('A02.C009','A02.P02'),('A08-C02','A08-P01')]),
 'CURRENCY_OTHER':('A03','A12','Context monetar proiect diferit. Nu este task P01 și se păstrează doar interfața funcțională',[('A06-C15','A06-P3')]),
 'GOV':('A12','A11','Documentarea, registrul, coordonarea, stările proiectului și acceptanțele',[])}
tasks_group={'T18':'SAGA','T35':'CHANNEL','T211':'CHANNEL','T213':'CRM','T224':'EFISCAL','T228':'SAGA','T232':'AUTH_PROXY','T234':'IAM','T236':'PERSONAL','T240':'HELP','T291':'RELEASE','T315':'RET','T318':'CHANNEL_SETTINGS','T321':'CHANNEL_SETTINGS','T343':'ORDERIMPORT','T352':'G3MATRIX','T366':'INVENTORY','T384':'CURRENCY_OTHER','T385':'GOV'}
exe_ext={'.py','.sql','.sh','.java','.mjs','.js','.cjs','.yaml','.yml','.jar'};idsreg=re.compile(r'(?<![\w])(?:P01\.)?(T\d{1,4}(?:\.\d{1,3})?)(?![\w])',re.I);ncode=re.compile(r'\bP(?:01|03|05)\.C\d{2}\.T\d{4}(?:\.\d+)?\b',re.I)
def literaladded(path):
 ds=git('diff','-U0',a,b,'--',path).decode('utf8','replace');n=0; refs=[]
 for l in ds.splitlines():
  if l.startswith('@@'):
   mt=re.search(r'\+(\d+)',l);n=int(mt.group(1)) if mt else 0
  elif l.startswith('+') and not l.startswith('+++'):
   for mt in idsreg.finditer(l[1:]):
    k=mt.group(1).upper();
    if k in status and (k,n) not in refs:refs.append((k,n))
   n+=1
  elif l.startswith(' '):n+=1
 return refs
def binary_ref(path):
 return ('Bundle iDempiere publicat în Git și folosit de mai multe funcții. Hashul containerului/JAR/class se va compara separat; nu atribui întregul binar unui singur task sau probei de sursă.')
def classify(z):
 p=z['path'];pp=PurePosixPath(p);name=pp.name;ext=pp.suffix.lower();arr=p.split('/');links=[];notes=[];agg=None;direct_type='';explicit=[];context=[];exclude=None;mode=None;secondary=[];reason=None
 if p in seedby:
  q=seedby[p];group='AUTH_PROXY';direct_type='DIRECT_DIN_SURSA_PLANIFICATĂ_ȘI_REGISTRU';explicit=['T232'];context=['T232.01'];mode='EXECUȚIE_ISOLATĂ_PROIECTATĂ';notes.append(f'Ancore SHA/linie/cazuri din A01_contributie_5_cai_si_A06.json#/registered_five_paths/{list(seedby).index(p)}. T232.01 este subtask corelat, nu o afirmație că fiecare fișier îi aparține exclusiv.');links=q['parent_edges'];secondary=['A10'] if p.startswith('proxy/') else []
 elif p.startswith('Documentatie/'):
  k=re.match(r'Documentatie/echipa-2026-10-09/(T\d+)(?:-|/)',p);topic=k.group(1) if k else None; group=tasks_group.get(topic,'HELP' if p.startswith('Documentatie/help/') else 'GOV'); direct_type='DOSAR_DE_TASK__ATRIBUIRE_DOCUMENTARĂ';
  if topic:explicit.append(topic)
  else:direct_type='TRANSVERSAL_FĂRĂ_TASK_UNIC';reason='Registru/manual/istoric transversal fără task unic demonstrat în cale.'
  if ext in exe_ext:
   mode='ARTEFACT_EXECUTABIL_ÎN_DOSAR_DOCUMENTAR';notes.append('Se revizuiește conținutul ca script/probă, nu ca simplu text; audit static/fixture izolat după gate, fără a executa scripturi de cabinet/montare pe țintele originale.');
   if topic:agg='DOSSIER:'+topic
  elif ext in {'.png','.jpg','.jpeg'}:
   mode='DOVADĂ_VIZUALĂ_DOCUMENTARĂ';exclude='Exclus numai din lista de cod executabil: captură statică, verificată individual prin OID și legată de UI/rol, nu probă a funcționării la noul HEAD.'
  elif ext in {'.tsv','.json','.jsonl'}:
   mode='TRASABILITATE_DATE_STRUCTURATE';exclude='Registru, captură structurată sau vector de probe, nu modul FE/BE. Se verifică schema/proveniența, referenced IDs și consumatorii înainte de a clasifica eventualul efect runtime.'
  else:
   mode='TRASABILITATE_DOCUMENTARĂ';exclude='Fișier text de analiză/raport/rezultat/istoric din dosarul indicat. Nu se substituie probei de funcționare; se urmăresc cerința, data, sursa și contradicțiile documentare.'
  if topic and topic in ['T384','T385']:notes.append('Proiect canonic diferit de P01 în maparea nouă. Nu este adăugat la numitorul de taskuri finalizate P01; context/excepție explicită.')
 elif p.startswith('tools/'):
  m0=re.match(r'tools/teste/t(\d+)(?:_\w+)?/',p);task='T'+m0.group(1) if m0 else None;mode='EXECUȚIE_TEST_LOCAL/REVIZIE_SCRIPT';group=tasks_group.get(task,'HELP' if p.startswith('tools/help/') else 'TOOLS');
  if task:explicit=[task];direct_type='CAZ_TEST_NUMIT_ÎN_CALE';notes.append('Lotul de teste din calea numerotată stabilește relația nominală, nu rezultatul testului.')
  elif p.startswith('tools/help/'):
   direct_type='TRANZITIV_FAMILIE_AJUTOR';context=['T240'];agg='HELP_TOOLCHAIN';reason='Utilitar de creare/verificare a ajutorului. Familia T240 este legată prin funcția comună, nu atribuire exclusivă demonstrată pentru acest fișier.'
   if 'mascheaza' in name:secondary+=['A01']
  else:direct_type='UTILITAR_COMUN';reason='Runner comun al setului contab/SAGA, cu multe sarcini și efecte potențiale. Legarea exclusivă de un task ar fi nefondată.';agg='RUNNERS_SHARED';notes.append('Verifică modificările de selecție a testelor per hunk, inclusiv ordinea/izolarea și protecția bazelor.')
 elif p.startswith('scripts/'):
  group='TOOLS';mode='STATIC_NON_OPERATIONAL';direct_type='SCRIPT_DE_REPO_COMUN';reason='Script de sincronizare oglindă; nicio legătură de implementare contractuală cu un singur task este demonstrată.';notes.append('Nu executa push/scrieri remote; verifică filtrarea, destinația și excluderile cu fixture local.')
 elif ext=='.jar':
  group='RELEASE';mode='ACOPERIT_PRIN_VERIFICAREA_BINARULUI';direct_type='AGREGAT_BINAR';agg='BUNDLE:'+name;reason=binary_ref(p);secondary+=['A02','A06'] if 'com.eva.ro.contab' in p else ['A01'];notes.append('Inspecție inventar intrări clase/resurse vechi/nou; JAR din Git diferă conceptual de runtime. Componente corelate prin clase selectate după gate.')
 elif '/ajutor/res/' in p or 'fixtures/help/' in p:
  group='HELP';mode='RESURSĂ_EMBARCATĂ';context=['T240'];direct_type='TRANZITIV_CONSUMATOR_AJUTOR';agg='HELP_RESOURCE:'+('/'.join(arr[-2:]) if name in ('zone.json',) else name);reason='Resursa este consumată de funcția comună de ajutor. Identitatea ecranului identifică help-ul, nu proprietatea exclusivă a acelui ecran de către T240.';notes.append('Verifică asocierea ecran→captură/zone/texte, română+i18n, rol, contrast și existența resursei în JAR. Pentru TSV/JSON verifică și conținutul structurat, nu doar hash.')
 elif 'com.eva.ro.saga.native' in p:
  group='AUTH_PROXY';mode='EXECUȚIE_ISOLATĂ_COD';direct_type='TRANZITIV_COMPONENTĂ_GARDĂ' if ext!='.java' else 'COD_GARDĂ_CU_REFERINȚĂ';context=['T232'];secondary=['A10'];agg='SAGA_NATIVE_GUARD';reason='Manifest/componenta OSGi aparțin unui plugin partajat. Numai delta de înregistrare/filtrare a gărzii este atribuită T232; registrul global al pluginului necesită review separat.' if ext!='.java' else 'Componenta Java este în familia gărzii consolei; verifică explicit identificatorul în hunk, apoi comparația cu JAR.'
 elif name in ('CorelareTabele.java','EvaMetadata.java','etichete.tsv'):
  group='META' if name!='etichete.tsv' else 'HELP';direct_type='RESURSĂ/PUNCT_DD_COMUN';mode='REVIEW_SEPARAT_PE_FRAGMENTS';agg='SHARED:'+name;reason='Registru DD, set de tabele sau mesaje partajat între taskuri. Citările din hunk sunt ancore locale; nu justifică atribuirea tuturor modificărilor unui singur task.';secondary=['A08','A09','A06'];
 elif '/corelare/' in p or '/form/' in p:
  group='ORDERIMPORT' if name=='PreiaDinSite.java' else 'CHANNEL_SETTINGS' if name in ('SursaSiteConfig.java','DialogSursaSite.java','DialogCanal.java','PanouScrieriPlatforma.java') else 'CHANNEL';mode='EXECUȚIE_ISOLATĂ_COD' if ext=='.java' else 'RESURSĂ_EMBARCATĂ';direct_type='HUNK_EXPLICIT_SAU_CONTEXTE_MULTIPLE';agg='CHANNEL_CORE';context=['T211'];reason='Componenta aparține fluxului de canal/import. Citațiile adăugate în hunk dovedște legătura nominală numai a fragmentului. Restul se verifică între sursă, configurație și JAR.';secondary=['A08','A06','A02'];
 else:
  group='HELP' if name in ('TestAjutor.java','TestListaAmplasare.java','TestListaPickingEcran.java','TestT163Ecran.java','TestT25Ecran.java','TestT40L4Ecran.java') else 'CHANNEL' if name.startswith(('TestT211','TestT35')) else 'META';direct_type='TEST_ÎN_MODUL_PARTAJAT';mode='EXECUȚIE_TEST_LOCAL/REVIZIE_SCRIPT';context=['T240'] if group=='HELP' else ['T211'] if group=='CHANNEL' else [];reason='Testul verifică o interfață/funcție cu dependențe multiple; sursa nominală din nume și citările în delta sunt separate.';agg='TESTS:'+group
 if (p.startswith('idempiere/') and ext in {'.java','.tsv','.xml','.mf'} and not '/ajutor/res/' in p) or (p.startswith('tools/') and not explicit and ext in exe_ext):
  added=literaladded(p);counts=collections.Counter(k for k,n in added); ds=[(k,n) for k,n in added if '.' not in k][:22];notes.extend([f'git:{b}:{p}:{n} conține {k} în linie adăugată; referință locală, nu atribuirea întregului fișier.' for k,n in dict.fromkeys(ds)][:5]);
  for k in counts:
   if k not in explicit and '.' not in k:explicit.append(k)
  if explicit and direct_type.startswith('TRANZITIV') and len(explicit)<5:direct_type+='; REFERINȚĂ_LITERALĂ_ÎN_FRAGMENT'
 if p.startswith('idempiere/') and name.startswith('TestT'):
  mt=re.match(r'Test(T\d+)',name)
  if mt and mt.group(1) in status and mt.group(1) not in explicit:explicit.append(mt.group(1));notes.append('ID tehnic este explicit în numele testului. Cazul poate conține și cerințe ale altor taskuri.')
 context=[k for k in context if k not in explicit];gr=group_defs[group];links=links or [oneedge(c,pipe) for c,pipe in gr[3]];notes.append(gr[2]);
 if not explicit and not context and not reason:reason='Nu există cheie canonică directă verificată. Se păstrează responsabil și peer pe suprafață pentru control ulterior.'
 owner,peer=gr[:2];
 if p in seedby:owner,peer=seedby[p]['owner'],seedby[p]['peer']
 if group=='META':secondary+=['A09']
 return {'family':group,'owner':owner,'peer':peer,'v1_owner':z['owner'],'v1_peer':z['peer'],'interfaces':[i for i in dict.fromkeys(secondary) if i not in (owner,peer)],'disposition':mode,'inclusion_basis':notes,'relationship_type':direct_type,'literal_or_folder_task_ids':list(dict.fromkeys(explicit)),'transitive_context_task_ids':list(dict.fromkeys(context)),'association_limit_or_reason_absent':reason,'parent_control_pipeline_edges':links,'product_execution_exclusion':exclude,'aggregate_group':agg,'before_gate_status':'PLAN_NON_EXECUTAT'}
rows=[];measuredtasks=set();gcnt=collections.Counter()
for n,z in enumerate(N):
 p=z['path'];sha=rr[p]; assert sha[-1]==z['change']; assert (z.get('old') or {}).get('git_oid','0'*40)==sha[2] and (z.get('new') or {}).get('git_oid','0'*40)==sha[3]; v=classify(z);assert v['owner']!=v['peer'];measuredtasks.update(v['literal_or_folder_task_ids']+v['transitive_context_task_ids']);gcnt[v['family']]+=1;rows.append({'path':p,'git_status':z['change'],'old':z.get('old'),'new':z.get('new'),'inventory_pointer':f'Inventar_delta_1632.json#/rows/{n}',**v})
taskref={k:tlookup(k) for k in sorted(measuredtasks)}
for row in rows:
 keys=row['literal_or_folder_task_ids']+row['transitive_context_task_ids'];row['task_references']=[{'technical':k,'canonical_direct':[u['code'] for u in taskref[k]['canonical_direct']],'canonical_via_relation':[u['code'] for u in taskref[k]['transitive']],'dictionary_pointer':'#/task_dictionary/'+k,'binding':'DIRECT_LOCATOR_OR_LITERAL' if k in row['literal_or_folder_task_ids'] else 'TRANSITIVE_OR_CONTEXT'}for k in keys];
 if not keys and row['disposition'].startswith('TRASABILITATE') and not row['product_execution_exclusion']:raise AssertionError(row['path'])
 if not row['parent_control_pipeline_edges'] and not row['product_execution_exclusion']:
  if row['family']=='GOV':row['product_execution_exclusion']='Control de metodă/registru A12, nu operație produs; se păstrează în reconcilierea taskurilor și se examinează static situațiile/artefactele.'
  else:raise AssertionError(row['path'])
 assert keys or row['association_limit_or_reason_absent'];assert row['owner'] and row['peer']
v2={'schema':'eva.audit.R11.path-traceability.v2','utc':datetime.datetime.now(datetime.UTC).isoformat(),'base':a,'head':b,'mode':'PLAN. Fără execuție pentru noul SHA. Comparație netă de arbori, fără afirmație de genealogie în clonă shallow.','source_hashes':{'inventory_delta':h(O/'Inventar_delta_1632.json'),'index_trasabilitate':h(B/'Index_trasabilitate.json'),'A11_rejection_v1':h(O/'A11_verdict_plan_delta_R11_v1.json'),'A01_five_files':h(O/'A01_contributie_5_cai_si_A06.json'),'new_status_registry_blob_oid':git('rev-parse',b+':'+regf).decode().strip(),'new_status_registry_sha256':hashlib.sha256(git('show',b+':'+regf)).hexdigest(),'new_canonical_map_blob_oid':git('rev-parse',b+':'+mapf).decode().strip(),'new_canonical_map_sha256':hashlib.sha256(git('show',b+':'+mapf)).hexdigest()},'A11_v1_gate':{'decision':gate['decision'],'score':gate['quality_score_plan'],'execution_authorized':False,'criterion_addressed':'R11-P2; celelalte blocaje P1/P3/P4 sunt în planul revizuit al coordonatorului.'},'scope':'Fișier cu dispoziție individuală pentru 1.632 căi schimbate, inclusiv scripturile din Documentatie. Nu este inventarul întregului repo și nu dovedește comportament; inventarul tuturor fișierelor și verificarea tuturor taskurilor se reconciliază separat.','association_rules':['DIRECT_LOCATOR_OR_LITERAL = ID explicit în cale/dosar ori linie adăugată. Asocierea documentală a unui dosar dovedește originea dovezii, nu implementarea unui task.','TRANSITIVE_OR_CONTEXT = familie funcțională/consumator, fără atribuire exclusivă; în task_dictionary, agregat_in/origine/împărțire sunt relații, niciodată sinonime de task.','Pentru taskuri din alt proiect conservăm codul real din registrul nou și nu le însumăm în P01.','Nr. și hashurile OID sunt verificate contra git diff --raw --no-renames; nul la old/new înseamnă adăugare/ștergere.','Documentele nu se numără ca teste. Scripts/SQL/Java în Documentatie rămân în audit cu statut executabil sau revizuire statică izolată înainte de orice execuție ulterioară.','Atribuirile funcționale din v2 păstrează owner/peer v1 pentru auditarea schimbării. Reviewer independent A11; arbitraj distinct unde rămân module comune.'],'summary':{'expected':1632,'actual':len(rows),'unique':len(set(z['path'] for z in rows)),'git_raw_oid_and_status_verified':len(rows),'file_families':dict(gcnt),'dispositions':dict(collections.Counter(z['disposition'] for z in rows)),'owner_counts':dict(collections.Counter(z['owner'] for z in rows)),'files_without_conclusive_task':sum(not z['task_references'] for z in rows),'non_P01_direct_ids':[k for k,v in taskref.items() if v['scope']=='OTHER_PROJECT_DIRECT'],'unresolved_task_ids':[k for k,v in taskref.items()if v['scope']=='ABSENT_DIN_REGISTRUL_NOU'],'total_traced_executable_under_documentatie':sum(z['disposition']=='ARTEFACT_EXECUTABIL_ÎN_DOSAR_DOCUMENTAR' for z in rows)},'task_dictionary':taskref,'rows':rows}
p=O/'Trasabilitate_delta_v2.json';assert not p.exists();p.write_text(json.dumps(v2,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('SHA256',h(p),'bytes',p.stat().st_size,v2['summary']);
