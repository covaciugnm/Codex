from pathlib import Path
import json,hashlib,shutil
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')
def rec(p):return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')
def prepend(p,s):p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
before=read(OUT/f'{DATE} EVA BERGER inainte calendar original.json');after=read(OUT/f'{DATE} EVA BERGER calendar readback original.json');src=read(OUT/f'{DATE} Email BERGER calendar sursa.json')
norm=lambda x:' '.join(x.split())
assert after['id']==before['id'] and after['status']=='pending' and norm(after['body']).startswith(norm(src['body_de']))
for key in ['account_email','to','cc','bcc','subject','attachments']:assert after[key]==before[key]
assert after['body'].count('Cosmin Adrian Covaciu')==1
assert 'Leistungs- und Rechnungsplan' in after['body'] and 'Vertragsanlage' in after['body']
assert 'EUR 45.000,00 netto' in after['body'] and 'EUR 54.000,00 brutto' in after['body']
public=ROOT/'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09'
oldmeta=read(public/f'{DATE} Email BERGER R09 NETRIMIS.json')
oldfinal=read(ROOT/'00.Proiect/09. Vertraege/2026.10.13 BERGER R09 - intern/2026.10.13 Registru BERGER R09 final.json')
for key in ['pdf','source','original_offer']:assert sha(ROOT/oldfinal[key]['cale'])==oldfinal[key]['sha256']
for f in oldfinal['PECH_files_frozen_verified']:assert sha(ROOT/f['cale'])==f['sha256']
meta=dict(oldmeta);meta.update({'status':'DRAFT EVA pending / NETRIMIS; cerere calendar facturare','body_de':src['body_de'],'body_de_with_eva_signature_original':after['body'],'eva_mail_original_readback':rel(OUT/f'{DATE} EVA BERGER calendar readback original.json'),'eva_mail_updated_at_original':after['updated_at'],'calendar_received':False,'calendar_agreed':False,'calendar_annex_attached':False})
eml=EmailMessage(policy=policy.SMTP);eml['From']=after['account_email'];eml['To']=', '.join(after['to'])
if after['cc']:eml['Cc']=', '.join(after['cc'])
eml['Subject']=after['subject'];eml['X-Unsent']='1';eml['X-EVA-Draft-ID']=after['id'];eml['X-Created-Date-Local']=DATE
eml.set_content(after['body'],charset='utf-8')
for att in oldmeta['attachments']:
    p=ROOT/att['local_path'];assert sha(p)==att['sha256']
    remote=next(a for a in after['attachments'] if a['id']==att['document_id'])
    assert remote['filename']==p.name and remote['size']==p.stat().st_size
    eml.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=p.name)
emlpath=public/f'{DATE} Email BERGER calendar facturare NETRIMIS.eml';assert not emlpath.exists();emlpath.write_bytes(eml.as_bytes())
parsed=BytesParser(policy=policy.default).parsebytes(emlpath.read_bytes());assert parsed['X-Unsent']=='1'
assert norm(parsed.get_body(preferencelist=('plain',)).get_content())==norm(after['body'])
parts=list(parsed.iter_attachments());assert len(parts)==2
for part,att in zip(parts,oldmeta['attachments']):assert hashlib.sha256(part.get_payload(decode=True)).hexdigest()==att['sha256']
txt=public/f'{DATE} Email BERGER calendar facturare NETRIMIS.txt'
fresh(txt,f"{DATE} | DRAFT EVA pending / NETRIMIS\nDe la: {after['account_email']}\nCătre: {', '.join(after['to'])}\nCC: {', '.join(after['cc']) or '(fără CC)'}\nID Eva-Mail draft: {after['id']}\nSubiect: {after['subject']}\nAtașamente: contract BERGER R09 și oferta originală, neschimbate. Calendarul este solicitat în draft; nu este primit/agreat/anexat.\n\n{after['body']}\n")
js=public/f'{DATE} Email BERGER calendar facturare NETRIMIS.json';fresh(js,json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
registry=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.13 Registru comunicatii.json'
partner=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - Markus Berger.txt'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',partner,registry,ROOT/'folder map/README.md']
hist=OUT/f'{DATE} Istoric jurnale inainte calendar';hist.mkdir(exist_ok=False);backups=[]
for p in targets:
    dest=hist/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}');shutil.copy2(p,dest);backups.append(rec(dest))
entry=f'''2026.10.13 | BERGER — cerere calendar de facturare cu valori în email
Status scurt: același draft EVA {after['id']} actualizat numai în corp, pending / NETRIMIS. Solicită înainte de semnare un Leistungs- und Rechnungsplan de agreat împreună și semnat ca anexă contractuală; nu există calendar primit sau deja agreat/anexat.
Pentru fiecare etapă: poziție de onorariu, prestație/livrabile, rezultat obiectiv facturabil, dată/termen relativ T0/B0, sumă netă, TVA, brut, cumul și sold rămas. Calendarul singur nu declanșează plata pentru prestații neefectuate; termenul de 14 zile după factura conformă rămâne.
Valorile originale sunt incluse expres: 13.000 statik + 20.000 planuri + 2.000 asistență statică + 10.000 PI = 45.000 EUR net, TVA20%9.000, total54.000 EUR. Împărțirea pe etape trebuie propusă de BERGER și să reconcilieze fiecare poziție/total, fără dublare. Nu au fost inventate sume intermediare sau procente de livrare. Pachetele suplimentare4/1.000 EUR net se arată separat numai dacă sunt comandate.
Contractul BERGER R09, PDF-ul, oferta și cele două atașamente EVA rămân neschimbate. PECH și documentele/emailurile sale sunt neatinse. Copii istorice ale emailului anterior păstrate; TXT/JSON/EML curente și readback original salvate, EML are cele două PDF-uri reale și X-Unsent1.
Ultimul răspuns comercial real BERGER:2026.08.17; această etapă nu este o solicitare deja trimisă sau o verificare zilnică de noi mesaje.
Următorul pas: lectura draftului, apoi trimiterea de utilizator și obținerea/agrearea calendarului înainte de semnare. Nicio trimitere, semnare sau plată.
Surse: {rel(txt)}; {rel(OUT/f'{DATE} EVA BERGER calendar readback original.json')}.
'''
for p in targets[:3]:prepend(p,entry)
central=read(registry);count=len(central['comunicatii']);dcount=len(central['drafturi']);pech=[d.copy() for d in central['drafturi'] if d.get('id')=='8e954def-ac5f-4782-b5c7-b25c64572bb9']
d=next(d for d in central['drafturi'] if d['id']==after['id'])
d.update({'statut':'DRAFT EVA pending / NETRIMIS; BERGER cerere calendar facturare','cale':rel(txt),'EML':rel(emlpath),'original_EVA':rel(OUT/f'{DATE} EVA BERGER calendar readback original.json'),'actualizare':'Numai corpul emailului: cerere calendar cu sume, viitoare anexă; contractul/atașamentele R09 neschimbate.'})
assert len(central['comunicatii'])==count and len(central['drafturi'])==dcount and [d for d in central['drafturi'] if d.get('id')=='8e954def-ac5f-4782-b5c7-b25c64572bb9']==pech
central.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'BERGER_calendar_facturare_cu_sume_cerut_in_draft','draft_id':after['id'],'status':'pending / NETRIMIS','calendar_received':False,'calendar_agreed':False,'calendar_annex_attached':False,'contract_R09_unchanged':True,'drafts_updated':1,'drafts_created':0,'sent':0,'PECH_unchanged':True,'registru':rel(OUT/f'{DATE} Registru actualizare email BERGER calendar.json')})
registry.write_text(json.dumps(central,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[4],f"# {DATE} — Email BERGER: calendar de facturare cu valori\n\nEmail curent: ../{rel(txt)}. Același draft EVA BERGER {after['id']} pending / NETRIMIS solicită un Leistungs- und Rechnungsplan agreat și semnat ca anexă înainte de semnare. Etape/livrabile/rezultate facturabile/date și sume nete/TVA/brute, cumul/sold; baza45.000 EUR net54.000 brut și cele patru poziții păstrate. Fără sume intermediare inventate, fără plăți declanșate numai de calendar. Calendarul nu este încă primit/agreat/anexat.\n\nContractul BERGER R09 și atașamentele rămân neschimbate; PECH neatins. Registru intern: ../{rel(OUT/f'{DATE} Registru actualizare email BERGER calendar.json')}. Istoricul este păstrat; nicio trimitere, semnare sau plată.")
final={'data':DATE,'status':'DRAFT EVA pending / NETRIMIS','draft_id':after['id'],'email_files':[rec(p) for p in [txt,js,emlpath]],'original_EVA':rec(OUT/f'{DATE} EVA BERGER calendar readback original.json'),'calendar_request_source':rec(OUT/f'{DATE} Email BERGER calendar sursa.json'),'contracts_unchanged':[oldfinal[k] for k in ['pdf','source','original_offer']],'PECH_files_unchanged':oldfinal['PECH_files_frozen_verified'],'attachments_unchanged':after['attachments'],'journal_backups':backups,'journals_updated':[rec(p) for p in targets],'calendar_received':False,'calendar_agreed':False,'calendar_annex_attached':False,'messages_unchanged':count,'drafts_created':0,'sent':0,'signatures':0,'payments':0,'readback':'PASS; EVA inserted blank line after list, wording identical after whitespace normalization'}
fresh(OUT/f'{DATE} Registru actualizare email BERGER calendar.json',json.dumps(final,ensure_ascii=False,indent=2)+'\n')
fresh(OUT/f'{DATE} Jurnal actualizare email BERGER calendar.txt',entry)
print(json.dumps({'status':'PASS','draft_id':after['id'],'email_only':True,'contracts_and_PECH_unchanged':True,'calendar_requested_not_received':True,'messages_unchanged':count,'sent':0},ensure_ascii=False))
