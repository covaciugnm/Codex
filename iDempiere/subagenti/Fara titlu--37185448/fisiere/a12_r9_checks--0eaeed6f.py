from a12_r9_orig import *
shell=r"""set -eu
d=$(mktemp -d /tmp/eva-a12-r9-lists.XXXXXXXX);case "$d" in /tmp/eva-a12-r9-lists.????????);;*)exit 2;;esac;trap 'rm -rf -- "$d"' EXIT
r=/home/saga-server/Documents/EvA-Contab;c=BASE;target='Documentatie/echipa-2026-10-09/T220-corelare-motor-defect-corelez'
mkdir -p "$d/work"; cd "$d/work"
git -C "$r" archive "$c" tools/status Documentatie/echipa-2026-10-09/00_CHECKLIST_DEFECTE.json "$target/04_raport_implementare.md" "$target/10_RR_executant_cod_r1.md" |tar xf -
before=$(git -C "$r" log -1 --format=%H "$c" -- "$target/04_raport_implementare.md");echo "cut=$c report_last_commit=$before";git -C "$r" ls-tree -l "$c" -- "$target/04_raport_implementare.md" "$target/10_RR_executant_cod_r1.md" tools/status/checklist_defecte.py Documentatie/echipa-2026-10-09/00_CHECKLIST_DEFECTE.json
for file in "$target/04_raport_implementare.md" "$target/10_RR_executant_cod_r1.md";do rc=0;python3 tools/status/checklist_defecte.py valideaza --auto-audit "$file" ||rc=$?;echo "target=$file RC=$rc";done
python3 - "$target/04_raport_implementare.md" "$d/bad.md" <<'PY'
import re,sys
s=open(sys.argv[1]).read().splitlines();r=False;out=[]
for l in s:
 if not r and re.match(r'\\|\\s*X[0-9]+\\s*\\|',l):r=True;continue
 out.append(l)
if not r:raise SystemExit('missing X row')
open(sys.argv[2],'w').write('\\n'.join(out)+'\\n')
print('one original X row removed')
PY
rc=0;python3 tools/status/checklist_defecte.py valideaza --auto-audit "$d/bad.md" ||rc=$?;echo "X mutant RC=$rc"
""".replace('BASE',BASE).replace(r'\\|',r'\|').replace(r'\\s',r'\s').replace(r'\\n',r'\n')
if __name__=='__main__':
 p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=shell.encode(),capture_output=True,timeout=100);f=P9/'T220_validator_documentar.log';f.write_bytes(p.stdout+p.stderr);print(p.returncode,sha(f),p.stdout.decode('utf8')[-850:])

