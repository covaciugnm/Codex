import json,shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import format_datetime
now=datetime.now(ZoneInfo('Europe/Bucharest'));day='2026.10.26';stamp=now.isoformat();tag=now.strftime('%H-%M-%S')
assert now.strftime('%Y.%m.%d')==day
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');reg=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Ciorne confirmare intalniri BERGER PECH')
proof=folder/(day+' Dovezi creare si recitire EVA.json');journal=folder/(day+' Jurnal ciorne confirmare.txt')
hist=Path('folder map')/(day+' Istoric ciorne confirmare '+tag)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def backup(p):
 p=Path(p)
 if p.exists():
  h=hist/p;h.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,h)
def save(p,text):
 p=Path(p);backup(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
p=read('folder map/2026.10.26 Dovezi ciorne confirmare intalniri.json');r=read(reg)
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==836
general=r['acoperire']['verificare_incrementala'].copy();bp=r['acoperire']['verificare_punctuala_BERGER_PECH'].copy()
new=[];files=[];sections={}
for item in p['drafts']:
 partner=item['partner'];d=item['readback'];a=item['args'];name='BERGER' if partner=='Markus Berger' else 'PECH'
 hour='11:30' if name=='BERGER' else '14:00'
 address='Schönbrunner Straße 123/2, 1050 Wien' if name=='BERGER' else 'Johann-Strauß-Gasse 32/6, 1040 Wien'
 assert d['status']=='pending' and d['account_email']=='office@ac-wohnart.at'
 assert d['id']==item['created']['id'] and d['reply_to_email_id']==a['reply_to_email_id']
 assert d['to']==a['to'] and d['cc']==a['cc'] and not d.get('bcc') and not d['attachments']
 assert all(x in d['body'] for x in ('2026.10.27','Dienstag',hour,'Wiener Ortszeit',address,'Wir kommen zu Ihnen ins Büro'))
 assert ('BERGER' not in d['body'].upper()) if name=='PECH' else ('PECH' not in d['body'].upper())
 txt=folder/(day+' Email confirmare '+name+' NETRIMIS.txt')
 raw=folder/(day+' DRAFT confirmare '+name+'.json');eml=txt.with_suffix('.eml')
 jsave(raw,{'data_lizibila':day,'statut':'DRAFT NETRIMIS','expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'ID_Eva_Mail_draft':d['id'],'original_EVA_create':item['created'],'original_EVA_readback':d,'argumente_creare':a,'nota':'Text cu semnatura adaugata de EVA; nu este mesaj trimis.'})
 save(txt,'Data: '+day+'\nStatut: DRAFT NETRIMIS (EVA pending)\nID Eva-Mail draft: '+d['id']+'\nExpeditor: '+d['account_email']+'\nDestinatari: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nSubiect: '+d['subject']+'\nIn raspuns la email ID: '+d['reply_to_email_id']+'\nAtasamente: niciunul\nData tehnica creare EVA: '+d['created_at']+'\n\nTEXT CIORNA RECITIT DIN EVA\n\n'+d['body'])
 message=EmailMessage(policy=SMTP);message['From']=d['account_email'];message['To']=', '.join(d['to'])
 if d['cc']:message['Cc']=', '.join(d['cc'])
 message['Subject']=d['subject'];message['Date']=format_datetime(datetime.fromisoformat(d['created_at'].replace('Z','+00:00')))
 message['X-Unsent']='1';message['X-EVA-Draft-ID']=d['id'];message['X-EVA-Status']='pending';message['X-EVA-Reply-To-Email-ID']=d['reply_to_email_id']
 message.set_content(d['body'],charset='utf-8');backup(eml);eml.write_bytes(message.as_bytes())
 draft={'data':day,'id':d['id'],'partener':partner,'statut':'DRAFT NETRIMIS; EVA pending verificat la recitire','cale':txt.as_posix(),'original_EVA':raw.as_posix(),'EML':eml.as_posix(),'expeditor':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'subiect':d['subject'],'created_at':d['created_at'],'updated_at':d['updated_at'],'reply_to_email_id':d['reply_to_email_id'],'atasamente':[],'intalnire_propusa':{'data':'2026.10.27','ora':hour,'timezone':'Europe/Vienna','loc':address,'confirmare_beneficiar':'pregatita in draft, NETRIMISA','confirmata_prin_trimiterea_draftului':False},'sursa':proof.as_posix()}
 assert not any(x['id']==d['id'] for x in r['drafturi'])
 r['drafturi'].append(draft);new.append(draft);files.extend([txt.as_posix(),raw.as_posix(),eml.as_posix()])
 s=next(x for x in r['statusuri'] if x.get('partener')==partner)
 s.setdefault('istoric_status',[]).append({'data_preluarii':day,**{k:s.get(k) for k in ('status','ultimul_raspuns','urmatorul_pas','sursa_status')}})
 s['status']='2026.10.26: confirmare intalnire 2026.10.27 '+hour+' ora Vienei, la '+address+', pregatita in EVA ca DRAFT NETRIMIS. Nu s-a trimis confirmarea catre partener si nu se considera acceptare a contractului.'
 s['urmatorul_pas']='Lectura si trimiterea ciornei din EVA de catre utilizator; apoi verificarea dovezii trimiterii. Confirmarea este deocamdata numai in draft.'
 s['data_actualizarii']=day;s['draft_confirmare_intalnire']=d['id'];s['sursa_status']=[raw.as_posix(),proof.as_posix()]
 sections[partner]=name+'\nStatus scurt: '+s['status']+'\nUltimul raspuns primit: '+str(s.get('ultimul_raspuns'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nDestinatari: '+', '.join(d['to'])+'; CC: '+', '.join(d['cc'])+'\nID draft: '+d['id']+'\nSursa: '+raw.as_posix()+'\n'
assert len(new)==2
entry={'data':day,'checked_at_iso':stamp,'tip':'Doua ciorne de confirmare intalniri, NETRIMISE','drafturi_noi':2,'mesaje_trimise':0,'draft_ids':[x['id'] for x in new],'sursa':proof.as_posix()}
r['acoperire']['ciorne_confirmare_intalniri_BERGER_PECH']=entry;r.setdefault('actualizari_punctuale',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general and r['acoperire']['verificare_punctuala_BERGER_PECH']==bp
jsave(reg,r);jsave(proof,{'operatiune':entry,'dovezi_originale':p,'fisiere':files,'nota':'Doar creare si recitire ciorne. Niciun email trimis, calendar creat, contract acceptat ori semnat. EML-urile sunt exporturi generate pentru ciorne si au X-Unsent: 1; nu sunt MIME originale ale mesajelor trimise.'})
text=day+' '+now.strftime('%H:%M:%S')+' — Ciorne confirmare intalniri 2026.10.27\n\n'+'\n'.join(sections.values())+'\nAmbele ciorne sunt in germana, din office@ac-wohnart.at, in firele existente, fara atasamente. Ora locala a Vienei si adresa completa sunt explicite in fiecare. Mesajele nu sunt trimise si nu reprezinta acceptarea contractelor.\nSursa: '+proof.as_posix()+'\n'
save(journal,text)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt');save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
for partner,section in sections.items():
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt');save(path,day+' '+now.strftime('%H:%M:%S')+' — Confirmare intalnire pregatita\n\n'+section+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,text+'Dosar: ../'+folder.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==836
print(json.dumps({'journal':journal.as_posix(),'proof':proof.as_posix(),'files':files,'draft_ids':[x['id'] for x in new],'real_email_IDs':836,'draft_status':'both pending, unsent','previous_coverage':'preserved'},ensure_ascii=False))
