from pathlib import Path
import json,hashlib,collections,datetime,concurrent.futures,gzip
O=Path(__file__).parent;E=O.parent;R=E.parent;F=E/'R6';G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');C=Path('D:/CodexWork/A12_evidence_20261102/blobs')
def rd(x):return json.loads(x.read_bytes())
def h(x):return hashlib.sha256(x).hexdigest()
def digest(p):return h(p.read_bytes())
def w(p,x):p.write_text(json.dumps(x,indent=1,ensure_ascii=False,default=str)+'\n',encoding='utf8')
def ptr(x,path):
 if not path:return x
 assert path.startswith('/')
 for t in path[1:].split('/'):
  t=t.replace('~1','/').replace('~0','~');x=x[int(t)] if isinstance(x,list) else x[t]
 return x
def canon(x):return h(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def cs(r):return r['operative_criteria_and_audit_criteria']+r['R3_new_criteria']+r['R4_new_criteria']
source={'A12_raport.json':'605241436af8ba8a4030bc127b81c993b36e4cc6ce06b119fd12ebbbdef03c09','Verificare_R6.json':'70d9f748e166f48801bf7725ace34a281f3ef8a25fcd3e528dc3b95a881d0988','Dovezi_criterii.json':'5cf6682e723e4b84fe2b49825b64c55041889e7e8fc705f8108baf8a565c02f7','Registru_reexecutare_R6.json':'9d1c1b578200af0d4d8e3d710909fee86f83b2b38dc4ea63d4cd9ade5ba84167'}
for p,v in source.items():assert digest(F/p)==v
rep=rd(F/'A12_raport.json')
for p,v in rep['inputs'].items():assert digest(R/p)==v,p
for p,v in rep['artifact_hashes'].items():assert digest(F/p)==v,p
old={x['task']:x for x in rd(E/'A11_ledger_652_R5.json')['records']};cat=rd(F/'Dovezi_criterii.json');ev=cat['evidence'];reg={x['criterion']:x for x in rd(F/'Registru_reexecutare_R6.json')['records']}; oldreg={x['criterion']:x for x in rd(E/'R5/Registru_reexecutare_R5.json')['records']};revedges={(eid,v['task'],v['criterion'],v['relation'])for eid,vs in cat['inverse_task_requirement_links'].items()for v in vs};assert len(reg)==1881
oracle=rd(E/'R6_pregatire/A12/Oracole_487_EV5.json')['rows']; positions={}
for a in oracle:
 q=a['oracle_or_verified_locator'];kind=a['numeric_basis'];i=a['r5_id'];assert i in ev and not a['permit_automatic_pass']
 if q and 'path'in q:
  p=next(x for x in (E/q['path'],G/q['path']) if x.is_file());assert digest(p)==q['sha'],p
  excerpt='\n'.join(p.read_text(encoding='utf8',errors='replace').splitlines()[q['start']-1:q['end']]);token=q['predicate_verbatim'].strip()
  if token not in excerpt and ' '.join(token.split()) not in ' '.join(excerpt.split()):positions[i]=[str(p),q['start'],token[:120],excerpt[:120]]
assert len(oracle)==487 and len({a['r5_id'] for a in oracle})==487
counts=collections.Counter();sourcecache={}
for i,x in ev.items():
 if not i.startswith('EV6-'):continue
 p=R/x['source'];data=sourcecache.setdefault(p,p.read_bytes());assert h(data)==x['sha_or_oid']
 for j in x['strict_primary_locators']:
  if j['kind']=='json-pointer':obs=ptr(json.loads(data),j['pointer']);assert canon(obs)==j['canonical_value_sha256'];counts['json']+=1
  else:assert h(data.decode('utf-8-sig',errors='replace').splitlines()[j['line']-1].encode())==j['line_sha256'];counts['line']+=1
contrast={x['criterion']:x for x in rd(E/'R6_pregatire/A12/Contraste_108_R5.json')['records']};assert len(contrast)==108
detail=rd(F/'probe/Cazuri_noi.json')['rows'];assert len(detail)==32
records81={x['criterion']:x for x in rd(E/'R6_pregatire/A12/Actiuni_81_reconstituite.json')['records']};assert set(records81)=={i for i,v in oldreg.items() if not v['individual_next_step']};assert all(reg[i]['R6_case_next_action'] for i in records81)
ann=rd(F/'probe/Anexe_1611_pentru_fisa.json')['records'];ann_rows=0;unique_ann=set()
for a in ann:
 for link in a['historical_controls']:
  path=G/link['file'];oid=link['blob_oid'];bp=next((z/(oid+'.gz') for z in (C,Path('D:/CodexWork/p01-r6-annex')) if (z/(oid+'.gz')).is_file()),None);b=gzip.decompress(bp.read_bytes()) if bp else path.read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
  line=b.decode('utf-8-sig',errors='replace').splitlines()[link['line']-1];assert h(line.encode())==link['line_text_sha256'];ann_rows+=1;unique_ann.add(oid)
def case(a):
 t=a['task'];base=old[t];j=rd(F/a['file']);assert digest(F/a['file'])==a['sha256'] and digest(F/a['html'])==a['html_sha256'] and digest(E/'R5'/a['file'])==base['sha_R5']==a['R5_source_sha']
 html=(F/a['html']).read_text(encoding='utf8');cases=cs(j);assert len(cases)==a['criteria'] and [x['id']for x in cases]==[x['id']for x in base['criteria']]
 edges=set();out=[];credits=set(base['earned_subchecks']); nc=0
 for c,v in zip(cases,base['criteria']):
  i=c['id'];state=c['current']['status'];assert 'id="'+i+'"' in html
  pairs=[(c['source_evidence_id'],'source')]+[(e,'authority') for e in c.get('authority_evidence_ids',[])]
  for k in ('current','closure'):pairs.extend((e,k)for e in c[k]['evidence_ids'])
  for field,prop,name in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:pairs.extend((e,name)for e in(c.get(field)or{}).get(prop,[]))
  pairs.extend((e,'case_context') for e in c.get('strict_related_sources_R5',[]))
  scs=c.get('R6_new_scenarios',[]);assert scs==detail.get(i,[])
  pairs.extend((x['evidence'],'R6_scenario') for x in scs)
  for eid,k in pairs: assert eid in ev;edges.add((eid,t,i,k))
  originalarea=v['A11_kind'];evaluation='DELIMITARE_R5_PĂSTRATĂ'
  if i in contrast and not scs:evaluation='CONFRUNTARE_NOMINALĂ_R5'
  if scs:evaluation='SEGMENT_DOVEDIT_SAU_CONTEXT_DELIMITAT';nc+=1
  if i=='T03-R2-039':evaluation='PRAG_STATIC_RESPINS_3_SUB_5; GARDĂ_LOCALĂ_JVM_CONFIRMATĂ';credits.add('QC10-R3')
  if i=='T06-R2-020':evaluation='PRECONDIȚIE_FIRMĂ_FĂRĂ_CUI; A NU CONFUNDA CU DOVADA REFUZULUI CUI_DIFERIT'
  if i=='T190-R2-007':evaluation='ACCEPTAT_CURENT_C4_8_VECTORI_DISTINCȚI_AMBELE_JAR';credits.add('QC09-R4')
  if i in ('T110-R3-001','T111-R3-001'):evaluation='COMPARAȚIE_DOCUMENTARĂ; DISPĂRUTĂ/INCOMPLETĂ UNELE EXPLICAȚII; NU E EXECUȚIE ERP'
  if scs and any(x['layer'].startswith(('PROCES_NATIV','SQL_TEST','GUARDĂ_'))for x in scs):credits.add('QC09-R1')
  if i in reg:
   g=reg[i]; assert g['R6_state']==state and g['R5_state_immutable']==v['state_R5'];res=g['resource_boundaries'];action=g['R6_case_next_action']
  else:g=None;res=None;action=None
  out.append({'id':i,'state_R5':v['state_R5'],'state_R6':state,'closure_R6':c['closure']['status'],'dispozitie_A11':evaluation,'previous_A11_kind':originalarea,'raw_scope':c['normative_content'][:150],'current_EVs':c['current']['evidence_ids'],'EV5_comparison':contrast[i]['assessment_R6_by_case'] if i in contrast else None,'new_scenarios':[{k:x.get(k) for k in ('evidence','layer','asserted_expected','result','remaining_scope')} for x in scs],'external_part':res.get('requires_external_or_hardware')if res else None,'owner_if_registered':g['owner'] if g else None,'action_exists':bool(action) if g else None})
 assert sum(x['state_R6']=='NEEXECUTAT' for x in out)==a['unexecuted'],t
 return dict(task=t,canonical=a['canonical'],title=a['title'],sha_R5=base['sha_R5'],sha_R6=a['sha256'],sha_html=a['html_sha256'],verified_subchecks=sorted(credits),R6_case_quality=round(len(credits)*0.2,1),decision='RELUARE_CU_PROBELE_NOMINALE_PĂSTRATE',criteria=out),edges
with concurrent.futures.ThreadPoolExecutor(8) as ex: result=list(ex.map(case,rep['records']))
rows=[x[0]for x in result];forward=set().union(*(x[1]for x in result));assert forward==revedges,(len(forward),len(revedges),list((forward^revedges))[:10])
states=collections.Counter(x['state_R6']for q in rows for x in q['criteria']);changes=collections.Counter((x['state_R5'],x['state_R6']) for q in rows for x in q['criteria'] if x['state_R6']!=x['state_R5'])
assert len(rows)==652 and sum(states.values())==2619 and states['NEEXECUTAT']==1587
stats={'annex_actual_source_line_occurrences':ann_rows,'annex_distinct_source_blobs':len(unique_ann),'annex_coverage':sum(bool(x['historical_controls'])for x in ann),'EV6_strict':counts,'distinct_EV6':sum(i.startswith('EV6')for i in ev),'source_predicate_locator_discrepancies':positions,'report_inputs_hash':len(rep['inputs']),'contrast':108,'actions_resolved':81,'oracle_number':len(oracle),'oracle_distribution':dict(collections.Counter(x['numeric_basis']for x in oracle)),'states':states,'actual_remaining_resource':str(collections.Counter((x['resource_boundaries'].get('requires_external_or_hardware'),x['original_1868'])for x in reg.values()if x['R6_state']=='NEEXECUTAT')),'delta':{'|'.join(k):v for k,v in changes.items()},'sources_sha256':source,'directions':len(forward),'sum_rows':sum(a['criteria'] for a in rep['records'])}
w(O/'strict_R6.json',stats);p=E/'A11_ledger_652_R6.json';w(p,{'reviewer':'A11','source':source['A12_raport.json'],'review_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'denominator':652,'criteria':2619,'symmetric_edges':len(forward),'new_case_count':len(detail),'new_scenario_claims':sum(map(len,detail.values())),'quality_10_tasks':sum(x['R6_case_quality']==10 for x in rows),'quality_scores_are_not_product_scores':True,'all_cases':rows});print(digest(p),str({k:v for k,v in stats.items() if k not in ['states','delta','sources_sha256','source_predicate_locator_discrepancies']}),list(positions)[:5],len(positions))

