from pathlib import Path
from copy import deepcopy
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
OLD=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Propuneri contract R07 - intern'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
records=[]
expected={'BERGER':'f7fba9da1f4936ccbdedfceb19d47f8a4dc608c85cba8b670db701077af927f8','PECH':'f94de0baea202d865914490f1854ad980dbd97fe2c4df26ebb0c930dbe0e81c9'}
for firm,domain,offer_date in [('BERGER','bmberger.at','2026.08.17'),('PECH','zt-pech.at','2026.09.17')]:
    source=OLD/f'{DATE} Werkvertrag {firm} R07.json';assert sha(source)==expected[firm]
    original=read(source);contract=deepcopy(original)
    contract['preamble']=[];contract['title']='WERKVERTRAG';contract['version']='R08 Werkvertrag'
    for key in ['sections','annexes','signatures','presentation']:assert contract[key]==original[key]
    assert len(contract['sections'])==16 and len(contract['annexes'])==6
    target=OUT/f'{DATE} Werkvertrag {firm} R08.json';fresh(target,contract)
    folder=ROOT/f'00.Proiect/09. Vertraege/{domain}/{DATE} Werkvertrag R08';folder.mkdir(exist_ok=False)
    shutil.copy2(target,folder/target.name);assert sha(folder/target.name)==sha(target)
    oldfolder=ROOT/f'00.Proiect/09. Vertraege/{domain}/{DATE} Vertragsvorschlag R07'
    oldmail=oldfolder/f'{DATE} Email {firm} Vertragsvorschlag NETRIMIS.json'
    mail=read(oldmail);old_body=mail['body_de'];parts=old_body.strip().split('\n\n')
    assert len(parts)==5 and 'Bitte prüfen' in parts[1]
    opening,review=parts[1].split(' Bitte prüfen',1)
    body='\n\n'.join([parts[0],opening,*original['preamble'],'Bitte prüfen'+review,*parts[2:]])+'\n'
    for v in original['preamble']:assert v in body
    other='PECH' if firm=='BERGER' else 'BERGER';assert other.lower() not in body.lower()
    mail['body_de']=body;mail['attachments']=[];mail['status']='DRAFT LOCAL / NETRIMIS; NU ESTE DRAFT CREAT IN EVA'
    mail['attachment_instruction_ro']='Contractul R08 fără preambul și oferta proprie originală Anlage5; trei paragrafe introductive transferate integral în corpul emailului.'
    assert mail['eva_mail_draft_id'] is None
    mail_target=OUT/f'{DATE} Email {firm} R08 sursa.json';fresh(mail_target,mail)
    offer_name=f'{DATE} Anlage 5 Originalangebot {firm} {offer_date}.pdf'
    offer=oldfolder/offer_name;dest=folder/offer_name;shutil.copy2(offer,dest);assert sha(offer)==sha(dest)
    records.append({'provider':firm,'domain':domain,'R07_source':str(source.relative_to(ROOT)),'R07_sha256':sha(source),'R07_email':str(oldmail.relative_to(ROOT)),'R07_email_sha256':sha(oldmail),'R08_source':str(target.relative_to(ROOT)),'R08_sha256':sha(target),'R08_email_source':str(mail_target.relative_to(ROOT)),'R08_email_sha256':sha(mail_target),'public_folder':str(folder.relative_to(ROOT)),'PDF_expected':str((folder/f'{DATE} Werkvertrag {firm} R08.pdf').relative_to(ROOT)),'offer_original_copy':str(dest.relative_to(ROOT)),'offer_sha256':sha(dest),'preamble_moved_verbatim':original['preamble'],'operative_content_identical':True,'prices_identical':True})
fresh(OUT/f'{DATE} Registru transfer preambul R08.json',{'data':DATE,'operatiuni':records,'scope':'Only move 3 preamble paragraphs to own cover email and remove introductory PDF presentation; operative contract unchanged','trimiteri':0,'semnaturi':0,'plati':0})
print(json.dumps([{'provider':r['provider'],'contract_sha256':r['R08_sha256'],'email_sha256':r['R08_email_sha256'],'paragraphs_moved':3,'sections_annexes_identical':True} for r in records],ensure_ascii=False))
