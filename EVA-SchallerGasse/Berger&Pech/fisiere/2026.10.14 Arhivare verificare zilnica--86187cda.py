from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
from email.message import EmailMessage
from email import policy,parser
import json,hashlib,shutil,re
R=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)').resolve()
V=Path(__file__).parent
A=(R/'08. Corespondenta/2026.10.14 Verificare zilnica').resolve()
assert A.is_relative_to(R)
A.mkdir(exist_ok=True)
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def unpack(x):return x.get('structuredContent') or json.loads(next(c['text'] for c in x['content'] if c['type']=='text'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(t):return re.sub(r'\s+',' ',re.sub(r'[<>:"/\\|?*\r\n]',' ',t)).strip()
proof=json.loads((V/'2026.10.14 Dovezi verificare Eva-Mail final.json').read_text(encoding='utf-8'))
docs=json.loads((V/'2026.10.14 Originale verificate si texte.json').read_text(encoding='utf-8'))
messages=[unpack(x['result']) for x in proof['full_new_emails']]
inventory=json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))
oldhash={}
for x in inventory:oldhash.setdefault(x['sha256'],x['cale'])
before=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json'
registry=json.loads(before.read_text(encoding='utf-8-sig'))
attbefore=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru atasamente.json'
attregistry=json.loads(attbefore.read_text(encoding='utf-8-sig'))
for p in [before,attbefore,R/'folder map/README.md']:
 shutil.copy2(p,A/('2026.10.14 Istoric '+p.name))
docrecords=[];newfiles=0
for d in docs:
 source=Path(d['local_staging_path']);assert sha(source)==d['sha256']
 if d['sha256'] in oldhash:
  target=R/oldhash[d['sha256']];assert sha(target)==d['sha256'];status='original descarcat integral; identic SHA-256 cu fisier existent, reutilizat'
 else:
  target=A/source.name;shutil.copy2(source,target);assert sha(target)==d['sha256'];oldhash[d['sha256']]=target.relative_to(R).as_posix();newfiles+=1;status='original integral salvat si verificat SHA-256'
 entry={'id':d['id'],'email_id':d['email_id'],'data':'2026.10.13','nume_original':d['name'],'octeti':d['size'],'sha256':d['sha256'],'cale':target.relative_to(R).as_posix(),'stare':status,'pagini':d['pages']}
 if 'claimed_balance_eur' in d:entry.update({k:d[k] for k in ['claimed_balance_eur','installation','payment_reference']})
 docrecords.append(entry)
 known=next((x for x in attregistry if x['id']==d['id']),None)
 if not known:attregistry.append(entry)
docmap={x['id']:x for x in docrecords}
PARTNERS={'94a8a995-412a-4fb6-a27d-c43b2ad0bf04':'Pech','d14ab99d-d50e-4e90-8365-16d989be5517':'Markus Berger','794a7efa-b90a-41dc-a8d3-071e7c3ac323':'Markus Berger','83cedef0-8a28-42f1-a055-7ebeb701b348':'Markus Berger','67559716-1ef2-4c7a-85d0-f8d1eaa03158':'CERHA HEMPEL','5f3fc243-11dc-4a13-8cff-f62bf1ea15df':'CERHA HEMPEL','6cd54b72-287e-4259-af32-a29c6ec3c5a2':'ARTUS','d2bb3a63-79fd-4d31-b497-2a13f570fab9':'CERHA HEMPEL','0fed52e8-a06b-47c5-ba04-84e5eb934d9f':'STURM ENERGIE','9561ffd7-c7c1-41a2-bee2-8fcc0ef109b1':'CERHA HEMPEL','eef758af-541f-4251-ae3b-5b1de20dc246':'CERHA HEMPEL'}
newentries=[];messagefiles={};images=[]
for m,wrapped in zip(messages,proof['full_new_emails']):
 dt=datetime.fromisoformat(m['received_at'].replace('Z','+00:00'));local=dt.astimezone(ZoneInfo('Europe/Bucharest'));date=local.strftime('%Y.%m.%d');sense='TRIMIS' if m['is_sent'] else 'PRIMIT';partner=PARTNERS[m['id']]
 prefix=date+' '+local.strftime('%H-%M')+' '+sense+' '+partner+' '+m['id'][:8]
 native=A/(prefix+' EVA original.json');write(native,wrapped['result'])
 meta={'data':date,'data_verificarii':'2026.10.14','ora_Romania':local.strftime('%H:%M:%S'),'received_at':m['received_at'],'subiect':m['subject'],'expeditor':m['from_address'],'destinatari':m.get('to',[]),'cc':m.get('cc',[]),'id_Eva_Mail':m['id'],'statut':sense,'account_email':m.get('account_email'),'trunchiat':m.get('truncated',False),'text_original_API':m['text'],'atasamente_documentare':[docmap[x['id']] for x in m.get('attachments',[]) if x.get('id') in docmap],'atasamente_toate_metadate':m.get('attachments',[]),'MIME_integral_furnizat_de_API':False}
 write(A/(prefix+'.json'),meta)
 text='2026.10.14 | Verificare; mesaj '+date+' '+local.strftime('%H:%M:%S')+' România\nStatut: '+sense+'\nSubiect: '+m['subject']+'\nExpeditor: '+m['from_address']+'\nDestinatari: '+', '.join(m.get('to',[]))+'\nCC: '+', '.join(m.get('cc',[]))+'\nID Eva-Mail: '+m['id']+'\nReceived_at original: '+m['received_at']+'\n\n'+m['text']
 (A/(prefix+'.txt')).write_text(text,encoding='utf-8');messagefiles[m['id']]=(A/(prefix+'.txt')).relative_to(R).as_posix()
 em=EmailMessage(policy=policy.SMTP);em['From']=m['from_address'];em['To']=', '.join(m.get('to',[]));em['Subject']=re.sub(r'[\r\n]+',' ',m['subject']);em['Date']=dt;em['X-EVA-Mail-ID']=m['id'];em['X-Archive-Readable-Date']=date;em['X-Archive-Status']=sense;em['X-Archive-Export-Type']='API reconstruction; not original MIME'
 if m.get('cc'):em['Cc']=', '.join(m['cc'])
 em.set_content(m['text'])
 for x in meta['atasamente_documentare']:em.add_attachment((R/x['cale']).read_bytes(),maintype='application',subtype='pdf',filename=clean(x['nume_original']))
 ep=A/(prefix+' export API.eml');ep.write_bytes(em.as_bytes());parsed=parser.BytesParser(policy=policy.default).parsebytes(ep.read_bytes())
 assert len(list(parsed.iter_attachments()))==len(meta['atasamente_documentare'])
 for x in m.get('attachments',[]):
  if x.get('id') in docmap:continue
  entry={'id':x.get('id'),'email_id':m['id'],'data':date,'partener':partner,'nume_original':x['name'],'octeti':x.get('size'),'stare':'numai metadate; imagine mica/inline, posibil semnatura; nu este document de oferta/plata; original nedescarcat','cale':str((A/(prefix+'.json')).relative_to(R))}
  images.append(entry)
  if not any(z['id']==entry['id'] for z in attregistry):attregistry.append(entry)
 entry={'data':date,'ora_utc':dt.strftime('%H:%M:%S'),'partener':partner,'domeniu':{'STURM ENERGIE':'Utilitati','ARTUS':'Contabilitate','CERHA HEMPEL':'Juridic'}.get(partner,'Structura / proiectare'),'sens':sense,'subiect':m['subject'],'expeditor':m['from_address'],'destinatari':'; '.join(m.get('to',[])),'cc':'; '.join(m.get('cc',[])),'id':m['id'],'cale':messagefiles[m['id']],'atasamente':len(m.get('attachments',[])),'trunchiat':m.get('truncated',False)}
 if not any(x['id']==m['id'] for x in registry['comunicatii']):registry['comunicatii'].append(entry);newentries.append(entry)
sturm=[x for x in docs if 'claimed_balance_eur' in x];total=sum(Decimal(x['claimed_balance_eur'].replace('.','').replace(',','.')) for x in sturm);assert total==Decimal('2662.60') and len(sturm)==14
sturm_lines=['2026.10.14 | STURM - 14 somații originale retrimise în emailul 2026.10.13','Sume pretinse de creditor; nu sunt datorii noi adăugate sau solduri bancare confirmate. Termen email 2026.10.19; PDF-urile datate 2026.08.26 au termenul istoric 2026.09.07.','Instalatie | Nume original PDF | Suma pretinsa EUR | Referinta plata | Sursa originalului']
for x in sorted(sturm,key=lambda z:z['installation']):sturm_lines.append(' | '.join([x['installation'],x['name'],x['claimed_balance_eur'],x['payment_reference'],docmap[x['id']]['cale']]))
sturm_lines+=['TOTAL pretins inclusiv cele 14 taxe de somație a câte 7 EUR: 2.662,60 EUR.','Această verificare nu confirmă un debit/încasare și nu solicită o plată dublă; se reconciliază plățile anterioare înainte de orice nouă plată.']
(A/'2026.10.14 STURM tabel sume si referinte.txt').write_text('\n'.join(sturm_lines)+'\n',encoding='utf-8')
mailboxes=unpack(proof['mailboxes'])['mailboxes'];sync={x['email']:x['last_sync'] for x in mailboxes}
searches=proof['searches'];assert all(x['result'] is not None and not x.get('error') and unpack(x['result'])['total']<=len(unpack(x['result'])['items']) for x in searches)
coverage={'data':'2026.10.14','perioada':'2026.10.12–14; suprapunere de o zi după verificarea zilnică 2026.10.13','cautari_complete':len(searches)+2,'paginare_completa':True,'mesaje_noi_ID':len(newentries),'mesaje_primite_ID':sum(not x['is_sent'] for x in messages),'mesaje_trimise_ID':sum(x['is_sent'] for x in messages),'PDF_originale_integrale_verificate':len(docrecords),'PDF_continuturi_noi_pe_disc':newfiles,'imagini_inline_numai_metadate':len(images),'oferta_noua_identificata':False,'sincronizari_originale':sync,'limite':'Office 2026.10.14 08:00:13 România; Gmail 2026.10.14 04:04:01 România; cosmin@ig.ro numai 2026.10.10 02:30:10 România. Căsuțele shared/team nesearchable nu sunt acoperite. API nu furnizează MIME integral; EML este reconstrucție API cu originale PDF reale. Nu este reconciliare bancară la zi. Imaginile mici/inline au numai metadate.'}
registry['data_actualizarii']='2026.10.14';registry['acoperire']['verificare_incrementala']=coverage;registry['acoperire']['mesaje_salvate']=len(registry['comunicatii'])
registry['acoperire']['atasamente_identificate']+=len(docrecords)+len(images)
registry['acoperire']['atasamente_documentare']+=len(docrecords)
registry['acoperire']['atasamente_documentare_salvate']+=len(docrecords)
registry['acoperire']['atasamente_salvate']+=len(docrecords)
registry['acoperire']['imagini_mici_numai_metadate']+=len(images)
registry['acoperire']['registru_atasamente_randuri']=len(attregistry)
registry['actualizari_punctuale'].append({'data':'2026.10.14','tip':'Verificare zilnica completa; 11 ID noi fata de registrul zilnic; nu 11 datorii/oferte','sursa':str((A/'2026.10.14 Dovezi verificare Eva-Mail.json').relative_to(R)),'mesaje_noi':len(newentries),'originale_PDF_verificate':34,'continuturi_PDF_noi':newfiles,'mesaje_trimise_de_agent':0})
drafts=[unpack(x) for x in proof['draft_readbacks']]
sent_map={'f8c09c6b-f102-4998-877d-62c269ac5cdd':'d14ab99d-d50e-4e90-8365-16d989be5517','8e954def-ac5f-4782-b5c7-b25c64572bb9':'94a8a995-412a-4fb6-a27d-c43b2ad0bf04'}
for d in drafts:
 entry=next(x for x in registry['drafturi'] if x['id']==d['id']);entry['statut']='EVA '+d['status']+' verificat 2026.10.14';entry['updated_at']=d['updated_at'];entry['sursa_statut']='08. Corespondenta/2026.10.14 Verificare zilnica/2026.10.14 Statut ciorne EVA original.json'
 if d['id'] in sent_map:entry['dovada_trimiterii_ulterioare']=sent_map[d['id']];entry['livrare']='trimitere inregistrata; fara confirmare de primire/acceptare'
write(R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.14 Registru comunicatii.json',registry)
write(R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.14 Registru atasamente.json',attregistry)
proof['rezultat']=coverage;proof['message_files']=messagefiles;proof['originale_PDF']=docrecords;proof['comparatie_arhiva']={'previous_registered_messages':802,'new_unique_IDs':len(newentries),'now_registered_messages':len(registry['comunicatii']),'economic_duplicates':'CERHA în trei căsuțe este aceeași somație, nu trei datorii; BERGER trimis inițial/retrimis are același contract; anexele CERHA și contractele R09 au hash identic celor existente'}
write(A/'2026.10.14 Dovezi verificare Eva-Mail.json',proof)
write(A/'2026.10.14 Registru anexe originale.json',docrecords)
shutil.copy2(V/'2026.10.14 Statut ciorne EVA original.json',A/'2026.10.14 Statut ciorne EVA original.json')
for name in ['2026.10.14 ARTUS somatie.png','2026.10.14 STURM original.png']:shutil.copy2(V/name,A/name)
notices={
 'Markus Berger':'Propunerea R09 45.000 EUR net / 54.000 EUR cu TVA trimisă inițial 2026.10.13 20:26 România, returnată 20:26 pentru IP expeditor blocat Spamhaus / 550 5.7.1. Retrimisă 21:40 România, ID d14ab99d-d50e-4e90-8365-16d989be5517, fără nouă nelivrare identificată până la ultima sincronizare; nu există confirmare de primire ori acceptare. Următorul pas: confirmarea primirii și calendarul/agreementul; ciorna Gmail rămâne pending. Surse: '+messagefiles['d14ab99d-d50e-4e90-8365-16d989be5517']+'; '+messagefiles['794a7efa-b90a-41dc-a8d3-071e7c3ac323'],
 'Pech':'Propunerea R09 69.300 EUR net / 83.160 EUR cu TVA trimisă 2026.10.13 21:40 România, ID 94a8a995-412a-4fb6-a27d-c43b2ad0bf04, CC ployer@zt-pech.at; contractul și oferta originale PDF verificate identice celor arhivate. Nu există răspuns/acceptare ori ofertă pentru PI/ZT/Bauwerksbuch complet și costuri încă neconfirmate. Următorul pas: răspunsul PECH, confirmarea funcțiilor/prețurilor/calendarelor înainte de semnare. Ciorna Gmail rămâne pending. Sursa: '+messagefiles['94a8a995-412a-4fb6-a27d-c43b2ad0bf04'],
 'CERHA HEMPEL':'Somația pentru factura 26/30363 de 2.640,22 EUR, termen 2026.10.16, a fost deja analizată separat în 2026.10.13; cele trei copii de căsuță sunt aceeași cerere. Noutatea: răspunsul din 2026.10.13 20:15 România anunță plata integrală și cere confirmarea încasării, dar este returnat pentru IP expeditor blocat Spamhaus / 550 5.7.1. Declarația din email nu este extras bancar sau confirmare de încasare; nu s-a identificat răspuns ulterior al creditorului. Următorul pas: verificarea dovezii bancare și retrimiterea/confirmarea comunicării prin canal funcțional, fără o nouă plată automată. Surse: '+messagefiles['5f3fc243-11dc-4a13-8cff-f62bf1ea15df']+'; '+messagefiles['67559716-1ef2-4c7a-85d0-f8d1eaa03158'],
 'ARTUS':'Zahlungserinnerung primită 2026.10.13: factura 1264971, 144,00 EUR pretinși deschiși, termen email 2026.10.20. PDF factura: 120 net + 24 TVA; PDF somație: 144 deschis, dobândă/taxe 0, plăți luate în calcul numai până 2026.10.09. PDF factura este datat 2026.09.15, emailul indică 2026.09.16; somația are UID client ATU57571979, factura ATU83086125, de clarificat administrativ. Următorul pas: reconcilierea plăților și răspunsul privind soldul; nu se consideră o datorie nouă suplimentară. Sursa: '+messagefiles['6cd54b72-287e-4259-af32-a29c6ec3c5a2'],
 'STURM ENERGIE':'Email primit 2026.10.13, Ticket365759 / client42017328: somațiile poștale au fost returnate cu mențiunea necunoscut; 14 PDF retrimise, solduri pretinse însumate 2.662,60 EUR incluzând 98 EUR taxe somație. Termen nou email 2026.10.19; PDF-urile sunt datate 2026.08.26 cu termen istoric 2026.09.07. Scrisorile anunță posibila cesiune a părții de rețea către operator, nu cesiune efectuată confirmată. Următorul pas: reconcilierea fiecărei instalații și dovezilor de plată, confirmarea adresei de corespondență; sumele nu sunt adăugate din nou registrului de datorii și nu sunt debit/încasare confirmate. Sursa: '+messagefiles['0fed52e8-a06b-47c5-ba04-84e5eb934d9f']+'; 08. Corespondenta/2026.10.14 Verificare zilnica/2026.10.14 STURM tabel sume si referinte.txt'
}
partners=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
for partner,note in notices.items():
 matches=sorted(partners.glob('* Log discutii - '+partner+'.txt'));prior=matches[-1].read_text(encoding='utf-8-sig') if matches else ''
 (partners/('2026.10.14 Log discutii - '+partner+'.txt')).write_text('2026.10.14 | Verificare zilnică\nStatus scurt / ultimul răspuns / următorul pas / surse: '+note+'\n\nISTORIC PĂSTRAT\n\n'+prior,encoding='utf-8')
report='''2026.10.14 | Noutăți Schallergasse 35 față de verificarea zilnică 2026.10.13

BERGER și PECH: propunerile R09 apar efectiv TRIMISE de pe office@ac-wohnart.at în 2026.10.13 la 21:40 România, cu contractul și oferta originale proprii. BERGER 45.000 EUR net, PECH 69.300 EUR net. Nu sunt contracte acceptate; nu există răspunsuri/ofertă nouă identificate. Cele două copii Gmail rămân pending / NETRIMISE; cele două ciorne office sunt acum sent.

Livrare BERGER: prima trimitere 20:26 a eșuat, 550 5.7.1 / IP expeditor blocat Spamhaus. Retrimiterea 21:40 nu are o nouă eroare identificată în interval, dar primirea nu este confirmată.

CERHA HEMPEL: răspunsul 20:15 care anunță plata facturii 26/30363, 2.640,22 EUR, a eșuat din aceeași cauză tehnică. Nu există confirmare de încasare; anunțul nu dovedește debitul bancar. Somația deja analizată 2026.10.13 menține termenul 2026.10.16. Se verifică dovada bancară și comunicarea, fără o plată dublă automată.

STURM: 14 somații retrimise după retur poștal «necunoscut»; total pretins 2.662,60 EUR, incluzând 98 EUR taxe, termen email 2026.10.19. Cele 14 instalații și referințe sunt în tabelul dedicat. Sume pretinse de creditor, de reconciliat cu plățile; nu 14 datorii noi adăugate. PDF-uri istorice 2026.08.26, termenul istoric 2026.09.07 nu înlocuiește termenul actual din email.

ARTUS: 144 EUR pentru factura1264971, termen2026.10.20. 120 EUR net+24 TVA; fără dobândă/taxă în somație. PDF factura2026.09.15 vs email2026.09.16; UID client diferit în somație, de clarificat. Încasarea nu este confirmată de această verificare.

Descărcări: 34 PDF originale verificate byte/SHA-256, din care 16 conținuturi noi salvate (14 STURM+factură și somație ARTUS), restul18 identice fișierelor existente și reutilizate. 11 ID-uri de email înregistrate suplimentar; copiile CERHA și retrimiterea BERGER nu dublează datorii/oferte. PDF-urile contractelor trimise sunt identice versiunilor R09 locale. Imaginile mici/inline au numai metadate.

Acoperire: 2026.10.12–14, suprapunere o zi; 68 căutări complete fără pagini restante. Office sincronizat2026.10.14 08:00:13 România, Gmail04:04:01; unele alte căsuțe sunt întârziate, shared/team nesearchable neacoperite. Nu s-au trimis mesaje, semnat contracte sau efectuat plăți de către această verificare.

Surse: toate exporturile TXT/JSON și EML reconstruite din API în 08. Corespondenta/2026.10.14 Verificare zilnica, cu originale PDF reale; 2026.10.14 Dovezi verificare Eva-Mail.json, 2026.10.14 Registru anexe originale.json și 2026.10.14 STURM tabel sume si referinte.txt. EML nu este MIME original integral furnizat de server.
'''
assert len(searches)+2==68
(A/'2026.10.14 Raport noutati Schallergasse 35.txt').write_text(report,encoding='utf-8')
for stem in ['Status proiect','Log progres proiect']:
 old=R/('2026.10.13 '+stem+'.txt');prior=old.read_text(encoding='utf-8-sig') if old.exists() else '';(R/('2026.10.14 '+stem+'.txt')).write_text(report+'\nISTORIC PĂSTRAT\n\n'+prior,encoding='utf-8')
readme=R/'folder map/README.md';old=readme.read_text(encoding='utf-8-sig');readme.write_text('# 2026.10.14 — Verificare zilnică: comunicări trimise, nelivrări și somații\n\n'+report+'\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
write(A/'2026.10.14 Rezultat arhivare.json',{'date':'2026.10.14','new_email_IDs':len(newentries),'PDFs_downloaded_verified':34,'PDF_new_contents':newfiles,'registered_messages':len(registry['comunicatii']),'searches_complete':len(searches)+2,'pending_gmail_drafts':2,'sent_office_drafts':2,'sent_by_agent':0,'signed':0,'payments_by_agent':0,'sources':messagefiles})
print(json.dumps({'new_IDs':len(newentries),'PDF_originals':34,'new_PDF_contents':newfiles,'searches_complete':len(searches)+2,'new_registry':str(R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.14 Registru comunicatii.json')},ensure_ascii=False))
