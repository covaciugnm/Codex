from a12_r10_base import *
s=open(Path(__file__).parent/'a12_r10_guard_diag.py',encoding='utf8').read()
s=s.replace('for tn in T220','test -f "$r/$policy"; cp "$r/$policy" "$s/$policy";chmod 600 "$s/$policy";echo "local policy outside object tree; per criterion full directory namespace"; for tn in T220').replace('git -C "$r" archive CUT "$dir"|tar xf -;','mkdir "$s/$tn";git -C "$r" archive CUT "$dir"|tar -x -C "$s/$tn";').replace('--director "$dir"','--director "$s/$tn"').replace('^((','^((').replace('Diagnostic_garda_date_personale.log','Garda_T220_T224_domeniu_reconstituit.log');exec(s)
