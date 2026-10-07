import os,json,html,pathlib,sys
os.environ['QT_QPA_PLATFORM']='offscreen'
from PySide6.QtGui import QGuiApplication,QPainter,QImage,QPdfWriter,QPageSize,QPageLayout,QTextDocument,QFont,QFontDatabase
from PySide6.QtCore import QRectF,QMarginsF,QSizeF
from PySide6.QtSvg import QSvgRenderer
app=QGuiApplication([])
for font in ['arial.ttf','arialbd.ttf','ariali.ttf','arialbi.ttf','segoeui.ttf']:
    font_path=pathlib.Path('C:/Windows/Fonts')/font
    if font_path.exists():QFontDatabase.addApplicationFont(str(font_path))
app.setFont(QFont('Arial',10))
root=pathlib.Path('EVA_PRINT_WEBSITE_BRIEF_2026-10-02').resolve()
records=[] if '--prompt-only' in sys.argv else json.loads((root/'02_MATERIALS/materials.en.json').read_text(encoding='utf8'))
def pdf_html(target,body):
    writer=QPdfWriter(str(target));writer.setResolution(96);writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4));writer.setPageMargins(QMarginsF(15,15,15,15))
    doc=QTextDocument();doc.setDefaultFont(QFont('Arial',10));doc.setHtml('<html><head><style>h1{font-size:21pt;color:#173d59}h2{font-size:13pt;color:#173d59}p,li{line-height:125%}a{color:#145f78}td{padding:5px}body{font-family:Arial}</style></head><body>'+body+'</body></html>');doc.print_(writer)
def e(s):return html.escape(str(s or ''))
for i,m in enumerate(records):
    renderer=QSvgRenderer(str(root/m['drawings']['svg']));assert renderer.isValid(),m['id']
    image=QImage(1400,900,QImage.Format.Format_ARGB32);image.fill(0xffffffff);painter=QPainter(image);renderer.render(painter);painter.end();assert image.save(str(root/m['drawings']['png']))
    writer=QPdfWriter(str(root/m['drawings']['pdf']));writer.setResolution(144);writer.setPageSize(QPageSize(QSizeF(350,225),QPageSize.Unit.Millimeter));writer.setPageMargins(QMarginsF(0,0,0,0));painter=QPainter(writer);renderer.render(painter,QRectF(0,0,writer.width(),writer.height()));painter.end()
    paragraphs=['<h1>'+e(m['name'])+'</h1>','<p><b>EVA PRINT engineering overview | 2026-10-02</b></p>','<p>This is an original research overview, not a manufacturer technical data sheet or a certified production profile. Grade data and the installed printer configuration require engineering review before acceptance.</p>','<p>'+e(m['description_en'])+'</p>','<p><b>Family:</b> '+e(m['family'])+'<br><b>Service status:</b> '+e(m['service_status'])+'<br><b>Stock:</b> Owner reports broad stock. Exact SKU, color and quantity are unverified.</p>']
    for label,key in [('Advantages','advantages'),('Limitations and process requirements','limitations')]:paragraphs+=['<h2>'+label+'</h2><ul>'+''.join('<li>'+e(t)+'</li>' for t in m[key])+'</ul>']
    paragraphs+=['<h2>Technical characteristics</h2>']
    if not m['properties']:paragraphs+=['<p>Measured values are not reproduced here without a confirmed specimen/test state. Consult the exact supplier document linked below. Do not use family-level expectations as grade-specific numerical properties.</p>']
    for p in m['properties']:paragraphs+=['<p><b>'+e(p['property'])+':</b> '+e(p['value'])+'<br>Supplier webpage value; specimen orientation, conditioning and test state have not been independently established.</p>']
    for k,v in m['settings'].items():
        if v and k not in ('source_url','values_are_grade_specific'):paragraphs+=['<p><b>'+e(k.replace('_',' ').title())+':</b> '+e(v)+'</p>']
    paragraphs+=['<h2>Proposed applications</h2><ul>'+''.join('<li>'+e(x['title'])+': '+e(x['description'])+'</li>' for x in m['application_examples'])+'</ul>','<h2>Manufacturer documents</h2>']
    if m['manufacturer_tds_status']!='downloaded':paragraphs+=['<p><b>An exact manufacturer TDS PDF was not retrieved.</b> The source product page remains the available reference. This overview does not substitute for manufacturer-certified values.</p>']
    for d in m['datasheets']:paragraphs+=['<p><b>'+e(d['document_type'])+'</b><br><a href="'+e(d['url'])+'">'+e(d['url'])+'</a><br>Local research copy: '+e(d['path'])+'</p>']
    paragraphs+=['<h2>Reference and drawing</h2>','<p>Supplier source: <a href="'+e(m['source_url'])+'">'+e(m['source_url'])+'</a></p>','<p>Original conceptual drawing: '+e(m['drawings']['pdf'])+'<br>Editable exchange drawing: '+e(m['drawings']['dxf'])+'</p>','<p>Drawings are illustrative studies, not released manufacturing geometry. Reference photos remain private until publication rights are established.</p>','<p><b>EVA PRINT SRL</b> | Five specialized engineers (owner declaration)<br>print@eva-org.com</p>']
    pdf_html(root/m['engineering_overview'],''.join(paragraphs))
    if i%25==0:print('Rendered',i+1,'of',len(records),flush=True)
prompt=(root/'01_PROMPT/EVA_PRINT_MASTER_PROMPT_EN.txt').read_text(encoding='utf8')
pdf_html(root/'01_PROMPT/EVA_PRINT_MASTER_PROMPT_EN.pdf','<h1>EVA PRINT website implementation prompt</h1>'+'<p>'+e(prompt).replace('\n\n','</p><p>').replace('\n','<br>')+'</p>')
print('Complete:',len(records),'PNG/PDF drawings and engineering overview PDFs',flush=True)
