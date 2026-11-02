import pathlib,json,hashlib,collections,datetime,re
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); E=R/'executie';D=E/'R2'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rep=rd(D/'A12_raport.json'); catalog=rd(D/'Dovezi_criterii.json'); ev=catalog['evidence']; inv=catalog['inverse_task_requirement_links'];R1={x['source_id']:x for x in rd(E/'A11_ledger_651_fise.json')['records']}; rub=rd(R/'A11_rubrica_control.json')
assert h(D/'A12_raport.json')=='f991fd378d7fe2dec3525e3ca7b948871974e42d95fd98db8cb7147c7a5ac925' and h(D/'Dovezi_criterii.json')=='e8b9cc9d71842950e04f96947649681dbf479e99a30e33dccad83b5b13852376'
norm=lambda t: str(t).strip().upper()
keys=set(R1);reportids={x['task'] for x in rep['records']};assert keys==reportids and len(keys)==len(rep['records'])==651
forward=set();reverse={(eid,w['task'],w['criterion'],w['relation']) for eid,li in inv.items() for w in li};results=[]; kinds=collections.Counter(); stat=collections.Counter(); generic=collections.Counter(); issues=collections.Counter(); shards=collections.Counter()
for rr in rep['records']:
 tid=rr['task']; prev=R1[tid];j=rd(D/rr['file']);old=j['r1_immutable']; checks={};errors=[]; ct=j['operative_criteria_and_audit_criteria']; rows=[]; codes=set(); found=[]
 checks['r2_file_hash']=h(D/rr['file'])==rr['sha256'];checks['r1_archive_hash']=h(D/'taskuri'/old['path'])==rr['R1_sha256']==old['sha256']==prev['sha256']; checks['task_identity']=j['task']==tid and j['canonical']==prev['canonical']; checks['separate_time_decisions']=bool(j['decision_at_closure'] and j['decision_current'])
 checks['all_36_controls']=len(j['control_register_R2'])==36; checks['no_metadata_in_criteria']=all(x['kind'] not in ['METADATA_NU_CRITERIU','DESCRIERE_DECLARATA_NU_DOVADA'] for x in ct); checks['r1_fragments_preserved']=len(j['r1_fragments_reclassified'])==prev['original_requirement_fragments']; checks['criteria_expected_and_source']=all(c.get('actor_or_role') and c.get('preconditions') and c.get('expected_oracle') and c.get('source_evidence_id') in ev for c in ct)
 for c in ct:
  assert c['id'] not in codes;codes.add(c['id']); kind=c['kind']; kinds[kind]+=1; current=c['current']; status=current['status']; stat[status]+=1
  links=[('source',c['source_evidence_id'])]+[('authority',i) for i in c.get('authority_evidence_ids',[])]
  for mode in ['closure','current']:
   cm=c[mode]; links.extend((mode,i) for i in cm['evidence_ids'])
   if not cm['observed'] and not cm.get('blocking_reason'):errors.append(c['id']+': '+mode+' fără observed/limit')
   if ('PASS' in cm['status'] or 'FAIL' in cm['status']) and (not cm['observed'] or not cm['evidence_ids']):errors.append(c['id']+': verdict fără probă')
  for rel,i in links:
   if i not in ev:errors.append(c['id']+': dangling '+i)
   forward.add((i,tid,c['id'],rel))
  if c['source_evidence_id'] and not c['normative_content']:errors.append(c['id']+': text normativ lipsă')
  if 'PASS' in status:bucket='DOCUMENTAR_ARTEFACT' if kind=='CONTROL_DISPOZIȚIE_REFERINȚE' else 'DOCUMENTAR_ADMIN' if kind=='DISPOZIȚIE_ADMINISTRATIVĂ' else 'REVERIFICAȚI_PASS_FUNCȚIONAL'
  elif 'FAIL' in status:bucket='DEFECT_COMPONENTĂ' if 'COMPONENTĂ' in status else 'CONTRADICȚIE_REGISTRU'
  elif status=='NEEXECUTAT': bucket='NEEXECUTAT'
  elif 'BLOCAT' in status:bucket='BLOCAT'
  else:bucket='NECONCLUDENT_SEGMENT' if current.get('observed') else 'NECONCLUDENT'
  shards[bucket]+=1; generic[c.get('next_action','')]+=1
  if current.get('observed'):found.append(c['id'])
  rows.append({'id':c['id'],'kind':kind,'source_id':c['source_evidence_id'],'current_status':status,'closure_status':c['closure']['status'],'A11_classification':bucket,'current_evidence_ids':current['evidence_ids'],'closure_evidence_ids':c['closure']['evidence_ids']})
 relevant=[x for x in ct if x['kind'] not in ('DISPOZIȚIE_ADMINISTRATIVĂ','CONTROL_TRANSFER_OBLIGAȚII','CONTROL_DISPOZIȚIE_REFERINȚE','DIRECTIVĂ_DE_METODĂ','CONTROL_DISPOZIȚIE_MONTARE')]
 # Accept score only for specifically improved R2 dimensions, not the scores automatically inherited by the executor.
 earned=set(prev['accepted_subchecks'])
 if all(checks.values()) and not errors:
  earned.add('QC01-R4')
  if j['known_closure_dates'] and ct:earned.add('QC02-R1')
  if ct and j['source_literal'] and (relevant or j['functional_criteria_unidentified']):earned.add('QC02-R4')
  if ct and all(c['current'].get('observed') and c['current']['evidence_ids'] and any(s in c['current']['status'] for s in ['PASS','FAIL']) for c in ct):earned.add('QC02-R2')
  if tid in ('T216','T354','T355','T227','T224','T229'):earned.add('QC10-R2')
 eligible={x['id'] for c in rub['criteria'] for x in c['report_subchecks']};assert not (earned-eligible)
 unresolved=[c['id'] for c in ct if c['current']['status'] in ('NEEXECUTAT','INCONCLUDENT','BLOCAT_ACCES')];cs=collections.Counter(c['current']['status'] for c in ct)
 fixes=['Verificați individual ' + ', '.join(unresolved[:4])+(' și alte '+str(len(unresolved)-4)+' criterii.' if len(unresolved)>4 else '.') if unresolved else 'Reverificați independent legăturile de cod și efect, inclusiv contraprobe.']
 if j['functional_criteria_unidentified']: fixes.append('Verificați dosarul nominal, anexele și eventualul succesor; dacă nu conțin cerințe funcționale proprii păstrați NEDETERMINABIL, distinct de decizia administrativă.')
 if j['missing_exact_closure_date_at_cutoff']:fixes.append('Prima observație Git delimitată nu dovedește data exactă de închidere sau montare.')
 if not j['zone_related_controls_only']:fixes.append('Fără răspuns nominal de la zonă în această versiune; cereți mapare probatorie sau dispoziție de neaplicabilitate motivată.')
 if tid=='T224':fixes.append('3/3 referințe la reviziile pretinse, fără echivalare cu funcționarea importurilor la SHA auditat.')
 if tid=='T229':fixes.append('Lista de finalizate și starea plan sunt contradictorii; închiderea administrativă istorică și funcționarea actuală rămân distincte.')
 if tid=='T227':fixes.append('Limitarea CESIRO privind JAR și AD_Form nu respinge funcționarea pe alte cabinete. Reverificați R57/rolul pe versiune și mediu corecte.')
 issues.update(errors)
 results.append({'task':tid,'canonical':j['canonical'],'file':rr['file'],'R1_hash':old['sha256'],'R2_hash':rr['sha256'],'R1_quality':prev['audit_quality_score'],'A11_R2_quality':len(earned)/5,'earned_subchecks_R2':sorted(earned),'known_functional_criteria':not j['functional_criteria_unidentified'],'criterion_dispositions':rows,'source_and_structure_checks':checks,'errors':errors,'current_counts':dict(cs),'functional_runtime_passes_confirmed':sum('REVERIFICAȚI_PASS_FUNCȚIONAL'==x['A11_classification'] for x in rows),'quality_gate':'PARȚIAL_DE_RELUAT','next':fixes,'R1_score_movement':'Creșterea reflectă trasabilitatea semantică unde a fost probată, nu o nouă execuție funcțională.'})
assert not issues and len(forward)==len(reverse)==4550 and forward==reverse
assert all(all(x['source_and_structure_checks'].values()) for x in results);assert sum(len(x['criterion_dispositions']) for x in results)==2196
hist=collections.Counter(f"{x['A11_R2_quality']:.1f}" for x in results)
v={'reviewer':'A11','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'population_and_scope':'651/651 din cutofful R1. T352 / T366 actualizat țin de supliment și nu se confundă cu rezultatele de aici.','R2_hash':h(D/'A12_raport.json'),'catalog_sha256':h(D/'Dovezi_criterii.json'),'R1_A11_ledger_sha256':h(E/'A11_ledger_651_fise.json'),'reviewed_all':len(results),'accepted_full':0,'forward_inverse_join':{'forward':len(forward),'inverse':len(reverse),'symmetric_difference_size':len(forward^reverse)},'kinds':dict(kinds),'status_distribution':dict(stat),'semantic_buckets':dict(shards),'histogram_report_quality_per_task':dict(hist),'errors':list(issues),'records':results}
put(E/'A11_ledger_651_R2.json',v);print(h(E/'A11_ledger_651_R2.json'),hist,shards, 'generic repeated:',sum(n for t,n in generic.items() if n>1),len(generic))

