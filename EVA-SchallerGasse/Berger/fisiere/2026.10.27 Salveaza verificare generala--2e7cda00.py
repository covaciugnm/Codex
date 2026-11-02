from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
root=Path.cwd();tz=ZoneInfo('Europe/Bucharest');now=datetime.now(tz);day=now.strftime('%Y.%m.%d');assert day=='2026.10.27'
stamp=now.isoformat();base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
out=Path('08. Corespondenta')/(day+' Verificare zilnica');proof=out/(day+' Dovezi verificare EVA.json');report=out/(day+' Raport verificare zilnica.txt');newreg=base/(day+' Registru comunicatii.json')
hist=Path('folder map')/(day+' Istoric verificare '+now.strftime('%H-%M-%S'))
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p);dest=root/p
 if dest.exists():
  backup=root/hist/p;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,x):save(p,json.dumps(x,ensure_ascii=False,indent=2))
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(tz).strftime('%Y.%m.%d %H:%M:%S')
p=read(Path('folder map/2026.10.27 Dovezi etapa generala.json'));r=read(Path(p['baseline_register']))
ids={x['id'] for x in r['comunicatii']};assert len(ids)==len(r['comunicatii'])==p['baseline_count']==839
assert len(p['pages'])==64 and not p['errors']
for page in p['pages']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
found={x['id'] for page in p['pages'] for x in page['result']['items']}
assert len(found)==4 and found-ids=={x['id'] for x in p['exclusions']}
assert len(p['exclusions'])==1 and p['exclusions'][0]['from_address']=='offers@travel.wizznews.com'
assert not any(x.get('raportare_generala_pendenta') for x in r.get('mesaje_incidentale_pentru_verificare_generala',[]))
before={k:hashlib.sha256(json.dumps(r[k],ensure_ascii=False,sort_keys=True).encode()).hexdigest() for k in ('comunicatii','drafturi')}
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
limits='Office sincronizat pana la '+local(sync['office@ac-wohnart.at'])+' Romania; Gmail pana la '+local(sync['covaciu.gnm@gmail.com'])+' Romania. Mesajele ulterioare pot lipsi. Celelalte casute sunt acoperite pana la sincronizarile individuale din dovada EVA; shared/team nesearchable excluse.'
entry={'data':day,'checked_at_iso':stamp,'perioada':'2026.10.25–2026.10.27; suprapunere de o zi fata de verificarea generala 2026.10.26; comparatie inclusiv cu verificarea BERGER/PECH 2026.10.26 16:07','cautari_complete':64,'pagini':64,'paginare_completa':True,'acoperire_actuala_office_completa':True,'mesaje_noi_ID':0,'mesaje_primite_ID':0,'mesaje_trimise_ID':0,'documente_originale_integrale_ID':0,'oferta_noua_identificata':False,'mesaje_deja_arhivate_raportate_acum':[],'sincronizari_originale':sync,'stare':'Nicio comunicare, oferta, pret, document sau confirmare relevanta noua. Cele trei mesaje BERGER/PECH din 2026.10.26 sunt deja arhivate si raportate. O reclama Wizz Air a fost exclusa ca nerelevanta.','limite':limits,'sursa':proof.as_posix()}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala']);r['acoperire']['verificare_incrementala']=entry;r['data_actualizarii']=day
r.setdefault('actualizari_punctuale',[]).append({'data':day,'tip':'Verificare generala','mesaje_noi':0,'sursa':proof.as_posix()})
for s in r['statusuri']:s['verificare_comunicari_2026_10_27']={'data':day,'checked_at_iso':stamp,'mesaje_noi':0,'sursa':proof.as_posix()}
for k,h in before.items():assert hashlib.sha256(json.dumps(r[k],ensure_ascii=False,sort_keys=True).encode()).hexdigest()==h
jsave(newreg,r)
proofdata={'verificare':entry,'baseline_register':p['baseline_register'],'baseline_ID_count':839,'final_ID_count':839,'new_relevant_email_ids':[],'already_archived_now_reported':[],'previously_reported_not_repeated':sorted(found&ids),'excluded_unrelated_email_ids':[x['id'] for x in p['exclusions']],'dovezi_originale':p,'nota':'Niciun mesaj sau atasament relevant nou. Textele si metadatele celor trei mesaje deja arhivate sunt reutilizate. Nicio trimitere, semnare, plata sau modificare comerciala. Intalnirile planificate astazi nu sunt considerate efectuate.'}
jsave(proof,proofdata)
summary=day+' | Verificare zilnica Schallergasse 35\nVerificat: '+stamp+'\n\nStatus scurt: Nu s-au identificat comunicari relevante noi, oferte, modificari de pret sau servicii, fisiere, termene ori confirmari de incasare fata de ultima verificare si raportarile punctuale.\nUltimul raspuns nou: niciunul identificat. Confirmarea BERGER si cele doua confirmari trimise de beneficiar din 2026.10.26 sunt deja arhivate si raportate; nu sunt repetate ca noutati.\nUrmatorul pas: urmarirea raspunsurilor si a documentelor; intalnirile BERGER/PECH din 2026.10.27 raman planificate, fara presupunerea ca au avut loc sau ca exista contracte acceptate.\n\nAcoperire: 64 cautari/64 pagini paginate integral, toate mesajele office primite si trimise si cautari globale dupa adresa, firme si referinte, 2026.10.25–2026.10.27. 4 rezultate unice: 3 deja arhivate/raportate si o reclama Wizz Air fara legatura cu proiectul, exclusa motivat. Registrul ramane la 839 ID-uri unice. Niciun atasament relevant nou de descarcat.\n'+limits+'\nSursa: '+proof.as_posix()+'\nNu s-au trimis emailuri, modificat contracte, semnat ori efectuat plati.\n'
save(report,summary)
for name in ('Status proiect','Log progres proiect'):
 previous=Path('2026.10.26 '+name+'.txt');save(Path(day+' '+name+'.txt'),summary+'\nISTORIC PASTRAT\n\n'+(root/previous).read_text(encoding='utf-8-sig'))
for partner in ('Markus Berger','Pech','WOHR'):
 s=next(x for x in r['statusuri'] if x.get('partener')==partner)
 detail=day+' | '+partner+'\nStatus scurt: Nicio noutate la verificarea generala; statusul anterior se pastreaza: '+s['status']+'\nUltimul raspuns: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSursa verificarii: '+proof.as_posix()+'\nSurse status anterior: '+str(s.get('sursa_status'))+'\n'+limits+'\n'
 previous=base/'Parteneri'/('2026.10.26 Log discutii - '+partner+'.txt');save(base/'Parteneri'/(day+' Log discutii - '+partner+'.txt'),detail+'\nISTORIC PASTRAT\n\n'+(root/previous).read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,summary+'Puncte curente: ../'+newreg.as_posix()+'; ../'+day+' Status proiect.txt; ../'+day+' Log progres proiect.txt. Registrul atasamentelor ramane 2026.10.22, fara anexe noi.\n\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
print(json.dumps({'register':newreg.as_posix(),'report':report.as_posix(),'proof':proof.as_posix(),'count':839,'new_relevant':0,'entry':entry},ensure_ascii=False))
