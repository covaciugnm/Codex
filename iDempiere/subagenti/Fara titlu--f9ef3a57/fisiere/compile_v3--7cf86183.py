import pathlib,json,subprocess,datetime,hashlib
L=pathlib.Path(__file__).parent
p=json.loads((L/'Preparation_v3.json').read_text(encoding='utf8'));(L/'classes_v3').mkdir();start=datetime.datetime.now(datetime.timezone.utc).isoformat();cp=subprocess.run(p['compile_command'],cwd=L,capture_output=True,timeout=60)
for suffix,b in [('stdout',cp.stdout),('stderr',cp.stderr)]:
 f=L/'logs'/('compile_v3.'+suffix+'.txt');assert not f.exists();f.write_bytes(b)
f=L/'logs/compile_v3.json';assert not f.exists();f.write_text(json.dumps({'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':p['compile_command'],'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(cp.stderr).hexdigest(),'product_source_changes':0},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'rc':cp.returncode,'stderr':cp.stderr.decode('utf8',errors='replace')},ensure_ascii=False))
