import csv,collections,datetime,decimal,hashlib,json,pathlib,re,sys,xml.etree.ElementTree as ET,zipfile
base=pathlib.Path('D:/CodexWork/a02-historic-r6'); book=base/'INVENTAR_IDEMPIERE_SAGA_EVA_2026-10-08.xlsx'; nm={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','pr':'http://schemas.openxmlformats.org/package/2006/relationships'}
def tag(s):return '{'+nm['s']+'}'+s
with zipfile.ZipFile(book)as z:
 ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():ss=[''.join(x.itertext())for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 spec=ET.fromstring(z.read('xl/workbook.xml'));rels={n.get('Id'):n.get('Target') for n in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))};sheetdata={}
 for sh in spec.find('s:sheets',nm):
  n=sh.get('name');tar=rels[sh.get('{'+nm['r']+'}id')]; sheet=ET.fromstring(z.read(tar.lstrip('/') if tar.startswith('/')else 'xl/'+tar)); rows={}
  for rr in sheet.findall('s:sheetData/s:row',nm):
   vals={}
   for cc in rr.findall('s:c',nm):
    typ=cc.get('t');v=cc.findtext('s:v','',nm); cv= ''.join(cc.find('s:is',nm).itertext()) if typ=='inlineStr' and cc.find('s:is',nm)is not None else ss[int(v)] if typ=='s' else v
    if cv!='':vals[re.sub('[0-9]+$','',cc.get('r'))]=cv
   if vals:rows[int(rr.get('r'))]=vals
  sheetdata[n]=rows
print('sheets',[(n,len(rows),min(rows),max(rows))for n,rows in sheetdata.items()]);
for name,rs in sheetdata.items():
 if not(name in ['iDempiere → SAGA (invers)','Module iDempiere instalabile','Sinteză']):continue
 print(name,[(r,[(k,str(v)[:100])for k,v in a.items()][:3])for r,a in rs.items()if len(a)<5 or a.get('A','') in ('Modul','ID iDempiere (AD_Menu_ID)')][:25]);
def table(f):
 with (base/f).open(encoding='utf-8-sig',newline='')as f:return list(csv.reader(f))
def normnum(x):
 try:return str(decimal.Decimal(x).normalize())
 except: return x
tables={'inverse':('invers_idempiere_saga.csv','iDempiere → SAGA (invers)'),'module':('module_idempiere.csv','Module iDempiere instalabile')};res={};inv=[];mods=[];compare={}
for key,(f,sheet) in tables.items():
 header,*ll=table(f);rs=sheetdata[sheet];start=next((r for r,x in rs.items()if x.get('A')==header[0] and x.get('B')==header[1]),None);print('start',key,start,header[:2],len(ll));
 if start is None:
  print([(r,x.get('A'),x.get('B'))for r,x in rs.items()if(x.get('A','').startswith('ID')or x.get('A')=='Modul')]);continue
 differences=[];missing=[];keys=[];actualdata=len([r for r,x in rs.items() if r>start and x.get('A') not in (None,'')]);
 for i,line in enumerate(ll):
  rn=start+i+1; cells=rs.get(rn,{});keys.append(line[0] if key=='inverse' else [line[0],line[1]])
  for j,v in enumerate(line):
   actual=cells.get(chr(65+j),'');
   if actual!=v and normnum(actual)!=normnum(v):differences.append([rn,chr(65+j),v[:60],actual[:60]])
 compare[key]={'sheet':sheet,'header_row':start,'first_data_row':start+1,'last_csv_row':start+len(ll),'columns':len(header),'csv_records':len(ll),'sheet_data_rows_below_header':actualdata,'mismatched_cells':len(differences),'first_mismatch_examples':differences[:12]};
 if key=='inverse':inv=ll;inv_header=header
 else:mods=ll;mod_header=header
(base/'xlsx-projection.json').write_text(json.dumps({'sheets':[{'name':n,'first_row':min(rs),'last_row':max(rs),'physical_nonempty_rows':len(rs)} for n,rs in sheetdata.items()],'comparison':compare,'summary_rows':[{ 'row':r,'name':x.get('A',''),'value':x.get('B',''),'source':x.get('C','')} for r,x in sheetdata['Sinteză'].items() if 'Module iDempiere' in x.get('A','') or 'frunze active' in x.get('A','')]},ensure_ascii=False,indent=2),encoding='utf8');print('comparison',json.dumps(compare,ensure_ascii=False));
