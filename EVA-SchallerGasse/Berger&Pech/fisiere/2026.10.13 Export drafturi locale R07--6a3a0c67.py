from pathlib import Path
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
import json, hashlib

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')
records=[]
for provider,domain,offer_date in [('BERGER','bmberger.at','2026.08.17'),('PECH','zt-pech.at','2026.09.17')]:
    source=WORK/f'{DATE} Email {provider} Unser Vertragsvorschlag DRAFT LOCAL.json'
    draft=json.loads(source.read_text(encoding='utf-8'))
    folder=ROOT/f'00.Proiect/09. Vertraege/{domain}/{DATE} Vertragsvorschlag R07'
    pdf=folder/f'{DATE} Werkvertrag {provider} R07.pdf'
    offer=folder/f'{DATE} Anlage 5 Originalangebot {provider} {offer_date}.pdf'
    assert pdf.is_file() and offer.is_file()
    evidence=ROOT/draft['recipient_evidence']['source_mail']
    assert sha(evidence)==draft['recipient_evidence']['sha256']
    # Editorial address spacing only; no price or negotiation text is added.
    draft['subject']='Schallergasse 35 - Unser Vertragsvorschlag'
    draft['attachments']=[{'filename':p.name,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in [pdf,offer]]
    draft['attachment_instruction_ro']='Două atașamente reale: numai propunerea R07 a acestui destinatar și oferta sa originală Anlage 5. Nu include audituri sau documentele altui furnizor.'
    draft['status']='DRAFT LOCAL / NETRIMIS; NU ESTE DRAFT CREAT IN EVA'
    draft['eva_mail_draft_id']=None
    other='PECH' if provider=='BERGER' else 'BERGER'
    assert other.lower() not in (draft['body_de']+' '+draft['subject']).lower()
    assert 'verhand' not in draft['body_de'].lower()
    eml=EmailMessage(policy=policy.SMTP)
    eml['From']=draft['from'];eml['To']=', '.join(draft['to'])
    if draft['cc']:eml['Cc']=', '.join(draft['cc'])
    eml['Subject']=draft['subject'];eml['X-Unsent']='1';eml['X-Created-Date-Local']=DATE
    eml.set_content(draft['body_de'],charset='utf-8')
    for p in [pdf,offer]:eml.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=p.name)
    target=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.eml'
    assert not target.exists();target.write_bytes(eml.as_bytes())
    reread=BytesParser(policy=policy.default).parsebytes(target.read_bytes())
    assert reread['X-Unsent']=='1' and str(reread['Subject'])==draft['subject']
    decoded_body=reread.get_body(preferencelist=('plain',)).get_content()
    assert decoded_body.replace('\r\n','\n').strip()==draft['body_de'].replace('\r\n','\n').strip()
    attachments=list(reread.iter_attachments());assert len(attachments)==2
    for part,p in zip(attachments,[pdf,offer]):
        assert part.get_filename()==p.name
        assert hashlib.sha256(part.get_payload(decode=True)).hexdigest()==sha(p)
    text_path=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.txt'
    fresh(text_path,f'''2026.10.13 | DRAFT LOCAL — NETRIMIS
De la: {draft['from']}
Către: {', '.join(draft['to'])}
CC: {', '.join(draft['cc']) or '(fără CC)'}
ID Eva-Mail draft: nu există; draft local, nu creat în EVA
Subiect: {draft['subject']}
Atașamente reale în EML: {pdf.name}; {offer.name}

{draft['body_de']}''')
    meta=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.json'
    fresh(meta,json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
    records.append({'provider':provider,'EML':str(target.relative_to(ROOT)),'EML_sha256':sha(target),'TXT':str(text_path.relative_to(ROOT)),'JSON':str(meta.relative_to(ROOT)),'status':draft['status'],'from':draft['from'],'to':draft['to'],'cc':draft['cc'],'subject':draft['subject'],'attachments':draft['attachments'],'readback':'PASS'})
fresh(OUT/f'{DATE} Registru drafturi locale R07.json',json.dumps({'data':DATE,'drafturi':records,'mesaje_trimise':0,'drafturi_EVA_create':0,'semnaturi':0,'plati':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','drafturi_locale':len(records),'atasamente_reale_verificate':4,'EVA_create':0,'trimise':0},ensure_ascii=False))
