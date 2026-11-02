from pathlib import Path
import json, hashlib, re, unicodedata
from xml.sax.saxutils import escape
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdfplumber

root=Path.cwd()
out=root/'08. Corespondenta/2026.10.26 Emailuri primite PDF'
out.mkdir(exist_ok=True)
index={r['cale']:r for r in json.loads((root/'folder map/inventar.json').read_text(encoding='utf-8'))}
regpath=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.26 Registru comunicatii.json'
reg=json.loads(regpath.read_text(encoding='utf-8-sig'))
rows=[]
seen=set()
for r in reg['comunicatii']:
    if r.get('sens')!='PRIMIT':continue
    sender=str(r.get('expeditor','')).lower()
    firm='BERGER' if '@bmberger.at' in sender else ('PECH' if '@zt-pech.at' in sender else None)
    if not firm or r['id'] in seen:continue
    assert not r.get('trunchiat'),r['id']
    seen.add(r['id']);rows.append((firm,r))
rows.sort(key=lambda x:(x[0],x[1]['data'],x[1].get('ora_utc','')))
pdfmetrics.registerFont(TTFont('AR','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('AB','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('AR',normal='AR',bold='AB',italic='AR',boldItalic='AB')
navy=colors.HexColor('#15394D'); gray=colors.HexColor('#566773')
title=ParagraphStyle('title',fontName='AB',fontSize=16,leading=20,textColor=navy,spaceAfter=6)
small=ParagraphStyle('small',fontName='AR',fontSize=8,leading=10.5,textColor=gray,splitLongWords=True)
body=ParagraphStyle('body',fontName='AR',fontSize=10,leading=13.5,spaceAfter=1.3,splitLongWords=True,allowWidows=0,allowOrphans=0)
meta=ParagraphStyle('meta',parent=body,fontSize=8.8,leading=11.5,textColor=gray)
def norm(t):return re.sub(r'\s+','',unicodedata.normalize('NFC',t))
outputs=[]
for firm,r in rows:
    src=root/r['cale'];digest=hashlib.sha256(src.read_bytes()).hexdigest()
    assert digest==index[r['cale']]['sha256'],('sursa modificata',r['cale'])
    text=src.read_text(encoding='utf-8-sig')
    js=src.with_suffix('.json')
    tech=''
    if js.exists():
        jd=json.loads(js.read_text(encoding='utf-8-sig'))
        if isinstance(jd,dict):
            tech=jd.get('received_at','')
            if not tech and isinstance(jd.get('email'),dict):tech=jd['email'].get('received_at','')
    target=out/firm/f"{r['data']} Email primit {firm} {r['id'][:8]}.pdf"
    target.parent.mkdir(exist_ok=True)
    story=[Paragraph(f"{firm} | EMAIL PRIMIT | {r['data']}",title),Paragraph('Export pentru tipărire din arhiva Eva-Mail. Textul original, semnătura și corespondența citată sunt păstrate integral. Atașamentele sunt documente separate.',small)]
    if tech:story += [Spacer(1,4),Paragraph('Dată tehnică originală: '+escape(str(tech)),small)]
    story += [Spacer(1,8),HRFlowable(width='100%',thickness=.6,color=navy),Spacer(1,9)]
    inbody=False; blank=False
    for ln in text.splitlines():
        if 'TEXTUL FURNIZAT DE EVA' in ln or 'TEXT ORIGINAL NEMODIFICAT' in ln:inbody=True
        if not ln.strip():
            if not blank:story.append(Spacer(1,4))
            blank=True
            continue
        blank=False
        story.append(Paragraph(escape(ln).replace('\t','&#160;&#160;&#160;&#160;'),body if inbody else meta))
    story += [KeepTogether([Spacer(1,8),HRFlowable(width='100%',thickness=.35,color=colors.HexColor('#CED7DC')),Spacer(1,5),Paragraph('Sursă arhivată: '+escape(r['cale'])+'<br/>SHA-256: '+digest+'<br/>Conversie: 2026.10.26. Exportul text disponibil nu reprezintă reproducerea vizuală a mesajului MIME/HTML original.',small)])]
    def footer(c,doc,firm=firm,date=r['data'],sid=r['id'][:8]):
        c.setStrokeColor(colors.HexColor('#D4DFE3'));c.line(42,35,553,35)
        c.setFillColor(gray);c.setFont('AR',7.3)
        c.drawString(42,23,f'{firm} | PRIMIT {date} | Eva-Mail {sid} | Export 2026.10.26')
        c.drawRightString(553,23,str(doc.page))
    SimpleDocTemplate(str(target),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=35,bottomMargin=49,title=f"{firm} - Email primit {r['data']} - {r['subiect']}",author='A&C Wohnart').build(story,onFirstPage=footer,onLaterPages=footer)
    with pdfplumber.open(target) as d:
        combined='\n'.join(p.crop((0,0,p.width,p.height-45)).extract_text() or '' for p in d.pages)
        assert norm(text) in norm(combined),('TEXT DIFERIT SAU LIPSA',r['id'])
        pages=len(d.pages)
    outputs.append({'firma':firm,'data_mesaj':r['data'],'id_eva':r['id'],'statut':'PRIMIT','expeditor':r['expeditor'],'destinatari':r['destinatari'],'cc':r['cc'],'subiect':r['subiect'],'sursa_txt':r['cale'],'sha256_sursa':digest,'sursa_json':str(js.relative_to(root)).replace('\\','/') if js.exists() else None,'data_tehnica_originala':tech or 'vezi exportul sursa','cale_pdf':str(target.relative_to(root)).replace('\\','/'),'sha256_pdf':hashlib.sha256(target.read_bytes()).hexdigest(),'pagini':pages,'text_integral_verificat':True})
manifest={'data_export':'2026.10.26','created_at_iso':datetime.now(ZoneInfo('Europe/Bucharest')).isoformat(),'sfera':'Toate mesajele PRIMITE din registrul local curent cu expeditor bmberger.at sau zt-pech.at; deduplicare dupa ID Eva-Mail. Fara verificare noua in casute. Notificarile MAILER-DAEMON nu sunt mesaje ale partenerilor si nu sunt incluse.','conversii':outputs,'numar_mesaje':len(outputs),'numar_pagini':sum(x['pagini'] for x in outputs),'contracte_modificate':False,'emailuri_trimise':0}
(out/'2026.10.26 Registru conversii email PDF.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'folder':str(out),'pdfs':[{k:x[k] for k in ['firma','data_mesaj','id_eva','pagini','cale_pdf']} for x in outputs],'total':len(outputs)},ensure_ascii=False))
