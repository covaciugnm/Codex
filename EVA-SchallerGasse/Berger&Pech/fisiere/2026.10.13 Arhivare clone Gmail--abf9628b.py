from pathlib import Path
from email.message import EmailMessage
from email.policy import SMTP
import json,hashlib,re
R=Path.cwd();I=R/'00.Proiect/09. Vertraege/2026.10.13 PECH R09 - intern';A=R/'08. Corespondenta/2026.10.13 Ciorne Gmail Berger si Pech'
A.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):
 r=json.loads(p.read_text(encoding='utf-8'));return r.get('structuredContent') or json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json';j=json.loads(registry.read_text(encoding='utf-8-sig'));count=len(j['comunicatii']);results=[]
for provider in ['BERGER','PECH']:
 source=get(I/('2026.10.13 BERGER original EVA pentru clone Gmail.json' if provider=='BERGER' else '2026.10.13 EVA PECH R09 readback original.json'))
 rawpath=I/f'2026.10.13 EVA Gmail {provider} readback original.json';d=get(rawpath)
 assert d['status']=='pending' and d['account_email']=='covaciu.gnm@gmail.com'
 assert d['body']==source['body'] and d['to']==source['to'] and d['cc']==source['cc'] and d['bcc']==source['bcc'] and d['subject']==source['subject']
 assert d['attachments']==source['attachments']
 folder=R/('00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09' if provider=='BERGER' else '00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09')
 files=[]
 for x in d['attachments']:
  p=folder/x['filename'];assert p.stat().st_size==x['size'];files.append({'filename':x['filename'],'local_path':str(p.relative_to(R)),'sha256':sha(p),'document_id':x['id'],'bytes':x['size']})
 meta={'data':'2026.10.13','subiect':d['subject'],'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'bcc':d['bcc'],'id_Eva_Mail':d['id'],'statut':'DRAFT EVA pending / NETRIMIS','created_at':d['created_at'],'updated_at':d['updated_at'],'body_original':d['body'],'attachments':files,'cloned_from_draft_id':source['id'],'source_status_at_readback':source['status'],'identical_body_recipients_subject_attachments':True,'original_EVA':str(rawpath.relative_to(R))}
 prefix=f'2026.10.13 Email {provider} Gmail NETRIMIS'
 write(A/(prefix+'.json'),meta)
 (A/(prefix+'.txt')).write_text('2026.10.13 | DRAFT EVA pending / NETRIMIS\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nSubiect: '+d['subject']+'\nID Eva-Mail: '+d['id']+'\nCreated_at: '+d['created_at']+'\nUpdated_at: '+d['updated_at']+'\n\n'+d['body']+'\n',encoding='utf-8')
 em=EmailMessage(policy=SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-EVA-Draft-ID']=d['id'];em['X-Archive-Readable-Date']='2026.10.13'
 if d['cc']:em['Cc']=', '.join(d['cc'])
 em.set_content(d['body'])
 for x in files:em.add_attachment((R/x['local_path']).read_bytes(),maintype='application',subtype='pdf',filename=x['filename'])
 (A/(prefix+'.eml')).write_bytes(em.as_bytes())
 entry={'data':'2026.10.13','id':d['id'],'statut':'DRAFT EVA pending / NETRIMIS; copie Gmail '+provider,'cale':str((A/(prefix+'.txt')).relative_to(R)),'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'subiect':d['subject'],'original_EVA':str(rawpath.relative_to(R)),'EML':str((A/(prefix+'.eml')).relative_to(R)),'atasamente':files,'sursa_id':source['id'],'sursa_statut':source['status']}
 assert not any(x['id']==entry['id'] for x in j['drafturi']);j['drafturi'].append(entry);results.append(meta)
 partner=R/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - {"Berger" if provider=="BERGER" else "Pech"}.txt'
 if not partner.exists() and provider=='BERGER':
  matches=list(partner.parent.glob('*Log discutii*Berger*'));partner=matches[-1] if matches else partner
 prior=partner.read_text(encoding='utf-8-sig') if partner.exists() else '';history=I/('2026.10.13 Istoric partener '+provider+' inainte clone Gmail.txt');history.write_text(prior,encoding='utf-8')
 note='2026.10.13 — Copie Gmail '+provider+' creată în EVA, pending / NETRIMIS. Expeditor covaciu.gnm@gmail.com; conținutul, destinatarii, subiectul și cele două PDF-uri identice sursei curente. ID '+d['id']+'. Sursa '+source['id']+' are statut EVA '+source['status']+' la citire; sursa nu a fost modificată prin clonare.\nUltimul răspuns: nu s-a preluat o comunicare primită nouă; copie cerută de utilizator.\nUrmătorul pas: lectura/selectarea ciornei de către utilizator; niciun mesaj trimis prin această operație.\nSursa: '+str((A/(prefix+'.json')).relative_to(R))+'; updated_at '+d['updated_at']+'.\n'
 partner.write_text(note+'\nISTORIC PĂSTRAT\n\n'+prior,encoding='utf-8')
 if provider=='BERGER':
  original=next(x for x in j['drafturi'] if x['id']==source['id']);original['statut']='EVA sent observat la readback; istoric draft BERGER';original['status_readback_source']=str((I/'2026.10.13 BERGER original EVA pentru clone Gmail.json').relative_to(R));original['nota_verificare']='Statut sent observat la citire; agentul nu a trimis și nu a modificat acest mesaj.'
j['actualizari_punctuale'].append({'data':'2026.10.13','tip':'Doua copii Gmail ale ciornelor curente BERGER si PECH','drafts_created':2,'sent':0,'source_berger_status':'sent observed only','originals_not_mutated_by_cloning':True,'sursa':str((A/'2026.10.13 Registru clone Gmail.json').relative_to(R))})
assert len(j['comunicatii'])==count
write(registry,j);write(A/'2026.10.13 Registru clone Gmail.json',{'date':'2026.10.13','drafturi':results,'drafts_created':2,'sent_by_agent':0,'existing_documents_unchanged':True})
note='2026.10.13 — Două ciorne identice de pe covaciu.gnm@gmail.com create în EVA: BERGER și PECH, ambele pending / NETRIMISE. Aceleași corpuri originale, destinatari, CC, subiect și atașamente PDF reale ca sursele curente. BERGER office apare cu statut sent la readback; agentul nu l-a trimis/modificat. PECH office R09 pending. Următorul pas: lectura/selectarea de către utilizator; nicio trimitere efectuată. Sursă: 08. Corespondenta/2026.10.13 Ciorne Gmail Berger si Pech/2026.10.13 Registru clone Gmail.json.\n'
for relative in ['2026.10.13 Status proiect.txt','2026.10.13 Log progres proiect.txt','folder map/README.md']:
 p=R/relative;previous=p.read_text(encoding='utf-8-sig');p.write_text(note+'\nISTORIC PĂSTRAT\n\n'+previous,encoding='utf-8')
print(json.dumps({'clones':[{k:x[k] for k in ['id_Eva_Mail','expeditor','destinatari','statut']} for x in results],'body_and_attachments_identical':True},ensure_ascii=False))
