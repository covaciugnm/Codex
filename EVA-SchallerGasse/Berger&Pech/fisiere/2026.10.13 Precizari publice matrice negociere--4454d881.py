from pathlib import Path
import json,hashlib,shutil
from docx import Document
ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
OUT=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH'
DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
source=WORK/f'{DATE} Cerinte comune negociere matrice.json'
assert sha(source)=='73b45b4c8a18908f6f30bcea9400a4506de02de3719ede324750ca6afe76aa0f'
matrix=read(source);items={x['id']:x for x in matrix['matrice']}
docx=OUT/f'{DATE} Matrice explicita cerinte comune BERGER PECH.docx'
pdf=docx.with_suffix('.pdf')
manifest=OUT/f'{DATE} Export baza negociere pentru verificare.json'
history=OUT/f'{DATE} Istoric matrice negociere export initial'
assert not history.exists();history.mkdir()
backups=[]
for p in [docx,pdf,manifest]:
    q=history/p.name;shutil.copy2(p,q);assert sha(p)==sha(q)
    backups.append({'cale':p.relative_to(ROOT).as_posix(),'copie':q.relative_to(ROOT).as_posix(),'sha256':sha(p)})
d=Document(docx);changed=[]
for table in d.tables:
    for row in table.rows:
        if len(row.cells)==5:
            for key in ['N034','N036']:
                if row.cells[0].text.startswith(key):
                    p=row.cells[4].paragraphs[0]
                    assert len(p.runs)==1
                    old=p.text;p.runs[0].text=items[key]['celule_publice']['diferenta_pozitie']
                    changed.append({'criteriu':key,'inainte':old,'dupa':p.text})
assert len(changed)==2
spacing=[('necesară:450','necesară: 450'),('Pentru6','Pentru 6'),('este1.000','este 1.000'),('nu1.000,02','nu 1.000,02'),
         ('teren100','teren 100'),('asistență20/','asistență 20/'),('final100','final 100')]
spacing_count=0
for table in d.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    for before,after in spacing:
                        spacing_count+=r.text.count(before);r.text=r.text.replace(before,after)
d.save(docx)
current=read(manifest)
for r in current['surse']:
    if r['cale'].endswith(source.name):r['sha256']=sha(source)
current['precizari_publice']='N034/N036 aliniate pozițiilor comune D01/D02; spații editoriale; metadate interne corectate separat'
manifest.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert pdf.resolve().is_relative_to(ROOT.resolve()) and pdf.name==f'{DATE} Matrice explicita cerinte comune BERGER PECH.pdf'
assert sha(pdf)==sha(history/pdf.name)
pdf.unlink()  # PDF nou intermediar, cu copie verificată; reexport readonly imediat.
for r in read(WORK/f'{DATE} Surse inghetate audit R05.json')['surse']:assert sha(ROOT/r['cale'])==r['sha256']
result={'data':DATE,'copii':backups,'modificari_publice':changed,'spatii_corectate':spacing_count,'sursa_json':sha(source),'docx_nou':sha(docx)}
(OUT/f'{DATE} Istoric precizari publice matrice.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'statut':'PASS','criterii_delta':len(changed),'spatii':spacing_count,'docx':sha(docx)},ensure_ascii=False))
