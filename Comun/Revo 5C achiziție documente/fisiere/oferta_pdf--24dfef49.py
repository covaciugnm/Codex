from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
DST = r"Z:\00. Proiecte 2025\2025.06.12 Ionel Capota SES\3. Achizitie\2. Revo 5C SRL\REVO 5C -CFMoto"
NAVY=colors.HexColor("#1F3A5F"); GREY=colors.HexColor("#555555"); LIGHT=colors.HexColor("#EEF2F7")
S=lambda n,**k: ParagraphStyle(n, **{"fontName":"Arial","fontSize":9.5,"leading":12, **k})
h1=S("h1",fontName="Arial-Bold",fontSize=16,leading=20,textColor=NAVY)
h2=S("h2",fontName="Arial-Bold",fontSize=10.5,leading=14,textColor=NAVY,spaceBefore=8,spaceAfter=3)
body=S("body"); small=S("small",fontSize=8,leading=10,textColor=GREY); bold=S("bold",fontName="Arial-Bold")

OFERTANTI=[
 dict(file="OFERTA_WM-ATV-015_REVO_5C_SRL.pdf", nr="WM-ATV-015", inv="WM-ATV-009", firma="REVO 5C S.R.L.",
      cui="52226710", j="J2025056106001", euid="EUID ROONRC.J2025056106001",
      adresa="Mun. Alba Iulia, Str. Septimius Severus, Nr. 47, Bl. TOR 3, Et. 3, Ap. 13, Jud. Alba",
      admin="Giurgiu Iulia-Elisabeta", contact="0748792524  ·  office@revo5c.ro", tva=False,
      pu="75.188,24", val="225.564,71"),
 dict(file="OFERTA_WM-ATV-016_MARIUS_CODE_WNK_SRL.pdf", nr="WM-ATV-016", inv="WM-ATV-010", firma="MARIUS CODE WNK SRL",
      cui="37707133", j="J2017000690010", euid="",
      adresa="Mun. Alba Iulia, Str. Ștefan Luchian, Nr. 15, Jud. Alba",
      admin="Vaida Elena", contact="", tva=True,
      pu="75.398,32", val="226.194,96", tvaval="47.500,94", tot="273.695,90"),
 dict(file="OFERTA_WM-ATV-017_ARIDE_RIDE_IT_SRL.pdf", nr="WM-ATV-017", inv="WM-ATV-011", firma="ARIDE RIDE IT SRL",
      cui="37932526", j="J1/978/2017", euid="",
      adresa="Mun. Alba Iulia, Str. Ștefan Luchian, Nr. 18, Jud. Alba",
      admin="Roș Radu Ioan", contact="", tva=True,
      pu="75.482,35", val="226.447,06", tvaval="47.553,88", tot="274.000,94"),
]

def build(C):
    def header_footer(c,doc):
        c.saveState()
        c.setFillColor(NAVY); c.rect(0,A4[1]-28*mm,A4[0],28*mm,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Arial-Bold",15); c.drawString(20*mm,A4[1]-13*mm,C["firma"])
        c.setFont("Arial",8.5)
        ids="CUI %s   ·   %s"%(C["cui"],C["j"]) + ("   ·   "+C["euid"] if C["euid"] else "")
        c.drawString(20*mm,A4[1]-18.5*mm,ids)
        c.drawString(20*mm,A4[1]-23*mm,C["adresa"]+"   ·   Administrator: "+C["admin"])
        c.setFillColor(GREY); c.setFont("Arial",7.5)
        foot="%s  ·  %s  ·  %s"%(C["firma"],C["cui"],C["j"]) + ("  ·  "+C["contact"] if C["contact"] else "")
        c.drawString(20*mm,12*mm,foot)
        c.drawRightString(A4[0]-20*mm,12*mm,"Proiect InoSocRural · Cod SMIS 311779 · valori exprimate în lei   ·   Pagina %d"%doc.page)
        c.restoreState()
    OUT=DST+"\\"+C["file"]
    doc=SimpleDocTemplate(OUT,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=33*mm,bottomMargin=16*mm,title="Oferta %s %s"%(C["nr"],C["firma"]))
    E=[]
    E.append(Paragraph("Proiect: InoSocRural – Întreprinderi sociale inovative în mediul rural din Regiunea Centru · Cod SMIS 311779",small))
    E.append(Spacer(1,4)); E.append(Paragraph("PROPUNERE TEHNICO-FINANCIARĂ",h1))
    E.append(Paragraph("Nr. %s / 04.05.2026"%C["nr"],bold)); E.append(Spacer(1,8))
    of=[Paragraph("<b>OFERTANT</b>",S("x",textColor=NAVY)),Paragraph("<b>%s</b>"%C["firma"],body),
        Paragraph(C["adresa"],body),Paragraph("CUI %s · %s"%(C["cui"],C["j"]),body),
        Paragraph("Reprezentant legal: %s, Administrator"%C["admin"],body)]
    if C["contact"]: of.append(Paragraph("Tel. "+C["contact"].replace("  ·  "," · "),body))
    ac=[Paragraph("<b>CĂTRE / ACHIZITOR</b>",S("y",textColor=NAVY)),Paragraph("<b>SC WILD MOTION S.R.L.</b>",body),
        Paragraph("Sat Hăpria, Strada Teilor, nr. 26, Comuna Ciugud, județul Alba, cod poștal 517243",body),Paragraph("CUI 52786696",body)]
    t=Table([[of,ac]],colWidths=[85*mm,85*mm]); t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,-1),LIGHT),("BOX",(0,0),(-1,-1),0.5,NAVY),("LINEBEFORE",(1,0),(1,0),0.5,NAVY),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8)]))
    E.append(t)
    E.append(Paragraph("Obiect achiziție",h2))
    E.append(Paragraph("Furnizare 3 bucăți CFMOTO CForce 1000, noi, sau echivalent, conform Invitației de participare nr. %s / 27.04.2026."%C["inv"],body))
    E.append(Paragraph("Centralizator financiar",h2))
    hdr=lambda s: Paragraph("<b>%s</b>"%s,S("hh",fontSize=8.5,leading=11,textColor=colors.white))
    prod=Paragraph("CFMOTO CForce 1000 – ATV 4x4, nou",body)
    if C["tva"]:
        rows=[[hdr("Nr."),hdr("Denumire produs"),hdr("Cant."),hdr("Preț unitar<br/>fără TVA"),hdr("Valoare<br/>fără TVA"),hdr("Valoare<br/>cu TVA (21%)")],
              ["1",prod,"3 buc.",C["pu"],C["val"],C["tot"]],
              ["",Paragraph("<b>Total fără TVA</b>",body),"","","",C["val"]+" lei"],
              ["",Paragraph("<b>TVA 21%</b>",body),"","","",C["tvaval"]+" lei"],
              ["",Paragraph("<b>TOTAL cu TVA inclus</b>",body),"","","",C["tot"]+" lei"]]
        ft=Table(rows,colWidths=[10*mm,66*mm,16*mm,26*mm,26*mm,26*mm]); lastcol=5
    else:
        rows=[[hdr("Nr."),hdr("Denumire produs"),hdr("Cant."),hdr("Preț unitar"),hdr("Valoare totală")],
              ["1",prod,"3 buc.",C["pu"],C["val"]],
              ["",Paragraph("<b>TVA</b>",body),"","","nu se aplică"],
              ["",Paragraph("<b>TOTAL DE PLATĂ</b>",body),"","",C["val"]+" lei"]]
        ft=Table(rows,colWidths=[10*mm,88*mm,18*mm,27*mm,27*mm]); lastcol=4
    ft.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("FONTNAME",(0,0),(-1,-1),"Arial"),("FONTSIZE",(0,0),(-1,-1),9),
     ("GRID",(0,0),(-1,1),0.4,colors.HexColor("#B0B8C4")),("ALIGN",(2,0),(-1,-1),"RIGHT"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
     ("BACKGROUND",(0,2),(-1,-1),LIGHT),("FONTNAME",(lastcol,2),(lastcol,-1),"Arial-Bold"),("LINEBELOW",(0,-1),(-1,-1),0.8,NAVY),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    E.append(ft)
    if not C["tva"]:
        E.append(Spacer(1,4)); E.append(Paragraph("<b>%s nu este plătitoare de TVA</b> – nu se aplică TVA (art. 310 din Legea nr. 227/2015 privind Codul fiscal). Prețul ofertat este valoare totală și finală."%C["firma"],S("nt",fontSize=8.5,leading=11,textColor=GREY)))
    E.append(Paragraph("Specificații tehnice ofertate",h2))
    for s in ["model ofertat: CFMOTO CForce 1000, produs nou;",
     "motor V-Twin, 4 timpi, capacitate 962,6 cmc; combustibil benzină; rezervor 26 l; răcire cu lichid; pornire electrică;",
     "putere omologată 84 CP; putere constructivă 90 CP; transmisie CVT;",
     "suspensie față dublu braț A; suspensie spate independentă; frâne hidraulice pe disc față/spate;",
     "anvelope față 27 X 9-14; anvelope spate 27 X 11-14; dimensiuni 2445 x 1270 x 1465 mm; greutate 443 kg; gardă la sol 300 mm;",
     "înmatriculabil, categorie permis B, omologare Euro 5+; garanție minimum 24 luni sau garanția comercială standard a producătorului, dacă aceasta este mai favorabilă achizitorului."]:
        E.append(Paragraph("—  "+s,S("li",leftIndent=10,firstLineIndent=-10,spaceAfter=2)))
    kv=[["Termen de livrare","maximum 30 de zile calendaristice de la semnarea contractului."],["Valabilitatea ofertei","30 de zile calendaristice de la data limită de depunere a ofertelor."],["Preț","ferm, nu se ajustează."]]
    kt=Table([[Paragraph("<b>%s</b>"%a,body),Paragraph(b,body)] for a,b in kv],colWidths=[40*mm,130*mm])
    kt.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),0.3,colors.HexColor("#B0B8C4")),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    E.append(Spacer(1,8)); E.append(kt); E.append(Spacer(1,8))
    E.append(Paragraph("Cu stimă,",body)); E.append(Spacer(1,4))
    E.append(Paragraph("<b>%s</b>,"%C["admin"],body)); E.append(Paragraph("Administrator · "+C["firma"],body)); E.append(Spacer(1,6))
    E.append(Paragraph("Semnătură și ștampilă: ______________________________",body))
    doc.build(E,onFirstPage=header_footer,onLaterPages=header_footer); print("OK",OUT)

for C in OFERTANTI: build(C)
