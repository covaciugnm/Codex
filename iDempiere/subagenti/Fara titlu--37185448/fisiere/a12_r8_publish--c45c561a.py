from a12_r8_zones import *
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from collections import Counter,defaultdict
A=E.parent
def safe(v):return html.escape(compact(v),quote=True)
def publicurl(s):return quote(s,safe='/:#')
def hlinks(u,reference):
 f=u['source']['file'];return '<a href="../../'+publicurl(f.replace('executie/','',1))+'">'+safe(Path(f).name)+'</a>'if f.startswith('executie/')else safe(f)
def wpage(w):
 out=[]
 for c in criteria(w):
  z=c['R8'];p=z['proofs'];lines=[]
  for v in p:
   sy=v['source']['file'];refs=hlinks(v,None)
   lines.append('<li><b>'+safe(v['phase'])+'</b> · '+safe(v['kind'])+'<br><i>Etalon.</i> '+safe(v['oracle'])+'<br><i>Observat.</i> '+safe(compact(v['observed'])[:1550])+'<br><i>Limită.</i> '+safe(v['qualification'])+'<br>'+refs+' <code>'+safe(v['pointer'])+'</code> · <small>'+safe(v['id'])+'</small></li>')
  out.append('<section id="'+safe(c['id'])+'"><h2>'+safe(c['id'])+'</h2><p>'+safe(c['normative_content'])+'</p><dl><dt>Observat în R7</dt><dd>'+safe(z['before'])+'</dd><dt>Stare în R8</dt><dd>'+safe(z['effective_status'])+'</dd><dt>Pas rămas</dt><dd>'+safe(z['next_action'])+'</dd></dl>'+('<ol>'+''.join(lines)+'</ol>'if lines else'')+'</section>')
 return '<!doctype html><html lang="ro"><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+safe(w['task'])+' · Audit R8</title><style>body{max-width:1020px;margin:35px auto;padding:0 20px;font:16px/1.6 system-ui;color:#19374d}section{border-top:1px solid #bfccd4;margin-top:25px}dt{font-weight:bold}dd{margin:0 0 8px}li{margin-bottom:16px;overflow-wrap:anywhere}code{font-size:.8em}small{color:#405d73}</style><nav><a href="../Audit_individual_P01_R8.html">Toate taskurile P01</a> · <a href="../taskuri/Fisa_'+safe(w['task'])+'.json">Fișa și dovezile integrale</a></nav><h1>'+safe(w['task'])+' · '+safe(w['title'])+'</h1><p>'+safe(w['canonical'])+' · '+safe(w['state_at_new_capture'])+'. Dosarul de bază a primit 6,0/10 în R7. R8 se transmite auditorului A11 pentru apreciere independentă.</p>'+''.join(out)+'</html>'
def state(c,obs,ex):
 before=c['current']['status'];t=c['id'];ms=[v for v in obs if v['phase']=='current'];hx=[v for v in obs if v['phase']=='historical'];corr=[v for v in obs if v['phase']=='correction']
 if t=='T159-R2-050':return 'CLI_ZERO_PE_INTERSECȚIE_VIDĂ_CONSERVARE_NEVERIFICATĂ'
 if t in ex:
  if t=='T354-R2-021':return 'DOUĂ_COMENZI_STAGING_REZERVATE_CERERE_4_CAZURILE_6_5_NATIVE'
  if t=='T354-R2-027':return 'DOUĂ_G1_PUBLICARE_13_PO_DIVERGENȚĂ_9_SEPARAT_DE_EV7'
  return ex[t]['adjudication']
 if not ms:
  if any(v['coverage']=='documentary_only'and 'DIVERGENȚĂ_DOCUMENTARĂ' in v['kind']for v in hx):return 'ABATERE_DOCUMENTARĂ_RECALCULATĂ'
  if any(v['coverage']=='documentary_only'for v in hx):return 'DOCUMENTAR_RECALCULAT_FĂRĂ_EXECUȚIE_DE_PRODUS'
  return before
 if t=='T06-R2-001':return 'DICȚIONAR_50_TOTALE_40_EVA_ISTORIC_ȘI_CESIRO'
 if t=='T06-R2-012':return 'CONTROL_LINUX_LIVRARE_DISTINCT_DE_EXECUȚIA_WINDOWS_CU_EȘECURI'
 if t=='T204-R2-024':return 'COMPARAȚIE_GIT_12_LINII_VS_4_SITURI_ETALON_UNITĂȚI_DISTINCTE'
 if t=='T310-R3-001':return 'CONFLICT_D107_PG_DOUĂ_SESIUNI_ȘI_JAR_CONFIRMĂ_FĂRĂ_CLICK_NOU'
 if t=='T04.06-R3-001':return 'ORACOL_EMAG_ȘI_REFERINȚĂ_EXPORT_TESTATE_CONECTOR_ERP_SEPARAT'
 if t=='T191-R2-007':return 'DICȚIONAR_C4_FAZĂ_NECUNOSCUTĂ'
 if any('ABATERE_ORACOL_EXECUTAT' in v['kind']for v in ms):return 'ABATERE_ORACOL_EXECUTAT_ÎN_STRATUL_NOMINAL'
 if any('DIVERGENȚĂ_ISTORIC_VS_CURENT' in v['kind']for v in ms):return 'DIVERGENȚĂ_DOCUMENTATĂ_ÎNTRE_EPOCI'
 if any(v['coverage']=='full_criterion_at_reported_layer'for v in ms):return 'ORACOL_EXERCITAT_LA_STRATUL_DIN_CERINȚĂ'
 return 'SUBCAZ_EXERCITAT_CU_LIMITĂ_INDIVIDUALĂ'
def build(shipped=False):
 assert shipped or os.environ.get('A12_R8_PREVIEW')=='1'
 dest=R if shipped else Path('D:/CodexWork/a12-r8-preview');(dest/'taskuri').mkdir(parents=True,exist_ok=True);(dest/'fise_html').mkdir(exist_ok=True)
 obs,zonefiles=sources();extras=attach(obs)
 q=rd(ER);ex={x['criterion']:x for x in q['criteria']};R7cat=rd(R7/'Dovezi_criterii.json');rev=defaultdict(list)
 r7reg=rd(R7/'Registru_reexecutare_R7.json');reg7={v['criterion']:v for v in r7reg['records']};cat=R7cat['evidence'].copy()
 lookup=defaultdict(list);corrset={(x['criterion'],p['id'])for x in ex.values()for p in x['references']};removed=0
 for eid,refs in R7cat['inverse_task_requirement_links'].items():
  for b in refs:
   row=b.copy()
   if (row['criterion'],eid)in corrset and row['relation']in ['current','R7_scenario']:
    row['relation']='R7_corrected_context';removed+=1
   s=(eid,row['relation'])
   if s not in lookup[row['criterion']]:lookup[row['criterion']].append(s);rev[eid].append(row)
 assert len(corrset)==10 and removed==20,(len(corrset),removed)
 classes=rd(E/'R7_pregatire/A12/Clasificare_nominala_1587.json')['records'];base={x['criterion']:x for x in classes};cohort={c for c,x in base.items()if x['category']=='FIXTURĂ_EXECUTABILĂ'and reg7[c]['R7_state']=='NEEXECUTAT'};assert len(cohort)==467
 provenance=[zonefiles['A03'],zonefiles['A05'],ER,DATA,R7report,E/'A11_control_A12_R7.json',E/'R8_pregatire/Index_883_relectura_surse.json',P/'Lista_93.json',P/'SQL/Executii_SQL_r8.json',P/'Dictionar_CESIRO_readonly.json',P/'JVM/Executii.json',P/'JVM/Executii_supliment.json',P/'T224_unelte_originale_simulate.log',P/'T204_T171_predicate_tail.log',P/'T227_T204_T171_grep_doua_versiuni.log',P/'Ofline_situri/Site_si_garda.json',P/'T314_sql_meniu_chei.json',E/'R7_supliment/A12_A06_metadate_Q.json',E/'R6_supliment/A12_UX_NIR_provenienta.json',E/'R3_zone/A04/Addendum_moneda_NIR.json',E/'R3_zone/A04/A04_raport.json',E/'Reverificare_Flux_S1_aviz_retur_R6.json',E/'A11_control_CESIRO1_EX01_EX08.json',*E.glob('A11_control_A0?_R*.json'),*E.glob('A11_control_A10_R*.json'),*extras['semantic_A11_T159_inputs']]
 docs=[];reg=[];states=Counter();metrics=Counter();det=Counter();categories=defaultdict(Counter);allids=set();caseby=Counter();phases=Counter();alloccounts=Counter()
 for rr in oldr['records']:
  p=R7/rr['file'];assert h(p)==rr['sha256'];w=rd(p);w['schema']='A12.R8';w['immutable_R7_parent']=rf(p);w['R8_review_gate']='Transmis spre audit A11, fără notă acordată de executor.';ew=0;curCount=0;lhs=0
  cset=criteria(w); task=w['task']
  for c in cset:
   id=c['id'];allids.add(id);prior=c['current']['status'];changes=obs.get(id,[]);eff=state(c,changes,ex);baseclaim=reg7.get(id,{});nxt=baseclaim.get('next_individual_R7_action')or baseclaim.get('individual_next_step')or c['current'].get('blocking_reason')or ('Verifică sursa normativă a lui '+id+' și limita observată înainte de orice acceptare.')
   if id in ex:nxt=ex[id]['not_observed']
   if isinstance(nxt,(dict,list)):nxt=compact(nxt)
   direct=[z for z in changes if z['phase']=='current'];history=[z for z in changes if z['phase']=='historical'];context=[z for z in changes if z['phase']in ['context','old_context','old_current_evidence']];other=[z for z in changes if z['phase']in ['correction','pending']]
   ss=next((v['qualification']for v in direct if 'NEEXECUTAT'not in v['kind']),None)
   if ss:nxt=ss+' '+nxt
   if id=='T159-R2-050':nxt='Recuperează succesorul fiecăreia din cele 302 perechi și reconciliază verdictul său prin altă cheie sau decizie explicită.'
   if id=='T310-R3-001':nxt='Într-un cabinet exclusiv, pornește două sesiuni ZK autentificate pe același beneficiar sintetic, capturează refuzul lui A și suma 230 în tabela originală.'
   if id=='T354-R2-021':nxt='Separă ord=0 pentru primele două comenzi site de C_Order #1000089 al celei de-a treia; pentru concurență reală trebuie două tranzacții cu overlap identificabil și un retry.'
   if id=='T354-R2-027':nxt='Verifică independent ramura de achiziție IsSOTrx=N și efectul 9 vs 13 în timpul calculului pentru canal. Proba de combinare S1/S2 în RAM este context.'
   rels=list(lookup[id]);nwids=[]
   for z in changes:
    eid=z['id'];assert eid not in cat,(id,eid);cat[eid]=z;nwids.append(eid);link='R8_'+z['phase'];rels.append((eid,link));rev[eid].append({'criterion':id,'task':task,'relation':link});phases[z['phase']]+=1
   c['R8']={'before':prior,'effective_status':eff,'source_explicit_R7':{'file':rr['file'],'sha256':rr['sha256']},'direct_oracle_measurements':len(direct),'retrospective_traces':len(history),'contexts_or_previously_ran':len(context),'constraints_corrections':len(other),'in_467':id in cohort,'proofs':changes,'next_action':nxt,'claims_bear_no_product_grade':True,'effective_evidence_links':[{'id':a,'relation':b}for a,b in rels]};states[eff]+=1
   if id in cohort:
    catg='PROBĂ_ACTUALĂ_LA_ORACOL_SAU_SUBCAZ'if direct else'RECALCUL_DOCUMENTAR_CERUT'if eff.startswith('DOCUMENTAR_RECALCULAT')or eff=='ABATERE_DOCUMENTARĂ_RECALCULATĂ' else'NUMAI_ISTORIC_SAU_ORACOL_DOCUMENTAT'if history else'CONTEXT_SEPARAT_FĂRĂ_EXECUȚIE'if context else'NEEXECUTAT_CU_TITULAR'
    categories[base[id]['owner']][catg]+=1;alloccounts[catg]+=1
   if direct:curCount+=1
   if history:lhs+=1
   if eff=='NEEXECUTAT':ew+=1
   row={'task':task,'canonical':w['canonical'],'criterion':id,'owner':base[id]['owner']if id in base else baseclaim.get('owner'),'in_467':id in cohort,'original_category_R7':base[id]['category']if id in base else None,'R7_status':prior,'R8_status':eff,'actual_measurement_sources_this_round':[z['id']for z in direct],'historic_sources_read':[z['id']for z in history],'context_and_prior_no_new_execution':[z['id']for z in context],'corrections_or_still_due':[z['id']for z in other],'normative_text':c['normative_content'],'next_action':nxt,'dossier':'taskuri/Fisa_'+task+'.json'};reg.append(row)
  docs.append((w,rr,curCount,lhs,ew))
 assert set(obs)<=allids,(set(obs)-allids);assert len(allids)==2619 and len(reg)==2619 and len(docs)==652 and sum(alloccounts.values())==467
 def out(d):
  w,rr,nx,ny,nz=d;fp=dest/rr['file'];htmlp=dest/rr['html'];wr(fp,w);page=wpage(w).replace('</style>','*{box-sizing:border-box}body,section,dd,code,small{overflow-wrap:anywhere;min-width:0}p{max-width:100%}@media(max-width:575px){body{padding:0 12px;margin:16px auto}ul,ol{padding-left:24px}}</style>');htmlp.write_text(page,encoding='utf8');return{'task':w['task'],'canonical':w['canonical'],'title':w['title'],'state':rr['state'],'file':rr['file'],'html':rr['html'],'criteria':rr['criteria'],'sha256':h(fp),'html_sha256':h(htmlp),'parent_R7':rr['sha256'],'direct_criteria_this_round':nx,'historical_criteria_this_round':ny,'current_unexecuted':nz}
 with ThreadPoolExecutor(max_workers=9)as px:index=list(px.map(out,docs))
 wr(dest/'Dovezi_criterii.json',{'schema':'A12.R8','R7_evidence_catalog_parent':rf(R7/'Dovezi_criterii.json'),'evidence':cat,'inverse_task_requirement_links':rev});wr(dest/'Registru_reexecutare_R8.json',{'schema':'A12.R8.full','root_R7_registry_sha':h(R7/'Registru_reexecutare_R7.json'),'total_criteria':2619,'cohort_size':467,'allocation_counts':dict(categories),'all_rows':reg,'remaining_NEEXECUTAT':[z['criterion']for z in reg if z['R8_status']=='NEEXECUTAT']})
 cfg={'schema':'A12.R8','utc':now(),'fixed_git_commit':'6df998aee0e514d30856c461962afe99ebd0d113','independent_gate':'A11 urmează să evalueze R8.','previous_A11_R7':{'score':6.0,'source':rf(E/'A11_control_A12_R7.json')},'score':None,'product_score':None,'scope':{'dossiers':652,'criteria':2619,'completed_live_population':652,'tasks_with_unavailable_canonical_alias_not_invented':True,'R7_NEEXECUTAT_raw':1517,'R8_NEEXECUTAT':states['NEEXECUTAT'],'r7_semantic_erratum_does_not_increment_raw_1517':True,'R8_states':dict(states),'R7_candidates_467_by_owner':{k:dict(v)for k,v in categories.items()},'467_counts':dict(alloccounts),'criteria_with_current_measurement_wave':sum(1 for z in reg if z['actual_measurement_sources_this_round']),'newly_exercised_prior_NEEXECUTAT':sum(1 for z in reg if z['R7_status']=='NEEXECUTAT'and z['actual_measurement_sources_this_round']),'criteria_with_historical_readback':sum(bool(z['historic_sources_read'])for z in reg),'current_native_vs_historical_oracle_not_conflated':True,'old_errors_10_edges_retyped':10,'EV7_N_old_link_kinds_removed':removed,'proof_links_by_epoch_R8':dict(phases),'evidence_count':len(cat),'bidirectional_relations':sum(map(len,rev.values()))},'findings':[{'id':'R8-T06','message':'În istoricul q31 și în CESIRO curent sunt 50 de coloane totale pentru EVA_ComparatieBanca, dintre care 40 EVA_. Există o tabelă, un proces cu cinci parametri, o formă și indexul unic.'},{'id':'R8-T159-C47','message':'0 reclasificate în CLI cu zero perechi în intersecția dintre 302 perechi vechi și categoriile actuale. Conservarea celor 302 decizii nu este dovedită.'},{'id':'R8-T216','message':'Q rămâne exclusă în staging. Martorul independent din arhiva istorică P93-095157 emite factura 1000357/T216P-1 CO și obține confirmarea API după retry, fără dovada plății sau a afișării în DOM pentru aceeași origine.'},{'id':'R8-T354-C20','message':'Două comenzi site REZERVAT au ord=0 și cer împreună 4 componente. La stoc A=6 comanda a treia generează document ERP; la 5 este ROȘU. Proba distinctă pe două G1 dă 13 pentru rezervarea SO și 9 în prezența ordinului de cumpărare de 4.'},{'id':'R8-T310','message':'Două sesiuni fizice și metoda SQL_REVIZIE/inConflict din ambele JAR refuză revizia veche păstrând 230. Dialogul ZK nu a fost acționat în această reexecuție.'}],'limits':['Citirea unui document istoric nu înseamnă că acțiunea a fost executată pe configurația curentă.','Fiecare apariție a aceluiași criteriu în două JAR are același etalon.','Cifrele financiare generate pe fixtures și rolurile GardenWorld nu reprezintă tranzacții ale clientului în producție.','Rămân criterii fără etalon, condiții externe și procese ERP neexecutate, identificate în registru.','Cele 883 surse din indicele separat oferă candidați pentru relectură; T04.06 are deja un oracol parțial recuperat.'],'source_hashes':{p.relative_to(B).as_posix():h(p)for p in sorted(set(provenance)) if p.is_file()},'records':index}
 idx=dest/'Audit_individual_P01_R8.html';body=index_page(cfg).replace('</style>','*{box-sizing:border-box}body{overflow-wrap:anywhere}.table-scroll{max-width:100%;overflow-x:auto;overscroll-behavior-x:contain}.table-scroll table{width:100%;min-width:740px}@media(max-width:575px){body{padding:0 12px;margin:16px auto}.table-scroll td,.table-scroll th{padding:5px 7px}input{width:100%}}</style>').replace('<table><thead>','<div class="table-scroll" role="region" tabindex="0" aria-label="Lista taskurilor P01, derulare orizontală"><table><thead>').replace('</tbody></table>','</tbody></table></div>');idx.write_text(body,encoding='utf8');cfg['assets']={f:h(dest/f)for f in ['Dovezi_criterii.json','Registru_reexecutare_R8.json','Audit_individual_P01_R8.html']};wr(dest/'A12_raport.json',cfg);print('r8_build',shipped,h(dest/'A12_raport.json'),states['NEEXECUTAT'],dict(alloccounts),sum(map(len,rev.values())))
def index_page(r):
 rows=''.join('<tr><td><a href="'+safe(z['html'])+'">'+safe(z['task'])+'</a></td><td>'+safe(z['canonical'])+'</td><td>'+safe(z['title'])+'</td><td>'+safe(z['state'])+'</td><td>'+str(z['criteria'])+'</td><td>'+str(z['direct_criteria_this_round'])+'</td><td>'+str(z['historical_criteria_this_round'])+'</td><td>'+str(z['current_unexecuted'])+'</td></tr>'for z in r['records']);s=r['scope']
 return '<!doctype html><html lang="ro"><meta charset=UTF-8><meta name=viewport content="width=device-width, initial-scale=1"><title>Audit individual P01 · Ediția 8</title><style>body{font:16px/1.45 system-ui;margin:28px auto;padding:0 18px;max-width:1450px;color:#183248}table{border-collapse:collapse}td,th{padding:7px;border-bottom:1px solid #cfdbe3;text-align:left}thead{position:sticky;top:0;background:#f0f5f8}input{font:inherit;padding:.5em;max-width:100%;width:25em}small{color:#4a677b}a{color:#175989}</style><h1>Audit individual P01 · runda 8</h1><p>652 fișe, 2.619 criterii. Au rămas '+str(s['R8_NEEXECUTAT'])+' cu starea NEEXECUTAT. Evidența separă proba actuală, urma istorică, corecția metodologică și condiția încă nerealizată.</p><p><a href="Registru_reexecutare_R8.json">Registru complet</a> · <a href="Dovezi_criterii.json">Dovezi și legături inverse</a> · <a href="A12_raport.json">Raport și amprente</a> · <a href="Verificare_R8.json">Control intern al livrării</a></p><label>Găsește un task sau un capitol <input id=f type=search></label><p id=n>652 fișe</p><table><thead><tr><th>Fișă</th><th>ID P01</th><th>Titlu</th><th>Stare portal</th><th>Criterii</th><th>Probe R8</th><th>Istoric</th><th>Neexecutate</th></tr></thead><tbody>'+rows+'</tbody></table><script>let ff=document.querySelector("#f"),rr=Array.from(document.querySelectorAll("tbody tr"));ff.addEventListener("input",()=>{let s=ff.value.toLocaleLowerCase("ro"),n=0;for(let r of rr){r.hidden=!r.textContent.toLocaleLowerCase("ro").includes(s);if(!r.hidden)n++}document.querySelector("#n").textContent=n+" fișe"})</script></html>'
if __name__=='__main__':build(os.environ.get('A12_R8_PREVIEW')!='1')

