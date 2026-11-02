from pathlib import Path
import subprocess as sp,json,hashlib,datetime
w=Path('D:/CodexWork/a05r8');out=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R8_pregatire/A05')
import importlib.machinery
a=importlib.machinery.SourceFileLoader('r8git',str(w.parent/'a05r8-git.py'))
# Import module's pure helpers only, without triggering modes.
import sys
sys.argv.append('unused')
mod=a.load_module()
codes={n:(w/n).read_text(encoding='utf8') for n in ['criterii_statice.sh','criterii_schelet.sh','mutant_c24.sh']}
program=mod.header+'codes='+repr(codes)+"""
import tempfile,pathlib
T163='9980254afc56f7a852e8b7c90dc6b3ba1d81f491';T333=g('rev-parse','d6068a9fa9^{commit}');src='/home/saga-server/Documents/EvA-Contab'
repo=pathlib.Path(tempfile.mkdtemp(prefix='eva-audit-a05r8-mutants-'))
def cmd(*a,env=None,data=None):return sp.run(a,input=data,cwd=repo,env=env or os.environ,capture_output=True)
assert cmd('git','init','--quiet','--template=','-b','master').returncode==0
alt=repo/'.git/objects/info/alternates'; alt.write_text(g('rev-parse','--path-format=absolute','--git-path','objects')+'\n')
os.environ.update({'GIT_AUTHOR_NAME':'A05 synth','GIT_COMMITTER_NAME':'A05 synth','GIT_AUTHOR_EMAIL':'a05@example.invalid','GIT_COMMITTER_EMAIL':'a05@example.invalid','GIT_NO_LAZY_FETCH':'1'})
cmd('git','update-ref','refs/heads/master',cut)
d=repo/'tools/teste/t333';d.mkdir(parents=True)
for n in ('criterii_schelet.sh','mutant_c24.sh'):(d/n).write_text(codes[n])
res=[]
for rev in (T333,cut):
 c=cmd('bash',str(d/'mutant_c24.sh'),rev);res.append({'task':'T333','rev':rev,'exit':c.returncode,'text':c.stdout.decode('utf8','replace'),'diagnostic':c.stderr.decode('utf8','replace')[:380]})
p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/corelare/ArticoleDiverse.java'
for rev in (T163,cut):
 ix=repo/'scratch.index';e=dict(os.environ,GIT_INDEX_FILE=str(ix));assert cmd('git','read-tree',rev,env=e).returncode==0
 old=git('show',rev+':'+p);new=old+b'\nclass AuditOnly { static String sql = "UPDATE m_storageonhand SET qtyonhand=99"; }\n'
 mb=cmd('git','hash-object','-w','--stdin',data=new).stdout.strip().decode();assert cmd('git','update-index','--cacheinfo','100644,'+mb+','+p,env=e).returncode==0
 tree=cmd('git','write-tree',env=e).stdout.strip().decode(); mut=cmd('git','commit-tree',tree,'-p',rev,'-m','A05 synthetic mutation C3').stdout.strip().decode()
 res2=cmd('bash','-s','--',mut,g('rev-parse',T163+'^'),data=codes['criterii_statice.sh'].encode());line=next(x for x in res2.stdout.decode().splitlines() if x.startswith('C-3 '))
 res.append({'task':'T163','rev':rev,'mutant_commit':mut,'mutant_blob_oid':mb,'expected':'at least 1 match after mutation','exit':res2.returncode,'text':line})
files=['idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+f for f in ['form/WArticoleDiverseForm.java','form/WInventarForm.java','form/InventarDiverse.java','corelare/ArticoleDiverseProces.java']]
changes=git('diff',g('rev-parse',T163+'^'),cut,'--',*files).decode()
rx=re.compile(r'(new (Label|Button|Window)|setValue|setTooltiptext|showNotification|Messagebox\.show|throw new [A-Za-z]*Exception|stare|notifica)\(\s*"[^"]*[a-zăâîșțA-Z]{3,}')
for path in files:
 text=git('show',cut+':'+path).decode()
 for n,line in enumerate(text.splitlines(),1):
  if rx.search(line) and '+'+line in changes.splitlines():
   b=git('blame','--porcelain','-L',str(n)+','+str(n),cut,'--',path).decode().splitlines()[0].split()[0]
   res.append({'task':'T163','case':'C6 actual regex hit attribution','rev':cut,'file':path,'line':n,'code':line.strip(),'git_blame':b,'commit_subject':g('show','-s','--format=%s',b)})
print(json.dumps(res,ensure_ascii=False))
"""
program=program.replace("+'\n')","+'\\n')").replace("old+b'\nclass","old+b'\\nclass").replace('=99"; }\n\'','=99"; }\\n\'')
data=json.loads(mod.remote(program));mod.dump(out/'Mutanti_si_atribuire.json',data)
