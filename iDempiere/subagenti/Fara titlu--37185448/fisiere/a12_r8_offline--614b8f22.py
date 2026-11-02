from a12_r8_cases import *
import sys,contextlib,io,subprocess
q=P/'Ofline_situri';q.mkdir(exist_ok=True);base=repo/'tools/teste/t216'
def run():
 tests=[]
 for f in [base/'test_dublura_site.py',base/'site/test_paritate.py',base/'test_proba_fus.py']:
  p=subprocess.run([sys.executable,'-B','-X','utf8',f],cwd=f.parent,capture_output=True,timeout=65);dest=q/(f.name+'.log');dest.write_bytes(p.stdout+p.stderr);tests.append({'source_path':f.relative_to(repo).as_posix(),'source_hash':sha(f),'exit':p.returncode,'log':source(dest),'tail':[s[:350]for s in dest.read_text(encoding='utf8',errors='replace').splitlines()if re.search(r'rezultat|^OK|^test_|^Ran |^FAIL|contraproba|cod_diferit|caz_lipsa',s,re.I)][-12:]})
 # Exact fixture guard, with inspect doubled, and a tripwire for any non-read call. No Docker daemon.
 f=repo/'tools/teste/t227/fixtura_saga.py';spec=importlib.util.spec_from_file_location('t227x',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);guards=[]
 for name,label,st in [('eva-test-p01-t227-a12','P01.T999',4),('eva-test-p01-unrelated','P01.T227',4),('eva-test-p01-t227-a12','P01.T227',0)]:
  trace=[]
  def fake(cmd,**kw):
   trace.append(cmd[:2]);assert cmd[0]=='docker'
   if cmd[1]=='inspect':return subprocess.CompletedProcess(cmd,0,label,'')
   if cmd[1]=='exec'and 'SELECT 'in kw.get('input','')and 'INSERT 'not in kw.get('input',''):return subprocess.CompletedProcess(cmd,0,'cong|0\nscinit|0\nscrulaj|0\nmcost|0','')
   raise RuntimeError('unexpected mutating command')
  buff=io.StringIO()
  with unittest.mock.patch.object(m.subprocess,'run',side_effect=fake),contextlib.redirect_stdout(buff):
   try:m.main(['stare',name]);rc=0
   except SystemExit as e:rc=e.code
  guards.append({'prefix_correct':name.startswith('eva-test-p01-t227-'),'label':label,'oracle':st,'observed_exit':rc,'calls':trace,'result':buff.getvalue().strip()});assert rc==st
 wr(q/'Site_si_garda.json',{'utc':now(),'tests':tests,'T227_R2_038':guards,'T227_guard_source':{'path':f.relative_to(repo).as_posix(),'sha256':sha(f)},'external_calls':0})
if __name__=='__main__':run()

