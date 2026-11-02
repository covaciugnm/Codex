from pathlib import Path
from functools import lru_cache
import gzip,json,re,hashlib,collections,datetime,unicodedata,sys,subprocess,html
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');D=Path(r'D:\CodexWork\A12_evidence_20261102');L=Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102');E=B/'executie';O=E/'taskuri';O.mkdir(exist_ok=True)
def rd(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,z):Path(p).write_text(json.dumps(z,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
def hs(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(s):return ' '.join(str(s or '').casefold().split())
def clean(s):
 s=str(s or '').strip();s=re.sub(r'(?i)((?:[A-Za-z0-9_.-]*password|parola|secret_key|api_key|token)\s*[=:]\s*)(\S+)',r'\1[redactat]',s);s=re.sub(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}', '[email redactat]',s);return s
def uniq(a):return list(dict.fromkeys(a))
def ul(s):return s if isinstance(s,list) else ([] if s is None or s=='' else [s])
@lru_cache(maxsize=1400)
def blob(o):
 try:return gzip.decompress((D/'blobs'/(o+'.gz')).read_bytes()).decode('utf-8-sig',errors='replace')
 except FileNotFoundError:return ''
m=rd(D/'map.json');P=m['target_paths'];alltree={}
for z in (D/'fulltree.raw').read_bytes().split(b'\0'):
 if z:
  h,n=z.split(b'\t',1);alltree[n.decode()]=h.split()[2].decode()
rg=rd(B/'capturi/00_STATUS_TASKURI.json');reg={x['id']:x for x in rg};idxs={x['id']:j for j,x in enumerate(rg)}
IX=[x for x in rd(B/'A12_index_taskuri.json')['rows'] if x['individual_review']];GI={x['id']:x for x in rd(E/'A12_referinte_git.json')['rows']};TR={x['ref']:x for x in rd(B/'Index_trasabilitate.json')['tasks']};co=rd(B/'capturi/00_CORESPONDENTA_COD_CAPITOL.json');cs={x['cod']:x for x in co['coduri']};bundle=rd(E/'Diferente_bundle_CESIRO.json');bund={x['class']:x for x in bundle['rows']};db=rd(E/'A12_DB_metadate_CESIRO.json');forms={x['classname']:x for x in db['rows']['forms'] if x['classname']};procs={x['classname']:x for x in db['rows']['processes'] if x['classname']};tables={x['tablename'].casefold():x for x in db['rows']['tables']};CMP=rd(D/'commitdiff.json');gate=rd(B/'A11_verdict_plan.json');assert gate['score']==10 and not gate['open_hard_blockers'];SHA=gate['independent_baseline']['repo_sha']
plan=rd(B/'A12_plan_taskuri.json');assert all(v.get('implementation_status')=='NEEXECUTAT' for v in IX)
rp=lambda su:next(n for n in P if n.endswith(su))
p99=rp('/99_PROPUNERE_PAS3.json');p99a=rp('/99a_DECIZII_PROPRIETAR_PAS3.md');p32=rp('/32_RASPUNSURI_PROPRIETAR.md');pold=rp('/00_DECIZIE_PROPRIETAR_APLICATIA_VECHE_20261023.md');p125='historical/55808bac2d/02a_inventar.json'
old={x['cod']:x for x in json.loads(blob(P[p125]))['coduri']};prop=json.loads(blob(P[p99]));mapping=prop['corespondenta']
cards={Path(p).stem:(p,json.loads(blob(o))) for p,o in P.items() if '/cartele_pas3/' in p and p.endswith('.json')}
scope_status=collections.defaultdict(list);examples=collections.Counter();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def lines(o):return blob(o).splitlines()
def evidence(pp,line,statement,kind,why,oid=None):
 oid=oid or P[pp];return {'type':kind,'git_blob':oid, 'path':pp,'line_or_json_pointer':line,'quote':clean(statement)[:750], 'interpretation':why}
def atom(s):
 return [x.strip() for x in re.split(r'(?:\s*;\s*|(?<=[.!?])\s+(?=[A-ZĂÎÂȘȚ„«])|\n(?=\s*[-•]))',clean(s)) if len(x.strip())>5]
def canon(x):return x.get('cod_capitol') or next((t['cod'] for t in co['coduri'] if t['id_tehnic']==x['id']),None)
def deepstrings(d):
 if isinstance(d,dict):return '\n'.join(deepstrings(i) for i in d.values())
 if isinstance(d,list):return '\n'.join(deepstrings(i) for i in d)
 return str(d or '')
def push(why,task):scope_status[why].append(task)
def get_histproof(k,v,j,cur):
 ss=m['task_declared_and_context_paths'][k]; res=[]; original=deepstrings({f:v.get(f) for f in ['fisier','cerere_proprietar','origine','sursa_deciziei','explicatii','observatii']})
 for pp,why in ss.items():
  if 'citare în registru' not in why and 'fisier' not in why and 'link declarat' not in why and 'document declarat' not in why:continue
  oid=P[pp];text=lines(oid)
  if not text:continue
  nm=Path(pp).name
  cits=uniq(int(i) for i in re.findall(re.escape(nm)+r'[:#](\d+)',original))
  meth='linie literal indicată de sursa taskului' if cits else None
  if not cits:
   candidates=[i for i,l in enumerate(text,1) if re.search(r'(?<![\w.])'+re.escape(k)+r'(?![\w.])',l,re.I)]
   if candidates:cits=candidates[:2];meth='mențiune exactă ID; nu conferă singură acceptare'
   else:
    cits=next(([i] for i,l in enumerate(text,1) if len(l.strip('# -*'))>=12 and len(l)<650),[]);meth='context document referit; NU probă de acceptare pentru task'
  for ii in cits:
   if 1<=ii<=len(text):res.append(evidence(pp,ii,text[ii-1], 'HISTORICAL_REFERENCE',meth))
 return res
def manifest_current(file):
 p=L/file
 if not p.is_file() or p.stat().st_size>700000:return None
 bb=p.read_bytes();o=hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()
 if o!=alltree.get(file):return None
 return bb.decode('utf-8-sig','replace').splitlines()
def history_doc(d):
 ref=d['ref'];cks=[{'kind':ck['kind'],'spec':ck['spec'],'result':ck.get('result')} for ck in d['checks']];out={'artifact':d['tip'],'ref_type':d['type'],'ref':ref,'checks':cks}
 for h in cks:
  w=h.get('result') or {};o=w.get('oid');ty=w.get('type')
  if ty=='commit' and o in CMP:
   dd=CMP[o]; changes=dd['changed']; code=[(z['path'],alltree.get(z['path'])==z['after']) for z in changes if Path(z['path']).suffix.lower() in {'.java','.py','.js','.rb','.sql','.xml','.html','.css','.tsx','.ts','.yml','.sh'} and not z['path'].startswith(('Documentatie/','Log-Istoric/'))]
   out.setdefault('commits',{})[o]={'commit_subject':clean(blob(o).split('\n\n',1)[-1].splitlines()[0])[:400] if blob(o) else None,'is_ancestor_of_pinned':dd['ancestor'],'diff_paths_total':len(changes),'non_document_code_paths_count':len(code),'same_blob_at_target_count':sum(a for _,a in code),'code_paths_now':code if d['tip']=='PRD-COD' else [],'caution':'Merge-base non confirmé ne signifie pas absence du contenu. Chaque path compare le blob après commit au blob cible. Cambios de una integración pueden incluir otras tareas.'}
  if ty=='blob' and (D/'blobs'/(o+'.gz')).exists():
   ls=lines(o);matches=[(j,clean(s)[:350]) for j,s in enumerate(ls,1) if re.search(r'(?:verdict|neexecutat|nu trece|nu a trecut|blocant|10/10|T\d+.*r[eé]zultat)',s,re.I) and len(s)<1100]
   out.setdefault('historical_content',{})[o]={'lines':len(ls),'text_excerpt':matches[:3] if matches else next(([(j,clean(s)[:350])] for j,s in enumerate(ls,1) if s.strip() and len(s)<800),[]),'scope':'Text istoric citit; nota veche/integrarea nu este PASS în această misiune.'}
 return out
def codechecks(docs,k):
 pool={}
 for a in docs:
  if a['artifact']!='PRD-COD':continue
  for o,commit in a.get('commits',{}).items():
   for fn,ident in commit['code_paths_now']:
    pool[fn]=o
 # Prioritize own named task paths; evaluate every candidate Java class matched materially to this task's PRD commit.
 info=[]
 for fn,o in pool.items():
  if not fn.endswith('.java') or '/test/' in fn:continue
  ls=manifest_current(fn)
  if not ls:continue
  pkg=next((re.search(r'^\s*package\s+([\w.]+)',i)[1] for i in ls if re.search(r'^\s*package\s+([\w.]+)',i)),None);cls=Path(fn).stem
  if not pkg:continue
  fqn=pkg+'.'+cls; ci=fqn.replace('.','/')+'.class'; metadata=forms.get(fqn) or procs.get(fqn)
  # Claim strict: registration in AD is necessary only for an actual iDempiere entrypoint, not all classes.
  if metadata or ci in bund or re.search(r'(?:extends ADForm|implements IFormController)', '\n'.join(ls)):
   table_names=uniq(t[0] for l in ls for t in re.findall(r'\b(?:FROM|JOIN|UPDATE|INTO)\s+([A-Za-z][\w]+)',l,re.I) if t.casefold() in tables) if False else uniq(t for l in ls for t in re.findall(r'\b(?:FROM|JOIN|UPDATE|INTO)\s+([A-Za-z][\w]+)',l,re.I) if t.casefold() in tables)
   info.append({'path':fn,'blob_at_sha':alltree[fn],'class':fqn,'line':next((i for i,l in enumerate(ls,1) if re.search(r'\b(?:class|interface)\s+'+re.escape(cls)+r'\b',l)),None),'bundle_status':bund.get(ci,{}).get('status'),'ad_dictionary_record':metadata,'tables_bound_by_literal_sql_and_ad_catalog':table_names,'scope':'Vérifie déclaration/metadata/aval SQL. Ni appel effectif ni autorisation d’une session; les classes du commit peuvent relever de tâches voisines.'})
 return info
def actual_report(v):
 k=v['source_id'];t=reg[k];state=v['source_state'];gr=GI[k];hist=get_histproof(k,t,idxs[k],v);facts=[];ev=[];find=[];req=[];owner=v['chapter_owner'];nk=v['canonical'];target=v['aggregate_target'];appr=False;transfer=None;cn=canon(reg[target]) if target else None
 req.extend([{'source':'registre:cerere_proprietar','text':s,'basis':'Reconstituée' if v['obligations'][0]['source_quality']=='RECONSTITUIT_DECLARAT' else 'registre'} for s in atom(t.get('cerere_proprietar') or '')])
 req.extend([{'source':'registre:descriere','text':s,'basis':'Țintă/descriere declarată; nu automat criteriu acceptat la închidere'} for s in atom(t.get('descriere') or '')])
 # inspect identity-preserving primary project decisions and actual target content.
 if target:
  row=mapping.get(k);same=(norm(t.get('cerere_proprietar'))==norm(reg[target].get('cerere_proprietar'))) if t.get('cerere_proprietar') and reg[target].get('cerere_proprietar') else None
  transfer={'destination':target,'target_state':reg[target]['stare_generala'],'target_canonical':cn,'accepted_mapping':row,'literal_request_unchanged':same,'dest_request_text':clean(reg[target].get('cerere_proprietar')),'dest_description':clean(reg[target].get('descriere')),'end_of_chain':v['aggregate_chain'][-1],'split_into':v.get('split_into',[])}
  if row:
   ev.append(evidence(p99,'/corespondenta/'+k,json.dumps(row,ensure_ascii=False),'HISTORICAL_REFERENCE','Cheie/valoare exactă din propunerea aprobabilă.'));ev.append(evidence(p99a,8,lines(P[p99a])[7],'HISTORICAL_REFERENCE','Aprobarea în bloc a propunerii; confirmă decizie, nu montarea.'));appr=(row==cn)
   facts.append(('Destinația tehnică este concordantă cu codul aprobat în 99 + 99a:8.' if appr else 'Ținta directă și codul din propunere nu coincid literal; verifică istoricul intermediar înainte de concluzie.'))
  else:facts.append('Relația către '+target+' există în registru; nu există cheie în această propunere 99. Controlul deciziei folosește celelalte dovezi istorice, nu aprobarea în bloc.')
  if same:facts.append('Cererea de origine și cea a țintei coincid după normalizarea exclusivă a spațierii/case; nu dovedește execuția.')
  elif same is False:push('TRACE_TRANSFER_TEXT_DIFFERENT',k);facts.append('Textele cererilor sursă/țintă diferă. Nu se deduce pierdere semantică numai din diferență; atribuie subpunctele separat.')
  if reg[target]['stare_generala'] not in {'închis','montat','agregat','anulat'}:push('TRACE_TRANSFER_TO_OPEN',k);facts.append('Destinația este '+reg[target]['stare_generala']+' la cutoff; un transfer de evidență nu închide implementarea la destinație.')
 if state=='anulat' or k=='T229':
  for pp in [pold,p32]:
   ll=lines(P[pp]);pat=r'(?<![\w.])'+re.escape(k)+r'(?!\w|\.\d)'
   for no,l in enumerate(ll,1):
    if re.search(pat,l):ev.append(evidence(pp,no,l,'HISTORICAL_REFERENCE','Rândul deciziei menționează chiar identitatea; verifică conținutul și cronologia, nu numai eticheta.'))
  facts.append('Anularea privește dispoziția și motivul/autoritatea, nu reușita implementării. '+clean(t.get('motiv') or (t.get('explicatii') or {}).get('ce'))[:350])
  if k=='T229':find.append('A12-F01_REACTIVARE');facts.append('Anularea istorică din tabelul proprietarului se regăsește la rândul T229; în registru starea a revenit la plan și este pe lista rămase din nou. Lista finalizate nu reflectă starea activă a aceleiași identități.')
 if v.get('split_into'):facts.append('Sunt '+str(len(v['split_into']))+' destinații de împărțire în maparea oficială; trebuie verificate toate cerințele împărțite, nu doar prima destinație.')
 # Read actual card(s): sources of detailed objectives, not merely registry copy.
 ck=nk or cn or mapping.get(k);card_key=ck if ck in cards else '.'.join(str(ck or '').split('.')[:3])
 if card_key in cards:
  path,card=cards[card_key]; exact=(ck==card_key);ev.append(evidence(path,'/cod',card['cod'],'HISTORICAL_REFERENCE','Cartela exactă.' if exact else 'Cartela părintelui; nu atribuie automat obiectivele copilului.'))
  if exact:
   for j,obj in enumerate(card.get('obiective',[])):
    if isinstance(obj,dict):
     for q in atom(obj.get('obiectiv','')):req.append({'source':path+'#/obiective/'+str(j),'text':q,'basis':'obiectiv din cartela exactă a '+('destinației' if not nk else 'taskului')})
     for z,ac in enumerate(obj.get('activitati',[])):
      if isinstance(ac,dict) and ac.get('descriere'):req.append({'source':path+f'#/obiective/{j}/activitati/{z}','text':clean(ac['descriere']),'basis':'activitate contractuală','result':ac.get('rezultat')})
  elif ck in card.get('sub_taskuri',[]):facts.append('Identitatea copilului figurează explicit în lista sub_taskuri a cartelei părinte.')
 # Inspect origin for retroactive tasks against frozen T125 inventory blob, not just live label.
 occ=[]
 for ent in ul(t.get('id_vechi')):
  oldid=ent.get('id') if isinstance(ent,dict) else ent
  if str(oldid) in old:
   ix0=old[str(oldid)];before=ix0.get('pe_pagini') or []; rec={'alias':oldid,'original_classification':ix0.get('clasificare'),'origin_status':ix0.get('stare_propusa'),'source_pointer':p125+'#/coduri[code='+str(oldid)+']','blob':P[p125],'proof':ix0.get('stare_dovada'),'first_sources':(ix0.get('refs') or [])[:6],'papers':ix0.get('documente_si_produse'),'source_page_matches':[{'title':clean(c.get('titlu')),'state':c.get('stare'),'list':c.get('lista')} for c in before if str(c.get('id_vechi') or '')==str(oldid) or len(before)==1]}
   occ.append(rec)
   if isinstance(ent,dict):facts.append('Alias structurat '+str(oldid)+' are clasificarea originală '+str(ix0.get('clasificare'))+' și stare '+str(ix0.get('stare_propusa'))+'; dovada inițială este '+str(ix0.get('stare_dovada'))+'.')
 if any(x.get('original_classification')=='GOL-SUB-TASK' for x in occ):push('TRACE_RETROACTIVE_ORIGIN',k)
 docs=[history_doc(dd) for dd in gr['documents']]
 for doc in docs:
  for z in doc.get('commits',{}).values():z['caution']='Ancestry negativă nu dovedește absența conținutului. Comparația se face la blobul țintă; un commit de integrare poate conține fișierele mai multor taskuri.'
 missing=[ck for d in docs for ck in d['checks'] if not (ck.get('result') or {}).get('oid')]
 if gr['declared_file'] and not (gr['declared_file_git'] or {}).get('oid'):missing.append({'kind':'declared_file','spec':gr['declared_file']})
 if missing:find.append('A12-F02_REF_GIT');push('REFERINTE_NEREZOLVATE',k)
 if v['missing_source_closure_time']:push('LIPSA_DATA_INCHIDERE',k)
 if not gr['declared_file_git'] and not docs and not t.get('linkuri'):push('FARA_ARTEFACT_DIRECT_IN_REGISTRU',k)
 if not nk:push('FARA_CANONIC_NU_E_DEFECT',k)
 if (t.get('cerere_proprietar') or '').startswith('(nescris'):push('CERERE_RECONSTITUITA',k)
 if len([f for f in hist if f['interpretation']!='context document referit; NU probă de acceptare pentru task'])==0 and not ev and not occ and not docs:push('FARA_PROBA_SPECIFICA_IN_CORPUS',k)
 cc=codechecks(docs,k)
 for z in cc:z['scope']='Lista de clase și tabele corelează sursa și metadatele. Nu dovedește efectul în sesiune; un commit de integrare poate include alte taskuri.'
 if cc:facts.append(f'{len(cc)} clase asociate fișierelor Java din commituri declarate au fost confruntate cu dicționarul live CESIRO și comparatorul JAR. Fără certificare comportamentală.')
 if docs:facts.append(f'Citite {len(docs)} declarații de livrabil; tipurile Git și conținutul textual disponibil sunt reunite cu comparația bloburilor. Afirmațiile autorilor rămân istorice.')
 status_doc='TRANSFER_DOCUMENTAT' if appr else 'EXISTĂ_DOVEZI_DE_DISPOZIȚIE' if ev or hist or occ else 'FĂRĂ_DECIZIE_INDEPENDENTĂ_SUFFICIENTĂ'
 if k=='T229':status_doc='ANULARE_ISTORICĂ_REACTIVARE_CURENTĂ'
 if k=='T227':
  facts+=['Cele două clase (VerificareImportSaga, WSagaVerificareImportForm) figurează în JAR-ul SHA țintă, nu în cel instalat CESIRO; AD_Form CESIRO nu are classname VerificareImport. Închiderea documentează integrarea, nu o montare în CESIRO.','Interogări native ale sursei Java executate în READ ONLY pe CTE sintetice: filtrul de client și analitic gol, documente completate nepostate cu prag temporal, costuri multiple fără multiplicare stoc; 3/3 au returnat valorile așteptate. Testul izolat al bilanțului harness-ului trece după folosirea UTF-8. Niciun test UI Compar în cabinet.']
  find.append('A12-F03_T227_INSTALARE');status_doc='COD/PACHET_GIT_SUSȚINUT; NEMONTAT_CESIRO_LA_PROBA_ACTUALĂ'
 ret={'schema':'eva.audit.task.first-pass.v1','audit_plan_digest':gate['artifact_hash'],'case_id':'A12/'+k,'source_id':k,'canonical':nk,'title':v['display_title'],'chapter':v['chapter'],'owner':owner,'required_zone_handoffs':v['secondary_zone_ids'],'reviewer':'A11','phase':'PRIMA_TRECERE_DOVEZI; reevaluare necesară','source_registry':v['source_registry'],'source_lists':v['source_lists'],'original_state':state,'original_dates':v['source_closure_times'],'source_cutoff':plan['scope']['snapshot_cutoff'],'current_sha':SHA,'source_identity_notes':{'aliases':v['legacy_aliases'],'alias_to_frozen_inventory':occ,'declared_file':gr['declared_file'],'file_git_object':gr['declared_file_git']},'atomic_requirements':req,'requirement_limit':'Extragere de cerere/descriere și obiective disponibile în cartela exactă; anexele/criteriile din versiuni ulterioare necesită reconciliere semantică. Nu se certifică automat exhaustivitatea subpunctelor prin despărțirea textului.','transfer':transfer,'historical_evidence':hist+ev,'artifacts_git_semantic_read':docs,'static_code_and_live_dictionary':cc,'individual_reasoning':facts,'disposition_evidence':status_doc,'findings':find,'planned_cross_controls':TR[k]['explicit_controls'],'global_evidence':['A12_referinte_git.json','A12_DB_metadate_CESIRO.json','Diferente_bundle_CESIRO.json']+(['A12_T227_SQL_sintetic.json','A12_test_local_T227.json'] if k=='T227' else []),'closure_snapshot':{'historical_state':state,'declared_receipts':v['declared_documents'],'closure_installed_version':None,'limit':'Nicio mapare implicită a buildului de azi la închidere. Declarații de montare și note vechi nu sunt dovezi de rulare independentă.'},'verdict_at_closure':'NEDETERMINAT pentru funcție; vezi dovezile distincte de dispoziție','verdict_current':'PARȚIAL_STATIC; NEMONTAT_CESIRO pentru forma T227' if k=='T227' else 'NEDETERMINAT_FUNCȚIONAL; verificări documentare și de cod limitate','assurance_level':'PARTIAL_CU_LIMITARI','independent_audit_score':None,'independent_review':'DE_PREDAT_A11'}
 flags={1:('PASS_DOVEDIT','Rând verificat în registrul live + hash + apartenență la lot.'),2:('PASS_DOVEDIT','ID păstrat separat de canonic/alias; fără renumerotare implicită.'),3:('INCONCLUDENT',f'{len(req)} unități de cerință documentate; nu sunt toate probate end-to-end.'),4:('INCONCLUDENT','Cronologia și dovezile atribuite sunt în fișă. Nu s-a identificat dovadă completă a comportamentului instalat la închiderea fiecărei cerințe.'),5:('INCONCLUDENT','SHA țintă confirmat; proveniența buildului istoric pe cabinet neconfirmată.'),6:('INCONCLUDENT',f'{len(cc)} clase comparate explicit; rezultatele implementării rămân dependente de probele pe cerință.'),12:('INCONCLUDENT' if cc or k=='T227' else 'NEEXECUTAT','Catalog CESIRO citit. Legăturile specifice reale găsite sunt în static_code_and_live_dictionary; lipsa unei clase AD nu dovedește lipsa funcției când nu e formă/proces distinct.'),28:('INCONCLUDENT','Comparația de pachete și commituri nu validează build sau instalare istorică la nivel de task.'),30:('INCONCLUDENT','Bloburi și capturi cu versiuni verificabile; acoperirea de execuție rămâne limitată.'),32:('INCONCLUDENT','Numitorul taskurilor este stabilit; criteriile fără probă funcțională rămân incluse.'),33:('INCONCLUDENT','Autoverificare structurală a primei treceri; independent și E2E încă neînchise.'),34:('NEEXECUTAT','A11 nu a acceptat această fișă la data producerii ei.'),35:('NEEXECUTAT','Delta finală de la închiderea misiunii rămâne de controlat.'),36:('PASS_DOVEDIT','Separarea stărilor, verdictului și a scorului de calitate explicită.')}
 if k=='T227':flags.update({8:('BLOCAT_ACCES','Forma absentă în AD/JAR CESIRO. Ecranul nu a fost deschis pentru probă.'),14:('INCONCLUDENT','Izolarea clientului dovedită pe query-urile cu CTE sintetice; accesul UI/rolul nu a fost probat.'),20:('INCONCLUDENT','3 interogări trecute pe CTE pentru client, stoc și documente. Nu constituie audit de sold E2E.'),28:('INCONCLUDENT','Două clase există în JAR Git și lipsesc din JAR CESIRO; aria de release a închiderii trebuie interpretată separat.')})
 ret['control_results']=[{'id':c['id'],'status':flags.get(n,('NEEXECUTAT',''))[0],'result_or_next_probe':flags.get(n,(None,c['action']+' Dovezi specifice datorate: '+c['required_evidence']))[1]} for n,c in enumerate(plan['per_task_checklist'],1)]
 return ret
def run():
 finished=[];allrefs={};findings=collections.defaultdict(list);counts=collections.Counter();agg=collections.Counter()
 for v in IX:
  k=v['source_id'];w=actual_report(v);w['disposition_evidence']=w['disposition_evidence'].replace('EXISTĂ_DOVEZI_DE_DISPOZIȚIE','ORIGINE_DOCUMENTARĂ; NU CERTIFICĂ DISPOZIȚIA').replace('SUFFICIENTĂ','SUFICIENTĂ')
  for atom_ in w['atomic_requirements']:atom_['basis']=atom_['basis'].replace('Reconstituée','Reconstituită')
  for ev in w['historical_evidence']:allrefs[ev['git_blob']]=ev['path']
  for f in w['findings']:findings[f].append(k)
  for attr in ['historical_evidence','artifacts_git_semantic_read','static_code_and_live_dictionary','atomic_requirements']:
   counts['tasks_with_'+attr]+=int(bool(w[attr]));counts['total_'+attr]+=len(w[attr])
  if w['transfer']:agg['aggregate']+=1;agg['approved_exact_99_mapping']+=int(w['disposition_evidence']=='TRANSFER_DOCUMENTAT');agg['literal_request_equal']+=int(w['transfer']['literal_request_unchanged'] is True)
  p=O/('Fisa_'+k+'.json');dump(p,w);finished.append({'id':k,'canonical':v['canonical'],'file':'taskuri/'+p.name,'sha256':hs(p),'findings':w['findings'],'verdict':w['verdict_current'],'status':w['assurance_level'],'atomic_requirement_fragments':len(w['atomic_requirements']),'direct_historical_evidence_rows':len(w['historical_evidence'])})
  if len(finished)%50==0 or len(finished)==651:dump(E/'A12_progres.json',{'phase':'PRIMA_TRECERE','produced':len(finished),'required':651,'tested_E2E':0,'reviewed_by_A11':0,'updated_utc':now()});print('CASE',len(finished),flush=True)
 assert len(finished)==len(IX)==651 and len({f['id'] for f in finished})==651
 pv={'id':'EV-A12-HIST-01','method':'Arbore Git complet la SHA; citire cat-file pe fiecare blob/commit selectat și recalculare SHA1 Git. Fișiere/ancore și extrase individuale în fișele nominale, cu limite.','scope':'Corpus de referințe nu implică audit integral al codului sau al runtime.','code':SHA,'git_file_paths_retrieved':len(P),'git_objects_retrieved':len(list((D/'blobs').glob('*.gz'))),'commit_objects_checked':len(CMP),'distinct_blobs_in_case_evidence':len(allrefs),'commit_diff_paths_total':sum(len(v['changed']) for v in CMP.values()),'referenced_commits_ancestors_of_target':sum(1 for x in CMP.values() if x['ancestor']),'command':'git ls-tree -r -z SHA; git cat-file --batch; git diff-tree --root --no-commit-id --no-renames -r --raw -z oid; git merge-base --is-ancestor reference SHA.','countercheck_T227':'git merge-base 6df998ae 033dc1c064d → d136200ded066ad9c6d5f797822b6dfe1f4de011. Codul și clasele T227 există în SHA țintă, deși commitul 033dc1c064d nu este strămoș.'}
 dump(E/'A12_provenienta_dovezi.json',pv)
 f={'phase':'Constatări și limite ale primei treceri; nu toate sunt defecte de implementare.','findings':[{'id':'A12-F01_REACTIVARE','category':'inconsistență registru','severity':'P2','confidence':'RIDICATĂ','tasks':findings['A12-F01_REACTIVARE'],'proof':'T229 are status plan și motiv reactivare 31.10; listele finalizate/rămase îl prezintă în stări diferite. Decizia istorică îl menționează nominal.','counter_evidence':'Anularea istorică a existat. Problema privește interpretarea listei drept închis acum.','action':'Distinge apartenența istorică de starea curentă și arată reactivarea.'},{'id':'A12-F02_REF_GIT','category':'referințe declarate nerezolvate la revizie','severity':'P2','confidence':'RIDICATĂ pentru proba Git; cauza de investigat','tasks':findings['A12-F02_REF_GIT'],'proof':'spec/kind/result în fișele individuale și A12_referinte_git.json.','counter_evidence':'Mutare, redenumire sau alt depozit posibile; nu dovedește lipsă funcțională.','action':'Stabilește referința corectă, versiunea și reia proba de conținut.'},{'id':'A12-F03_T227_INSTALARE','category':'diferență de livrare dovedită, nu defect de cod demonstrat','severity':'P2 pentru decizia de exploatare','confidence':'RIDICATĂ pentru CESIRO','tasks':['T227'],'proof':'Două clase sunt în JAR Git și lipsesc din JAR montat. Zero formă AD pentru classname VerificareImport din 189. 3 probe SQL pe fixture au trecut; UI nu este probată.','counter_evidence':'Taskul închis declară montare ulterioară; diferența nu contrazice automat integrarea de cod.','action':'După montarea autorizată, verifică meniul/drepturile și efectuează probă Compar în cabinet izolat.'}],'coverage_limits':[{'id':name,'count':len(set(lst)),'case_ids':sorted(set(lst))} for name,lst in scope_status.items()],'caution':'Absența unui cod canonic, a unei date, texte diferite sau originea retroactivă nu sunt fiecare un defect funcțional.'}
 dump(E/'A12_constatari_prima_trecere.json',f)
 report={'schema':'eva.audit.A12.first_pass.v1','phase':'PRIMA_TRECERE_PARTIALĂ_PREDATĂ_A11','generated_utc':now(),'gate_digest':gate['artifact_hash'],'commit':SHA,'cutoff':plan['scope']['snapshot_cutoff'],'summary':'651/651 fișe au primit verificarea de proveniență, dispoziție și dovezi nominale disponibile. Acoperirea integrală a fișelor NU înseamnă acoperire integrală a implementării. Controalele neexecutate se mențin distinct; autorul nu acordă nota finală.','counts':{'registered':693,'individual_required':651,'individual_first_pass':len(finished),'individual_reports_accepted_by_A11':0,'full_implementation_certified':0,'E2E_executed_by_A12':0,'local_harness_cases_T227':1,'sql_fixture_queries_T227':3,'zone_reports_integrated':0,'absent_closure_time_in_sources':244,'without_canonical_in_cohort':417}|dict(counts),'aggregate_checks':dict(agg),'evidence_provenance':pv,'live_dictionary':{'file':'A12_DB_metadate_CESIRO.json','sha256':hs(E/'A12_DB_metadate_CESIRO.json'),'counts':db['counts'],'scope':db['limit']},'other_evidence':[{'file':p,'sha256':hs(E/p)} for p in ['A12_constatari_prima_trecere.json','A12_T227_SQL_sintetic.json','A12_test_local_T227.json','A12_provenienta_dovezi.json','A12_referinte_git.json','Diferente_bundle_CESIRO.json']],'remaining_work':['A01–A10: încorporează efectiv rezultatele controalelor și pipeline-urilor din Index_trasabilitate per cerință. Nu certifica un task printr-un raport comun de capitol.','A12: reia nominal probele lipsă în mediu de test izolat; confirmă caracterul pur documentar și N/A individual numai după acord A11.','A11: verificare independentă a fiecărei fișe, a predărilor și contra-dovezilor, apoi reexecutare unde dovezile sunt insuficiente.','Root: delta registru/Git/deploy la închidere și reexecutare fișe afectate.'],'zone_handoffs':{u:{'task_ids':[v['source_id'] for v in IX if u==v['chapter_owner'] or u in v['secondary_zone_ids']],'status':'AȘTEAPTĂ_DOVEZI_EXECUTOR_REVERIFICATE'} for u in [f'A{n:02d}' for n in range(1,11)]},'records':finished,'report_score':None,'implementation_score':None,'report_status':'PARTIAL_CU_LIMITARI'}
 dump(E/'A12_raport.json',report);print('DONE',report['counts'],report['aggregate_checks'],{k:len(v) for k,v in findings.items()},flush=True)
if __name__=='__main__':run()


