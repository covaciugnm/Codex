import docx, os, shutil
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
NAVY=RGBColor(0x1F,0x3A,0x5F); GREY=RGBColor(0x55,0x55,0x55); WHITE=RGBColor(255,255,255)
SCR=r"C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\b1650741-0498-4f07-886c-4c34f3dcc08a\scratchpad"
DST=r"Z:\00. Proiecte 2025\2025.06.12 Ionel Capota SES\3. Achizitie\2. Revo 5C SRL\REVO 5C -CFMoto"
NAME="Factura_nr_5_14.10.2026_REVO_5C_SRL_WILD_MOTION"
d=docx.Document()
sec=d.sections[0]; sec.page_height=Cm(29.7); sec.page_width=Cm(21)
sec.left_margin=sec.right_margin=Cm(1.5); sec.top_margin=Cm(1.1); sec.bottom_margin=Cm(1.0)
st=d.styles["Normal"]; st.font.name="Calibri"; st.font.size=Pt(10); st.element.rPr.rFonts.set(qn("w:eastAsia"),"Calibri")
st.paragraph_format.space_after=Pt(0)

def shade(cell,hexcol):
    tcPr=cell._tc.get_or_add_tcPr(); s=OxmlElement("w:shd"); s.set(qn("w:val"),"clear"); s.set(qn("w:color"),"auto"); s.set(qn("w:fill"),hexcol); tcPr.append(s)
def borders(tbl, color="B0B8C4", sz=4, inside=True):
    tblPr=tbl._tbl.tblPr; b=OxmlElement("w:tblBorders")
    edges=["top","left","bottom","right"]+(["insideH","insideV"] if inside else [])
    for e in edges:
        x=OxmlElement("w:"+e); x.set(qn("w:val"),"single"); x.set(qn("w:sz"),str(sz)); x.set(qn("w:color"),color); b.append(x)
    tblPr.append(b)
def noborders(tbl):
    tblPr=tbl._tbl.tblPr; b=OxmlElement("w:tblBorders")
    for e in ["top","left","bottom","right","insideH","insideV"]:
        x=OxmlElement("w:"+e); x.set(qn("w:val"),"nil"); b.append(x)
    tblPr.append(b)
def para(text="", bold=False, size=10, color=None, align=None, italic=False, space_after=0):
    p=d.add_paragraph(); r=p.add_run(text); r.bold=bold; r.italic=italic; r.font.size=Pt(size)
    if color: r.font.color.rgb=color
    if align is not None: p.alignment=align
    p.paragraph_format.space_after=Pt(space_after)
    return p
def cell_lines(cell, lines):
    cell.paragraphs[0].text=""
    first=True
    for ln in lines:
        txt,kw=(ln if isinstance(ln,tuple) else (ln,{}))
        p=cell.paragraphs[0] if first else cell.add_paragraph()
        r=p.add_run(txt); r.font.size=Pt(kw.get("size",9)); r.bold=kw.get("bold",False)
        if kw.get("color"): r.font.color.rgb=kw["color"]
        p.paragraph_format.space_after=Pt(kw.get("after",1))
        first=False

# ---- Antet
t=d.add_table(rows=1,cols=2); noborders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
c0,c1=t.rows[0].cells; c0.width=Cm(10.5); c1.width=Cm(6.9)
cell_lines(c0,[("REVO 5C S.R.L.",{"size":16,"bold":True,"color":NAVY,"after":2}),
 ("Furnizor",{"size":8,"color":GREY,"after":2}),
 "Sediu: Mun. Alba Iulia, Str. Septimius Severus, Nr. 47, Bl. TOR 3, Et. 3, Ap. 13, Jud. Alba",
 "CUI: 52226710   |   Nr. ONRC: J2025056106001",
 "EUID: ROONRC.J2025056106001",
 "Cont IBAN: RO51BTRLRONCRT0CZ4497001",
 "Banca: Banca Transilvania (SWIFT BTRLRO22)",
 "Telefon: 0748792524   |   E-mail: office@revo5c.ro"])
cell_lines(c1,[("FACTURĂ",{"size":20,"bold":True,"color":NAVY,"after":2}),
 ("Seria REVO   Nr. 5",{"size":11,"bold":True,"after":2}),
 ("Data emiterii: 14.10.2026",{"size":10,"after":2}),
 ("Data scadenței: 13.11.2026",{"size":10,"after":2}),
 ("Regim TVA: neplătitor de TVA",{"size":10,"after":2}),
 ("Moneda: RON",{"size":10,"after":2})])
for p in c1.paragraphs: p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
p=d.add_paragraph(); pPr=p._p.get_or_add_pPr(); bd=OxmlElement("w:pBdr"); b=OxmlElement("w:bottom")
b.set(qn("w:val"),"single"); b.set(qn("w:sz"),"12"); b.set(qn("w:color"),"1F3A5F"); bd.append(b); pPr.append(bd)
p.paragraph_format.space_after=Pt(8)

# ---- Cumparator + referinte
t=d.add_table(rows=1,cols=2); borders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
c0,c1=t.rows[0].cells; c0.width=Cm(9.6); c1.width=Cm(7.8); shade(c0,"EEF2F7"); shade(c1,"F7F7F7")
cell_lines(c0,[("CUMPĂRĂTOR",{"size":8,"bold":True,"color":NAVY,"after":3}),
 ("SC WILD MOTION S.R.L.",{"size":11,"bold":True,"after":2}),
 "Sediu: Sat Hăpria, Strada Teilor, nr. 26, Comuna Ciugud, județul Alba, cod poștal 517243",
 "CUI: 52786696   |   Nr. ONRC: J2025082656000",
 "Cont IBAN: RO42BTRLRONCRTODB3187901",
 "Banca: Banca Transilvania",
 "Telefon: 0769982977",
 "Reprezentant legal: CAPOTA NICOLAE-IOAN, Administrator"])
cell_lines(c1,[("REFERINȚE",{"size":8,"bold":True,"color":NAVY,"after":3}),
 ("Contract de furnizare produse nr. WM-ATV-033 / 18.05.2026",{"after":2}),
 ("Notă justificativă de atribuire nr. WM-ATV-022 / 11.05.2026",{"after":2}),
 ("Ofertă nr. WM-ATV-015 / 04.05.2026",{"after":2}),
 ("Proces-verbal de recepție nr. WM-ATV-036 / 14.10.2026",{"after":2}),
 ("Proiect: InoSocRural – Întreprinderi sociale inovative în mediul rural din Regiunea Centru, Cod SMIS 311779",{"after":2}),
 ("Contract de subvenție: PIDS/83/PIDS_P3/OP4/ESO4.1/PIDS_A12/311779",{"after":2}),
 ("Cod CPV: 34113200-4 – Vehicule pentru orice teren",{"after":2})])
for row in t.rows:
    for c in row.cells: c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
_sp=d.add_paragraph(); _sp.paragraph_format.space_after=Pt(2); _sp.add_run(' ').font.size=Pt(2)

# ---- Linii factura
hdr=["Nr. crt.","Denumirea produselor","U.M.","Cant.","Preț unitar","Valoare totală"]
w=[Cm(1.2),Cm(9.2),Cm(1.4),Cm(1.4),Cm(2.6),Cm(2.6)]
t=d.add_table(rows=2,cols=6); borders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,h in enumerate(hdr):
    c=t.rows[0].cells[i]; c.width=w[i]; shade(c,"1F3A5F"); c.paragraphs[0].text=""
    r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(8.5); r.font.color.rgb=WHITE
    c.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER; c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
desc=["CFMOTO CForce 1000 – ATV 4x4, nou",
      "Înmatriculabil, omologare Euro 5+, 962,6 cmc, 84 CP omologați, CVT",
      "Serii de identificare: REVO-WM-CFmoto1, REVO-WM-CFmoto2, REVO-WM-CFmoto3",
      "Contract WM-ATV-033 / 18.05.2026 · PV recepție WM-ATV-036 / 14.10.2026"]
vals=[["1"],desc,["buc."],["3"],["75.188,24"],["225.564,71"]]
for i,lines in enumerate(vals):
    c=t.rows[1].cells[i]; c.width=w[i]; c.paragraphs[0].text=""
    for j,ln in enumerate(lines):
        p=c.paragraphs[0] if j==0 else c.add_paragraph()
        r=p.add_run(ln); r.font.size=Pt(9 if j==0 else 8)
        if j>0: r.font.color.rgb=GREY; r.italic=True
        if i==1 and j==0: r.bold=True
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER if i in (0,2,3) else (WD_ALIGN_PARAGRAPH.RIGHT if i in (4,5) else WD_ALIGN_PARAGRAPH.LEFT)
    c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
_sp=d.add_paragraph(); _sp.paragraph_format.space_after=Pt(2); _sp.add_run(' ').font.size=Pt(2)

# ---- Totaluri
t=d.add_table(rows=3,cols=2); borders(t,color="1F3A5F"); t.alignment=WD_TABLE_ALIGNMENT.RIGHT
tot=[("Total valoare","225.564,71 lei",False),("TVA","nu se aplică",False),("TOTAL DE PLATĂ","225.564,71 lei",True)]
for i,(a,b,bold) in enumerate(tot):
    ca,cb=t.rows[i].cells; ca.width=Cm(5.2); cb.width=Cm(3.6)
    ca.paragraphs[0].text=""; ra=ca.paragraphs[0].add_run(a); ra.bold=bold; ra.font.size=Pt(11 if bold else 10)
    cb.paragraphs[0].text=""; rb=cb.paragraphs[0].add_run(b); rb.bold=bold; rb.font.size=Pt(11 if bold else 10); cb.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.RIGHT
    if bold:
        shade(ca,"1F3A5F"); shade(cb,"1F3A5F"); ra.font.color.rgb=WHITE; rb.font.color.rgb=WHITE
    else:
        shade(ca,"EEF2F7"); shade(cb,"EEF2F7")
_sp=d.add_paragraph(); _sp.paragraph_format.space_after=Pt(2); _sp.add_run(' ').font.size=Pt(2)
para("Total de plată în litere: douăsutedouăzecișicincimiicincisuteșaizecișipatru lei și 71 bani.",size=9,italic=True,color=GREY,space_after=2)
para("Mențiuni: REVO 5C S.R.L. nu este plătitoare de TVA – nu se aplică TVA (art. 310 din Legea nr. 227/2015 privind Codul fiscal). Preț ferm conform art. 4 din Contract. Plata prin ordin de plată în maximum 30 de zile de la primirea facturii, după semnarea procesului-verbal de recepție fără obiecțiuni. Produse noi, livrate la Sat Hăpria, Strada Teilor, nr. 26, Comuna Ciugud, jud. Alba, cu certificate de garanție (minimum 24 luni), documente de conformitate/omologare și documente pentru înmatriculare.",size=8,color=GREY,space_after=5)

# ---- Predare / primire
para("DATE PRIVIND EXPEDIȚIA, PREDAREA ȘI PRIMIREA PRODUSELOR",bold=True,size=9,color=NAVY,space_after=3)
t=d.add_table(rows=1,cols=2); borders(t); t.alignment=WD_TABLE_ALIGNMENT.CENTER
c0,c1=t.rows[0].cells; c0.width=Cm(8.7); c1.width=Cm(8.7); shade(c0,"F7F7F7"); shade(c1,"F7F7F7")
cell_lines(c0,[("PREDAT DE FURNIZOR",{"size":8,"bold":True,"color":NAVY,"after":3}),
 ("REVO 5C S.R.L.",{"bold":True,"after":2}),
 "Delegat: GIURGIU IULIA-ELISABETA – Administrator",
 "CI seria AX nr. 749798, eliberată de SPCLEP Alba Iulia la 05.07.2019",
 "CNP: 2880628011161",
 "Domiciliu: Mun. Alba Iulia, Str. Cloșca nr. 6, bl. 4, sc. E, et. 4, ap. 66, jud. Alba",
 "Mijloc de transport: autovehicul AB10ZEN",
 "Data expedierii: 14.10.2026",
 ("",{"after":6}),
 "Administrator – semnătura și ștampila: ______________________"])
cell_lines(c1,[("PRIMIT DE CUMPĂRĂTOR",{"size":8,"bold":True,"color":NAVY,"after":3}),
 ("SC WILD MOTION S.R.L.",{"bold":True,"after":2}),
 "Reprezentant: CAPOTA NICOLAE-IOAN – Administrator",
 "CI nr. AB1006888, eliberată de SPCLEP Alba Iulia la 07.08.2025",
 "CNP: 1810515011155",
 "Locul primirii: Sat Hăpria, Strada Teilor, nr. 26, Comuna Ciugud, jud. Alba",
 "Data primirii: 14.10.2026",
 ("",{"after":6}),
 "Administrator – semnătura și ștampila: ______________________"])

_end=d.add_paragraph(); _end.paragraph_format.space_after=Pt(0); _end.paragraph_format.line_spacing=Pt(1); _end.add_run(" ").font.size=Pt(1)
sec.footer_distance=Cm(0.5); sec.header_distance=Cm(0.5)
fp0=sec.footer.paragraphs[0]; fp0.alignment=WD_ALIGN_PARAGRAPH.CENTER
r0=fp0.add_run("Factura circulă fără semnătură și ștampilă conform art. 319 alin. (29) din Legea nr. 227/2015 privind Codul fiscal. Întocmit de: GIURGIU IULIA-ELISABETA, Administrator. Emisă în 2 exemplare."); r0.font.size=Pt(7); r0.font.color.rgb=GREY
fp=sec.footer.add_paragraph(); fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=fp.add_run("REVO 5C S.R.L.  ·  CUI 52226710  ·  J2025056106001  ·  Factura seria REVO nr. 5 / 14.10.2026  ·  Pagina 1/1"); r.font.size=Pt(7.5); r.font.color.rgb=GREY
local=os.path.join(SCR,NAME+".docx"); d.save(local); print("DOCX",local)

import win32com.client, pythoncom
pythoncom.CoInitialize()
word=win32com.client.DispatchEx("Word.Application"); word.Visible=False
doc=word.Documents.Open(local); doc.ExportAsFixedFormat(os.path.join(SCR,NAME+".pdf"),17); doc.Close(False); word.Quit()
for ext in (".docx",".pdf"):
    shutil.copy2(os.path.join(SCR,NAME+ext), os.path.join(DST,NAME+ext)); print("->",os.path.join(DST,NAME+ext))
