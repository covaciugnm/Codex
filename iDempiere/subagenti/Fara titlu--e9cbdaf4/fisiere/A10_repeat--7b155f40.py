import pathlib,json,datetime
O=pathlib.Path(__file__).parent;E=O.parent
header=(E/'A10/runtime_probe.py').read_text(encoding='utf8').split('Base.metadata.create_all(engine)')[0]
exec(header)
Base.metadata.create_all(engine)
with SessionLocal() as db:
 audit.record(db,action='A11-R2',entity_type='QA',entity_id='synthetic',after={'token':'TOP_ONLY_A11','children':[{'auth_context':{'token':'INNER_ONLY_A11'}}],'public':'kept'});db.commit()
 sa=db.query(AuditEvent).filter_by(action='A11-R2').one().after_json
assert sa['token']=='***MASKED***' and sa['children'][0]['auth_context']['token']=='INNER_ONLY_A11' and sa['public']=='kept'
client=TestClient(app)
with patch.object(health.IdempiereClient,'health',return_value={'reachable':False,'mode':'live','error':'Synthetic lab refusal'}):
 h1=client.get('/api/v1/internal/idempiere/health')
assert h1.status_code==200 and h1.json()['status']=='ok' and h1.json()['idempiere']['reachable'] is False
out={'fixture':'New ASGI/SQLite offline audit, entirely synthetic marker. No live secret or ERP connection.','top_level_masked':True,'nested_list_token_retained':True,'other_field_retained':True,'HTTP_readiness':h1.status_code,'declared':h1.json()['status'],'actual_dependency':h1.json()['idempiere']['reachable'],'network_block':denied};(O/'A10_redaction_readiness.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out)

