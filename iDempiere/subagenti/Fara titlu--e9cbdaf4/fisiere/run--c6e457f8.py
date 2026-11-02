from pathlib import Path
import collections, subprocess, tempfile, hashlib, json, csv, itertools, datetime
O=Path(__file__).parent;E=O.parent;R=E.parent;G3=E/'R7_pregatire/G3';G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');DEP=Path('D:/CodexWork/eva-audit-secondary-20261102');J=Path('C:/Program Files/Java/jdk-21/bin')
def rd(p):return json.loads(p.read_bytes())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
one=G3/'Combinatii_CPP_S1_S2.json';j=rd(one);assert h(one)=='77d068975f239f73f61861e23bbd65634c49aacb9a89b5ae569eca8413e070fb';assert h(G3/'AuditCombinatii.java')==j['source_harness_sha'] and h(G3/'inputs.csv')==j['inputs_sha'] and h(G3/'expected.csv')==j['expected_sha']
def oracle(row):
 i,q1,q2,qp,perm=row.split(','); qs=list(map(int,(q1,q2,qp))); out=['-']*3;stocks=[120]*3
 for k in map(int,perm):
  n=qs[k-1]
  if not n:continue
  req=([6*n]*3 if k==1 else [3*n]*3 if k==2 else [n,0,0])
  ok=all(before>=needed for before,needed in zip(stocks,req));out[k-1]='REZERVAT'if ok else 'ROSU'
  if ok:stocks=[b-v for b,v in zip(stocks,req)]
 return ','.join([i,*out,*map(str,stocks),str(min(stocks)//6),str(min(stocks)//3)])
rows=(G3/'inputs.csv').read_text(encoding='utf8').splitlines();want=[oracle(s)for s in rows];assert len(set(rows))==16632 and want==(G3/'expected.csv').read_text(encoding='utf8').splitlines()
for f in ('git.csv','instalat.csv'):assert want==(G3/f).read_text(encoding='utf8').splitlines()
ext=[];keys=set()
for a,b,p in itertools.product([0,1,10,19,20,21],[0,1,19,39,40,41],[0,1,2,3,60,119,120,121]):
 for order in ('132','213','321'):
  key=f'{a},{b},{p},{order}';keys.add(key);ext.append(f'{len(ext)+1},'+key)
tmp=Path(tempfile.mkdtemp(prefix='a11-r4-g3-'));capt=[]
infile=E/'A11_reproduceri_CESIRO1/Q_redacted_synthetic_detail.json'
for nm,file in [('git','cod-master-contab.jar'),('instalat','com.eva.ro.contab_13.0.0.jar')]:
 jar=DEP/file;cp=';'.join(map(str,[jar,*DEP.glob('org.*.jar'),Path('D:/CodexWork/a05-support-jars/*')]))
 call=subprocess.run([str(J/'javac.exe'),'-encoding','UTF-8','-cp',cp,'-d',str(tmp),str(G3/'AuditCombinatii.java'),str(O/'OwnerMatrix.java')],capture_output=True,text=True);assert call.returncode==0,call.stderr
 run=[str(J/'java.exe'),'-Duser.timezone=UTC','-cp',str(tmp)+';'+cp];p=subprocess.run(run+['AuditCombinatii'],input='\n'.join(rows+ext)+'\n',capture_output=True,text=True);assert p.returncode==0,p.stderr;assert p.stdout.splitlines()==want+[oracle(a)for a in ext]
 z=subprocess.run(run+['com.eva.ro.contab.corelare.OwnerMatrix',str(infile)],capture_output=True,text=True);assert z.returncode==0,(z.stdout,z.stderr)
 capt.append(dict(target=nm,sha256=h(jar),original_matches=len(rows),extra_opposite_permutations_matches=len(ext),owner_version_readout=z.stdout.splitlines()))
summary=dict(supplement_sha256=h(one),original_input_sha=h(G3/'inputs.csv'),reference_oracle_rebuilt_from_arithmetic=True,original_size=len(rows),new_extra_perm_size=len(ext),shared_allocations='120 P1/P2/P3 în G1=101, S1=6 din fiecare, S2=3 din fiecare, P1 direct; refuzul lasă intact stocul',fresh_case_example=next({'input':q,'result':oracle(q)} for q in ext if ',10,19,60,321' in q),result=capt,scope='Executat pe ambele JAR-uri fixate. Alocare componentă în memorie, fără DB/rezervare concurentă, ofertă publicată, acțiune gestionar ori vindere fizică. Matricea locală owner/seller folosește valoarea explicită proprie a Q și intrări contrafactuale, nu scrie ERP.',before_report_supplement_not_credited=True);write(O/'readback.json',summary);print(h(O/'readback.json'),len(rows),len(ext))

