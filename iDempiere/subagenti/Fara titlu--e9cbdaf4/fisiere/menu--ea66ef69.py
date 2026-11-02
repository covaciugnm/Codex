import pathlib,sys,tempfile,os,secrets,json,hashlib
from unittest.mock import patch
O=pathlib.Path(__file__).parent;root=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
with tempfile.TemporaryDirectory(prefix='a11-menu-') as temp:
 os.environ.update(EVA_ENV='test',EVA_AUTH_ENFORCE='1',IDEMPIERE_MOCK='1',EVA_DATABASE_URL='sqlite:///'+str(pathlib.Path(temp)/'db.sqlite3').replace(chr(92),'/'),EVA_JWT_SECRET=secrets.token_hex(32),ONLYOFFICE_JWT_SECRET=secrets.token_hex(32),EVA_ANAF_OAUTH_ZILNIC='0')
 sys.path[:0]=['D:/CodexWork/eva-a01-fixture-deps',str(root/'backend')]
 from app.routers import idempiere_meta as m
 from starlette.requests import Request
 req=Request({'type':'http','method':'GET','path':'/a11','headers':[],'query_string':b'lang=ro'})
 author=json.loads((O.parent/'A09/native_actions.json').read_text(encoding='utf8'))
 rows=[(x['action'],x['ad_menu_id'],x['native_object']) for x in author['cases']]+[('W',11111,7104),('X',11112,7106),('F',11113,7107)]
 cases=[]
 for action,mid,oid in rows:
  tag,key={'W':('window','ad_window_id'),'X':('form','ad_form_id'),'F':('workflow','ad_workflow_id')}[action]
  record=dict(ad_menu_id=mid,name_en='a11',name_loc='a11',name='a11',is_translated=True,description=None,action=action,ad_window_id=None,ad_form_id=None,ad_workflow_id=None,ad_process_id=None,ad_task_id=None,ad_workbench_id=None,ad_infowindow_id=None,object_name='a11',primary_table=None,isactive='Y',issummary='N');record[key]=oid
  with patch.object(m.readdb,'_rows',return_value=[record]): observed=m.menu_item_meta(mid,req)['menu']
  cases.append([mid,action,tag,oid,observed.get('type'),observed.get('object_id')])
 file=O/'A09_action_handler.json'
 ob={'native_reference':author['native'],'code_sha256':hashlib.sha256((root/'backend/app/routers/idempiere_meta.py').read_bytes()).hexdigest(),'source_236':len(author['cases']),'incorrect_type_236':sum(c[2]!=c[4] for c in cases[:-3]),'wrong_id_236':sum(c[3]!=c[5] for c in cases[:-3]),'synthetic_controls_W_X_F':cases[-3:],'scope':'Original handler; replaced DB read with captured AD pairs and 3 novel controls; neither active operator nor calls to live database.'};assert ob['incorrect_type_236']==236 and cases[-3][2:4]==cases[-3][4:6];file.write_text(json.dumps(ob,ensure_ascii=False,indent=2),encoding='utf8');print(ob)

