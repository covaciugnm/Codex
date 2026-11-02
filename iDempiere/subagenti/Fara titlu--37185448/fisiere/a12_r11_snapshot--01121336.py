from a12_r10_publish import *
import subprocess,tarfile,io,datetime
P=E/'R11_plan_delta';dst=P/'A12_tracker_snapshot_v2';dst.mkdir(exist_ok=True);prev=rd(B/'capturi/MANIFEST.json');names=[v['file']for v in prev['files']];must={'00_STATUS_TASKURI.json','00_CORESPONDENTA_COD_CAPITOL.json','00_STATUS_FINALIZATE.json','00_STATUS_RAMASE.json','00_STARI_TASKURI.json','00_CATALOG_PROIECTE.json','00_CAPITOLE_PROIECTE.json'};assert set(names)==must
remote=r"""import hashlib,os,json,sys,subprocess,gzip,tarfile,io,pathlib,datetime
folder=pathlib.Path('/home/saga-server/Documents/EvA-Contab/Documentatie/echipa-2026-10-09')
check=subprocess.check_output(['docker','inspect','--format','{{json .Mounts}}','eva-claude-usage']).decode();mount=[d for d in json.loads(check)if d['Destination']=='/status'];assert len(mount)==1 and pathlib.Path(mount[0]['Source'])==folder and mount[0]['RW'] is False
names=NAMES;start=datetime.datetime.now(datetime.timezone.utc).isoformat();buf={};first={};last={}
for n in names:buf[n]=(folder/n).read_bytes();first[n]=hashlib.sha256(buf[n]).hexdigest()
for n in names:last[n]=hashlib.sha256((folder/n).read_bytes()).hexdigest()
assert first==last
status=json.loads(buf['00_STATUS_TASKURI.json']);assert isinstance(status,list)
with tarfile.open(fileobj=sys.stdout.buffer,mode='w:gz')as aa:
 for n,bytes_ in buf.items():
  x=tarfile.TarInfo(n);x.size=len(bytes_);aa.addfile(x,io.BytesIO(bytes_))
 jj=json.dumps({'source':'https://eva-org.com/claude/taskuri','mount':mount[0]['Source'],'target':mount[0]['Destination'],'writeable':mount[0]['RW'],'started':start,'ended':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha_before':first,'sha_after':last,'github_remote_head':subprocess.check_output(['git','-C','/home/saga-server/Documents/EvA-Contab','ls-remote','origin','refs/heads/master']).decode().strip()},ensure_ascii=False).encode()
 x=tarfile.TarInfo('manifest.json');x.size=len(jj);aa.addfile(x,io.BytesIO(jj))
""".replace('NAMES',repr(names))
if not(dst/'manifest.json').exists():
 pr=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','python3','-'],input=remote.encode(),capture_output=True,timeout=55);assert pr.returncode==0,pr.stderr.decode()[-660:]
 with tarfile.open(fileobj=io.BytesIO(pr.stdout),mode='r:gz')as arc:
  for member in arc.getmembers():
   assert member.name in must|{'manifest.json'};pp=dst/member.name;pp.write_bytes(arc.extractfile(member).read())
v=rd(dst/'manifest.json');assert v['sha_before']==v['sha_after']and all(sha(dst/n)==v['sha_before'][n]for n in names);print(sha(dst/'manifest.json'),v['started'],v['github_remote_head'],len(rd(dst/'00_STATUS_TASKURI.json')))

