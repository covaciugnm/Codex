from a12_r11x_base import *
root=O/'A01'
for f in (root/'Manifest_A01_R11.json',root/'A01_raport_R11.json',next(f for f in root.rglob('*.json')if 'fise' in str(f).lower())):
 j=read(f);print(f.name,[(k,len(v)if isinstance(v,(list,dict))else str(v)[:110])for k,v in j.items()])
 for k in ['file','files','tests','controls','axes','file_records']:
  if k in j:print(k,str(j[k][0]if isinstance(j[k],list)and j[k] else j[k])[:550])

