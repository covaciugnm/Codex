from pathlib import Path
import json,shutil,hashlib
from email.message import EmailMessage
from email.policy import SMTP
r=Path(__file__).resolve().parent.parent
c=r/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau'
raw=c/'2026.10.14 Draft Eva-Mail Donau NUMAI DONAU verificat.json'
d=json.loads(raw.read_text(encoding='utf8'))
assert d['status']=='pending' and not d['cc'] and not d['bcc']
assert all(x.endswith('@donauversicherung.at') for x in d['to'])
assert 'Empfänger in CC' not in d['body']
def preserve(p):
 t=c/'Istoric'/'2026.10.14 Inainte de eliminarea CC'/p.relative_to(r);t.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and not t.exists():shutil.copy2(p,t)
s='2026.10.14 Email polita anterioara si plata primelor NETRIMIS'
for ext in ['.txt','.json','.eml']:preserve(c/(s+ext))
j=json.loads((c/(s+'.json')).read_text(encoding='utf8'));j.update(cc=[],bcc=[],body=d['body'],eva_mail_id=d['id'],status='draft Eva-Mail pending NETRIMIS; numai DONAU');(c/(s+'.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
(c/(s+'.txt')).write_text('2026.10.14 | DRAFT EVA-MAIL NETRIMIS | ID '+d['id']+'\nDe la: '+d['account_email']+'\nCătre: '+'; '.join(d['to'])+'\nCC: fără\nBCC: fără\nSubiect: '+d['subject']+'\nAtașamente: niciunul\n\n'+d['body'],encoding='utf-8-sig')
em=EmailMessage(policy=SMTP);em['From']=d['account_email'];em['To']=', '.join(d['to']);em['Subject']=d['subject'];em['X-Unsent']='1';em['X-Eva-Draft-ID']=d['id'];em.set_content(d['body']);(c/(s+'.eml')).write_bytes(em.as_bytes())
marker='2026.10.14 — DONAU: destinatari corectați, numai DONAU, fără CC/BCC'
note=marker+'\n\nStatus scurt: La precizarea utilizatorului au fost eliminați Capra, Maritczak și Commerz din CC-ul draftului '+d['id']+'. Rămân exclusiv cele patru adrese DONAU din To. CC și BCC sunt goale. A fost eliminată și cererea de includere a destinatarilor CC din corpul emailului.\nUltimul răspuns DONAU: 2026.10.06. Verificarea actuală privește doar draftul, recitit din Eva-Mail cu status pending / NETRIMIS. Niciun email nu a fost trimis prin această operațiune.\nUrmătorul pas: revizuire și eventuală trimitere de către utilizator din EVA → Drafts.\nSursă: '+raw.relative_to(r).as_posix()+'\n\n'
def prepend(p,prefix=''):
 old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
 if marker in old:return
 preserve(p);p.write_text(prefix+note+'ISTORIC PĂSTRAT — instrucțiunea actuală privind destinatarii prevalează\n\n'+old,encoding='utf-8-sig')
for name in ['2026.10.14 Status proiect.txt','2026.10.14 Log progres proiect.txt']:prepend(r/name)
arc=r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
for name in ['Donau Versicherung','Maritczak - Commerz Inkasso','CERHA HEMPEL']:prepend(arc/'Parteneri'/f'2026.10.14 Log discutii - {name}.txt')
prepend(r/'folder map/README.md','# ');prepend(c/'2026.10.14 Jurnal actualizare.txt')
rp=arc/'2026.10.14 Registru comunicatii.json';preserve(rp);reg=json.loads(rp.read_text(encoding='utf-8-sig'))
entry={'data':'2026.10.14','subiect':marker,'status':'pending / NETRIMIS','eva_mail_draft_id':d['id'],'to':d['to'],'cc':[],'bcc':[],'email_trimis':False,'sursa':raw.relative_to(r).as_posix(),'urmatorul_pas':'Revizuire și eventuală trimitere de către utilizator.'}
if not any(x.get('subiect')==marker for x in reg.setdefault('actualizari_punctuale',[])):reg['actualizari_punctuale'].append(entry)
for e in reg.get('statusuri',[]):
 if e.get('partener')=='Donau Versicherung':e['draft_eva_mail_reauditat_2026_10_14']=entry
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf8')
mp=c/'2026.10.14 Manifest draft Eva-Mail Donau.json';preserve(mp)
files=[c/(s+x) for x in ['.txt','.json','.eml']]+[raw]
mp.write_text(json.dumps({'data':'2026.10.14','eva_mail_id':d['id'],'status':'pending / NETRIMIS','to':d['to'],'cc':[],'bcc':[],'files':[{'path':p.relative_to(r).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]},ensure_ascii=False,indent=2),encoding='utf8')
print('Draft și arhivă corectate: numai DONAU, CC/BCC goale, NETRIMIS.')
