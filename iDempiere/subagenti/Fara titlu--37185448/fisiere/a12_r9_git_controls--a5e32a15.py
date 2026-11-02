from a12_r9_orig import *
import subprocess
shell=r'''set -eu
source=/home/saga-server/Documents/EvA-Contab
scratch=$(mktemp -d /tmp/eva-a12-r9-git.XXXXXXXX)
case "$scratch" in /tmp/eva-a12-r9-git.????????) ;; *) exit 2;; esac
trap 'rm -rf -- "$scratch"' EXIT
git init -q "$scratch/r"; cd "$scratch/r"; echo "$source/.git/objects" > .git/objects/info/alternates
git config user.email audit-local@example.invalid; git config user.name audit
cut=CODE
T314D=Documentatie/echipa-2026-10-09/T314-meniu-vanzari-canale-comenzi-facturare
T06D=Documentatie/echipa-2026-10-09/T06-comparatie-saga-2026
T204D=Documentatie/echipa-2026-10-09/T204-tiparire-loturi-ramase
path=idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/setup/EvaMetadata.java
git archive "$cut" "$T314D/dovezi-04/t0_lr4.sh" "$T314D/dovezi-10a-lotA/auto-verificare/criterii_statice.sh" "$T06D/dovezi-09-plan/scripturi/bloc_t171.py" "$T204D/dovezi-01-plan/t204_ferestre.py.txt"|tar xf -
echo "START T06"
v=c532f597279; b=$(git rev-parse c532f597279^1); echo "T06 old BASE=$b V=$v"
for r in "$v" "$cut"; do echo "run T06 $r"; rc=0; python3 -I "$T06D/dovezi-09-plan/scripturi/bloc_t171.py" . "$b" "$r" "$path" || rc=$?; echo "exit=$rc"; done
mkdir -p "$(dirname "$path")"; git read-tree "$v"; git show "$v:$path" > "$path"; printf '\n// Audit R9: martor în afara blocului.\n' >> "$path"; git add -- "$path"; tree=$(git write-tree); mv=$(echo 'mutant extra output audit'|git commit-tree "$tree" -p "$v");rc=0;python3 -I "$T06D/dovezi-09-plan/scripturi/bloc_t171.py" . "$v" "$mv" "$path"||rc=$?;echo "T06 extra-positive-violation RC=$rc"
echo "START T204"
for r in ae18abdfd7 2eac815f7a "$cut";do echo "T204 target $r";rc=0;python3 -I "$T204D/dovezi-01-plan/t204_ferestre.py.txt" . "$r" > "$scratch/ferestre" || rc=$?;grep '^#' "$scratch/ferestre"|tail -10;echo "fixture_outputs_lines=$(wc -l < "$scratch/ferestre"), rc=$rc";done
echo "START T314"
for target in 11c03ac3e1 "$cut";do 
 echo "T314 metrics $target";rc=0;bash "$T314D/dovezi-10a-lotA/auto-verificare/criterii_statice.sh" "$scratch/r" "$target" 4f3614927d > "$scratch/out" 2>&1||rc=$?;
 grep -E '^(# vârf|K-25|## K-22|## K-23|## K-12 / K-24|## K-20|garda_parteneri_scriere|fișiere scanate:|rc=|REZULTAT)' "$scratch/out";echo "hist-vs-cut full guard exit=$rc";done
echo "END"
'''.replace('cut=CODE','cut='+BASE)
if __name__=='__main__':
 p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=shell.encode(),capture_output=True,timeout=200);f=P9/'R9_scripturi_Git_T06_T204_T314.log';initial=P9/'R9_scripturi_Git_obiect_966aed025b_absent.log'
 if f.exists()and not initial.exists():initial.write_bytes(f.read_bytes())
 f.write_bytes(p.stdout+p.stderr);print(p.returncode,sha(f));print(p.stdout.decode('utf8')[:900])

