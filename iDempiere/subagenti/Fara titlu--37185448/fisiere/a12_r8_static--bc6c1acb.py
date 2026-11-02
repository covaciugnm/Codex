from a12_r8_arch import *
script=r"""set -eu
r=/home/saga-server/Documents/EvA-Contab
d=$(mktemp -d /tmp/eva-a12-r8-git.XXXXXXXX)
case "$d" in /tmp/eva-a12-r8-git.????????) ;; *) exit 2;; esac
trap 'rm -rf -- "$d"' EXIT
git init -q "$d/r"; cd "$d/r"; printf '%s\n' "$r/.git/objects" > .git/objects/info/alternates
H=BASE; B=5a1b35454d63baef76c605b47ef650f79e387e2a; V=007458e202
git update-ref refs/heads/master "$B"; git symbolic-ref HEAD refs/heads/master
mkdir -p tools/teste/t227; git show "$H":tools/teste/t227/verificari_statice.sh > tools/teste/t227/verificari_statice.sh
for k in old head; do rev="$V"; [ "$k" != head ] || rev="$H"; out="$d/out-$k"; echo "=== CASE $k rev=$rev historical-base=$B"; z=0; bash tools/teste/t227/verificari_statice.sh "$rev" "$out" >"$d/progress" 2>&1 || z=$?; cat "$d/progress"; echo "T227 COMPLETE $k rc=$z"; for id in K-2 K-4c K-9a K-10a K-12a K-16 K-24 K-27 K-28; do echo "TRACE $k $id"; cat "$out/$id.txt"; done; done
echo "T204_DIFF_COMPARE"
BB=ae18abdfd7; VV=2eac815f7a; git diff "$BB..$VV" -- '*/CatalogTiparire.java' | grep -cE '^[+-].*"W[A-Za-z0-9]+Form"' || true
git show "$BB":idempiere/plugins/com.eva.ro.contab/test/fixtures/t29_tipar_vechi.tsv | awk -F'\t' '!/^#/ && NF {a[$3]++} END{for(k in a) print "BB",k,a[k]}'
git show "$H":idempiere/plugins/com.eva.ro.contab/test/fixtures/t29_tipar_vechi.tsv | awk -F'\t' '!/^#/ && NF {a[$3]++} END{for(k in a) print "HEAD",k,a[k]}'
echo "T204_GIT_MERGETREE"
git merge-tree --write-tree "$BB" "$VV"; echo "historical rc=$?"
git merge-tree --write-tree "$H" "$VV"; echo "baseline rc=$?"
echo "T204_C20"
git diff "$BB..$VV" -- '*/src/**' |grep -cE '^\+.*(setStyle\(|style=")'||true
echo "T204_C21"
git diff "$BB..$VV" -- '*/WSagaReconciliereForm.java' '*/DialogSursaSite.java' '*/DialogImportDecont.java' '*/ProcesCorelare.java' '*/FacturaTipar.java'|wc -l
git diff -U0 "$BB..$VV" -- '*/WSagaCorelareForm.java'|grep -c '^-[^-]' || true
echo "T204_C17_new_network"
git diff "$BB..$VV" -- '*/src/**'|grep -cE '^\+.*(HttpClient|URLConnection|https?://)'||true
echo "T171_C11"
git show "$H":idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/documente/res/etichete.tsv | awk -F'\t' '/^# T171 A — început/{a=1;next} /^# T171 A — sfârșit/{a=0} /^# T171 B — început/{b=1;next} /^# T171 B — sfârșit/{b=0} {if(a && $1 ~ /^compsaga\./) ac++; if (b && $1 ~ /^compsaga\./) bc++; if($1!~/^#/ && $1!="") m[$1]++}END{for(k in m) if(m[k]>1)du++; print ac,bc,du+0}'
""".replace('BASE','6df998aee0e514d30856c461962afe99ebd0d113')
if __name__=='__main__':
 p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=script.encode(),capture_output=True,timeout=220);q=P/'T227_T204_T171_grep_doua_versiuni.log';q.write_bytes(p.stdout+p.stderr);print(p.returncode,sha(q));print(q.read_text(encoding='utf8',errors='replace')[-1200:])

