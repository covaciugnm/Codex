from a12_r10_base import *
from a12_r8_arch_survs import a,txt
from concurrent.futures import ThreadPoolExecutor
doc=next(z for z in a if '/T201-'in z['file']and z['file'].endswith('/K-25.txt'));table=[(int(n),int(m),s)for n,m,s in re.findall(r'^(\d+) - / (\d+) \+ +(.*)$',txt(doc),re.M)];assert len(table)==8
sh=r"""set -eu
rt=/home/saga-server/Documents/EvA-Contab;td=$(mktemp -d /tmp/eva-a12-r10-git.XXXXXXXX)
case "$td" in /tmp/eva-a12-r10-git.????????);;*) exit 2;;esac
trap 'rm -rf -- "$td"' EXIT
git init -q "$td/r"; cd "$td/r"; echo "$rt/.git/objects" >.git/objects/info/alternates
git config user.email audit-local@example.invalid;git config user.name audit-local
for ver in aa987e558ae 984a00c1117;do b=$(git rev-parse "$ver^1");rc=0;git merge-base --is-ancestor "$ver" BASE ||rc=$?;echo "VERSION $ver parent=$b ancestor=$rc"
 for file in FILES;do vals=$(git diff --numstat "$b..$ver" -- "$file"); echo "FILE $file $vals";done
 git diff --check "$b..$ver" -- FILES;echo "DIFFCHECK=$?";git merge-tree --write-tree "$b" "$ver" >/dev/null;echo "MERGE_TREE=$?"
done
cd "$td";mkdir export;git -C "$rt" archive BASE -- tools/teste idempiere |tar -x -C export
cd export
python3 tools/teste/garda_parteneri_scriere.py;echo "GLOBAL_RC=$?";python3 - <<'PY'
import sys
sys.path.insert(0,"tools/teste")
import garda_parteneri_scriere as g
print("FILES_SCAN",sum(1 for _ in g.fisiere(g.CAI_IMPLICITE+[g.DOSARE_TASKURI])))
PY
printf 'import urllib.request\nurllib.request.urlopen("https://partener.example.invalid",data=b"R10")\n' > idempiere/plugins/transport_r10_canary.py
set +e;python3 tools/teste/garda_parteneri_scriere.py --cai idempiere/plugins/transport_r10_canary.py;echo "GUARD_CANARY_RC=$?";set -e
for tn in T220-corelare-motor-defect-corelez T224-efactura-pornire;do
 echo "AUDITDOC $tn tranche source scope -- only documentation folder";git -C "$rt" archive BASE -- Documentatie/echipa-2026-10-09/"$tn" |tar -xf -
 dir="Documentatie/echipa-2026-10-09/$tn";rc=0;bash tools/teste/garda_date_personale.sh --director "$dir" > "$td/guarddata" 2>&1 ||rc=$?;echo "DATA_RC=$rc";grep -E '^#.*(?:nume|zona strictă)' "$td/guarddata"|tail -2 ||true
 rc=0;bash tools/teste/garda_date_personale.sh --secrete --director "$dir" > "$td/guardsecrets" 2>&1 ||rc=$?;echo "SECRET_RC=$rc";grep -E '^#.*(secrete|fișiere|linii)' "$td/guardsecrets"|tail -2||true;done
""".replace('BASE',BASE).replace('FILES;',shlex.join(t[-1]for t in table)+';').replace('-- FILES;','-- '+shlex.join(t[-1]for t in table)+';')
if __name__=='__main__':
 v=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=sh.encode(),capture_output=True,timeout=165);f=P10/'Evaluare_T201_T220_T224.log';f.write_bytes(v.stdout+v.stderr);print(v.returncode,sha(f));print(v.stdout.decode('utf8')[-550:])

