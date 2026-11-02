from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
from email import policy
import json,hashlib,shutil
root=Path.cwd();out=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11';qa=root/'folder map/2026.10.29 QA BERGER R11';backup=qa/'backup-doua-atasamente';backup.mkdir(exist_ok=True)
src=out/'2026.10.29 Ciorna BERGER R11 cu ambele PDF-uri - EVA original.json';m=json.loads(src.read_text(encoding='utf-8'));d=m['original_EVA'];assert d['status']=='pending' and len(d['attachments'])==2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(qa/'2026.10.29 Readback comparatie EVA.pdf')==sha(out/d['attachments'][1]['filename'])
em=EmailMessage(policy=policy.SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Subject']=d['subject'];em['Date']=datetime.fromisoformat(d['updated_at'].replace('Z','+00:00'));em['X-Unsent']='1';em['X-EVA-Draft-ID']=d['id'];em.set_content(d['body'])
for a in d['attachments']:em.add_attachment((out/a['filename']).read_bytes(),maintype='application',subtype='pdf',filename=a['filename'])
dest=out/'2026.10.29 Email BERGER R11 - ambele PDF-uri NETRIMIS.eml';dest.write_bytes(em.as_bytes())
now=datetime.now().astimezone().isoformat(timespec='seconds');rel=src.relative_to(root).as_posix()
entry=f'''2026.10.29 | Ciorna BERGER R11 - AMBELE PDF-uri
Verificat: {now}
Status scurt: La cererea expresa a utilizatorului, aceeasi ciorna EVA contine acum DOUA PDF-uri: contractul R11 (32 pagini, 335.514 octeti) si comparatia original/modificat cu decizii (44 pagini, 224.847 octeti). Status pending/NETRIMIS. Sumele si documentele comerciale nu s-au modificat.
Ultimul raspuns extern relevant: neschimbat, BERGER 2026.10.27 privind Bauwerksbuch 2.500 EUR net. Actualizarea de azi este o modificare de ciorna, nu mesaj trimis sau acceptare.
Urmatorul pas: Redeschiderea ciornei in EVA; proprietarul verifica ambele PDF-uri inainte de trimitere. Confirmarile si completarile BERGER presemnare raman deschise.
Sursa: {rel}; EVA draft {d['id']}; atasamente {[a['id'] for a in d['attachments']]}. Comparatia descarcata din EVA are SHA-256 identic cu PDF-ul local. API readback confirma doua atasamente; interfata nu a putut fi verificata vizual din cauza indisponibilitatii instrumentului UI. Este salvata si copia EML netrimisa cu ambele atasamente reale.
Nu s-au trimis emailuri, semnat contracte sau efectuat plati. Documentele PDF si PECH nemodificate; acoperirea verificarilor globale email nu este extinsa.
'''
for i,p in enumerate([root/'2026.10.29 Status proiect.txt',root/'2026.10.29 Log progres proiect.txt',root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - Markus Berger.txt',root/'folder map/README.md']):
 old=p.read_text(encoding='utf-8');shutil.copy2(p,backup/f'{i}-{p.name}');p.write_text(entry+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
reg=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.29 Registru comunicatii.json';shutil.copy2(reg,backup/reg.name);j=json.loads(reg.read_text(encoding='utf-8'))
for dr in j['drafturi']:
 if dr.get('id')==d['id']:
  dr.setdefault('istoric_atasamente',[]).append({'data':now,'atasamente':dr.get('atasamente',[]),'sursa':dr.get('sursa')});dr.update(atasamente=d['attachments'],sursa=rel,data_verificarii=now,status='pending',statut='DRAFT NETRIMIS; doua PDF-uri confirmate prin readback')
j['actualizari_punctuale'].append({'data':'2026.10.29','ora_iso':now,'tip':'Ciorna BERGER R11 doua PDF-uri','draft_id':d['id'],'status':'pending / NETRIMIS','atasamente':d['attachments'],'sursa':rel})
for s in j['statusuri']:
 if s.get('partener')=='Markus Berger':s['ciorna_R11_atasamente']=d['attachments'];s['ciorna_R11_sursa']=rel
assert len(j['comunicatii'])==845 and len(j['drafturi'])==17
reg.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'2026.10.29 Log atasare ambele PDF-uri BERGER.txt').write_text(entry,encoding='utf-8')
print(json.dumps({'draft_id':d['id'],'status':d['status'],'attachments':d['attachments'],'eml':str(dest),'comparison_hash':sha(qa/'2026.10.29 Readback comparatie EVA.pdf')},ensure_ascii=False))
