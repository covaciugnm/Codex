import csv,pathlib,json,hashlib,datetime
R=pathlib.Path(__file__).resolve().parent
def read(name):
 with (R/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
c=read('cases-batch-01.csv'); e=read('evidence-index-batch-01.csv'); controls=read('inventory-controls-batch-01.csv')+read('inventory-controls-partial.csv')
ci={x['control_id'] for x in controls}; ei={x['evidence_id'] for x in e}; errors=[]
for x in c:
 for token in x['control_id'].split(';'):
  if token.strip() not in ci:errors.append({'case':x['case_id'],'issue':'unresolved_control','value':token})
 for token in x['evidence_ids'].split(';'):
  if token.strip() not in ei:errors.append({'case':x['case_id'],'issue':'unresolved_evidence','value':token})
 if x['status']=='PASS' and 'NOT_RUN' in x['recovery_path']:errors.append({'case':x['case_id'],'issue':'pass_with_unrun_recovery'})
for x in e:
 if x['source_kind']=='tool_transcript':
  for field in ['call_ref','call_code','timestamp','observed_interval','timestamp_precision','description','redaction']:
   if not x.get(field):errors.append({'evidence':x['evidence_id'],'issue':'missing_'+field})
  if x.get('path') or x.get('sha256'):errors.append({'evidence':x['evidence_id'],'issue':'transcript_unexpected_file_claim_manual_review'})
manifest=json.loads((R/'batch-01-manifest.json').read_text(encoding='utf-8-sig'))
for name,digest in manifest.items():
 if hashlib.sha256((R/name).read_bytes()).hexdigest()!=digest.lower():errors.append({'file':name,'issue':'manifest_mismatch'})
out={'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':len(c),'author_status_counts':{s:sum(x['status']==s for x in c) for s in ['PASS','FAIL','BLOCKED','NOT_RUN']},'candidate_controls_batch':len(read('inventory-controls-batch-01.csv')),'route_observations':len(read('inventory-routes-batch-01.csv')),'errors':errors,'independent_ui_reproduction':'NOT_RUN; no UI handoff; tool policy stop respected','g1':'INCOMPLETE_NOT_SIGNED','g4':'NOT_COMPLETE','caution':'PASS counts are author observations only; transcript references are not local screenshot files and not independently replayed.'}
(R/'review-agent-2-batch-01-integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
