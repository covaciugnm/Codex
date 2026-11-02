from a12_r7_pg_cui import *
from collections import Counter
import zipfile
r=rd(RP/'Clasificare_nominala_1587.json');rows={v['criterion']:v for v in r['records']};out=[]
ft={}
for row in (D/'fulltree.raw').read_bytes().split(b'\0'):
 if not row:continue
 a,k=row.decode(errors='replace').split('\t',1);entry=a.split()
 if entry[1]=='blob':ft[k]=entry[2]
def readgit(f):
 path=f.relative_to(repo).as_posix();oid=ft[path];b=f.read_bytes();valid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 if not valid:
  b=sp.check_output(['ssh','-o','BatchMode=yes',server,cmdgit+'cat-file blob '+oid]);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 return b,{'source':path,'git_object':oid,'sha256':hashlib.sha256(b).hexdigest(),'local_bytes_equal_git':valid}
def observe(cid,which,basis,target,raw,rule,qual='Nu certifică comportamentul produsului la închidere.'):
 if cid not in rows:return
 out.append({'criterion':cid,'case_scope':which,'authority':rows[cid]['source_row'],'asset':basis,'expected_subcase':target,'observed_now':raw,'comparison':rule,'limit':qual})
source=plug/'src/com/eva/ro/contab';labels=[source/'documente/res/etichete.tsv',source/'form/reges/res/etichete.tsv']
jars=[('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]
for f in labels:
 b,e=readgit(f);data=b.decode('utf8').splitlines();r=[z.split('\t')for z in data if not z.startswith('#')];key=Counter(z[0]for z in r); vals=[sum(len(z)!=3 for z in r),sum(v>1 for v in key.values()),sum(z[0].startswith('t03.') and (len(z)<3 or not z[1]or not z[2])for z in r)];observe('T03-R2-047',f.name+'/'+f.parent.parent.name,e,[0,0,0],vals,'CONFORM'if vals==[0,0,0]else'ABATERE_NUMERICĂ','Se execută formula literală din plan; separă rândurile goale și defectul de traducere.');observe('T03-R2-065',f.parent.parent.name,e,0,vals[1],'CONFORM'if not vals[1]else'ABATERE_NUMERICĂ','Uniq -d include cheia goală dacă apare repetat. Nu echivalează cu duplicarea unei etichete afișate.')
 for t,j in jars:
  arc=f.relative_to(plug/'src').as_posix()
  with zipfile.ZipFile(j)as a:
   embedded=a.read(arc);c=sum('TestT03Lot5' in name for name in a.namelist())
  observe('T03-R2-057',t+'/'+arc,{**e,'jar':sha(j)},[0,True],[c,embedded==b],'CONFORM'if not c and embedded==b else 'DIFERENȚĂ_DE_EDIȚIE','Valoarea originală privea JAR-ul de probă. Aici este comparația dintre resursa de la HEAD și fiecare dintre JAR Git/instalat.')
f=plug/'test/TestT03Lot5.java';b,e=readgit(f);aset=sorted(set(re.findall(r'T03-\d\d',b.decode('utf8'))));target=set('T03-'+format(i,'02d')for i in range(1,37)if i!=29);observe('T03-R2-055','toate 35 ID nominale',e,sorted(target),{'missing':sorted(target-set(aset)),'extra':sorted(set(aset)-target)},'IDENTIC'if set(aset)==target else 'DIFERENȚĂ_INVENTAR','Nu furnizează rezultatul celor 40 sau mai multe teste; returnarea unui ID în sursă nu înseamnă rularea acestuia.')
f=plug/'test/fixtures/t29_tipar_vechi.tsv';b,e=readgit(f);lines=[i for i,l in enumerate(b.decode('utf8').splitlines(),1)if re.search(r'\t(P2b|P4)\t',l)];observe('T204-R2-006','fixture de tipărire istorică P2b/P4',e,0,{'count':len(lines),'lines':lines},'CONFORM'if not lines else'ABATERE_NUMERICĂ')
for t,j in jars:
 rr=sp.run([java/'javap.exe','-p','-cp',j,'com.eva.ro.contab.banca.MotorContare'],stdout=sp.PIPE,stderr=sp.STDOUT,encoding='utf8',errors='replace')
 found=[l.strip()for l in rr.stdout.splitlines()if re.search(r'numePotrivit|acelasiNume|cheieNume',l)]
 observe('T06-R2-007','javap firma de metodă '+t,{'jar_sha':sha(j),'javap_stdout_sha':hashlib.sha256(rr.stdout.encode()).hexdigest()},rows['T06-R2-007']['original_inputs_and_accepted_oracle']['expected'],found,'SEMNTĂTURI_NOMINALE_FĂRĂ_VERDICT_DE_ANSAMBLU','Testează semnăturile concrete; refuzul și paritatea numelor sunt verificate separat.')
for cid,nm in [('T190-R2-013','SalariatiImporter.java')]:
 fps=list(repo.rglob(nm));fps=[f for f in fps if f.is_file()and f.relative_to(repo).as_posix()in ft]
 for f in fps:
  b,e=readgit(f);ls=b.decode('utf8').splitlines();start=next((i for i,l in enumerate(ls)if re.search(r'private void scrieContracteReges',l)),None)
  if start is None:continue
  end=next(i for i in range(start+1,len(ls))if re.match(r'^    }',ls[i]));sites=[(i+1,ls[i].strip())for i in range(start,end+1)if 'substring'in ls[i]];observe(cid,'prima comandă awk | grep -c substring',e,1,{'lines':sites,'count':len(sites)},'CONFORM'if len(sites)==1 else'ABATERE_NUMERICĂ','A doua comandă privind git diff master nu este exercitată aici.')
# Two historic artifacts only when the filename is unique inside the explicitly named historical case.
for folder,nm in [('T186','20a_inventar.tsv'),('T196','A2_2023-02.txt')]:
 fs=[(name,oid)for name,oid in ft.items()if '/'+folder+'-'in name and name.endswith('/'+nm)]
 if len(fs)!=1:continue
 name,oid=fs[0];b=sp.check_output(['ssh','-o','BatchMode=yes',server,cmdgit+'cat-file blob '+oid]);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;e={'source':name,'git_object':oid,'sha256':hashlib.sha256(b).hexdigest()};ls=b.decode('utf8').splitlines()
 if folder=='T186':
  c=Counter((l.split('\t')+['']*10)[9]for l in ls[1:]);observe('T186-R2-008','coloana 10, excluzând header',e,{'curat':243,'conflict':56,'nou':39},dict(c),'CONFORM'if dict(c)=={'curat':243,'conflict':56,'nou':39}else'ABATERE_NUMERICĂ')
 else:
  mr=[x for x in ls if x.startswith('MARCAJ')];observe('T196-R2-006','marcaje după buton în fixtura istorică',e,['MINIM_MAX_APLICAT','STAT_CALCULAT_OK'],{'stat_calculat_ok':sum('STAT_CALCULAT_OK'in x for x in mr),'minim_max_aplicat':sum('MINIM_MAX_APLICAT'in x for x in mr)},'ARTEFACT_HISTORIC_REVERIFICAT')
  expected=['SAL_BRUT','CAS','CASS','IMPOZIT','NET','DED_PERS'];matched=[z for z in ls if z.startswith('FISA|')and any('|'+code+'|' in z for code in expected)];observe('T196-R2-007','număr de linii FISA din șase concepte declarate',e,12,len(matched),'CONFORM'if len(matched)==12 else'ABATERE_NUMERICĂ','Regulă de domeniu din cerință, nu evaluarea unui grep fără bare literale în expresia shell.')
wr(RP/'Masuratori_statice_nominale_R7.json',{'utc':datetime.now(UTC).isoformat(),'rows':out,'source_git':shaGit,'mutations':'aucune; validations de texte et de bytecode sans exécuter des directives de document.'});print([(w['criterion'],w['comparison'])for w in out])

