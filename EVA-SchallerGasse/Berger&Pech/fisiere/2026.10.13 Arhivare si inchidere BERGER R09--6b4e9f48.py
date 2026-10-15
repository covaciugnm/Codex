from pathlib import Path
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')
def rec(p):return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,d):assert not p.exists(),p;p.write_text(d,encoding='utf-8')
def prepend(p,s):p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
r=read(OUT/f'{DATE} Registru modificari BERGER R09.json');folder=ROOT/r['public_folder']
src=ROOT/r['source_R09'];pdf=ROOT/r['PDF_expected'];offer=ROOT/r['original_offer']
assert sha(src)==r['source_R09_sha256'] and sha(folder/src.name)==sha(src)
assert sha(ROOT/r['source_R08'])==r['source_R08_sha256'] and sha(offer)==r['original_offer_sha256']
qa=read(OUT/f'{DATE} QA text PDF BERGER R09.json');assert qa['text_status']=='PASS' and qa['source_sha256']==sha(src) and qa['pdf_sha256']==sha(pdf)
visual=OUT/f'{DATE} QA vizual BERGER R09.txt';assert visual.is_file()
assert (OUT/f'{DATE} Audit comercial final BERGER R09.txt').is_file()
e=read(OUT/f'{DATE} Registru EVA BERGER R09.json');serverpath=ROOT/e['server_readback_path'];server=read(serverpath)
mail=read(ROOT/r['email_source']);assert server['id']==r['draft_id'] and server['status']=='pending'
assert server['account_email']==mail['from'] and server['to']==mail['to'] and server['cc']==mail['cc'] and server['subject']==mail['subject']
assert server['body'].startswith(mail['body_de'].strip()) and server['body'].count('Cosmin Adrian Covaciu')==1
assert len(server['attachments'])==2
for a in e['attachments']:
    local=ROOT/a['local_path'];remote=next(x for x in server['attachments'] if x['id']==a['document_id'])
    assert sha(local)==a['sha256'] and remote['filename']==local.name and remote['size']==local.stat().st_size
assert read(OUT/f'{DATE} Verificare octeti PDF BERGER R09 EVA.json')['status']=='PASS'
# Freeze all PECH deliverables and email archives against R08's final registry.
oldreg=ROOT/f'00.Proiect/09. Vertraege/{DATE} Contracte R08 - intern/{DATE} Registru contracte emailuri R08 final.json'
old=read(oldreg);pechfiles=[]
for item in old['livrabile']:
    for key in ['pdf','sursa','oferta_originala']:
        p=ROOT/item[key]['cale'];assert sha(p)==item[key]['sha256']
        if item['provider']=='PECH':pechfiles.append(item[key])
for item in old['emailuri_arhivate_hashuri']:
    if '/zt-pech.at/' in item['cale']:assert sha(ROOT/item['cale'])==item['sha256'];pechfiles.append(item)
pechlive=read(OUT/f'{DATE} PECH verificare draft nemodificat original.json')
pechold=read(ROOT/'00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R08/2026.10.13 EVA draft PECH R08 original.json')
for key in ['id','status','to','cc','body','attachments','updated_at']:assert pechlive[key]==pechold[key]
mail['status']='DRAFT EVA pending / NETRIMIS; BERGER R09'
mail['eva_mail_draft_id']=server['id'];mail['eva_mail_created_at_original']=server['created_at'];mail['eva_mail_updated_at_original']=server['updated_at']
mail['body_de_with_eva_signature_original']=server['body'];mail['attachments']=e['attachments'];mail['eva_mail_original_readback']=e['server_readback_path']
eml=EmailMessage(policy=policy.SMTP);eml['From']=mail['from'];eml['To']=', '.join(mail['to'])
if mail['cc']:eml['Cc']=', '.join(mail['cc'])
eml['Subject']=mail['subject'];eml['X-Unsent']='1';eml['X-EVA-Draft-ID']=server['id'];eml['X-Created-Date-Local']=DATE
eml.set_content(server['body'],charset='utf-8')
for p in [pdf,offer]:eml.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=p.name)
emlpath=folder/f'{DATE} Email BERGER R09 NETRIMIS.eml';assert not emlpath.exists();emlpath.write_bytes(eml.as_bytes())
parsed=BytesParser(policy=policy.default).parsebytes(emlpath.read_bytes());assert parsed['X-Unsent']=='1' and parsed['X-EVA-Draft-ID']==server['id']
assert parsed.get_body(preferencelist=('plain',)).get_content().replace('\r\n','\n').strip()==server['body'].replace('\r\n','\n').strip()
parts=list(parsed.iter_attachments());assert len(parts)==2
for part,p in zip(parts,[pdf,offer]):assert part.get_filename()==p.name and hashlib.sha256(part.get_payload(decode=True)).hexdigest()==sha(p)
mailjson=folder/f'{DATE} Email BERGER R09 NETRIMIS.json';fresh(mailjson,json.dumps(mail,ensure_ascii=False,indent=2)+'\n')
mailtxt=folder/f'{DATE} Email BERGER R09 NETRIMIS.txt';fresh(mailtxt,f"{DATE} | DRAFT EVA pending / NETRIMIS\nDe la: {mail['from']}\nCătre: {', '.join(mail['to'])}\nCC: {', '.join(mail['cc']) or '(fără CC)'}\nID Eva-Mail draft: {server['id']}\nSubiect: {mail['subject']}\nAtașamente reale: {pdf.name}; {offer.name}\n\n{server['body']}\n")
registry=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json'
partner=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - Markus Berger.txt'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',partner,registry,ROOT/'folder map/README.md']
hist=OUT/f'{DATE} Istoric jurnale inainte R09';hist.mkdir(exist_ok=False);backup=[]
for p in targets:
    dest=hist/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}');shutil.copy2(p,dest);backup.append({'original':rel(p),'copie':rel(dest),'sha256':sha(dest)})
entry=f'''2026.10.13 | BERGER R09 — corecții explicite ale utilizatorului; PECH neatins
Status scurt: finalizată numai revizia BERGER. PDF numai germană/contract, 29 pagini. Baugrubensicherung/Verbau, Stützmauern și Außenanlagen bauseits ca în oferta originală; numai sarcinile propriei clădiri furnizate de AN. Fundațiile/subzidirile clădirii rămân în scopul contractat.
Statische Betreuung: 2.000 EUR net, maximum 8 vizite statice; o begehung T0 cu asistență statică efectivă consumă un loc. PI rămâne poziție separată de 10.000 EUR net, fără plafon numeric și fără pachete suplimentare pentru PI-only. Prezența comună se numără o singură dată și nu produce tarif PI/deplasare duplicat. Vizitele statice suplimentare: pachete distinct comandate de 4 / 1.000 EUR net, 1.200 EUR cu TVA20%; facturare după prestație, cu regulile legale de abbestellung păstrate.
Bază: 45.000 EUR net / 54.000 EUR cu TVA20%, cele patru poziții și regia originală nemodificate. Un pachet complet comandat/executat: total 46.000 net / 55.200 cu TVA; două: 47.000 net / 56.400 cu TVA. Nicio comandă sau majorare automată.
Comercial: facturi parțiale/avansuri după prestație, 14 zile calendaristice de la primirea facturii conforme, fără deduceri contractuale. Eliminat Haftrücklass 5%, garanția substitutivă AG, penalitatea contractuală și grila procentuală E1–E7. Păstrate cele trei adaosuri comerciale cerute: Gewährleistung 3 ani, fără indexare și Bauphasenrahmen 18 luni. Drepturile legale imperative rămân. Garanția 3 ani este pentru prestațiile proprii, nu pentru defectele istorice ale clădirii.
Valabilitate originală: 8 săptămâni din 2026.08.17 până în 2026.10.12; contractul nu resetează automat oferta. Confirmarea actuală a sumelor/valabilității înainte de semnare este prevăzută.
Email BERGER german foarte politicos actualizat în același draft EVA {server['id']}; status pending / NETRIMIS. Atașament R08 înlocuit numai cu PDF BERGER R09; oferta originală proprie păstrată. Citire înapoi, hash PDF încărcat/descărcat și EML cu atașamente reale verificate. Nicio trimitere, semnare sau plată.
Ultimul răspuns comercial real BERGER: 2026.08.17. Nu este scan general zilnic de mesaje noi. PECH: fișierele, PDF-ul, emailul și draftul R08 sunt verificate neschimbate; punctul transmis despre Pos.02 este amânat la cererea utilizatorului.
Următorul pas: lectura BERGER R09 și confirmarea utilizatorului; abia după confirmare se lucrează la PECH.
Surse: {rel(pdf)}; {rel(mailtxt)}; {rel(serverpath)}; {rel(OUT/f'{DATE} Registru BERGER R09 final.json')}.
'''
for p in targets[:3]:prepend(p,entry)
central=read(registry);count=len(central['comunicatii']);dcount=len(central['drafturi'])
pechcentral=copy_pech=json.loads(json.dumps([x for x in central['drafturi'] if x.get('id')==pechlive['id']]))
target=next(x for x in central['drafturi'] if x['id']==server['id'])
target.update({'data':DATE,'statut':'DRAFT EVA pending / NETRIMIS; BERGER R09','cale':rel(mailtxt),'original_EVA':rel(serverpath),'EML':rel(emlpath),'atasamente':e['attachments'],'actualizare':'Același draft; numai BERGER modificat, fără trimitere.'})
assert len(central['drafturi'])==dcount and [x for x in central['drafturi'] if x.get('id')==pechlive['id']]==pechcentral
central.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'BERGER_R09_corecturi_ofertei_conditii_originale','registru':rel(OUT/f'{DATE} Registru BERGER R09 final.json'),'draft_id':server['id'],'status':'pending / NETRIMIS','drafturi_actualizate':1,'drafturi_create':0,'mesaje_noi':0,'mesaje_trimise':0,'PECH_nemodificat':True,'PECH_asteapta_confirmare':True})
assert len(central['comunicatii'])==count;registry.write_text(json.dumps(central,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[4],f"# {DATE} — BERGER R09 finalizat; PECH așteaptă confirmarea\n\nPunct curent BERGER: ../{rel(pdf)} și ../{rel(mailtxt)}. PDF numai contract, fără introducere. Bază 45.000 EUR net, maximum8 vizite statice; PI10.000 separat fără plafon numeric. Verbau/Baugrubensicherung bauseits. Vizite statice suplimentare în pachete de4/1.000 EUR net, numai comandate. Facturare originală după prestație,14 zile fără rețineri; fără grilă procentuală/retention/penalitate. Adaosuri comerciale păstrate:3ani Gewährleistung,noindex,18luni B0. Valabilitatea originală8săptămâni necesită reconfirmare actuală, fără reset automat.\n\nAcelași draft EVA BERGER{server['id']} actualizat, pending / NETRIMIS; numai contractul BERGER R09 și oferta sa originală atașate. R08 rămâne istoric. PECH PDF/email/draft R08 nemodificate; modificarea Pos.02 este amânată până la confirmarea utilizatorului privind închiderea BERGER.\n\nRegistru intern: ../{rel(OUT/f'{DATE} Registru BERGER R09 final.json')}. Jurnale și index actualizate; fără mesaje trimise, semnături sau plăți.")
audits=[rec(p) for p in sorted(set(OUT.glob(f'{DATE} Audit*.txt'))|set(OUT.glob(f'{DATE} Adendum audit*.txt')))]
final={'data':DATE,'status':'BERGER R09 finalizat; draft pending / NETRIMIS; PECH nemodificat și amânat','pdf':{**rec(pdf),'pagini':29},'source':rec(src),'original_offer':rec(offer),'changes':rec(OUT/f'{DATE} Registru modificari BERGER R09.json'),'qa_text':rec(OUT/f'{DATE} QA text PDF BERGER R09.json'),'qa_visual':rec(visual),'audits':audits,'email_files':[rec(p) for p in [emlpath,mailjson,mailtxt,serverpath]],'eva':e,'pdf_bytes_EVA':rec(OUT/f'{DATE} Verificare octeti PDF BERGER R09 EVA.json'),'PECH_files_frozen_verified':pechfiles,'PECH_EVA_unchanged':rec(OUT/f'{DATE} PECH verificare draft nemodificat original.json'),'history_R08':rec(oldreg),'journal_backups':backup,'journals_updated':[rec(p) for p in targets],'drafts_updated':1,'drafts_created':0,'sent':0,'signatures':0,'payments':0,'next':'Așteaptă confirmarea utilizatorului pentru a începe PECH.'}
fresh(OUT/f'{DATE} Registru BERGER R09 final.json',json.dumps(final,ensure_ascii=False,indent=2)+'\n')
fresh(OUT/f'{DATE} Jurnal actualizare BERGER R09.txt',entry)
print(json.dumps({'status':'PASS','BERGER_only':True,'PECH_frozen_files':len(pechfiles),'draft_updated':server['id'],'messages_unchanged':count,'sent':0},ensure_ascii=False))
