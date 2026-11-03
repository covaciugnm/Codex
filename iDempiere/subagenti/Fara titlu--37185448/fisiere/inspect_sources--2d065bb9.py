from pathlib import Path
import json,gzip
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=B/'executie/R11_fisiere'
for name in ['A11/Verdict_A11_R11_lot_04_v1.json','A11/A11_martor_bootstrap_lot_04.json','A11/A11_martor_documente_lot_04.json','Suite_originale_API_portal_v10/Rezultate_suite_originale.json','A12/Val_02/Matrice_criterii_task_probe.json','A12/Val_02/Contracte_17_si_capitole.json','A12/Val_02/Handoff_val_02_v2.json']:
 j=json.loads((O/name).read_text(encoding='utf-8-sig'));print('\nFILE',name,'KEYS',list(j))
 if 'constatari'in j:
  for i,r in enumerate(j['constatari']):print(i,json.dumps(r,ensure_ascii=False))
 elif 'criterion_rows'in j:
  for k in ['cases','nominal_links','criterion_rows']:
   x=j[k];print(k,str(x[:2]if isinstance(x,list)else x)[:4000])
 elif 'suite' in name.lower(): print(json.dumps(j,ensure_ascii=False)[:3500])
 else:print(str(j)[:1000])
with gzip.open(O/'A12/Val_02/Registru_6709_val_02.jsonl.gz','rt',encoding='utf8') as f:
 for l in f:
  r=json.loads(l)
  if r['path'].endswith('test_t58_close_month.py') or r['path'].endswith('TrimiteFacturaSite.java'):print('ROW',json.dumps(r,ensure_ascii=False)[:7000])
