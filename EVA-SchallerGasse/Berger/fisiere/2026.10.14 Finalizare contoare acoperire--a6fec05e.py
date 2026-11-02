from pathlib import Path
import json
R=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
base=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
p=base/'2026.10.14 Registru comunicatii.json'
old=json.loads((base/'2026.10.13 Registru comunicatii.json').read_text(encoding='utf-8-sig'))['acoperire']
d=json.loads(p.read_text(encoding='utf-8'));a=d['acoperire'];n=a['verificare_incrementala'];pdf=n['PDF_originale_integrale_verificate'];images=n['imagini_inline_numai_metadate']
for key in ['atasamente_documentare','atasamente_documentare_salvate','atasamente_salvate']:a[key]=old[key]+pdf
a['atasamente_identificate']=old['atasamente_identificate']+pdf+images
a['imagini_mici_numai_metadate']=old['imagini_mici_numai_metadate']+images
a['registru_atasamente_randuri']=len(json.loads((base/'2026.10.14 Registru atasamente.json').read_text(encoding='utf-8')))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:a[k] for k in ['atasamente_identificate','atasamente_salvate','atasamente_documentare','atasamente_documentare_salvate','registru_atasamente_randuri']}))
