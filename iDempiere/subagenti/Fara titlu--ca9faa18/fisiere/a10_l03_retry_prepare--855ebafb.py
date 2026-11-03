from pathlib import Path
import importlib.util,json
p=Path('D:/CodexWork/a10_l03_shell.py');s=importlib.util.spec_from_file_location('harness',p);m=importlib.util.module_from_spec(s)
import sys
sys.argv=['harness','library'];s.loader.exec_module(m)
m.L=Path('D:/CodexWork/a10-r12-l03/shell_v2');m.L.mkdir(exist_ok=False)
m.DISPATCH=m.DISPATCH.replace('sys.dont_write_bytecode=True',"sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')")
m.DEPENDENCY=m.DEPENDENCY.replace('name=Path(sys.argv[0]).name','name=Path(__file__).name')
for name,cfg in [('normal',{}),('partner_fail',{'partner_rc':41}),('secret_fail',{'secret_rc':42}),('merge_conflict',{'conflict':True}),('cleanup_fail',{'partner_rc':41,'rm_fail':1})]:m.prep10(name,cfg)
for name,cfg in [('normal',{}),('changed',{'jar':'changed'}),('missing_class',{'jar':'missing_class'}),('duplicate_last_base',{'jar':'duplicate_last_base'}),('duplicate_last_variant',{'jar':'duplicate_last_variant'}),('corrupt',{'jar':'corrupt'}),('missing_jar',{'jar':'missing_jar'}),('child_fail',{'partner_rc':41,'secret_rc':42,'runner_rc':43})]:m.prep01(name,cfg)
m.put(m.L/'Preparation_manifest.json',{str(p.relative_to(m.L)):m.sha(p) for p in m.L.glob('*/Case_preflight.json')})
print(json.dumps({'cases':13,'manifest':m.sha(m.L/'Preparation_manifest.json')}))
