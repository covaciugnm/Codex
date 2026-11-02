import subprocess,re,pathlib
w=pathlib.Path('D:/CodexWork/p01cross-supervisor.sh'); s=w.read_text(encoding='utf8').replace('p01crossr2','p01ex05r1').replace('R2 cross','EX05 CESIRO1').replace('synthetic WMS native ERP','synthetic CESIRO ERP provenance').replace('seq 1 550','seq 1 240').replace('--asteapta 30','--asteapta 8')
target=pathlib.Path('D:/CodexWork/a06ex');target.mkdir(exist_ok=True)
host='saga-server@192.168.100.151'; opts=['-o','BatchMode=yes','-o','StrictHostKeyChecking=yes']
dest=subprocess.check_output(['ssh',*opts,host,'umask 077; mktemp -d /tmp/eva-contab-codex-ex05.XXXXXXXX'],text=True).strip()
assert re.fullmatch(r'/tmp/eva-contab-codex-ex05\.[A-Za-z0-9]{8}',dest)
for name,data in [('supervisor.sh',s),('lab.py',pathlib.Path('D:/CodexWork/p01cross-lab.py').read_text(encoding='utf8').replace('eva-contab-codex-p01cross-r2.','eva-contab-codex-ex05.').replace('p01crossr2','p01ex05r1'))]:
 loc=target/name;loc.write_text(data,encoding='utf8',newline='\n');subprocess.run(['scp','-q',*opts,str(loc),host+':'+dest+'/'+name],check=True)
(target/'remote.txt').write_text(dest);print(dest,flush=True)
try:r=subprocess.run(['ssh',*opts,host,'bash '+dest+'/supervisor.sh '+dest+' >'+dest+'/events.log 2>&1'],timeout=2300);print('Closed',r.returncode,flush=True)
except Exception as e:print(type(e).__name__)

