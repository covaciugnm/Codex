from a12_r11x_base import *
for p in [O/'Python/Registru_Python.json',O/'Surse_web_si_config/Registru_sintaxa_si_controle.json',O/'Surse_web_si_config/Triaj_cinci_fisiere.json',O/'Surse_web_si_config/Martori_lexicali_XSD.json']:
 j=read(p);print(p.name,list(j))
 for k,v in j.items():
  if isinstance(v,list)and v:print(k,len(v),str(v[0])[:980])

