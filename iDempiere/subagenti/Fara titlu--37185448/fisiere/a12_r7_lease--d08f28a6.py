from a12_r7_pg_cui import *
s=(T7/'root-template.sh').read_text(encoding='utf8').replace('p01uizkr5','p01a12r7t06').replace('P01.T259','P01.T06').replace('p01-t259','p01-t06').replace('runda r2','runda r7').replace('R2 cross synthetic WMS native ERP','A12 R7 native SAGA archive CUI validation').replace('R2 cross authorized audit P01 native ERP','A12 R7 compare SAGA archive on isolated GardenWorld').replace('R2 cross test cabinet closed','A12 R7 test cabinet closed').replace('--durata 85','--durata 30').replace('$(seq 1 480)','$(seq 1 240)')
new=sp.check_output(['ssh','-o','BatchMode=yes',server,'umask 077; mktemp -d /tmp/eva-contab-codex-p01a12r7t06.XXXXXXXX']).decode().strip();assert re.fullmatch(r'/tmp/eva-contab-codex-p01a12r7t06\.[a-zA-Z0-9]+',new)
(T7/'current_fixture_path.txt').write_text(new,encoding='utf8');(T7/'supervisor_ours.sh').write_text(s,encoding='utf8')
def remote(cmd,input=None):return sp.run(['ssh','-o','BatchMode=yes',server,cmd],input=input,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=25)
r=remote('cat >'+new+'/supervisor.sh && chmod 700 '+new+'/supervisor.sh',s.encode());assert r.returncode==0,r.stdout
lab=sp.check_output(['ssh','-o','BatchMode=yes',server,'cat /tmp/eva-contab-codex-p01uizk-r5.vUjauFBh/lab.py']).decode().replace('p01uizk-r5','p01a12r7t06').replace('p01uizkr5','p01a12r7t06');r=remote('cat >'+new+'/lab.py',lab.encode());assert r.returncode==0
r=remote('cd '+new+' && nohup bash supervisor.sh '+new+' </dev/null >supervisor-log 2>&1 &');print('requested',new,r.returncode)

