from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml.ns import qn
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader,PdfWriter
import html,json,hashlib

work=Path(r'C:\Users\User\.codex\visualizations\2026\10\22\01a16433-6d2f-7bf2-93f1-ca88c3efba44')
root=Path(r'Z:\00.Roboti\AGV-Jining.Aowei')
src=root/'100. Inbox';out=root/'2.Verificare achizitie 2026-10-22'
d=Document()
for x in list(d.styles.element.iter(qn('w:pBdr'))):x.getparent().remove(x)
s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7);s.top_margin=s.bottom_margin=Cm(1.9);s.left_margin=s.right_margin=Cm(2)
for n in ['Normal','Title','Heading 1','Heading 2']:
 d.styles[n].font.name='Calibri';d.styles[n].font.color.rgb=RGBColor(0,0,0)
d.styles['Normal'].font.size=Pt(11);d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Title'].font.size=Pt(23);d.styles['Heading 1'].font.size=Pt(15)
def p(t):d.add_paragraph(t)
def h(t):d.add_paragraph(t,'Heading 1')
def entry(a,b):
 q=d.add_paragraph();q.add_run(a+' ').bold=True;q.add_run(b)
d.add_paragraph('Explicația modificărilor document cu document','Title')
p('22 octombrie 2026 | Dosarul achiziției platformei Jining Aowei. Documentul explică diferența dintre materialele originale și proiectele pregătite pentru corectare și confirmare de către furnizor.')
p('Au fost create o proformă propusă și o anexă tehnică. Originalele nu au fost modificate. Nu au fost emise în numele furnizorului facturi, declarații CE, certificate ISO, rapoarte de încercare sau documente vamale. Câmpurile neconfirmate sunt marcate explicit.')
h('1 Factura și fișa tehnică din PDF')
p('Sursă: PI261001RO (1).pdf, două pagini. Document nou: 02_Proforma_revizuita_PROIECT_EN.docx.')
entry('Păstrat','Vânzătorul indicat, referința 261001102RO și valorile 2.500 EUR + 1.370 EUR - 70 EUR = 3.800 EUR, cu reconfirmarea comercială de către vânzător.')
entry('Reformulat','Descrierea a fost structurată pe model/configurație, cumpărător, livrare, plată, garanție, documente și date bancare. Au fost separate termenul de expediere și sosirea la destinație.')
entry('De completat','Cumpărătorul legal, codul fiscal, adresele, modelul/revizia, importatorul, condițiile DDP, configurația completă, garanția și instrucțiunile bancare. Clauzele noi sunt propuneri, nu acorduri deja acceptate.')
entry('Nu s-a decis arbitrar','Nu s-a ales între 100 kg și 200 kg; nu s-au inventat numărul bateriilor, puterea pe motor sau un cont bancar corect. Nu s-a păstrat semnătura/ștampila pe proiect.')
h('2 Fișele și reproducerile de ofertă')
p('Surse: 4440845121.png, 5030967443.png, 5033561657.png și 5040969889.png. Toate sunt incluse ca originale în PDF-ul consolidat.')
entry('Document nou','03_Anexa_tehnica_si_conformitate_PROIECT_EN.docx centralizează valorile și întrebările. Încărcătorul de 110 V a fost semnalat; compatibilitatea cu 230 V/50 Hz este o cerință propusă de confirmat, nu o caracteristică deja dovedită.')
entry('Clarificări cerute','Sarcina utilă, dimensiunile, viteza în sarcină, greutatea proprie, motoarele/controlerele, configurația bateriilor, conectorii, SDK-ul și funcțiile de siguranță. Navigația autonomă nu este presupusă din denumirea AGV.')
d.add_page_break();h('3 Declarația și certificatele furnizorului')
entry('5071728143.png Declarația CE','Originalul este neschimbat. Se solicită reemitere pentru unitatea livrată, confirmarea modelului AWC-08/seriei/VIN, completarea persoanei autorizate din UE și identificarea semnatarului. Aplicabilitatea directivelor/standardelor trebuie justificată de producător. Nu s-a redactat o declarație semnată în locul său.')
entry('5066591032.png Atestarea SZUTEST','Originalul este neschimbat. Se cere explicarea legăturii dintre modelele EAW06, WL108, 910, 916, 918, 920, 930 și AWC-08. Nu s-au schimbat numărul certificatului, modelele, datele sau semnătura. Autenticitatea nu este confirmată de această analiză.')
entry('5066555651.png Certificatul ISO','Originalul este neschimbat. A fost semnalat termenul înscris 5 martie 2025. Se cere o copie actuală dacă furnizorul continuă să invoce certificarea. Certificarea sistemului de management nu înlocuiește conformitatea produsului.')
h('4 Fotografii și baterii')
entry('30786693131.jpg și 30786697085.jpg','Fotografiile KIJO 6-GFM-85 sunt neschimbate. Au fost consemnate marca KIJO, simbolul Pb și capacitățile 85 Ah/20 h și 72 Ah/3 h. Diferența față de marca Chaowei din fișă trebuie confirmată. Tipul AGM/VRLA/GEL și caracterul non-spillable rămân neconfirmate.')
entry('Documente cerute pentru baterii','Fișa modelului exact, chimia și configurația ansamblului, documentația UE aplicabilă bateriei și confirmarea transportatorului pentru expedierea concretă. Cerința UN 38.3 nu este preluată automat pentru plumb; dacă se livrează Li-ion/LiFePO4, se solicită dovezile relevante și actualizarea documentelor.')
entry('30788002505.jpg și 30788006047.jpg','Platforma și telecomanda sunt reproduse fără modificarea conținutului. Fotografiile nu au fost tratate ca dovadă de SDK, navigație autonomă, sarcină certificată sau oprire sigură.')
h('5 Lista de verificare și solicitarea către furnizor')
p('01_Lista_inadvertente_si_checklist.docx este un raport nou cu 16 puncte, inventarul și lista documentelor pe etape. 04_Solicitare_furnizor_EN.txt este un mesaj nou, netrimis, care cere corecturile. 05_Surse_oficiale_si_baterii.txt consemnează explicațiile și sursele oficiale; nu este un certificat de transport sau import.')
d.add_page_break();h('6 Ce conține PDF-ul pentru furnizor')
p('PDF-ul consolidat include inventarul, raportul de verificare în română, proiectele în engleză, solicitarea în engleză, nota privind bateriile și sursele, PDF-ul original de două pagini și toate cele 11 imagini originale, inclusiv certificatele și reproducerile de ofertă. Cuprinsul și semnele de carte permit accesul la fiecare secțiune.')
p('Paginile PDF originale sunt preluate, iar imaginile sunt așezate pe pagini PDF cu denumirea sursei. Redimensionarea pentru pagină nu corectează conținutul documentelor. Pentru a păstra originalele, numerotarea pachetului este realizată prin cuprins și semne de carte, fără suprascrierea lor.')
p('Cele patru fișiere MP4 sunt înregistrări video, nu documente statice; numele lor sunt enumerate în pachet. Conținutul lor integral nu este convertit în pagini PDF. Dacă sunt necesare destinatarului, se trimit separat din 100. Inbox. Exemplele de la alți furnizori rămân în folderul de referințe și nu fac parte din dosarul Aowei pentru expediere.')
h('7 Ce trebuie obținut pentru închiderea dosarului')
entry('De la furnizor','Proforma/factura reemisă și anexa confirmată; documente de conformitate corelate cu modelul; documente baterie; manual; garanție; instrucțiuni bancare coerente; teste și lista livrabilelor.')
entry('La expediere și import','Factura comercială finală, packing list, documentul de transport și documentele vamale/fiscale corespunzătoare importatorului real. Nu au fost generate anticipat documente care trebuie emise de vânzător, transportator sau vamă.')
entry('Din partea cumpărătorului','Confirmarea entității juridice, adresei de livrare, utilizării dorite, sarcinii necesare și condițiilor acceptate. Aceste informații nu au fost deduse din ofertele altor furnizori.')
p('Concluzie: setul pregătit este un dosar de corectare și solicitare de completări. El poate fi trimis furnizorului pentru răspuns, dar nu dovedește că documentația finală a achiziției este completă sau că neconcordanțele au fost remediate de acesta.')
d.save(out/'07_Explicatia_modificarilor_document_cu_document.docx')

pdfmetrics.registerFont(TTFont('DejaVu',r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold',r'C:\Windows\Fonts\arialbd.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='DejaVu',fontSize=10,leading=14,spaceAfter=7,splitLongWords=True))
styles.add(ParagraphStyle(name='TitleX',fontName='DejaVuBold',fontSize=20,leading=25,spaceAfter=16))
styles.add(ParagraphStyle(name='SmallX',fontName='DejaVu',fontSize=9,leading=12,spaceAfter=6,splitLongWords=True))
def make_text(path,title,text):
 story=[Paragraph(html.escape(title),styles['TitleX'])]
 for line in text.splitlines():
  if line.strip():story.append(Paragraph(html.escape(line),styles['BodyX']))
  else:story.append(Spacer(1,5))
 SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42).build(story)
make_text(work/'email.pdf','Request to supplier', (out/'04_Solicitare_furnizor_EN.txt').read_text(encoding='utf-8'))
make_text(work/'batteries.pdf','Battery requirements and official sources', (out/'05_Surse_oficiale_si_baterii.txt').read_text(encoding='utf-8'))
imgpdf=work/'seller_images.pdf';c=canvas.Canvas(str(imgpdf),pagesize=A4)
imgs=sorted(p for p in src.iterdir() if p.suffix.lower() in ['.png','.jpg','.jpeg'])
for img in imgs:
 w,h=A4;c.setFont('DejaVuBold',11);c.drawString(30,h-30,'SELLER ORIGINAL / '+img.name)
 c.setFont('DejaVu',8);c.drawString(30,h-44,'Reproduced as supplied. Content has not been corrected or authenticated.')
 ir=ImageReader(str(img));iw,ih=ir.getSize();scale=min((w-60)/iw,(h-90)/ih)
 c.drawImage(ir,(w-iw*scale)/2,25+(h-90-ih*scale)/2,width=iw*scale,height=ih*scale,mask='auto')
 c.showPage()
c.save()
segments=[('Review and checklist RO',work/'01_Lista_inadvertente_si_checklist.pdf'),('Revised proforma DRAFT EN',work/'02_Proforma_revizuita_PROIECT_EN.pdf'),('Technical annex DRAFT EN',work/'03_Anexa_tehnica_si_conformitate_PROIECT_EN.pdf'),('Request to supplier EN',work/'email.pdf'),('Battery requirements and sources RO',work/'batteries.pdf'),('Seller invoice and technical sheet ORIGINAL',src/'PI261001RO (1).pdf'),('Seller images and certificates ORIGINAL',imgpdf)]
page=3;index=[]
for title,path in segments:
 count=len(PdfReader(str(path)).pages);index.append((title,path,page,count));page+=count
cover=work/'cover.pdf';story=[Paragraph('Aowei purchase documentation',styles['TitleX']),Paragraph('Review package for supplier response | 22 October 2026',styles['BodyX']),Paragraph('Reference invoice 261001102RO dated 1 October 2026. Quoted total EUR 3,800.',styles['BodyX']),Paragraph('The revised proforma and technical annex are buyer-prepared proposals for completion and reissue by the seller. They are not supplier-issued invoices or compliance certificates. Supplier originals are reproduced unchanged in the appendix.',styles['BodyX']),Spacer(1,12)]
for title,path,start,count in index:story.append(Paragraph(f'<b>Pages {start}–{start+count-1}</b> | {html.escape(title)}',styles['BodyX']))
story += [Spacer(1,12),Paragraph('Requested response: resolve the marked discrepancies, complete the bracketed fields and return corrected documents issued by the responsible supplier/manufacturer. Banking details and unverified product values have not been approved by this package.',styles['BodyX']),PageBreak(),Paragraph('Original file inventory',styles['TitleX'])]
story.append(Paragraph('All static files from the original Aowei Inbox are included: one two-page PDF and eleven images. Repeated screenshots are retained for completeness.',styles['BodyX']))
for f in sorted(src.iterdir()):
 if f.is_file():story.append(Paragraph(html.escape(f.name)+(' — video, send separately' if f.suffix=='.mp4' else ' — included'),styles['SmallX']))
story.append(Spacer(1,10));story.append(Paragraph('Videos are listed only; their full content is not represented by this static PDF. Comparative documents from other suppliers are retained in the local reference folder and are not part of this Aowei supplier package.',styles['BodyX']))
SimpleDocTemplate(str(cover),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=42,bottomMargin=42).build(story)
assert len(PdfReader(str(cover)).pages)==2
writer=PdfWriter();writer.append(str(cover),outline_item='Cover and original inventory')
for title,path,start,count in index:
 offset=len(writer.pages);writer.append(str(path),outline_item=title)
 if path==imgpdf:
  for n,img in enumerate(imgs):writer.add_outline_item(img.name,offset+n)
writer.add_metadata({'/Title':'Aowei purchase documentation for supplier response','/Subject':'Original seller documents and clearly marked proposed revisions','/Author':'Prepared for buyer review'})
dest=out/'06_Dosar_complet_Aowei_pentru_furnizor.pdf'
with dest.open('wb') as f:writer.write(f)
print('COMBINED',len(writer.pages),str(dest),flush=True)
manifest={'pdf':str(dest),'pages':len(writer.pages),'sections':[{'title':t,'first_page':s,'pages':c} for t,_,s,c in index],'original_files':[{'file':f.name,'included':f.suffix!='.mp4','sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(src.iterdir()) if f.is_file()]}
(out/'08_Inventar_si_trasabilitate.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('EXPLANATION',str(out/'07_Explicatia_modificarilor_document_cu_document.docx'),flush=True)
