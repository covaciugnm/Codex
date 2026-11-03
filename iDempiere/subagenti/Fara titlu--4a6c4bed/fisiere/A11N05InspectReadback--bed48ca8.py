import json,pathlib
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03')
d=json.loads((B/'Readback_independent_final_v1.json').read_text(encoding='utf8'))
for k,v in d['rows'].items():
 print(k,len(v),json.dumps(v[0],ensure_ascii=False)[:2000] if v else '')
print('movements')
for k,v in d['rows'].items():
 if 'movement' in k or 'moves' in k:
  for x in v:print(json.dumps(x,ensure_ascii=False))
