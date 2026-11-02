from a12_r8_cases import *
for k in ['PB-95_tipar_factura_site.txt','PB-93_auto_confirma_trimis.txt','PB-0_premise_cheie_out.txt']:
 z=next((x for x in a if '/T216-'in x['file'] and '/BAZA-PB-95/'in x['file']and x['file'].endswith(k)),None)or next((x for x in a if '/T216-'in x['file']and x['file'].endswith(k)),None)
 if z:print(z['file'],z['oid'],txt(z)[:1950])
for x in a:
 if '/T216-' in x['file']and re.search('incas|(?i:plata)|card.*\\.txt|achita|aloc|site_.*factura',x['file'].split('/')[-1],re.I):print(x['file'].split('/',3)[-1])

