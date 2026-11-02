import json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone,timedelta
day='2026.10.24'
now=datetime.now(timezone(timedelta(hours=3)))
assert now.strftime('%Y.%m.%d')==day
stamp=now.isoformat()
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
folder=Path('08. Corespondenta')/(day+' Verificare zilnica')
proof=folder/(day+' Dovezi verificare EVA.json')
report=folder/(day+' Raport verificare zilnica.txt')
reg=base/(day+' Registru comunicatii.json')
hist=Path('folder map')/(day+' Istoric verificare '+now.strftime('%H-%M-%S'))
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,text):
 p=Path(p)
 if p.exists():
  h=hist/p
  h.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(p,h)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(text.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
p=read('folder map/2026.10.24 Dovezi etapa generala.json')
r=read(p['baseline_register'])
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==835
assert not p['errors'] and len(p['pages'])==64
known={x['id'] for x in r['comunicatii']}
found={e['id'] for page in p['pages'] for e in page['result']['items']}
assert len(found)==7
assert found-known=={'3796c6c1-d196-4824-8d3a-0650566ac096','6ce00b15-d11a-448e-be53-046a3eddc9c8'}
assert {x['id'] for x in p['exclusions']}==found-known
for page in p['pages']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
assert not any(x.get('raportare_generala_pendenta') for x in r.get('mesaje_incidentale_pentru_verificare_generala',[]))
sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
limits='Office sincronizat pana la 2026.10.24 08:00:13 Romania; Gmail pana la 2026.10.24 04:20:19 Romania. Mesajele ulterioare pot lipsi. Cosmin@ig.ro ramas la 2026.10.10 02:30:10 Romania; shared/team nesearchable excluse. Newsletterul Skyscanner este trunchiat de API si exclus din fragment; nu se pretinde citire integrala.'
entry={'data':day,'checked_at_iso':stamp,'perioada':'2026.10.22–2026.10.24; suprapunere de o zi fata de verificarea generala 2026.10.23; comparatie inclusiv cu verificarile BERGER/PECH din 2026.10.23','cautari_complete':64,'pagini':64,'paginare_completa':True,'acoperire_actuala_office_completa':True,'mesaje_noi_ID':0,'mesaje_primite_ID':0,'mesaje_trimise_ID':0,'documente_originale_integrale_ID':0,'oferta_noua_identificata':False,'mesaje_deja_arhivate_raportate_acum':[],'sincronizari_originale':sync,'stare':'Nicio comunicare, oferta, pret, document sau confirmare relevanta noua. Cinci rezultate deja arhivate si raportate; doua mesaje marketing excluse.','limite':limits,'sursa':proof.as_posix()}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala'])
r['acoperire']['verificare_incrementala']=entry
r['data_actualizarii']=day
r.setdefault('actualizari_punctuale',[]).append({'data':day,'tip':'Verificare generala','mesaje_noi':0,'sursa':proof.as_posix()})
for s in r['statusuri']:
 s['verificare_comunicari_2026_10_24']={'data':day,'mesaje_noi':0,'sursa':proof.as_posix()}
jsave(reg,r)
proofdata={'verificare':entry,'baseline_register':p['baseline_register'],'baseline_ID_count':835,'final_ID_count':835,'new_relevant_email_ids':[],'already_archived_now_reported':[],'previously_reported_not_repeated':[x for x in found if x in known],'dovezi_originale':p,'nota':'Fara mesaje/atasamente relevante noi de salvat; se reutilizeaza sursele existente. Fara email trimis, contract modificat/semnat, eveniment calendar creat ori plata efectuata.'}
jsave(proof,proofdata)
summary=day+' — Verificare zilnica Schallergasse 35\nVerificat: '+stamp+'\n\nStatus scurt: Nu s-au identificat comunicari relevante noi, oferte, modificari de pret/servicii, documente, termene sau confirmari de incasare fata de ultima verificare si raportarile punctuale.\nUltimul raspuns nou: niciunul identificat. Raspunsul PECH si schimbul WÖHR din 2026.10.22 sunt deja arhivate si raportate, nu sunt repetate ca noutati.\nUrmatorul pas: continuarea urmaririi discutiilor si confirmarii intalnirilor, fara trimitere de emailuri prin aceasta verificare.\n\nAcoperire: 64 cautari/64 pagini paginate integral, toate mesajele office primite si trimise si cautari globale dupa adresa, firme si referinte, 2026.10.22–2026.10.24. Sapte rezultate unice: cinci deja arhivate, doua marketing excluse (Skyscanner si nobilacasa). Registrul ramane la 835 ID-uri unice; niciun atasament relevant nou de descarcat.\n'+limits+'\nSursa: '+proof.as_posix()+'\n\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte ori efectuat plati.\n'
save(report,summary)
for name in ('Status proiect','Log progres proiect'):
 old=Path('2026.10.23 '+name+'.txt')
 save(Path(day+' '+name+'.txt'),summary+'\nISTORIC PASTRAT\n\n'+old.read_text(encoding='utf-8-sig'))
for partner in ('Markus Berger','Pech','WOHR'):
 s=next(x for x in r['statusuri'] if x.get('partener')==partner)
 detail=day+' — '+partner+'\nStatus scurt: Nicio noutate la verificarea generala; statusul anterior se pastreaza: '+s['status']+'\nUltimul raspuns: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSursa verificarii: '+proof.as_posix()+'\nSurse status anterior: '+str(s.get('sursa_status'))+'\n'+limits+'\n'
 old=base/'Parteneri'/('2026.10.23 Log discutii - '+partner+'.txt')
 save(base/'Parteneri'/(day+' Log discutii - '+partner+'.txt'),detail+'\nISTORIC PASTRAT\n\n'+old.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md')
save(path,summary+'Puncte curente: ../'+reg.as_posix()+'; ../'+day+' Status proiect.txt; ../'+day+' Log progres proiect.txt. Registrul de atasamente ramane 2026.10.22, fara anexe noi.\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
print(json.dumps({'register':reg.as_posix(),'report':report.as_posix(),'proof':proof.as_posix(),'count':835,'new_relevant':0,'entry':entry},ensure_ascii=False))
