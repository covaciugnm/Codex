from a12_r6_dataset import *
from urllib.parse import quote
from collections import Counter
res13={
'T02.10':(False,'Registrul istoric, avizul revizorului și statusul validării sunt căutabile în materialele interne; o revizie actuală nu reproduce semnătura de atunci.'),
'T07.02':(False,'Ramura nominală, routerele de pornire/import și simulatorul de provisioning se testează local.'),
'T12.01':(True,'Amprentele și adresele exemplarelor istorice sunt locale când există în arhivă; confirmarea ediției direct la autoritatea emitentă necesită acces la documentul oficial.'),
'T17.02':(False,'Excluderea commitului și concurența pe fluxul simulat sunt verificări locale. Gărzii mock nu i se cere partener real.'),
'T18.01':(False,'Tabelul exact, cinci stări per firmă și tranzacția se verifică în clona ERP.'),
'T18.02':(False,'Lunile închise și prima deschisă sunt din procesele native și perioada synthetic GardenWorld.'),
'T18.03':(False,'SAGA poate fi un fișier sintetic cu referințe reconciliate în ERP; nu cere serviciu fiscal real.'),
'T18.07':(False,'env-file și simulatorul SPV cu UBL sintetic sunt sub controlul laboratorului.'),
'T27.36':(False,'Harta, clasele și forma sunt interne. Aici nu se acceptă validatoare ANAF reale ca precondiție pentru afişarea locală.'),
'T36.15':(False,'Remedierea a șase ID-uri și probele din buton se verifică prin ZK cu două conturi de laborator; rămâne necesară o probă nominală.'),
'T36.16':(False,'Rândurile istorice L9 și patru unelte de test se pot reproduce intern.'),
'T36.66':(False,'Guardul UI poate fi exercitat pe o copie de surse cu un literal nou și unul permis.'),
'T40.14':(False,'Firme și scheme locale permit testarea FIFO/LIFO/CMP și importul TIP_DESC.')}
reg5=rd(R5/'Registru_reexecutare_R5.json')['records'];regmap={z['criterion']:z for z in reg5};q=[];act=rd(aux/'Actiuni_81_reconstituite.json');actm={x['criterion']:x for x in act['records']};ii={x['criterion']:i for i,x in enumerate(reg5)}
def allc(w):return sum([w[k]for k in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def links(c):
 v=[(c['source_evidence_id'],'source')]+[(z,'authority')for z in c.get('authority_evidence_ids',[])]
 for f in ['current','closure']:v.extend((z,f)for z in c[f]['evidence_ids'])
 for f,key,rel in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:v.extend((z,rel)for z in c.get(f,{}).get(key,[]))
 v.extend((z,'case_context')for z in c.get('strict_related_sources_R5',[]))
 v.extend((z['evidence'],'R6_scenario')for z in c.get('R6_new_scenarios',[]));return set(v)
def eh(v):return html.escape(str(v if v is not None else '—'))
def strv(v):return v if isinstance(v,str)else json.dumps(v,ensure_ascii=False)
def label(q):return eh(strv(q))
def page(w,checks):
 cs=[]
 for c in checks:
  cid=c['id'];old=c.get('R6_numerical_R5_review')or {};new=c['R6_new_scenarios'];sr=regmap.get(cid);sn=sr.get('individual_next_step')if sr else c.get('next_action');acts=sr.get('R6_case_next_action') if sr else None
  ls=''.join('<li><b>'+eh(z['layer'])+'</b> · '+eh(z['asserted_expected'])+'<br>'+label(z['measured'])+'<br><small>'+eh(z['remaining_scope'])+' · '+eh(z['evidence'])+'</small></li>'for z in new)
  cs.append('<section id="'+eh(cid)+'"><h2>'+eh(cid)+'</h2><p>'+eh(c['normative_content'])+'</p><dl><dt>În R6</dt><dd>'+eh(c['current']['status'])+'</dd><dt>La închidere</dt><dd>'+eh(c['closure']['status'])+'</dd><dt>Ce s-a observat</dt><dd>'+label(c['current'].get('observed'))+'</dd><dt>Comparație numerică pentru probele din R5</dt><dd>'+label(old.get('assessment_R6_by_case'))+'</dd><dt>Ce mai trebuie verificat și de cine</dt><dd>'+label(acts or sn)+'</dd></dl>'+('<ol>'+ls+'</ol>'if ls else '')+'</section>')
 style='body{font:16px/1.5 system-ui;max-width:1000px;margin:32px auto;padding:0 20px;color:#213649}h2{font-size:1.2rem}section{border-top:1px solid #ccc}dt{font-weight:650}dd{margin:0 0 10px;overflow-wrap:anywhere}small{color:#536779}'
 return '<!doctype html><html lang="ro"><meta charset="utf-8"><style>'+style+'</style><title>'+eh(w['task'])+' · Audit R6</title><body><nav><a href="../Audit_individual_P01_R6.html">Înapoi la index</a> · <a href="../taskuri/Fisa_'+quote(w['task'])+'.json">Date și referințe</a></nav><h1>'+eh(w['task'])+' · '+eh(w['title'])+'</h1><p>'+eh(w['canonical'])+' · '+eh(w['state_at_new_capture'])+' · '+str(len(checks))+' criterii. Avizul A11 pentru această rundă este în așteptare.</p>'+''.join(cs)+'</body></html>'
def recase(rr):
 f=R5/rr['file'];w=rd(f);assert sh(f)==rr['sha256'];checklist=allc(w);w['schema']='A12_R6';w['source_R5_immutable']={'sha256':rr['sha256'],'relative':f.relative_to(B).as_posix(),'quality_A11':5.6}
 for c in checklist:
  cid=c['id'];prev=c['current'].copy();ex=cases.get(cid,[]);c['R6_new_scenarios']=ex
  if cid in contr:
   i,ck=contr[cid];c['R6_numerical_R5_review']={'source':comparison.relative_to(B).as_posix(),'sha256':sh(comparison),'pointer':'/records/'+str(i),'assessment_R6_by_case':ck['assessment_R6_by_case'],'source_case_count_if_measured':ck['source_case_count_if_measured'],'repetition_per_target_is_not_new_business_case':True}
   for x in c['R5_measured_scenarios']:
    i,o=om[x['evidence']]; x['R6_oracle_ref']={'file':OR.relative_to(B).as_posix(),'sha':sh(OR),'pointer':'/rows/'+str(i),'numeric_basis':o['numeric_basis']};x['R6_automatic_credit']=False
  if ex or cid in contr:c['before_R6_current']=prev
  if ex:
   ck=[z for z in ex if z['closure_phase']];new=[z for z in ex if not z['closure_phase']]
   if ck:
    c['R5_closure_preserved']=c['closure'].copy();c['closure']={'status':'PROBĂ_DOCUMENTARĂ_NOMINALĂ_R6','observed':' | '.join(strv(z['measured'])for z in ck),'evidence_ids':list(dict.fromkeys([*c['closure']['evidence_ids'],*(z['evidence']for z in ck)])),'blocking_reason':ck[0]['remaining_scope']}
   if all(z['layer'] in ['DOCUMENT_PRIMARY','REGISTRU_ISTORIC']for z in ex):state='DOCUMENTAR_R6_DOMENIU_VERIFICAT'
   elif all(z['result']in ['SONDĂ_DICTȚIONAR','CONTEXT_NATIV']for z in ex):state='R6_CONTEXTE_NATIVE_FĂRĂ_TESTUL_INTEGRAL'
   elif cid=='T03-R2-039':state='ABATERE_STATICĂ_3_DIN_MINIM_5_GARDĂ_CONCURENTĂ_OBSERVATĂ'
   elif cid=='T06-R2-020':state='PRECONDIȚIE_CUI_CLIENT_NESATISFĂCUTĂ'
   elif cid=='T163-R2-029':state='DIFERENȚĂ_ÎNTRE_JAR_GIT_ȘI_INSTALAT_REPRODUSĂ'
   elif cid=='T190-R2-007':state='CERINȚĂ_UNITARĂ_8_DIN_8_REPRODUSĂ_PE_AMBELE_JAR'
   else:state='R6_SUBCAZ_EXERCITAT_LIMITE_NOMINALE'
   ids=list(dict.fromkeys([*prev['evidence_ids'],*(it['evidence']for it in ex)]));c['current']={'status':state,'observed':' | '.join(strv(z['measured'])for z in ex[:2])+' · '+str(len(ex))+' probe nominale în R6. '+(c.get('R6_numerical_R5_review',{}).get('assessment_R6_by_case')or''),'evidence_ids':ids,'blocking_reason':' '.join(dict.fromkeys(z['remaining_scope'] for z in ex))}
  elif cid in contr:
   zk=contr[cid][1];c['current']['observed']=(prev.get('observed')or'')+' | Reevaluare R6: '+zk['assessment_R6_by_case']
   scoped=[om[z['evidence']][1]['numeric_basis']for z in c['R5_measured_scenarios']]
   if scoped and all(x.startswith('CONDIȚIE_DE_TEST_NERECUPERATĂ')for x in scoped) and prev['status']=='PROBĂ_PARȚIALĂ_R5_COMPONENTĂ':
    c['current']['status']='OBSERVAT_FĂRĂ_PREDICAT_NOMINAL_RECUPERAT';c['current']['blocking_reason']='Recuperează predicatul și intrările din testul nominal înaintea oricărui verdict de conformitate.'
   elif cid in ['T216-R2-008','T216-R2-009']:c['current']['status']='CONTRAEXEMPLU_COMERCIAL_ÎN_ARIA_MĂSURATĂ'
   elif cid in ['T329-R2-017','T330-R2-002','T330-R2-011','T330-R2-013','T354-R2-016','T314-R2-005']:c['current']['status']='INCONCLUDENT_PRECONDIȚIE_SAU_BAZĂ_DE_COMPARAȚIE_ABSENTĂ'
  if cid in regmap:
   a=regmap[cid];src=a['entry_and_oracle_specific_to_case'];a['R5_state_immutable']=a['R5_state'];a['R6_state']=c['current']['status'];a['R6_new_scenarios']=[z['evidence']for z in ex];ax=ar.get(cid)
   if ax:
    ix,ann=ax;a['R6_archive_review']={'verified_source':(R/'probe/Anexe_1611_pentru_fisa.json').relative_to(B).as_posix(),'pointer':'/records/'+str(ix),'artifacts_matching':len(ann['historical_controls']),'outcome':ann['search_result'],'no_runtime_credit':True}
   if a['resource_boundaries']['requires_external_or_hardware']is None:
    ext,reason=res13[w['task']];a['resource_boundaries']={'classification':'INTERN_CU_DEPENDENȚĂ_DE_AUTORITATE_DOCUMENTARĂ'if ext else'INTERN_SAU_ARHIVĂ','requires_external_or_hardware':ext,'specific_boundary':reason}
   if cid in actm:
    a['R6_case_next_action']=dict(actm[cid],actor=src.get('roles_or_interfaces_named_in_source')or'Rol operațional încă nenomit în această sursă; titularul de verificare este '+a['owner'])
    a['individual_next_step']=a['R6_case_next_action'];a['R5_next_step_was_empty']=True
   else:a['R6_case_next_action']=a['individual_next_step']
   if ex:a['R6_case_next_action']={'probe_done':[{'evidence':v['evidence'],'remaining':v['remaining_scope']}for v in ex[:2]],'owner':a['owner'],'exact_scope_still_needed':c['normative_content'],'recorded_initial_state':src.get('environment_or_legacy_baseline'),'see_prior':a['individual_next_step']}
   a['decision_owner_and_open_input']={'owner':a['owner'],'historical_criterion':c['normative_content'],'starting_parameters':src.get('fixture_literals_verbatim')or src.get('environment_or_legacy_baseline'),'source_pointer':src['source_pointer_original'],'missing_data':a['missing_or_conditional'],'holder_of_missing_business_decision':'Autorul cerinței sau responsabilul funcțional al capitolului, când în sursa nominală lipsește un etalon.'}
   c['R6_register_position']={'file':'Registru_reexecutare_R6.json','pointer':'/records/'+str(ii[cid]),'external_part_only':a['resource_boundaries']['requires_external_or_hardware']}
   if c['current']['status']=='NEEXECUTAT':c['current']['blocking_reason']='Caz '+cid+' · '+strv(a['R6_case_next_action'])[:960]
  for eid,phase in links(c):
   assert eid in ev,(cid,eid);reverse[eid].append({'task':w['task'],'criterion':cid,'relation':phase})
 w['R6_summary']={'score':None,'R5_reviewed':list(c['id']for c in checklist if c['id']in contr),'new_trials':list(c['id']for c in checklist if c.get('R6_new_scenarios')),'unexecuted':list(c['id']for c in checklist if c['current']['status']=='NEEXECUTAT'),'not_certified_separate_from_unexecuted':list(c['id']for c in checklist if c['current']['status'] in ['INCONCLUDENT_PRECONDIȚIE_SAU_BAZĂ_DE_COMPARAȚIE_ABSENTĂ','OBSERVAT_FĂRĂ_PREDICAT_NOMINAL_RECUPERAT','PRECONDIȚIE_CUI_CLIENT_NESATISFĂCUTĂ','R6_CONTEXTE_NATIVE_FĂRĂ_TESTUL_INTEGRAL'])}
 return w,rr
def go():
 work=[recase(z)for z in parent['records']]
 def save(t):
  w,rr=t;out=R/rr['file'];hp=R/rr['html'];wr(out,w);hp.write_text(page(w,allc(w)),encoding='utf8')
  return {'task':w['task'],'canonical':w['canonical'],'title':w['title'],'state':rr['state'],'file':rr['file'],'html':rr['html'],'sha256':sha(out),'html_sha256':sha(hp),'R5_source_sha':rr['sha256'],'criteria':rr['criteria'],'new_observed_R6':len(w['R6_summary']['new_trials']),'unexecuted':len(w['R6_summary']['unexecuted'])}
 with ThreadPoolExecutor(max_workers=10)as pool:records=list(pool.map(save,work))
 assert len(records)==652 and len({r['task']for r in records})==652
 wr(R/'Dovezi_criterii.json',{'schema':'A12_R6','prior_R5_sha':sh(R5/'Dovezi_criterii.json'),'evidence':ev,'inverse_task_requirement_links':dict(reverse)})
 wr(R/'Registru_reexecutare_R6.json',{'schema':'A12.R6','original':1868,'additional':13,'register_items':len(reg5),'sources':{'R5':sh(R5/'Registru_reexecutare_R5.json'),'81_refilled':sh(aux/'Actiuni_81_reconstituite.json'),'108_reviewed':sh(comparison),'487_checked':sh(OR),'archival_search':sh(an)},'records':reg5})
 tx=''.join('<tr><td><a href="'+eh(x['html'])+'">'+eh(x['task'])+'</a></td><td>'+eh(x['canonical'])+'</td><td>'+eh(x['title'])+'</td><td>'+eh(x['state'])+'</td><td>'+eh(x['criteria'])+'</td><td>'+eh(x['new_observed_R6'])+'</td><td>'+eh(x['unexecuted'])+'</td></tr>' for x in records)
 stat=Counter(c['current']['status']for w,_ in work for c in allc(w))
 htmlstr='<!doctype html><html lang="ro"><meta charset="utf-8"><style>body{font:16px/1.45 system-ui;max-width:1450px;margin:24px auto;padding:0 20px;color:#234}th,td{text-align:left;padding:5px;border-bottom:1px solid #ccc}th{position:sticky;top:0;background:#edf4fa}</style><title>Audit P01 · R6</title><h1>Audit individual P01 · runda 6</h1><p>652 taskuri și '+str(sum(stat.values()))+' criterii. '+str(stat['NEEXECUTAT'])+' criterii nu au o execuție individuală. Există separat rezultate neconcludente, măsurări de componentă și condiții care nu au fost îndeplinite. Nota A11 este în așteptare.</p><p><a href="A12_raport.json">Raport</a> · <a href="Registru_reexecutare_R6.json">Registrul de reexecuție</a> · <a href="Dovezi_criterii.json">Dovezi și relații</a></p><table><tr><th>Task</th><th>Identitate</th><th>Obiectiv</th><th>Stare</th><th>Criterii</th><th>Probe R6</th><th>Neexecutat</th></tr>'+tx+'</table></html>'
 (R/'Audit_individual_P01_R6.html').write_text(htmlstr,encoding='utf8')
 pdeps={p for p in [E/'A11_control_A12_R5.json',R5/'A12_raport.json',OR,comparison,an,hp,hp2,Prep/'Istoric/Manifest_Istoric.json',Prep/'Marcaje_JVM_SQL.json',native,aux/'Actiuni_81_reconstituite.json',*sorted(aux.glob('*.json'))]if p.is_file()};pdeps.update(B/v['source']for i,v in ev.items()if i.startswith('EV6-'))
 ex=Counter(z['technical_owner'] if 'technical_owner'in z else z['owner'] for z in reg5 if z['R6_state']=='NEEXECUTAT')
 counts={'tasks':652,'criteria':sum(stat.values()),'old_R5_neexecutat':1611,'new_R6_NEEXECUTAT':stat['NEEXECUTAT'],'new_obs':sum(len(v)for v in cases.values()),'individual_new_criteria':len(cases),'EV6':sum(z.startswith('EV6-')for z in ev),'reviews_previous_108':len(contr),'487_EV5_oracle_categories':Counter(o['numeric_basis']for o in orows),'remaining_by_owner':ex,'scope_13':{k:v[0]for k,v in res13.items()},'81_empty_actions_resolved':sum(bool(z.get('R5_next_step_was_empty'))for z in reg5),'remaining_external_or_hardware_or_authority_in_part':sum(bool(z['resource_boundaries']['requires_external_or_hardware']) for z in reg5 if z['R6_state']=='NEEXECUTAT'),'additional_13_now_unexecuted':sum(z['R6_state']=='NEEXECUTAT'and not z['original_1868']for z in reg5),'resolved_historical_upper_bound_only':2,'raw_states':stat,'edges':sum(map(len,reverse.values())),'context_or_observation_without_dispositive_support_distinct':sum(v for k,v in stat.items()if k in ['INCONCLUDENT_PRECONDIȚIE_SAU_BAZĂ_DE_COMPARAȚIE_ABSENTĂ','OBSERVAT_FĂRĂ_PREDICAT_NOMINAL_RECUPERAT','PRECONDIȚIE_CUI_CLIENT_NESATISFĂCUTĂ','R6_CONTEXTE_NATIVE_FĂRĂ_TESTUL_INTEGRAL'])}
 report={'schema':'A12_P01_R6','published_utc':datetime.now(UTC).isoformat(),'cutoff_git':shaGit,'independent_score_R6':None,'A11_review_R5':5.6,'status':'PROPUS_SPRE_CONTROL_A11','score_functional_automated':None,'counts':counts,'notes':['Analizele vizuale și NIR au o stare publicată separat. R6 folosește doar materialele nominale sigilate în lista de mai jos.','Pentru cele 410 probe R5 fără expected propriu există un predicat al testului, o regulă de domeniu sau un refuz explicit de a atribui conformitatea. Un rând de probă nu este un scenariu comercial distinct.','La T06 au fost lansate independent procese reale, cu AD_PInstance. CUI absent al GardenWorld nu exercită etapa arhivei cu CUI diferit; zero rânduri în fixture este distinct de 168 în scenariul istoric.','T03 are o diferență statică 3<5. În martor separat, pe ambele JAR, două tranzacții și două fire au avut un singur câștigător. Baza-locală de probă a fost eliminată. T337 nu primește credit pentru lanțul nativ cu opțiunea dezactivată.','Potrivirea cu anexele istorice nu furnizează automat un prag independent al cerinței sau status actual. Candidaturile au fost recitite la liniile și bloburile exacte.','Dacă 148 de condiții de test nu au putut fi localizate, observația individuală nu primește credit numeric; catalogul păstrează atât rândul cât și limitele.'], 'inputs':{p.relative_to(B).as_posix():sh(p)for p in sorted(pdeps)},'artifact_hashes':{k:sha(R/k)for k in ['Audit_individual_P01_R6.html','Dovezi_criterii.json','Registru_reexecutare_R6.json','probe/Anexe_1611_pentru_fisa.json','probe/Cazuri_noi.json']},'records':records};wr(R/'A12_raport.json',report);print('report',sha(R/'A12_raport.json'),'new',counts['new_obs'],'unexec',stat['NEEXECUTAT'],'edges',counts['edges'])
if __name__=='__main__':go()

