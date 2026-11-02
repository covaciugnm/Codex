import pathlib,tempfile,hashlib,os,subprocess,json
root=pathlib.Path('D:/CodexWork/eva-audit-p01-readonly-20261102/tools/status')
def msys(p):return '/'+p.drive[0].lower()+'/'+p.as_posix()[3:]
records=[]
with tempfile.TemporaryDirectory(prefix='a11-queue-only-') as tmp:
 test=pathlib.Path(tmp).resolve();qb=test/'q';qm=test/'m';qb.mkdir();qm.mkdir();marker=test/'a11-only-marker';keeper=test/'unrelated'
 env=dict(os.environ,EVA_COADA_DIR=msys(qb),EVA_COADA_REG=msys(test/'build.jsonl'),EVA_COADA_MONTARI_DIR=msys(qm),EVA_COADA_MONTARI_REG=msys(test/'deploy.jsonl'));keeper.write_text('sentinel')
 for n in ['coada_builduri.sh','coada_montari.sh']:
  marker.write_text('temporary fixture only')
  p=subprocess.run(['C:/Program Files/Git/bin/bash.exe',msys(root/n),'elibereaza','../a11-only-marker'],cwd=test,env=env,capture_output=True,timeout=12)
  records.append({'script':n,'sha256':hashlib.sha256((root/n).read_bytes()).hexdigest(),'returncode':p.returncode,'synthetic_marker_survived':marker.exists(),'second_unrelated_file_survived':keeper.exists(),'stdout':p.stdout.decode('utf8','replace')[:160],'stderr':p.stderr.decode('utf8','replace')[:160]})
assert all(not x['synthetic_marker_survived'] and x['second_unrelated_file_survived'] for x in records)
out=pathlib.Path(__file__).parent/'A10_queue_traversal.json';out.write_text(json.dumps({'tests':records,'scope':'Pinned scripts, Git Bash, two test queue directories/sibling markers in a new temporary directory. Deployment and real queues untouched.'},ensure_ascii=False,indent=2),encoding='utf8');print(records)

