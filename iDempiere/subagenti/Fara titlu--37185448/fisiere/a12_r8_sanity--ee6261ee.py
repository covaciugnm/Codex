from a12_r8_cases import *
p=next(z for z in a if z['file'].endswith('dovezi-40-audit/proba_finala/C-01_C-02_dictionar.txt'));print(txt(p));r=rd(P/'Rezultate_A12_93_si_supliment.json')['cases']
for t in ('T224-R2-009','T224-R2-016','T224-R2-011','T314-R2-027','T310-R3-001','T06-R2-012','T204-R2-025'):
 print(t,[(x['kind'],str(x['observed'])[:135])for x in r[t]][:6])

