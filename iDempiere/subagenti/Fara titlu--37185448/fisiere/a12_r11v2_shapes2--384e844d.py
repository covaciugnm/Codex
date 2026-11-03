from a12_r11x_base import *
for f in ['A02/Raport_A02_R11_DB.json','A03/Fisa_GenD101.json','A03/Fisa_ValidatorAnaf.json','A04/Fisa_AsociereEFactura.json','A05/Fisa_NotaSetWms.json','A07/fise/Fisa_TrimiteFacturaSite.json','A08/Evenimente_A12.json']:
 j=read(O/f); print('\n',f)
 if isinstance(j,list):print(str(j[0])[:2500]);continue
 for k in ['coverage','six_axes','nominal','file_records','evidence','oracles','actor','reconciliation','persistent_effect']:
  if k in j:print(k,str(j[k])[:3000])
j=read(P/'A12_registru_693_stari_alias_v2.json');print('register fields',j.keys());print(str(j)[:1500]);print('R10', [f.name for f in (E/'R10').glob('*.json')][:20])

