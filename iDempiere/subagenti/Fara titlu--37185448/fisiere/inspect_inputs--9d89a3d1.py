from pathlib import Path
import json,hashlib
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=B/'executie/R11_fisiere'
names=['Triaj_fixture_UI_Val03/Raport_triaj_UI_config.json','Triaj_fixture_UI_Val03/Erata_metoda_V12_V13.json','Backend_extindere_Val04/Raport_8_suite_backend.json','HR_izolare_Val03/Raport_A01_HR_Val03.json']
for n in names:
 p=O/n;j=json.loads(p.read_text(encoding='utf-8-sig'));print('\nFILE',n,'SHA',hashlib.sha256(p.read_bytes()).hexdigest(),'KEYS',list(j))
 for k,v in j.items():
  if isinstance(v,list):print(k,'LIST',len(v),json.dumps(v,ensure_ascii=False)[:7000])
  elif isinstance(v,dict):print(k,'DICT',list(v),json.dumps(v,ensure_ascii=False)[:7000])
  else: print(k,v)
