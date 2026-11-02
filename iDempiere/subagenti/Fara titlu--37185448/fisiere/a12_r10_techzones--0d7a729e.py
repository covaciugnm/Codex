from a12_r10_base import *
a=Path(__file__).parent/'a12_r10_receipt.py';exec(a.read_text(encoding='utf8').split("j=P10/")[0]);import subprocess
dest=P10/'Zone_A02_A10';dest.mkdir(exist_ok=True)
cmd=r'''set -eu
r=/home/saga-server/Documents/EvA-Contab;d=Documentatie/echipa-2026-10-09/T11-reges-simulator-complet;h=faa1b5424d;b=7012faab2;cut=CUT;p=idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab
git -C "$r" rev-parse "$b^{commit}" "$h^{commit}"
git -C "$r" merge-base "$h" 8451985a2b
git -C "$r" rev-list --count "$b..$h"
for f in 08_manager_plan_v2.md 11_E5_auditor_cod.md 13_auditor_integrare.md;do printf '%s blob=' "$f";git -C "$r" rev-parse "$cut:$d/$f";git -C "$r" show "$cut:$d/$f"|grep -nEi '^.*([|] R-03 [|]|[|] R-13 [|]|baz. = .7012faa|Ramur. / v.rf|0 elemente AD noi|16b.*S04|vârf [|] .c1-integrare-t11)'|head -5;done
printf 'R03_METADATA_diff_wc_l=';git -C "$r" diff "$b..$h" -- "$p/setup/EvaMetadata.java"|wc -l
printf 'R03_RegesTabele_nonEVAAdded=';git -C "$r" diff -U0 "$b..$h" -- "$p/reges/RegesTabele.java"|grep '^+'|grep -v '^+++'|grep -vc 'EVA_Actiune'||test $? = 1
printf 'R13_JARS_added_or_changed=';git -C "$r" diff --name-only "$b..$h"|grep -c '\.jar$'||test $? = 1
printf 'Total changed files in same interval=';git -C "$r" diff --name-only "$b..$h"|wc -l
printf 'Control R03 nominal allowed plus forbidden yields one=';printf '%s\n' '+++ b/Z.java' '+ EVA_Actiune' '+ AltaAD'|grep '^+'|grep -v '^+++'|grep -vc 'EVA_Actiune'
printf 'Control R13 .jar true, .jar.md ignored, result=';printf '%s\n' 'doc/report.jar.md' 'ed/test.jar'|grep -c '\.jar$'
printf 'Relation actual integration follows b..h='; git -C "$r" show -s --pretty=%P 00398bb9c8
'''.replace('CUT',BASE)
q=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=cmd.encode(),capture_output=True,timeout=45);q.check_returncode();tests=q.stdout.decode().splitlines();pf=dest/'Teste_Git.json';wr(pf,{'utc':now(),'cutoff':BASE,'driver':cmd,'results':tests,'stderr':q.stderr.decode(),'comment':'The branch audited independently and the integration later built/committed with jar are different ranges.'});print(tests[-7:])
for cid,marker,oracle,ng,lim in [('T11-R2-019','R03_','Ambele expresii originale dau 0 în intervalul de implementare și cel puțin un martor negativ altă coloană.',[q for q in tests if 'Control R03' in q],'Contract static despre două fișiere concrete. Nu implică absența vreunui nou AD_Element introdus prin alt mecanism sau în altă versiune.'),('T11-R2-029','R13_','Zero căi JAR dintre toate fișierele modificate în $BAZA..$H; extensia literală diferențiază .jar de .jar.md.',[q for q in tests if 'Control R13' in q],'Nu s-a reprodus build-ul temporar 16b și nu a fost deschis cabinetul S04 istoric. Alt JAR al integrării ulterioare este altă versiune.')]:
 hit=[p for p in tests if p.startswith(marker)];assert hit and all(p.endswith('=0')for p in hit);add(cid,'Git complet, interval documentat, expresii și martor controlat',oracle,{'base':tests[0],'branch':tests[1],'mergebase':tests[2],'count_commits':tests[3],'measurements':hit,'total_paths':next(x for x in tests if 'Total changed files'in x)},ng,lim,[jr(pf,'/results')]); 
p=dest/'Rezultat.json';wr(p,{'utc':now(),'receipts':out,'count':len(out)});print(sha(p))
