import pathlib,os,json,hashlib,datetime
O=pathlib.Path(__file__).parent;E=O.parent;src=(E/'R2_zone/A07/api-full-guard.py').read_text(encoding='utf8');prefix,body=src.split(" case('no_auth'",1)
custom=""" case('deny-foreign','A','m','RO10000012','a11-deny-key')
 case('B-first','B','m','RO77777777','A11-SHARED-RMA',qty=3)
 case('A-different-payload','A','m','RO77777777','A11-SHARED-RMA',qty=7)
 case('A-new-key','A','m','RO77777777','A11-NEW-KEY',qty=7)
 case('A-same-key-different-payload','A','m','RO77777777','A11-NEW-KEY',qty=11)
"""
exec(compile(prefix+custom,'A11_reversed_GardenWorld_synthetic','exec')); dbkeys=[]
with SessionLocal() as db:
 dbkeys=[(x.tenant_cui,x.status_code,x.endpoint)for x in db.query(IdempotencyKey).all()]
cli.close();engine.dispose();tmp.cleanup()
ev=[(x['case'],x['status'],x['response'].get('rma_id'),x['remote_before'],x['remote_after'])for x in events];assert ev[0][1]==403 and ev[1][1]==ev[2][1]==ev[3][1]==ev[4][1]==201;assert ev[1][2]==ev[2][2] and ev[3][2]==ev[4][2]!=ev[1][2] and ev[2][4].get('cA',0)==0 and len(dbkeys)==2
out={'scope':'Normal ASGI HTTP entry and real auth/IAM/idempotency in temporary SQLite. Only downstream CRUD is stubbed; no actual production private ERP data accessed. Reversed cabinet order and different payloads, extra legitimate order as control.','time':datetime.datetime.now(datetime.UTC).isoformat(),'base_fixture_sha':hashlib.sha256(src.encode()).hexdigest(),'events':ev,'persisted_idempotency':dbkeys,'external_calls':denied,'cleanup':not wd.exists()}
(O/'A07_RMA_reversed.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(ev)

