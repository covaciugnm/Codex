from a12_r11x_base import *
for p in [O/'A06/Fisa_ValideazaComenzi.json', O/'A06/Manifest_A06_R11_Git.json',O/'A06/Fisa_DetaliuComanda.json',O/'Java/Registru_sintaxa_Java.json']:
 j=read(p);print(p.name,[(k,len(v) if isinstance(v,(dict,list))else str(v)[:140])for k,v in j.items()])
 for k in ['file','axes','binding','results','rows','controls','evidence']:
  if k in j: print(k,str(j[k][0]if isinstance(j[k],list)and j[k] else j[k])[:1040])

