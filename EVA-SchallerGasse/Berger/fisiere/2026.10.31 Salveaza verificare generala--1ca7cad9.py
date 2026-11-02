from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
ROOT=Path.cwd();TZ=ZoneInfo('Europe/Bucharest');now=datetime.now(TZ);DAY='2026.10.31';STAMP=now.isoformat(timespec='seconds');BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');OUT=Path('08. Corespondenta')/(DAY+' Verificare zilnica');changed=[];backup=Path('folder map')/(DAY+' Istoric verificare generala')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p)
 if p.exists():
  b=backup/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');changed.append(p.as_posix())
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t,prior=None):
 p=Path(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else Path(prior).read_text(encoding='utf-8-sig') if prior and Path(prior).exists() else ''
 save(p,t+'\n\nISTORIC PASTRAT\n\n'+old)
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
P=read('folder map/2026.10.31 Dovezi etapa generala.json');assert not P['errors'];R=read(P['baseline_register']);AR=read(BASE/'2026.10.30 Registru atasamente.json');oldcount=len(R['comunicatii']);oldac=len(AR);draft_hash=digest(R['drafturi'])
for pg in P['pages']:assert pg['args']['offset']+len(pg['result']['items'])>=pg['result']['total']
e=P['new_email'];m=P['mirror_email'];assert not e['truncated'] and not m['truncated'];assert e['thread_id']==m['thread_id'] and e['text'].replace('\r\n','\n').strip()==m['text'].replace('\r\n','\n').strip()
assert sorted((x['name'],x['size']) for x in e['attachments'])==sorted((x['name'],x['size']) for x in m['attachments'])
assert not e['is_sent'] and e['from_address'].lower()=='bogdan.capra@cerhahempel.com' and e['to']==['M.Kornhofer@cp-ag.at']
assert e['id'] not in {x['id'] for x in R['comunicatii']}
for a in e['attachments']:assert a['size']<1000 and a['name'].startswith('image') and a['content_type']=='image/jpeg'
jp=OUT/'2026.10.30 17-09-38 PRIMIT CERHA HEMPEL ed08780f.json';tp=jp.with_suffix('.txt')
jsave(jp,{'data_lizibila':local(e['received_at'])+' Romania','statut':'PRIMIT in casuta office; mesaj extern Capra catre Kornhofer','original_EVA':e,'nota':'Export API integral, nu MIME original. Destinatarii si CC sunt pastrati exact asa cum ii returneaza EVA. Nu se deduce confirmarea livrarii la Kornhofer. Cele trei imagini mici sunt logo/semnatura; metadate pastrate, fara anexe documentare noi.'})
save(tp,'Data lizibila: '+local(e['received_at'])+' Romania\nData tehnica: '+e['received_at']+'\nStatut: PRIMIT in office; corespondenta externa Capra catre Kornhofer\nSubiect: '+e['subject']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e.get('cc',[]))+'\nID Eva-Mail: '+e['id']+'\nJSON: '+jp.as_posix()+'\n\nTEXT ORIGINAL EVA\n\n'+e['text'])
row={'data':'2026.10.30','ora_utc':'15:09:38','partener':'CERHA HEMPEL','domeniu':'Recuperare documentatie autorizare','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e.get('cc',[]),'id':e['id'],'cale':tp.as_posix(),'json':jp.as_posix(),'atasamente':[],'atasamente_numai_metadate':[a['id'] for a in e['attachments']],'trunchiat':False,'data_preluarii':DAY,'deja_raportat_punctual':False}
R['comunicatii'].append(row)
for a in e['attachments']:
 if a['id'] not in {x['id'] for x in AR}:AR.append({'id':a['id'],'email_id':e['id'],'data':'2026.10.30','partener':'CERHA HEMPEL','nume_original':a['name'],'octeti':a['size'],'cale':None,'sha256':None,'stare':'Numai metadate: imagine mica de semnatura/logo fara continut documentar; text NO_TEXT_FOUND; originalul metadatelor este in exportul emailului.'})
aliasp=OUT/'2026.10.30 Alias EVA Capra 8250512a.json';jsave(aliasp,{'data_lizibila':local(m['received_at'])+' Romania','canonical_email_id':e['id'],'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','original_EVA':m,'verificare':'thread_id, expeditor, subiect si corp integral identice; aceleasi nume/dimensiuni anexe. Fara descarcare separata/hash al imaginilor de semnatura.'})
R.setdefault('aliasuri_email_EVA',[]).append({'alias_id':m['id'],'canonical_id':e['id'],'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','cale':aliasp.as_posix(),'verificare':'thread_id + body exact + sender/subject + attachment names/sizes'})
# Clear obsolete incidental flags only for IDs already integrated, retaining the history.
known={x['id'] for x in R['comunicatii']}
for inc in R.get('mesaje_incidentale_pentru_verificare_generala',[]):
 iid=inc.get('email_id',inc.get('id'))
 if iid in known:
  if inc.get('raportare_generala_pendenta') or 'in asteptarea verificarii generale' in inc.get('nota',''):
   inc['nota_anterioara']=inc.get('nota');inc['statut_anterior']=inc.get('statut');inc['raportare_generala_pendenta']=False;inc['statut']='Deja integrat si raportat punctual/general; verificat la '+DAY+'; nu se renotifica.';inc['data_verificarii_integrarii']=DAY
s=next(x for x in R['statusuri'] if x.get('partener')=='CERHA HEMPEL')
s.setdefault('istoric_status',[]).append({'data_preluarii':DAY,**{k:s.get(k) for k in ('status','ultimul_raspuns','urmatorul_pas','sursa_status')}})
s.update({'status':'2026.10.30 17:09:38 Romania: email primit in office cu cererea efectiva a lui Capra catre Kornhofer pentru planurile si documentele vizate ale autorizatiei. Nu mai este doar promisiunea contactarii. Niciun raspuns al vanzatorului ori plan vizat nou primit identificat.','ultimul_raspuns':'Capra cere Kornhofer planurile vizate, decizia integrala cu anexe/derogare §69/Planwechsel si Baubeschreibung in forma vizata; daca nu le detine, solicita indicarea posibilului detinator, inclusiv Pristounig. Reaminteste ca la predarea din 2026.03.17 a primit Bestandsunterlagen, Energieausweis DG si Bauphysik.','urmatorul_pas':'Urmarirea raspunsului Kornhofer si identificarea exemplarelor vizate, separat de documentatia existenta deja primita. Urmarirea MA37 continua; emailul nou nu fixeaza termen de raspuns si nu confirma recuperarea planurilor ori comunicarea unui cost.','sursa_status':[tp.as_posix(),jp.as_posix()],'ultima_comunicare':'2026.10.30','ultimul_primit':'2026.10.30','subiect_ultimul_primit':e['subject'],'data_actualizarii':DAY,'verificat':DAY})
syncp={x['email']:x.get('last_sync') for x in P['mailboxes_primary']['mailboxes']};syncs={x['email']:x.get('last_sync') for x in P['mailboxes_secondary']['mailboxes']}
limits='Ultima sincronizare afisata: Primary office '+local(syncp['office@ac-wohnart.at'])+'; Gmail '+local(syncp['covaciu.gnm@gmail.com'])+'; conexiunea office secundara '+local(syncs['office@ac-wohnart.at'])+' Romania. Sunt indicatori, nu dovada exhaustivitatii; mesajele ulterioare neindexate pot lipsi. Shared/team necautabile excluse.'
metas={x['id']:x for pg in P['pages'] for x in pg['result']['items']};qcount=len({json.dumps({k:v for k,v in pg['args'].items() if k!='offset'},sort_keys=True) for pg in P['pages']})
proof=OUT/(DAY+' Dovezi verificare EVA.json');report=OUT/(DAY+' Raport verificare zilnica.txt')
entry={'data':DAY,'checked_at_iso':STAMP,'perioada':P['period'],'cautari_complete':qcount,'pagini':len(P['pages']),'paginare_completa':True,'acoperire_actuala_office_completa':True,'metadate_unice_ID':len(metas),'mesaje_noi_ID':1,'mesaje_noutati_neraportate':1,'mesaje_integrate_deja_raportate':0,'ID_alias_oglinda_noi':1,'mesaje_primite_ID':1,'mesaje_trimise_de_utilizator_ID':0,'atasamente_noi_registru_ID':len(AR)-oldac,'atasamente_documentare_noi':0,'atasamente_numai_metadate_noi':3,'oferte_noi_identificate':False,'sincronizari_originale_primary':syncp,'sincronizari_originale_secondary':syncs,'limite':limits,'sursa':proof.as_posix(),'stare':'Capra a adresat efectiv cererea Kornhofer; o comunicatie canonica noua, fara pret/termen nou si fara planuri vizate primite. Raspunsul Capra de la 16:56:53 a fost deja raportat punctual si nu este renotificat.'}
R.setdefault('istoric_verificari_incrementale',[]).append(R['acoperire']['verificare_incrementala']);R['acoperire']['verificare_incrementala']=entry;R['acoperire']['registru_atasamente_randuri']=len(AR);R['data_actualizarii']=DAY
assert len(R['comunicatii'])==oldcount+1 and digest(R['drafturi'])==draft_hash
jsave(BASE/(DAY+' Registru comunicatii.json'),R);jsave(BASE/(DAY+' Registru atasamente.json'),AR)
summary=f"""{DAY} | VERIFICARE ZILNICA SCHALLERGASSE 35
Verificat: {STAMP}
Status scurt: O comunicare noua relevanta; Capra a adresat efectiv cererea catre Kornhofer. Nu sunt oferte sau preturi noi.

NOUTATE
Email primit in office la 2026.10.30 17:09:38 Romania, ID {e['id']}, de la Bogdan Capra catre M.Kornhofer@cp-ag.at.
Solicita verificarea detinerii planurilor de autorizare cu viza oficiala (situatie, niveluri, sectiuni, fatade, racordari vecini, cote), a deciziei integrale cu anexe, deciziei §69 si modificarilor/Planwechsel cu planurile aferente, precum si Baubeschreibung si restul documentelor de autorizare vizate.
Daca vanzatorul nu le detine, solicita indicarea posibilului detinator, inclusiv arhitectul Klaus Pristounig. Capra precizeaza distinct ca in 2026.03.17 a primit Bestandsunterlagen, Energieausweis DG si Bauphysik.
Acesta este un demers efectiv, ulterior promisiunii de la 16:56:53 deja raportate. Nu confirma primirea de catre Kornhofer, raspunsul acestuia sau recuperarea documentelor. EVA nu listeaza CC; nu se inventeaza un CC.
Preturi/sume: niciuna noua. Termene: niciun termen nou de raspuns. Anexe: numai 3 imagini mici de semnatura, fara documente tehnice noi.
Urmatorul pas: {s['urmatorul_pas']}
Surse: {tp.as_posix()}; {jp.as_posix()}.

FARA RENOTIFICARE
Raspunsul Capra 2026.10.30 16:56:53 este deja integrat si raportat separat. Factura/protocolul WÖHR, raspunsul DONAU, cererile MA37, R11 BERGER si invitatia actualizata sunt cunoscute, fara comunicari noi suplimentare identificate in aceasta cautare.
Nu sunt identificate acceptari/semnari noi, oferte sau confirmari de plata noi. Calendarul nu a fost modificat si nicio sedinta nu este declarata efectuata.

ACOPERIRE
{qcount} cautari/{len(P['pages'])} pagini complete; {len(metas)} ID-uri metadate unice. Control integral office primit/trimis in ambele conexiuni, cautari globale dupa adresa/firme/referinte. Perioada {P['period']}.
Registru {oldcount}->{len(R['comunicatii'])} comunicatii canonice. Un alias nou Capra comparat integral; nu este a doua comunicatie. {len(P['excluded_ids'])} ID-uri excluse motivat: patru ID-uri de teste tehnice EVA si patru mesaje de marketing fara legatura specifica proiectului.
Cele trei imagini mici au numai metadate pastrate, fara anexe documentare originale noi de descarcat. Textul integral si metadatele emailului original sunt pastrate in JSON/TXT; exportul API nu este MIME original.
{limits}
Sursa verificare: {proof.as_posix()}
Nu s-au trimis emailuri, semnat ori efectuat plati, modificat contracte sau calendar.
"""
save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(DAY+' '+name+'.txt',summary,'2026.10.30 '+name+'.txt')
partnernote=DAY+' | CERHA HEMPEL\nStatus scurt: '+s['status']+'\nUltimul raspuns: '+s['ultimul_raspuns']+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSurse: '+str(s['sursa_status'])+'\n'+limits
prepend(BASE/'Parteneri'/(DAY+' Log discutii - CERHA HEMPEL.txt'),partnernote,BASE/'Parteneri'/'2026.10.30 Log discutii - CERHA HEMPEL.txt')
prepend('folder map/README.md',summary+'\nRaport: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'baseline_unique_ids':oldcount,'final_unique_ids':len(R['comunicatii']),'new_unreported_email_ids':[e['id']],'known_not_renotified':['c61d9755-daf2-4e6d-aa49-3e8db7bd919f'],'export':row,'mirror_alias':R['aliasuri_email_EVA'][-1],'excluded':P['excluded_ids'],'dovezi_originale':P,'nota':'O singura comunicare noua Capra catre Kornhofer; nu este raspuns al vanzatorului, predare de planuri ori acceptare comerciala.'})
Path('folder map/2026.10.31 Fisiere actualizate verificare generala.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'report':report.as_posix(),'email_source':tp.as_posix(),'proof':proof.as_posix(),'count':len(R['comunicatii']),'new_unreported':1,'decision':'NOTIFY'},ensure_ascii=False))

