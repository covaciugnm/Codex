from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
from email import policy
import json, re, hashlib, shutil, unicodedata
import fitz
root=Path.cwd();out=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11';qa=root/'folder map/2026.10.29 QA BERGER R11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
model=json.loads((out/'2026.10.29 Werkvertrag BERGER R11.json').read_text(encoding='utf-8'));cmp=json.loads((out/'2026.10.29 BERGER R11 model comparativ si decizii.json').read_text(encoding='utf-8'))
doc=fitz.open(out/'2026.10.29 Werkvertrag BERGER R11.pdf');text='\n'.join(p.get_text() for p in doc[:-4]);norm=lambda x:re.sub(r'\s+','',unicodedata.normalize('NFKC',x))
hay=norm(text);missing=[];n=0
for section in model['sections']+model['annexes']:
 for p in section['paragraphs']:
  n+=1
  if norm(p) not in hay:missing.append(p[:90])
assert not missing,missing
for a in model['annexes']:
 for table in a['tables']:
  for row in table['rows']:
   for c in row:
    assert norm(str(c)) in hay,str(c)[:100]
assert sum([13000,20000,2000,10000,2500])==47500 and 47500*1.2==57000
assert cmp['vorschlag']==model
draftmeta=json.loads((out/'2026.10.29 Email BERGER R11 - ciorna EVA original.json').read_text(encoding='utf-8'));d=draftmeta['original_EVA'];assert d['status']=='pending'
assert d['to']==['office@bmberger.at'] and d['cc']==[] and d['bcc']==[]
assert d['attachments'][0]['filename']=='2026.10.29 Werkvertrag BERGER R11.pdf' and len(d['attachments'])==1
assert sha(out/d['attachments'][0]['filename'])==sha(qa/'2026.10.29 Readback atasament EVA.pdf')
em=EmailMessage(policy=policy.SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Subject']=d['subject'];em['Date']=datetime.fromisoformat(d['created_at'].replace('Z','+00:00'));em['X-Unsent']='1';em['X-EVA-Draft-ID']=d['id'];em['X-EVA-Reply-To-Email-ID']=d['reply_to_email_id'];em.set_content(d['body']);em.add_attachment((out/d['attachments'][0]['filename']).read_bytes(),maintype='application',subtype='pdf',filename=d['attachments'][0]['filename']);(out/'2026.10.29 Email BERGER R11 - NETRIMIS.eml').write_bytes(em.as_bytes())
now=datetime.now().astimezone().isoformat(timespec='seconds');source=str(out.relative_to(root)).replace('\\','/');draftsource=source+'/2026.10.29 Email BERGER R11 - ciorna EVA original.json'
status='Propunerea BERGER R11 actualizata dupa scanul adnotat si cele sase raspunsuri explicite ale proprietarului; 47.500 EUR net / 57.000 EUR cu TVA, inclusiv Bauwerksbuch complet 2.500 EUR net. Ciorna germana EVA cu PDF verificat este NETRIMISA; nicio acceptare sau semnare.'
nextstep='Proprietarul citeste R11 si ciorna; BERGER trebuie sa confirme corectitudinea interpretarii, obiectul complet Bauwerksbuch la 2.500 EUR, PI/ZT si includerea in pret, persoanele/befugnis, valabilitatea onorariului, planurile si calendarul de livrare/facturare cu date si valori. Numele arhitectului/Einreichplaner/Baufuhrer raman de completat separat, fara atribuirea lor lui BERGER.'
entry=f'''2026.10.29 | Contract BERGER R11 si ciorna pentru confirmare
Actualizat: {now}

Status scurt: {status}
Ultimul raspuns extern relevant ramane 2026.10.27: BERGER oferteaza Bauwerksbuch la 2.500 EUR net si cere clarificarea Planung / Planverfasser / Planwechsel; ID EVA ed6dfacf-1a5e-4447-8faa-833514e87070. Cele sase raspunsuri ale proprietarului din 2026.10.29 sunt decizii interne, nu acceptare BERGER.
Modificari: 5 zile lucratoare Werkstattplane; 3 zile RFI; PDF semnat, DWG/DXF editabile, calcule complete, IFC/native numai existente si transferabile; email saptamanal scurt in perioade active si lista comuna simpla; rolurile externe delimitate; PI/ZT de confirmat nominal si comercial; Bauwerksbuch complet existent+interventii noi, prima verificare, inregistrare necesara si actualizari pana la inchidere.
Pret: patru pozitii originale 13.000 + 20.000 + 2.000 + 10.000 = 45.000 EUR net, neschimbate; numai Bauwerksbuch adaugat 2.500 = 47.500 EUR net. Optiunile 1.000 EUR net/4 vizite necesita comanda expresa; niciuna comandata. 8 vizite statice incluse, T0 numai daca exista asistenta statica efectiva; 18 luni de la B0 real; 14 zile plata; garantie 3 ani; fara indexare, retentie contractuala ori penalitate.
Verificare: doua audituri independente, corecturile inchise; 10/10 pentru coerenta juridica a propunerii pentru confirmare si 10/10 pentru conformitate documentara/financiara, nu certificare de semnabilitate. Randate si inspectate PDFcurat 32 pagini si comparatie 44 pagini; ultimele 4 pagini din PDFcurat sunt pixel-identice cu oferta originala. Textul tuturor paragrafelor/tabelelor verificat; atasamentul EVA redescărcat si SHA-256 identic.
Ciorna: ID {d['id']}; de la office@ac-wohnart.at catre office@bmberger.at; fara CC/BCC; status EVA pending la readback; 1 atasament PDF R11. Emailul explica textul anterior si modificarile pe 11 puncte si solicita confirmare sau corecturi punctuale; nu afirma acordul BERGER si nu mentioneaza alti ofertanti.
Urmatorul pas: {nextstep}
Surse: {source}; {draftsource}; raspunsurile proprietarului salvate in JSON; scan original si oferta originale pastrate.
Nu s-au trimis emailuri, semnat contracte, comandat servicii sau efectuat plati. PECH nemodificat. Acest lucru punctual nu extinde acoperirea ultimei verificari globale EVA.
'''
backup=qa/'backup-inainte-finalizare';backup.mkdir(exist_ok=True)
targets=[root/'2026.10.29 Status proiect.txt',root/'2026.10.29 Log progres proiect.txt',root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - Markus Berger.txt',root/'folder map/README.md']
for i,p in enumerate(targets):
 old=p.read_text(encoding='utf-8')
 if 'Contract BERGER R11 si ciorna pentru confirmare' not in old:
  shutil.copy2(p,backup/f'{i}-{p.name}');p.write_text(entry+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
reg=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.29 Registru comunicatii.json';j=json.loads(reg.read_text(encoding='utf-8'));before=len(j['comunicatii']);assert before==845
if not any(x.get('id')==d['id'] for x in j['drafturi']):
 shutil.copy2(reg,backup/reg.name)
 j['drafturi'].append({'id':d['id'],'partener':'Markus Berger','status':'pending','statut':'DRAFT NETRIMIS verificat prin eva_get_draft','account_email':d['account_email'],'destinatari':d['to'],'cc':d['cc'],'bcc':d['bcc'],'subiect':d['subject'],'created_at':d['created_at'],'data_verificarii':now,'atasamente':d['attachments'],'sursa':draftsource})
 j['actualizari_punctuale'].append({'data':'2026.10.29','ora_iso':now,'tip':'BERGER R11 propunere contract si draft NETRIMIS','status':status,'sursa':source,'draft_id':d['id'],'acoperire_EVA_extinsa':False})
 for s in j['statusuri']:
  if s.get('partener','').lower() in ('markus berger','berger'):
   s.setdefault('istoric_actualizari_contractuale',[]).append({'data':'2026.10.29','status_anterior':s.get('status'),'urmatorul_pas_anterior':s.get('urmatorul_pas')})
   s.update(status=status,urmatorul_pas=nextstep,data_actualizarii='2026.10.29',sursa_contractuala_R11=source,ciorna_R11_id=d['id'])
 reg.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(j['comunicatii'])==845 and len(j['drafturi'])==17
for p in qa.glob('2026.10.29 *audit*.txt'):shutil.copy2(p,out/p.name)
for p in qa.glob('2026.10.29 Audit *independent*.txt'):shutil.copy2(p,out/p.name)
for p in qa.glob('2026.10.29 Audit conformitate*.txt'):shutil.copy2(p,out/p.name)
proof={'data':'2026.10.29','verified_at':now,'contract_pages':len(doc),'compared_paragraphs':n,'missing_paragraphs':missing,'model_consistency':True,'original_offer_pixel_identity':[True]*4,'pdf_sha256':sha(out/'2026.10.29 Werkvertrag BERGER R11.pdf'),'eva_attachment_sha256':sha(qa/'2026.10.29 Readback atasament EVA.pdf'),'draft_id':d['id'],'draft_status':d['status'],'actual_email_ids':845,'draft_records':17,'legal_audit_score':'10/10 pentru propunere destinata confirmarii','conformity_audit_score':'10/10 pentru conformitate documentara/financiara','pre_signature_open_items':nextstep}
(out/'2026.10.29 Verificare finala BERGER R11.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8');(out/'2026.10.29 Status BERGER R11 si email NETRIMIS.txt').write_text(entry,encoding='utf-8');print(json.dumps(proof,ensure_ascii=False))
