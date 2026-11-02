from pathlib import Path
from email.message import EmailMessage
from email.policy import SMTP
import json,hashlib,re
R=Path.cwd();I=R/'00.Proiect/09. Vertraege/2026.10.13 PECH R09 - intern';P=R/'00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=json.loads((I/'2026.10.13 EVA PECH R09 readback original.json').read_text(encoding='utf-8'))
d=raw.get('structuredContent') or json.loads(next(x['text'] for x in raw['content'] if x['type']=='text'))
assert d['status']=='pending' and d['id']=='8e954def-ac5f-4782-b5c7-b25c64572bb9'
assert d['to']==['sekretariat@zt-pech.at'] and d['cc']==['ployer@zt-pech.at']
assert d['account_email']=='office@ac-wohnart.at'
body=(I/'2026.10.13 Email PECH R09 body fara semnatura.txt').read_text(encoding='utf-8').strip()
assert re.sub(r'\s+',' ',d['body']).startswith(re.sub(r'\s+',' ',body))
frozen=json.loads((I/'2026.10.13 Fisiere inghetate Berger si Pech R08.json').read_text(encoding='utf-8'))
assert all(sha(R/p)==h for p,h in frozen.items())
expected=[P/'2026.10.13 Werkvertrag PECH R09.pdf',P/'2026.10.13 Anlage 5 Originalangebot PECH 2026.09.17.pdf']
assert sorted(x['filename'] for x in d['attachments'])==sorted(x.name for x in expected)
records=[]
for p in expected:
 att=next(x for x in d['attachments'] if x['filename']==p.name)
 assert att['size']==p.stat().st_size
 records.append({'filename':p.name,'local_path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size,'document_id':att['id']})
proof=json.loads((I/'2026.10.13 Verificare bytes PDF in EVA.json').read_text(encoding='utf-8'))
assert proof['sha256']==records[0]['sha256'] and proof['status']=='PASS'
name='2026.10.13 Email PECH R09 NETRIMIS'
meta={'data':'2026.10.13','subiect':d['subject'],'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'bcc':d['bcc'],'id_Eva_Mail':d['id'],'statut':'DRAFT EVA pending / NETRIMIS','created_at':d['created_at'],'updated_at':d['updated_at'],'body_original':d['body'],'attachments':records,'original_EVA':str((I/'2026.10.13 EVA PECH R09 readback original.json').relative_to(R)),'sent':False}
write(P/(name+'.json'),meta)
(P/(name+'.txt')).write_text('2026.10.13 | DRAFT EVA pending / NETRIMIS\nSubiect: '+d['subject']+'\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nID Eva-Mail: '+d['id']+'\nCreated_at: '+d['created_at']+'\nUpdated_at: '+d['updated_at']+'\n\n'+d['body']+'\n',encoding='utf-8')
em=EmailMessage(policy=SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Cc']=', '.join(d['cc']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-EVA-Draft-ID']=d['id'];em['X-Archive-Readable-Date']='2026.10.13';em.set_content(d['body'])
for p in expected:em.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=p.name)
(P/(name+'.eml')).write_bytes(em.as_bytes())
from email import policy,parser
check=parser.BytesParser(policy=policy.default).parsebytes((P/(name+'.eml')).read_bytes())
assert {x.get_filename():hashlib.sha256(x.get_payload(decode=True)).hexdigest() for x in check.iter_attachments()}=={x['filename']:x['sha256'] for x in records}
old=json.loads((R/'00.Proiect/09. Vertraege/2026.10.13 Contracte R08 - intern/2026.10.13 Werkvertrag PECH R08.json').read_text(encoding='utf-8-sig'))
new=json.loads((I/'2026.10.13 Werkvertrag PECH R09.json').read_text(encoding='utf-8'))
diff=[]
for category in ['sections','annexes']:
 for o,n in zip(old[category],new[category]):
  if o!=n:diff.append({'category':category,'number':n['number'],'before':o,'after':n})
assert old['annexes'][3]['tables'][0]==new['annexes'][3]['tables'][0]
assert old['annexes'][3]['tables'][4]==new['annexes'][3]['tables'][4]
assert all(row[-2:]==['',''] for row in new['annexes'][3]['tables'][6]['rows'])
write(I/'2026.10.13 Registru PECH R09 final.json',{'date':'2026.10.13','source_sha256':sha(I/'2026.10.13 Werkvertrag PECH R09.json'),'pdf_sha256':sha(expected[0]),'original_positions_unchanged':True,'regie_unchanged':True,'base_net_eur':'69300.00','vat_eur':'13860.00','base_gross_eur':'83160.00','full_functions_required':True,'full_function_prices_confirmed':False,'blank_pending_price_fields':True,'calendar':'Working E1-E7 allocation; joint calendar to confirm before signature','status':'proposal; unsent; unsigned; no payment','draft_id':d['id'],'attachments':records,'byte_verification':proof,'original_r08_and_berger_unchanged':frozen,'changes_from_R08':diff,'email_files':{str((P/(name+x)).relative_to(R)):sha(P/(name+x)) for x in ['.txt','.json','.eml']}})
registry=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json'
j=json.loads(registry.read_text(encoding='utf-8-sig'));berger=next(x for x in j['drafturi'] if x['id']=='5a66f053-9d6b-45e2-880b-baecf778b46f').copy();count=len(j['comunicatii']);draftcount=len(j['drafturi'])
row=next(x for x in j['drafturi'] if x['id']==d['id']);row.update({'data':'2026.10.13','statut':'DRAFT EVA pending / NETRIMIS; PECH R09','cale':str((P/(name+'.txt')).relative_to(R)),'original_EVA':meta['original_EVA'],'EML':str((P/(name+'.eml')).relative_to(R)),'atasamente':records,'actualizare':'PECH R09: sase pozitii 69.300 EUR net pastrate; PI/ZT/Bauwerksbuch complete cerute, bold, acoperire neconfirmata, fara sume; calendar E1-E7 varianta de lucru de agreat; BERGER neschimbat.'})
j['actualizari_punctuale'].append({'data':'2026.10.13','tip':'PECH R09 contract + email draft','sursa':str((I/'2026.10.13 Registru PECH R09 final.json').relative_to(R)),'draft_id':d['id'],'drafts_updated':1,'drafts_created':0,'sent':0,'functions_required_pending_costs':True,'berger_unchanged':True})
assert len(j['comunicatii'])==count and len(j['drafturi'])==draftcount and next(x for x in j['drafturi'] if x['id']==berger['id'])==berger
write(registry,j)
notice='''2026.10.13 — PECH R09: propunere contract și email actualizate, NETRIMISE.
Status scurt: șase poziții originale păstrate, 69.300 EUR net / 83.160 EUR brut; regie originală păstrată. PI complet, certificarea integrală ZT și Bauwerksbuch întreg existent + intervenții noi, Erstprüfung și înregistrare rămân cerințe explicite, bold, cu asumarea și acoperirea onorariului neconfirmate și fără sume atribuite. Contribuțiile tehnice proprii PECH rămân în baza celor șase poziții.
Ultimul răspuns: în această intervenție nu s-au preluat comunicări primite noi; instrucțiunile utilizatorului au fost aplicate propunerii și aceluiași draft EVA pending, fără trimitere.
Calendar: E1-E7 ca variantă de lucru, numai pentru propriile șase poziții; calendar comun de livrare/facturare pe etape mari cu net/TVA/brut de agreat înainte de semnare. 18 luni de la B0 real, 12 Abnahmen incluse + până la 6 opționale proprii ×450 EUR net; costurile funcțiilor complete nu se deduc automat din tariful vizitelor.
Următorul pas: lectura utilizatorului, apoi clarificarea de către PECH a funcțiilor, prestatorilor, prețurilor incluse sau suplimentare și calendarului; niciun cost extern nu este comandat tacit. Contract nesemnat, draft netrimis, fără plăți. BERGER și PECH R08 sunt intacte.
Surse: 00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09/2026.10.13 Werkvertrag PECH R09.pdf; 2026.10.13 Email PECH R09 NETRIMIS.txt/json/eml în același folder; registru intern 00.Proiect/09. Vertraege/2026.10.13 PECH R09 - intern/2026.10.13 Registru PECH R09 final.json. EVA ID 8e954def-ac5f-4782-b5c7-b25c64572bb9, To sekretariat@zt-pech.at, CC ployer@zt-pech.at, actual updated_at: '''+d['updated_at']+'\n'
for relative in ['2026.10.13 Status proiect.txt','2026.10.13 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - Pech.txt']:
 p=R/relative;prior=p.read_text(encoding='utf-8-sig') if p.exists() else '';p.write_text(notice+'\nISTORIC PĂSTRAT\n\n'+prior,encoding='utf-8')
readme=R/'folder map/README.md';previous=readme.read_text(encoding='utf-8-sig')
readme.write_text('# 2026.10.13 — PECH R09: funcții complete cerute, costuri de confirmat\n\n'+notice+'\nISTORIC PĂSTRAT\n\n'+previous,encoding='utf-8')
print(json.dumps({'draft_status':d['status'],'attachments':records,'communicatii_unchanged':count,'drafts_unchanged':draftcount,'frozen_files_verified':len(frozen),'journals_updated':3},ensure_ascii=False))
