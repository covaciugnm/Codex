from a12_r8_arch import *
import subprocess,shlex
# Reexecute original tools in a disposable export. No native or network or external API.
doc=searchdoc=None
script="""set -eu
r=/home/saga-server/Documents/EvA-Contab
t=$(mktemp -d /tmp/eva-a12-r8-tools.XXXXXXXX)
case "$t" in /tmp/eva-a12-r8-tools.????????) ;; *) exit 2;; esac
trap 'rm -rf -- "$t"' EXIT
mkdir -p "$t/repo" "$t/log" "$t/sentinel"
git -C "$r" archive BASE -- tools | tar -x -C "$t/repo"
cd "$t/repo"
echo -e '#!/usr/bin/env bash\\necho UNEXPECTED_REAL_ESCAPE >> "$AUDIT_SENTINEL"; exit 126' > "$t/sentinel/docker"
chmod 700 "$t/sentinel/docker"
export PATH="$t/sentinel:$PATH" AUDIT_SENTINEL="$t/log/escape" TZ=UTC
for s in tools/teste/t18/test_cabinet_env_spv.sh tools/teste/t10/test_pregateste_cabinet_t10.sh tools/teste/test_cabinet_orfane.sh tools/teste/test_cabinet_subnet.sh; do
 out="$t/log/$(basename "$s").txt"; echo "BEGIN $s"; rc=0; timeout 180s bash "$s" > "$out" 2>&1 || rc=$?; cat "$out"; echo "END $s return=$rc"
done
echo "unexpected_fallback_docker=$(test -e "$AUDIT_SENTINEL" && wc -l < "$AUDIT_SENTINEL" || echo 0)"
""".replace('BASE',BASE)
if __name__=='__main__':
 proc=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=script.encode(),capture_output=True,timeout=650);q=P/'T224_unelte_originale_simulate.log';q.write_bytes(proc.stdout+proc.stderr);print('rc',proc.returncode,'hash',sha(q));print('\n'.join(k for k in q.read_text(encoding='utf8',errors='replace').splitlines()if k.startswith(('END','unexpected','BEGIN'))))

