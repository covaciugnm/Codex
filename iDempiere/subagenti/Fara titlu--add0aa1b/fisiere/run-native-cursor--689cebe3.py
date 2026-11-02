from pathlib import Path
import os,sys,subprocess,json,time
w=Path('D:/CodexWork/a06ex');remote=(w/'remote.txt').read_text().strip();host='saga-server@192.168.100.151';opts=['-o','BatchMode=yes','-o','StrictHostKeyChecking=yes']; subprocess.run(['scp','-q',*opts,str(w/'native-cursor.py'),host+':'+remote+'/native-cursor.py'],check=True)
out=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/supliment_CESIRO1/probe/EX04-evidence')
for stage,fault in [('setup','none'),('429-empty','429'),('500-empty','500'),('truncated-empty','truncated'),('partial-empty','partial'),('fault-in-detail','detail500'),('commit-before-cursor','none'),('restart','none'),('B-identity','none'),('late-update','none'),('stable-replay','none')]:
 if (out/('native-'+stage+'.json')).exists():continue
 (w/'fault-cursor.txt').write_text(fault)
 if stage=='late-update':
  (w/'advance-cursor').write_text('now')
  for _ in range(20):
   if (w/'advanced-cursor').exists():break
   time.sleep(.4)
  assert (w/'advanced-cursor').exists()
 p=subprocess.run(['ssh',*opts,host,'cd '+remote+' && python3 native-cursor.py '+stage],capture_output=True,timeout=70)
 if p.returncode:raise RuntimeError(p.stderr.decode('utf8','replace')[-750:])
 r=json.loads(p.stdout.decode('utf8'));(out/('native-'+stage+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(stage,r['process'],[(a[0],a[1]) for a in r['after']['cursor']],len(r['after']['rows']),flush=True)

