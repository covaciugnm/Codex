from a12_r11x_base import *
st=read(B/'Runda_11_stare.json');print('state',list(st));print('scan',st.get('code_scan'))
for a in ['A02','A03','A04','A05','A07','A08','A09','A10','A11']:
 p=O/a
 print(a,[(f.relative_to(p).as_posix(),f.stat().st_size)for f in p.glob('*.json')])
for a,n in [('Shell_rapoarte_imagini','Registru_formate.json'),('SQL_CSS_HTML','Registru_parsare_v2.json'),('Date_pachete','Registru_date_pachete.json'),('Configurare_sabloane_extensii','Registru_configurari.json'),('Controale_si_fixturi','Registru_controale_si_fixturi.json')]:
 f=O/a/n;j=read(f);print(n,sha(f),[(k,len(v)if isinstance(v,(dict,list))else str(v)[:180])for k,v in j.items()]);print('ex',str(j.get('rows',[None])[0])[:800])

