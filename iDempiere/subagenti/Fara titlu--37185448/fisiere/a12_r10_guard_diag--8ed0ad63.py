from a12_r10_base import *
cmd=r'''set -eu
r=/home/saga-server/Documents/EvA-Contab; s=$(mktemp -d /tmp/eva-a12-r10-gdiag.XXXXXXXX);case "$s" in /tmp/eva-a12-r10-gdiag.????????);;*)exit 2;;esac;trap 'rm -rf -- "$s"' EXIT;cd "$s"
git -C "$r" archive CUT tools/teste |tar xf -;policy=tools/teste/garda_date_personale.hashes
echo 'Git tree policy presence:'
git -C "$r" ls-tree -l CUT -- "$policy"
if test -f "$r/$policy";then echo "untracked or working file present sha256=$(sha256sum "$r/$policy"|cut -d' ' -f1)";fi
for tn in T220-corelare-motor-defect-corelez T224-efactura-pornire;do
 dir="Documentatie/echipa-2026-10-09/$tn";git -C "$r" archive CUT "$dir"|tar xf -; rc=0;bash tools/teste/garda_date_personale.sh --director "$dir" >datareport 2>&1||rc=$?;printf 'dir=%s rc=%s\n' "$tn" "$rc"; grep -E '^([[:alpha:]]+Error:|# zona strictă|# fișiere verificate|# linii verificate|fatal:|usage:|unrecognized)' datareport|head -8||true
done
'''.replace('CUT',BASE)
p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=cmd.encode(),capture_output=True,timeout=120);f=P10/'Diagnostic_garda_date_personale.log';f.write_bytes(p.stdout+p.stderr);print(p.returncode,sha(f),p.stdout.decode()[-950:])
