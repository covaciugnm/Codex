import json, gzip, os, collections
from pathlib import Path
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
E=B/'executie'; P=E/'R11_plan_delta'; O=E/'R11_fisiere'
for f in ['Plan_delta_R11_v3.json','A06_protocol_fisier_cu_fisier.json','A06_sablon_fisa_fisier.json','Manifest_Dispatch_tehnic_integral.json','Index_invers_delta_task_control_pipeline_v3.json','A12_inventar_si_receptie_v2.json','A11_verdict_plan_delta_R11_v3.json']:
 j=json.loads((P/f).read_text(encoding='utf-8-sig')); print(f,[(k,str(v)[:170] if not isinstance(v,(dict,list)) else len(v)) for k,v in j.items()])
 if f.startswith('A06_sablon'): print(j)
for f in P.glob('*.gz'):
 with gzip.open(f,'rt',encoding='utf-8') as s: print(f.name,str(json.loads(next(s)))[:6500])
print('O', list(O.glob('*')))
print('local',list(Path('D:/CodexWork/a01-r11-frozen').glob('*'))[:30])

