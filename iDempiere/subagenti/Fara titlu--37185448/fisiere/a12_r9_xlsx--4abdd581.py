from a12_r9_orig import *
from a12_r6_exec import plug,repo,java,sec,base,policy,execute
from xml.sax.saxutils import escape
from zipfile import ZipFile,ZIP_DEFLATED
from decimal import Decimal
out=P9/'T04_profils';out.mkdir(exist_ok=True);R9L.mkdir(exist_ok=True)
def sheet(rows):
 return '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+''.join('<row r="'+str(ii)+'">'+''.join('<c r="'+chr(65+i)+str(ii)+'" t="inlineStr"><is><t>'+escape(str(n))+'</t></is></c>'for i,n in enumerate(row))+'</row>'for ii,row in enumerate(rows,1))+'</sheetData></worksheet>'
def gen(name,sub,rows,note,cases):
 head=['AWB','Suma ramburs','Ramburs compensat','Ramburs de transferat','Moneda']
 regs=[('client',[['Cont sintetic de test'],['C1']]),('expeditii',[['Titlu de audit']for i in range(sub-1)]+[head]+rows),('facturi',[['Nr factura','Rest','Compensat','Sold'],['INV-R9-0007','397,94','284,98','112,96']])]
 fn=out/name;WB='<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join('<sheet name="'+k+'" sheetId="'+str(i)+'" r:id="rId'+str(i)+'"/>'for i,(k,v)in enumerate(regs,1))+'</sheets></workbook>';RE='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join('<Relationship Id="rId'+str(i)+'" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet'+str(i)+'.xml"/>'for i in range(1,4))+'</Relationships>'
 with ZipFile(fn,'w',ZIP_DEFLATED)as zz:
  zz.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml"/><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join('<Override PartName="/xl/worksheets/sheet'+str(i)+'.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'for i in range(1,4))+'</Types>');zz.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
  zz.writestr('xl/workbook.xml',WB);zz.writestr('xl/_rels/workbook.xml.rels',RE)
  for i,(k,v)in enumerate(regs,1):zz.writestr('xl/worksheets/sheet'+str(i)+'.xml',sheet(v))
 return {'file':fn.name,'sha256':sha(fn),'head_row':sub,'note':note,'input_awb':[r[0]for r in rows],'expected':cases}
j='''import com.eva.ro.contab.corelare.ParserDecont;import java.nio.file.*;import java.math.*;public class AuditR9Parser{public static void main(String[] args)throws Exception{for(String f:args){Path p=Path.of(f);byte[] bytes=Files.readAllBytes(p);var rr=ParserDecont.parseaza(p.getFileName().toString(),bytes,"RON");var read=ParserDecont.foi(p.getFileName().toString(),bytes);System.out.println("CASE|"+p.getFileName()+"|"+rr.stare+"|"+rr.randuri.size()+"|"+read.stream().map(x->x.nume()+"="+x.randuri().size()).toList()+"|"+rr.eroare);for(var row:rr.randuri)System.out.println("ROW|"+p.getFileName()+"|"+row.awbNorm+"|"+row.suma+"|"+row.declarat+"|"+row.compensat+"|"+row.comision);}}}'''
def probe():
 fixtures=[gen('r9-transfer1.xlsx',3,[['A1200001','150,00','0','150,00','RON'],['A1200002','162,02','0','162,02','RON']],'Deux lignes transférées, troisième feuille présente.',{'count':2,'somme':'312.02'}),gen('r9-transfer2.xlsx',40,[['A1200003','200,00','0','200,00','RON'],['A1200004','276,59','0','276,59','RON']],'Frontière du rang40.',{'count':2,'somme':'476.59'}),gen('r9-compensat.xlsx',4,[['A1200005','284,98','284,98','0','RON']],'Compensé intégral, zéro à transférer.',{'count':1,'compensated':'284.98','transfer':'0.00'}),gen('r9-header41.xlsx',41,[['A1200006','99,00','0','99,00','RON']],'Negativ: același antet mutat la 41.',{'count':0})]
 # Explicitly populate valid [Content_Types]/rels package? CititorTabelar reads xl/workbook.xml + inner rels only; no physical Excel presentation credited.
 javaf=out/'AuditR9Parser.java';javaf.write_text(j,encoding='utf8');cases=[];res=[]
 for tag in ['git','instalat']:
  dest=R9L/('compiled_'+tag);dest.mkdir(exist_ok=True);jar=sec/('cod-master-contab.jar'if tag=='git'else'com.eva.ro.contab_13.0.0.jar');cp=';'.join(map(str,[dest,jar,base,'D:/CodexWork/a05-support-jars/*','D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a12-r6-preprobes/deps/*']))
  c=execute([java/'javac.exe','-cp',cp,'-sourcepath','','-d',dest,javaf],R9L);assert c.returncode==0,c.stdout
  f=out/(tag+'_casuri.log');tmpfail=out/(tag+'_limitare_temp_initiala.log')
  if f.exists()and not tmpfail.exists():tmpfail.write_bytes(f.read_bytes())
  v=execute([java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir=D:/CodexWork/a12-r6-preprobes','-Dfile.encoding=UTF-8','-cp',cp,'AuditR9Parser',*[out/x['file']for x in fixtures]],R9L);f.write_text(v.stdout,encoding='utf8');matches=[]
  for s in v.stdout.splitlines():
   if not s.startswith(('CASE|','ROW|')):continue
   fields=s.split('|');matches.append({'line':s})
  cases.append({'target':tag,'jar_sha':sha(jar),'exit':v.returncode,'log':source(f),'markers':matches})
 for x in fixtures:
  for z in cases:
   lines=[y['line'].split('|')for y in z['markers']if y['line'].split('|')[1]==x['file']];metric=next(l for l in lines if l[0]=='CASE');vs=[l for l in lines if l[0]=='ROW'];nums=lambda i:sum((Decimal(l[i])for l in vs if l[i]!='null'),Decimal('0.00'))
   res.append({'file':x['file'],'target':z['target'],'state':metric[2],'sheets':metric[4],'count':len(vs),'sum_output_transfer':str(nums(3)),'sum_declared':str(nums(4)),'sum_compensated':str(nums(5)),'expected':x['expected'],'expected_count_equal':len(vs)==x['expected']['count'],'expected_sum_equal':nums(3)==Decimal(x['expected']['somme'])if 'somme'in x['expected']else None,'compensation_equal':nums(5)==Decimal('284.98')and nums(3)==0 if x['file']=='r9-compensat.xlsx'else None})
 f=P9/'T04_07_08_parser_oracles.json';wr(f,{'utc':now(),'sources':{k:r7map[k]['source_row']for k in ['T04.07-R3-001','T04.08-R3-001']},'source_criteria':block(r7map['T04.08-R3-001']['source_row']['source_file'],r7map['T04.08-R3-001']['source_row']['sha_or_git_blob'],[34,35,64,65,190,196,197,198,199,200,201,245,248]),'inputs':fixtures,'java_source':source(javaf),'cases':cases,'observations':res,'boundary':'Citirea și interpretarea parserului real pe arhiva XLSX cu trei foi. Nu este operația persistentă ImportDecontCurier, nu demonstrează antete persistate, legături cu factura sau idempotenta. Facturi poate fi citită brut, articolul ei contabil rămâne distinct.'});print(sha(f),[(x['file'],x['target'],x['count'],x['sum_output_transfer'],x['sum_compensated'])for x in res])
if __name__=='__main__':probe()

