import subprocess,json,pathlib,datetime
out=pathlib.Path(r'\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01\executie\A01');rows=[]
for c,keys in [('eva-contab-backend',['EVA_ENV','EVA_AUTH_ENFORCE','EVA_MFA_ENFORCE','EVA_TENANT_AUTHZ','IDEMPIERE_MOCK','EVA_IDM_MEMBER_WRITE']),('eva-contab-frontend',['EVA_ME_CACHE_TTL'])]:
 for k in keys:
  p=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',f'docker exec {c} printenv {k}'],capture_output=True,text=True,timeout=10);raw=p.stdout.strip();rows.append({'container':c,'key':k,'value':raw if p.returncode==0 and len(raw)<28 else None,'outcome':('SET' if p.returncode==0 else 'UNSET' if p.returncode==1 and not p.stderr.strip() else 'ERROR')})
for c in ('eva-contab-frontend','eva-contab-storefront','eva-contab-backend'):
 p=subprocess.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151',"docker inspect --format '{{range .Mounts}}{{if eq .Destination \"/var/run/docker.sock\"}}{{.Destination}} RW={{.RW}}{{end}}{{end}}' "+c],capture_output=True,text=True,timeout=10);rows.append({'container':c,'type':'docker socket mount only','value':p.stdout.strip(),'rc':p.returncode})
(out/'runtime_flags.json').write_text(json.dumps({'timestamp':datetime.datetime.now(datetime.UTC).isoformat(),'method':'SSH read-only, only named non-secret policy variables and docker.sock mount','rows':rows},indent=2),encoding='utf-8');print(rows)
