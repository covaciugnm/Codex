import sys, json, hashlib, gzip, re, collections, pathlib, datetime
BASE=pathlib.Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');E=BASE/'executie';R=E/'A11_reproduceri_lot1';BLOB=pathlib.Path('D:/CodexWork/A12_evidence_20261102/blobs')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def H(x):return hashlib.sha256(x).hexdigest()
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def clean(s):return re.sub(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}','[email redactat]',re.sub(r'(?i)((?:[A-Za-z0-9_.-]*password|parola|secret_key|api_key|token)\s*[=:]\s*)(\S+)',r'\1[redactat]',str(s or '').strip()))
def ptr(j,s):
 for k in s.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');j=j[int(k)] if isinstance(j,list) else j[k]
 return j
def hxval(val,c):return H(json.dumps(val,ensure_ascii=False,sort_keys=True).encode())[:c]
cache={}; blobcache={}
def cap(n):
 if n not in cache:cache[n]=read(BASE/'capturi'/n)
 return cache[n]
def blob(oid):
 if oid not in blobcache:
  data=gzip.decompress((BLOB/(oid+'.gz')).read_bytes())
  if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=oid:raise ValueError('bad object')
  blobcache[oid]=data.decode('utf-8-sig',errors='replace')
 return blobcache[oid]
a=read(E/'A12_raport.json');idx=read(BASE/'A12_index_taskuri.json');inv={x['source_id']:x for x in idx['rows'] if x['individual_review']}
actual=set(p.name for p in (E/'taskuri').glob('Fisa_*.json'));expected=set(pathlib.Path(x['file']).name for x in a['records']);assert actual==expected and len(actual)==651
rubro=read(BASE/'A11_rubrica_control.json');criteria=[t['id'] for c in rubro['criteria'] for t in c['report_subchecks']]
counts=collections.Counter();status_by=collections.Counter();led=[];anomalies=[];numcons=0
for row in a['records']:
 id=row['id'];path=E/row['file'];data=path.read_bytes();d=json.loads(data.decode('utf-8-sig'));orig=inv[id];err=[];assert H(data)==row['sha256']
 if d['source_id']!=id or d['canonical']!=orig['canonical'] or d['original_state']!=orig['source_state']:err.append('identitate/stare')
 source_hits=0
 for x in d['source_registry']+d['source_lists']:
  try: ptr(cap(x['file']),x['pointer']);source_hits+=1
  except Exception as ex:err.append('source pointer invalid: '+x['file']+x['pointer'])
 checked_quotes=0; qerr=[]
 for ev in d['historical_evidence']:
  try:
   s=blob(ev['git_blob']); pos=ev['line_or_json_pointer']
   if isinstance(pos,int):v=s.splitlines()[pos-1]
   else:
    v=ptr(json.loads(s),pos)
    if pos.startswith('/corespondenta/'):v=json.dumps(v,ensure_ascii=False)
   if clean(v)[:750]!=ev['quote']:qerr.append({'oid':ev['git_blob'],'loc':pos,'reason':'text diferit la pointer/linia citată'})
   else:checked_quotes+=1
  except Exception as ex:qerr.append({'oid':ev['git_blob'],'loc':ev['line_or_json_pointer'],'reason':type(ex).__name__+': '+str(ex)[:100]})
 statuslist=d['control_results'];byid={x['id']:x['status'] for x in statuslist};ckcounts=collections.Counter(byid.values());status_by.update(byid.values())
 if len(byid)!=36 or any('A12-CK-'+str(k).zfill(2) not in byid for k in range(1,37)):err.append('36 controale neidentice')
 if d['assurance_level']!='PARTIAL_CU_LIMITARI' or d['independent_audit_score'] is not None:err.append('incongruență verdict')
 if d['transfer'] and d['transfer'].get('destination'):
  dest=d['transfer']['destination']
  if dest!=orig['aggregate_target']:err.append('destinație diferită')
 req=[];types=collections.Counter()
 for k,f in enumerate(d['atomic_requirements']):
  txt=f['text'];src=f['source'];basis=f.get('basis','')
  if src.startswith('registre:cerere_proprietar') and re.match(r'^[\(\s]*(nescris|reconstitui|sursa[: ]|surse[: ]|coordonare[ :]|textul original|sursa document)',txt,re.I): typ='METADATA_NU_CRITERIU'
  elif src.startswith('registre:descriere'):typ='DESCRIERE_DECLARATA_NU_DOVADA'
  elif 'activit' in basis.lower() or f.get('result'):typ='ACTIVITATE_SAU_TINTA_CANDIDATA'
  elif src.startswith('registre:cerere_proprietar'):typ='TEXT_CERERE_CANDIDAT_DE_ATOMIZAT'
  else:typ='CONTEXT_SAU_OBIECTIV_DE_CALIFICAT'
  req.append({'ordinal':k+1,'kind_for_review':typ,'text_sha256':H(txt.encode()),'source':src,'has_structured_target':bool(f.get('result')),'task_status_and_specific_evidence_id': bool(f.get('status') and f.get('evidence_ids'))});types[typ]+=1
 count_direct=len(d['static_code_and_live_dictionary']);hist_n=len(d['historical_evidence']);finds=d['findings'];fids=[x if isinstance(x,str) else x.get('id') for x in finds];stored=d['artifacts_git_semantic_read'];hist_commits=sum(len(x.get('commits',{})) for x in stored);state=d['original_state']
 refcols=[x.get('id') if isinstance(x,dict) else x for x in d['planned_cross_controls']]
 pointers_good=not err; quotes_good=not qerr;hist_dates=d.get('original_dates') or []
 # Partial contribution only; unscored subchecks deliberately fail wholesale, not 10 via N/A.
 partial={
 'QC01-R1':d['current_sha']==a['commit'] and d['source_cutoff']==a['cutoff'] and pointers_good,
 'QC01-R2':pointers_good and d['source_id'] in inv,'QC01-R3':bool(d.get('owner')) and pointers_good,
 'QC01-R4':pointers_good and len(byid)==36, 'QC01-R5':False,
 'QC02-R1':pointers_good and hist_n>0 and quotes_good,'QC02-R2':all(t['task_status_and_specific_evidence_id'] for t in req) and bool(req) and quotes_good,
 'QC02-R3':False,'QC02-R4':state in ('agregat','anulat') and d.get('disposition_evidence') in ('TRANSFER_DOCUMENTAT','DECIZIE_ANULARE_DOCUMENTATA') and quotes_good and hist_n>0,
 'QC02-R5':False,
 'QC03-R5': d['assurance_level']=='PARTIAL_CU_LIMITARI' and byid.get('A12-CK-09')!='PASS_DOVEDIT',
 'QC04-R1':False,'QC04-R4':False,'QC05-R1':bool(count_direct) and quotes_good and isinstance(d.get('static_code_and_live_dictionary'),list),
 'QC07-R4':quotes_good and '[unredacted_secret]' not in json.dumps(d,ensure_ascii=False),'QC07-R5':d['phase'].find('')>=0 and d['independent_audit_score'] is None,
 'QC08-R1':False,'QC08-R2':False,'QC08-R4':id=='T227',
 'QC09-R1':pointers_good and quotes_good and hist_n>0,'QC09-R2':False,'QC09-R5':False,
 'QC10-R1':id=='T227' and bool(fids),'QC10-R2':False,'QC10-R3':False,'QC10-R4':False,'QC10-R5':False
 }
 # The row-level evidence is documentary; masking not inferred as complete from placeholder search.
 partial['QC07-R4']=False;partial['QC07-R5']=False
 # QC01-R1 needs independent deployment bounds, not only an administrative snapshot.
 partial['QC01-R1']=partial['QC01-R1'] and 'closure_installed_version' in d['closure_snapshot'] and id=='T227'
 # No per-task DB probe inferred solely from a static class/table coincidence.
 partial['QC05-R1']=id=='T227' and byid.get('A12-CK-12')!='PASS_DOVEDIT'
 # Repeatable documentary hashes allow qualified evidence and are already distinguished in every file, not claiming execution of functional tests.
 partial['QC09-R2']=quotes_good and d['assurance_level']=='PARTIAL_CU_LIMITARI' and (hist_n>0 or count_direct>0 or bool(stored))
 accepted=[s for s in criteria if partial.get(s,False)];score=round(len(accepted)*0.2,1)
 nexts=[]
 if types['METADATA_NU_CRITERIU']:nexts.append('Îndepărtează din numitor metadata de proveniență, păstrând-o ca sursă; califică „cerință necunoscută” unde nu există alt text normativ.')
 if state=='agregat': nexts.append('Pentru '+str((d['transfer'] or {}).get('destination') or orig.get('aggregate_target') or 'destinația neprecizată')+' verifică predarea fiecărui obiectiv și dovada propriei funcționalități; nu moșteni verdictul părintelui.')
 elif state=='anulat':nexts.append('Verifică decizia de anulare, autorul, data și ce efecte au rămas; N/A se decide pentru fiecare criteriu, nu pentru tot taskul.')
 elif id=='T229':nexts.append('Reconciliere stare plan/reactivare cu lista istorică de anulare și criteriile preluate; nu clasifica drept montat.')
 else:nexts.append('Leagă revendicarea '+state+' de build/deploy la închidere și comportamentul la SHA curent; fără dovadă rămâne NEDETERMINAT istoric.')
 nexts.append('Titular '+str(d['owner'])+': leagă fiecare cerință verificabilă de control/flux/evidență specifică; execută scenariile admise sau marchează cauza concretă a neexecuției.')
 if qerr or err:nexts.insert(0,'Corectează pointerii/citările nevalidate și reexecută verificarea independentă.')
 counts.update(types);counts['cases']+=1;counts['case_meta']+=int(types['METADATA_NU_CRITERIU']>0);counts['quote_ok']+=checked_quotes;counts['quote_errors']+=len(qerr);counts['source_hits']+=source_hits;counts['file_errors']+=len(err);counts['structured_requirements']+=sum(x['task_status_and_specific_evidence_id'] for x in req);numcons+=len(req)
 led.append(dict(source_id=id,canonical=d['canonical'],chapter=d['chapter'],owner=d['owner'],source_status=state,file=row['file'],sha256=row['sha256'],disposition='PARTIAL_DE_RELUAT',audit_quality_score=score,accepted_subchecks=accepted,unearned_subchecks=[s for s in criteria if s not in accepted],quality_score_limit='Aplicarea rubricii A11 pentru raportul individual prezent; lipsurile nu se transformă în N/A.',result_at_closure=d['verdict_at_closure'],result_current=d['verdict_current'],source_pointer_count=source_hits,has_source_closure_date=bool(hist_dates),source_capture=d['source_cutoff'],original_requirement_fragments=len(req),fragment_kinds=dict(types),fragment_records=req,verified_historical_quotes=checked_quotes,unverified_quotes=qerr,observed_static_classes=count_direct,artifact_rows=len(stored),commit_rows=hist_commits,registered_findings=fids,planned_handoffs=refcols,primary_constraint=d['requirement_limit'],source_disposition=d['disposition_evidence'],raw_control_counts=dict(ckcounts),control_ids_by_status={s:[k for k,v in byid.items() if v==s] for s in ckcounts},integrity_issues=err,actions=nexts))
 if qerr or err:anomalies.append([id,qerr[:2],err[:2]])
assert set(x['source_id'] for x in led)==set(inv)
result=dict(schema='eva.audit.a11.adjudicari-task-v1',utc=now(),reviewer='A11',scope='Inspecție nominală a aptitudinii fiecărei fișe din prima rundă pentru acceptare; verificare structură, comparație cu surse primare și citări, analiza limitelor. Nu este o reexecutare funcțională a tuturor cerințelor.',method='Pentru fiecare raport: identificare/stare/canonic/hash, toate trimiterile registru/liste, toate fragmentele de cerință și tipul lor, toate citările istorice la blob și linie/JSON pointer, dovezi Git/dicționar, predări, verdict și toate cele 36 controale. Punctele de raport câștigate de verificările documentare sunt listate nominal. Lipsa probelor funcționale sau a acceptării N/A permite numai PARTIAL_DE_RELUAT.',source_report='A12_raport.json',source_sha256=H((E/'A12_raport.json').read_bytes()),rubric_sha256=H((BASE/'A11_rubrica_control.json').read_bytes()),reviewed=len(led),accepted_fully=0,fragment_total=numcons,totals=dict(counts),status_counts=dict(status_by),score_histogram=dict(collections.Counter(str(x['audit_quality_score']) for x in led)),records=led)
(E/'A11_ledger_651_fise.json').write_text(json.dumps(result,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k in ['reviewed','accepted_fully','fragment_total','totals','score_histogram','status_counts']}));print('anomalies',anomalies[:3])

