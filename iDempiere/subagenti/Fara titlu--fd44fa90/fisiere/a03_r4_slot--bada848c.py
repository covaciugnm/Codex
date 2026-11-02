from a03_r4_exec import *
import re
ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=8','saga-server@192.168.100.151']
def sh(s):return sp.run(ssh+[s],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=18)
def clean_summary(raw):
 return [x[:390] for x in raw.splitlines() if re.search(r'REFUZ|PERMIS|slot=|foreign clients|webui=|remaining_owned|CLEANED|verified A07|BLOCAT|OCUPAT',x,re.I) and not re.search(r'pass|bearer|token',x,re.I)]
dest=os.environ.get('A03_OFFICIAL_TASK','58');assert dest in ('58','158')
pidfile=work/('remote_loc.txt' if dest=='58' else 'remote_loc_T158.txt');pattern=r'/tmp/eva-contab-codex-a03r4\.[a-zA-Z0-9]+'
def start():
 assert not pidfile.exists(),'do not allocate twice'
 loc=sh('umask 077; mktemp -d /tmp/eva-contab-codex-a03r4.XXXXXXXX');wd=loc.stdout.strip();assert re.fullmatch(pattern,wd),wd;pidfile.write_text(wd)
 sup=P('D:/CodexWork/p01cross-supervisor.sh').read_text(encoding='utf8').replace('eva-contab-codex-p01crossr2','eva-contab-codex-a03r4').replace('p01crossr2','a03r4').replace('P01.T220','P01.T58').replace('p01-t220','p01-t58').replace('--runda r2','--runda r4').replace('--asteapta 30 ','').replace('R2 cross authorized audit P01 native ERP','A03 R4 T58 signed isolated sequence test').replace('R2 cross synthetic WMS native ERP','A03 R4 T58 ERP fixture').replace('R2 cross test cabinet closed','A03 R4 T58 cabinet closed').replace('$(seq 1 550)','$(seq 1 150)')
 if dest=='158':sup=sup.replace('P01.T58','P01.T158').replace('p01-t58','p01-t158')
 lab=P('D:/CodexWork/p01cross-lab.py').read_text(encoding='utf8').replace('eva-contab-codex-p01cross-r2.','eva-contab-codex-a03r4.').replace('eva-contab-codex-p01crossr2','eva-contab-codex-a03r4')
 pilot='''from lab import *
import hashlib
t=auth('GardenAdmin',11,102,11); out={'when':now(),'scope':'Dedicated fresh synthetic GardenWorld; owner enforced by lab; no external integrations','actor':'GardenAdmin, client11, role102, org11','probes':[]}
for mm in ['2026-08','2026-09']:
  before=rows("SELECT gl_journal_id,documentno,docstatus,posted FROM adempiere.gl_journal WHERE ad_client_id=11 AND description LIKE 'INCHIDERE-VC "+mm+"%' ORDER BY gl_journal_id")
  assets=rows("SELECT count(*) FROM adempiere.a_asset WHERE ad_client_id=11 AND isactive='Y'");begin=sql('SELECT clock_timestamp()')
  data={'DateFrom':mm+'-01','DateTo':mm+('-31' if mm.endswith('08') else '-30'),'Operatie':'VC','EvaVerificOrdinea':True}
  code,obj=api(t,'POST','processes/eva_inchiderevenituri',data)
  after=rows("SELECT gl_journal_id,documentno,docstatus,posted FROM adempiere.gl_journal WHERE ad_client_id=11 AND description LIKE 'INCHIDERE-VC "+mm+"%' ORDER BY gl_journal_id")
  delta=rows("SELECT count(*) FROM adempiere.gl_journal WHERE ad_client_id=11 AND description LIKE 'INCHIDERE-VC "+mm+"%' AND created > '"+begin+"'::timestamptz")
  out['probes'].append({'month':mm,'assets':assets,'before':before,'request':data,'http':code,'summary':str(obj.get('summary',obj.get('detail','')))[:1000],'isError':obj.get('isError'),'after':after,'new_journals':delta})
  if 'pasul 5' in out['probes'][-1]['summary']:break
(W/'pilot.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(W/'finish').touch()
'''
 for nm,b in [('super.sh',sup),('lab.py',lab),('pilot.py',pilot)]:
  p=work/nm;p.write_text(b,encoding='utf8',newline='\n');x=sp.run(['scp','-q','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',p,'saga-server@192.168.100.151:'+wd+'/'+nm],capture_output=True,text=True,timeout=22);assert x.returncode==0,x.stderr[:250]
 q=sh(f'cd {wd} && chmod 700 super.sh && (nohup bash super.sh {wd} > lifecycle.log 2>&1 < /dev/null & echo $! > supervisor.pid) && cat supervisor.pid');dump1('T58_slot_status.json',{'utc':now(),'owner':'eva-contab-codex-a03r4','resource_task':'P01.T'+dest,'requested_legacy_criterion':'P01.T58','requested':'§61 coada_builduri.sh cere, official containere_test.sh allocation; cleanup checked per this owner only','state':'REQUESTED','pid':q.stdout.strip(),'workdir':wd,'evidence':'No production data; per-agent fixture and owner check.'})
def inspect():
 wd=pidfile.read_text();assert re.fullmatch(pattern,wd);res=sh(f'cd {wd} && printf "ready " && test -f ready && echo yes || true; cd {wd} && test -f lifecycle.log && tail -24 lifecycle.log'); sc=clean_summary(res.stdout)
 if sh(f'test -f {wd}/pilot.json').returncode==0:
  z=sh(f'if test -f {wd}/pilot2.json; then cat {wd}/pilot2.json; else cat {wd}/pilot.json; fi');val=json.loads(z.stdout);dump1('T58_native_gate.json',val)
 elif sh(f'test -f {wd}/ready').returncode==0:
  started=sh(f'cd {wd} && if mkdir pilot_started 2>/dev/null; then (nohup python3 pilot.py >pilot.log 2>&1 < /dev/null &); fi'); sc.append('pilot started on exclusive ready cabinet')
 elif sh(f'test -f {wd}/supervisor.pid && kill -0 $(cat {wd}/supervisor.pid) 2>/dev/null').returncode!=0:sc.append('supervisor finished')
 dump1('T58_slot_status.json',{'utc':now(),'owner':'eva-contab-codex-a03r4','resource_task':'P01.T'+dest,'requested_legacy_criterion':'P01.T58','status':sc,'pilot_captured':(probe/'T58_native_gate.json').exists(),'owner_containers':sh("docker ps -a --filter label=eva.sesiune=eva-contab-codex-a03r4 --format '{{.Names}}'").stdout.splitlines(),'working_dir':wd})
def finish():
 wd=pidfile.read_text();assert re.fullmatch(pattern,wd);sh(f'touch {wd}/finish');inspect()
if __name__=='__main__':{'start':start,'inspect':inspect,'finish':finish}[sys.argv[1]]()
