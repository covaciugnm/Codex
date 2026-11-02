from pathlib import Path as P
import json,hashlib,collections,re
from concurrent.futures import ThreadPoolExecutor
d=P('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');e=d/'executie';out=e/'R4_zone/A03';out.mkdir(exist_ok=True,parents=True);probe=out/'dovezi';probe.mkdir(exist_ok=True)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,default=str,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
reg=j(e/'R6/Registru_reexecutare_R6.json'); recs=[r for r in reg['records'] if r['owner']=='A03'];ids={r['criterion']:r for r in recs}
def pull(t):
 p=e/'R6/taskuri'/('Fisa_'+t+'.json')
 v=j(p); un=set(v['R6_summary']['unexecuted']);w=[]
 for field in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']:
  for c in v.get(field,[]):
   cid=c.get('id',c.get('criterion_id')); 
   if cid not in un or cid not in ids:continue
   r=ids[cid]; en=r['entry_and_oracle_specific_to_case']; w.append({'id':cid,'task':t,'canonical':v.get('canonical'),'source':str(p.relative_to(e)),'hash':h(p),'criterion':c.get('normative_content',c.get('text')),'oracle':c.get('expected_oracle',c.get('expected')),'scope':en.get('expected_structured'),'fixtures':en.get('named_test_fixtures_in_source'),'symbols':en.get('verified_symbol_entrypoints'),'protocol':r['protocol_ref'],'source_evidence_id':c.get('source_evidence_id'),'row':r})
 return w
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=8) as pool:rows=sum(pool.map(pull,sorted(set(r['task'] for r in recs))),[])
 dump(probe/'A03_R6_criterii.json',rows);print('total',len(rows),'tasks',len(set(x['task'] for x in rows))); print(collections.Counter(x['task'] for x in rows).most_common(22))
 for r in rows:
  s=str(r['oracle'])+' '+str(r['criterion']); k=r['id']; 
  if (r['task'] in ('T03','T03.05','T03.06','T154.05','T157.01','T176.01','T199','T194','T29.01','T256','T58','T170','T180') or 'curs' in s.lower() and 'valut' in s.lower()) and re.search(r'(?:[0-9],[0-9]|[0-9]\.[0-9]|[0-9] ?RON|[0-9] ?EUR|USD|[0-9] ?lei|XSD|12/202|08/202|sponsoriz|TVA la încasare|NEROT|procent|valut|register)',str(r['criterion']),re.I):
   print(k, str(r['criterion'])[:170])
