from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json,csv,shutil,re
B=Path(__file__).parent;prs=json.loads((B/'projects.json').read_text(encoding='utf-8'));rs=json.loads((B/'records.json').read_text(encoding='utf-8'));jobs=json.loads((B/'jobs.json').read_text(encoding='utf-8'))
rs=[r for r in rs if r['title'] not in ['Raport de audit independent și checklist','Checklist corecturi audit']]
jobs=[j for j in jobs if Path(j['docx']).name!='Raport_audit_si_checklist.docx']
report=B/'auditor'/'Raport_audit_final.txt';check=B/'auditor'/'Checklist_audit_final.csv'
text=report.read_text(encoding='utf-8-sig');checkrows=list(csv.DictReader(check.open(encoding='utf-8-sig',newline='')))
for pr in prs:
 out=Path(pr['out'])/'19 Audit si corecturi';copytxt=out/'Raport_audit_independent.txt';copycsv=out/'Checklist_corecturi_final.csv';shutil.copy2(report,copytxt);shutil.copy2(check,copycsv)
 d=Document();sec=d.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=Cm(1.8);sec.bottom_margin=Cm(1.8);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
 d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(10);d.styles['Normal'].paragraph_format.space_after=Pt(5)
 p=d.add_paragraph('Raport de audit independent și checklist','Title');p.paragraph_format.space_after=Pt(8)
 ppr=p._p.get_or_add_pPr();border=OxmlElement('w:pBdr');bottom=OxmlElement('w:bottom');bottom.set(qn('w:val'),'nil');border.append(bottom);ppr.append(border)
 for run in p.runs:run.font.name='Arial';run.font.size=Pt(15);run.font.color.rgb=RGBColor(0,0,0)
 d.add_paragraph(pr['title']+'\nAnunț nr. '+pr['num']+'/16.10.2026\nVerificare documentară la 01.11.2026')
 d.add_paragraph('Raportul auditorului este reprodus mai jos. Nota privind organizarea nu înlocuiește documentele lipsă și nu declară dosarul complet pentru depunere.')
 for line in text.splitlines():
  if not line.strip():continue
  p=d.add_paragraph(line)
  if len(line)<100 and (line.isupper() or re.match(r'^\d+\.\s',line) or line.startswith('Scor') or line.startswith('Concluzie')):
   p.runs[0].bold=True;p.paragraph_format.keep_with_next=True
 d.add_page_break();d.add_paragraph('Checklistul corecturilor','Heading 1')
 for row in checkrows:
  values=list(row.values());p=d.add_paragraph(' | '.join(str(x or '') for x in values[:3]));p.runs[0].bold=True;p.paragraph_format.keep_with_next=True
  for key,value in list(row.items())[3:]:d.add_paragraph(key+': '+str(value or ''))
 d.add_paragraph('Completare de inventar: raportul și checklistul au fost adăugate după verificarea celor 119 poziții pe proiect. Registrul final include și aceste două documente interne. Nu se aplică semnături în numele persoanelor.')
 checklist=False
 for p in d.paragraphs:
  if p.text=='Checklistul corecturilor':
   checklist=True
   for r in p.runs:r.font.color.rgb=RGBColor(0,0,0);r.font.size=Pt(12)
  if checklist:
   p.paragraph_format.keep_together=True
   p.paragraph_format.keep_with_next=not p.text.startswith('Termen:') and not p.text.startswith('Completare de inventar:')
 foot=sec.footer.paragraphs[0];foot.text='ROSE | Audit intern dosar Sebeș | 01.11.2026 | '
 fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
 word=out/'Raport_audit_si_checklist.docx';pdf=out/'Raport_audit_si_checklist.pdf';d.save(word);jobs.append(dict(docx=str(word),pdf=str(pdf),project=pr['id']))
 for idx,title,dest,src in [(121,'Raport de audit independent și checklist',word,report),(122,'Checklist corecturi audit',copycsv,check)]:
  rs.append(dict(project=pr['id'],folder=19,title=title,status='Audit intern',source=str(src),dest=str(dest),obs='Document intern. Scorul de organizare este separat de pregătirea documentară pentru depunere.',owner='Auditor / ROSE',signer='Nu se semnează pentru depunere',required='Document intern',action='Urmăriți închiderea lipsurilor externe; nu se depune ca declarație de eligibilitate.',due='2026-11-02T16:00:00',email_due='2026-11-03T00:00:00',id=f"P{pr['id']}-{idx}"))
(B/'records.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8');(B/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'audit_checklist.json').write_text(json.dumps(checkrows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Audit delivery prepared')
