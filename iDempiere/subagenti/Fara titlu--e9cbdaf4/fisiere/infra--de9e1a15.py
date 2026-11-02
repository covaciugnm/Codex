import hashlib,datetime,pathlib,tempfile,subprocess,os,json
O=pathlib.Path(__file__).parent;root=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
author=(O.parent/'A10/runtime_probe.py').read_text(encoding='utf8')
harness=author.split('Base.metadata.create_all(engine)')[0].replace("base=Path(__file__).parent","base=O")
exec(harness)
Base.metadata.create_all(engine);client=TestClient(app)
with SessionLocal() as db:
 db.add(EVA_AI_Task(eva_uuid='A11-JOB',task_type='__isolated_no_provider__',tenant_cui='X',priority=1,status='Queued'));db.commit()
with SessionLocal() as a, SessionLocal() as b:
 first=worker.claim_next(a,'X');second=worker.claim_next(b,'X'); ids=[first.eva_uuid,second.eva_uuid]; service.process_task(a,first);a.commit();service.process_task(b,second);b.commit()
with SessionLocal() as db:
 results=db.query(EVA_AI_Result).filter_by(task_uuid='A11-JOB').count()
 audit.record(db,action='A11',entity_type='TEST',entity_id='test',after={'token':'A11-TOP-SYNTHETIC','raw':{'token':'A11-INNER-SYNTHETIC'}});db.commit()
 raw=db.query(AuditEvent).filter_by(action='A11').one().after_json
with patch.object(health.IdempiereClient,'health',return_value={'reachable':False,'error':'A11 fixture timeout','mode':'live'}):
 res=client.get('/api/v1/internal/idempiere/health')
o={'checks':{'claimed_ids':ids,'result_rows':results,'top_redacted':raw['token']=='***MASKED***','nested_canary_present':raw['raw']['token']=='A11-INNER-SYNTHETIC','readiness_report':res.json(),'readiness_http':res.status_code},'scope':'Pinned backend real worker/endpoint/audit store with temporary SQLite and separate sessions; manual schedule of interleaving, not a measurement of production concurrency; private test markers only and zero integration traffic.'};assert results==2 and o['checks']['nested_canary_present'];write('A10_backend_independent.json',o);print(o)

