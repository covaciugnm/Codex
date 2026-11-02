from a12_r7_prepare_results import *
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
from collections import Counter
import html
R6=old;rr6=rd(old/'Registru_reexecutare_R6.json')['records'];rmap={v['criterion']:v for v in rr6};ridx={v['criterion']:i for i,v in enumerate(rr6)};reclassified={x['evidence']:(i,x)for i,x in enumerate(q148)}
def alls(w):return sum([w[k]for k in ('operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria')],[])
def norm(v):return str(v)if isinstance(v,str)else json.dumps(v,ensure_ascii=False)
def eh(v):return html.escape(norm(v)if v is not None else '—')
def rels(c):
 r=[(c['source_evidence_id'],'source')]+[(v,'authority')for v in c.get('authority_evidence_ids',[])]
 for field in ['closure','current']:r += [(i,field)for i in c[field]['evidence_ids']]
 for k,field,tag in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:r += [(v,tag)for v in c.get(k,{}).get(field,[])]
 r += [(v,'case_context')for v in c.get('strict_related_sources_R5',[])]+[(v['evidence'],'R6_scenario')for v in c['R6_new_scenarios']]
 r += [(v['evidence'],'R7_scenario')for v in c['R7_new_scenarios']]+[(v['evidence'],'R7_context')for v in c['R7_context']];return set(r)
def page(w):
 chunks=[]
 for c in alls(w):
  idx=c['id'];tri0=c.get('R7_cohort_position');rec=c['R7_new_scenarios'];ctx=c['R7_context']
  dl=lambda k,v:'<dt>'+eh(k)+'</dt><dd>'+eh(v)+'</dd>'
  oldlabel=c['current']['status'];t=tri0['category']if tri0 else None;cont=('<h3>Probe din această rundă</h3><ul>'+''.join('<li><b>'+eh(z['result'])+'</b> · '+eh(z['expected'])+'<br>'+eh(z['observed'])+'<br><small>'+eh(z['qualification'])+' · '+eh(z['evidence'])+'</small></li>'for z in rec)+' </ul>')if rec else ''
  if ctx:cont+='<details><summary>Contexte și limite verificate ('+str(len(ctx))+')</summary><ul>'+''.join('<li>'+eh(z['result'])+' · '+eh(z['observed'])+'<br><small>'+eh(z['qualification'])+'</small></li>'for z in ctx)+'</ul></details>'
  chunks.append('<section id="'+eh(idx)+'"><h2>'+eh(idx)+'</h2><p>'+eh(c['normative_content'])+'</p><dl>'+dl('La închidere',c['closure']['status'])+dl('Stare curentă',oldlabel)+dl('Ce arată proba',c['current'].get('observed'))+dl('Încadrare dacă era neexecutat',t)+dl('Metodă, titular și condiția rămasă',tri0.get('case_method')if tri0 else c['current'].get('blocking_reason'))+'</dl>'+cont+'</section>')
 return '<!doctype html><html lang="ro"><meta charset="utf-8"><title>'+eh(w['task'])+' · Audit P01 R7</title><style>body{font:16px/1.55 system-ui;max-width:1000px;margin:32px auto;padding:0 18px;color:#183047}section{border-top:1px solid #c6d0d8;padding-top:14px}dt{font-weight:650}dd{margin:0 0 10px;overflow-wrap:anywhere}small{color:#536779}li{margin:7px 0}</style><body><nav><a href="../Audit_individual_P01_R7.html">Index P01</a> · <a href="../taskuri/Fisa_'+quote(w['task'])+'.json">Date și referințe</a></nav><h1>'+eh(w['task'])+' · '+eh(w['title'])+'</h1><p>'+eh(w['canonical'])+' · '+eh(w['state_at_new_capture'])+' · '+str(len(alls(w)))+' criterii. Verdictul A11 asupra rundei R7 este în așteptare.</p>'+''.join(chunks)+'</body></html>'
def build():
 docs=[];state=Counter();old_new=Counter()
 for rr in prior['records']:
  w=rd(old/rr['file']);assert sha(old/rr['file'])==rr['sha256'];w['schema']='A12_R7';w['parent_R6_immutable']={'sha':rr['sha256'],'file':(old/rr['file']).relative_to(ROOT).as_posix(),'A11_score':5.8}; key=w['task']
  related=exrefs.get(key,[])
  if related:w['R7_EX_independent']={'plan_preserved':True,'subject':related,'A11_cases':{k:{'pointer':'/cases/'+k,'subscore_quality':exd['cases'][k].get('quality_score'),'report_sha':exd['cases'][k]['sha256_report']}for k in related},'source':ex.relative_to(ROOT).as_posix(),'source_sha':dig(ex),'scope':'Este nota de audit EX a probei la momentul respectiv. Nu este o certificare retroactivă a taskului.'}
  for c in alls(w):
   cid=c['id'];prev=c['current'].copy();x=candidates.get(cid,[]);ctx=contexts.get(cid,[]);c['R7_new_scenarios']=x;c['R7_context']=ctx
   if cid in cix:
    i,tri0=cix[cid];c['R7_cohort_position']={'source':classp.relative_to(ROOT).as_posix(),'hash':dig(classp),'pointer':'/records/'+str(i),'category':tri0['category'],'case_method':tri0['case_method'],'owner':tri0['owner'],'has_partial_external':tri0['has_partial_external'],'current_was_NEEXECUTAT':True}
   for sc in c['R5_measured_scenarios']:
    q=sc['evidence']
    if q in reclassified:
     i,origin=reclassified[q];sc['R7_recovered_predicate']={'source':P148.relative_to(ROOT).as_posix(),'hash':dig(P148),'pointer':'/rows/'+str(i),'level':origin['comparison']['code_state'],'group_child_count':len(origin['comparison']['child_assertions'])}
   if ctx or x:c['R6_current_before_R7']=prev
   if x:
    sec=[u for u in x if u['phase']=='closure'];cur=[u for u in x if u['phase']=='current'];reported=[u for u in cur if u['result'] in ['ABATERE_NUMERICĂ','DIFERENȚĂ_INVENTAR','DIFERENȚĂ_DE_EDIȚIE','TRASEU_Q_BLOCAT_V01','FAIL_ÎN_TEST']]
    fullA=[u for u in cur if u['result'].startswith('PASS')]; histid=sec[0]['evidence']if sec else None
    if sec:
     c['before_R7_closure']=c['closure'].copy();c['closure']={'status':'DOCUMENT_VERDICT_PLAN_ISTORIC_RELECTURĂ_R7','observed':norm(sec[0]['observed']),'evidence_ids':list(dict.fromkeys([*c['closure']['evidence_ids'],*(v['evidence']for v in sec)])),'blocking_reason':sec[0]['qualification']}
    if cid=='T06-R2-020':label='REFUZ_CUI_STRĂIN_NATIV_168_168_CONFIRMARE_ȘI_RETRY'
    elif cid=='T03-R2-039':label='GARDĂ_PER_JVM_ȘI_LACĂT_PG_CONDIȚIONAL_ABATERE_STATICĂ_RĂMÂNE'
    elif cid in ('T58-R2-005','T58-R2-006'):label='REFUZ_ERP_CONFIRMAT_LA_STRATUL_NOMINAL'
    elif cid=='T58-R2-009':label='PROCES_NATIV_NOTĂ_VC_CO_POSTATĂ'
    elif cid=='T58-R2-010':label='REFUZ_INVERSARE_AMORT_COMPONENTĂ_NATIVĂ'
    elif cid in ['T216-R2-001','T216-R2-002','T216-R2-005','T216-R2-006','T216-R2-007']:label='CONTRAEXEMPLU_PENTRU_ORIGINEA_Q'
    elif any(z['result']=='ABATERE_NUMERICĂ' or z['result']=='DIFERENȚĂ_INVENTAR' for z in cur):label='ABATERE_DE_PRAG_DELIMITATĂ_LA_COD_SAU_FIXTURĂ'
    elif fullA:label='ORACOL_NOMINAL_ACOPERIT_ÎN_PROBELE_A03'
    elif histid and not cur:label='DOVADĂ_DOCUMENTARĂ_PLAN_NOMINAL'
    elif all(u['result'] in ['PREDICAT_CONDIȚIE_EXECUTATĂ','GRUP_DE_ASERȚIUNI_APEL_IDENTIFICAT']for u in x):
     label='R7_CONDIȚIE_TEST_IDENTIFICATĂ'if prev['status']=='OBSERVAT_FĂRĂ_PREDICAT_NOMINAL_RECUPERAT'else prev['status']
    elif prev['status']=='NEEXECUTAT':label='R7_SUBCAZ_EXECUTAT_CU_ORACOL_EXPLICIT'
    else:label='R7_PROBĂ_SUPLIMENTARĂ_CU_LIMITE'
    top=reported+cur+sec or x; unique=list(dict.fromkeys([*prev.get('evidence_ids',[]),*(z['evidence']for z in x)]))
    c['current']={'status':label,'observed':' | '.join(norm(z['observed'])for z in top[:2])+' · '+str(len(x))+' înregistrări de probă în R7.','evidence_ids':unique,'blocking_reason':' '.join(dict.fromkeys(z['qualification']for z in x))}
   elif cid in cix:
    tri0=cix[cid][1];c['current']['blocking_reason']=tri0['case_method'];c['current']['supplemental_context_only']=len(ctx)
   if cid in rmap:
    rec=rmap[cid];rec['immutable_R6_state']=rec['R6_state'];rec['R7_state']=c['current']['status'];rec['R7_scope_mapped']=c.get('R7_cohort_position');rec['R7_observed_evidence']=[z['evidence']for z in x];rec['R7_context_evidence']=[z['evidence']for z in ctx]
    if cid in cix:rec['next_individual_R7_action']=cix[cid][1]['case_method']
   state[c['current']['status']]+=1
   old_new[(prev['status'],c['current']['status'])]+=1
   for eid,phase in rels(c):
    assert eid in ev,(eid,key,cid);rev[eid].append({'task':key,'criterion':cid,'relation':phase})
  w['R7_summary']={'score':None,'product_score':None,'review_state':'DIRECTOR_A11_INDEPENDENT_PENDING','formerly_neexec_in_cohort':[c['id']for c in alls(w)if c['id']in cix],'directly_exercised_this_round':[c['id']for c in alls(w)if c['R7_new_scenarios']],'contextual_evidence_only_or_additional':[c['id']for c in alls(w)if c['R7_context']],'still_NEEXECUTAT':[c['id']for c in alls(w)if c['current']['status']=='NEEXECUTAT']}
  docs.append((w,rr))
 def output(t):
  w,rr=t;p=R/rr['file'];hp=R/rr['html'];wr(p,w);hp.write_text(page(w),encoding='utf8')
  return {'task':w['task'],'canonical':w['canonical'],'title':w['title'],'state':rr['state'],'file':rr['file'],'html':rr['html'],'R6_sha':rr['sha256'],'sha256':sha(p),'html_sha256':sha(hp),'criteria':rr['criteria'],'direct_criteria_R7':len(w['R7_summary']['directly_exercised_this_round']),'context_criteria_R7':len(w['R7_summary']['contextual_evidence_only_or_additional']),'unexecuted':len(w['R7_summary']['still_NEEXECUTAT'])}
 with ThreadPoolExecutor(max_workers=10)as px:idx=list(px.map(output,docs))
 assert sum(state.values())==2619 and len(idx)==652
 wr(R/'Dovezi_criterii.json',{'schema':'A12.R7','R6_prior_hash':dig(old/'Dovezi_criterii.json'),'evidence':ev,'inverse_task_requirement_links':dict(rev)})
 wr(R/'Registru_reexecutare_R7.json',{'schema':'A12.R7','source_R6_hash':dig(old/'Registru_reexecutare_R6.json'),'original_1868':1868,'additional13':13,'original_R6_neexecutat_cohort':1587,'classification_source':dig(classp),'records':rr6})
 rows=''.join('<tr><td><a href="'+eh(z['html'])+'">'+eh(z['task'])+'</a></td><td>'+eh(z['canonical'])+'</td><td>'+eh(z['title'])+'</td><td>'+eh(z['state'])+'</td><td>'+eh(z['criteria'])+'</td><td>'+eh(z['direct_criteria_R7'])+'</td><td>'+eh(z['unexecuted'])+'</td></tr>'for z in idx)
 intro='<p>652 de fișe și 2.619 criterii. Din cele 1.587 de criterii fără execuție în R6, '+str(old_new[('NEEXECUTAT','NEEXECUTAT')])+' sunt în continuare fără execuție individuală. Clasificarea distinge ce se poate reproduce, ce ține de istoric, ce decizie sau ce date lipsesc și unde traseul testat se oprește la un defect. Pentru fiecare caz, dovezile și limitele sunt la nivelul rezultatului măsurat.</p>'
 (R/'Audit_individual_P01_R7.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Audit individual P01 · R7</title><style>body{font:16px/1.5 system-ui;margin:30px auto;padding:0 18px;max-width:1450px;color:#18354c}td,th{padding:5px;border-bottom:1px solid #d2d9df;text-align:left}th{position:sticky;top:0;background:#f2f6fa}</style><h1>Audit individual P01 · runda 7</h1>'+intro+'<p><a href="A12_raport.json">Raport și proveniență</a> · <a href="Registru_reexecutare_R7.json">Registrul de reexecuție</a> · <a href="Dovezi_criterii.json">Catalogul de dovezi</a></p><table><tr><th>Fișă</th><th>ID canonic</th><th>Obiectiv</th><th>Stare</th><th>Criterii</th><th>Probă R7</th><th>Neexecutate</th></tr>'+rows+'</table>',encoding='utf8')
 srcs={input_report,E/'A11_control_A12_R6.json',E/'A11_control_suplimente_A12_postR6.json',E/'A11_reproduceri_R6/independent_jvm.json',classp,P148,ex,explan,ux,RP/'stack_exec.json',RP/'stack_exec_neexec.json',E/'R4_zone/A06/A06_raport.json',E/'A11_control_A04_R3.json',E/'A11_control_A05_R4.json',*RP.glob('*.json'),*[(RP/'SQL/Matrice_SQL_reala_R7.json')],*[(ROOT/o['source'])for k,o in ev.items()if k.startswith('EV7-')]}
 # Include the verified source-only supplemental findings exactly at their source, not as independent product acceptance.
 for u in [E/'R3_zone/A04/Addendum_moneda_NIR.json',E/'R3_zone/A04/A04_raport.json',E/'R4_zone/A05/A05_raport.json']:
  if u.is_file():srcs.add(u)
 count={'cases':len(idx),'criteria':sum(state.values()),'remaining_NEEXECUTAT':state['NEEXECUTAT'],'R6_previously_NEEXECUTAT':1587,'classified_local':1542,'classified_with_external_component':45,'by_class_before_tests':jd(classp)['classification_counts'],'directly_updated_criteria':len(candidates),'context_criteria':len(contexts),'new_observation_links':sum(map(len,candidates.values())),'new_context_links':sum(map(len,contexts.values())),'EV7_new':sum(k.startswith('EV7-')for k in ev),'links_symmetric':sum(map(len,rev.values())),'148_predicate_results':jd(P148)['statistics'],'accepted_by_A12_as_independent_product_grade':0,'states':state}
 count['prior_1587_now_observed']=1587-state['NEEXECUTAT'];count['after_by_class_remaining']={cat:sum(1 for cid,(_,tr)in cix.items()if tr['category']==cat and rmap[cid]['R7_state']=='NEEXECUTAT')for cat in jd(classp)['classification_counts']}
 report={'schema':'A12.R7.P01','utc':datetime.now(UTC).isoformat(),'score':None,'product_score':None,'source_implementation_git_head_fixed':shaGit,'review_state':'PROPUS_A11','R6_score_from_A11':5.8,'counts':count,'findings':[{'id':'R7-T06-CUI','case':'T06-R2-020','fact':'CUI valid identic → proces acceptat; alt CUI valid → refuz specific, 168→168 cu amprentă de conținut identică după retry.'},{'id':'R7-T06-REZUMAT','case':'T06-R2-017','fact':'La un cont cu 2 configurări de schemă, procesul raportează 2 conturi și 336 rânduri scrise pe 168 note. Sunt 168 ID persistate. Nu constituie dublare de postări financiare.'},{'id':'R7-T03-GARDA','case':'T03-R2-039','fact':'3<5 pentru expresia statică. Stare in-memory separată în două JVM; pe CESIRO UI este socat, iar procesul lunar are un lacăt PostgreSQL distinct și verifică starea. Nu există dovadă de două înregistrări contabile create prin acel proces.'},{'id':'R7-T216-Q','case':'T216-R2-001/002/005/006/007','fact':'2 linii în DTO, 0 persistate. V01+V02 se reduc la V01 când se adaugă seller.cui în varianta controlată; comanda Q nu traversează validarea către ERP.'}],'limitations':['531 de criterii aveau cel puțin un traseu local identificat la început, nu 531 aplicații certificate. Fiecare înregistrare marchează ce s-a executat efectiv și ce a rămas deschis.','Un grup de aserțiuni cu același mesaj și două JAR-uri nu este un număr de scenarii comerciale independente. Au fost recitite toate cele 148 cazuri, 52 ca predicat individual și 96 ca apel la un grup executat cu vectorii săi.','O decizie istorică din dosarul unui predecesor se leagă ca documentare; nu stabilește automat o acceptare funcțională a succesorului.','10 rulari original și 10 mutante SQL cu baze izolate ajută la detectarea sensibilității testului. Un mutant provocat nu este un defect în buildul inițial.','Restul fără execuție include specificații funcționale, istorice și contracte externe parțiale; fiecare are un verificator și o condiție nominală.'],'inputs':{p.relative_to(ROOT).as_posix():dig(p)for p in sorted(srcs)if p.is_file()},'artifacts':{k:dig(R/k)for k in ['Audit_individual_P01_R7.html','Dovezi_criterii.json','Registru_reexecutare_R7.json','probe/Rezultate_R7.json']},'records':idx}
 wr(R/'A12_raport.json',report);print('R7',sha(R/'A12_raport.json'),count['remaining_NEEXECUTAT'],count['directly_updated_criteria'],count['links_symmetric'])
if __name__=='__main__':build()

