from a12_r8_review import *
from functools import lru_cache
import concurrent.futures,html,hashlib,os,time,shutil
R=E/'R8';R.mkdir(exist_ok=True)
DATA=P/'Rezultate_A12_93_si_supliment.json';R7report=R7/'A12_raport.json';ER=E/'R7_supliment/Erata_A12_R7_cinci_criterii.json';oldr=rd(R7report)
@lru_cache(maxsize=4096)
def h(p):return sha(p)
def rf(p):return {'file':p.relative_to(B).as_posix(),'sha256':h(p)}
def check_art(obj):
 if isinstance(obj,list):
  for x in obj:check_art(x)
 elif isinstance(obj,dict):
  p=obj.get('file')or obj.get('path');hh=obj.get('sha256')
  if isinstance(p,str)and isinstance(hh,str)and p.startswith(('executie/','capturi/')) and len(hh)==64:
   f=B/p;assert f.is_file()and h(f)==hh,(p,hh)
  for v in obj.values():check_art(v)
def ptr(x,p):
 for s in p[1:].split('/')if p else[]:x=x[int(s)]if isinstance(x,list)else x[s.replace('~1','/').replace('~0','~')]
 return x
def esc(s):return '~'.join([])if s is None else str(s).replace('~','~0').replace('/','~1')
def stripped_id(o):return 'EV8-'+hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:23]
def zmake(t,kind,epoch,mode,exp,obs,f,pt,lim,cred='subcase'):
 x={'criterion':t,'kind':kind,'phase':epoch,'method':mode,'oracle':exp,'observed':obs,'source':rf(f),'pointer':pt,'qualification':lim,'coverage':cred};x['id']=stripped_id(x);return x
def archive_scope(z):return z['phase']=='historical'
def compact(v):
 if isinstance(v,str):return v
 return json.dumps(v,ensure_ascii=False)
CORE=set()
def sources():
 collection=collections.defaultdict(list);raw=rd(DATA);check_art(raw['cases'])
 for t,ss in raw['cases'].items():
  for i,x in enumerate(ss):
   ph=x['phase'];ki=x['kind'];coverage=x['coverage']
   if ph=='current'and t in ('T212.02-R2-002','T351-R2-001'):ph='context'
   if t in ('T216-R2-002','T216-R2-006','T216-R2-005') and ph=='current':ph='context'
   if ki=='DICȚIONAR_CESIRO_CITIT' and t=='T314-R2-020':ph='context'
   if t=='T227-R2-021' and ph=='current':ph='context'
   if t in ['T204-R2-025','T204-R2-014','T224-R2-016']and ki in ['RECALCUL_SURSĂ_LIVRARE','TRANSFER_DOCUMENTAT_CĂTRE_DOSARUL_NOMINAL','AUDIT_DOCUMENTAR_RECALCULAT']:coverage='documentary_only'
   v=zmake(t,ki,ph,x['method'],x['oracle'],x['observed'],DATA,'/cases/'+esc(t)+'/'+str(i),x['limit'],coverage);collection[t].append(v)
 f=P/'T314_sql_meniu_chei.json';yy=rd(f);t='T314-R2-012';collection[t].append(zmake(t,'QUERY_MENIU_SQLITE_REEXECUTAT','current','Interogarea SQL_CANALE extrasă din sursa temei actuale.','Canale active în compania 11, sursele RESPINSA trebuie distinse în lista Comenzi.',{'read':yy['actual_menu_query_firm11'],'mutant_filtered':yy['negative_control_same_fixtures_add_key_predicate'],'foreign':yy['actual_menu_query_firm12']},f,'',yy['adjudication']))
 # Replacement relations of R7 semantic erratum are independent of new runtime tests.
 err=rd(ER)
 for i,x in enumerate(err['criteria']):
  t=x['criterion'];collection[t].append(zmake(t,'CORECȚIE_A11_RELAȚIE','correction','Erratum confirmat în raportul A11 al R7',x['accepted_text'],x['adjudication'],ER,'/criteria/'+str(i),x['not_observed'],'source_qualification'))
 A3=E/'R8_pregatire/A03/Registru_A03_R8_final.json';a3=rd(A3);assert h(A3)=='7bdfc31bf06daed0f4f1c7bc19250981c787bf1cdbe13a677f63cf5ee9420e4d';assert len(a3['r8'])==239
 for i,x in enumerate(a3['r8']):
  c=x['criterion'];s=x['status'];check_art(x['dovezi']);ph='current' if s in ['CONFORM_ORACOL_EXECUTAT','PARȚIAL_EXERCITAT','ABATERE_ORACOL_EXECUTAT']else'historical'if s in ['RECALCUL_PE_INSTANTANEU_ISTORIC','DOAR_DOCUMENT_INDEXAT']else'pending' 
  v=zmake(c,s+'_A03',ph,'Raport A03 confruntat cu locatorul și sursele nominale, nu o a doua execuție.',x['historical_requirement'],x['mesurat'],A3,'/r8/'+str(i),x['limita'],'full_criterion_at_reported_layer'if s in ['CONFORM_ORACOL_EXECUTAT','ABATERE_ORACOL_EXECUTAT']else'provenance_only'if s=='DOAR_DOCUMENT_INDEXAT'else 'subcase');collection[c].append(v)
 # A05 draft never accepted in build. Only overridable for previews; do not seal with provisional.
 q=E/'R8_pregatire/A05';final5=q/'Registru_nominal_final_A05_v2.json';files=[final5]if final5.is_file()else[];f=next(iter(files),None)
 if f is None and os.environ.get('A12_R8_PREVIEW')=='1':f=q/'Registru_nominal_progres_A05.json'
 assert f is not None,'A05 final pending'
 if f==final5:assert h(f)=='0e9ec456c2b5d743b0b9492e2f85e6a02f52fa20a3959e390593f04550af67b9'
 a5=rd(f);assert len(a5['rows'])==135
 for path,expected in a5.get('proofs',{}).items():assert h(B/path)==expected,(path,expected)
 for i,x in enumerate(a5['rows']):
  cc=x['criterion'];s=x['classification'];arr=x['observations']; each=0
  for j,z in enumerate(arr):
   check_art(z);layer=z.get('layer','');ph='historical'if 'histor' in layer.lower() or 'DOCUMENTAR'in s else 'current';cov='documentary_only'if s=='REEXECUTAT_DOCUMENTAR'else'full_criterion_at_reported_layer'if x['full_criterion_reexecuted'] else 'subcase';p='/rows/'+str(i)+'/observations/'+str(j)
   collection[cc].append(zmake(cc,s+'_'+str(x.get('verdict',''))+'_'+layer+'_A05',ph,'Rezultat A05 la punctul de intrare indicat; SHA martorului verificat.',x['oracle'],z.get('observed'),f,p,x['remaining']or'Încadrarea completă se limitează la etalonul în fișă.',cov));each+=1
  if each==0:collection[cc].append(zmake(cc,s+'_A05','historical' if x['historical_documents']else'pending','Intrare A05 și existența documentelor individuale.',x['oracle'],s,f,'/rows/'+str(i),x['remaining']or'Sursa actuală nu a fost executată pentru acest criteriu.','provenance_only'))
 # Distinguish numerical results from newer scope, especially C4 amendment.
 t191=E/'R8_pregatire/T191'
 for name in ['Dispozitii_T191.json','T191_supliment_sase_criterii.json']:
  p=t191/name;obj=rd(p)
  for i,z in enumerate(obj['rows']):
   c=z['criterion'];obs=z.get('actual',z.get('observed_limit'));exp=z.get('expected_subcase',z.get('subject'));s=z.get('scope_disposition',z.get('disposition'));ph='current'
   if s and re.search('ARHIV|ISTOR|PROVENIEN|SUBSET.*ACT|INVENTAR',s,re.I):ph='historical'
   if name.startswith('T191_supliment')and c=='T191-R2-007':ph='context'
   if name.startswith('Dispozitii')and c=='T191-R2-007':ph='context'
   collection[c].append(zmake(c,s or 'T191_VERIFICAT',ph,'Coordonatorul a predat probe din Git, Java sau dicționar pentru condiția nominală.',exp,obs,p,'/rows/'+str(i),z.get('scope_limit')or 'Se aplică amendamentul autorului; nu se transferă către cazurile fără probe.'))
  if name.startswith('Dispozitii'):
   for cn in ['Garda_parteneri_C18.json','C18_martor_si_concluzie.json']:
    pp=t191/cn;collection['T191-R2-025'].append(zmake('T191-R2-025','GARDĂ_ORIGINALĂ_ȘI_CONTRAPROBĂ','current','Script original POSIX din directorul cu surse, fixture de control static.','Garda rc0 și 0 diffs cu clienți; pe un mutant minim, o detecție și rc1.',{'positive_rc':0,'counterexample_rc':1,'external_calls':0},pp,'','Este controlul de sursă, nu trafic real către parteneri.'))
 # Extra outside 467.
 p=E/'R8_pregatire/T04.06/Recuperare_oracol_cai.json';x=rd(p);t='T04.06-R3-001'
 collection[t].append(zmake(t,'ORACOL_RECUPERAT_ȘI_TESTAT_PARȚIAL','current','Sursa 8d5d907c90a7f19e5596577a07854a5000a634ca și probe aliniază căile eMAG.','5 căi permise și 17 nepermise eMAG; cele 7 refuzuri EVA Export sunt un lot distinct.',{'allowed':5,'denied_before_sender':17,'targets':['git','instalat'],'still_unverified_EVA_Export':7},p,'','Nu închide toate condițiile, face parte din cohorta de 883, nu din 467.'))
 f=E/'R7_supliment/A12_A06_metadate_Q.json';osnap=rd(f); cg=E/'R7_pregatire/G3/Combinatii_CPP_S1_S2.json'; wm=E/'Reverificare_Flux_S1_aviz_retur_R6.json'
 for c in ['T216-R2-001','T216-R2-002','T216-R2-005','T216-R2-006','T216-R2-007']:
  collection[c].append(zmake(c,'AD_EVA_PROPRIE_DEFAULT','context','Readback în suplimentul meta Q.','Localizează producerea flagului proprietar al comenzii.',{'default':'N','standard_ad_tabs':0,'custom_menu_candidates':3,'triggers_found_in_scope':0},f,'','Alți writers pot exista; metadatele nu dovedesc comportamentul după validare.'))
 for c in ('T354-R2-021','T354-R2-027'):collection[c].append(zmake(c,'ARITMETICĂ_G3_UN_POOL','context','Matricea aritmetică directă în memorie.','16.632 combinații într-un pool cu P1/P2/P3 câte120, S1=20, S2=40.',{'cases_per_jar':16632,'arithmetic_mismatch':0},cg,'','Acoperă doar un pool; nu rezervări persistente pe două comenzi sau două G1.'))
 return collection,{'A03':A3,'A05':f if False else next((z for z in files),q/'Registru_nominal_progres_A05.json'),'T191':t191}
if __name__=='__main__':
 obs,ds=sources();print(len(obs),sum(map(len,obs.values())),ds)

