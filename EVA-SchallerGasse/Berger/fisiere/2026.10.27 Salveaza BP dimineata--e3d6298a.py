from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
root=Path.cwd();tz=ZoneInfo('Europe/Bucharest');now=datetime.now(tz);day=now.strftime('%Y.%m.%d');assert day=='2026.10.27'
stamp=now.isoformat();tag=now.strftime('%H-%M-%S');base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');reg=base/(day+' Registru comunicatii.json')
out=Path('08. Corespondenta')/(day+' Verificare Berger Pech');proof=out/(day+' '+tag+' Dovezi verificare EVA.json');report=out/(day+' '+tag+' Raport verificare BERGER PECH.txt');hist=Path('folder map')/(day+' Istoric BP '+tag)
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p);dest=root/p
 if dest.exists():
  backup=root/hist/p;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,x):save(p,json.dumps(x,ensure_ascii=False,indent=2))
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(tz).strftime('%Y.%m.%d %H:%M:%S')
p=read(Path('folder map/2026.10.27 Dovezi etapa BP dimineata.json'));r=read(reg)
known={x['id'] for x in r['comunicatii']};assert len(known)==len(r['comunicatii'])==p['baseline_count']==839
assert not p['errors'] and len(p['searches'])==25
found={x['id'] for page in p['searches'] for x in page['result']['items']};assert found<=known and len(found)==3
for page in p['searches']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
before={k:hashlib.sha256(json.dumps(r[k],ensure_ascii=False,sort_keys=True).encode()).hexdigest() for k in ('comunicatii','drafturi')}
general=r['acoperire']['verificare_incrementala'].copy();sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger','Pech'],'mesaje_noi':0,'mesaje_trimise_noi':0,'mesaje_primite_noi':0,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':25,'page_count':25,'perioada':'2026.10.26–2026.10.27, suprapunere de o zi si deduplicare inclusiv fata de verificarea generala 2026.10.27 08:04','paginare_completa':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'mesaje_incidentale_alti_parteneri':0,'sursa':proof.as_posix()}
header=day+' '+now.strftime('%H:%M:%S')+' | Verificare BERGER/PECH\n\n'
short='Nicio noutate BERGER/PECH: nici raspunsuri suplimentare, observatii contractuale, contrapropuneri, preturi/servicii, calendar, atasamente ori nelivrari noi. Cele trei mesaje din 2026.10.26 sunt deja arhivate si raportate.'
coverage='Acoperire: 25 cautari/25 pagini paginate integral, primite si trimise in office si Gmail si cautari globale dupa domenii/adrese/firme, Schallergasse si referinte AN01/AN02/R09; inclusiv nelivrari. 3 rezultate unice deja arhivate, fara ID nou fata de registrul cu 839 mesaje.\nSincronizare Romania: office '+local(sync['office@ac-wohnart.at'])+'; Gmail '+local(sync['covaciu.gnm@gmail.com'])+'. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.\n'
sections={}
for s in r['statusuri']:
 if s.get('partener') not in ('Markus Berger','Pech'):continue
 partner=s['partener'];sections[partner]=partner+'\nStatus scurt: Nicio noutate; situatia pastrata: '+s['status']+'\nUltimul raspuns: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSurse status anterior: '+str(s.get('sursa_status'))+'\n'
 s['verificare_punctuala_BERGER_PECH_2026_10_27']={'checked_at_iso':stamp,'mesaje_noi':0,'sursa':proof.as_posix()}
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general
for k,h in before.items():assert hashlib.sha256(json.dumps(r[k],ensure_ascii=False,sort_keys=True).encode()).hexdigest()==h
text=header+'Status scurt: '+short+'\n\n'+'\n'.join(sections.values())+'\n'+coverage+'Sursa: '+proof.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati. Intalnirile planificate nu sunt considerate efectuate.\n'
jsave(reg,r);jsave(proof,{'verificare':entry,'baseline_unique_ids':839,'final_unique_ids':839,'new_BP_email_ids':[],'previously_archived_not_repeated':sorted(found),'dovezi_originale':p,'general_baseline':general,'nota':'Nicio noutate de exportat. Se reutilizeaza sursele arhivate; confirmarile trimise si raspunsul BERGER au fost deja raportate 2026.10.26. Nicio trimitere sau actiune comerciala.'})
save(report,text)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt');save(path,text+'\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
for partner,section in sections.items():
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt');save(path,header+section+'\n'+coverage+'Sursa: '+proof.as_posix()+'\n\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,text+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'entry':entry,'register_count':839,'general_coverage_preserved':True},ensure_ascii=False))
