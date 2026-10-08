from pathlib import Path
import json,html,re,hashlib,shutil,gzip,sys
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
from continut_raport import PAGES
from colecteaza_documentatia import ROOT,REG,CSS
sys.stdout.reconfigure(encoding='utf-8')
S=json.loads((REG/'registru_surse.json').read_text(encoding='utf-8')); SD={s['id']:s for s in S}
R=ROOT/'01_Raport'; R.mkdir(exist_ok=True)
AN=ROOT/'07_Anexe_tehnice';AN.mkdir(exist_ok=True)
QA=Path(__file__).parent/'verificare_vizuala';QA.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
styles={
 'title':ParagraphStyle('title',fontName='Arial-Bold',fontSize=21,leading=25,spaceAfter=15,textColor=colors.black),
 'heading':ParagraphStyle('heading',fontName='Arial-Bold',fontSize=17,leading=21,spaceAfter=12,textColor=colors.black),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10.5,leading=14,spaceAfter=9),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=9.5,leading=12),
 'headcell':ParagraphStyle('headcell',fontName='Arial-Bold',fontSize=9.5,leading=12,textColor=colors.white),
 'refs':ParagraphStyle('refs',fontName='Arial',fontSize=8.2,leading=10.5,spaceBefore=8,textColor=colors.HexColor('#3d4b58'))}
def esc(t):return html.escape(str(t))
def par(t,style='body'):return Paragraph(esc(t),styles[style])
W,H=landscape(A4); M=35; TW=W-2*M
def draw_page(c,d):
    c.setTitle('Analiza iDempiere HR și SSM SU pentru România')
    c.setAuthor('Documentație proiect iDempiere')
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#4b5563'))
    c.drawString(M,18,'iDempiere · HR · SSM/SU | Analiză documentară | 08.10.2026')
    c.drawRightString(W-M,18,str(d.page))
def table(headers,rows,widths=None):
    data=[[par(x,'headcell') for x in headers]]+[[par(x,'cell') for x in row] for row in rows]
    widths=widths or [1/len(headers)]*len(headers)
    t=Table(data,colWidths=[TW*x for x in widths],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#23394d')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#d9d9d9')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f1f4f7')]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t
story=[]; htmlparts=[]
for n,p in enumerate(PAGES,1):
    if n>1:story.append(PageBreak())
    title=(str(n)+' '+p['title']) if n>1 else p['title']
    story.append(par(title,'title' if n==1 else 'heading'))
    htmlparts.append('<section id="cap'+str(n)+'"><h1>'+esc(title)+'</h1>')
    for t in p['paras']: story.append(par(t));htmlparts.append('<p>'+esc(t)+'</p>')
    if p['headers']:
        story.append(table(p['headers'],p['rows'],p['widths']));story.append(Spacer(1,8))
        htmlparts.append('<table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in p['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in p['rows'])+'</tbody></table>')
    for t in p['after']: story.append(par(t));htmlparts.append('<p>'+esc(t)+'</p>')
    refs=[]; hrefs=[]
    for id in p['refs']:
        assert id in SD,id
        s=SD[id]; refs.append('<a href="'+esc(s['url'])+'" color="#165a87">'+esc(id+' '+s['titlu'])+'</a>')
        local=('<a href="../'+esc(s['fisier'])+'">copie locală</a>') if s['fisier'] else 'descărcare indisponibilă'
        hrefs.append('<li><a href="'+esc(s['url'])+'">'+esc(id+' '+s['titlu'])+'</a> · '+local+'</li>')
    if refs:story.append(Paragraph('Surse: '+'; '.join(refs)+'.',styles['refs']))
    if hrefs:htmlparts.append('<details><summary>Surse și copii locale</summary><ul>'+''.join(hrefs)+'</ul></details>')
    htmlparts.append('</section>')

pdf=R/'Analiza_iDempiere_HR_SSM_SU.pdf'
SimpleDocTemplate(str(pdf),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=30,bottomMargin=34,allowSplitting=1).build(story,onFirstPage=draw_page,onLaterPages=draw_page)
nav='<nav><h2>Cuprins</h2><ol>'+''.join('<li><a href="#cap'+str(i)+'">'+esc(p['title'])+'</a></li>' for i,p in enumerate(PAGES,1))+'</ol></nav>'
(R/'Analiza_iDempiere_HR_SSM_SU.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Analiza iDempiere HR și SSM SU</title><style>'+CSS+'section{margin:50px 0}details{font-size:14px}@media print{nav{display:none}section{break-before:page}a{color:#000}}</style><body><p><a href="../INDEX.html">Deschide indexul dosarului</a> · <a href="Analiza_iDempiere_HR_SSM_SU.pdf">Raport PDF</a></p>'+nav+''.join(htmlparts)+'</body></html>',encoding='utf-8')
(R/'continut_structurat.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2),encoding='utf-8')

def annex(name,title,intro,headers,rows):
    doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>'+esc(title)+'</title><style>'+CSS+'td[contenteditable]{background:#fff9e6}button{padding:10px;font-size:16px}@media print{button{display:none}}</style><body><p><a href="../INDEX.html">Index dosar</a></p><h1>'+esc(title)+'</h1><p>'+esc(intro)+'</p><button onclick="window.print()">Tipărește sau salvează PDF</button><table><tr>'+''.join('<th>'+esc(x)+'</th>' for x in headers)+'</tr>'
    for row in rows:
        doc+='<tr>'+''.join('<td'+(' contenteditable="true"' if x=='DE COMPLETAT' else '')+'>'+esc(x)+'</td>' for x in row)+'</tr>'
    doc+='</table><p>Celulele galbene pot fi completate în browser. Pentru păstrarea rezultatelor folosiți tipărirea în PDF sau butonul de salvare HTML de mai jos.</p><button onclick="save()">Salvează formularul completat</button><script>function save(){let a=document.createElement("a");a.href=URL.createObjectURL(new Blob(["<!doctype html>"+document.documentElement.outerHTML],{type:"text/html;charset=utf-8"}));a.download="'+name+'_completat.html";a.click();URL.revokeObjectURL(a.href)}</script></body></html>'
    (AN/(name+'.html')).write_text(doc,encoding='utf-8')
annex('A01_Cerinte_beneficiar','Fișă de cerințe pentru selecția HR și SSM SU','Completați datele de volum și constrângerile înainte de cererea de ofertă. Nu introduceți parole sau date medicale individuale.', ['Cerință','Răspuns beneficiar','Dovadă sau observație'],[[x,'DE COMPLETAT','DE COMPLETAT'] for x in ['Versiune iDempiere, Java și bază de date','Lista pluginurilor instalate','Număr companii și angajați activi','Puncte de lucru și tipuri de risc','Număr de utilizatori HR și aprobatori','Terminale pontaj și formate export','Reguli de ture și muncă de noapte','Soluție actuală payroll și responsabil validare','Documente și raportări românești obligatorii','Tipuri de instruire și frecvențe','Număr anual de documente și semnături','Cerințe de arhivare și recuperare','Identitate unică și SSO','Buget de implementare și operare','Criterii eliminatorii și termen']])
tests=next(p for p in PAGES if p['title']=='Scenarii de test gata de folosit')['rows']
annex('A02_Registru_acceptanta','Registru de acceptanță pilot','Documentați execuția efectivă. Toate rezultatele sunt inițial necompletate; raportul nu prezintă teste de aplicație executate.', ['ID','Scenariu','Rezultat așteptat','Obținut și dovadă','Acceptat de'],[r+['DE COMPLETAT','DE COMPLETAT'] for r in tests])
questions=['Ce funcții sunt incluse în ediția și prețul ofertate?','Ce versiuni ale aplicației și API-ului sunt suportate?','Puteți demonstra crearea, actualizarea și dezactivarea unui angajat prin API?','Cum se transmite schimbarea postului și a grupei de risc?','Ce persoane semnează fiecare tip de document și în ce ordine?','Ce tip de semnătură este folosit și ce dovezi se exportă?','Se descarcă prin API PDF-urile finale și istoricul de semnare?','Cum se exportă integral dosarul la încetarea contractului?','Ce documente sunt șabloane și cine răspunde de adecvarea lor?','Cum actualizați șabloanele la modificarea legislației?','Există limitări de API, utilizatori, documente sau stocare?','Ce costuri apar separat pentru semnături, integrare și suport?','Care este procedura de restaurare și termenul de suport?','Puteți executa scenariile T01–T12 aplicabile?']
annex('A03_Intrebari_furnizori','Întrebări pentru furnizori','Formular de evaluare, pregătit pentru trimitere de către beneficiar. Nu a fost trimis niciun mesaj către furnizori.', ['Întrebare','Răspuns furnizor','Document sau demonstrație'],[[q,'DE COMPLETAT','DE COMPLETAT'] for q in questions])
annex('A04_Cost_total','Fișă de cost total comparabil','Introduceți oferte reale, aceeași perioadă și aceleași volume. Nu sunt presupuse prețuri.', ['Componentă','Variantă HR nativ','Variantă Frappe HR','Variantă Java separat'],[[q,'DE COMPLETAT','DE COMPLETAT','DE COMPLETAT'] for q in ['Licențe și abonamente','Găzduire, backup și monitorizare','Build și compatibilizare','Migrare date','Localizare salarială România','Conector HR și iDempiere','Conector SSM/SU','Semnături electronice','Instruire utilizatori','Suport și actualizări anuale','Export și ieșire din platformă','Total conform ofertelor']])
sql='''-- Inventar numai de citire pentru iDempiere PostgreSQL.
-- Nu a fost executat pe baza beneficiarului. Rulați într-o sesiune separată cu rol read-only.
-- Exportați separat rezultatele fiecărui SELECT. Nu extrage date personale.
BEGIN TRANSACTION READ ONLY;
SELECT ad_menu_id, name, action, ad_window_id, ad_process_id, isactive FROM ad_menu ORDER BY name;
SELECT ad_window_id, name, windowtype, isactive FROM ad_window ORDER BY name;
SELECT ad_tab_id, ad_window_id, name, ad_table_id, seqno, isactive FROM ad_tab ORDER BY ad_window_id, seqno;
SELECT ad_table_id, tablename, name, entitytype, isactive FROM ad_table ORDER BY tablename;
SELECT ad_process_id, name, classname, isreport, isactive FROM ad_process ORDER BY name;
SELECT c.ad_table_id, c.columnname, c.name, c.ad_reference_id, c.isactive FROM ad_column c ORDER BY c.ad_table_id, c.columnname;
ROLLBACK;
-- Lista bundle-urilor OSGi și versiunile se exportă din administrarea aplicației.
-- Meniurile efectiv vizibile depind și de rol; inventarul de mai sus este global.
'''
(AN/'A05_Inventar_iDempiere_readonly.sql').write_text(sql,encoding='utf-8')

good=sum(s['stare']=='DESCARCAT' for s in S);bad=len(S)-good
groupcounts={}
for s in S:
    g=s['grup']; groupcounts.setdefault(g,{'recuperate':0,'indisponibile':0});groupcounts[g]['recuperate' if s['stare']=='DESCARCAT' else 'indisponibile']+=1
rows=[]
for s in sorted(S,key=lambda s:(s['grup'],s['id'])):
    dest='<a href="'+esc(s['fisier'])+'">Deschide copia locală</a>' if s['fisier'] else 'Indisponibil: '+esc(s.get('eroare',''))
    rows.append('<tr><td>'+esc(s['id'])+'</td><td>'+esc(s['grup'])+'</td><td>'+esc(s['titlu'])+'</td><td>'+dest+'</td><td><a href="'+esc(s['url'])+'">Sursa oficială</a></td><td>'+esc(s['stare'])+'</td></tr>')
index='<!doctype html><html lang="ro"><meta charset="utf-8"><title>Dosar iDempiere HR și SSM SU</title><style>'+CSS+'input{padding:12px;width:90%;font-size:18px}thead{position:sticky;top:0}td{font-size:14px}</style><body><h1>Dosar iDempiere HR și SSM SU</h1><p>Analiză în română, documentații originale, anexe și registru de proveniență. 08.10.2026.</p><p><strong>'+str(good)+' surse recuperate; '+str(bad)+' descărcări nereușite din '+str(len(S))+' surse inventariate.</strong> Linkurile indisponibile nu sunt prezentate ca documente descărcate.</p><ul><li><a href="01_Raport/Analiza_iDempiere_HR_SSM_SU.pdf">Raport PDF</a></li><li><a href="01_Raport/Analiza_iDempiere_HR_SSM_SU.html">Raport HTML cu cuprins și legături locale</a></li>'
for f in sorted(AN.glob('*.html')):index+='<li><a href="'+f.relative_to(ROOT).as_posix()+'">'+esc(f.stem.replace('_',' '))+'</a></li>'
index+='</ul><p>Copiile HTML sunt text și tabele offline, fără scripturile sau imaginile externe ale site-urilor. Manualele PDF sunt păstrate în forma descărcată. Documentațiile originale nu sunt traduse integral; raportul și anexele proprii sunt în română.</p><input id="q" placeholder="Filtrează produs, modul, document sau stare"><table><thead><tr><th>ID</th><th>Produs</th><th>Document</th><th>Local</th><th>Online</th><th>Stare</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table><script>document.getElementById("q").oninput=function(){document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(this.value.toLowerCase()))}</script></body></html>'
(ROOT/'INDEX.html').write_text(index,encoding='utf-8')
(REG/'rezumat_recuperare.json').write_text(json.dumps({'total_surse':len(S),'recuperate':good,'nerecuperate':bad,'pe_grupe':groupcounts},ensure_ascii=False,indent=2),encoding='utf-8')
reader=PdfReader(pdf)
summary=[]
for i,p in enumerate(reader.pages,1):
    text=p.extract_text() or ''; summary.append({'pagina':i,'caractere':len(text),'inceput':text[:140]})
(QA/'pagini.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pagini_pdf':len(reader.pages),'capitole':len(PAGES),'surse':len(S),'recuperate':good,'nerecuperate':bad,'pdf':str(pdf)},ensure_ascii=False))
