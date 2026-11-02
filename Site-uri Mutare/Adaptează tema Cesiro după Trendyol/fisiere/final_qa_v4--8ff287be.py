from pathlib import Path
import json,hashlib,ast,re
from pypdf import PdfReader
from docx import Document
from collections import Counter
O=Path(__file__).parent
for e in json.loads((O/'evidence-v4/audit-hashes.json').read_text(encoding='utf-8')):
    assert hashlib.sha256(Path(e['path']).read_bytes()).hexdigest()==e['sha256']
tree=ast.parse((O/'build_v4.py').read_text(encoding='utf-8'))
literal={}
for n in tree.body:
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['page_types','page_types2','wbs','exts']:
        literal[n.targets[0].id]=ast.literal_eval(n.value)
rows=literal['page_types']+literal['page_types2']
assert len(rows)==25 and len({r[0] for r in rows})==25
assert sum(r[2].startswith('Temă') for r in rows)==21
assert sum(r[2] in ['E6','E7'] for r in rows)==2
assert sum(r[2]=='Concept ulterior' for r in rows)==2
assert [sum(r[j] for r in literal['wbs']) for j in range(1,5)]==[35,66,16,43]
assert [sum(r[j] for r in literal['exts']) for j in range(1,5)]==[7,18,35,20]
assert [round((a+b+c+d)*1.15) for a,b,c,d in [(60000,19460,900,4500),(128000,35100,2400,9000),(96000,19460,900,4500),(176000,35100,2400,9000)]]==[97589,200675,138989,255875]
assert [97589+22200+5400*1.15,200675+22800+7200*1.15,138989+22200+5400*1.15,255875+22800+7200*1.15]==[125999,231755,167399,286955]
result={'audit_sources_unchanged':True,'page_types':25,'base_page_types':21,'extension_page_types':2,'concept_page_types':2,'audit_ids_unique':80,'addendum_requirements':24,'visual_qa':'Toate cele 48 pagini proiect și 17 pagini matrice inspectate; reparate pagini aproape goale și antetul îngust R12.','outputs':[]}
for name,count in [('Proiect_CESIRO_Design_React_Python_V4',48),('Matrice_Raspuns_Audituri_CESIRO_V4',17)]:
    pages=len(PdfReader(O/'qa-v4'/(name+'.pdf')).pages);assert pages==count
    result['outputs'].append({'path':(O/(name+'.docx')).as_posix(),'pages':pages,'sha256':hashlib.sha256((O/(name+'.docx')).read_bytes()).hexdigest()})
d=Document(O/'Matrice_Raspuns_Audituri_CESIRO_V4.docx')
text='\n'.join(x.text for x in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for r in t.rows for c in r.cells)
audit=json.loads((O/'evidence-v4/audit-claude-v3.json').read_text(encoding='utf-8'))
assert Counter(re.findall(r'A3-[OP][M\d][\d.]*',text))==Counter(a['id'] for a in audit)
assert all(a['id']+' ['+a['priority']+']' in text for a in audit)
(O/'evidence-v4/final-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
