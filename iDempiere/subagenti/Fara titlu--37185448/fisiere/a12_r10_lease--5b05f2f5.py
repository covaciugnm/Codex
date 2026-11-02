from a12_r10_base import *
import time
server='saga-server@192.168.100.151';S='p01a12r10t06';actor='eva-contab-codex-'+S;sloc=Path('D:/CodexWork/a12-r10-local');sloc.mkdir(exist_ok=True);loc=sloc/'scratch.txt'
def ssh(command,input=None,timeout=30):
 return subprocess.run(['ssh','-o','BatchMode=yes',server,command],input=input,capture_output=True,timeout=timeout)
def current():
 x=loc.read_text().strip();assert re.fullmatch('/tmp/eva-contab-codex-p01a12r10t06[.][A-Za-z0-9]{8}',x);return x
def setup():
 if loc.exists():
  old=current();rc=ssh('test -f '+old+'/supervisor-log && tail -1 '+old+'/supervisor-log');assert (rc.returncode!=0 or rc.stdout.strip()==b'CLEANED'), 'There is already an active R10 fixture.'
 x=ssh('umask 077; mktemp -d /tmp/eva-contab-codex-p01a12r10t06.XXXXXXXX');x.check_returncode();loc.write_text(x.stdout.decode().strip());w=current()
 s=Path('D:/CodexWork/a12-r7/root-template.sh').read_text(encoding='utf8').replace('p01uizkr5',S).replace('P01.T259','P01.T171').replace('p01-t259','p01-t171').replace('runda r2','runda r10').replace('R2 cross synthetic WMS native ERP','A12 R10 auth banking comparator and typed UI').replace('R2 cross authorized audit P01 native ERP','A12 R10 test valid read flag, rerun and bank counts').replace('R2 cross test cabinet closed','A12 R10 bank comparator synthetic lab closed').replace('--durata 85','--durata 35').replace('$(seq 1 480)','$(seq 1 290)')
 lab=Path('D:/CodexWork/p01uizk-lab.py').read_text(encoding='utf8').replace('p01uizk-r5',S).replace('p01uizkr5',S)
 for name,data in [('supervisor.sh',s),('lab.py',lab)]:
  r=ssh('umask 077; cat > '+w+'/'+name,data.encode());r.check_returncode()
 cmd='cd '+w+' && (nohup bash supervisor.sh '+w+' >supervisor-log 2>&1 </dev/null &)'
 p=ssh(cmd);p.check_returncode();print(w)
if __name__=='__main__':setup()

