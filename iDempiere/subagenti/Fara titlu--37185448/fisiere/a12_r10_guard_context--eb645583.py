from a12_r10_base import *
s=open(Path(__file__).parent/'a12_r10_guard_diag.py',encoding='utf8').read()
s=s.replace('for tn in T220','test -f "$r/$policy"; cp "$r/$policy" "$s/$policy";chmod 600 "$s/$policy";echo "Supplement with local operational hash-only policy, SHA as printed above, not a tracked file"; for tn in T220').replace('Diagnostic_garda_date_personale.log','Reprise_garda_scope_historic.log')
exec(s)
