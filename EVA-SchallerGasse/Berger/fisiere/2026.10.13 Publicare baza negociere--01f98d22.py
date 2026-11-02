from pathlib import Path
import json, hashlib, shutil
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK = ROOT / '00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
OUT = ROOT / '00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH'
DATE = '2026.10.13'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def text(x):
    if x is None: return ''
    if isinstance(x, str): return x
    if isinstance(x, list): return '\n'.join(text(v) for v in x)
    if isinstance(x, dict): return '\n'.join(f'{k}: {text(v)}' for k,v in x.items())
    return str(x)

def field(p, name):
    for typ,val in [('begin',None),('instr',name),('end',None)]:
        r=p.add_run(); e=OxmlElement('w:instrText' if typ=='instr' else 'w:fldChar')
        if typ=='instr': e.text=' '+val+' '; e.set(qn('xml:space'),'preserve')
        else: e.set(qn('w:fldCharType'),typ)
        r._r.append(e)

def doc(title, landscape=False):
    d=Document(); s=d.sections[0]
    s.page_width=Cm(29.7 if landscape else 21); s.page_height=Cm(21 if landscape else 29.7)
    s.left_margin=s.right_margin=Cm(1.5 if landscape else 1.8)
    s.top_margin=Cm(1.5 if landscape else 1.8); s.bottom_margin=Cm(1.5 if landscape else 1.8)
    s.footer_distance=Cm(.65); s.header_distance=Cm(.65)
    n=d.styles['Normal']; n.font.name='Calibri'; n.font.size=Pt(11); n.font.color.rgb=RGBColor(0,0,0)
    n.paragraph_format.space_after=Pt(5); n.paragraph_format.line_spacing=1.05; n.paragraph_format.widow_control=True
    lg=OxmlElement('w:lang');lg.set(qn('w:val'),'ro-RO');n._element.get_or_add_rPr().append(lg)
    for st,size in [('Title',19),('Heading 1',14),('Heading 2',12)]:
        a=d.styles[st];a.font.name='Calibri';a.font.size=Pt(size);a.font.bold=True;a.font.color.rgb=RGBColor(0,0,0)
        a.paragraph_format.space_before=Pt(9);a.paragraph_format.space_after=Pt(5);a.paragraph_format.keep_with_next=True
        if a._element.pPr is not None:
            for e in list(a._element.pPr):
                if e.tag==qn('w:pBdr'):a._element.pPr.remove(e)
    d.core_properties.title=title;d.core_properties.subject='Cerințe comune ale A&C Wohnart pentru negocierea BERGER și PECH'
    d.core_properties.author='A&C Wohnart'
    d.add_paragraph(title,'Title')
    d.add_paragraph('Schallergasse 35, 1120 Wien | 2026.10.13 | Bază de negociere')
    p=s.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run('2026.10.13 | Negociere | ');field(p,'PAGE');p.add_run(' / ');field(p,'NUMPAGES')
    for r in p.runs:r.font.name='Calibri';r.font.size=Pt(8.5)
    return d

def para(d, body, label=None):
    p=d.add_paragraph()
    if label:p.add_run(label+' ').bold=True
    p.add_run(text(body));return p

def tbl(d, headers, rows, widths, font=10):
    t=d.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Cm(w)
    for c,x in zip(t.rows[0].cells,headers):c.text=text(x)
    for vals in rows:
        assert len(vals)==len(headers)
        for c,x in zip(t.add_row().cells,vals):c.text=text(x)
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
        if ri==0:pr.append(OxmlElement('w:tblHeader'))
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
            cp=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D7DCE0');b.append(e)
            cp.append(b)
            sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8EDF1' if ri==0 else ('F7F9FA' if ri%2==0 else 'FFFFFF'));cp.append(sh)
            m=OxmlElement('w:tcMar')
            for side in ['top','bottom','left','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'85');e.set(qn('w:type'),'dxa');m.append(e)
            cp.append(m)
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(2);p.paragraph_format.space_before=Pt(1)
                p.paragraph_format.line_spacing=1.02;p.paragraph_format.keep_with_next=ri==0;p.paragraph_format.widow_control=True
                for r in p.runs:r.font.name='Calibri';r.font.size=Pt(font);r.font.bold=ri==0
    p=d.add_paragraph();p.paragraph_format.space_after=Pt(2)
    return t

def href(d, label, url):
    p=d.add_paragraph();p.add_run(label+' ')
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),d.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True))
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr');co=OxmlElement('w:color');co.set(qn('w:val'),'1F4E79');pr.append(co);r.append(pr)
    te=OxmlElement('w:t');te.text=url;r.append(te);h.append(r);p._p.append(h)
    p.paragraph_format.space_after=Pt(3)
    for rr in p.runs:rr.font.size=Pt(9)

def assert_frozen():
    f=read(WORK/f'{DATE} Surse inghetate audit R05.json')
    for r in f['surse']: assert sha(ROOT/r['cale'])==r['sha256'], r['cale']

assert_frozen()
matrix_file=WORK/f'{DATE} Cerinte comune negociere matrice.json'
objections_file=WORK/f'{DATE} Obiectii negociere reformulate.json'
firms_file=WORK/f'{DATE} Date firme pentru negociere.json'
matrix=read(matrix_file);objections=read(objections_file);firms=read(firms_file)
field_labels={
 'legal_name':'Denumire juridică','legal_form':'Formă juridică','registered_seat':'Sediu statutar',
 'business_address':'Adresă de activitate','correspondence_address':'Adresă pentru corespondență',
 'firmenbuchnummer':'Număr Firmenbuch','firmenbuchgericht':'Instanța Firmenbuch','uid':'Cod TVA UID',
 'commercial_representatives':'Reprezentanți comerciali','commercial_representative':'Reprezentant comercial',
 'published_commercial_representatives':'Administratori publicați','published_representation_mode':'Mod de reprezentare publicat',
 'contact_email':'Email','contact_phone':'Telefon','contact_mobile':'Telefon mobil','gisa':'Număr GISA',
 'gln':'GLN administrație','euid':'EUID','gewerberechtlicher_geschaeftsfuehrer':'Responsabil din dreptul profesiei',
 'trade':'Activitate publicată','website':'Site','project_contact':'Contact proiect','offer_prepared_by':'Pregătirea ofertei',
 'secretariat_email':'Email secretariat','professional_statement':'Abilitare declarată'}
firm_sources={s['id']:s for s in firms['sources']}
firm_public=[]
for key,records in firms['companies'].items():
    public=[]
    for r in records:
        value='Neidentificat' if r['value'] is None else text(r['value'])
        if isinstance(r['value'],list) and r['value'] and isinstance(r['value'][0],dict):
            value='\n'.join(f"{v['name']}, {v['role']}; {v['authority']}" for v in r['value'])
        public.append({'camp':field_labels.get(r['field'],r['field']), 'valoare':value,
                       'sursa_publica':', '.join(r['sources'])+'; '+r.get('location',''),
                       'statut':r.get('status','')+('\n'+r['note'] if r.get('note') else '')})
    name=next(r['value'] for r in records if r['field']=='legal_name')
    used=set(s for r in records for s in r['sources'])
    firm_public.append({'nume':name,'campuri':public,
                        'surse_online':[{'titlu':s['id']+' '+s.get('title','Sursă publică'),'url':s['url']} for s in firms['sources'] if 'url' in s and s['id'] in used]})
firms['firme']=firm_public
assert len(matrix['matrice'])>=60
assert len(objections['mapare_30'])==30
OUT.mkdir(exist_ok=True)
for p in [matrix_file,objections_file,firms_file]:
    dest=OUT/p.name
    if not dest.exists():shutil.copy2(p,dest)
    assert sha(p)==sha(dest)

d=doc('Cerințe comune de negociere pentru BERGER și PECH',True)
para(d,'Solicităm același pachet tehnic și contractual de la ambii ofertanți, la valorile de bază de 45.000 EUR net pentru BERGER și 69.300 EUR net pentru PECH. Cerințele de mai jos sunt poziția A&C Wohnart pentru negociere; contractele R05 sunt documentele de pornire. Diferențele de scop, termene, numărare a vizitelor și protecții contractuale sunt tratate explicit pentru uniformizare.')
para(d,'Scopul comun include proiectarea completă a structurii, documentația de execuție, asistența și verificările PI, contribuțiile legale la finalizare și Bauwerksbuch pentru clădirea existentă și intervențiile noi. Se solicită 18 luni ale fazei de execuție de la B0 real, cu planificarea T0 separată, 12 vizite fizice incluse și până la 6 suplimentare plătite. BauKG, managementul general REALIG, ÖBA generală și Bauführung sunt excluse.')
para(d,'Diferențele economice sunt valorile și tarifele prevăzute distinct pentru fiecare. Suplimentul BERGER de 2.000/12 EUR net este o propunere AG nouă, derivată; PECH a ofertat 450 EUR net pentru o recepție suplimentară, iar aplicarea acestui tarif la pachetul comun este propusă. Nu urmărim majorarea cerinței de asigurare; datele administrative și profesionale se completează separat, cu respectarea obligațiilor legale aplicabile. Același criteriu primește aceeași cerință AG și aceeași probă de îndeplinire pentru ambii.')
para(d,'Prestațiile suplimentare față de scop se aprobă în scris, cu conținut, tarif și plafon. Compensațiile întemeiate pe lege, inclusiv decontul și împiedicările potrivit §1168 ABGB, se analizează separat pe cauză și dovezi. Regula comenzii nu înlătură aceste drepturi sau §1170b ABGB atunci când este aplicabil.')
d.add_paragraph('Comparația economică','Heading 1')
tbl(d,['Element','BERGER','PECH','Cerința comună de negociere'],[
 ['Preț de bază','45.000 EUR net\n54.000 EUR cu TVA','69.300 EUR net\n83.160 EUR cu TVA','Același pachet de servicii și aceleași condiții de prestare. Menținerea totalului propus pentru fiecare.'],
 ['Vizite fizice incluse','12 solicitate în prețul de bază\nOferta inițială avea max. 8 Betreuungstermine','12 solicitate în prețul de bază\nOferta inițială avea 12 Abnahmen','Aceeași definiție, același registru și același plan de etape; o întâlnire digitală nu consumă o vizită fizică.'],
 ['Vizite suplimentare 13–18','2.000 /12 EUR net pe vizită\nPropunere AG derivată\nMax. 6 =1.000 EUR net','450 EUR net pe vizită\nTarif ofertat, propus pentru pachetul comun\nMax. 6 =2.700 EUR net','Până la 6, numai efectiv comandate și prestate conform regulii comune. Același conținut; tarife diferite.'],
 ['Total cu toate cele 6 opțiuni','46.000 EUR net\n55.200 EUR cu TVA','72.000 EUR net\n86.400 EUR cu TVA','Buget condiționat de executarea tuturor opțiunilor; nu se facturează automat. Costurile distincte nu pot fi introduse tacit.'],
 ['Rotunjire suplimente BERGER','Cumulat: rotunjire a n ×2.000 /12 la 2 zecimale','Nu este necesară:450 EUR fix','Pentru6 BERGER totalul exact este1.000 EUR net, nu1.000,02 EUR.'],
], [4.1,5.2,5.2,12.2],10.5)
d.add_paragraph('Aceleași repere de livrare și de plată','Heading 1')
para(d,'Propunem aceleași evenimente E1–E7 pentru ambii. Fiecare își alocă sumele din propriile poziții la aceste evenimente, cu reconcilierea exactă a totalului de bază. Scadența privește numai prestația completă, efectiv predată și verificabilă; nu avansul pentru PI sau finalizarea încă neefectuată. Planificarea D1–D5 este distinctă de cele 18 luni de execuție de la B0.')
tbl(d,['Reper comun','Livrabil și probă comună','Termen propus identic'],[
 [x['id'],x['livrabil_comun'],x['termen_propusa']] for x in objections['repere_facturare_comune']
],[3.2,16.3,7.2],10.5)
d.add_paragraph('Diferențe concrete care trebuie uniformizate','Heading 1')
diffrows=[]
for x in matrix['diferente_reale']:
    diffrows.append([x.get('id',''),x.get('tema',x.get('criteriu','')),text(x.get('berger','')),text(x.get('pech','')),text(x.get('pozitie_comuna',x.get('pozitie_negociere',x.get('cerinta_comuna',''))))])
tbl(d,['ID','Criteriu','Text BERGER actual','Text PECH actual','Poziție comună AG'],diffrows,[1.1,3.3,6.3,6.3,9.7],10)

d.add_paragraph('Matricea explicită pe criterii și faze','Heading 1')
para(d,'Pentru fiecare criteriu, coloana centrală stabilește ce cerem de la ambii. Coloanele BERGER și PECH descriu oferta inițială și textul R05; ultima coloană explică diferența și poziția de negociere. O diferență față de ofertă justifică o discuție concretă despre pachet, fără a elimina cerința AG.')
groups={}
for x in matrix['matrice']:groups.setdefault(x['capitol_faza'],[]).append(x)
for group,items in groups.items():
    d.add_paragraph(group,'Heading 2')
    rows=[]
    for x in items:
        c=x['celule_publice']
        criterion=text(c['criteriu'])
        if not criterion.startswith(x['id']):criterion=x['id']+'\n'+criterion
        party_cells=[]
        for party in ['berger','pech']:
            pp=x[party]
            refs='; '.join(rr['referinta'] for rr in pp['referinte_r05'])
            party_cells.append('Oferta inițială: '+text(pp['original'])+'\nR05 actual: '+text(pp['r05_rezumat'])+'\nClauze: '+refs)
        rows.append([criterion,text(c['cerinta_comuna']),party_cells[0],party_cells[1],text(c['diferenta_pozitie'])])
    tbl(d,['Criteriu','Cerință identică pentru ambii','BERGER ofertă și R05','PECH ofertă și R05','Diferența și poziția AG'],rows,[2.5,8.5,5.3,5.3,5.1],10)

# Datele firmelor sunt publicate într-o anexă distinctă de cerințele tehnice.
d.add_paragraph('Datele firmelor și sursele de completare','Heading 1')
para(d,'Datele de identificare au fost căutate în documentele existente și în surse publice. Se disting datele documentate de informațiile publicate online, precum și reprezentarea comercială de funcția profesională. Documentele originale și contractele R05 sunt păstrate.')
for company in firms['firme']:
    d.add_paragraph(company['nume'], 'Heading 2')
    tbl(d,['Câmp','Valoare','Sursă și nivelul verificării'],[
        [x['camp'],text(x['valoare']),text(x['sursa_publica'])+'\n'+text(x.get('statut',''))]
        for x in company['campuri']
    ],[4.3,8.7,13.7],10)
    for s in company.get('surse_online',[]):href(d,s.get('titlu','Sursă publică'),s['url'])
    if company.get('observatii'):para(d,company['observatii'])
d.add_paragraph('Registrul surselor de identificare','Heading 2')
tbl(d,['ID','Document sau sursă publică','Data și limitele sursei'],[
    [s['id'],s.get('path',s.get('url','')),s.get('document_date',s.get('consulted','2026.10.13'))+'\n'+s.get('limit',s.get('role',''))]
    for s in firms['sources']
],[1.2,14.0,11.5],9.5)
d.add_paragraph('Surse și trasabilitate','Heading 1')
para(d,'Ofertele originale BERGER din 2026.08.17 și PECH AN01 din 2026.09.17, cererea tehnică AG din 2026.07.20, documentația proiectului și contractele R05 sunt sursele comparației. Rapoartele de audit anterioare păstrează analiza juridică și citatele complete; prezenta matrice reformulează poziția comună de negociere.')
para(d,f"Acoperire: {len(matrix['matrice'])} criterii explicite. Fișierul JSON «2026.10.13 Cerinte comune negociere matrice.json» păstrează citatele germane, referințele pe clauze și maparea la cele 60 de teme și 401 de componente din auditul anterior.")
para(d,'Actualizările și propunerile din acest document nu sunt introduse în contractele R05 și nu au fost trimise ofertanților. Pentru răspunsuri comparabile, fiecare ofertant trebuie să indice expres, pe același ID, dacă include cerința în preț sau propune o rezervă cuantificată.')
matrix_doc=OUT/f'{DATE} Matrice explicita cerinte comune BERGER PECH.docx'
assert not matrix_doc.exists();d.save(matrix_doc)

d=doc('Poziții comune de negociere și obiecții BERGER și PECH')
para(d,'Solicităm același conținut și aceleași condiții ambilor ofertanți, la valorile propuse pentru fiecare. Documentul pregătește răspunsurile la obiecții și stabilește ce trebuie clarificat în scris. Existența unei cerințe mai ample decât oferta inițială este o poziție legitimă de negociere; evaluăm separat fezabilitatea, prețul și obligațiile legale.')
para(d,'Cerințele tehnice, livrabilele, calendarul, numărarea vizitelor, condițiile de plată și protecțiile contractuale trebuie uniformizate. Valorile ofertelor și tarifele suplimentare rămân diferențe economice. Nu insistăm pe creșterea asigurării; completarea documentelor administrative are rol secundar.')
d.add_paragraph('Reguli pentru o negociere comparabilă','Heading 1')
para(d,objections['principii_comune'])
for x in objections['puncte_negociere']:
    d.add_paragraph(x['id']+' '+x['tema'],'Heading 1')
    para(d,x['de_ce_ar_obiecta'],'Obiecția posibilă')
    para(d,x['evaluare_echilibrata'],'Evaluarea')
    para(d,x['pozitie_comuna_AG'],'Cerința identică AG')
    tbl(d,['Ce păstrăm','Ce poate fi negociat'],[
        ['Cerința AG\n'+text(x['ferm_AG']),'Economie și organizare\n'+text(x['negociabil_economic'])],
        ['Reguli legale aplicabile\n'+text(x['imperativ_legal']),'Răspuns scris concret\n'+text(x['raspuns_scris_cerut'])],
    ],[8.7,8.7],10.5)
    if x.get('formulare_comuna_DE'):
        para(d,x['formulare_comuna_DE'],'Formulare comună propusă în germană')
    para(d,x['referinte_R05'],'Referințe')
d.add_paragraph('Repere comune pentru livrare și facturare','Heading 1')
para(d,'Aceleași repere E1–E7 se propun ambilor. Sumele se alocă din pozițiile proprii și trebuie să reconcilieze totalul; diferă valorile, nu dovada prestării sau condiția scadenței. Partea BWB cu termen legal anterior se tratează separat, numai după livrarea completă a părții respective.')
tbl(d,['Reper','Livrabil și dovada prestării','Termen comun propus'],[
 [x['id'],x['livrabil_comun'],x['termen_propusa']] for x in objections['repere_facturare_comune']
],[2.6,10.3,4.5],10)
d.add_paragraph('Formatul comun de răspuns al ofertanților','Heading 1')
response=objections['format_raspuns_comun']
para(d,response['statusuri'],'Aceleași trei răspunsuri pe criteriu')
para(d,response['campuri_obligatorii'],'Câmpuri de completat')
para(d,response['reguli'],'Reguli ale răspunsului')
para(d,response['declaratie_comuna_DE'],'Declarație propusă în germană')
para(d,response['exemplu_supliment_DE'],'Cerere de supliment în germană')
tbl(d,['ID criteriu','Răspunsul ofertantului'],[
    ['INCLUS','Confirmă că întreaga cerință, livrabilul, termenul și proba de îndeplinire sunt incluse în totalul propus.'],
    ['REZERVĂ CONCRETĂ','Redă exact elementul exceptat, motivul, soluția alternativă și efectul asupra prețului/calendarului. Trimiterea generică la AGB nu este un răspuns pe criteriu.'],
    ['PREȚ','Indică suma netă/TVA și dacă este inclusă, tarif suplimentar, plafon sau preț ferm pentru o comandă distinctă.'],
    ['TERMEN','Confirmă data/triggerul comun sau propune o dată relativă exactă, cu dependențele concrete.'],
    ['PERSOANĂ ȘI DOCUMENT','Numește responsabilul eligibil pentru funcția cerută și documentul de predare/semnare care probează prestarea.'],
    ['ACCEPTARE PACHET','Confirmă lista finală de excepții și documentele prioritare. Fiecare rezervă trebuie rezolvată în aceeași matrice, fără excluderi tacite.'],
],[4.0,13.4],10.5)
d.add_paragraph('Concordanță cu observațiile anterioare','Heading 1')
para(d,'Cele 30 de obiecții anterioare sunt consolidate în punctele de mai sus. Corespondența completă este păstrată în JSON. Cerințele noi sunt tratate drept obiectul negocierii; riscurile juridice și diferențele reale de text sunt păstrate ca puncte de rezolvat.')
tbl(d,['Obiecția anterioară','Punct nou'],[[x.get('vechi',x.get('id','')),x.get('nou',x.get('punct',''))] for x in objections['mapare_30']],[8.7,8.7],10)
d.add_paragraph('Surse pentru regulile juridice','Heading 1')
for s in objections['surse']:
    if s.get('url'):href(d,s.get('id',s.get('titlu','Sursă')),s['url'])
para(d,'Contractele R05 sunt documentele de pornire și rămân nemodificate. Nu a fost transmisă o cerere, semnat un contract ori făcută o plată prin această reformulare.')
objections_doc=OUT/f'{DATE} Obiectii reformulate si pozitii comune negociere.docx'
if not objections_doc.exists():d.save(objections_doc)
else:
    first=read(OUT/f'{DATE} Export obiectii negociere pentru verificare.json')
    assert sha(objections_file)==first['sursa_json_sha256']
    assert sha(objections_doc)==first['docx_sha256']

manifest={'data':DATE,'statut':'BAZĂ DE NEGOCIERE — cerințe comune, contracte R05 nemodificate',
 'documente':[{'prestator':'Matrice comună','docx':matrix_doc.relative_to(ROOT).as_posix()},
              {'prestator':'Obiecții reformulate','docx':objections_doc.relative_to(ROOT).as_posix()}],
 'surse':[{'cale':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [matrix_file,objections_file,firms_file]],
 'numar_criterii':len(matrix['matrice']),'numar_puncte_negociere':len(objections['puncte_negociere'])}
man=OUT/f'{DATE} Export baza negociere pentru verificare.json'
assert not man.exists();man.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert_frozen()
print(json.dumps(manifest,ensure_ascii=False))
