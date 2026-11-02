from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
root=Path.cwd();now=datetime.now(ZoneInfo('Europe/Bucharest'));day=now.strftime('%Y.%m.%d');tag=now.strftime('%H-%M-%S');stamp=now.isoformat(timespec='seconds');base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');out=Path('08. Corespondenta')/(day+' Checklist BERGER');proof=out/(day+' '+tag+' Dovezi checklist BERGER.json');report=out/(day+' '+tag+' Checklist BERGER.txt');hist=Path('folder map')/(day+' Istoric checklist BERGER '+tag)
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 dest=root/p
 if dest.exists():
  bak=root/hist/p;bak.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,bak)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t):save(p,t+'\n\nISTORIC PASTRAT\n\n'+((root/p).read_text(encoding='utf-8-sig') if (root/p).exists() else ''))
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest')).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'
p=read(Path('folder map/2026.10.29 Dovezi checklist BERGER 17.json'));r=read(Path(p['baseline_register']));known={m['id'] for m in r['comunicatii']};assert not p['errors'] and set(p['scoped_email_ids'])<=known
for s in p['searches']:assert s['args']['offset']+len(s['result']['items'])>=s['result']['total']
found={e['id'] for s in p['searches'] for e in s['result']['items']};assert found==set(p['scoped_email_ids'])|set(p['excluded_unrelated_email_ids']);assert p['draft_readback']['status']=='sent';assert all(f['unchanged'] for f in p['baseline']['relevant_current_files'])
before={k:digest(r[k]) for k in ('comunicatii','drafturi')};general=r['acoperire']['verificare_incrementala'].copy();status=next(s for s in r['statusuri'] if s.get('partener')=='Markus Berger')
sources={e['id']:e for e in r['comunicatii'] if e['id'] in p['scoped_email_ids']};sent=sources['96e74e69-7ff6-402c-9959-597c0b472950'];assert sent['sens']=='TRIMIS' and len(sent['atasamente'])==3
checks=[
 {'punct':1,'criteriu':'Emailuri primite/trimise si nelivrari','rezultat':'FARA NOUTATI','detalii':'25 cautari/25 pagini complete; 53 ID-uri metadate unice; 4 ID-uri BERGER, toate deja arhivate. Nicio nelivrare BERGER. Cautari globale si control integral primit/trimis pentru office si Gmail.','surse':[v['cale'] for v in sources.values()]},
 {'punct':2,'criteriu':'Contract, observatii si contrapropuneri','rezultat':'FARA NOUTATI','detalii':'Nu exista raspuns comercial nou sau contrapropunere la R11. Propunerea R11 este trimisa; nu este acceptare sau contract semnat. PDF-urile locale sunt neschimbate fata de index.','surse':[sent['cale']]+[v['cale'] for v in p['baseline']['relevant_current_files']]},
 {'punct':3,'criteriu':'Preturi, servicii si suplimente','rezultat':'FARA NOUTATI','detalii':'Propunerea curenta ramane 45.000 EUR net initial + 2.500 EUR net Bauwerksbuch = 47.500 EUR net /57.000 EUR cu TVA; 8 vizite statice si optiuni 1.000 EUR net/4 vizite. PI/ZT si intinderea completa Bauwerksbuch asteapta confirmare; nicio acceptare comerciala noua.','surse':sent['atasamente']},
 {'punct':4,'criteriu':'Atasamente si versiuni','rezultat':'FARA NOUTATI','detalii':'Niciun ID de atasament BERGER nou si niciun continut nou. Cele 3 PDF-uri reale din mesajul Sent au fost integral descarcate/hash-verificate la 16:01; se reutilizeaza sursele neschimbate.','surse':sent['atasamente']},
 {'punct':5,'criteriu':'Draft versus Sent / primire / acceptare','rezultat':'TRIMIS, DEJA RAPORTAT','detalii':'Get_draft confirma in continuare sent; mesajul Sent 96e74e69 confirma expedierea 2026.10.29 13:06:48 Romania si cele trei PDF-uri reale. Get_draft enumera cele doua PDF-uri atasate prin ciorna; scanul suplimentar este demonstrat de mesajul Sent. Nu exista confirmare de primire ori acceptare identificata.','surse':[sent['cale'],sent['json']]},
 {'punct':6,'criteriu':'Invitatii ICS si calendar','rezultat':'PENDING CUNOSCUT, FARA MODIFICARE','detalii':'Ultima invitatie arhivata SEQUENCE 2, acelasi UID ca invitatia initiala, ramane 2026.11.02 14:00–14:30 Viena /15:00–15:30 Romania. Participant NEEDS-ACTION. Calendarul EVA afiseaza in continuare evenimentul vechi 2026.10.29. Neconcordanta si RSVP neconfirmat au fost deja raportate la 16:01; nu sunt noutati. Nu se considera sedinta efectuata.','surse':['08. Corespondenta/2026.10.29 Verificare Berger Pech/2026.10.29 15-03-39 PRIMIT BERGER d5bc6ece.ics','calendar_readback in dovada verificarii']},
 {'punct':7,'criteriu':'Termene si actiuni necesare','rezultat':'PENDING CUNOSCUT, FARA ACTIUNE NOUA','detalii':status['urmatorul_pas'],'surse':status.get('sursa_status',[])},
]
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']};limits='Indicatori ultima sincronizare EVA: office '+local(sync['office@ac-wohnart.at'])+' Romania; Gmail '+local(sync['covaciu.gnm@gmail.com'])+' Romania. Mesajele neindexate ulterior pot lipsi. Acestia sunt indicatorii afisati, nu dovada exhaustivitatii; unele rezultate pot avea data mai recenta. Shared/team necautabile excluse.'
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger'],'mesaje_noi':0,'atasamente_noi_ID':0,'continuturi_documentare_noi':0,'query_count':len(p['searches']),'page_count':len(p['searches']),'metadate_unice':len(found),'mesaje_BERGER_deja_arhivate':len(p['scoped_email_ids']),'perioada':p['period'],'paginare_completa':True,'control_integral_casute':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'decizie_notificare':'DONT_NOTIFY','sursa':proof.as_posix()}
summary=f'''{day} {now.strftime('%H:%M:%S')} | CHECKLIST BERGER
Status scurt: Nicio comunicare, observatie contractuala, oferta/pret, atasament, invitatie sau actiune noua fata de verificarea 2026.10.29 16:01:36. Cele patru ID-uri BERGER sunt deja arhivate. Situatia in asteptare ramane neschimbata; nu se repeta notificarea.
Ultimul raspuns extern: invitatia Teams actualizata 2026.10.29 15:03:39 Romania, SEQUENCE 2, pentru 2026.11.02 14:00 Viena /15:00 Romania; nu este raspuns comercial.
Ultima trimitere: R11 2026.10.29 13:06:48 Romania cu 3 PDF-uri, deja raportata. Draft sent; fara confirmare de primire sau acceptare identificata.
Urmatorul pas cunoscut: {status['urmatorul_pas']}

'''
for c in checks:summary+=f"{c['punct']}. {c['criteriu']} — {c['rezultat']}\n{c['detalii']}\nSurse: {c['surse']}\n\n"
summary+=f'Acoperire: 25 cautari/25 pagini, 53 ID-uri metadate, 4 BERGER arhivate/0 noi; 49 metadate colaterale sau fara legatura BERGER, excluse motivat. Registrul ramane la {len(r["comunicatii"])} ID-uri; nicio modificare la comunicatii, ciorne, preturi sau atasamente.\n'+limits+'\nSursa: '+proof.as_posix()+'\nNu s-au trimis emailuri/RSVP, modificat contracte/documente comerciale sau calendar, semnat ori efectuat plati. PECH nu este obiectul acestui control.\n'
status['checklist_BERGER_ultim']={'checked_at_iso':stamp,'rezultat':'FARA NOUTATI','sursa':proof.as_posix(),'checklist':report.as_posix()};r['acoperire']['verificare_punctuala_BERGER']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert all(digest(r[k])==h for k,h in before.items()) and r['acoperire']['verificare_incrementala']==general
jsave(Path(p['baseline_register']),r);save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(Path(day+' '+name+'.txt'),summary)
prepend(base/'Parteneri'/(day+' Log discutii - Markus Berger.txt'),summary);prepend(Path('folder map/README.md'),summary+'\nChecklist: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'checklist':checks,'baseline_unique_ids':p['baseline']['register_count'],'final_unique_ids':len(r['comunicatii']),'previously_archived_not_repeated':p['scoped_email_ids'],'excluded_unrelated_BERGER':p['excluded_unrelated_email_ids'],'dovezi_originale':p,'general_baseline_preserved':general,'nota':'Nu sunt mesaje/atasamente BERGER noi de exportat; se reutilizeaza originalele deja verificate. Neconcordanta calendarului si confirmarile asteptate sunt cunoscute, nu declanseaza notificare noua.'})
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'checks':len(checks),'new_messages':0,'decision':'DONT_NOTIFY','register_count':len(r['comunicatii'])},ensure_ascii=False))
