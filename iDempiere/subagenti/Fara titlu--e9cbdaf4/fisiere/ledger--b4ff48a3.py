from pathlib import Path
import hashlib,json,concurrent.futures,collections,base64,datetime
O=Path(__file__).parent;E=O.parent;R=E.parent;F=E/'R7';G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');P=E/'R7_pregatire/A12'
def rd(p):return json.loads(p.read_bytes())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1,default=str)+'\n',encoding='utf8')
def ptr(j,s):
 for k in s.lstrip('#/').split('/'):
  if k:k=k.replace('~1','/').replace('~0','~');j=j[int(k)] if isinstance(j,list)else j[k]
 return j
def cases(j):return j['operative_criteria_and_audit_criteria']+j['R3_new_criteria']+j['R4_new_criteria']
src={'A12_raport.json':'04c62ea2a020515ca6c20210eb450be343a56fd1dada2be253bb3b41297626ec','Verificare_R7.json':'82f8a425ff3991545414efa4fb31ab213bd1b2a56339d7f794030ea408b8528a','Dovezi_criterii.json':'5d293be29c6b96b83c04aa8e30fb0d9d9dd864dd455a29c38e981a9bf738321b','Registru_reexecutare_R7.json':'57b0417fe20d4a74e0c02e00970a6ed883ca4db43074044ed085d03305c1f821'}
for p,s in src.items():assert h(F/p)==s
j=rd(F/'A12_raport.json')
for p,s in j['inputs'].items():assert h(R/p)==s,p
for p,s in j['artifacts'].items():assert h(F/p)==s,p
r6={x['task']:x for x in rd(E/'A11_ledger_652_R6.json')['all_cases']};cl={x['criterion']:x for x in rd(P/'Clasificare_nominala_1587.json')['records']};reg={v['criterion']:v for v in rd(F/'Registru_reexecutare_R7.json')['records']};cat=rd(F/'Dovezi_criterii.json');ev=cat['evidence'];rev={(i,v['task'],v['criterion'],v['relation'])for i,ws in cat['inverse_task_requirement_links'].items()for v in ws};ob=rd(F/'probe/Rezultate_R7.json');assert len(reg)==1881
pred=rd(P/'148_predicate_prin_stack.json')['rows'];o6=rd(E/'R6_pregatire/A12/Oracole_487_EV5.json')
missing={v['r5_id']for v in o6['rows']if v['oracle_or_verified_locator']is None};assert missing=={v['evidence']for v in pred} and len(missing)==148
preds=collections.Counter();anchors=0;conditions=[]
for row in pred:
 c=row['comparison'];preds[c['code_state']]+=1;s=P/c['trace_log'];assert h(s)==c['log_sha']and h(G/c['test_source'])==c['test_source_sha']
 line=s.read_text(encoding='utf-8-sig',errors='replace').splitlines()[c['trace_line']-1];parts=line.strip().removeprefix('ANCHOR:').split('|');output=base64.b64decode(parts[0]).decode().strip();assert output==c['r7_actual'].strip();frames=[(int(t.split(':')[-2]),t.split(':')[-1])for t in parts[1:]if t];assert frames==[tuple(v)for v in c['stack_exact']]
 for aa in c['source_anchors']:
  g=G/aa['file'];assert h(g)==aa['sha'];ls=g.read_text(encoding='utf8').splitlines();a,b=aa['range'];ex='\n'.join(ls[a-1:b]);assert aa['source_condition'].strip()==ex.strip(),(row['evidence'],a,b);anchors+=1
 for child in c['child_assertions']:
  conditions.append((row['criterion'],row['evidence'],child))
sql=rd(P/'SQL/Matrice_SQL_reala_R7.json')['rows'];SQL=P/'SQL';roll=collections.Counter()
for x in sql:
 assert h(SQL/x['executed_sql'])==x['sql_sha'] and h(SQL/x['log'])==x['logsha'] and x['fixture_dropped'] and not x['errors']
 assert x['OK']+x['FAIL']==len(x['all_markers']);roll[(x['variant'], 'trials')]+=1;roll[(x['variant'],'OK')]+=x['OK'];roll[(x['variant'],'FAIL')]+=x['FAIL'];assert (x['FAIL']>0)==(x['variant']=='mutant')
cache={};levels=collections.Counter()
for i,v in ev.items():
 if not i.startswith('EV7-'):continue
 p=R/v['source']
 if p not in cache:assert h(p)==v['sha_or_oid'];cache[p]=rd(p)
 assert all(canon(ptr(cache[p],q['pointer']))==q['canonical_value_sha256']for q in v['strict_primary_locators']);levels[v['level']]+=1
qblocks={'T216-R2-002','T216-R2-005','T216-R2-006'};gcontext={'T354-R2-021','T354-R2-027'}
def one(t):
 k=t['task'];j7=rd(F/t['file']);prior=r6[k];a=cases(j7);b=prior['criteria']
 assert h(F/t['file'])==t['sha256']and h(F/t['html'])==t['html_sha256']and prior['sha_R6']==h(E/'R6'/t['file'])==t['R6_sha'];assert [c['id']for c in a]==[c['id']for c in b]
 html=(F/t['html']).read_text(encoding='utf8');edges=set();adjs=[];sc=set(prior['verified_subchecks'])
 for c,b6 in zip(a,b):
  i=c['id'];assert 'id="'+i+'"' in html;cur=c['current'];direct=c.get('R7_new_scenarios',[]);context=c.get('R7_context',[]);assert direct==ob['new'].get(i,[])and context==ob['context'].get(i,[])
  pairs=[(c['source_evidence_id'],'source')]+[(e,'authority')for e in c.get('authority_evidence_ids',[])]
  for kf in ['current','closure']:pairs.extend((e,kf)for e in c[kf]['evidence_ids'])
  for key,prop,role in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:pairs.extend((e,role)for e in(c.get(key)or{}).get(prop,[]))
  pairs.extend((e,'case_context')for e in c.get('strict_related_sources_R5',[]))
  for xs,role in ((c.get('R6_new_scenarios',[]),'R6_scenario'),(direct,'R7_scenario'),(context,'R7_context')):pairs.extend((x['evidence'],role)for x in xs)
  for e,role in pairs:assert e in ev;edges.add((e,t['task'],i,role))
  val='MENȚINE_LIMITA_ANTERIOARĂ'
  if direct:val='SUBCAZ_EVALUAT_ÎN_STRATUL_SURSEI';sc.add('QC09-R2')
  if context and not direct:val='CONTEXT_ACTUAL_FĂRĂ_CREDIT_NORMATIV'
  if i in qblocks:val='DEPENDENȚĂ_Q_EXCLUSĂ; FACTURAREA_SAU_AFISAREA_DUPĂ_VALIDARE_NEEXECUTATĂ'
  if i in gcontext:val='PROBA_NOUĂ_SEMANTIC_CONTEXT; DOVEZILE_R5/R6_SEPARATE'
  if i in ('T216-R2-001','T216-R2-007'):val='CONTRAEXEMPLU_ORIGINE_Q_LA_INGESTIE; NU_ABSENȚA_FUNCȚIEI_GENERALE'
  if i=='T354-R2-008':val='SUPORT_PENTRU_ATOMICITATE_GRUP; NU_SCENARIUL_EXACT_A10_B20/B7_SAU_PARAMETRUL_PARTIAL'
  if i=='T03-R2-039':val='3_SUB_5_RĂMÂNE; GARDĂ_JVM_LOCALĂ; PG_PE_CĂILE_CU_TRANZACȚIE'
  if i=='T06-R2-020':val='ACCEPT_REFUZ_SPECIFIC_CUI_ȘI_REPLAY_168_ÎN_FIXTURE';sc.add('QC07-R1')
  if i in reg:assert reg[i]['R7_state']==cur['status']and reg[i]['R6_state']==b6['state_R6'] and reg[i]['task']==t['task']
  classification=cl.get(i)
  if classification:
   assert b6['state_R6']=='NEEXECUTAT' and classification['task']==t['task'] and classification['source_row']['source_evidence_id']==c['source_evidence_id']
  adjs.append(dict(id=i,norm=c['normative_content'],R6=b6['state_R6'],R7=cur['status'],A11=val,classification=classification['category']if classification else None,partial_external=classification['has_partial_external']if classification else None,owner=reg[i]['owner']if i in reg else None,source=c['source_evidence_id'],direct=[dict(id=v['evidence'],layer=ev[v['evidence']]['level'],observed=v['observed'],expected=v['expected'],lim=v['qualification'])for v in direct],context=[v['evidence']for v in context],credits_prior=list(b6['current_EVs'])))
 assert sum(c['R7']=='NEEXECUTAT'for c in adjs)==t['unexecuted'];return dict(task=t['task'],canonical=t['canonical'],chapter=j7['chapter'],sha_R6=t['R6_sha'],sha_R7=t['sha256'],sha_HTML=t['html_sha256'],quality=round(len(sc)*.2,1),accepted_subchecks=sorted(sc),criteria=adjs),edges
with concurrent.futures.ThreadPoolExecutor(8)as ex:res=list(ex.map(one,j['records']))
rows=[a for a,b in res];fw=set().union(*(b for a,b in res));assert fw==rev and len(fw)==9639;allc=[(a,b)for a in rows for b in a['criteria']];assert set(cl)=={b['id']for a,b in allc if b['R6']=='NEEXECUTAT'}
def profile(aa):
 cc=[b for a,b in aa];return dict(task_count=len({a['task']for a,b in aa}),criterion_count=len(cc),current_unexecuted=sum(b['R7']=='NEEXECUTAT'for b in cc),prior_unexecuted=sum(b['R6']=='NEEXECUTAT'for b in cc),labeled_direct=sum(bool(b['direct'])for b in cc),labeled_context=sum(bool(b['context'])for b in cc),previous_unexecuted_moved=sum(b['R6']=='NEEXECUTAT'and b['R7']!='NEEXECUTAT'for b in cc),no_previous_external_among_still_open=sum(b['partial_external'] is False and b['R7']=='NEEXECUTAT'for b in cc),previous_partial_external_among_still_open=sum(b['partial_external'] is True and b['R7']=='NEEXECUTAT'for b in cc),q_and_g3_retyped=[b['id']for b in cc if b['id']in qblocks|gcontext])
stats=profile(allc);assert stats['criterion_count']==2619 and stats['current_unexecuted']==1517 and stats['labeled_direct']==118 and stats['previous_unexecuted_moved']==70
by={k:profile([(a,b)for a,b in allc if a['chapter']==k])for k in ('P01.C03','P01.C10')};states=collections.Counter(b['R7']for a,b in allc);n=collections.Counter((b['classification'],b['R7']=='NEEXECUTAT')for a,b in allc if b['classification']);extras={'continued_missing_in_same_class':{'|'.join((k,str(x))):v for (k,x),v in n.items()},'predicate_types':dict(preds),'source_anchors_for_148':anchors,'group_child_source_assertions':len(conditions),'trial_markers':{'|'.join(k):v for k,v in roll.items()},'sources_new_evidence':len(cache),'EV7_levels':dict(levels),'distinct_EV7':sum(levels.values()),'states':states}
p=E/'A11_ledger_652_R7.json';w(p,dict(scope='652 fișe păstrează fiecare cerință, clasificarea inițială R6, nivelul și dispoziția A11.',report_sha=src['A12_raport.json'],sym_edges=len(fw),orphan_edges=0,quality_10_cases=sum(a['quality']==10 for a in rows),records=rows,summary=stats));c03=E/'A11_dispozitii_C03_C10_R7.json';w(c03,dict(pinned_sha=src['A12_raport.json'],chapter_summary=by,all_chapter_rows=[a for a in rows if a['chapter']in by]));w(O/'readback_R7.json',dict(stats=stats,chapters=by,checks=extras,source_files=src));print(h(p),h(c03),stats,by,str(n))

