from pathlib import Path
import json,hashlib,shutil
from docx import Document
ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
OUT=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH'
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
source=WORK/f'{DATE} Obiectii negociere reformulate.json'
assert 'N07' not in read(source)['puncte_negociere'][1]['negociabil_economic']
assert 'P07' in read(source)['puncte_negociere'][1]['negociabil_economic']
docx=OUT/f'{DATE} Obiectii reformulate si pozitii comune negociere.docx'
pdf=docx.with_suffix('.pdf')
manifest=OUT/f'{DATE} Export obiectii negociere pentru verificare.json'
dest=OUT/source.name
old=read(manifest)
assert sha(dest)==old['sursa_json_sha256'] and sha(docx)==old['docx_sha256']
history=OUT/f'{DATE} Istoric obiectii negociere N01.2'
assert not history.exists();history.mkdir()
backups=[]
for p in [docx,pdf,manifest,dest]:
    q=history/p.name;shutil.copy2(p,q);assert sha(p)==sha(q)
    backups.append({'original':p.relative_to(ROOT).as_posix(),'copie':q.relative_to(ROOT).as_posix(),'sha256':sha(p)})
d=Document(docx)
paragraphs=list(d.paragraphs)+[p for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs]
count=0
before='\n'.join(p.text for p in paragraphs)
for p in paragraphs:
    for r in p.runs:
        count+=r.text.count('N07');r.text=r.text.replace('N07','P07')
assert count==1,count
assert '\n'.join(p.text for p in paragraphs)==before.replace('N07','P07')
d.save(docx)
shutil.copy2(source,dest)
old['sursa_json_sha256']=sha(source);old['docx_sha256']=sha(docx);old['versiune_editoriala']='N01.3, N07 corectat la P07; fără altă modificare'
manifest.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert pdf.resolve().is_relative_to(ROOT.resolve()) and pdf.name==f'{DATE} Obiectii reformulate si pozitii comune negociere.pdf'
assert sha(pdf)==sha(history/pdf.name)
pdf.unlink()  # Doar PDF-ul nou, cu copie verificată; urmează exportul Word readonly.
(OUT/f'{DATE} Istoric corectie editoriala N01.3.json').write_text(json.dumps({'data':DATE,'modificare':'O singură trimitere N07→P07 în noul raport','copii':backups,'sursa_noua':sha(dest),'docx_nou':sha(docx)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in read(WORK/f'{DATE} Surse inghetate audit R05.json')['surse']:assert sha(ROOT/r['cale'])==r['sha256']
print(json.dumps(old,ensure_ascii=False))
