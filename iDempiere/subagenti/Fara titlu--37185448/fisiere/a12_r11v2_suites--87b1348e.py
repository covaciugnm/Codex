from a12_r11x_base import *
p=O/'Suite_originale_API_portal_v7';f=p/'Rezultate_suite_originale.json';j=read(f);print(sha(f));print([(k,len(v)if isinstance(v,(list,dict))else str(v)[:170])for k,v in j.items()])
for k,v in j.items():
 if isinstance(v,list)and v:
  print(k, str(v[0])[:2800]);print('last',str(v[-1])[:1200])
print('sources',list(read(p/'Surse_izolate_Git.json'))[:10])
j=read(P/'A12_inventar_si_receptie_v2.json')
for x in j['bidirectional_transactional_cases']:print(x['id'],x['objective'])

