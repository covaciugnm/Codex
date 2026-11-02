from a12_r3_survey import *
from functools import lru_cache
from collections import defaultdict,Counter
from pathlib import Path
import unicodedata,json,re,subprocess as sp
R=E/'R5';R4=E/'R4';P=E/'R5_pregatire';cat=rd(R4/'Dovezi_criterii.json')['evidence'];oldqueue={r['criterion']:r for r in rd(R4/'Registru_1868.json')['records']};loc=rd(R/'probe/locatori_EV4_verificați.json')['by_id']; repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
def normalize(v):return ''.join(c for c in unicodedata.normalize('NFD',str(v).casefold())if unicodedata.category(c)!='Mn')
def clean(v): return re.sub(r'[\x60*]', '',v).strip() if isinstance(v,str)else v
def md_fields(row):return [p.strip().replace(r'\|','|')for p in re.split(r'(?<!\\)\|',row.strip().strip('|'))]
def suite_ids(s):return list(dict.fromkeys(re.findall(r'\bTest[A-Z][A-Za-z0-9_]+\b',s)))
def file_refs(s):return list(dict.fromkeys(re.findall(r'(?<![A-Za-z0-9_])(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.(?:java|py|html|tsx?|sh|sql|tsv|json|md|out|txt|xsd)\b',s,re.I)))
fmap=defaultdict(list);rootfiles={}
for t in sp.check_output(['rg','--files',str(repo)]).decode('utf8',errors='replace').splitlines():
 p=Path(t);rel=p.relative_to(repo).as_posix();fmap[p.name.casefold()].append(rel);rootfiles[rel]=p
@lru_cache(maxsize=4096)
def resolve_file(tag):
 nm=Path(tag).name.lower();v=fmap.get(nm,[]);prefer=[s for s in v if s.lower().endswith('/'+tag.lower())or s.lower()==tag.lower()]
 if len(prefer)==1:return prefer[0]
 if len(v)==1:return v[0]
 return None
@lru_cache(maxsize=4096)
def decls(name,fn=None):
 rel=resolve_file(name+'.java')
 if not rel:return None
 ll=rootfiles[rel].read_text(encoding='utf8',errors='replace').splitlines();rx=rf'\b{re.escape(fn)}\s*\(' if fn else rf'\b(?:class|record|interface|enum)\s+{re.escape(name)}\b';hits=[]
 for n,line in enumerate(ll,1):
  if re.search(rx,line) and not line.strip().startswith(('*','//')):hits.append((n,line.strip()))
 hits.sort(key=lambda z:(not bool(re.search(r'\b(public|protected|private|static)\b',z[1])),z[0]))
 return {'file':rel,'line':hits[0][0] if hits else None,'symbol':name+('.'+fn if fn else ''),'line_kind':'declarație sau referință identificată în cod; nu probă comportamentală','sha256':sha(rootfiles[rel])} if hits else None
def explicit_markers(txt,rx):return list(dict.fromkeys(m[0][:145] for m in re.finditer(rx,txt,re.I)))[:7]
def fields(c):
 ev=cat[c['source_evidence_id']];data=ev['content_or_observation'];src=str(ev['source']);pt=ev['pointer'];out={'source_file':src,'source_pointer_original':pt,'sha_or_git_blob':ev['sha_or_oid'],'source_authority_class':ev['level']}; doc={}
 if isinstance(data,dict) and isinstance(data.get('row'),str)and data.get('columns'):
  cols=[normalize(q)for q in data['columns']];values=md_fields(data['row']);doc=dict(zip(cols,values));out['original_table']={'columns':data['columns'],'values':values,'heading':data.get('heading')};out['original_heading_or_scope']=data.get('heading')
  fun=lambda keys:[v for k,v in doc.items()if any(s in k for s in keys)]
  oracle=' | '.join(fun(['astept','oracol','tinta','obiectiv numeric','valoare finala']));cmd=' | '.join(fun(['comanda','proba','dovada','cum verific','metoda']));context=' | '.join(fun(['cabinet','integrare','mediu','perioada','initial','precond','actor','date prob','t0']))
  contract=' | '.join(fun(['criter','indicator','rezultat (']));out['expected_structured']=clean(oracle) if oracle else None;out['recipe_from_own_row']=cmd or None;out['environment_or_legacy_baseline']=context or None;out['constraint_from_own_row']=clean(contract) if contract else None
 elif isinstance(data,dict) and 'indicator' in data:
  out.update(expected_structured=data.get('target'),recipe_from_own_row=data.get('proof'),environment_or_legacy_baseline=data.get('T0'),constraint_from_own_row=data.get('indicator'))
 else:
  out['expected_structured']=None;out['recipe_from_own_row']=None;out['environment_or_legacy_baseline']=None;out['constraint_from_own_row']=None
 # Source-declared observations/thresholds are independently parsed from original fields; descriptive source text is kept only when it helps define a target.
 original=c['normative_content'];ctx=out.get('constraint_from_own_row')or original;cmd=out.get('recipe_from_own_row') or '';s=ctx+' '+cmd;exp=c['expected_oracle']
 out['named_test_fixtures_in_source']=suite_ids(s)
 pairs=list(dict.fromkeys(re.findall(r'\b([A-Z][A-Za-z0-9_]{2,})\.([a-z][A-Za-z0-9_]{2,})\s*\(',s)))
 syms=[]
 for cl,fn in pairs[:7]:
  z=decls(cl,fn)
  if z:syms.append(z)
 for cl in out['named_test_fixtures_in_source'][:4]:
  z=decls(cl)
  if z:syms.append(z)
 out['verified_symbol_entrypoints']=syms
 out['versioned_paths_uniquely_resolved']=[{'literal':t,'actual':p,'sha256':sha(rootfiles[p])}for t in file_refs(ctx+' '+cmd)[:10] if (p:=resolve_file(t))]
 out['native_entities_explicit']=list(dict.fromkeys(re.findall(r'\b(?:M|AD|C|GL|EVA|I|PP)_[A-Za-z][A-Za-z0-9_]{2,66}\b',ctx+' '+cmd)))[:10]
 out['roles_or_interfaces_named_in_source']=explicit_markers(ctx+' '+cmd,r'(?:\b(?:GardenAdmin|GardenUser|SuperUser|AD_Role|accountant|gestionar(?:ul)?|contabil(?:ul)?|terminal(?:ul)?|operator(?:ul)?|responsabil(?:ul)?)\b[^,;|()\n]{0,46}|(?:ecranul|fila|butonul|rolul|meniul)\s+[«„"][^»”"]+[»”"])')
 out['fixture_literals_verbatim']=explicit_markers(ctx+' '+cmd,r'(?:\b[A-Z]{1,5}\d*\s*[=:×]\s*[-+]?\d+(?:[,.]\d+)?(?:\s*(?:buc|RON|EUR|USD|h|zile|seturi))?|\b\d+(?:[,.]\d+)?\s*(?:[×x]\s*\d+|buc(?:ăți)?|RON|EUR|USD|zile|sesiuni|locatori|scheme|comenzi|msec|procentaje|%)|\b\d{2}[./-]\d{2}[./-]\d{4}\b|\b\d{4}-\d\d-\d\d\b|(?:stoc|cantitate|preț|sold|client|firma|gestiune|schema|lot)\s*[=:]\s*[A-Za-z\d.,-]{1,18})')
 out['negative_inputs_verbatim']=explicit_markers(ctx+' '+cmd,r'(?:„(?:-1|0|abc|36501)”|«(?:-1|0|abc|36501)»|(?:refuz|respinge|ambiguu|necunoscut|concurent|repetarea|duplicat|stornarea|nul|inactiv)\w*\s+[^;|]{3,74})')
 original_rowsource=out.get('original_table') or 'numeric'
 # An executable example and business outcome have separate maturity.
 namedcmd=bool(out['named_test_fixtures_in_source'] or syms or re.search(r'\bSELECT\b|\bgrep\b|\bpython3?\s+|\bbash\s+|\\.(?:sh|py)\s+',cmd,re.I));out['executable_recipe_declared']=namedcmd
 outcome=out['expected_structured']; out['business_oracle_missing']=not bool(outcome) or bool(isinstance(outcome,str)and (outcome.strip().casefold() in ('ok','da','făcut','—','test') or normalize(outcome)==normalize(ctx).strip()))
 out['required_scenario_gaps']=[]
 if not namedcmd and not out['roles_or_interfaces_named_in_source']:out['required_scenario_gaps'].append('punct de intrare sau acțiune de rol nominală')
 if not out['fixture_literals_verbatim'] and not out['named_test_fixtures_in_source']:out['required_scenario_gaps'].append('identitate/date de intrare ori fixtură numită')
 if out['business_oracle_missing']:out['required_scenario_gaps'].append('valoare țintă sau comportament independent de descriere')
 if not out['negative_inputs_verbatim']:out['required_scenario_gaps'].append('contraexemplu delimitat în această sursă')
 return out
def workload(rows):
 oo=[]
 for rr in rows:
  w=rd(R4/rr['file']);k=rr['task'];allc=[*w['operative_criteria_and_audit_criteria'],*w['R3_new_criteria'],*w['R4_new_criteria']]
  for c in allc:
   if c['id']not in oldqueue and c['current']['status']!='NEEXECUTAT':continue
   f=fields(c);p=oldqueue.get(c['id'],{});oo.append({'task':k,'criterion':c['id'],'technical_owner':p.get('zone_owner') or c.get('actor_or_role'),'originally_in_1868':c['id']in oldqueue,'R4_status':c['current']['status'],'component_source':f,'protocol_group':p.get('actual_specialist_if_needed'),'external_split':p.get('resource_split'),'source_not_an_accepted_runtime':True})
 return oo
if __name__=='__main__':
 import concurrent.futures as cf
 rr=rd(R4/'A12_raport.json')['records'];rows=[]
 with cf.ThreadPoolExecutor(max_workers=6)as px:
  for part in px.map(lambda v:workload([v]),rr):rows.extend(part)
 wr(R/'probe/parametri_individuali_din_sursa.json',{'protocol':'Nu copiează oracolul într-un șablon. Păstrează valorile originale distinct de comandă, fixtură, markerii de intrare și datele lipsă. Clasele și metodele provin din fișiere realmente rezolvate, nu dintr-un rol ales generic. Datele din surse descriptive nu se transformă în oracole normative.','records':rows});print(len(rows),sum(bool(r['component_source']['original_table'])for r in []),sum(bool(x['component_source']['executable_recipe_declared'])for x in rows),sum(bool(x['component_source']['expected_structured'])for x in rows))

