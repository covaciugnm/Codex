from a12_r11x_base import *
for zone in ['A03','A04','A05']:
 for f in sorted((O/zone).glob('Fisa_*.json')):
  j=read(f);print(zone,f.stem, {k:j[k] for k in ['method','status','scope','coverage','identity','finding','task_primary']if k in j})
j=read(P/'A12_registru_693_stari_alias_v2.json')
print('rowexample',str(j['rows'][0])[:2500])
rr=read(E/'R10/Registru_reexecutare_R10.json');print('rows',str(rr['rows'][0])[:2200])
for f in ['A03/Raport_A03_R11_fiscal.json','A07/Raport_A07_R11.json','A08/A08_raport_R11.json']:
 j=read(O/f);print(f,json.dumps(j,ensure_ascii=False)[:7500])

