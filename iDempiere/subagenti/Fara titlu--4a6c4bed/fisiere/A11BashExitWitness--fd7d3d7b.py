import subprocess,json,hashlib,datetime
from pathlib import Path
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A11/Val03_loturi')
code='false; echo "after_false_with_success_substitution=$(true); rc=$?"; true; echo "after_true_with_failed_substitution=$(false); rc=$?"'
p=subprocess.run(['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc','-c',code],capture_output=True,text=True,encoding='utf-8',check=True)
assert p.stdout.splitlines()==['after_false_with_success_substitution=; rc=0','after_true_with_failed_substitution=; rc=1']
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'A11 independent','method':'Bash generic built-ins only; no repository/product execution or filesystem mutation by child','script':code,'stdout':p.stdout,'stderr':p.stderr,'rc':p.returncode,'unique_language_controls':2,'oracle':'Expected previous-command statuses are 1 then 0; output is changed by command-substitution statuses 0 then 1. This demonstrates the shell evaluation mechanism only.','application_relevance':'I10 garzi.sh echoes $(git rev-parse ...) before $? after merge-tree; actual Git-conflict witness is separate executor evidence.','product_score':None,'owned_background_processes':0}
out=O/'Control_A11_Bash_exit_substitution_v1.json';assert not out.exists();out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
