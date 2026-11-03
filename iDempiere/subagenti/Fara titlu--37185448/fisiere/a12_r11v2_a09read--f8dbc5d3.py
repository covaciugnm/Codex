from a12_r11x_base import *
p=O/'A09';j=read(p/'Manifest_A09_R11.json');print(str(j)[:6300])
for f in p.rglob('Fisa*.json'):
 j=read(f);print('\n'+f.name,[(k,len(v)if isinstance(v,(dict,list))else str(v)[:170])for k,v in j.items()])
 for k in ['file','coverage','axes','six_axes','execution_scope','review','controls']:
  if k in j:print(k,str(j[k])[:1050])
print(read(p/'Raport_A09_R11.json'))

