from pathlib import Path
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
import json, hashlib, re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent; DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')
registry=json.loads((OUT/f'{DATE} Registru EVA drafturi R08.json').read_text(encoding='utf-8'))
records=[]
for item in registry['drafturi']:
    provider=item['provider'];source=OUT/f'{DATE} Email {provider} R08 sursa.json'
    draft=json.loads(source.read_text(encoding='utf-8'))
    server=json.loads((ROOT/item['server_readback_path']).read_text(encoding='utf-8'))
    assert server['id']==item['draft_id'] and server['status']=='pending'
    assert server['account_email']==draft['from'] and server['to']==draft['to'] and server['cc']==draft['cc']
    assert server['subject']==draft['subject']
    body=server['body'];is_html=bool(re.search(r'<(?:p|div|br|html|body)\b',body,re.I))
    if is_html:
        soup=BeautifulSoup(body,'html.parser')
        for br in soup.find_all('br'):br.replace_with('\n')
        plain=soup.get_text('\n',strip=True)
    else:plain=body
    normalize=lambda s:' '.join(s.split())
    assert normalize(draft['body_de']) in normalize(plain)
    folder=(ROOT/item['server_readback_path']).parent
    draft['status']='DRAFT EVA / pending / NETRIMIS'
    draft['eva_mail_draft_id']=server['id'];draft['eva_mail_original_readback']=item['server_readback_path']
    draft['eva_mail_created_at_original']=server.get('created_at')
    draft['eva_mail_updated_at_original']=server.get('updated_at')
    draft['body_de_with_eva_signature_original']=body
    draft['attachments']=item['attachments']
    draft['attachment_instruction_ro']='Atașamente reale: contractul propriu R08 și oferta proprie originală Anlage 5. Draft EVA pending, netrimis.'
    eml=EmailMessage(policy=policy.SMTP)
    eml['From']=draft['from'];eml['To']=', '.join(draft['to'])
    if draft['cc']:eml['Cc']=', '.join(draft['cc'])
    eml['Subject']=draft['subject'];eml['X-Unsent']='1';eml['X-EVA-Draft-ID']=server['id'];eml['X-Created-Date-Local']=DATE
    eml.set_content(plain,charset='utf-8')
    if is_html:eml.add_alternative(body,subtype='html',charset='utf-8')
    for attach in item['attachments']:
        p=ROOT/attach['local_path'];assert sha(p)==attach['sha256']
        eml.add_attachment(p.read_bytes(),maintype='application',subtype='pdf',filename=p.name)
    target=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.eml'
    assert not target.exists();target.write_bytes(eml.as_bytes())
    reread=BytesParser(policy=policy.default).parsebytes(target.read_bytes())
    assert reread['X-Unsent']=='1' and reread['X-EVA-Draft-ID']==server['id']
    parts=list(reread.iter_attachments());assert len(parts)==2
    for part,att in zip(parts,item['attachments']):
        assert part.get_filename()==att['filename']
        assert hashlib.sha256(part.get_payload(decode=True)).hexdigest()==att['sha256']
    text_path=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.txt'
    fresh(text_path,f"{DATE} | DRAFT EVA — NETRIMIS / pending\nDe la: {draft['from']}\nCătre: {', '.join(draft['to'])}\nCC: {', '.join(draft['cc']) or '(fără CC)'}\nID Eva-Mail draft: {server['id']}\nSubiect: {draft['subject']}\nAtașamente PDF: {'; '.join(a['filename'] for a in item['attachments'])}\n\n{plain}\n")
    meta=folder/f'{DATE} Email {provider} Vertragsvorschlag NETRIMIS.json'
    fresh(meta,json.dumps(draft,ensure_ascii=False,indent=2)+'\n')
    records.append({'provider':provider,'draft_id':server['id'],'status':draft['status'],'EML':str(target.relative_to(ROOT)),'EML_sha256':sha(target),'TXT':str(text_path.relative_to(ROOT)),'JSON':str(meta.relative_to(ROOT)),'server_readback_path':item['server_readback_path'],'attachments':item['attachments'],'readback':'PASS'})
fresh(OUT/f'{DATE} Registru export emailuri EVA R08.json',json.dumps({'data':DATE,'drafturi':records,'drafturi_EVA_create':2,'mesaje_trimise':0,'semnaturi':0,'plati':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','drafturi_EVA_arhivate':2,'atasamente_reale_EML':4,'trimise':0},ensure_ascii=False))
