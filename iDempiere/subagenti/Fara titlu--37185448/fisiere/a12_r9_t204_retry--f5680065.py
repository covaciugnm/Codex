from a12_r9_orig import *
shell=r'''set -eu
s=$(mktemp -d /tmp/eva-a12-r9-204.XXXXXXXX);case "$s" in /tmp/eva-a12-r9-204.????????) ;;*) exit 1;;esac;trap 'rm -rf -- "$s"' EXIT
git init -q "$s/r";cd "$s/r";echo /home/saga-server/Documents/EvA-Contab/.git/objects>.git/objects/info/alternates
git update-ref refs/heads/master ae18abdfd7;git symbolic-ref HEAD refs/heads/master
dd=Documentatie/echipa-2026-10-09/T204-tiparire-loturi-ramase/dovezi-01-plan
git archive CODE "$dd"|tar xf -
for rev in ae18abdfd7 2eac815f7a CODE;do echo "R=$rev";ret=0;python3 -I "$dd/t204_ferestre.py.txt" . "$rev" > "$s/o" 2> "$s/err" ||ret=$?;cat "$s/err";grep '^#' "$s/o"|tail -10;echo "Candidaturi: $(wc -l < "$s/o"); rc=$ret";done
'''.replace('CODE',BASE)
r=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=shell.encode(),capture_output=True,timeout=100);p=P9/'T204_07_clasificator_ferestre.log';p.write_bytes(r.stdout+r.stderr);print(r.returncode,sha(p),r.stdout.decode()[-750:])

