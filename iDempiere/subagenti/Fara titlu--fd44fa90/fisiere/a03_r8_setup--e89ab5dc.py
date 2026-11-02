from a03_r8_base import *
docs={t:tuple('/'+x+'/' for x in dirs) for t,dirs in {'T58':['dovezi-51-auditor','dovezi-52-auditor','dovezi-13-poarta1'],'T159':['dovezi-10'],'T186':['dovezi-20-plan'],'T156':['dovezi-02-plan'],'T254':['dovezi-02-plan','dovezi-03-spec'],'T256':['dovezi-02-plan']}.items()}
def setup():
 selected=set()
 for t,ds in docs.items():
  for p in paths:
   dpath=path(t,'')
   if not p.startswith(dpath):continue
   if '/' not in p[len(dpath):] and p.endswith(('.md','.py','.tsv','.txt')) or any(d in p for d in ds) and p.endswith(('.sh','.py','.tsv','.txt','.java','.sql','.csv','.md')):selected.add(p)
 selected.update(['idempiere/plugins/com.eva.ro.contab/src','idempiere/plugins/com.eva.ro.contab/test','tools/teste/t256','tools/teste/garda_parteneri_scriere.py','tools/teste/garda_date_personale.sh'])
 valid=[]
 for p in selected:
  if p.startswith('tools/') and not any(k==p or k.startswith(p+'/') for k in paths):continue
  valid.append(p)
 cmd=f"""set -eu
BASE=$(mktemp -d /tmp/p01-a03r8-source-XXXXXX)
cd "$BASE"; git init -q
git -C {repo} rev-parse --path-format=absolute --git-path objects > "$BASE/.git/objects/info/alternates"
git update-ref refs/heads/audit-fixed {sha}
git symbolic-ref HEAD refs/heads/audit-fixed
git -C {repo} archive {sha} {' '.join(shlex.quote(p) for p in sorted(valid))} | tar -xf - -C "$BASE"
printf '%s' "$BASE"
"""
 r=ssh('bash -s',cmd.encode(),timeout=90);assert r.returncode==0,(r.stderr[:400]);w=r.stdout.decode();assert re.fullmatch(r'/tmp/p01-a03r8-source-[a-zA-Z0-9]+',w),w;(work/'remote.txt').write_text(w)
 print(w)
if __name__=='__main__':setup()

