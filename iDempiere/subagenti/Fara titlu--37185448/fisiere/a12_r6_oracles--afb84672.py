from a12_r6_exec import *
from collections import Counter,defaultdict
from functools import lru_cache
import unicodedata
def strip(x):return ' '.join(re.findall('[a-z0-9_]+',''.join(c for c in unicodedata.normalize('NFD',str(x).lower())if unicodedata.category(c)!='Mn')))
def edgesource(p):return {'path':p.relative_to(repo).as_posix()if p.is_relative_to(repo)else p.relative_to(E).as_posix(),'sha':sha(p)}
@lru_cache(maxsize=1024)
def lines(p):return p.read_text(encoding='utf8',errors='replace').splitlines()
testpaths=defaultdict(list)
for z in (repo/'idempiere/plugins').glob('*/test/**/*.java'):testpaths[z.stem].append(z)
@lru_cache(maxsize=512)
def java_candidates(p):
 out=[];ls=lines(p)
 for i,l in enumerate(ls):
  if not re.search(r'\b(?:chk|check|verif|verifica|ok|egal|eq|caz|assume|assertEquals|identic)\s*\(',l,re.I):continue
  stmt=l.strip();j=i
  while ';'not in stmt and j<len(ls)-1 and j-i<12:
   j+=1;stmt+=' '+ls[j].strip()
  vals=re.findall(r'"((?:\\.|[^"\\]){7,})"',stmt)
  if len(stmt)>6500 or not vals:continue
  out.append((i+1,j+1,stmt,vals))
 return out
def score_java(label,fragment):
 norm=strip(label);f=strip(fragment)
 if len(f)<12 or len(f.split())<3:return 0
 if f in norm:return len(f)
 return 0
def javapred(suite,literal):
 fs=testpaths.get(suite,[])
 if len(fs)!=1:return None
 p=fs[0];cand=[]
 for a,b,stmt,vals in java_candidates(p):
  score=max([score_java(literal,v)for v in vals]or[0])
  if score>=16:cand.append((score,a,b,stmt))
 if not cand:return None
 cand.sort(reverse=True)
 if len(cand)>1 and cand[0][0]==cand[1][0]:return None
 score,a,b,stmt=cand[0];return {**edgesource(p),'start':a,'end':b,'predicate_verbatim':stmt,'scope':'Condiția și pragul sunt ale testului original, nu un oracol de business independent.'}
@lru_cache(maxsize=256)
def sqlcand(p):
 out=[]
 for i,l in enumerate(lines(p),1):
  if 'THEN' not in l.upper()or 'FAIL'not in l.upper():continue
  label=re.search(r'\$m\$(.*?)\$m\$',l);other=re.search(r"(?:THEN\s+'OK\s*|END\s*\|\|\s*)'([^']{10,})'",l,re.I)
  if label:out.append((i,l,label[1]))
  elif other:out.append((i,l,other[1]))
 return out
def sqlpred(file,raw):
 p=E/file
 if p.suffix!='.pglog':return None
 sql=p.with_suffix('.sql')
 if not sql.is_file():return None
 vals=[(len(strip(msg)),i,line,msg)for i,line,msg in sqlcand(sql)if len(strip(msg))>9 and strip(msg)in strip(raw)]
 vals.sort(reverse=True)
 if not vals or len(vals)>1 and vals[0][0]==vals[1][0]:return None
 n,i,line,msg=vals[0];e=re.search(r'\$e\$(.*?)\$e\$',line);cond=re.search(r'CASE WHEN\s+(.*?)\s+THEN',line,re.I)
 if not cond:return None
 return {**edgesource(sql),'start':i,'end':i,'literal_threshold':e[1]if e else None,'predicate_verbatim':cond[1],'scope':'Predicat SQL predeclarat în instrucțiunea generată înaintea execuției PG. Descrierea rezultatului este separată.'}
r=E/'R5';obs=rd(E6/'Contraste_108_R5.json')['records'];ev=rd(r/'Dovezi_criterii.json')['evidence'];queue=rd(r/'Registru_reexecutare_R5.json')['records'];reg={v['criterion']:v for v in queue};out=[];types=Counter()
for c in obs:
 for x in c['observed_raw_R5']:
  eid=x['r5_id'];e=ev[eid];decl=x['source_declared_target'];kind=e['level'];entry=x['entry'];spec=None;assessment=None
  if decl is not None:
   category='PRAG_EXPLICIT_ÎN_R5';spec={'declared_target':decl,'input':x['input']}
  elif kind in ('EXECUȚIE_COMPONENTĂ_ASERȚIUNE','SQL_PRODUS_PORTAT_POSTGRESQL'):
   file=e['source'].removeprefix('executie/');spec=sqlpred(file,x['measured']) or javapred(Path(entry).stem,x['measured'])
   category=('PREDICAT_DE_TEST_LOCALIZAT'if spec else 'CONDIȚIE_DE_TEST_NERECUPERATĂ_NU_SE_ACORDĂ_CONFORMITATE')
  elif kind=='SIMULATOR_HTTP_LOOPBACK':
   category='CONTRACT_LOCAL_ȘI_ABSENȚĂ_ORACOL_INTEGRAL';spec={'observed':x['measured'],'source':e['source'],'norm':c['norm'],'exact_threshold_independently_known':None}
  elif kind=='REPRODUCERE_EXECUTOR_NOMINALĂ':
   category='POLITICĂ_FUNCȚIONALĂ_ÎN_CERINȚĂ';spec={'norm':c['norm'],'observed':x['measured'],'strict_pointer':e['pointer'],'scope':c['assessment_R6_by_case']}
  else:category='ORACOL_NUMERIC_INDEPENDENT_NEIDENTIFICAT'
  types[category]+=1
  out.append({'r5_id':eid,'criterion':c['criterion'],'observation':x['measured'],'layer':x['artifact_or_protocol'],'numeric_basis':category,'original_status':c['classification'],'oracle_or_verified_locator':spec,'authorized_parent_contract':c['independently_declared_target'],'R6_subcase_evaluation':c['assessment_R6_by_case'],'permit_automatic_pass':False})
assert len(out)==487 and len({q['r5_id']for q in out})==487
wr(E6/'Oracole_487_EV5.json',{'source_R5':sha(r/'A12_raport.json'),'method':'Recitire originală. Pentru cod și SQL se acceptă un fragment de mesaj normalizat identificat fără egalitate între două site-uri, localizat în testul de pe SHA fixat sau într-o instrucțiune SQL generată înainte de rulare. Starea în rândul de mai jos nu dovedește scopul integral al cerinței. Dacă predicatul original nu poate fi identificat, observația rămâne descriptivă.','states':types,'rows':out})
anx=rd(E/'R6_pregatire/Anexe/Anexe_nominale_R5.json');a={x.get('criterion')or x.get('id'):x for x in anx['rows']};empty=[q for q in queue if not q['individual_next_step']];repaired=[]
for v in empty:
 c=v['criterion'];x=v['entry_and_oracle_specific_to_case'];ax=a.get(c,{})
 params={k:x.get(k) for k in ['environment_or_legacy_baseline','fixture_literals_verbatim','negative_inputs_verbatim','roles_or_interfaces_named_in_source','native_entities_explicit','verified_symbol_entrypoints']if x.get(k)}
 repaired.append({'task':v['task'],'criterion':c,'owner':v['owner'],'source':x['source_file'],'source_pointer':x['source_pointer_original'],'source_identity':x['sha_or_git_blob'],'protocol':v['protocol_ref'],'action_to_execute':x['recipe_from_own_row']or(x['verified_symbol_entrypoints']if x['verified_symbol_entrypoints']else 'Rezolvă operația concretă din sursa indicată.'),'instance_to_prepare':params,'independent_oracle_to_compare':x['expected_structured']or x.get('constraint_from_own_row'),'nominal_scope_from_source':x.get('constraint_from_own_row'),'annex_proposals_not_execution':ax.get('anchors',[]),'prior_R5_state':v['R5_state'],'decision':'EXECUTĂ_SCENARIUL_CU_PRAGUL_DECLARAT'if x.get('expected_structured')and x.get('recipe_from_own_row')else'PARAMETRU_LIPSĂ_IDENTIFICAT','further_input':'Contraexemplul sau schimbarea numerică trebuie măsurate în operația identificată pentru '+c+'; o rulare pe alt JAR nu adaugă un al doilea scenariu.'})
assert len(repaired)==81;wr(E6/'Actiuni_81_reconstituite.json',{'source':sha(r/'Registru_reexecutare_R5.json'),'record_count':81,'records':repaired});print('oracle',types,sha(E6/'Oracole_487_EV5.json'),'actions',sha(E6/'Actiuni_81_reconstituite.json'))

