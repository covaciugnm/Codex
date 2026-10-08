from pathlib import Path
import json,html,shutil,csv,re
import report_data as d
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
P=Path(__file__).parent; O=P/'package'; R=O/'01_Raport';R.mkdir(exist_ok=True)
reg=[x for x in json.loads((O/'registru_documentatii.json').read_text(encoding='utf8')) if not x['id'].startswith('V')]
for x in reg:
 if x.get('local') and not x.get('error'):
  marker=O/x['group']/(x['id']+'_INDISPONIBIL.txt')
  if marker.exists():marker.unlink()
refs={x.stem.replace('_ref',''):json.loads(x.read_text()) for x in (P/'evidence').glob('*_ref.json')}
for page in d.PAGES:
 for i,(kind,b) in enumerate(page['blocks']):
  if kind=='p':page['blocks'][i]=(kind,b.replace('ERPNext ajunge la 83,0 și MFG2 la 80,0','ERPNext ajunge la 84,0 și MFG2 la 78,0'))
  if kind=='t':
   for row in b['rows']:
    if row[0]=='Tryton' and row[1]=='Documentația oficială latest':row[1]='8.2.0 production (PyPI); manual latest';row[2]='Distribuția sursă production 8.2.0 descărcată; toate modulele trebuie fixate pe aceeași familie.'
for id,title,path in d.SOURCES_EVA:
 reg.append(dict(id=id,title=title,url=d.BASE+path,group='08_EVA',note='Cod privat inspectat; legătură la commit, fără republicarea sursei brute.'))
# Preserve public code evidence and provenance, never private audit files.
E=O/'09_Dovezi_cod';E.mkdir(exist_ok=True)
for n in refs:
 if (P/'evidence'/n).exists():shutil.copytree(P/'evidence'/n,E/n,dirs_exist_ok=True)
 for suffix in ['_ref.json','_paths.txt']:
  f=P/'evidence'/(n+suffix)
  if f.exists():shutil.copy2(f,E/f.name)
d.page('Ghidul bibliotecii locale și limitele descărcărilor')
d.p('Fișierul Comparatie_ERP_Productie.xlsx este matricea de lucru: funcții pe rânduri, aplicații și module pe coloane, versiuni și surse în foi distincte. Bifa indică o capabilitate documentată, nu o instalare și testare în mediul EVA. Filtrați coloana Capitol și păstrați vizibile coloanele de identificare când derulați orizontal.')
d.p('INDEX.html și README.md deschid biblioteca. Subfolderele 02–07 păstrează documentațiile oficiale disponibile, sursele originale comprimate, manualele și arhivele de cod. 09_Dovezi_cod conține probe publice de implementare și referințe fixate. Registrul JSON și fila Surse din Excel indică pentru fiecare document URL-ul, starea transferului și calea locală.')
d.p(f"La generare: {len(reg)} referințe în registru; {sum(bool(x.get('local')) for x in reg)} cu copie locală; {sum(bool(x.get('error')) for x in reg)} transferuri nereușite. Referințele EVA sunt linkuri private, nu manuale descărcate. O descărcare reușită poate reprezenta o pagină sau o arhivă cu mai multe fișiere.")
d.p('Copiile HTML de lectură păstrează textul și legăturile; imaginile și elementele interactive sunt eliminate din această vedere. Fișierul original.html.gz păstrează răspunsul HTML original, dar nu toate resursele externe. Manualele PDF și arhivele de surse sunt fișiere originale complete când transferul a reușit. Pagini blocate HTTP 403/404 sau timeout rămân explicit indisponibile; biblioteca nu este prezentată drept o oglindă integrală a tuturor site-urilor.')
d.p('Documentația Odoo include și funcții Enterprise; ea nu reprezintă dovada includerii în Community. Matricea Community se bazează pe codul public identificat. Manualele latest/stable sunt capturi de documentație, nu promisiuni privind comportamentul fiecărui release.')
d.p('Drepturile documentațiilor și codului aparțin proiectelor originale. Sunt păstrate atribuirea, legăturile și licențele disponibile. Codul privat EVA, cheile SSH, datele de clienți și jurnalele de autentificare nu sunt incluse în pachet.')
for label,ids in [('Dovezi principale pentru aplicații',['SRC_idempiere','SRC_mfg2','SRC_libero','SRC_erpnext','SRC_odoo','SRC_ofbiz','SRC_dolibarr','T01','TRYTON_SDIST']),('Dovezi EVA și documentație operațională',['V01','V02','V03','V04','V05','V06','ASSET_AssetMaintenance-iDempiere','E01','T01','F01','D02'])]:
 d.page(label)
 for sid in ids:
  q=next((r for r in reg if r['id']==sid),None)
  if q:d.h(sid+' — '+q['title']);d.p(q['url'])

esc=lambda s:html.escape(str(s))
md=['# Managementul producției — EVA și iDempiere','\nAudit documentar și static, 8 octombrie 2026. Vezi și [Excel comparativ](Comparatie_ERP_Productie.xlsx).\n']
ht=['<!doctype html><html lang="ro"><meta charset="utf-8"><title>ERP Producție — analiză</title><style>body{max-width:1180px;margin:40px auto;font:16px/1.55 Arial;color:#1c2c40;padding:20px}h1,h2{color:#183d63}table{width:100%;border-collapse:collapse;font-size:14px}th{background:#203e60;color:white}td,th{padding:9px;border-bottom:1px solid #d8e0e8;text-align:left;vertical-align:top}tr:nth-child(even){background:#f1f5f9}a{color:#075ba1}section{margin:55px 0}nav{columns:2}@media print{section{break-before:page}}</style><h1>Managementul producției</h1><p>EVA • iDempiere • cinci alternative open-source | 8 octombrie 2026</p><p><a href="Comparatie_ERP_Productie.xlsx">Descarcă Excel</a> · <a href="Raport_ERP_Productie.pdf">Descarcă PDF</a> · <a href="../INDEX.html">Biblioteca surselor</a></p><nav>']
for i,page in enumerate(d.PAGES,1):ht.append(f'<p><a href="#c{i}">{i}. {esc(page["title"])}</a></p>')
ht.append('</nav>')
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'));pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
styles={'title':ParagraphStyle('title',fontName='Arial-Bold',fontSize=20,leading=24,spaceAfter=16,textColor=colors.HexColor('#183d63')),'h':ParagraphStyle('h',fontName='Arial-Bold',fontSize=11,leading=14,spaceBefore=10,spaceAfter=6,textColor=colors.HexColor('#183d63')),'p':ParagraphStyle('p',fontName='Arial',fontSize=9.2,leading=13,spaceAfter=9),'cell':ParagraphStyle('cell',fontName='Arial',fontSize=8,leading=10.5),'th':ParagraphStyle('th',fontName='Arial-Bold',fontSize=8,leading=10.5,textColor=colors.white)}
def pp(s,style='p'):
 t=esc(s)
 if str(s).startswith('https://'):t='<link href="'+esc(s)+'" color="#075ba1">'+t+'</link>'
 return Paragraph(t,styles[style])
story=[]
for i,page in enumerate(d.PAGES,1):
 if i>1:story.append(PageBreak())
 story.append(pp(f'{i:02d}  '+page['title'],'title'));md.append('\n## '+str(i)+'. '+page['title']+'\n');ht.append(f'<section id="c{i}"><h2>{i}. {esc(page["title"])}</h2>')
 for kind,b in page['blocks']:
  if kind in ['p','h']:
   story.append(pp(b,kind));md.append(('### ' if kind=='h' else '')+b+'\n');ht.append(f'<{"h3" if kind=="h" else "p"}>{esc(b)}</{"h3" if kind=="h" else "p"}>')
  else:
   raw=[b['head']]+b['rows']; widths=b.get('widths') or [1]*len(b['head']); widths=[495*x/sum(widths) for x in widths]
   t=Table([[pp(x,'th' if j==0 else 'cell') for x in row] for j,row in enumerate(raw)],colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#203e60')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),0.7,colors.HexColor('#203e60'))]));story.extend([t,Spacer(1,10)])
   md+=['| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in [b['head'],['---']*len(b['head'])]+b['rows']];md.append('')
   ht.append('<table>'+''.join('<tr>'+''.join(f'<{"th" if j==0 else "td"}>{esc(x)}</{"th" if j==0 else "td"}>' for x in row)+'</tr>' for j,row in enumerate(raw))+'</table>')
 ht.append('</section>')
def footer(c,doc):
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#607286'));c.drawString(50,27,'EVA / ERP Producție • Audit documentar • 08.10.2026');c.drawRightString(545,27,str(doc.page));c.setStrokeColor(colors.HexColor('#d8e0e8'));c.line(50,40,545,40)
SimpleDocTemplate(str(R/'Raport_ERP_Productie.pdf'),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50,topMargin=47,bottomMargin=55,title='Managementul producției — EVA și iDempiere',author='Analiză tehnică pentru CESIRO').build(story,onFirstPage=footer,onLaterPages=footer)
(R/'Raport_ERP_Productie.md').write_text('\n'.join(md),encoding='utf8');(R/'Raport_ERP_Productie.html').write_text(''.join(ht)+'</html>',encoding='utf8')

# Native plugins are assessed as add-ons, not as complete ERP installations.
mods=[
('MFG2','13.0.0 / 7f353732ba27','GPLv2','SRC_mfg2','MRP, CRP, ordine, rute, consum/recepție, colectori cost; build pe EVA obligatoriu.'),
('Libero','14.0.0 / b2adfea08d50','GPLv2','SRC_libero','Familia manufacturing; master 14 nu este validat pentru EVA 13.'),
('Asset Maintenance','2.1.0.3; iD13 declarat','Verificare pachet','I02','Planuri, contoare, sarcini, cereri și ordine mentenanță.'),
('BOMDrop','Versiune exactă neconfirmată','Verificare pachet','I05','Configurare componente obligatorii/opționale și variante.'),
('AutoBOMOrder','Compatibilitate istorică 4.1','Verificare pachet','I06','Expansiune BOM în comanda de vânzare.'),
('CopyBOMToProduct','Compatibilitate istorică 7.1','Verificare pachet','I07','Copiere BOM către produs.'),
('Beluga copyBOM','1.0.0','GPLv2 declarat','I08','Copiere rețetă pentru articole similare.'),
('Sales Forecasting','iD4.1/5.1 în wiki','Verificare pachet','I09','Perioade și previziuni de vânzare.'),
('Purchasing Forecast','iD2.1/3.0 în wiki','Verificare pachet','I10','Necesar și propuneri de achiziție.'),
('TOC Buffer','Wiki6.2 / binar7.1','Verificare pachet','I03','Praguri dinamice și istoric buffer.'),
('TargetCostBOM','iD10 + Libero declarat','Verificare pachet','I19','Cost BOM și comparație între date.'),
('Kanban Dashboard','Versiune exactă neconfirmată','Verificare pachet','I04','Carduri, priorități, stări, swimlanes și WIP vizual.'),
('Libero Warehousing','ALPHA; versiune neconfirmată','Condiții distribuție neclarificate','I11','Outbound; inbound incomplet în descriere.'),
('Red1 WMS','BETA; versiune neconfirmată','Verificare pachet','I12','Handling units și locații; pilot 13 necesar.'),
('Scale Connector','Compatibilitate istorică3.1','Verificare pachet','I13','Citire prin RS-232; nu OPC UA/MQTT implicit.'),
('Multiple ASI','Versiune exactă neconfirmată','Verificare pachet','I14','Candidat pentru editare/alocare a atributelor; detalii neconfirmate.'),
('CopyWFNodes','Versiune exactă neconfirmată','Verificare pachet','I15','Utilitar de copiere noduri workflow.'),
('BPM Configurator','Versiune exactă neconfirmată','Verificare pachet','I16','Configurare procese; nu motor MRP demonstrat.'),
('Logilite DMS','Versiune exactă neconfirmată','Verificare pachet','I17','Documente și atașamente; aprobarea reviziilor se verifică.'),
('TMS','Versiune exactă neconfirmată','Verificare pachet','I18','Transport; componentă conexă producției.'),
('REST bxservice','Revizie instalată neconfirmată','Verificare pachet','I90','Acces modele/procese; conector EVA de business de construit.')]
versions=[['ERPNext','version-16 / 7474d9e78627','GPL-3.0','SRC_erpnext','Ediție liberă autogăzduită; BOM, Work Order, Job Card, planificare.'],['Tryton','8.2.0 production; documentație latest','GPL-3.0-or-later','TRYTON_SDIST','Module oficiale distincte; toate pe aceeași familie la instalare.'],['Odoo Community','19.0 / 9ec2b55d3fa3','LGPL-3.0','SRC_odoo','mrp, maintenance, subcontracting; nu include Enterprise.'],['Apache OFBiz','release24.09 / 0749c835f0f3','Apache-2.0','SRC_ofbiz','Motor ERP separat, Java; nu plugin OSGi.'],['Dolibarr','23.0 / 11abdaed08a9','GPL-3.0-or-later','SRC_dolibarr','BOM și Manufacturing Orders activate în distribuția liberă.'],['iDempiere nucleu','release-13 / 0bbc4fa5df2e','GPLv2','SRC_idempiere','Producție simplă și suport ERP; motor MRP extins separat.'],['EVA inspectată',d.EVA_SHA[:12],'Repository privat; nu se presupune licență publică','V01','Cod analizat static; configurația și JAR-urile live nu au fost inspectate.']]+[list(x) for x in mods]
labels={'N':'✓ Da','M':'✓ Modul oficial','C':'△ Parțial','A':'△ Extensie','D':'✕ Nu (dezvoltare)','U':'? Neconfirmat','N*':'△ Cod cu limite','-':'— Fără obiect'}
mf=[['N','N','N','N','N','C','C','U'],['N','N','N','N','N','C','C','C'],['N','N','C','N','N','N','D','D'],['N','N','N','C','N','C','C','D'],['-','C','-','C','C','C','U','D'],['C','C','C','U','C','D','D','D'],['-','U','U','D','U','D','D','U'],['N','N','N','C','N','C','C','D'],['C','C','C','C','-','C','-','D'],['C','U','U','U','C','C','D','D'],['N','C','N','U','D','N','-','D'],['-','-','C','U','D','-','U','-']]
specific={'Asset Maintenance':{'Registru de utilaje':'N','Plan mentenanță preventivă':'N','Contor ore sau cicluri':'N','Ordin de intervenție':'N'},'BOMDrop':{'Variante de produs':'C','BOM și componente':'C'},'Sales Forecasting':{'Forecast pentru cerere':'N'},'Purchasing Forecast':{'Propuneri de aprovizionare':'N','Calcul necesar net de materiale':'C'},'TOC Buffer':{'Praguri de reaprovizionare':'N'},'TargetCostBOM':{'Cost pe ordin și articol':'C','Analiză abateri standard efectiv':'C'},'Kanban Dashboard':{'Kanban vizual configurabil':'N'},'Libero Warehousing':{'Picking pentru producție':'C'},'Red1 WMS':{'Handling units paleți':'N'},'Multiple ASI':{'Consum pe lot explicit în UI':'U'},'Logilite DMS':{'Instrucțiune aprobată pe revizie':'C'},'TMS':{'Necesar transport':'N'},'REST bxservice':{'API sau servicii de extensie':'N'}}
rows=[]
for ci,cat in enumerate(d.MATRICES):
 for ri,(name,status) in enumerate(cat['rows']):
  statuses=status.split()+[mf[ci][ri],mf[ci][ri]]+[specific.get(m[0],{}).get(name,'-') for m in mods[2:]]
  rows.append([cat['category'],name]+[labels[s] for s in statuses]+[cat['sources']+' '+' '.join(m[3] for m,st in zip(mods,statuses[7:]) if st!='-'),cat['note']])
extra=[('Configurare și utilitare','Expansiune BOM în comanda client','AutoBOMOrder','N'),('Configurare și utilitare','Copiere BOM către alt produs','CopyBOMToProduct','N'),('Configurare și utilitare','Copiere rețetă Beluga','Beluga copyBOM','N'),('Configurare și utilitare','Componente opționale și obligatorii','BOMDrop','N'),('Planificare și rapoarte','Istoric și ajustare buffer TOC','TOC Buffer','N'),('Planificare și rapoarte','Comparație cost BOM între două date','TargetCostBOM','N'),('Mentenanță','Sarcini standard și cereri intervenție','Asset Maintenance','N'),('Depozit și echipamente','Citire cântar RS-232','Scale Connector','N'),('Depozit și echipamente','Editare multiple ASI','Multiple ASI','U'),('Configurare și utilitare','Copiere noduri workflow','CopyWFNodes','N'),('Configurare și utilitare','Configurare BPM extensie','BPM Configurator','U'),('Documente și integrare','Gestiune documente DMS','Logilite DMS','N'),('Documente și integrare','Servicii REST modele și procese','REST bxservice','N')]
for cat,name,target,state in extra:
 st=['U']*7+['-']*len(mods);idx=next(i for i,m in enumerate(mods) if m[0]==target);st[7+idx]=state
 rows.append([cat,name]+[labels[s] for s in st]+[mods[idx][3],'Rând dedicat extensiei. Alte produse: neconfirmat pentru această formulare exactă; nu absență dovedită.'])
source_lookup={x['id']:x for x in reg}
versions=[r+[source_lookup.get(r[3],{}).get('url','')] for r in versions]
payload={'headers':['Capitol','Funcție']+[v[0] for v in versions]+['Surse de categorie','Limite de interpretare'],'versions':versions,'rows':rows,'sources':reg,'legend':list(labels.items()),'moduleStart':9,'auditDate':'2026-10-08','counts':{'functions':len(rows),'software':7,'modules':len(mods)}}
(P/'workbook_data.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf8')
(O/'registru_documentatii.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf8')
with (R/'Matrice_functii.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(payload['headers']);w.writerows(rows)
index=['<!doctype html><meta charset="utf-8"><title>Biblioteca ERP producție</title><style>body{max-width:1200px;margin:40px auto;font:15px/1.5 Arial}table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ccc;text-align:left}th{background:#203e60;color:white}a{color:#075ba1}</style><h1>Biblioteca ERP producție</h1><p>8 octombrie 2026 • EVA și iDempiere • evaluare tehnică și managerială</p><ul><li><a href="01_Raport/Comparatie_ERP_Productie.xlsx">Excel comparativ</a></li><li><a href="01_Raport/Raport_ERP_Productie.pdf">Raport PDF</a></li><li><a href="01_Raport/Raport_ERP_Productie.html">Raport HTML</a></li><li><a href="registru_documentatii.json">Registrul surselor și descărcărilor</a></li></ul><p>✓ Da / △ Parțial sau extensie / ✕ Dezvoltare / ? Neconfirmat. Nicio aplicație nu a fost validată funcțional în mediul beneficiarului. Copiile HTML de lectură omit imaginile; originalele sunt păstrate separat.</p>']
readme=['# ERP — Managementul producției','\nDocumentație separată pentru EVA / iDempiere. Audit: **8 octombrie 2026**.','\n- [Excel comparativ](01_Raport/Comparatie_ERP_Productie.xlsx) — '+str(len(rows))+' funcții, 7 aplicații/configurații și '+str(len(mods))+' module/extensii.','- [Raport PDF](01_Raport/Raport_ERP_Productie.pdf)','- [Raport HTML](01_Raport/Raport_ERP_Productie.html)','- [Raport Markdown](01_Raport/Raport_ERP_Productie.md)','- [Index local al bibliotecii](INDEX.html)','- [Registru surse și descărcări](registru_documentatii.json)','\n**Recomandare:** pilot EVA + MFG2 pentru integrare nativă; ERPNext ca alternativă externă. Compatibilitatea și corectitudinea tranzacțiilor sunt condiții eliminatorii.','\nRaportul include inspecție statică de cod și cercetare documentară; nu include instalarea sau testarea funcțională a ERP-urilor. Zero taxe obligatorii de licență pentru selecția liberă nu înseamnă zero cost de implementare. Modulele cu licență neconfirmată nu sunt aprobate ca 100% gratuite.','\n## Biblioteca surselor','\nDocumentațiile originale aparțin autorilor lor. HTML-urile de lectură sunt copii text, fără imagini; originalele HTML sunt comprimate separat. PDF-urile și arhivele de cod descărcate sunt integrale. Registrul arată explicit erorile HTTP/timeout; nu pretindem o oglindă integrală a tuturor site-urilor.','\n| ID | Document / original | Copie locală |','| --- | --- | --- |']
for group in sorted(set(x['group'] for x in reg)):
 index.append('<h2>'+esc(group)+'</h2><table><tr><th>ID</th><th>Original</th><th>Copie locală / stare</th></tr>')
 for x in [r for r in reg if r['group']==group]:
  local=f'<a href="{esc(x["local"])}">Deschide copia</a>' if x.get('local') else esc(x.get('error','Link la sursă privată'))
  index.append(f'<tr><td>{esc(x["id"])}</td><td><a href="{esc(x["url"])}">{esc(x["title"])}</a></td><td>{local}</td></tr>')
  readme.append('| '+x['id']+' | ['+x['title'].replace('|','/')+']('+x['url']+') | '+('['+'Deschide'+']('+x['local']+')' if x.get('local') else x.get('error','Link privat; sursă nepublicată'))+' |')
 index.append('</table>')
(O/'INDEX.html').write_text(''.join(index),encoding='utf8');(O/'README.md').write_text('\n'.join(readme),encoding='utf8')
print('Report chapters',len(d.PAGES),'Excel functions',len(rows),'columns',len(payload['headers']),flush=True)
