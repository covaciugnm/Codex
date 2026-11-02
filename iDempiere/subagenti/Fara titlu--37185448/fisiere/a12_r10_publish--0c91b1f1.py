from a12_r10_base import *
from a12_r9_publish import S,H,e,criteria,enc,read,ptr,node_file,ThreadPoolExecutor
from copy import deepcopy
from urllib.parse import quote
import collections,hashlib,datetime,inspect,os
R10=E/'R10';pplan=P10/'Plan_R10_164_et_dix_zones.json';histfile=P10/'Cai_nominale_873_fara_dublare.json'
def obs(c,kind,s,pt,expected,observed,negative,lim,scope,cls='exercised'):
 assert pt and isinstance(expected,str)and expected and observed is not None
 value=ptr(read(s),pt);assert value is not None
 row={'criterion':c,'relation':'R10_'+cls,'kind':kind,'ref':node_file(c,s,pt),'expected':expected,'observed':observed,'negative':negative,'limit':lim,'extent':scope}
 return 'EV10-'+hashlib.sha256(enc(row).encode()).hexdigest()[:24],row
def checkref(r):
 p=B/r['file'];assert H(p)==r['sha256'],(p,r['sha256']);doc=read(p)if p.suffix=='.json'else None
 if 'pointer'in r:assert ptr(doc,r['pointer'])is not None
 if 'line'in r:line=p.read_text(encoding='utf8',errors='replace').splitlines()[r['line']-1];assert hashlib.sha256(line.encode()).hexdigest()==r['line_sha256']
def collect(preview=False):
 r=collections.defaultdict(list);origin=collections.defaultdict(set);zone_report={}
 for s in [P10/'Raport_preliminar_A12.json',P10/'Registru_componenta_A12_supliment.json',P10/'Registru_pg_implicite_A12.json',P10/'Registru_SAGA_banca_A12.json',P10/'Registru_documentar_A12.json',P10/'Registru_SAGA_UI_A12.json',P10/'Zone_A02_A10/Rezultat.json',P10/'Zone_A02_A10/T254_receptie.json',P10/'Zone_A02_A10/T326_T333_receptie.json',P10/'Zone_A08/Rezultat.json',P10/'Zone_A08/T351_receptie.json',P10/'Zone_A09/Rezultat.json',P10/'Zone_A04/Rezultat.json',P10/'Zone_A01/Rezultat.json',P10/'Zone_A01/T159_receptie.json',P10/'Zone_A01/T58_receptie.json',P10/'T216_comparator_de_reutilizare.json',P10/'Controale_independente_A11.json']:
  if not s.exists():continue
  for c,items in read(s).get('receipts',{}).items():
   for i,v in enumerate(items):
    for x in v['references']:checkref(x)
    cls='independent'if v['extent']=='independent_control_only'else'context'if v['extent']=='context_only'else'exercised';r[c].append(obs(c,v['kind'],s,'/receipts/'+c+'/'+str(i),v['expected'],v['observed'],v['negative_or_control'],v['limits'],v['extent'],cls));origin[c].add('A11'if v['kind'].startswith('A11 ·')else'COORDONATOR'if v['kind'].startswith('COORDONATOR')else'A12'if 'A06 C20'not in v['kind']else'A06')
 af=E/'R10_pregatire/A07_T216/T216_raport.json';a7=rd(af);assert H(af)=='02101779827b2d1b07411de6a9d42f97c4f4fb7635ec7b20f0bfa455a2f073cd'and(len(a7['criteria']),len(a7['artifacts']))==(9,38)
 for a in a7['artifacts']:assert H(af.parent/a['file'])==a['sha256']
 for i,v in enumerate(a7['criteria']):
  c=v['id'];cc='exercised'if v['r10_scope']in ['CONTRAEXEMPLU_EXECUTAT','CONTRAEXEMPLU_LA_IMPORT_RESTUL_CONDIȚIONAT','PARȚIAL_DATE_DISTINCTE_LA_INTRARE']else'boundary'
  r[c].append(obs(c,v['r10_scope'],af,'/criteria/'+str(i),v['normative_content'],v['r10_observation'],'Originea proprie eligibilă din probă a ajuns la validarea explicită cu trei roluri.','Acceptul nu se extinde la comandă validată, factură, plata sau retur. Mărimile K2 din DECIZIE și mențiunile istorice sunt separate.',v['r10_scope'],cc));origin[c].add('A07')
 zone_report['A07']={'historical_reference_errata':S(P10/'T216_metadate_R9_corectate.json'),'signed_report':S(af),'criteria':9,'source_artifacts_checked':38}
 a05file=P10/'A05_handoff_adaptor.json'
 if a05file.exists():
  z=read(a05file);zone_report['A05']={'signed_report':z['signed_report'],'checked_files':z['count_checked'],'type':'Proprietarul A05, verificări directe'}
  for c,items in z['receipts'].items():
   for i,v in enumerate(items):
    for x in v['references']:checkref(x)
    r[c].append(obs(c,v['kind'],a05file,'/receipts/'+c+'/'+str(i),v['expected'],v['observed'],v['negative_or_control'],v['limits'],v['extent'],'exercised'if v['extent']=='subcase'else'boundary'));origin[c].add('A05')
 elif not preview:raise ValueError('Await signed A05 package')
 for zi,z in enumerate(read(pplan)['each_zone']):
  for i,v in enumerate(z['assigned']):
   c=v['id'];r[c].append(obs(c,'Propriu caz, rol, intrare, martor şi urmărirea datelor',pplan,'/each_zone/'+str(zi)+'/assigned/'+str(i),v['threshold'],{'assignment':v['execution_owner'],'fixture':v['fixture']},v['negative'],'Repartizare și protocol. Înregistrarea nu conferă rezultat de execuție.','no_product_credit','assignment'))
 for i,v in enumerate(read(histfile)['records']):
  c=v.get('criterion',v.get('id'));assert c in r9
  r[c].append(obs(c,'Traseu individual pentru recuperarea etalonului',histfile,'/records/'+str(i),'Localizează criteriul și distinge sursa de comparator.',{'method':v['route_to_next_control'],'authority':'pointer istoric/cod disponibil'},None,'Metoda propusă singură nu certifică operația.','no_product_credit','rediscovery'))
 return r,origin,zone_report
def decision(c,pr,rows):
 qual=[w for _,w in rows if w['relation']=='R10_exercised']
 if not qual:return pr
 direct={
 'T06-R2-016':'ETALON_1_1_10_60_ȘI_RESULT_1_MĂSURAT_NATIV_R10',
 'T06-R2-018':'RELUARE_ZK_168_TOATE_CU_INSTANȚA_NOUĂ_R10',
 'T06-R2-019':'FORMULAR_NATIV_DOAR_VERIFICĂ_0_SCRIERI_HASH_IDENTIC_R10',
 'T06-R2-022':'ORACOLE_ZK_ȘI_CSV_MĂSURATE_DEFECT_SUBSOL_FILTRAT_R10',
 'T201-R2-013':'ORACOL_JDBC_2X20_CONCURENȚĂ_ȘI_MUTANT_MĂSURAT_R10',
 'T201-R2-014':'ORACOL_JDBC_FĂRĂ_GOL_41_41_ȘI_MUTANT_MĂSURAT_R10',
 'T211.03-R2-003':'INVARIANTĂ_OFERTĂ_12960_CAZURI_PE_FIECARE_JAR_R10',
 'T210-R2-004':'POST_ANONIM_REFUZAT_ÎN_ROUTERUL_ASGI_EXERCITAT_R10',
 'T11-R2-019':'ZERO_ZERO_PE_CELE_DOUĂ_FIȘIERE_ÎN_INTERVALUL_EXACT_R10',
 'T06-R2-024':'MERGE_VÂRF_ISTORIC_DOCUMENTAT_VÂRF_ABSENT_PENTRU_REEXECUȚIE_R10',
 'T254-R2-004':'ETALOANE_BYTECODE_ORIGINALE_5_0_ȘI_CELE_AMENDATE_SEPARATE_R10'}
 if c in direct:return direct[c]
 if c=='T354-R2-021':return 'COMENZI_NATIVE_ARTICOLE_PRIMARE_ȘI_LIMITA_DE_REZERVARE_R10'
 if c in ['T216-R2-001','T216-R2-007']:return 'CONTRAEXEMPLU_ANTET_PROPRIU_PIERDE_LINIILE_R10'
 if c=='T216-R2-008':return 'ORIGINE_DISTINCTĂ_LA_INTRARE_ADRESE_ERP_NECORELATE_R10'
 return 'SUBCONDIȚIE_NOMINALĂ_REEXECUTATĂ_R10'
def render(doc):
 import a12_r9_publish as prev
 fn=inspect.getsource(prev.dos_html).replace('dos_html','rendered').replace('R9','R10').replace('R8','R9').replace("'R10_plan','R10_external_boundary','R10_retained_partial','R10_source_location'","'R10_assignment','R10_rediscovery'")
 ns={'e':e,'criteria':criteria};exec(fn,ns);return ns['rendered'](doc).replace('</nav>',' · <a href="../../R9/fise_html/Fisa_'+quote(doc['task'],safe='')+'.html">Fișa R9</a></nav>',1)
def table(z,n):
 import a12_r9_publish as prev
 fn=inspect.getsource(prev.indexer).replace('indexer','tabular').replace('R9','R10').replace('Runda 9','Runda 10').replace('r9_measured','r10_measured');ns={'e':e};exec(fn,ns);return ns['tabular'](z,n)
def build(preview=False):
 dest=Path('D:/CodexWork/a12-r10-preview')if preview else R10
 if not preview:assert not(dest/'MANIFEST_R10.json').exists()
 parent=rd(R9/'A12_raport.json');cat=rd(R9/'Dovezi_criterii.json');ev=cat['evidence'];inv=cat['inverse_task_requirement_links'];rr,ori,zone=collect(preview)
 (dest/'taskuri').mkdir(parents=True,exist_ok=True);(dest/'fise_html').mkdir(exist_ok=True);index=[];reg=[];states=Counter();types=Counter();q=Counter();work=[];seen={}
 fset={v['criterion']for v in f164}; locset={v['criterion']for v in nw873};hset={v['criterion']for v in his167}
 for pi in parent['records']:
  pf=R9/pi['file'];assert H(pf)==pi['sha256'];w=rd(pf);w['schema']='A12.R10';w['immutable_R9_parent']=S(pf);w['scoring_authority_R10']='A11 independent';xn=0;un=0
  for c in criteria(w):
   id=c['id'];pr=c['R9']['effective_status'];o=rr.get(id,[]);sf=decision(id,pr,o);ss=[v for _,v in o if v['relation']=='R10_exercised'];states[sf]+=1;xn+=bool(ss);un+=sf=='NEEXECUTAT'
   fol=' '.join(dict.fromkeys(v['limit']for v in ss))if ss else c['R9']['next'];links=list(c['R9']['effective_evidence_links'])
   for eid,v in o:
    assert eid not in ev;ev[eid]=v;inv[eid]=[{'criterion':id,'task':w['task'],'relation':v['relation']}];links.append({'id':eid,'relation':v['relation']});types[v['relation']]+=1
   c['R10']={'prior':pr,'effective_status':sf,'observations':o,'effective_evidence_links':links,'next':fol,'no_grade':True}
   q['measured_or_doc']+=bool(ss);q['previously_unexecuted_now_narrow_observation']+=bool(ss)and pr=='NEEXECUTAT';q['in_164_receipted']+=(id in fset and bool(ss));q['in_873_receipted']+=(id in locset and bool(ss));q['in_167_receipted']+=(id in hset and bool(ss))
   base_row={k:v for k,v in r9[id].items()if k not in ['individual_evidence_or_plan','measured_or_documentary_or_previous_supplement','next']};reg.append(base_row|{'R10':sf,'next':fol,'R10_associated_evidence_ids':[k for k,v in o],'R10_primary_responsible_contributing':sorted(ori.get(id,[])),'R10_observed_or_documentary':bool(ss),'R10_entry_cohorts':{'164':id in fset,'873':id in locset,'167':id in hset}});seen[id]=(sf,ss)
  work.append((w,pi,xn,un))
 def emit0(t):
  w,pi,xn,un=t;f=dest/pi['file'];hh=dest/pi['html'];wr(f,w);hh.write_text(render(w),encoding='utf8');return{'task':w['task'],'title':w['title'],'state':pi['state'],'canonical':w['canonical'],'file':pi['file'],'html':pi['html'],'parent_R9_sha256':pi['sha256'],'sha256':H(f),'html_sha256':H(hh),'criteria':pi['criteria'],'r10_measured_or_document':xn,'unexecuted':un}
 with ThreadPoolExecutor(max_workers=8)as px:index=list(px.map(emit0,work))
 assert(len(set(seen)),len(index),len(reg))==(2619,652,2619)and set(rr)<=set(seen)
 df=dest/'Dovezi_criterii.json';wr(df,{'schema':'A12.R10','parent_R9':S(R9/'Dovezi_criterii.json'),'evidence':ev,'inverse_task_requirement_links':inv});rf=dest/'Registru_reexecutare_R10.json';wr(rf,{'schema':'A12.R10','population_652':652,'criteria_2619':2619,'rows':reg,'open_NEEXECUTAT':[z['criterion']for z in reg if z['R10']=='NEEXECUTAT']});hp=dest/'Audit_individual_P01_R10.html';hp.write_text(table(index,states['NEEXECUTAT']),encoding='utf8')
 zlist=[]
 for zone0 in read(pplan)['each_zone']:
  owner=zone0['owner'];ass=zone0['assigned'];assigned_ids=[t['id']for t in ass];meter=[c for c in assigned_ids if bool(seen[c][1])];actual=[c for c,oz in ori.items()if owner in oz]
  zlist.append({'zone':owner,'title':zone0['sector'],'assigned_164_count':len(ass),'assigned_ids':assigned_ids,'assigned_with_new_measure':meter,'contributed_measure_or_qualified_observation':sorted(actual),'domain_report_new':zone.get(owner),'previous_round_owner_evidence_retained':True,'comment':'Registrul separă zona responsabilă de agentul care a făcut efectiv măsurarea. Fiecare fișă păstrează probele și limitele originale.'})
 summaries=['<li><strong>'+e(v['zone'])+' · '+e(v['title'])+'</strong> — '+str(v['assigned_164_count'])+' cazuri repartizate, '+str(len(v['assigned_with_new_measure']))+' cu observație nouă pe acest lot. '+('Raport zonal nou înregistrat.' if v['domain_report_new'] else 'Probele zonale din rundele precedente au fost păstrate.')+'</li>'for v in zlist]
 info='<section aria-label="Repartizare și surse"><h2>Cele zece zone</h2><p>Registrul pornește de la 164 de criterii cu date de test, 873 fără comparator nou și 167 de cazuri istorice. O observație nouă poate rezolva doar un pas dintr-o cerință mai mare. A11 acordă nota în documentul său de recepție.</p><ul>'+''.join(summaries)+'</ul><details><summary>Ce s-a verificat în această rundă</summary><ul><li><a href="fise_html/Fisa_T06.html">T06 și comparația bancară</a>. Procesul și interfața au produs câte 168 de rânduri și 22 de diferențe. În fișă este separat defectul de afișare a totalului după filtrarea pe un cont gol.</li><li><a href="fise_html/Fisa_T201.html">T201 și numerotarea registrelor</a>. Două conexiuni au primit 40 de numere distincte. Tranzacția anulată a lăsat numărul 41 pentru următoarea alocare.</li><li><a href="fise_html/Fisa_T204.html">T204 și tipăriturile</a>. Toate cele 12 texte PDF comparate au coincis în fiecare JAR. Ștergerea unui câmp în copia pentru test a fost detectată în toate cele 12 documente.</li><li><a href="fise_html/Fisa_T216.html">T216 și comenzile de canal</a>. Importul a preluat antetul, însă a pierdut calitatea de comandă proprie și linia. Facturarea și plata unei comenzi validate rămân deschise pentru această origine.</li><li><a href="fise_html/Fisa_T329.html">T329 și costul pe lot</a>. Fișa distinge postările încercate, rollbackul și notele efectiv păstrate în fiecare schemă.</li></ul></details></section>'
 page0=table(index,states['NEEXECUTAT']);hp.write_text(page0.replace('<label>Caută',info+'<label>Caută',1),encoding='utf8');H.cache_clear()
 p07=E/'R10_pregatire/A07_T216/T216_raport.json';files=[pplan,histfile,P10/'T330_reconciliere_de_componente_301.json',P10/'Version_git_ultima_verificare.json',P10/'T216_metadate_R9_corectate.json',P10/'Raport_preliminar_A12.json',P10/'Registru_componenta_A12_supliment.json',E/'A11_control_A12_R9.json',E/'A11_control_supliment_G3_C20_postR9.json',E/'R9_supliment/A06_G3_C20/Raport_G3_C20.json',p07,E/'delta/2026-11-02T19-45-29-330Z/Delta.json',P10/'A05_handoff_adaptor.json',P10/'Registru_pg_implicite_A12.json',P10/'Registru_SAGA_banca_A12.json',P10/'Registru_documentar_A12.json',P10/'Registru_SAGA_UI_A12.json',P10/'Zone_A02_A10/Rezultat.json',P10/'Zone_A02_A10/T254_receptie.json',P10/'Zone_A02_A10/T326_T333_receptie.json',P10/'Zone_A08/Rezultat.json',P10/'Zone_A08/T351_receptie.json',P10/'Zone_A09/Rezultat.json',P10/'Zone_A04/Rezultat.json',P10/'Zone_A01/Rezultat.json',P10/'Zone_A01/T159_receptie.json',P10/'Zone_A01/T58_receptie.json',P10/'T216_comparator_de_reutilizare.json',P10/'Controale_independente_A11.json']
 stage={'utc':now(),'schema':'A12.R10.P01','parent':S(R9/'MANIFEST_R9.json'),'master':BASE,'prior_quality_A11':6.4,'independent_grade':None,'product_grade':None,'counts':{'cases':652,'criteria':2619,'intake_R9_NEEXECUTAT':1204,'R10_NEEXECUTAT':states['NEEXECUTAT'],'states':states,'exercises':q,'total_relations':sum(map(len,inv.values())),'additions_by_type':types,'initially_fixture_ready':164,'initially_without_new_comparator':873,'initially_historical':167},'all_ten_zones':zlist,'delta':{'P01':693,'cohort':652,'other_changed':['T228','T321'],'no_new_final_eligible':True},'input_files':{p.relative_to(B).as_posix():H(p)for p in files if p.exists()},'assets':{p.name:H(p)for p in [df,rf,hp]},'open_findings':'Nicio notă atribuită de A12. Distingeți origine nouă de P93/Q, comandă de set de rezervă nativă pe produse primare, constatare de regulă din produs de limită a laboratorului. Un caz încă NEEXECUTAT rămâne în registru și după o mențiune contextuală.','records':index}
 afr=[q['id']for q in read(E/'A11_control_A12_R9.json')['remaining_reaudit']];assert len(afr)==5
 stage['five_A11_actions_receipt']={
 'R9-Q1':{'asked':afr[0],'intake_distinct':[164,873,167],'direct_or_documentary_in_164':q['in_164_receipted'],'pending_from_intake_164':sorted(v['criterion']for v in reg if v['R10_entry_cohorts']['164']and v['R10']=='NEEXECUTAT'),'lookups':['Registru_reexecutare_R10.json','A12_raport.json#/all_ten_zones']},
 'R9-Q2':{'asked':afr[1],'bounds':S(p07),'metadata_crosscheck':S(P10/'T216_metadate_R9_corectate.json'),'result':'Originea proprie a ajuns la antet, dar conversia s-a oprit înaintea unui C_Order eligibil. Factura, numărul, încasarea și returul din aceeași comandă rămân neprobate. TVA 21% este condiție diferită.'},
 'R9-Q3':{'asked':afr[2],'independent':S(E/'A11_control_supliment_G3_C20_postR9.json'),'ids':['T354-R2-004','T354-R2-021','T354-R2-027'],'result':'Au fost separate documentele persistente cu produse primare, refuzul setului în calea manuală, repetarea creării POST și repetarea CO pe documentul existent.'},
 'R9-Q4':{'asked':afr[3],'handoff_A05':zone.get('A05'),'alternative_component_ledger_only':S(P10/'T330_reconciliere_de_componente_301.json'),'ids':['T329-R2-012','T330-R2-025'],'rule':'Controlul costului pe schemă și ASI și numitorul suitei de la export nu sunt interschimbabile.'},
 'R9-Q5':{'asked':afr[4],'routers_873':S(histfile),'comparator_on_intake_873':q['in_873_receipted'],'example_signed_references':[S(P10/'Registru_documentar_A12.json'),S(P10/'T210_auth_trace_routes.json'),S(P10/'T227_mutanti_nominali.json'),S(P10/'Zone_A02_A10/T254_bytecode.json')],'limit':'Documentul autoritativ, sursa unei implementări, un rezultat istoric și o măsurare refăcută sunt nivele distincte.'}}
 latest=E/'R10_pregatire/Delta_roluri_2026-11-02T20-46-47-993Z.json';ld=read(latest);assert H(latest)=='87b1c75932f76166493aa212115ea283de57182ccbafbd9151017780c7da7975' and ld['current_head']==BASE and ld['all_projects']==[996,996] and ld['p01']==693 and ld['frozen_cases']==652 and not ld['changed_frozen'];assert H(B/ld['from'])==ld['from_sha256'] and H(B/ld['to'])==ld['to_sha256'];assert len(ld['changes'])==3 and not any(z['in_frozen_R9'] for z in ld['changes'])
 stage['delta']={'R10_opening_snapshot_19_45Z':S(E/'delta/2026-11-02T19-45-29-330Z/Delta.json'),'since_previous_cutoff_at_opening':['T228','T321'],'latest_tracker_cutoff_20_46_47Z':S(latest),'snapshot_pair_exact':{'from':S(B/ld['from']),'to':S(B/ld['to'])},'records_all_projects_before_after':ld['all_projects'],'P01':ld['p01'],'already_frozen':ld['frozen_cases'],'head':ld['current_head'],'changes_since_19_45Z':ld['changes'],'new_eligible_final_tasks':[],'reopened_or_changed_frozen':ld['changed_frozen']}
 stage['input_files'][latest.relative_to(B).as_posix()]=H(latest);stage['input_files'][ld['from']]=ld['from_sha256'];stage['input_files'][ld['to']]=ld['to_sha256']
 extra=[v for v in reg if v['cohorts']['external_38']];assert len(extra)==38
 stage['external_boundaries_intake']={'R8_R9_tags_unchanged':38,'overlap_164':sum(v['R10_entry_cohorts']['164'] for v in extra),'overlap_873':sum(v['R10_entry_cohorts']['873'] for v in extra),'overlap_167':sum(v['R10_entry_cohorts']['167'] for v in extra),'218_separate_historical_partial_tags':sum(v['cohorts']['separate_partial_218'] for v in reg),'external_tags_with_some_new_subcase':sorted(v['criterion']for v in extra if v['R10_observed_or_documentary']),'not_additive':True,'scope':'Cele 38 sunt subcondiții cu partener, hardware sau autorizare externă. Ele provin din două poziții cu fixtură și 36 din lotul rezidual 167. Nu sunt 38 taskuri în plus și o verificare locală nu achită partea externă.'}
 wr(dest/'A12_raport.json',stage);print('R10',preview,H(dest/'A12_raport.json'),stage['counts']['R10_NEEXECUTAT'],q,flush=True)
if __name__=='__main__':build(os.environ.get('A12_R10_PREVIEW')=='1')
