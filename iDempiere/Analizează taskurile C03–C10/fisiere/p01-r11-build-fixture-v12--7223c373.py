from pathlib import Path

base = Path('D:/CodexWork')
child = (base/'p01-r11-test-isolated-child-v10.py').read_text(encoding='utf8')
start = child.index(" if e=='subprocess.Popen':")
end = child.index(" if e in ('socket.sendto'", start)
child = child[:start] + " if e=='subprocess.Popen':refuse(e)\n" + child[end:]
child = child.replace("'outcome':report.outcome}",
                      "'outcome':report.outcome,'report_type':type(report).__name__,'subtest_context':repr(getattr(report,'context',None))[:1000],'failure':str(report.longrepr)[-2500:] if report.failed else None}")
insert = '''
actor_fixture_evidence = None
if os.environ.get('EVA_AUDIT_ACTOR_FIXTURE') == '1':
 import app as portal
 original_client = portal.app.test_client
 original_token = portal.current_token
 original_user = portal._current_user_me
 original_request = portal._eva_req
 forbidden_calls = []
 portal._eva_req = lambda *args, **kwargs: (forbidden_calls.append(True) or ({},200))
 for label, token, user in [('absent',None,{}),('invalid','invalid-token',{})]:
  portal.current_token = lambda token=token: token
  portal._current_user_me = lambda user=user: user
  response = original_client().get('/app/api/saga/import/completeness-audit')
  assert response.status_code == 302 and response.location == '/app/login'
  assert forbidden_calls == []
 portal.current_token = original_token
 portal._eva_req = original_request
 portal._current_user_me = lambda: {'user':{'uuid':'synthetic-manager','email':'actor@example.invalid','role':'manager','tenant_cui':'AUDIT001'},'access':[{'tenant_cui':'AUDIT001'}]}
 portal._cabinet_info = lambda: ('AUDIT001','Synthetic cabinet')
 portal._firm_name = lambda cui: 'Synthetic '+str(cui)
 def actor_client(*args, **kwargs):
  client = original_client(*args, **kwargs)
  client.set_cookie('eva_cui','AUDIT001',domain='localhost')
  return client
 portal.app.test_client = actor_client
 actor_fixture_evidence = {'active_company_cookie':'AUDIT001','auth_me':'synthetic manager response; authentication backend is not exercised','cabinet_name':'synthetic fixture','no_token_refused_before_proxy':True,'invalid_user_refused_before_proxy':True,'upstream_calls_for_refused_controls':len(forbidden_calls),'persistent_erp_effect':False}

'''
child = child.replace("mode,path=sys.argv[1:];", insert+"mode,path=sys.argv[1:];")
child = child.replace("'windows_pair_adapter':adapter_evidence}","'windows_pair_adapter':adapter_evidence,'actor_fixture':actor_fixture_evidence}")
(base/'p01-r11-test-isolated-child-v12.py').write_text(child,encoding='utf8')

source = (base/'p01-r11-original-config-v11d.py').read_text(encoding='utf8')
source = source.replace('Suite_originale_config_sintetice_v11d','Suite_originale_config_sintetice_v12')
source = source.replace('p01-r11-test-isolated-child-v10.py','p01-r11-test-isolated-child-v12.py')
source = source.replace("front=[]", "front=['event_theme_admin','storefront_admin_i18n','saga_completeness_audit_ui','idempiere_web_module_coverage']")
source = source.replace("stores=['event_themes','seasonal_themes']", "stores=['event_themes','seasonal_themes','audit_regressions']")
source = source.replace("  node_guard=fixture/'deny-node-network.cjs';", "  if rel in ('tests/test_saga_completeness_audit_ui.py','tests/test_idempiere_web_module_coverage.py'):ev['EVA_AUDIT_ACTOR_FIXTURE']='1'\n  node_guard=fixture/'deny-node-network.cjs';")
source = source.replace("'synthetic_config_scope':'Theme metadata", "'synthetic_config_scope':'Subprocess execution entirely refused in this child; no Node execution. For the 2 authentication/context suites only, valid auth/me reply and company cookie are injected. Theme metadata")
(base/'p01-r11-original-config-v12.py').write_text(source,encoding='utf8')
print('V12 separates child/subtest events and disables every child process.')
