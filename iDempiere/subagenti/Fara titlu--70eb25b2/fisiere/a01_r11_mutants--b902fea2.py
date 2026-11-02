import sys,os,unittest,contextlib,io,hashlib,json,datetime,logging,socket
from pathlib import Path
from unittest import mock
W=Path(r'D:\CodexWork\a01-r11-frozen');F=W/'new/frontend';sys.path[:0]=[str(F),str(F/'tests'),r'D:\CodexWork\eva-a01-fixture-deps'];sys.dont_write_bytecode=True
import app as portal
logging.disable(logging.CRITICAL);cases=[]
for name,guards in [('baseline',{}),('remove_raw_validator',{'cale_webui_permisa':lambda _:True}),('remove_effective_validator',{'cale_trimisa_in_webui':lambda _:True}),('remove_both',{'cale_webui_permisa':lambda _:True,'cale_trimisa_in_webui':lambda _:True}),('deny_all',{'cale_webui_permisa':lambda _:False})]:
 with contextlib.ExitStack() as es:
  for k,v in guards.items():es.enter_context(mock.patch.object(portal,k,v))
  s=unittest.TestLoader().discover(str(F/'tests'),pattern='test_t232*.py');buf=io.StringIO();
  with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):result=unittest.TextTestRunner(stream=buf,verbosity=0).run(s)
  record={'mutation':name,'source_files_unchanged':True,'tests_executed':result.testsRun,'failures_or_subtest_failures':len(result.failures),'errors':len(result.errors),'failure_names':[str(o[0]) for o in result.failures][:25],'stdout_sha256':hashlib.sha256(buf.getvalue().encode()).hexdigest()};cases.append(record)
print([(x['mutation'],x['tests_executed'],x['failures_or_subtest_failures'],x['errors']) for x in cases]);(W/'original-test-mutants.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.UTC).isoformat(),'cases':cases,'method':'Unmodified original test modules exercised against runtime-only replacements of designated validator function(s). 13 unittest methods including parameterized subcases. Counts below are subcase failures, not a per-test score.'},indent=2)+'\n',encoding='utf8')
