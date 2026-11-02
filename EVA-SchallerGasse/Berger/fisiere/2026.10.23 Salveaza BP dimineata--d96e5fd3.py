import json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone,timedelta
day='2026.10.23'
now=datetime.now(timezone(timedelta(hours=3)))
assert now.strftime('%Y.%m.%d')==day
tag=now.strftime('%H-%M-%S')
stamp=now.isoformat()
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
rp=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Verificare Berger Pech')
folder.mkdir(parents=True,exist_ok=True)
proof=folder/(day+' '+tag+' Dovezi verificare EVA.json')
report=folder/(day+' '+tag+' Raport verificare BERGER PECH.txt')
hist=Path('folder map')/(day+' Istoric BP '+tag)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,s):
 p=Path(p)
 if p.exists():
  b=hist/p
  b.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(p,b)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(s.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
p=read('folder map/2026.10.23 Dovezi etapa BP dimineata.json')
r=read(rp)
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==835
assert len(p['searches'])==22 and not p['errors']
known={x['id'] for x in r['comunicatii']}
allids={x['id'] for page in p['searches'] for x in page['result']['items']}
assert len(allids)==9
assert allids-known=={'03afbf29-8f7a-4790-bcd4-d94da52be53d'}
for page in p['searches']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
for f in p['contract_sources']:assert hashlib.sha256(Path(f['cale']).read_bytes()).hexdigest()==f['sha256']
mb={m['email']:m for m in p['mailboxes']['mailboxes']}
general=r['acoperire']['verificare_incrementala'].copy()
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger','Pech'],'mesaje_noi':0,'mesaje_trimise_noi':0,'mesaje_primite_noi':0,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':22,'page_count':22,'perioada':'2026.10.21–2026.10.23; suprapunere de o zi fata de verificarea punctuala 2026.10.22 si comparatie inclusiv cu verificarea generala 2026.10.23 08:00','paginare_completa':True,'acoperire_office_limitata':False,'sincronizare_office':mb['office@ac-wohnart.at']['last_sync'],'sincronizare_gmail':mb['covaciu.gnm@gmail.com']['last_sync'],'mesaje_incidentale_alti_parteneri':0,'candidati_nerelevanti_exclusi':1,'sursa':proof.as_posix()}
bp='Nicio noutate BERGER/PECH fata de verificarea generala 2026.10.23 08:00: nici raspunsuri suplimentare, observatii contractuale, contrapropuneri, preturi/servicii noi, termene/calendar, atasamente ori nelivrari relevante noi.'
ber='Ultimul raspuns BERGER: 2026.10.21, confirma primirea si cere analiza peste weekend. Propunerea trimisa pentru 2026.10.27 11:00 Viena este deja raportata; fara confirmarea orei/locului.'
pech='Ultimul raspuns PECH: 2026.10.22 17:52:22 Romania, poate confirma 2026.10.27 14:00 Viena daca beneficiarul vine la biroul PECH, Johann-Strauß-Gasse 32/6, 1040 Wien. Deja raportat la verificarea generala de azi; nu se repeta ca noutate. Nu este acceptare a contractului.'
nxt='Urmatorul pas BERGER: urmarirea confirmarii intalnirii si a observatiilor asupra propunerii. Urmatorul pas PECH: confirmarea disponibilitatii de a veni la biroul lor la ora propusa, fara acceptarea conditiilor comerciale prin aceasta verificare.'
cov='Acoperire: 2026.10.21–2026.10.23; 22 cautari/22 pagini paginate integral, ambele conturi si global, mesaje primite si trimise, domenii/adrese/referinte si notificari de nelivrare. Noua rezultate unice: opt deja arhivate, inclusiv trei mesaje WÖHR care nu sunt noutati BERGER/PECH; o nelivrare catre office@cesiro.ro citita integral si exclusa, fara legatura cu proiectul. Comparatie cu 835 ID-uri; niciun mesaj/atasament relevant nou de salvat. R09 BERGER, R09 PECH si AN02 neschimbate, SHA-256 verificat.\nSincronizari, ora Romania: office 2026.10.23 10:00:13; Gmail 2026.10.23 10:05:25. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.\n'
text=day+' '+now.strftime('%H:%M:%S')+' — Verificare BERGER/PECH\n\nStatus scurt: '+bp+'\n'+ber+'\n'+pech+'\n'+nxt+'\n\n'+cov+'Sursa: '+proof.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati.\n'
jsave(proof,{'verificare':entry,'baseline_unique_ids':835,'final_unique_ids':835,'new_BP_email_ids':[],'incidental_other_partner_email_ids':[],'attachments_verified':[],'dovezi_originale':p,'general_baseline':general,'nota':'Raspunsul PECH din 2026.10.22 este deja arhivat si raportat la verificarea generala 2026.10.23, nu este noutate repetata. Nelivrarea CESIRO este exclusa. Fara mesaje sau anexe relevante noi.'})
save(report,text)
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry
r.setdefault('verificari_parteneri',[]).append(entry)
for s in r['statusuri']:
 if s.get('partener') in ('Markus Berger','Pech'):
  s['verificare_punctuala_BERGER_PECH_2026_10_23']={'checked_at_iso':stamp,'mesaje_noi':0,'sursa':proof.as_posix()}
assert r['acoperire']['verificare_incrementala']==general
jsave(rp,r)
for fn in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+fn+'.txt')
 save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
for partner in ('Markus Berger','Pech'):
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt')
 save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md')
save(path,text+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'register':rp.as_posix(),'entry':entry,'message_IDs':835,'general_coverage_preserved':True},ensure_ascii=False))
