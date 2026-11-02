from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
import json
B=Path(__file__).parent;prs=json.loads((B/'projects.json').read_text(encoding='utf-8'));rs=json.loads((B/'records.json').read_text(encoding='utf-8'));jobs=json.loads((B/'jobs.json').read_text(encoding='utf-8'))
for pr in prs:
 d=Document();s=d.sections[0];s.top_margin=Cm(1.8);s.bottom_margin=Cm(1.8);s.left_margin=Cm(1.8);s.right_margin=Cm(1.8);s.page_width=Cm(21);s.page_height=Cm(29.7)
 d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(9)
 d.add_paragraph('Opis de lucru al dosarului de participare','Title');d.add_paragraph(pr['title']+'\nAnunț nr.'+pr['num']+'/16.10.2026 | Asociația Romanian Soul Entity | CIF29433614')
 d.add_paragraph('Acest opis este pentru finalizarea dosarului. Nu certifică existența documentelor lipsă. Se completează cu paginile dosarului final după validare, semnare și scanare. Referințele oficiale și variantele istorice nu se transmit automat.')
 table=d.add_table(rows=1,cols=4);table.style='Table Grid'
 for c,t in zip(table.rows[0].cells,['ID','Document','Stare','Pagini finale']):c.text=t
 selected=[r for r in rs if r['project']==pr['id'] and r['folder']!=0 and r['required'] not in ['Arhivă','Referință','Dosar suport consolidat','Document de lucru'] and r['status'] not in ['Sursa CV','Arhivat de reinnoit'] and not r['title'].startswith('Dovadă experiență') and not r['title'].startswith('Diplome și certificate')]
 for r in sorted(selected,key=lambda r:(r['folder'],r['id'])):
  for c,v in zip(table.add_row().cells,[r['id'],r['title'],r['status'],'[de completat]']):c.text=v
 d.add_paragraph('Data prevăzută pentru finalizare:02.11.2026\nSzoke Andrei-Alexandru – președinte\nSemnătura și ștampila: ____________________')
 target=Path(pr['out'])/'17 Opis si numerotare'/'Word pentru semnare'/'17_Opis_DE_FINALIZAT.docx';target.parent.mkdir(exist_ok=True);d.save(target)
 jobs.append(dict(docx=str(target),pdf=str(target.parent.parent/'PDF pentru semnare'/'17_Opis_DE_FINALIZAT.pdf'),project=pr['id']))
 rs.append(dict(project=pr['id'],folder=17,title='Opis de lucru al dosarului',status='De finalizat',source='Registrul documentelor și cerințele anunțului',dest=str(target),obs='Paginile finale se stabilesc după semnare și scanare; lipsurile nu sunt declarate prezente.',owner='ROSE',signer='Szoke Andrei-Alexandru',required='Obligatoriu',action='Selectați documentele valide, închideți lipsurile, numerotați și completați paginile.',due='2026-11-02T16:00:00',email_due='2026-11-03T00:00:00',id=f"P{pr['id']}-119"))
(B/'records.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8');(B/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Opis create 2')
