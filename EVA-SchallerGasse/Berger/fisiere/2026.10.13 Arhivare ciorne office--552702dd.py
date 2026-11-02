from pathlib import Path
from email.message import EmailMessage
from email import parser,policy
import json,hashlib,shutil
R=Path.cwd();A=R/'08. Corespondenta/2026.10.13 Ciorne office Berger si Pech'
def get(name):
 x=json.loads((A/name).read_text(encoding='utf-8'));return x.get('structuredContent') or json.loads(next(y['text'] for y in x['content'] if y['type']=='text'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json'
shutil.copy2(registry,A/'2026.10.13 Registru comunicatii inainte copii office.json')
j=json.loads(registry.read_text(encoding='utf-8-sig'));real_count=len(j['comunicatii']);result=[];checked=[]
inventory={x['cale']:x for x in json.loads((R/'folder map/inventar.json').read_text(encoding='utf-8'))}
for provider in ['BERGER','PECH']:
 d=get(f'2026.10.13 EVA {provider} readback original.json');g=get(f'2026.10.13 EVA Gmail {provider} source original.json')
 assert d['status']==g['status']=='pending' and d['account_email']=='office@ac-wohnart.at' and g['account_email']=='covaciu.gnm@gmail.com'
 for key in ['to','cc','bcc','body','subject','attachments']:assert d[key]==g[key],key
 folder=R/('00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09' if provider=='BERGER' else '00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09')
 attachments=[]
 for att in d['attachments']:
  p=folder/att['filename'];rel=p.relative_to(R).as_posix();assert p.stat().st_size==att['size'];assert sha(p)==inventory[rel]['sha256'];checked.append({'path':rel,'sha256':sha(p)})
  attachments.append({'filename':p.name,'local_path':rel,'document_id':att['id'],'bytes':att['size'],'sha256':sha(p)})
 prefix=f'2026.10.13 Email {provider} office NETRIMIS'
 meta={'data':'2026.10.13','expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'bcc':d['bcc'],'subiect':d['subject'],'ID_Eva_Mail':d['id'],'statut':'DRAFT EVA pending / NETRIMIS','created_at':d['created_at'],'updated_at':d['updated_at'],'body_original':d['body'],'atasamente':attachments,'original_EVA':str((A/f'2026.10.13 EVA {provider} readback original.json').relative_to(R)),'gmail_identical_draft_id':g['id'],'no_send':True}
 write(A/(prefix+'.json'),meta)
 (A/(prefix+'.txt')).write_text('2026.10.13 | DRAFT EVA pending / NETRIMIS\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nSubiect: '+d['subject']+'\nID Eva-Mail: '+d['id']+'\nCreated_at: '+d['created_at']+'\nUpdated_at: '+d['updated_at']+'\n\n'+d['body']+'\n',encoding='utf-8')
 em=EmailMessage(policy=policy.SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-EVA-Draft-ID']=d['id'];em['X-Archive-Readable-Date']='2026.10.13'
 if d['cc']:em['Cc']=', '.join(d['cc'])
 em.set_content(d['body'])
 for att in attachments:em.add_attachment((R/att['local_path']).read_bytes(),maintype='application',subtype='pdf',filename=att['filename'])
 path=A/(prefix+'.eml');path.write_bytes(em.as_bytes());parsed=parser.BytesParser(policy=policy.default).parsebytes(path.read_bytes())
 assert {x.get_filename():hashlib.sha256(x.get_payload(decode=True)).hexdigest() for x in parsed.iter_attachments()}=={x['filename']:x['sha256'] for x in attachments}
 entry={'data':'2026.10.13','id':d['id'],'statut':'DRAFT EVA pending / NETRIMIS; '+provider+' office','cale':str((A/(prefix+'.txt')).relative_to(R)),'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'subiect':d['subject'],'original_EVA':meta['original_EVA'],'EML':str(path.relative_to(R)),'atasamente':attachments,'gmail_identical_draft_id':g['id']}
 existing=next((x for x in j['drafturi'] if x['id']==d['id']),None)
 if existing:existing.update(entry)
 else:j['drafturi'].append(entry)
 result.append(meta)
 partner=R/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - {"Berger" if provider=="BERGER" else "Pech"}.txt'
 if not partner.exists():
  matches=list(partner.parent.glob('*Log discutii*'+('Berger' if provider=='BERGER' else 'Pech')+'*'));partner=matches[-1] if matches else partner
 previous=partner.read_text(encoding='utf-8-sig') if partner.exists() else '';(A/f'2026.10.13 Istoric jurnal {provider} inainte office.txt').write_text(previous,encoding='utf-8')
 note='2026.10.13 — Ciornă '+provider+' office@ac-wohnart.at verificată pending / NETRIMIS. ID '+d['id']+'. Corp, destinatari, CC, subiect și cele două PDF-uri identice ciornei Gmail '+g['id']+'. '+('Ciornă office nouă, deoarece sursa anterioară apare sent; istoricul trimis nu a fost modificat.' if provider=='BERGER' else 'Ciorna office R09 existentă păstrată; nu s-a creat un duplicat.')+'\nUltimul răspuns: instrucțiunea utilizatorului de a avea ambele ciorne și pe office; nicio comunicare primită nouă.\nUrmătorul pas: lectura/selectarea ciornei; nu s-a trimis niciun email.\nSursa: '+str((A/(prefix+'.json')).relative_to(R))+'; updated_at '+d['updated_at']+'.\n'
 partner.write_text(note+'\nISTORIC PĂSTRAT\n\n'+previous,encoding='utf-8')
j['actualizari_punctuale'].append({'data':'2026.10.13','tip':'Ciorne BERGER si PECH si pe office@ac-wohnart.at','drafts_created':1,'existing_drafts_reused':1,'drafts_updated':0,'sent':0,'gmail_preserved':True,'sursa':str((A/'2026.10.13 Registru ciorne office.json').relative_to(R))})
assert len(j['comunicatii'])==real_count
write(registry,j);write(A/'2026.10.13 Registru ciorne office.json',{'date':'2026.10.13','office_drafts':result,'created':1,'existing_reused':1,'sent':0,'four_pending_drafts_verified':True,'pdfs_unchanged':checked,'real_message_count_unchanged':real_count})
note='2026.10.13 — BERGER și PECH: câte o ciornă pending / NETRIMIS pe office@ac-wohnart.at și pe covaciu.gnm@gmail.com, patru ciorne active verificate. Textele, destinatarii, CC, subiectele și PDF-urile fiecărei perechi sunt identice. BERGER office nou ID f8c09c6b-f102-4998-877d-62c269ac5cdd; PECH office R09 existent ID 8e954def-ac5f-4782-b5c7-b25c64572bb9. BERGER office anterior cu statut sent rămâne istoric neatins. Ultimul răspuns: cerința utilizatorului aplicată; nicio comunicare primită nouă. Următorul pas: lectura/selectarea de către utilizator; nicio trimitere. Sursa: 08. Corespondenta/2026.10.13 Ciorne office Berger si Pech/2026.10.13 Registru ciorne office.json.\n'
for relative in ['2026.10.13 Status proiect.txt','2026.10.13 Log progres proiect.txt','folder map/README.md']:
 p=R/relative;previous=p.read_text(encoding='utf-8-sig');(A/('2026.10.13 Istoric '+p.name)).write_text(previous,encoding='utf-8');p.write_text(note+'\nISTORIC PĂSTRAT\n\n'+previous,encoding='utf-8')
print(json.dumps({'office_pending':[{'id':x['ID_Eva_Mail'],'to':x['destinatari']} for x in result],'paired_with_gmail_identically':True,'created':1,'sent':0},ensure_ascii=False))
