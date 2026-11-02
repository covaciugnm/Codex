from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,re
ROOT=Path.cwd();TZ=ZoneInfo('Europe/Bucharest');now=datetime.now(TZ);DAY=now.strftime('%Y.%m.%d');TAG=now.strftime('%H-%M-%S');STAMP=now.isoformat(timespec='seconds');BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');OUT=Path('08. Corespondenta/2026.10.29 Verificare Berger Pech');HIST=Path('folder map')/(DAY+' Istoric BP '+TAG)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 dest=ROOT/p
 if dest.exists():
  b=ROOT/HIST/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t):save(p,t+'\n\nISTORIC PASTRAT\n\n'+((ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else ''))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'
p=read(Path('folder map/2026.10.29 Dovezi etapa BP dupa-amiaza.json'));assert not p['errors'];r=read(Path(p['baseline_register']));assert len(r['comunicatii'])==p['baseline_count']==845;general=r['acoperire']['verificare_incrementala'].copy();known={e['id'] for e in r['comunicatii']}
for s in p['searches']:assert s['args']['offset']+len(s['result']['items'])>=s['result']['total']
metas={x['id']:x for s in p['searches'] for x in s['result']['items']};newids=[m['id'] for m in p['new_mails']];assert len(newids)==3 and not known.intersection(newids)
attreg=read(BASE/'2026.10.27 Registru atasamente.json');attbefore=len(attreg);exports=[];ics_records=[];downloaded=[]
for pair in p['new_mails']:
 e=pair['email'];assert not e.get('truncated');sent=e['is_sent'];sens='TRIMIS' if sent else 'PRIMIT';dt=datetime.fromisoformat(e['received_at'].replace('Z','+00:00'));tag=dt.astimezone(TZ).strftime('%Y.%m.%d %H-%M-%S')+' '+sens+' BERGER '+e['id'][:8];jp=OUT/(tag+'.json');tp=OUT/(tag+'.txt')
 jsave(jp,{'data_lizibila':dt.astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S'),'statut':sens,'original_EVA':e,'nota':'Export API cu text original si metadate; nu reprezinta export MIME/EML integral.'})
 text='Data lizibila: '+local(e['received_at'])+' Romania\nData tehnica originala: '+e['received_at']+'\nStatut: '+sens+'\nSubiect: '+e['subject']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e.get('cc',[]))+'\nID Eva-Mail: '+e['id']+'\nSursa JSON: '+jp.as_posix()+'\n\nTEXT ORIGINAL EVA\n\n'+e['text'];save(tp,text)
 files=[]
 for a in e.get('attachments',[]):
  name=DAY+' TRIMIS BERGER 96e74e69 - '+re.sub(r'^2026[._]10[._](?:27|29)[ _]*','',a['name']);fp=OUT/name;assert (ROOT/fp).stat().st_size==a['size'];h=sha(fp)
  expected={'2026_10_27_Werkvertrag_Anmerkungen.pdf':'388db92e0281dd12755f312c00fe268973b08acabd3e03b0ea73a1a232b3e63f','2026.10.29 Werkvertrag BERGER R11.pdf':'934d95049f46d116b3e7db50835ac153d9e48c2c720fdc1b313a8b01df772eb3','2026.10.29 BERGER Comparatie contract R09 R11 cu decizii.pdf':'47765cfe908572ca4b95488eaae967504737e8c59a2055479b01b3aa0876cb76'};assert h==expected[a['name']]
  item={'id':a['id'],'email_id':e['id'],'data':DAY,'partener':'Markus Berger','sens':'TRIMIS','nume_original':a['name'],'octeti':a['size'],'sha256':h,'cale':fp.as_posix(),'stare':'original integral descarcat din mesajul Sent; hash identic cu sursa deja verificata; fara continut documentar nou'};attreg.append(item);downloaded.append(item);files.append(fp.as_posix())
 if 'BEGIN:VCALENDAR' in e['text']:
  raw=e['text'][e['text'].index('BEGIN:VCALENDAR'):];ip=OUT/(tag+'.ics');(ROOT/ip).write_bytes(raw.encode('utf-8'));unfold=re.sub(r'\r?\n[ \t]','',raw)
  def val(key):return re.search(r'^'+key+r':(.+)$',unfold,re.M).group(1).strip()
  uid=val('UID');seq=int(val('SEQUENCE'));start=val(r'DTSTART;TZID=W\. Europe Standard Time');end=val(r'DTEND;TZID=W\. Europe Standard Time');st=datetime.strptime(start,'%Y%m%dT%H%M%S').replace(tzinfo=ZoneInfo('Europe/Vienna'));en=datetime.strptime(end,'%Y%m%dT%H%M%S').replace(tzinfo=ZoneInfo('Europe/Vienna'));ics_records.append({'email_id':e['id'],'uid':uid,'sequence':seq,'start_vienna':st.isoformat(),'end_vienna':en.isoformat(),'start_romania':st.astimezone(TZ).isoformat(),'end_romania':en.astimezone(TZ).isoformat(),'attendee_partstat':'NEEDS-ACTION','cale':ip.as_posix()})
 item={'data':dt.astimezone(TZ).strftime('%Y.%m.%d'),'ora_utc':dt.strftime('%H:%M:%S'),'partener':'Markus Berger','domeniu':'Contract R11 transmis' if sent else 'Actualizare invitatie Teams','sens':sens,'subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e.get('cc',[]),'id':e['id'],'cale':tp.as_posix(),'json':jp.as_posix(),'atasamente':files,'trunchiat':False,'data_preluarii':DAY};r['comunicatii'].append(item);exports.append(item)
old=read(Path('08. Corespondenta/2026.10.27 BERGER contract adnotat si Teams/2026.10.27 13-46-46 PRIMIT BERGER 1338b947.json'));oldun=re.sub(r'\r?\n[ \t]','',old['text']);olduid=re.search(r'^UID:(.+)$',oldun,re.M).group(1).strip();assert len({x['uid'] for x in ics_records})==1 and ics_records[0]['uid']==olduid
latest=max(ics_records,key=lambda a:a['sequence']);assert latest['sequence']==2 and latest['start_vienna'].startswith('2026-11-02T14:00:00')
jsave(BASE/(DAY+' Registru atasamente.json'),attreg)
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']};limits='Office sincronizat pana la '+local(sync['office@ac-wohnart.at'])+' Romania; Gmail pana la '+local(sync['covaciu.gnm@gmail.com'])+' Romania. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.'
proofpath=OUT/(DAY+' '+TAG+' Dovezi verificare EVA.json');reportpath=OUT/(DAY+' '+TAG+' Raport verificare BERGER PECH.txt')
entry={'data':DAY,'checked_at_iso':STAMP,'parteneri':['Markus Berger','Pech'],'mesaje_noi':3,'mesaje_primite_noi':2,'mesaje_trimise_noi':1,'atasamente_noi_ID':3,'continuturi_documentare_noi':0,'query_count':len(p['searches']),'page_count':len(p['searches']),'perioada':p['period'],'paginare_completa':True,'control_integral_casute':True,'metadate_unice':len(metas),'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'sursa':proofpath.as_posix()}
berger_status='2026.10.29: R11 este TRIMIS la 13:06:48 Romania catre office@bmberger.at, cu 3 PDF-uri (scanul adnotat original, contractul R11, comparatia R09/R11). Draft EVA sent, mesaj Sent verificat. Nu exista confirmare de primire sau acceptare. Doua actualizari Teams pentru acelasi UID; ultima SEQUENCE 2 muta discutia la 2026.11.02 14:00–14:30 Viena / 15:00–15:30 Romania; RSVP NEEDS-ACTION. Calendarul EVA afiseaza inca evenimentul vechi 2026.10.29.'
nextstep='Verificarea si confirmarea noii invitatii Teams pentru 2026.11.02, ora 15:00 Romania (14:00 Viena); reconcilierea calendarului ramas la 2026.10.29. Urmarirea raspunsului BERGER la R11: Bauwerksbuch complet 2.500 EUR net, total 47.500 net/57.000 brut, PI/ZT si includerea in pret, persoane si calendar valoric. Nicio acceptare a acestor clauze dedusa din invitatie.'
for s in r['statusuri']:
 if s.get('partener')=='Markus Berger':
  s.setdefault('istoric_actualizari_contractuale',[]).append({'data':DAY,'status_anterior':s.get('status'),'urmatorul_pas_anterior':s.get('urmatorul_pas')});s.update(status=berger_status,ultimul_raspuns='Invitatie Teams actualizata de Meetingtisch, 2026.10.29 15:03:39 Romania; SEQUENCE 2, 2026.11.02 ora 14:00 Viena. Nu este raspuns comercial la R11.',ultima_trimitere='R11 TRIMIS 2026.10.29 13:06:48 Romania; ID 96e74e69-7ff6-402c-9959-597c0b472950; trei PDF-uri',urmatorul_pas=nextstep,sursa_status=[x['cale'] for x in exports],data_actualizarii=DAY)
 if s.get('partener') in ('Markus Berger','Pech'):s['verificare_punctuala_BERGER_PECH_2026_10_29']={'checked_at_iso':STAMP,'mesaje_noi':3 if s['partener']=='Markus Berger' else 0,'sursa':proofpath.as_posix()}
for d in r['drafturi']:
 if d.get('id')==p['draft_readback']['id']:
  d.setdefault('istoric_status',[]).append({'status':d.get('status'),'sursa':d.get('sursa'),'data':STAMP});d.update(status='sent',statut='TRIMIS confirmat prin mesaj Sent si get_draft',email_trimis_id='96e74e69-7ff6-402c-9959-597c0b472950',data_trimiterii='2026-10-29T11:06:48.351968Z',sursa=next(x['json'] for x in exports if x['sens']=='TRIMIS'),data_verificarii=STAMP)
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r['acoperire']['registru_atasamente_randuri']=len(attreg);r['verificari_parteneri'].append(entry)
for e in p['incidental_project_metadata']:
 if not any(a.get('id')==e['id'] for a in r.setdefault('mesaje_incidentale_pentru_verificare_generala',[])):r['mesaje_incidentale_pentru_verificare_generala'].append(dict(e,nota='Identificat incidental la control BP; corp/atasamente nerevizuite, in asteptarea verificarii generale. Nu este noutate BP.'))
assert len(r['comunicatii'])==848 and len(r['drafturi'])==17 and r['acoperire']['verificare_incrementala']==general;jsave(Path(p['baseline_register']),r)
report=f'''{DAY} {now.strftime('%H:%M:%S')} | Verificare BERGER/PECH

Status scurt BERGER: {berger_status}
Ultimul raspuns: doua actualizari de invitatie, nu doua sedinte; versiunea SEQUENCE 1 (2026.11.02 13:00 Viena) este depasita de SEQUENCE 2 (14:00 Viena). Identitatea UID cu invitatia initiala 2026.10.29 este verificata. STATUS:CONFIRMED apartine evenimentului organizatorului; participantul office ramane NEEDS-ACTION, fara acceptare RSVP dedusa. Calendar EVA citit, nemodificat, nereconciliat.
Contract: 45.000 EUR net initial + 2.500 EUR net Bauwerksbuch = 47.500 EUR net / 57.000 EUR cu TVA, propunere trimisa; nicio noua oferta, acceptare a pretului, contract semnat ori plata. Cele trei atasamente Sent sunt integral descarcate si SHA-256 identice cu sursele verificate; trei ID-uri de document noi, zero continuturi documentare noi.
Urmatorul pas BERGER: {nextstep}

PECH: nicio comunicare, oferta, pret, termen sau atasament nou. Ultimul raspuns extern ramane 2026.10.27, recomandarea arhitectului Roland Gasperl; nu este mandat sau oferta acceptata. Urmatorul pas: urmarirea raspunsului comercial si delimitarea responsabililor conform statusului anterior.

Acoperire: {len(p['searches'])} cautari / {len(p['searches'])} pagini complete, 51 ID-uri de metadate unice, primit/trimis in office si Gmail, cautari globale domenii/adrese/firme/proiect/referinte, inclusiv nelivrari. 3 mesaje BP noi, 2 BP deja arhivate; 4 metadate de proiect din alte subiecte rezervate verificarii generale; 42 metadate fara legatura BP. Nicio nelivrare BP identificata. Registru 845 -> 848 ID-uri; 17 istoric ciorne; registru atasamente {attbefore} -> {len(attreg)}. Limitele/cifrele istorice ale preluarii generale nu sunt extinse automat.
{limits}
Surse: {proofpath.as_posix()}; '''+'; '.join(x['cale'] for x in exports)+'''
Nu s-au trimis emailuri, modificat contracte/documente comerciale sau calendar, semnat ori efectuat plati. Trimiterea efectuata de utilizator este doar constatata prin EVA.
'''
save(reportpath,report)
for name in ('Status proiect','Log progres proiect'):prepend(Path(DAY+' '+name+'.txt'),report)
for partner in ('Markus Berger','Pech'):prepend(BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt'),report)
prepend(Path('folder map/README.md'),report+'\nRaport: ../'+reportpath.as_posix())
jsave(proofpath,{'verificare':entry,'baseline_unique_ids':845,'final_unique_ids':848,'new_BP_email_ids':newids,'exports':exports,'downloaded':downloaded,'ical_versions':ics_records,'latest_event':latest,'calendar_discrepancy':'Calendar EVA inca 2026.10.29; invitatia cu acelasi UID actualizata la 2026.11.02; nu s-a modificat calendar/RSVP.','dovezi_originale':p,'general_baseline_preserved':general,'atasamente_rows_before':attbefore,'atasamente_rows_after':len(attreg)})
print(json.dumps({'report':reportpath.as_posix(),'proof':proofpath.as_posix(),'new_messages':3,'latest_event':latest,'register_count':848,'attachments':len(attreg)},ensure_ascii=False))
