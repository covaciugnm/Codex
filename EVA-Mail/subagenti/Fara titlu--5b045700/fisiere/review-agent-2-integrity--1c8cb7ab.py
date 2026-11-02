"""Read-only structural checks for EVA audit artifacts; never validates product behavior."""
import csv, hashlib, json, pathlib, datetime, re

ROOT = pathlib.Path(__file__).resolve().parent
checks=[]
def record(level,code,message,ids=None):
    checks.append(dict(level=level,code=code,message=message,ids=ids or []))
def pick(*names):
    return next((ROOT/n for n in names if (ROOT/n).is_file()),None)
def table(label, names, columns):
    path=pick(*names)
    if path is None:
        record('PENDING','missing_'+label,'Artifact not yet delivered: '+', '.join(names)); return []
    try:
        with path.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f); rows=list(reader); fields=reader.fieldnames or []
        if label=='controls' and 'evidence_id' in fields and 'evidence_ids' not in fields:
            fields.append('evidence_ids')
            for row in rows: row['evidence_ids']=row.get('evidence_id','')
        if 'partial' in path.name:
            record('PENDING','partial_'+label,'Partial artifact only; G1 denominator is not frozen')
        missing=sorted(set(columns)-set(fields))
        if missing: record('ERROR','columns_'+label,'Missing schema columns: '+', '.join(missing))
        record('INFO','loaded_'+label,str(len(rows))+' rows loaded from '+str(path.relative_to(ROOT)))
        return rows
    except Exception as ex:
        record('ERROR','parse_'+label,type(ex).__name__); return []
def tokens(value):
    return [x.strip() for x in re.split(r'[;|]',value or '') if x.strip()]
def unique(rows,key,label):
    seen=set(); dup=[]; empty=0
    for row in rows:
        ident=row.get(key,'').strip()
        if not ident: empty+=1
        elif ident in seen: dup.append(ident)
        seen.add(ident)
    if empty: record('ERROR','empty_'+label,str(empty)+' rows have no '+key)
    if dup: record('ERROR','duplicate_'+label,'Duplicate IDs',sorted(set(dup)))
    return seen-{''}

requirements=table('requirements',['requirements.csv'],['requirement_id','description','case_ids','evidence_ids','status'])
reqids={r.get('requirement_id') for r in requirements}
seeds=table('seeds',['historical-retest-seeds.csv'],['case_id','risk_id','procedure','expected','status'])
unique(seeds,'case_id','seed')
expected_risks={f'A{i:02}' for i in range(1,23)}|{f'U{i:02}' for i in range(1,5)}
missing_risks=expected_risks-{x.get('risk_id') for x in seeds}
if missing_risks: record('ERROR','historic_traceability','Missing historic risks',sorted(missing_risks))

controls=table('controls',['inventories/inventory-controls.csv','inventory-controls.csv','inventory-controls-partial.csv'],['control_id','platform','screen','state','role','evidence_ids'])
# One semantic control may have several state/role rows, so uniqueness uses the tuple.
controlids={x.get('control_id') for x in controls}
seen=set()
for row in controls:
    key=tuple(row.get(c,'') for c in ('control_id','platform','screen','state','role'))
    if key in seen: record('ERROR','duplicate_control_state','Duplicate control/platform/screen/state/role row',[row.get('control_id','')])
    seen.add(key)

ev=table('evidence',['evidence/evidence-index.csv','evidence-index.csv','evidence-index-partial.csv'],['evidence_id','path','sha256','timestamp','platform','description','redaction'])
evids=unique(ev,'evidence_id','evidence')
for row in ev:
    ident=row.get('evidence_id','')
    raw=row.get('path','')
    if not raw:
        record('ERROR','empty_evidence_path','No file path',[ident]); continue
    p=pathlib.Path(raw)
    p=(ROOT/p).resolve() if not p.is_absolute() else p.resolve()
    try: p.relative_to(ROOT)
    except ValueError:
        record('ERROR','external_evidence','Evidence outside audit package; copy/redact explicitly',[ident]); continue
    if not p.is_file(): record('ERROR','missing_evidence_file','Referenced file missing',[ident]); continue
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual.lower()!=row.get('sha256','').strip().lower(): record('ERROR','hash_mismatch','Evidence hash missing or mismatched',[ident])
    for c in ('timestamp','platform','description','redaction'):
        if not row.get(c,'').strip(): record('ERROR','evidence_metadata','Missing '+c,[ident])

case_columns=['case_id','requirement_id','risk_id','platform_build','screen','control_id','role','data_fixture','preconditions','steps','expected_ui','expected_server_effect','recovery_path','dependencies','side_effect_class','status','actual','evidence_ids','issue_id','executed_at','executor','reviewer','retest_build']
cases=table('cases',['cases/cases.csv','cases.csv','cases-partial.csv'],case_columns)
caseids=unique(cases,'case_id','case')
allowed={'PASS','FAIL','BLOCKED','NOT_RUN','N/A'}
for row in cases:
    ident=row.get('case_id',''); status=row.get('status','')
    if status not in allowed: record('ERROR','invalid_status','Unsupported test status',[ident])
    if row.get('requirement_id') not in reqids: record('ERROR','unknown_requirement','Requirement ID not found',[ident])
    if status in {'PASS','FAIL'}:
        needed=['platform_build','steps','expected_ui','expected_server_effect','recovery_path','actual','evidence_ids','executed_at','executor']
        missing=[c for c in needed if not row.get(c,'').strip()]
        if missing: record('ERROR','execution_metadata','Executed case missing: '+', '.join(missing),[ident])
        if row.get('control_id') and row.get('control_id') not in controlids: record('ERROR','unknown_control','UI control not found in delivered inventory',[ident])
        if status=='FAIL' and not row.get('issue_id','').strip(): record('ERROR','fail_without_issue','FAIL needs an issue reference',[ident])
    if status=='N/A' and (not row.get('actual','').strip() or not row.get('reviewer','').strip()): record('ERROR','na_without_review','N/A needs reason and reviewer',[ident])
    if status=='BLOCKED' and not row.get('actual','').strip(): record('ERROR','blocker_without_reason','BLOCKED needs reason; owner/next action verified manually',[ident])
    missing_evidence=set(tokens(row.get('evidence_ids')))-evids
    if missing_evidence: record('ERROR','unknown_case_evidence','Evidence IDs absent from index',[ident]+sorted(missing_evidence))
for row in requirements:
    unknown=set(tokens(row.get('case_ids')))-caseids
    if unknown: record('ERROR','unknown_requirement_case','Requirement case reference unresolved',[row.get('requirement_id','')]+sorted(unknown))
for row in controls:
    unknown=set(tokens(row.get('evidence_ids')))-evids
    if unknown: record('ERROR','unknown_control_evidence','Control evidence reference unresolved',[row.get('control_id','')]+sorted(unknown))

manifest=pick('plan-manifest.json')
if manifest:
    for row in json.loads(manifest.read_text(encoding='utf-8-sig')):
        p=pathlib.Path(row['Path'])
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest().lower()!=row['Hash'].lower():
            record('ERROR','plan_manifest_mismatch','Plan artifact changed after manifest',[p.name])

if not cases: record('PENDING','g4_not_started','No delivered execution matrix; no product pass rate can be reported')
record('MANUAL','g1_review_required','Reviewer must reconcile source/runtime routes, all conditional controls/states, exact current versions, graph recovery and evidence redaction before signing inventory')
record('MANUAL','behavior_not_verified','Structural checks do not prove behavior or substitute independent UI reproduction')
out=dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='audit-artifact-integrity-only',checks=checks,counts={k:sum(x['level']==k for x in checks) for k in ['ERROR','PENDING','INFO','MANUAL']},product_verdict='NOT_EVALUATED')
target=ROOT/'review-agent-2-integrity-results.json'
target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(target),'counts':out['counts'],'product_verdict':'NOT_EVALUATED'},ensure_ascii=False))
