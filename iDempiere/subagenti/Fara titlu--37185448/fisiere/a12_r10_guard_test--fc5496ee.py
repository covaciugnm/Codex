from a12_r10_base import *
cmd=r'''set -eu
r=/home/saga-server/Documents/EvA-Contab;s=$(mktemp -d /tmp/eva-a12-r10-guard.XXXXXXXX);case "$s" in /tmp/eva-a12-r10-guard.????????);;*)exit 2;;esac;trap 'rm -rf -- "$s"' EXIT
cd "$s";git -C "$r" archive CUT tools/teste/garda_parteneri_scriere.py tools/teste/garda_parteneri_scriere.permise tools/teste/garda_date_personale.py tools/teste/garda_date_personale.sh || true
'''.replace('CUT',BASE)
cmd=r'''set -eu
r=/home/saga-server/Documents/EvA-Contab;s=$(mktemp -d /tmp/eva-a12-r10-guard.XXXXXXXX);case "$s" in /tmp/eva-a12-r10-guard.????????);;*)exit 2;;esac;trap 'rm -rf -- "$s"' EXIT
cd "$s"; git -C "$r" archive CUT tools/teste | tar xf -
mkdir -p cases
cat >cases/a.py <<'PY'
def do_not_execute():
 network.write("https://api.stripe.com/v1/payment_intents",method="POST")
PY
cat >cases/b.py <<'PY'
def do_not_execute():
 network.read("https://api.stripe.com/v1/payment_intents",method="GET")
PY
for f in cases/{a,b}.py;do rc=0;python3 tools/teste/garda_parteneri_scriere.py --cai "$f" >"$s/c" 2>&1||rc=$?;echo "file=$f rc=$rc";head -1 "$s/c";done
for tn in T220-corelare-motor-defect-corelez T224-efactura-pornire;do
 dir="Documentatie/echipa-2026-10-09/$tn";git -C "$r" archive CUT "$dir"|tar xf -; rc=0;bash tools/teste/garda_date_personale.sh --director "$dir" >"$s/datareport" 2>&1||rc=$?;echo "dir=$tn data-rc=$rc";grep -E '^(# zona strictă|# fișiere verificate|# linii verificate)' "$s/datareport" |tail -2 ||true
done
'''.replace('CUT',BASE)
if __name__=='__main__':
 p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=cmd.encode(),capture_output=True,timeout=120);f=P10/'Etalon_garda_parteneri_si_T33.log';f.write_bytes(p.stdout+p.stderr);print(p.returncode,sha(f),p.stdout.decode()[-450:])

