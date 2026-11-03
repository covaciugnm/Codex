from a12_r11x_base import *
for zone in ['A07','A08']:
 for s in sorted((O/zone).glob('fise/*.json')if zone=='A07'else(O/zone).glob('Fisa_*.json')):
  j=read(s);print(s.name)
  for c in j['controls']:print(c.get('id'),c['axes'])
p=O/'Controale_si_fixturi/Martor_requirements_v2.json';j=read(p);print('REQ',str(j)[:3600])
for s in sorted((O/'A09').glob('*.json')):print('A09',s.name)
for s in sorted((O/'A10').glob('*.json')):print('A10',s.name)

