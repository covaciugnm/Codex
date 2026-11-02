from a12_r10_lease import *
from a12_r8_arch_survs import a,txt
w=current();basepath='idempiere/plugins/com.eva.ro.contab/com.eva.ro.contab_13.0.0.jar';srcs=[z for z in a if '/T06-comparatie-saga-2026/dovezi-40-audit/'in z['file']and ('produs_imbinare' in z['file']or re.search(r'C-17|X110',z['file']))];print([(s['file'],txt(s)[:450])for s in srcs])
cmd='''set -u
r=/home/saga-server/Documents/EvA-Contab
temp=$(mktemp -d /tmp/r10-a12-merge.XXXXXXXX);case "$temp" in /tmp/r10-a12-merge.????????);;*) exit 10;;esac;trap 'rm -rf -- "$temp"' EXIT;git init --bare -q "$temp/one";echo "$r/.git/objects" >"$temp/one/objects/info/alternates"
rc=0;git -C "$temp/one" merge-tree --write-tree 2fe3d2300e 5be8e9d79e || rc=$?; echo "historical exact master and branch MERGE_RC=$rc"
rc=0;git -C "$temp/one" merge-tree --write-tree CUT c532f59727 ||rc=$?;echo "latest/official integration MERGE_RC=$rc"
for v in c532f59727 CUT;do printf '%s jar blob=' "$v";git -C "$r" rev-parse "$v:PATH1";git -C "$r" show "$v:PATH1"|md5sum;done
cd ROOM
c=$(cat auditor-app);test "$(docker inspect -f '{{index .Config.Labels "eva.sesiune"}}' "$c")" = eva-contab-codex-p01a12r10t06 || exit 11
docker exec "$c" sh -c 'find /opt/idempiere -name com.eva.ro.contab_13.0.0.jar -type f -exec md5sum {} \\;'
docker exec "$c" md5sum /opt/idempiere/saga-archives/A12R10_BANK_168.sqlite
md5sum A12R10_BANK_168.sqlite
docker exec "$c" sha256sum /opt/idempiere/saga-archives/A12R10_BANK_168.sqlite
sha256sum A12R10_BANK_168.sqlite
'''.replace('CUT',BASE).replace('PATH1',basepath).replace('ROOM',w)
out=ssh('bash -s',cmd.encode(),timeout=45);assert out.returncode==0,out.stderr.decode()[:250];p=P10/'T06_merge_arhiva_si_JAR.json';wr(p,{'utc':now(),'commands':cmd,'cutoff':BASE,'historical_verified_git_files':[{'file':s['file'],'blob':s.get('blob',s.get('git_blob')),'text':txt(s)[:620]}for s in srcs],'outputs':out.stdout.decode().splitlines(),'stderr':out.stderr.decode().splitlines(),'qualification':'Archive SHA identique à l’entrée créée avant les processus, source et conteneur hashés; ce n’est pas la base q31 originale; dernière version historique et HEAD ne sont pas interchangeables.'});print(sha(p),out.stdout.decode()[-820:])
