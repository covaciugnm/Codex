import json,hashlib,shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
tz=ZoneInfo('Europe/Bucharest')
now=datetime.now(tz)
day='2026.10.25'
assert now.strftime('%Y.%m.%d')==day
stamp=now.isoformat();tag=now.strftime('%H-%M-%S')
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
reg=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Verificare Berger Pech')
proof=folder/(day+' '+tag+' Dovezi verificare EVA.json')
report=folder/(day+' '+tag+' Raport verificare BERGER PECH.txt')
hist=Path('folder map')/(day+' Istoric BP '+tag)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,text):
 p=Path(p)
 if p.exists():
  h=hist/p;h.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,h)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
def readable(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(tz).strftime('%Y.%m.%d %H:%M:%S')
p=read('folder map/2026.10.25 Dovezi etapa BP dimineata.json');r=read(reg)
ids={x['id'] for x in r['comunicatii']}
assert len(ids)==len(r['comunicatii'])==p['baseline_count']==836
assert len(p['searches'])==22 and not p['errors']
found={x['id'] for page in p['searches'] for x in page['result']['items']}
assert found<=ids and len(found)==1
for page in p['searches']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
general=r['acoperire']['verificare_incrementala'].copy()
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
office=sync['office@ac-wohnart.at'];gmail=sync['covaciu.gnm@gmail.com']
regression='Gmail raporteaza acum un last_sync anterior celui din verificarea generala 08:49 (atunci 2026.10.25 08:46:51 Romania); se pastreaza ambele valori si nu se presupune extinderea acoperirii.'
assert gmail<general['sincronizari_originale']['covaciu.gnm@gmail.com']
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger','Pech'],'mesaje_noi':0,'mesaje_trimise_noi':0,'mesaje_primite_noi':0,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':22,'page_count':22,'perioada':'2026.10.23–2026.10.25; suprapunere de o zi fata de verificarea BERGER/PECH 2026.10.24 16:58, inclusiv comparatie cu verificarea generala 2026.10.25 08:49','paginare_completa':True,'acoperire_office_limitata':False,'sincronizare_office':office,'sincronizare_gmail':gmail,'mesaje_incidentale_alti_parteneri':0,'nota_sincronizare':regression,'sursa':proof.as_posix()}
headers=day+' '+now.strftime('%H:%M:%S')+' — Verificare BERGER/PECH\n\n'
short='Nicio noutate BERGER/PECH fata de verificarile anterioare: nici raspunsuri suplimentare, observatii contractuale, contrapropuneri, preturi/servicii, termene/calendar, atasamente sau nelivrari relevante noi. Raspunsul BERGER din 2026.10.24 este deja arhivat si raportat, nu este repetat ca noutate.'
sections={}
for s in r['statusuri']:
 if s.get('partener') in ('Markus Berger','Pech'):
  partner=s['partener']
  sections[partner]=partner+'\nStatus scurt: nicio noutate la acest control. Situatia pastrata: '+s['status']+'\nUltimul raspuns: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSurse anterioare: '+str(s.get('sursa_status'))+'\n'
  s['verificare_punctuala_BERGER_PECH_2026_10_25']={'checked_at_iso':stamp,'mesaje_noi':0,'sursa':proof.as_posix()}
coverage='Acoperire: 22 cautari/22 pagini paginate integral, mesaje primite si trimise in ambele conturi si cautari globale dupa domenii/adrese/referinte, inclusiv nelivrari. 2026.10.23–2026.10.25. Un rezultat unic, raspunsul BERGER din 2026.10.24, deja arhivat si raportat. Comparatie cu 836 ID-uri unice; niciun mesaj ori atasament relevant nou de salvat.\nSincronizare Romania: office '+readable(office)+'; Gmail '+readable(gmail)+'. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse. '+regression+'\n'
text=headers+'Status scurt: '+short+'\n\n'+'\n'.join(sections.values())+'\n'+coverage+'Sursa verificarii: '+proof.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati.\n'
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general
jsave(reg,r)
jsave(proof,{'verificare':entry,'baseline_unique_ids':836,'final_unique_ids':836,'new_BP_email_ids':[],'incidental_other_partner_email_ids':[],'attachments_verified':[],'dovezi_originale':p,'general_baseline':general,'nota':'Nicio noutate de exportat. Se reutilizeaza sursele arhivate, inclusiv mesajul BERGER deja raportat 2026.10.24. Nicio schimbare comerciala sau trimitere.'})
save(report,text)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt');save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
for partner,section in sections.items():
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt')
 save(path,headers+section+'\n'+coverage+'Sursa: '+proof.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,text+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'register':reg.as_posix(),'entry':entry,'unique_IDs':836,'general_coverage_preserved':True},ensure_ascii=False))
