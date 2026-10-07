from pathlib import Path
import json,hashlib,zipfile,re,xml.etree.ElementTree as E
from decimal import Decimal as D
from pypdf import PdfReader
r=Path(__file__).resolve().parent;o=r/'7.1 Audit iterativ';n={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def wb(p):
 z=zipfile.ZipFile(p);names=[x.attrib['name']for x in E.fromstring(z.read('xl/workbook.xml')).find('m:sheets',n)];s={}
 for i,name in enumerate(names,1):
  s[name]={}
  for c in E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('.//m:c',n):
   v=c.find('m:v',n);f=c.find('m:f',n);s[name][c.attrib['r']]={'v':v.text if v is not None else None,'f':f.text if f is not None else None,'t':c.attrib.get('t')}
 return s
baseline=json.loads((o/'Runda2_Verificare_independenta_XLSX.json').read_text(encoding='utf-8'))
same=[{'file':x['file'],'sha256':hashlib.sha256((r/x['file']).read_bytes()).hexdigest(),'same_as_round2':hashlib.sha256((r/x['file']).read_bytes()).hexdigest()==x['sha256']}for x in baseline]
p=r/'7.8 Completari tehnice Runda3/OPEX_36_luni.xlsx';s=wb(p);b=s['OPEX 36 luni'];pm=s['Ipoteze'];errors=[];tests=[]
for sn,ss in s.items():
 for addr,c in ss.items():
  if c['t']=='e':errors.append([sn,addr,c['v']])
def col(i):
 v=''
 while i:i,j=divmod(i-1,26);v=chr(65+j)+v
 return v
for i in range(3,39):
 c=col(i);expected=D(0)
 for rr in range(12,17):
  value=D(pm[f'{c}{rr+4}']['v'])*D(pm[f'{c}12']['v']);expected+=value
  if D(b[f'{c}{rr}']['v'])!=value:errors.append(['OPEX',f'{c}{rr}','product'])
 if D(b[f'{c}10']['v'])!=expected:errors.append(['OPEX',f'{c}10','subtotal'])
 for rr in [34,37,42,43]:
  if b[f'{c}{rr}']['v']!='n.a.':errors.append(['OPEX',f'{c}{rr}','unknown must not become zero'])
for addr,exp in [('AM10','312960'),('AN10','312960'),('AO10','312960'),('AP10','938880'),('B5','938880')]:
 if D(b[addr]['v'])!=D(exp):errors.append(['OPEX',addr,'sum'])
for addr in ['B6','B7','B8','B47','B48','B49','B50','B52','B53','B54']:
 if b[addr]['v']!='n.a.':errors.append(['OPEX',addr,'unknown must be n.a.'])
formulas=sum(c['f']is not None for ss in s.values()for c in ss.values())
# Read-only boundary checks of the same guarded arithmetic, without writing production workbook.
num=lambda x:isinstance(x,(int,float,D))
guarded=lambda vals:sum(vals)if all(num(x)for x in vals)else 'n.a.'
tests=[{'case':'one_service_36months','expected':938880,'actual':guarded([12600,3780,7560,840,1300])*36}, {'case':'five_services_36months','expected':4694400,'actual':guarded([12600,3780,7560,840,1300])*36*5},{'case':'missing_cost','expected':'n.a.','actual':guarded([12600,None,7560,840,1300])},{'case':'explicit_zero_cost','expected':22300,'actual':guarded([12600,0,7560,840,1300])}]
for t in tests:
 if t['actual']!=t['expected']:errors.append(['boundary',t['case']])
profiles=json.loads((r/'7.8 Completari tehnice Runda3/Fise_posturi_date.json').read_text(encoding='utf-8'));problems=[]
for scenario,key in [('MINIM','Ore_pilot'),('MAXIM','Ore_extins')]:
 target=next(r/x['file'] for x in baseline if scenario in x['file'] and '0pct' in x['file']);bb=wb(target)['Buget']
 for x in profiles:
  refs=[int(y)for y in re.findall(r'Buget!(\d+)',x['Linii_XLSX'])];hours=sum(D(bb[f'E{y}']['v'])for y in refs)
  if hours!=D(str(x[key])):problems.append([scenario,x['ID'],'hours',str(hours)])
  for rr in refs:
   if D(bb[f'F{rr}']['v'])!=D(str(x['Cost_angajator_ora'])):problems.append([scenario,x['ID'],'rate'])
pdfdir=r/'2.1 Legislatie si eligibilitate/Recuperari Runda3';reg=json.loads((pdfdir/'Registru_validat_Runda3.json').read_text(encoding='utf-8'));pdfs=[]
for x in reg:
 p1=pdfdir/x['fisier'];sha=hashlib.sha256(p1.read_bytes()).hexdigest();reader=PdfReader(p1);pdfs.append({'name':x['nume'],'file':x['fisier'],'pages':len(reader.pages),'pages_match':len(reader.pages)==x['pagini'],'sha256':sha,'hash_match':sha.lower()==x['sha256'].lower(),'reading_scope':'Technical validation by auditor; legal selective reading documented by jurist, not integral reading.'})
result={'unchanged_project_budgets':same,'opex':{'file':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'formulas':formulas,'errors':errors,'boundary_checks':'Independent arithmetic reproductions; workbook formulas inspected read-only, not a full Excel engine mutation test.','tests':tests,'known_subset_36_months':b['AP10']['v'],'integral_total':b['AP34']['v'],'with_payment_gap':b['B52']['v']},'profiles':{'count':len(profiles),'errors':problems},'pdfs':pdfs}
(o/'Runda3_Controale_independente.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'budgets_unchanged':all(x['same_as_round2']for x in same),'opex_formulas':formulas,'opex_errors':errors,'profile_errors':problems,'pdf_count':len(pdfs),'pdf_all_valid':all(x['pages_match']and x['hash_match']for x in pdfs)},ensure_ascii=True))
