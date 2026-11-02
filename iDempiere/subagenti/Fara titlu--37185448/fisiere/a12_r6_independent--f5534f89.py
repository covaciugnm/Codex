from a12_r6_exec import *
from a12_r6_mutations_cal import original
import uuid
def fiscal():
 p=T/'mutant_test_legal.py'
 p.write_text('''from decimal import Decimal
from datetime import date
import pytest,sys
from app.idempiere import readdb
class Plug:
 def pytest_collection_modifyitems(self,items):
  orig=readdb.parametru_legal_rand
  def bad(key,when):
   try: return orig(key,when)
   except readdb.ParametruLegalLipsa:return {"cheie":key,"valoare":Decimal("0"),"validfrom":date(2018,1,1),"validto":None,"temeilegal":"mutant"}
  if sys.argv[1]=="fallback":readdb.parametru_legal_rand=bad
  elif sys.argv[1]=="tie":readdb._cheie_rand_ales=lambda r:(r["validfrom"],r.get("origine")!="MANUAL")
sys.exit(pytest.main(["-p","no:cacheprovider","-q","--tb=short",*sys.argv[2:]],plugins=[Plug()]))
''',encoding='utf8'); testf=repo/'backend/tests/test_t159_registru_legal.py';env=dict(os.environ,IDE_MPIERE_MOCK='1',IDEMPIERE_MOCK='1',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='D:/CodexWork/eva-a01-fixture-deps;'+str(repo/'backend'))
 out=[]
 for case,tests in [('control',['test_valoare_registru_alt_decat_seed_si_refuz','test_ruta_get_si_refuz_422','test_t159d_egalitate_validfrom_manual_castiga_in_orice_ordine']),('fallback',['test_valoare_registru_alt_decat_seed_si_refuz','test_ruta_get_si_refuz_422']),('tie',['test_t159d_egalitate_validfrom_manual_castiga_in_orice_ordine'])]:
  rr=sp.run([sys.executable,'-X','utf8',p,case,*[str(testf)+'::'+k for k in tests]],cwd=repo/'backend',env=env,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=55);lg=E6/('t159_mutant_'+case+'.log');lg.write_bytes(rr.stdout);out.append({'variant':case,'observations':tests,'returncode':rr.returncode,'summary':rr.stdout.decode('utf8',errors='replace').splitlines()[-1],'log':lg.name,'sha':sha(lg),'change':'fallback returnează 0 implicit în loc de refuz; tie acordă prioritate SEED; control nemodificat. Monkeypatch numai procesul testului; sistemul extern nu e folosit.'})
 wr(E6/'T159_test_matrice.json',{'original_suite':sha(testf),'test_fixture_backend':sha(E6/'T159_backend_pytest.log'),'mutations':out,'runner_sha':sha(p)});print('fiscal',[(r['variant'],r['returncode'])for r in out])
def documents():
 li='Documentatie/echipa-2026-10-09/T204-tiparire-loturi-ramase/dovezi-01-plan/07_ecrane_t204.txt';b=original(li);p=E6/'registre_git/07_ecrane_t204.txt';p.write_bytes(b);scope=set(b.decode().splitlines());src=E6/'t204_numere_head.log';within=False;outside=[]
 for l in src.read_text(encoding='utf8').splitlines():
  if l.startswith('3 ALE MELE'):within=True;continue
  if l.startswith('4 '):within=False
  if within and re.match(r'^    [A-Za-z0-9]+ W',l):outside.append(l.split()[1])
 mat=set(outside)&scope
 p1=E6/'t330_contract_git_exact.log';s=p1.read_text(encoding='utf8');orig='com/eva/ro/contab/documente/Fefo.java'
 rr=sp.run(['rg','--files',str(plug/'src')],stdout=sp.PIPE);f=next(Path(q)for q in rr.stdout.decode().splitlines()if q.endswith('Fefo.java'))
 data={'T204-R2-004':{'raw':src.name,'raw_sha':sha(src),'whitelist_count':len(scope),'whitelist_source':li,'whitelist_sha':sha(p),'actual_unfiltered':outside,'intersection':sorted(mat),'expected_remaining_in_original_set':0,'actual_remaining_in_original_set':len(mat),'core_guard_excluded':('WSagaReconciliereForm' in outside and 'WSagaReconciliereForm'not in mat),'limit':'Măsurare statică exactă pe setul nominal; nu a deschis cele 26 de ecrane.'},'T330-R2-027':{'original_path':'Documentatie/echipa-2026-10-09/COORDONARE_SESIUNI.md','result_count':len(s.splitlines()),'target':1,'text':s,'git_sha':shaGit,'output_sha':sha(p1),'versioned_API_source':f.relative_to(repo).as_posix(),'sha':sha(f),'actual_signatures':[(i,z.strip())for i,z in enumerate(f.read_text(encoding='utf8').splitlines(),1)if re.search(r'public static .* (ordine|propus|decizieExpirat)\(',z)],'limit':'O linie de coordonare la HEAD nu dovedește cronologia față de avizul inițial; semnătura de decizie diferă de forma planului și explică explicit parametrul retur.'}}
 wr(E6/'T204_T330_citire_documentara_exacta.json',data);print('doc',len(scope),len(mat),len(s.splitlines()))
def locator():
 s='''import com.eva.ro.contab.corelare.AlegereLocatie;
class A12LocatorR6 {public static void main(String[] args) {int f=0;
int[][] a={{42,201,201,41,42},{42,202,201,41,41},{0,201,201,41,41},{-1,201,201,41,41}};
for(int[] x:a){int v=AlegereLocatie.alege(x[0],x[1],x[2],x[3]);System.out.println(java.util.Arrays.toString(x)+" => "+v);if(v!=x[4])f++;}
Object[][] b={{42,11,11,true,null},{42,12,11,true,"t323b.refuz.firma"},{42,11,0,true,"t323b.refuz.firma"},{42,11,11,false,"t323.art.refuz.inactiv"},{0,12,11,false,null}};
for(Object[] x:b){String v=AlegereLocatie.refuz((int)x[0],(int)x[1],(int)x[2],(boolean)x[3]);System.out.println(java.util.Arrays.toString(x)+" => "+v);if(!java.util.Objects.equals(v,x[4]))f++;}System.exit(f);}}'''
 p=T/'A12LocatorR6.java';p.write_text(s,encoding='utf8');out=[]
 for t,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]:
  td=T/('loc'+t);td.mkdir(exist_ok=True);cp=';'.join(map(str,[td,j,base]));cc=execute([java/'javac.exe','-encoding','UTF-8','-sourcepath','','-cp',cp,'-d',td,p],T);assert cc.returncode==0,cc.stdout
  rr=execute([java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-cp',cp,'A12LocatorR6'],T);lg=E6/('T323_locator_'+t+'.log');lg.write_text(rr.stdout,encoding='utf8');out.append({'target':t,'artifact_sha':sha(j),'exit':rr.returncode,'raw':lg.name,'sha':sha(lg),'input_and_oracle_are_independent':sha(p),'eligible':rr.returncode==0})
 wr(E6/'T323_nou_vector_alegere.json',{'claim':'T323-R2-002, AlegereLocatie.alege/refuz, două gestiuni și locatori 41/42. Alocare pe fiecare din cele șapte documente în ERP nu este probată de corpul sau acest vector.','results':out});print('locator',[(v['target'],v['exit'])for v in out])
if __name__=='__main__':
 documents()
 with ThreadPoolExecutor(max_workers=2)as x:
  for f in x.map(lambda g:g(),[fiscal,locator]):pass

