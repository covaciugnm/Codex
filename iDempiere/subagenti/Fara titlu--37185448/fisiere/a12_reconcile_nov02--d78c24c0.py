from pathlib import Path
import json, hashlib, collections, re, datetime, shutil
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01')
def read(p):return json.loads((B/p).read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(f,d):(B/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ul(x):return x if isinstance(x,list) else ([] if x is None or x=='' else [x])
def uniq(a):return list(dict.fromkeys(a))
man=read('capturi/MANIFEST.json')
hashes={}
for d in man['files']:
 p='capturi/'+d['file'];assert h(p)==d['live'] and (B/p).stat().st_size==d['bytes'];hashes[d['file']]=h(p)
T=read('capturi/00_STATUS_TASKURI.json'); reg={t['id']:t for t in T}; assert len(reg)==len(T)
P={k:v for k,v in reg.items() if v['proiect']=='P01'}
ST=read('capturi/00_STARI_TASKURI.json'); final={x['cod'] for x in ST['stari'] if x['grupa']=='Finalizat'};assert not set(x['stare_generala'] for x in P.values())-{x['cod'] for x in ST['stari']}
co=read('capturi/00_CORESPONDENTA_COD_CAPITOL.json');bycode=collections.defaultdict(list);xrefs=collections.defaultdict(list)
for j,x in enumerate(co['coduri']):bycode[x['cod']].append(x['id_tehnic']);xrefs[x['id_tehnic']].append(j)
alias=collections.defaultdict(list)
for x in T:
 for a in ul(x.get('id_vechi')):alias[str(a)].append(x['id'])
def resolve(ref):
 r=ref.strip()
 if r in reg:return [r],'ID tehnic exact'
 if r in bycode:return bycode[r],'cod capitol exact din corespondență'
 if r in alias:return alias[r],'alias exact al registrului'
 m=re.fullmatch(r'(P\d+)\.(T.+)',r)
 if m:
  z,k=resolve(m[2]);return [t for t in z if reg[t]['proiect']==m[1]],k+' filtrat proiect'
 return [],'fără corespondență'
def list_trace(src,key):
 orig=read('capturi/'+src);out=[]
 def go(lst,par=None,inherited=[]):
  for j,x in enumerate(lst):
   path=(par+'/copii' if par else '/'+key)+'/'+str(j)
   rr=(x.get('task') or '').strip(); scanned=[]
   # exact înaintea împărțirii; slash unește ID-uri distincte. Nicio inferență din titlu sau simplu prefix.
   tokens=[t.strip() for t in rr.split('/') if t.strip()]
   for u in tokens:
    z,k=resolve(u);scanned.extend(z)
   if not scanned and not rr:scanned=list(inherited)
   own=uniq(scanned)
   out.append({'pointer':path,'record':x,'own':own,'raw':rr});go(x.get('copii',[]),path,own)
 go(orig[key]);return out
FIN='00_STATUS_FINALIZATE.json';REM='00_STATUS_RAMASE.json'
lf=list_trace(FIN,'finalizate');lr=list_trace(REM,'ramase')
S={k for k,v in P.items() if v['stare_generala'] in final}
E={k for y in lf for k in y['own'] if k in P}
CO=S|E;inv=read('Inventar_P01.json');ip={x['technical']:x for x in inv['rows']}; assert set(ip)==set(P)
unexpected=sorted(CO^{t for t,x in ip.items() if x['in_individual_review']});assert not unexpected,unexpected
M=read('Matrice_interfete.json');D=read('Plan_director.json'); chapters={x['code']:x for x in M['chapters']};rub=read('A11_rubrica_control.json');dt=read('Inventar_tehnic.json');A11=read('A11_observatii_preliminare.json')
links=collections.defaultdict(list)
for src,ls in [(FIN,lf),(REM,lr)]:
 for y in ls:
  for k in y['own']:
   if k in P:links[k].append({'file':src,'pointer':y['pointer'],'id':y['record']['id'],'task_field':y['raw'],'state':y['record'].get('stare'),'dates':{nm:val for nm,val in y['record'].items() if nm in ['aparut_la','inceput_la','finalizat_la','termen','ultima_actualizare','finalizat_sursa']}})
aux=[]
for u in inv['all_unmapped_list_rows_for_project_attribution']:
 name=u['row_id'];src=u['source'];ls=lf if src==FIN else lr;y=next(yy for yy in ls if yy['record']['id']==name); matches,why=resolve(name)
 if name.startswith('T40.'):
  assert len(matches)==1 and matches[0] in CO;group='SOUS_RANG_P01_EXISTANT';dest=matches;reason='ID du sous-rang ou alias exact + parent T40; pas une nouvelle unité.';reason='ID/alias exact al rândului auxiliar, titlu compatibil și părinte T40; unitatea P01 este deja inclusă.'
 elif name.startswith(('T52.','T53.')):
  par=name.split('.')[0];assert reg[par]['proiect']=='P11';group='P11_IN_AFARA_P01';dest=matches or [par];reason='Parent source P11. Aliasul exact, când există, păstrează subtaskul; în lipsă se notează doar părintele P11, nu se inventează un ID de subtask.'
 elif name=='INTREBARI.4':
  group='COORDONARE_NETERMINATĂ';parent=next(yy for yy in ls if yy['record']['id']=='INTREBARI');dest=parent['own'];reason='Subrând «de făcut» conține predări AMD și confirmări la sesiunile existente; fără ID tehnic propriu. Se ține ca obligație de coordonare, nu ca task finalizat.'
 else:
  assert name=='A';group='ANTET_ISTORIC';kids=y['record']['copii'];assert len(kids)==46
  dest=uniq(k for n in kids for k in resolve(n['task'])[0]); assert len(dest)==46;reason='Antet Seria A, fără câmp task; toate cele 46 de referințe ale copiilor rezolvate separat (ID sau alias).'
 aux.append({'row':name,'source':src,'pointer':y['pointer'],'group':group,'source_ref':u['own_reference'],'source_state':u['state'],'canonical_or_parent_ids':dest,'basis':reason,'additional_completed_P01_units':0})
 if group=='SOUS_RANG_P01_EXISTANT':
  k=dest[0];links[k].append({'file':src,'pointer':y['pointer'],'id':name,'task_field':y['raw'],'state':u['state'],'dates':{nm:val for nm,val in y['record'].items() if nm in ['aparut_la','inceput_la','finalizat_la','termen','ultima_actualizare','finalizat_sursa']},'indirect_binding':'tehnic/alias confirmat prin row_id + parent + titlu; nu prin textul liber «task nou»'})
for y in aux:
 if y['group']=='SOUS_RANG_P01_EXISTANT':y['group']='SUBRAND_P01_EXISTENT'
def ref(f,p):return 'capturi/'+f+'#'+p
op=[]
for j,v in enumerate(T):
 k=v['id']
 if k not in P:continue
 comb=ip[k]; c=v.get('capitol') or co['capitol_randuri_vechi'].get(k);assert c==comb['chapter']; owner=chapters[c]['owner']
 codes=uniq([x for x in [v.get('cod_capitol')]+[co['coduri'][ii]['cod'] for ii in xrefs[k]] if x]);assert not codes or len(codes)==1
 pa=v.get('parinte');merge=v.get('agregat_in');split=co['inchise_prin_impartire'].get(k,[])
 original=v.get('cerere_proprietar') or ''; desc=v.get('descriere') or ''; state=v['stare_generala']; eligible=k in CO
 trajectory=[]; seen=set(); dest=k
 while dest in reg and dest not in seen and reg[dest].get('agregat_in'):
  seen.add(dest);nxt=reg[dest]['agregat_in'];trajectory.append({'from':dest,'to':nxt,'target_state':reg.get(nxt,{}).get('stare_generala')});dest=nxt
 reason='AUTOR_DECLARAT' if original.strip() and not ('reconstituit' in original.lower() or 'nescris' in original.lower()) else ('RECONSTITUIT_DECLARAT' if original.strip() else 'ABSENT')
 obligations=[{'id':k+'-SRC-1','kind':'cerere_proprietar','text':original or None,'pointer':ref('00_STATUS_TASKURI.json',f'/{j}/cerere_proprietar'),'source_quality':reason,'instruction':'Atomizează după gate și verifică fiecare subpunct, inclusiv anexele. Cererea reconstituită nu dobândește statut de citat avizat.'},{'id':k+'-SRC-2','kind':'descriere','text':desc or None,'pointer':ref('00_STATUS_TASKURI.json',f'/{j}/descriere'),'source_quality':'DESCRIERE_REGISTRU','instruction':'Compară cu cererea, decizia și materialele; tratează diferențele explicit. Nu este dovadă de execuție.'}]
 if state=='agregat':
  specific='La fiecare cerință inițială, urmărește lanțul de preluare și împarte dacă este cazul. Probează dispoziția și rezultatul separat la destinație; nicio închidere implicită prin agregare.'
 elif state=='anulat':
  specific='Verifică decizia datată, titularul deciziei, motivul, sfera anulată, protecția împotriva activării parțiale și eventuala reactivare. Nu atribui conformitate de software unei anulări.'
 elif k in E-S:
  specific='Conflict între lista finalizatelor și stare curentă: verifică evenimentele, amendamentul/ordinul, ce s-a anulat istoric și ce s-a redeschis. Nu trata taskul curent ca final.'
 elif state=='montat':
  specific='Confirmă release, cabinet, hash pachet, drepturi și efect conform criteriilor, închiderea de atunci separat de starea actuală. Statusul montat este declarație istorică.'
 elif state=='închis':
  specific='Separă motivul închiderii (cod/document/integrare) de montare. Cere probă specifică de acceptare și instalare dacă s-a pretins funcție exploatabilă.'
 else:specific='În afara lotului individual de finalizate la cutoff; păstrează în inventar și urmărește eventualele predări de la taskuri agregate/referențiate.'
 obligations.append({'id':k+'-DISP','kind':'control_dispoziție','text':specific,'pointer':ref('00_STATUS_TASKURI.json',f'/{j}/stare_generala'),'source_quality':'CONTROL_DE_AUDIT_PROPUS','instruction':'NEEXECUTAT'})
 allrefs=[{'file':'00_STATUS_TASKURI.json','pointer':'/'+str(j),'sha256':hashes['00_STATUS_TASKURI.json']}]
 allrefs += [{'file':'00_CORESPONDENTA_COD_CAPITOL.json','pointer':'/coduri/'+str(ii),'sha256':hashes['00_CORESPONDENTA_COD_CAPITOL.json']} for ii in xrefs[k]]
 f=v.get('finalizat_la'); when=[{'kind':'finalizat_la registru','value':f,'origin':ref('00_STATUS_TASKURI.json',f'/{j}/finalizat_la')}] if f else []
 when += [{'kind':'finalizat_la listă auxiliară','value':s['dates']['finalizat_la'],'origin':ref(s['file'],s['pointer']+'/finalizat_la')} for s in links[k] if s['dates'].get('finalizat_la')]
 op.append({'source_id':k,'source_project':'P01','source_title':v['denumire'],'display_title':v['nume_sugestiv'],'canonical':codes[0] if codes else None,'identity_status':'CANONIC_CONFIRMAT' if codes else 'FĂRĂ_COD_CANONIC; păstrează ID tehnic','legacy_aliases':ul(v.get('id_vechi')),'aliases_in_canonical_map':uniq(a for ii in xrefs[k] for a in ul(co['coduri'][ii].get('id_vechi'))),'chapter':c,'source_state':state,'state_group':next(x['grupa'] for x in ST['stari'] if x['cod']==state),'individual_review':eligible,'selection_reason':'STARE_FINALĂ' if k in S else ('LISTĂ_FINALIZATE_ÎN_CONFLICT' if k in E else 'NEFINALIZAT_LA_CUTOFF'),'source_series':v.get('serie'),'last_updated_source':v.get('ultima_actualizare'),'source_closure_times':when,'missing_source_closure_time':not when,'deadline':v.get('termen'),'declared_progress':v.get('procent'),'declared_reason':v.get('motiv'),'declared_decision_source':v.get('sursa_deciziei'),'parent':pa,'aggregate_target':merge,'aggregate_chain':trajectory,'aggregation_cycle':dest in seen,'absent_terminal_target':bool(trajectory) and dest not in reg,'split_into':split,'chapter_owner':owner,'secondary_zone_ids':chapters[c]['handoff'],'auditor':'A12','reviewer':'A11','candidate_interfaces':[x['id'] for x in M['contracts'] if owner in (x['from'],x['to'])],'interfaces_limit':'Filtre de tri par titular; legătura efectivă task→pas se verifică din cerință și sursă, nu se presupune.','obligations':obligations,'source_registry':allrefs,'source_lists':links[k],'declared_documents':v.get('documente_produse',[]),'declared_file':v.get('fisier'),'declared_links_pointer':ref('00_STATUS_TASKURI.json',f'/{j}/linkuri') if v.get('linkuri') else None,'claims_notes_pointer':ref('00_STATUS_TASKURI.json',f'/{j}/observatii') if v.get('observatii') else None,'source_explanations_pointer':ref('00_STATUS_TASKURI.json',f'/{j}/explicatii') if v.get('explicatii') else None,'pending_reviews':['A12-CK-01..36', 'SF-01..09 pentru fiecare cerință aplicabilă'] if eligible else [],'implementation_status':'NEEXECUTAT','audit_quality':None})
index={'schema':'eva.audit.P01.task.planning-index.v2','generated_utc':now(),'cutoff':man['ended_utc'],'mode':'PLANIFICARE; un rând pentru fiecare înregistrare P01. Niciun audit de implementare executat.','snapshots':hashes,'cohort_definition':'stări cu grupa Finalizat în dicționar ∪ referințe P01 din lista finalizatelor. Stările anulată și agregată primesc control de dispoziție, nu PASS implementare.','counts':{'all_projects':len(T),'P01':len(P),'official_final':len(S),'explicit_list_P01_unique':len(E),'intersection':len(E&S),'official_only':len(S-E),'list_only':sorted(E-S),'individual':len(CO),'outside_cohort':len(P)-len(CO),'without_canonical_in_cohort':sum(x['individual_review'] and not x['canonical'] for x in op),'without_canonical_P01':sum(not x['canonical'] for x in op),'state_histogram':dict(collections.Counter(x['source_state'] for x in op))},'rows':op}
write('A12_index_taskuri.json',index)
rec={'schema':'eva.audit.P01.population.reconciliation.v2','cutoff':man['ended_utc'],'method':'Recitire independentă a celor șapte fișiere live. Verificare SHA/bytes, unicitate ID, domeniu proiect=status brut, stări după grupa Finalizat, vizitare recursivă a celor două registre, rezoluții exacte ID/cod/alias și moștenire exclusiv pentru task gol. Comparare set de identități rezultat cu Inventar_P01, nu doar total. Nodurile auxiliare fără cheie se judecă separat după părinte, titlu și aliasul rândului.','manifest_hash':h('capturi/MANIFEST.json'),'live_hashes':hashes,'files_succeeded':len(hashes),'all_task_ids_unique':len(reg)==len(T),'canonical_collision_inside_P01':len([1 for k in bycode if k.startswith('P01.') and len(set(bycode[k]))>1]),'counts':index['counts'],'official_states':sorted(final),'source_aux_rows':{'final_roots':len(read('capturi/'+FIN)['finalizate']),'final_nodes_recursive':len(lf),'remaining_roots':len(read('capturi/'+REM)['ramase']),'remaining_nodes_recursive':len(lr)},'explicit_final_criteria':'Apartenență la lista finalizate, nu o deducție textuală din procentul 100%, titlu sau montarea pur declarată. Etichetele contradictorii rămân păstrate.','auxiliary_reconciliation':aux,'aux_categories':dict(collections.Counter(x['group'] for x in aux)),'aux_additional_completed':sum(x['additional_completed_P01_units'] for x in aux),'symmetric_difference_vs_parent_individual_ids':unexpected,'T229_explanation':'Registru P01.C11.T0007=plan, 1% și reactivat prin ordin 31.10; pe finalizate anulare istorică, pe rămase în lucru. Fișă individuală pentru contradicție. Nici finalizat operațional, nici dovadă a unei implementări funcționale.','independent_consistency_checks':{'project_filter':'proiect == P01; nu titlu sau capitol presupus','chapters_declared':len(chapters),'chapters_with_P01_tasks':len({x['chapter'] for x in op}),'rows_agree_with_task_ids':set(ip)==set(P),'cohort_size_agrees':len(CO)==inv['summary']['individual_review_population'],'task_chapter_and_canonical_sources_checked_for_all':True,'aux_nodes_have_zero_increment':True,'count_missing_closure_time_in_cohort':sum(x['individual_review'] and x['missing_source_closure_time'] for x in op),'aggregate_edge_missing_terminal':sum(x['absent_terminal_target'] for x in op),'aggregate_cycle':sum(x['aggregation_cycle'] for x in op)},'limitations':['Fișierele montate în serviciu sunt surse de stare declarată la cutoff; nu sunt teste de implementare/deploy.','Mai multe date sunt surse istorice reconstituite sau aproximări; ora de editare nu înlocuiește ora de închidere.','Absența unui cod canonic nu exclude un rând. Captura live diferă de copia Git pentru patru fișiere; aceste diferențe sunt păstrate.'],'next':'După 10/10 plan: câte o fișă pentru fiecare dintre cele 651 identități; restul 42 urmărite ca dependențe/delta, apoi recitirea inventarului la închidere.'}
write('A12_reconciliere_P01.json',rec)
print('COUNTS',index['counts'],rec['aux_categories'],rec['independent_consistency_checks'])

