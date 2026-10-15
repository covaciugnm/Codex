from pathlib import Path
import fitz,json,re,hashlib
from docx import Document
p=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/04. Firme + Executie/01. Verificator (Pruefingenieur)/TOMS/2026-10-01 Contract v3 - propunere')
f=p/'2026-10-01 Werkvertrag TOMS - Entwurf AG v3.pdf';d=fitz.open(f)
txt='\n'.join(x.get_text() for x in d)
word=Document(f.with_suffix('.docx'))
def norm(s):return re.sub(r'\s+','',s).replace('\u00ad','').replace('#','')
pdfn=norm(txt)
missing=[x.text[:160] for x in word.paragraphs if x.text.strip() and norm(x.text) not in pdfn]
checks={
'total_net': '37.900,00' in txt,
'total_vat':'7.580,00' in txt,
'total_gross':'45.480,00' in txt,
'no_BauKG':not any(s in txt for s in ['BauKG','ANG 840']),
'free_included_calculations':'ohne zusätzliches Entgelt' in txt,
'forces_on_plans':norm('unmittelbar auf den zugehörigen Führungs-, Positions- bzw. Lastplänen') in pdfn,
'timeline':all(s in txt for s in ['01.10.2026','09.10.2026','16.10.2026','22.10.2026','23.10.2026','28.10.2026']),
'insurance_date_and_limit':all(s in txt for s in ['03.03.2026','1.500.000,00','01.01.2027']),
'old_insurance_recency_removed':'nicht älter als drei Monate' not in txt,
'legal_deadline':'31.12.2027' in txt,
'offer_extension':'31.12.2026' in txt,
'one_change':norm('einmalige zusammengefasste Planwechsel-/Änderungsbearbeitung') in pdfn,
'proposal_status':'Vertragsangebot der AG' in txt,
'signature_fields':txt.count('Unterschriftsdatum')>=2,
'no_empty_pages':all(len(x.get_text().strip())>20 for x in d),
'all_docx_paragraphs_in_pdf':not missing}
bounds=[]
for i,pg in enumerate(d):
 for b in pg.get_text('blocks'):
  if b[0]<0 or b[1]<0 or b[2]>pg.rect.width+1 or b[3]>pg.rect.height+1:bounds.append(i+1)
checks['no_text_outside_pages']=not bounds
report={'pages':len(d),'checks':checks,'missing_paragraphs':missing,'out_of_bounds_pages':bounds,'hashes':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [f,f.with_suffix('.docx')]},'visual_review':'Prima pagină, o pagină de clauze, ultima pagină și zona semnăturilor au fost inspectate. PDF-ul EVA folosește paragrafe/listări pentru anexele tabelare.'}
(p/'_lucru'/'QA final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
