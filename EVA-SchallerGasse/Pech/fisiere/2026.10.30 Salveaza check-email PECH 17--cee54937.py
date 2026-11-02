from pathlib import Path
from datetime import datetime, timezone, timedelta
from email import policy
from email.parser import BytesParser
import json, hashlib, shutil, sqlite3, csv, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd(); b=r/'folder map'; now=datetime.now(timezone(timedelta(hours=2))); day=now.strftime('%Y.%m.%d'); tag=now.strftime('%H-%M-%S'); stamp=now.isoformat(timespec='seconds')
p=json.loads((b/'2026.10.30 Dovezi check-email PECH 17.json').read_text(encoding='utf-8'))
manifest=json.loads((b/'2026.10.30 Manifest Capra 17.json').read_text(encoding='utf-8'))
e=p['capra_primary']; m=p['capra_secondary']; draft=p['draft_readback']
assert day=='2026.10.30' and not p['errors'] and draft['status']=='pending'
assert all(s['args']['offset']+len(s['result']['items'])>=s['result']['total'] for s in p['searches'])
assert all(e[k]==m[k] for k in ['text','subject','from_address','to','cc','received_at','is_sent','thread_id'])
assert not e['truncated'] and not e['is_sent']
assert sorted((a['name'],a['size']) for a in e['attachments'])==sorted((a['name'],a['size']) for a in m['attachments'])
ids={x['id'] for s in p['searches'] for x in s['result']['items']}
assert len(ids)==66 and len(p['searches'])==25
for a in manifest:
 assert hashlib.sha256((r/a['path']).read_bytes()).hexdigest()==a['sha256'] and (r/a['path']).stat().st_size==a['size']
out=r/'08. Corespondenta/2026.10.30 Check-email PECH';out.mkdir(exist_ok=True)
capra=r/'08. Corespondenta/2026.10.29 Capra Baupolizei'
ctxt=capra/'2026.10.30 16-56-53 PRIMIT Capra c61d9755.txt';cjson=ctxt.with_suffix('.json')
assert json.loads(cjson.read_text(encoding='utf-8'))['email']['text']==e['text']
hist=b/(day+' Istoric check-email PECH '+tag);hist.mkdir()
changed=[]
def rel(f):return f.relative_to(r).as_posix()
def preserve(f):
 if f.exists():
  q=hist/f.relative_to(r);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q)
def save(f,t):
 preserve(f);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t,encoding='utf-8');changed.append(f)
def jsave(f,d):save(f,json.dumps(d,ensure_ascii=False,indent=2))
def local(t):return datetime.fromisoformat(t.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=2))).strftime('%Y.%m.%d %H:%M:%S') if t else 'indisponibil'
rp=r/p['baseline']['register_path']; reg=json.loads(rp.read_text(encoding='utf-8')); status=next(x for x in reg['statusuri'] if x['partener']=='Pech'); cs=next(x for x in reg['statusuri'] if x['partener']=='CERHA HEMPEL')
prior=json.loads((r/status['draft_amanare_2026_11_03']['sursa']).read_text(encoding='utf-8'))['draft']
assert all(prior[k]==draft[k] for k in ['id','status','body','subject','to','cc','attachments'])
oldcount=len(reg['comunicatii']); olddraft=copy.deepcopy(reg['drafturi']); general=copy.deepcopy(reg['acoperire']['verificare_incrementala'])
already=any(x.get('id')==e['id'] for x in reg['comunicatii'])
if not already:
 reg['comunicatii'].append({'data':day,'ora_utc':'14:56:53','partener':'CERHA HEMPEL','domeniu':'Recuperare documentatie autorizare','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':rel(ctxt),'json':rel(cjson),'atasamente':[a['path'] for a in manifest],'trunchiat':False,'data_preluarii':day,'deja_raportat_punctual':True,'sursa_raportarii':'08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.30 17-01 Jurnal verificare.txt'})
alias=out/(day+' Alias Capra cb1a4280.json');jsave(alias,{'data_lizibila':day,'statut':'PRIMIT - alias aceluiasi mesaj','canonical_id':e['id'],'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','email':m,'verificare':'Corp integral, thread_id, data, expeditor, destinatari, CC, subiect identice; nume/dimensiuni anexe identice. Octetii anexelor descarcati din conexiunea Primary.'})
if not any(x['alias_id']==m['id'] for x in reg.get('aliasuri_email_EVA',[])):
 reg.setdefault('aliasuri_email_EVA',[]).append({'alias_id':m['id'],'canonical_id':e['id'],'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','cale':rel(alias),'verificare':'thread_id, corp integral, expeditor, destinatari, CC, data, subiect; nume/dimensiuni anexe'})
cs.setdefault('istoric_status',[]).append({k:copy.deepcopy(cs.get(k)) for k in ['status','ultima_comunicare','ultimul_primit','ultimul_raspuns','urmatorul_pas','sursa_status']})
cs.update({'status':'2026.10.30: Capra confirma primirea cererii si va contacta Kornhofer; ofera retransmiterea documentelor cunoscute cu index. Planurile vizate nu sunt confirmate ca recuperate.','ultima_comunicare':day,'ultimul_primit':day,'subiect_ultimul_primit':e['subject'],'ultimul_raspuns':'2026.10.30 16:56:53 Romania: va contacta Kornhofer; poate retransmite Bestandsunterlagen, Energieausweis DG, Bauphysik cu index; Pristounig este indicat ca posibil detinator. Recomanda abordare amiabila inaintea unei analize juridice detaliate.','urmatorul_pas':'Urmarirea contactarii efective a vanzatorului si a raspunsului MA37; solicitarea pachetului pastrat de avocat cu index si verificarea separata a exemplarelor vizate. Nicio confirmare ca planurile vizate au fost predate.','sursa_status':[rel(ctxt),rel(cjson)],'data_actualizarii':day,'verificat':day,'mesaje':sum(x.get('partener')=='CERHA HEMPEL' for x in reg['comunicatii'])})
arp=r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.30 Registru atasamente.json'; ar=json.loads(arp.read_text(encoding='utf-8')); akeys={x['id'] for x in ar}
for a in manifest:
 if a['attachment_id'] not in akeys:
  ar.append({'id':a['attachment_id'],'email_id':e['id'],'data':day,'partener':'CERHA HEMPEL','nume_original':a['name_original'],'octeti':a['size'],'sha256':a['sha256'],'cale':a['path'],'stare':'Original descarcat integral; fragmente, dimensiune si SHA256 verificate. Retransmitere istorica, nu planuri vizate noi.','duplicat_al':a['identic_arhiva']})
proof=out/(day+' '+tag+' Dovezi check-email PECH.json');report=out/(day+' '+tag+' Raport check-email PECH.txt')
primary={x['email']:x.get('last_sync') for x in p['mailboxes_primary']['mailboxes']};secondary={x['email']:x.get('last_sync') for x in p['mailboxes_secondary']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Pech'],'mesaje_noi_PECH':0,'mesaje_noi_proiect_fata_de_13':1,'mesaje_integrate_registru':int(not already),'mesaje_deja_raportate_monitorizare_Capra':[e['id']],'atasamente_intrari':8,'query_count':25,'page_count':25,'metadate_unice':66,'perioada':p['period'],'paginare_completa':True,'sincronizare_office':primary['office@ac-wohnart.at'],'sincronizare_gmail':primary['covaciu.gnm@gmail.com'],'sincronizare_office_secundar':secondary['office@ac-wohnart.at'],'draft_amanare_status':'pending','decizie_notificare':'DONT_NOTIFY','motiv':'Fara noutati directe PECH; Capra este deja raportat separat in monitorizarea Baupolizei, acelasi ID si continut.','sursa':rel(proof)}
note=f'''{day} {now.strftime('%H:%M:%S')} UTC+02:00 | CHECK-EMAIL PECH
Status scurt: Fara raspunsuri, oferte, contrapropuneri, termene, programari, anexe sau nelivrari PECH noi fata de controlul 2026.10.30 13:03:33.
Ultimul raspuns PECH: 2026.10.27, DI Bernhard Ployer recomanda Roland Gasperl. Ultima trimitere: 2026.10.28, acces servieta; nu exista confirmare noua a primirii sau functionarii.
Draftul de multumire/amanare ebe46e54-bdee-407a-971f-1025f67f6482 ramane pending/NETRIMIS, identic versiunii arhivate. Data 2026.11.03 este propusa, fara confirmarea PECH.
Noutate conexa proiectului, deja preluata de monitorizarea Capra: raspuns PRIMIT 2026.10.30 16:56:53 de la Bogdan.Capra@cerhahempel.com catre office@ac-wohnart.at, CC gol, ID {e['id']}; alias {m['id']}. Confirma primirea cererii si anunta ca va contacta Kornhofer. Ofera retransmiterea documentelor cunoscute (Bestandsunterlagen, Energieausweis DG, Bauphysik) cu index; poate contacta Klaus Pristounig, posibil detinator. Recomanda mai intai demersuri amiabile. Nu confirma contactarea deja efectuata, recuperarea planurilor vizate, un nou raspuns MA37 sau acceptarea argumentatiei juridice.
Anexe: 8 intrari, 5 continuturi distincte; EML original al corespondentei 2026.03.17, PDF proces-verbal 2026.03.17 si imagini de semnatura. EML citit integral, contine corespondenta istorica si acelasi PDF. SHA256 PDF 95a38ffe17d43718584749fa9854e4442e00b9a76f6ad11d87242fed0405342d, identic arhivei. Nu sunt planuri vizate noi. Toate originalele descarcate integral si verificate pe fragmente; descarcarea HTTP a intors 403, alternativa oficiala EVA base64 a reusit.
Urmatorul pas: urmarirea raspunsului PECH si confirmarii datei/orei dupa eventuala trimitere de catre utilizator; urmarirea contactarii vanzatorului, a raspunsului MA37 si a pachetului cu index oferit de Capra. Oferta de retransmitere nu inseamna pachet deja predat.
Acoperire: 25 cautari/25 pagini complete; 2026.10.29-2026.10.30, suprapunere o zi. 66 ID-uri unice: 44 Gmail din alte subiecte, 22 office (11 comunicatii oglindite). Dintre office, 8 comunicatii deja cunoscute, 2 mesaje tehnice de reconectare fara relevanta PECH si 1 raspuns Capra cu 1 alias. Nicio pagina restanta. Registrul general si verificarea generala sunt pastrate; un singur mesaj canonic Capra, fara dublarea aliasului.
Sincronizare afisata UTC+02:00: office Primary {local(primary['office@ac-wohnart.at'])}; Gmail {local(primary['covaciu.gnm@gmail.com'])}; office secundar {local(secondary['office@ac-wohnart.at'])}. Indicatorii nu garanteaza exhaustivitatea; mesaje inca neindexate pot lipsi. Casutele shared/team necautabile nu sunt incluse.
Surse: {rel(proof)}; {rel(ctxt)}; 08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.30 17-01 Jurnal verificare.txt. Identitatea raspunsului cu cel raportat separat in sarcina Monitorizeaza raspunsul Baupolizei a fost verificata; nu repetam notificarea.
Nu s-au trimis emailuri, modificat ciorne/calendar/documente comerciale, semnat contracte sau efectuat plati. Decizie: DONT_NOTIFY.
'''
status['verificare_punctuala_PECH']={'checked_at_iso':stamp,'mesaje_noi':0,'draft_amanare_status':'pending','sursa':rel(proof)}
status['documente_autorizare_ultima_noutate']={'data':day,'partener_sursa':'CERHA HEMPEL','id_eva_mail':e['id'],'status':'Kornhofer va fi contactat; pachet cunoscut cu index oferit, planuri vizate nerecuperate','sursa':rel(ctxt)}
reg['acoperire']['verificare_punctuala_PECH']=entry;reg.setdefault('verificari_parteneri',[]).append(entry);reg['data_actualizarii']=day
assert reg['drafturi']==olddraft and reg['acoperire']['verificare_incrementala']==general
jsave(rp,reg);jsave(arp,ar);save(report,note)
jsave(proof,{'verificare':entry,'dovezi':p,'manifest_atasamente':manifest,'alias_body_equal':True,'draft_unchanged':True,'general_baseline_preserved':general,'register_count':len(reg['comunicatii']),'sursa_deduplicare':{'thread_id':'01a187f1-eb13-7372-95db-4fc7cea6eec5','titlu':'Monitorizează răspunsul Baupolizei','jurnal':'08. Corespondenta/2026.10.29 Capra Baupolizei/2026.10.30 17-01 Jurnal verificare.txt','observatie':'Comentariile sarcinii confirma raportarea aceluiasi raspuns Capra; nu se dubleaza notificarea.'}})
jsave(r/'08. Corespondenta/2026.10.30 Capra recuperare documente/2026.10.30 Manifest originale Capra.json',{'data':day,'email_id':e['id'],'statut':'PRIMIT','email_sursa':rel(cjson),'atasamente':manifest,'nota':'Copii suplimentare verificate; originalele aceleiasi comunicari exista si in arhiva Capra. Nu reprezinta mesaje sau planuri noi suplimentare.'})
for f in [r/(day+' Status proiect.txt'),r/(day+' Log progres proiect.txt'),r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'/(day+' Log discutii - Pech.txt')]:
 old=f.read_text(encoding='utf-8-sig') if f.exists() else '';save(f,note+'\nISTORIC PASTRAT\n\n'+old)
f=b/'README.md';save(f,f'{day} {now.strftime("%H:%M:%S")} | PECH verificat: fara noutati directe, draft amanare NETRIMIS. Raspunsul Capra 16:56:53 integrat o singura data in registre; deja raportat separat, fara renotificare. Raport: ../{rel(report)}\n\n'+f.read_text(encoding='utf-8-sig'))
changed += [r/a['path'] for a in manifest]
inv=b/'inventar.json';cp=b/'inventar.csv';dp=b/'cautare.sqlite'
# Citire proaspata la indexare, pentru a pastra actualizarile independente din celelalte verificari.
rows=json.loads(inv.read_text(encoding='utf-8'));indexed={x['cale']:x for x in rows};bysha={x['sha256']:x for x in rows}
for f in [inv,cp,dp]:preserve(f)
db=sqlite3.connect(dp,timeout=30)
for f in changed:
 if b in f.parents:continue
 data=f.read_bytes();sha=hashlib.sha256(data).hexdigest();st=f.stat();path=rel(f);dup=bysha.get(sha)
 if f.suffix.lower() in ['.txt','.json']:txt=data.decode('utf-8-sig')
 elif f.suffix.lower()=='.eml':
  em=BytesParser(policy=policy.default).parsebytes(data);body=em.get_body(preferencelist=('plain',));txt=str(em.items())+'\n'+(body.get_content() if body else '')
 elif dup and dup.get('text_cache') and (r/dup['text_cache']).exists():txt=(r/dup['text_cache']).read_text(encoding='utf-8-sig')
 else:txt='Original binar pastrat; '+f.name
 cache=b/'texte'/f'{sha}.txt';cache.write_text(txt,encoding='utf-8');row=indexed.get(path,{})
 row.update({'cale':path,'folder':f.parent.relative_to(r).as_posix(),'extensie':f.suffix.lower(),'octeti':len(data),'modificat':datetime.fromtimestamp(st.st_mtime).isoformat(),'modificat_ns':st.st_mtime_ns,'sha256':sha,'duplicat_al':dup['cale'] if dup and dup['cale']!=path else '', 'ce_reprezinta':'Verificare PECH si corelare raspuns Capra pentru recuperarea documentelor','baza_descrierii':'EVA integral; SHA256; verificare '+day,'extras_continut':' '.join(txt.split())[:1000],'stare_citire':'text extras' if txt else 'original binar pastrat','text_cache':cache.relative_to(r).as_posix(),'detalii':{},'rezumat_verificat':'Fara noutati directe PECH. Raspuns Capra deja raportat separat; anexe istorice, fara planuri vizate noi.','ocr_cache':''})
 indexed[path]=row;db.execute('DELETE FROM documente WHERE cale=?',(path,));db.execute('INSERT INTO documente VALUES (?,?,?,?)',(path,row['ce_reprezinta'],txt,sha))
db.commit();db.close();rows=sorted(indexed.values(),key=lambda x:x['cale']);inv.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with cp.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps({'report':rel(report),'decision':'DONT_NOTIFY','new_direct_pech':0,'capra_deduplicated':e['id'],'register_before':oldcount,'register_after':len(reg['comunicatii']),'attachment_register':len(ar),'files_indexed':len([f for f in changed if b not in f.parents])},ensure_ascii=False))
