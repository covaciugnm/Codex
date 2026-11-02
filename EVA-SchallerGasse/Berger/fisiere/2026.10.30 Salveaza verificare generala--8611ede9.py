from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import json,hashlib,shutil,re
ROOT=Path.cwd();TZ=ZoneInfo('Europe/Bucharest');NOW=datetime.now(TZ);DAY=NOW.strftime('%Y.%m.%d');STAMP=NOW.isoformat(timespec='seconds');TAG=NOW.strftime('%H-%M-%S');BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');OUT=Path('08. Corespondenta')/(DAY+' Verificare zilnica');HIST=Path('folder map')/(DAY+' Istoric verificare '+TAG)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def save(p,t):
 dest=ROOT/p
 if dest.exists():
  old=ROOT/HIST/p;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,old)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t,previous=None):
 old=(ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else ((ROOT/previous).read_text(encoding='utf-8-sig') if previous and (ROOT/previous).exists() else '')
 if old.splitlines() and t.splitlines() and old.splitlines()[0]==t.splitlines()[0]:old=old.partition('\n\nISTORIC PASTRAT\n\n')[2]
 save(p,t+'\n\nISTORIC PASTRAT\n\n'+old)
def unwrap(j):return j.get('original_EVA',j.get('email',j))
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'
def norm(t):return t.replace('\r\n','\n').strip()
P=read(Path('folder map/2026.10.30 Dovezi etapa generala.json'));assert not P['errors'] and not P['secondary_errors'];R=read(BASE/'2026.10.29 Registru comunicatii.json');oldcount=len(R['comunicatii']);known={x['id'] for x in R['comunicatii']};IDX=read(Path('folder map/inventar.json'));I={x['cale']:x for x in IDX}
for pg in P['pages']:assert pg['args']['offset']+len(pg['result']['items'])>=pg['result']['total']
METAS={e['id']:e for pg in P['pages'] for e in pg['result']['items']};sources={};cached={};already_reported=[];exports=[];attadds=[]
LOCAL={
'8f1be79a-83fc-4713-9ff0-bc5e3e4f4cd7':Path('05. Asigurari/Asigurare cladire/2026.10.29 Raspuns Donau/2026.10.29 Email primit Donau.json'),
'478abcb0-1094-4b10-b3e4-ecbc02840715':Path('08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.29 PRIMIT 478abcb0.json'),
'c45958f2-9372-4430-acfe-f175759221cf':Path('08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.29 TRIMIS c45958f2.json'),
'f36feb1c-1b40-43f8-b34b-7f7e47dcedac':Path('08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.29 TRIMIS f36feb1c.json')}
DONAU=read(Path('05. Asigurari/Asigurare cladire/2026.10.29 Raspuns Donau/2026.10.29 Manifest anexe.json'))
CAPRA=read(Path('08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.29 Dovezi cautari si acoperire.json'))['attachments_saved'];AM={x['id']:{'path':x.get('file',x.get('path')),'sha256':x['sha256'],'size':x.get('size')} for x in DONAU+CAPRA}
ar_source=BASE/'2026.10.29 Registru atasamente.json';AR=read(ar_source);old_attcount=len(AR);knownatt={x['id'] for x in AR}
for m in P['primary_mails']:
 e=m['email'];eid=e['id'];assert not e['truncated'];cached[eid]=e
 if eid in LOCAL:
  lp=LOCAL[eid];assert lp.as_posix() in I and sha(lp)==I[lp.as_posix()]['sha256'];orig=unwrap(read(lp));assert norm(orig['text'])==norm(e['text']);already_reported.append(eid)
 sent=e['is_sent'];sens='TRIMIS' if sent else 'PRIMIT';partner='WOHR' if 'woehr' in e['from_address'].lower() else ('Donau Versicherung' if 'donau' in e['from_address'].lower() else ('MA37' if eid=='c45958f2-9372-4430-acfe-f175759221cf' else 'CERHA HEMPEL'))
 dt=datetime.fromisoformat(e['received_at'].replace('Z','+00:00'));label=dt.astimezone(TZ).strftime('%Y.%m.%d %H-%M-%S')+' '+sens+' '+partner+' '+eid[:8];jp=OUT/(label+'.json');tp=OUT/(label+'.txt');files=[]
 for a in e.get('attachments',[]):
  aid=a['id']
  if partner=='WOHR':
   fp=OUT/'Anexe WOEHR'/('2026.10.29 '+a['name']);assert (ROOT/fp).stat().st_size==a['size'];ver='Original integral descarcat HTTP din EVA in aceasta verificare; cifrele si campurile protocolului verificate vizual.'
  else:
   assert aid in AM,(aid,a['name']);fp=Path(AM[aid]['path']);assert fp.as_posix() in I and sha(fp)==I[fp.as_posix()]['sha256']==AM[aid]['sha256'];assert (ROOT/fp).stat().st_size==a['size'];ver='Original deja salvat in actualizarea punctuala 2026.10.29; neschimbat SHA256 fata de index si manifest; reutilizat, fara pretinderea unei noi descarcari din EVA.'
  row={'id':aid,'email_id':eid,'data':dt.astimezone(TZ).strftime('%Y.%m.%d'),'partener':partner,'nume_original':a['name'],'octeti':a['size'],'sha256':sha(fp),'cale':fp.as_posix(),'stare':ver};files.append(fp.as_posix());attadds.append(row)
  if aid not in knownatt:AR.append(row);knownatt.add(aid)
 jsave(jp,{'data_lizibila':local(e['received_at']),'statut':sens,'original_EVA':e,'deja_arhivat_raportat_punctual':eid in LOCAL,'sursa_punctuala':LOCAL[eid].as_posix() if eid in LOCAL else None,'nota':'Export API cu text original si metadate; nu este MIME original. Integrare in registrul general, nu o comunicare noua pentru mesajele deja discutate.'})
 meta='Data lizibila: '+local(e['received_at'])+' Romania\nData tehnica originala: '+e['received_at']+'\nStatut: '+sens+'\nSubiect: '+e['subject']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e.get('cc',[]))+'\nID Eva-Mail: '+eid+'\nSursa JSON: '+jp.as_posix()+'\nAtasamente: '+str(files)+'\n\nTEXT ORIGINAL EVA\n\n'+e['text'];save(tp,meta)
 row={'data':dt.astimezone(TZ).strftime('%Y.%m.%d'),'ora_utc':dt.strftime('%H:%M:%S'),'partener':partner,'domeniu':'Proiect Schallergasse35','sens':sens,'subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e.get('cc',[]),'id':eid,'cale':tp.as_posix(),'json':jp.as_posix(),'atasamente':files,'trunchiat':False,'data_preluarii':DAY,'deja_raportat_punctual':eid in LOCAL}
 sources[eid]=row
 if eid not in known:R['comunicatii'].append(row);known.add(eid);exports.append(row)
# Canonical originals for the already-reported BERGER messages used to match mirror connections.
for row in R['comunicatii']:
 if row['id'] in ('96e74e69-7ff6-402c-9959-597c0b472950','d5bc6ece-d75a-4510-be57-9153b380adfa','eb6ea055-27bb-44b8-88eb-ff4b77618b21'):
  jp=Path(row.get('json',str(Path(row['cale']).with_suffix('.json'))));cached[row['id']]=unwrap(read(jp))
aliases=[]
for m in P['secondary_mails']:
 e=m['email'];matches=[(cid,c) for cid,c in cached.items() if c.get('thread_id')==e.get('thread_id') and c.get('from_address','').lower()==e.get('from_address','').lower() and c['subject']==e['subject'] and norm(c['text'])==norm(e['text'])];assert len(matches)==1,(e['id'],len(matches));cid,c=matches[0]
 ca=sorted((a['name'],a.get('size')) for a in c.get('attachments',[]));ea=sorted((a['name'],a.get('size')) for a in e.get('attachments',[]));assert ca==ea,(cid,ca,ea)
 label='2026.10.29 Alias EVA '+e['id'][:8]+'.json';fp=OUT/'Alias conexiune office'/label;jsave(fp,{'data_lizibila':local(e['received_at']),'canonical_email_id':cid,'link_id':m['link_id'],'original_EVA':e,'verificare':'Message-ID/thread_id, expeditor, subiect si text integral identice; numele/dimensiunile anexelor corespund. Nu se pretinde o descarcare/hash integral separat al anexelor conexiunii oglinda.'});aliases.append({'alias_id':e['id'],'canonical_id':cid,'link_id':m['link_id'],'cale':fp.as_posix(),'verificare':'thread_id + body exact + sender/subject + attachment names/sizes'})
for aid,cid in P['sensitive_aliases_metadata_only'].items():
 e=METAS[aid];aliases.append({'alias_id':aid,'canonical_id':cid,'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','metadata':e,'verificare':'Metadate: expeditor/destinatar/subiect/data si lipsa anexelor corespund sursei canonice; corpul cu credentiale nu este recitit/rearhivat. Comparatie MIME/byte integrala neefectuata.'})
R.setdefault('aliasuri_email_EVA',[])
for a in aliases:
 if not any(x.get('alias_id')==a['alias_id'] for x in R['aliasuri_email_EVA']):R['aliasuri_email_EVA'].append(a)
new_ids=[x['id'] for x in exports];assert len(new_ids)==5 and len(already_reported)==4 and len(aliases)==10
R['data_actualizarii']=DAY;regpath=BASE/(DAY+' Registru comunicatii.json');arpath=BASE/(DAY+' Registru atasamente.json');jsave(arpath,AR)
invoice='7632b31a-e277-4b7d-a486-63e11aa1d04e';invsource=sources[invoice];invoicepdf=next(p for p in invsource['atasamente'] if 'Rechnung' in p);protocol=next(p for p in invsource['atasamente'] if '20261027' in p);due=(datetime(2026,10,29)+timedelta(days=14)).strftime('%Y.%m.%d');assert due=='2026.11.12'
facts={'invoice_no':'26101261SR','invoice_date':'2026.10.29','work_date':'2026.10.27','maintenance_net':285,'repair_hour_net':115,'net':400,'vat':80,'gross':480,'due_calculated':due,'due_basis':'14 zile de la data facturii, fara deduceri','payment_status':'Factura indica Offener Betrag; plata nu este confirmata in aceasta verificare.','equipment':'WOHR PL 422, doua locuri, fabrica 971105','protocol_defects':[{'punct':'1.3','constatare':'Fundamenterder nu este conectat: Nein.'},{'punct':'2.4','constatare':'Fixarea conductelor electrice si hidraulice: Nein.'},{'punct':'2.5-2.6','constatare':'Platforme si fosa: Verschmutzt.'},{'punct':'4.2','constatare':'Cilindrii hidraulici: Nicht in Ordnung (Rep. erf.); observatie li+re. undicht, scurgeri la stanga si dreapta.'},{'punct':'4.5','constatare':'Ulei hidraulic: Nicht in O. (Olanalyse notwendig), analiza necesara.'},{'punct':'4.9','constatare':'Conducte hidraulice: Nicht in O. (Austausch notwendig), inlocuire necesara.'}],'tightening_annotated':['2.3: Nicht in Ordnung (Angezogen)','4.10: Nicht in O. (Nachgezogen)'],'missing_release':'Protocolul nu contine o confirmare explicita ca instalatia poate fi utilizata in siguranta pana la remediere.','remedial_offer':'Promisa ulterior de Regina Helfer; intarziere din cauza incarcarii; fara pret sau data ferma.','repair_authorization':'Confirmarea 2026.09.15 accepta pretul de mentenanta 285 EUR net. Solicitarea initiala cerea deviz pentru aprobare inainte de reparatii; justificarea orei suplimentare de 115 EUR si aprobarea se cer separat, fara a declara automat factura nevalabila.','new_bank_notice':'Factura mentioneaza un cont bancar nou; nu se efectueaza plata.','sources':[invsource['cale'],invoicepdf,protocol,'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/WOHR/2026.09.15 14-03 TRIMIS Re WG Wartung und gegebenenfalls Reparat ee722e0a.txt']}
jsave(OUT/(DAY+' Fapte verificate WOEHR factura si protocol.json'),facts)
wohrstatus='WÖHR confirma efectuarea mentenantei la 2026.10.27 prin factura 26101261SR si protocolul datat. Factura 2026.10.29: 285 EUR mentenanta +115 EUR o ora reparatie =400 net +80 TVA =480 EUR brut; scadenta calculata 2026.11.12. Protocolul arata scurgeri la ambii cilindri, conducte de inlocuit, analiza uleiului, legatura de pamant si fixari neconsemnate ca existente; reparatii suplimentare de ofertat, fara pret sau termen ferm. Plata si remedierea integrala neconfirmate.'
wohrnext='Solicitarea ofertei de remediere, a prioritatii/termenului si a confirmarii scrise privind utilizarea instalatiei pana la reparatie. Clarificarea justificarii/aprobarii orei suplimentare de 115 EUR net, fata de mentenanta de 285 EUR net confirmata initial; verificarea facturii si a contului indicat nou inainte de aprobarea platii. Scadenta facturii 2026.11.12; nu se efectueaza plata automat.'
updates={
'WOHR':{'status':wohrstatus,'ultimul_raspuns':'Regina Helfer, 2026.10.29 17:27:24 Romania: transmite factura si protocolul; promite oferta de remediere, cu intarziere din cauza volumului de lucru.','urmatorul_pas':wohrnext,'sursa_status':invsource['atasamente']+[invsource['cale']]},
'Donau Versicherung':{'status':'Integrare in registrul general a raspunsului 2026.10.29 deja analizat si raportat punctual: confirma incasarea primei si acoperirea actuala; mentine expirarea ordinara 2036.01.01. Nu confirma sold zero, alocarea detaliata ori acoperirea retroactiva. Nicio comunicare ulterioara noua identificata.','ultimul_raspuns':'Andreas Höbinger 2026.10.29: documente contractuale si precizari; sursele/anexele punctuale neschimbate fata de index.','urmatorul_pas':'Urmarirea clarificarii alocarii celor 4.775,43 EUR, soldului, perioadelor/spartelor acoperite si concluziilor juridice deja redactate; fara a repeta raspunsul ca noutate.','sursa_status':[sources['8f1be79a-83fc-4713-9ff0-bc5e3e4f4cd7']['cale'],'05. Asigurari/Asigurare cladire/2026.10.29 Raspuns Donau/2026.10.29 Email primit Donau.json']},
'CERHA HEMPEL':{'status':'Integrare corespondenta 2026.10.29 deja raportata punctual: solicitare A&C privind planurile vizate si interventia efectiv trimisa de Capra la MA37, A&C in CC. Nu este raspuns al autoritatii si nici predare de documente.','ultimul_raspuns':'Capra 2026.10.29 13:34:23 Romania cere MA37 existenta documentelor in Bauakt/Uberwachungsakt, acces si termene posibile.','urmatorul_pas':'Urmarirea raspunsului MA37 si a recuperarii planurilor; termenul solicitat vanzatoarei prin Capra 2026.11.11 ramane cerere, fara acceptare identificata.','sursa_status':[sources[x]['cale'] for x in ('f36feb1c-1b40-43f8-b34b-7f7e47dcedac','478abcb0-1094-4b10-b3e4-ecbc02840715')]},
'MA37':{'status':'Cererea directa A&C TRIMISA 2026.10.29 si revenirea avocatului sunt deja raportate. Niciun raspuns nou al autoritatii sau confirmare a localizarii/predarii planurilor identificata.','ultimul_raspuns':'Ultima comunicare actuala este cererea trimisa A&C 2026.10.29 12:49:46 Romania, nu raspuns autoritate; Capra revine separat la 13:34:23.','urmatorul_pas':'Urmarirea accesului Bauakt/Uberwachungsakt, exemplarului C, inventarului, copiilor vizate si stadiului; termen de raspuns solicitat in cererea directa 2026.11.18, fara acceptare autoritate presupusa.','sursa_status':[sources['c45958f2-9372-4430-acfe-f175759221cf']['cale'],sources['478abcb0-1094-4b10-b3e4-ecbc02840715']['cale']]}}
for s in R['statusuri']:
 if s.get('partener') in updates:
  s.setdefault('istoric_status',[]).append({'data_preluarii':DAY,**{k:s.get(k) for k in ('status','ultimul_raspuns','urmatorul_pas','sursa_status')}});s.update(updates[s['partener']]);s['data_actualizarii']=DAY
draft=P['pech_draft_readback'];assert draft['status']=='pending';pech=next((s for s in R['statusuri'] if s.get('partener')=='Pech'),None)
if pech is not None:pech['draft_amanare_2026_10_29']={'id':draft['id'],'status':'pending / NETRIMIS','solicitare':'Amanare discutie pana 2026.11.03, ora la propunerea PECH; nu este amanare acceptata.','verificat':STAMP,'sursa':'08. Corespondenta/2026.10.29 PECH amanare intalnire/2026.10.29 DRAFT PECH amanare - EVA.json'}
syncp={x['email']:x.get('last_sync') for x in P['mailboxes_primary']['mailboxes']};syncs={x['email']:x.get('last_sync') for x in P['mailboxes_secondary']['mailboxes']};limits='Indicatori sincronizare: Primary office '+local(syncp.get('office@ac-wohnart.at'))+'; Gmail '+local(syncp.get('covaciu.gnm@gmail.com'))+'; a doua conexiune office '+local(syncs.get('office@ac-wohnart.at'))+' Romania. Sunt indicatorii afisati, nu dovada exhaustivitatii; mesajele ulterioare neindexate pot lipsi, shared/team necautabile excluse.'
proof=OUT/(DAY+' Dovezi verificare EVA.json');report=OUT/(DAY+' Raport verificare zilnica.txt')
entry={'data':DAY,'checked_at_iso':STAMP,'perioada':P['period'],'cautari_complete':len({json.dumps({k:v for k,v in pg['args'].items() if k!='offset'},sort_keys=True) for pg in P['pages']}),'pagini':len(P['pages']),'paginare_completa':True,'acoperire_actuala_office_completa':True,'metadate_unice_ID':len(METAS),'mesaje_noi_ID':5,'mesaje_noutati_neraportate':1,'mesaje_integrate_deja_raportate':4,'ID_alias_oglinda':len(aliases),'mesaje_primite_ID':3,'mesaje_trimise_ID':2,'atasamente_noi_registru_ID':len(AR)-old_attcount,'atasamente_cu_continut_nou':3,'documente_PDF_noi':2,'oferta_noua_identificata':False,'factura_noua':True,'sincronizari_originale_primary':syncp,'sincronizari_originale_secondary':syncs,'limite':limits,'sursa':proof.as_posix(),'stare':'Noutate WÖHR: factura 480 EUR brut si protocol cu defecte; alte patru comunicatii 2026.10.29 deja raportate sunt integrate fara a fi repetate ca noutati.'}
R.setdefault('istoric_verificari_incrementale',[]).append(R['acoperire']['verificare_incrementala']);R['acoperire']['verificare_incrementala']=entry;R['acoperire']['registru_atasamente_randuri']=len(AR)
assert len(R['comunicatii'])==oldcount+5;jsave(regpath,R)
summary=f'''{DAY} | Verificare zilnica Schallergasse 35
Verificat: {STAMP}

NOUTATI FATA DE COMUNICARILE DEJA RAPORTATE
WÖHR - factura si protocol noi, email primit 2026.10.29 17:27:24 Romania, ID {invoice}.
Executarea mentenantei din 2026.10.27 este acum sustinuta de factura si protocolul tehnicianului; nu numai de programare.
Factura 26101261SR din 2026.10.29: mentenanta doua locuri PL422 285,00 EUR net + o ora reparatie 115,00 EUR net =400,00 EUR net +80,00 EUR TVA =480,00 EUR brut. Factura indica suma deschisa; plata nu este confirmata. Termen 14 zile de la factura, scadenta calculata {due}. Factura mentioneaza cont bancar nou.
Protocol fabrica971105, datat2026.10.27: ambii cilindri hidraulici au scurgeri; conducte de inlocuit; analiza uleiului necesara; conectarea prizei de pamant si fixarea traseelor electrice/hidraulice sunt marcate Nein; platformele/fosa sunt murdare. Pozitiile2.3 si4.10 consemneaza strangere/restrangere, fara a declara ca toate defectele au fost remediate. Alte campuri raman necompletate; nu se presupune o certificare integrala de siguranta.
Regina Helfer spune ca un coleg va transmite oferta de remediere, cu intarziere din cauza incarcarii; nu exista pret sau termen ferm. Aceasta este promisiune de oferta, nu oferta primita ori comanda de reparatii.
Actiuni: {wohrnext}
Surse originale verificate vizual: {invoicepdf}; {protocol}; email {invsource['cale']}.

INTEGRARI FARA REPETAREA NOUTATILOR DEJA DISCUTATE
DONAU, Capra si MA37: patru mesaje din2026.10.29 au fost deja arhivate si raportate in dosarele punctuale; sunt acum integrate in registrul general cu anexele locale neschimbate. Confirmarea DONAU a incasarii/acoperirii actuale si pozitia2036 nu sunt noutati ale acestei rulari. Nu se deduc sold zero ori acoperire retroactiva. Cererile la MA37 sunt trimise; nu este raspuns al autoritatii. Termene solicitate11.11 si18.11, neacceptate expres.
BERGER: mesajul R11 trimis si invitatia actualizata2026.11.02 14:00Viena/15:00Romania sunt deja raportate; nicio observatie comerciala noua. PECH: ciorna de amanare pana2026.11.03 este in continuare pending/NETRIMISA la readback, fara acceptare a amanarii.
S-au identificat10 ID-uri din a doua conexiune care corespund mesajelor canonice. Opt corpuri au fost comparate integral prin Message-ID/text; doua mesaje de acces cu credentiale au numai metadate corelate, fara recitirea parolelor. Nu sunt numarate ca10 comunicari noi. Patru reclame fara legatura excluse.

ACOPERIRE
{len(P['pages'])} cautari/pagini complete, {len(METAS)} ID-uri metadate; control integral office primit/trimis in ambele conexiuni si cautari globale adresa/firme/referinte. Registru {oldcount}->{len(R['comunicatii'])} comunicatii canonice; {len(aliases)} aliasuri oglinda consemnate; registru atasamente {old_attcount}->{len(AR)} pozitii. Trei fisiere WÖHR descarcate integral; doua PDF-uri citite si randate, protocolul inspectat vizual. Anexele DONAU/Capra reutilizate SHA256 dupa manifest si index; nu se pretinde redescarcarea lor. Sursele tehnice si textul tertilor sunt pastrate. Nu s-au trimis emailuri, semnat, platit ori modificat contracte/calendar.
{limits}
Sursa generala: {proof.as_posix()}
'''
save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(Path(DAY+' '+name+'.txt'),summary,Path('2026.10.29 '+name+'.txt'))
for partner,up in updates.items():
 journal=BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt');prior=BASE/'Parteneri'/('2026.10.29 Log discutii - '+('MA37 Baupolizei' if partner=='MA37' else partner)+'.txt');text=DAY+' | '+partner+'\nStatus scurt: '+up['status']+'\nUltimul raspuns: '+up['ultimul_raspuns']+'\nUrmatorul pas: '+up['urmatorul_pas']+'\nSurse: '+str(up['sursa_status'])+'\nSursa verificare: '+proof.as_posix()+'\n'+limits;prepend(journal,text,prior)
prepend(Path('folder map/README.md'),summary+'\nRaport: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'baseline_unique_ids':oldcount,'final_unique_ids':len(R['comunicatii']),'new_general_ids':new_ids,'new_unreported_email_ids':[invoice],'already_reported_local_ids':already_reported,'aliases':aliases,'exports':exports,'attachments':attadds,'woehr_facts':facts,'dovezi_originale':P,'nota':'Doar WÖHR este noutate necomunicata. Nicio oferta de remediere primita, nicio plata sau acceptare comerciala presupusa.'})
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'invoice_pdf':invoicepdf,'protocol_pdf':protocol,'canonical_count':len(R['comunicatii']),'aliases':len(aliases),'attachments_count':len(AR),'due':due,'new_unreported':1,'decision':'NOTIFY'},ensure_ascii=False))
