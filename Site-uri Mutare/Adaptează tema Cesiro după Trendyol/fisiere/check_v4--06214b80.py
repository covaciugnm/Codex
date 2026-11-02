from pathlib import Path
from pypdf import PdfReader
from docx import Document
from collections import Counter
from PIL import Image,ImageOps,ImageDraw
import json,re,hashlib
O=Path(__file__).parent
audit=json.loads((O/'evidence-v4/audit-claude-v3.json').read_text(encoding='utf-8'))
for stem,prefix in [('Proiect_CESIRO_Design_React_Python_V4','proiect'),('Matrice_Raspuns_Audituri_CESIRO_V4','matrice')]:
    d=Document(O/(stem+'.docx'))
    txt='\n'.join(e.text for e in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for r in t.rows for c in r.cells)
    if prefix=='matrice':
        ids=re.findall(r'A3-[OP][M\d][\d.]*',txt)
        assert Counter(ids)==Counter(a['id'] for a in audit),(Counter(ids),len(ids))
        for a in audit: assert a['id']+' ['+a['priority']+']' in txt
    else:
        for forbidden in ['Next.js','revalidateTag','Suspense','cloaking','Neincluse în bugetul temei']:
            assert forbidden not in txt,forbidden
        assert len(d.inline_shapes)==9,len(d.inline_shapes)
    pdf=PdfReader(O/'qa-v4'/(stem+'.pdf'))
    print(stem,len(pdf.pages),'pagini')
    for i,pg in enumerate(pdf.pages,1):
        content=pg.extract_text() or ''
        print(i,len(content),repr(content[:85].replace('\n',' ')))
    imgs=sorted((O/'qa-v4/final').glob(prefix+'-*.png'))
    assert len(imgs)==len(pdf.pages)
    for start in range(0,len(imgs),4):
        canvas=Image.new('RGB',(1280,1850),'#e3e5e8')
        for j,path in enumerate(imgs[start:start+4]):
            im=Image.open(path).convert('RGB');im.thumbnail((620,875))
            x=(j%2)*640+10;y=(j//2)*925+30
            canvas.paste(im,(x,y));ImageDraw.Draw(canvas).text((x,y-20),path.stem,fill='black')
        canvas.save(O/'qa-v4/final'/f'contact-{prefix}-{start//4+1:02}.png')
    (O/'qa-v4'/(prefix+'-text.txt')).write_text(txt,encoding='utf-8')
print('Validări structurale trecute')
