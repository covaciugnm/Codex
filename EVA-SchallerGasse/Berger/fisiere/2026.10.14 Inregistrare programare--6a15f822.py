from pathlib import Path
import json,shutil,tomllib
R=Path.cwd();A=R/'08. Corespondenta/2026.10.14 Monitorizare Berger Pech'
C=Path(r'C:\Users\User\.codex\automations\verificare-emailuri-berger-i-pech\automation.toml')
c=tomllib.loads(C.read_text(encoding='utf-8'))
assert c['kind']=='heartbeat' and c['status']=='ACTIVE'
assert c['rrule']=='FREQ=DAILY;BYHOUR=10,16;BYMINUTE=0;BYSECOND=0'
assert c['target_thread_id']=='01a0f6eb-c105-7760-973e-241d6f6be8c1'
shutil.copy2(C,A/'2026.10.14 Configurare automatizare originala.toml')
note='2026.10.14 — Verificări programate BERGER/PECH, zilnic la 10:00 și 16:00, Europe/Bucharest, ACTIVE. Automatizare verificare-emailuri-berger-i-pech în acest chat. Mesaje primite/trimise office și Gmail, răspunsuri, oferte/contrapropuneri, sume, servicii, termene, atașamente și nelivrări; numai noutăți, fără repetarea actualizărilor deja arhivate. Verificarea generală 08:00 rămâne activă. Ultimul răspuns: programarea solicitată a fost creată și verificată; nu s-a efectuat o nouă verificare comercială. Următorul pas: rulările programate și afișarea aici a noutăților ori a lipsei lor cu limite de sincronizare. Nicio trimitere, semnare, modificare de document comercial sau plată. Sursa: 08. Corespondenta/2026.10.14 Monitorizare Berger Pech/2026.10.14 Programare verificari Berger Pech.json și configurarea originală salvată în același folder.\n'
paths=[R/'2026.10.14 Status proiect.txt',R/'2026.10.14 Log progres proiect.txt',R/'folder map/README.md',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.14 Log discutii - Markus Berger.txt',R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.14 Log discutii - Pech.txt']
for i,p in enumerate(paths):
 prior=p.read_text(encoding='utf-8-sig') if p.exists() else ''
 if '2026.10.14 — Verificări programate BERGER/PECH' in prior:continue
 (A/('2026.10.14 Istoric '+str(i+1)+' '+p.name)).write_text(prior,encoding='utf-8')
 p.write_text(note+'\nISTORIC PĂSTRAT\n\n'+prior,encoding='utf-8')
registry=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.14 Registru comunicatii.json'
d=json.loads(registry.read_text(encoding='utf-8-sig'));shutil.copy2(registry,A/'2026.10.14 Registru comunicatii inainte programare.json')
n=len(d['comunicatii']);d['monitorizare_parteneri']={'id':c['id'],'status':c['status'],'ore':['10:00','16:00'],'fus_orar':'Europe/Bucharest','afisare':'in acest chat','scop':'Numai comunicari BERGER si PECH','sursa':'08. Corespondenta/2026.10.14 Monitorizare Berger Pech/2026.10.14 Programare verificari Berger Pech.json','verificare_generala_08_passtrata':True}
d['actualizari_punctuale'].append({'data':'2026.10.14','tip':'Programare BERGER PECH 10:00 si 16:00','automation_id':c['id'],'status':'ACTIVE','mesaje_noi':0,'sent':0,'sursa':d['monitorizare_parteneri']['sursa']})
assert len(d['comunicatii'])==n
registry.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'automation_id':c['id'],'status':c['status'],'hours':['10:00','16:00'],'thread':c['target_thread_id'],'messages_unchanged':n},ensure_ascii=False))
