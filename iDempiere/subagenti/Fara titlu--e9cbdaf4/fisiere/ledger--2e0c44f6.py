from pathlib import Path
import hashlib,json,collections,concurrent.futures,datetime,re
O=Path(__file__).parent;E=O.parent;F=E/'R5';R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def hf(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fh(p):b=p.read_bytes();return hashlib.sha256(b).hexdigest(),json.loads(b.decode('utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1,default=str)+'\n',encoding='utf8')
hashes={'A12_raport.json':'ec00d36e6ee2eb4755981e22c0c332279b8319cb58080f535e6879de44de97cd','Verificare_R5.json':'c4512a932b0ce9679d42b9ed394b0f4c5fc6097d2854ad795aca838f044a6a8e','Dovezi_criterii.json':'c5fb6bfb8096575be0b39b852cf2e6a9c321d2e192899ab65a5bf5797528e27d','Registru_reexecutare_R5.json':'0960b117ae005eeafe193f9993d3579ccafb751392bd8f18ddb3389eecb085c4'}
for k,v in hashes.items():assert hf(F/k)==v
rep=rd(F/'A12_raport.json');old=rd(E/'A11_ledger_652_R4.json');prev={v['task']:v for v in old['cases']}; e=rd(F/'Dovezi_criterii.json'); catalog=e['evidence'];rev={(eid,w['task'],w['criterion'],w['relation'])for eid,edges in e['inverse_task_requirement_links'].items()for w in edges};allreg=rd(F/'Registru_reexecutare_R5.json'); reg={x['criterion']:x for x in allreg['records']}; physical=rd(F/'Protocol_exec.json');protos=physical.get('protocols')or physical
assert len(reg)==1881 and sum(x['original_1868'] for x in reg.values())==1868 and len(protos)>=1
for k,v in rep['sources'].items():assert hf(R/k)==v,k
for k,v in rep['artifact_hashes'].items():assert hf(F/k)==v,k
def cases(j):return j['operative_criteria_and_audit_criteria']+j['R3_new_criteria']+j['R4_new_criteria']
def check(t):
 q=t['task'];sha,j=fh(F/t['file']);sha4,j4=fh(E/'R4'/t['file']);assert sha==t['sha256'] and hf(F/t['html'])==t['html_sha256'] and t['R4_sha']==sha4==prev[q]['R4_hash'];ow={c['id']:c for c in cases(j4)};new=cases(j);assert [x['id']for x in new]==list(ow) and len(new)==t['criteria'];rawhtml=(F/t['html']).read_text(encoding='utf-8');assert rawhtml.count('<h1>')==1
 links=set();diff={};disps=[];new_ev={};score=set(prev[q]['verified_subchecks']);msum=0;sc=set();extcount=0;reg_in=0
 for c in new:
  id=c['id']; cc=c['current'];state=cc['status'];g=ow[id];linkpairs=[(c['source_evidence_id'],'source')]+[(x,'authority')for x in c.get('authority_evidence_ids',[])];assert c['source_evidence_id'] in catalog;assert 'id="'+id+'"' in rawhtml
  for ph in ('closure','current'):
   assert not c[ph].get('observed') or c[ph]['evidence_ids']
   linkpairs.extend((x,ph) for x in c[ph]['evidence_ids'])
  for field,prop,tag in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:linkpairs.extend((i,tag) for i in (c.get(field)or{}).get(prop,[]))
  linkpairs.extend((i,'case_context')for i in c.get('strict_related_sources_R5',[]))
  for eid,rel in linkpairs:assert eid in catalog;links.add((eid,q,id,rel))
  added=c.get('R5_measured_scenarios',[]);cat=next(x['A11_scope']for x in prev[q]['all_criteria'] if x['id']==id)
  decisions=[]
  for x in added:
   eid=x['evidence']; assert eid in cc['evidence_ids'] and eid.startswith('EV5-') and x['result'] and x['scope_limit'] and x['entry']
   eobj=catalog[eid];level=eobj['level'];sc.add(level)
   classif={'EXECUȚIE_COMPONENTĂ_ASERȚIUNE':'ASERȚIUNE_JVM_LIMITATĂ','SQL_PRODUS_PORTAT_POSTGRESQL':'SQL_EXECUTAT_PE_FIXTURE','FUNCȚIE_CU_ORACOL_INDEPENDENT':'VECTEUR_AȘTEPTAT_INDEPENDENT','SQL_CABINET_SINTETIC':'DB_FIXTURE_SEGMENT','MĂSURĂ_TEXT_PE_COD_FIXAT':'MĂSURĂ_DE_COD','REPRODUCERE_EXECUTOR_NOMINALĂ':'RELUARE_ÎN_ARIA_RAPORTULUI_SURSĂ','SIMULATOR_HTTP_LOOPBACK':'CONTRACT_HTTP_SIMULAT','ARBORE_GIT_ISTORIC':'DOVADĂ_DOCUMENTARĂ_GIT'}[level]
   decisions.append({'eid':eid,'level':level,'disposition':classif,'explicit_expected_in_scenario':bool(x.get('explicit_expected')),'entry':str(x['entry'])[:150],'result':str(x['result'])[:245]});new_ev[eid]=(q,id,level);msum+=1
  qualification='Fișa păstrează delimitarea R4.' if not added else 'Probe noi de segment; nu atestă rezultatul integral al criteriului dacă pași sau oracole lipsesc.'
  if added:
   cat='R5_SEGMENT_TIPAT';diff[id]=[g['current']['status'],state]
   if state=='ARBORE_ISTORIC_NOMINAL_VERIFICAT_ÎN_R5':cat='ATRIBUIRE_ISTORICĂ_NUMAI'
  if id=='T03-R2-039':cat='ABATERE_NUMERICĂ_LA_TESTUL_DE_COD';qualification='Primele 0 corespund. Apar numai 3 linii cu ocupaExclusiv în form/*.java, sub pragul explicit de 5. Defect al criteriului static după comanda declarată, nu dovadă de cursă în produs.'
  elif id=='T11-R2-023':qualification='0 ține de comanda secundă (catch urmat numai de gol), unde oracolul este 0. Fereastra 126–135 din prima comandă nu mai conține handlerul; log.fine este la 157. Control drift, nu dovadă de lipsă a jurnalului.'
  elif id=='T11-R2-008':qualification='Opt linii în outputul grep înseamnă rânduri găsite. Inspectați conținutul catch pentru log/așteptarea reală; volumul singur nu satisface criteriul.'
  elif id=='T190-R2-007':qualification='Criteriul cere 8 cazuri. Dovezile asociate acestei fișe arată perechea Text2000/255 pe două JAR-uri, unul din vectori; nu echivalați cu 2/8 sau 8/8.'
  elif id in ('T325-R2-016','T326-R2-039'):qualification='Atât FAIL pe prima variantă a harnessului, cât și OK la calibrare sunt păstrate pe Git/instalat. Nu le tratați drept două remedieri ale produsului; documentați cauza calibrării.'
  rr=reg.get(id);rs=None
  if rr:
   assert rr['task']==q and rr['R5_state']==state and rr['R4_state']==g['current']['status']  ,(id,rr['task'],q,rr['R5_state'],state,rr['R4_state'],g['current']['status'],rr['individual_next_step']);reg_in+=1;rs={'protocol':rr['protocol_ref'],'maturity':rr['maturity'],'missing':rr['missing_or_conditional'],'original_1868':rr['original_1868'],'resource':rr['resource_boundaries'].get('classification'),'external_part':rr['resource_boundaries'].get('requires_external_or_hardware'),'individual_next_step_empty':not bool(rr['individual_next_step']),'next':str(rr['individual_next_step'])[:310]};extcount+=bool(rs['external_part'])
  disps.append({'id':id,'state_R4':g['current']['status'],'state_R5':state,'closure_R5':c['closure']['status'],'A11_kind':cat,'qualifier':qualification,'evidence_R5':decisions,'evidence_ids_current':cc['evidence_ids'],'resource_if_registered':rs})
 assert t['new_observed']==len(diff) and t['unknown']==sum(x['state_R5']=='NEEXECUTAT' for x in disps)
 if diff:score.add('QC09-R2')
 if 'FUNCȚIE_CU_ORACOL_INDEPENDENT' in sc or 'SQL_PRODUS_PORTAT_POSTGRESQL' in sc:score.add('QC09-R1')
 if 'SQL_PRODUS_PORTAT_POSTGRESQL' in sc or 'SQL_CABINET_SINTETIC'in sc:score.add('QC05-R1')
 if q=='T03' and 'T03-R2-039' in diff:score.discard('QC10-R3')
 return {'task':q,'canonical':t['canonical'],'title':t['title'],'sha_R4':sha4,'sha_R5':sha,'sha_HTML_R5':t['html_sha256'],'quality_R4':prev[q]['R4_quality_score'],'quality_R5':len(score)/5,'earned_subchecks':sorted(score),'fully_quality_accepted':False,'current_full_positive_for_its_own_literal_functional_scope':q=='T259','criteria':disps,'changed_with_measurements':diff,'measurements':msum,'registered_actions':reg_in,'registered_external_portion':extcount},links,new_ev
with concurrent.futures.ThreadPoolExecutor(max_workers=7)as ex:res=list(ex.map(check,rep['records']))
rows=[x[0]for x in res];forward=set().union(*(x[1]for x in res));assert forward==rev and len(forward)==7762;current=collections.Counter();matures=collections.Counter();lev=collections.Counter();scen_dist=collections.Counter();meas_ids=[];all_eids=set(); ext_or=0; profiles=collections.Counter()
for row,_,ev5 in res:
 assert not all_eids & set(ev5);all_eids.update(ev5);meas_ids.extend(row['changed_with_measurements']);ext_or+=row['registered_external_portion'];profiles[str(row['quality_R5'])]+=1
 for eid,(_,id,level)in ev5.items():lev[level]+=1
 for d in row['criteria']:
  current[d['state_R5']]+=1
  if d['resource_if_registered']:matures[d['resource_if_registered']['maturity']]+=1
  for s in d['evidence_R5']:scen_dist[str(s['explicit_expected_in_scenario'])]+=1
assert len(rows)==652 and sum(current.values())==2619 and current['NEEXECUTAT']==1611 and len(meas_ids)==108 and len(set(meas_ids))==108 and len(all_eids)==487 and sum(matures.values())==1881
v={'reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'R5_report':hashes['A12_raport.json'],'R4_ledger':hf(E/'A11_ledger_652_R4.json'),'652_task_rows':len(rows),'total':sum(current.values()),'fwd_edges':len(forward),'inverse_edges':len(rev),'orphan_edges':len(forward^rev),'new_criteria_measured':len(set(meas_ids)),'new_EVs_adjudicated':len(all_eids),'evidence_level_counts':lev,'explicit_expected_per_new_scenario':scen_dist,'states':current,'maturity':matures,'actual_additional_external_in_1881':ext_or,'scores':profiles,'full_quality_10':0,'current_literal_business_case_positive':['T259'],'records':rows};f=E/'A11_ledger_652_R5.json';wr(f,v);print(hf(f),len(rows),len(meas_ids),current['NEEXECUTAT'],ext_or,dict(scen_dist),dict(profiles))

