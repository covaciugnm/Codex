from pathlib import Path
import json, hashlib, re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((OUT/f'{DATE} Registru transfer preambul R08.json').read_text(encoding='utf-8'))
checks=[]
for item in reg['operatiuni']:
    src=json.loads((ROOT/item['R08_source']).read_text(encoding='utf-8'))
    old=json.loads((ROOT/item['R07_source']).read_text(encoding='utf-8'))
    assert sha(ROOT/item['R07_source'])==item['R07_sha256']
    for key in ['sections','annexes','signatures','presentation']:assert src[key]==old[key]
    assert src['preamble']==[]
    assert sha(ROOT/item['offer_original_copy'])==item['offer_sha256']
    pdf=ROOT/item['PDF_expected'];reader=PdfReader(pdf)
    pages=[p.extract_text() for p in reader.pages]
    text='\n'.join(pages)
    other='PECH' if item['provider']=='BERGER' else 'BERGER'
    for forbidden in ['Vorbemerk','Vertragsvorschlag','verhand',other]:assert forbidden.lower() not in text.lower(),forbidden
    metadata=str(reader.metadata)
    for forbidden in ['Vorbemerk','Vertragsvorschlag','verhand',other]:assert forbidden.lower() not in metadata.lower(),forbidden
    assert 'WERKVERTRAG' in pages[0] and 'Vertragsparteien und Vertretung' in pages[0]
    for prem in item['preamble_moved_verbatim']:assert prem not in text
    email=json.loads((ROOT/item['R08_email_source']).read_text(encoding='utf-8'))
    assert all(email['body_de'].count(p)==1 for p in item['preamble_moved_verbatim'])
    checks.append({'provider':item['provider'],'PDF_sha256':sha(pdf),'pagini':len(pages),'clauze_anexe_semnaturi_prezentare_R07_identice':True,'preambul_numai_in_email':True,'fara_referiri_externe_interzise':True,'metadate_verificate':True})
out=OUT/f'{DATE} Control integritate PDF R08.json'
assert not out.exists()
out.write_text(json.dumps({'data':DATE,'status':'PASS','controale':checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','PDF':checks},ensure_ascii=False))
