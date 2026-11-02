from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil

ROOT=Path(__file__).resolve().parent.parent;DAY='2026.10.29';PREV='2026.10.28';TZ=ZoneInfo('Europe/Bucharest');NOW=datetime.now(TZ);STAMP=NOW.isoformat(timespec='seconds')
BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');OUT=Path('08. Corespondenta')/(DAY+' Verificare zilnica')
PROOF=OUT/(DAY+' Dovezi verificare EVA.json');REPORT=OUT/(DAY+' Raport verificare zilnica.txt');NEWREG=BASE/(DAY+' Registru comunicatii.json')
HIST=Path('folder map')/(DAY+' Istoric verificare '+NOW.strftime('%H-%M-%S'))
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p);dest=ROOT/p
 if dest.exists():
  old=ROOT/HIST/p;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,old)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.encode('utf-8'))
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'
def prepend(p,previous,text):
 p=Path(p);previous=Path(previous);src=p if (ROOT/p).exists() else previous
 old=(ROOT/src).read_text(encoding='utf-8-sig') if (ROOT/src).exists() else ''
 save(p,text+'\n\nISTORIC PASTRAT\n\n'+old)

p=read(Path('folder map/2026.10.29 Dovezi etapa generala.json'));r=read(Path(p['baseline_register']));ids={x['id'] for x in r['comunicatii']}
assert len(ids)==len(r['comunicatii'])==p['baseline_count']==845
assert len(p['pages'])==66 and not p['errors'] and not p['emails']
for page in p['pages']:assert page['result']['offset']+len(page['result']['items'])>=page['result']['total']
found={x['id']:x for page in p['pages'] for x in page['result']['items']};excluded={x['id'] for x in p['exclusions']}
assert len(found)==8 and len(excluded)==2 and set(found)-ids==excluded
assert {x['from_address'] for x in p['exclusions']}=={'offers@travel.wizznews.com','no-reply@sender.skyscanner.com'}
assert not any(x.get('raportare_generala_pendenta') for x in r.get('mesaje_incidentale_pentru_verificare_generala',[]))
protected={k:hashlib.sha256(json.dumps(r[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest() for k in ('comunicatii','drafturi')}
sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
limits='Office sincronizat pana la '+local(sync['office@ac-wohnart.at'])+' Romania; Gmail pana la '+local(sync['covaciu.gnm@gmail.com'])+' Romania. Mesajele ulterioare pot lipsi. Celelalte casute sunt acoperite pana la sincronizarile individuale din dovada EVA; shared/team nesearchable excluse.'
entry={'data':DAY,'checked_at_iso':STAMP,'perioada':'2026.10.27–2026.10.29; suprapunere de o zi fata de verificarea generala 2026.10.28; deduplicare inclusiv fata de verificarile BERGER/PECH 2026.10.28','cautari_complete':66,'pagini':66,'paginare_completa':True,'acoperire_actuala_office_completa':True,'mesaje_noi_ID':0,'mesaje_primite_ID':0,'mesaje_trimise_ID':0,'documente_originale_integrale_ID':0,'oferta_noua_identificata':False,'mesaje_deja_arhivate_raportate_acum':[],'sincronizari_originale':sync,'stare':'Nicio comunicare, oferta, modificare de pret sau servicii, document, termen nou ori confirmare de incasare identificata. Cele 6 mesaje relevante rezultate sunt deja arhivate si raportate. Doua reclame de calatorie excluse motivat.','limite':limits,'sursa':PROOF.as_posix()}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala']);r['acoperire']['verificare_incrementala']=entry;r['data_actualizarii']=DAY
r.setdefault('actualizari_punctuale',[]).append({'data':DAY,'tip':'Verificare generala','mesaje_noi':0,'sursa':PROOF.as_posix()})
for s in r['statusuri']:s['verificare_comunicari_2026_10_29']={'data':DAY,'checked_at_iso':STAMP,'mesaje_noi':0,'sursa':PROOF.as_posix()}
for k,h in protected.items():assert hashlib.sha256(json.dumps(r[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==h
jsave(NEWREG,r)
jsave(PROOF,{'verificare':entry,'baseline_register':p['baseline_register'],'baseline_ID_count':845,'final_ID_count':845,'new_relevant_email_ids':[],'already_archived_now_reported':[],'previously_reported_not_repeated':sorted(set(found)&ids),'excluded_unrelated_email_ids':sorted(excluded),'dovezi_originale':p,'nota':'Nicio noutate relevanta de exportat. Se reutilizeaza sursele celor 6 mesaje deja arhivate: observatiile BERGER, invitatia Teams, cele doua raspunsuri dupa discutii si cele doua mesaje de acces TRIMISE. Originalele integrale cu parole raman exclusiv in EVA; copiile locale redactate sunt reutilizate, fara citirea sau salvarea din nou a parolelor. attachment_names in cautare poate proveni din conversatie; verificarile get_email anterioare si originalele deja salvate raman sursa. Niciun atasament nou. Registrul atasamentelor ramane 2026.10.27, 908 pozitii. Nicio trimitere, semnare, plata sau modificare comerciala.'})
summary=DAY+' | Verificare zilnica Schallergasse 35\nVerificat: '+STAMP+'\n\nStatus scurt: Nu s-au identificat comunicari relevante noi, oferte, modificari de pret sau servicii, fisiere, termene ori confirmari de incasare fata de ultima verificare si raportarile punctuale.\nUltimul raspuns nou: niciunul identificat. Cele patru mesaje BERGER/PECH din 2026.10.27 si cele doua mesaje de acces TRIMISE in 2026.10.28 sunt deja arhivate si raportate; nu sunt repetate ca noutati.\nUrmatorul pas: urmarirea raspunsurilor, confirmarii functionarii accesului si documentelor necesare. Intalnirea Teams BERGER din 2026.10.29 ramane invitatie/programare; nu este considerata efectuata sau acceptare contractuala. Draftul MA37 nu este considerat trimis fara mesaj Sent ori alta dovada.\n\nAcoperire: 66 cautari / 66 pagini paginate integral, toate mesajele office primite si trimise si cautari globale dupa adresa, firme si referinte, inclusiv Gasperl, pentru 2026.10.27–2026.10.29. 8 ID-uri rezultate: 6 deja arhivate/raportate si 2 reclame Wizz Air/Skyscanner fara legatura, excluse motivat. Registrul ramane la 845 ID-uri unice; cele 16 inregistrari de ciorne istorice sunt pastrate nemodificate. Niciun atasament relevant nou; registrul atasamentelor ramane 2026.10.27, 908 pozitii.\n'+limits+'\nSursa: '+PROOF.as_posix()+'\nNu s-au trimis emailuri, modificat contracte, semnat ori efectuat plati. Trimiterea mesajelor de acces nu constituie confirmare de primire sau functionare.\n'
save(REPORT,summary)
for name in ('Status proiect','Log progres proiect'):prepend(Path(DAY+' '+name+'.txt'),Path(PREV+' '+name+'.txt'),summary)
for partner in ('Markus Berger','Pech','WOHR','Roland Gasperl'):
 s=next(x for x in r['statusuri'] if x.get('partener')==partner)
 text=DAY+' | '+partner+'\nStatus scurt: Nicio noutate la verificarea generala; status anterior pastrat: '+s['status']+'\nUltimul raspuns extern: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUltima trimitere: '+str(s.get('ultima_trimitere','conform surselor anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSursa verificarii: '+PROOF.as_posix()+'\nSurse status anterior: '+str(s.get('sursa_status'))+'\n'+limits+'\n'
 prepend(BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt'),BASE/'Parteneri'/(PREV+' Log discutii - '+partner+'.txt'),text)
prepend(Path('folder map/README.md'),Path('folder map/README.md'),summary+'\nPuncte curente: ../'+NEWREG.as_posix()+'; ../'+DAY+' Status proiect.txt; ../'+DAY+' Log progres proiect.txt.\n')
print(json.dumps({'register':NEWREG.as_posix(),'report':REPORT.as_posix(),'proof':PROOF.as_posix(),'count':845,'new_relevant':0,'entry':entry},ensure_ascii=False))
