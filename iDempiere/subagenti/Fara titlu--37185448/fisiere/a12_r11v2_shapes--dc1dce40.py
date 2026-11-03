from a12_r11x_base import *
files=['A02/Triaj_nominal_174_SQL.json','A02/Raport_A02_R11_DB.json','A03/Fisa_GenD101.json','A04/Fisa_AsociereEFactura.json','A05/Fisa_NotaSetWms.json','A07/fise/Fisa_TrimiteFacturaSite.json','A08/Evenimente_A12.json']
for f in files:
 j=read(O/f);print('\n',f)
 if 'file'in j: print('FILE',j['file']);print('CONTROLS',str(j.get('controls'))[:2400]);print('review',j.get('review'))
 else:
  print([(k,len(v)if isinstance(v,(dict,list))else str(v)[:120])for k,v in j.items()])
  for k in ['rows','files','events','cases','findings']:
   if k in j:print(k,str(j[k][0]if isinstance(j[k],list)and j[k]else j[k])[:1600])
r=read(P/'A12_registru_693_stari_alias_v2.json');print('REGISTER',list(r))
print(str(r.get('rows',[])[0])[:2000])
print('R10', [f.name for f in (E/'R10').glob('*.json')][:20])

