from a12_r8_publish import *
from a12_r8_arch import pool,BASE
import gzip
from html.parser import HTMLParser
class DOM(HTMLParser):
 def __init__(self):super().__init__();self.sections=[];self.href=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='section':self.sections.append(d.get('id'))
  if t=='a':self.href.append(d.get('href'))
@lru_cache(maxsize=300)
def obj(p):return rd(p)
arc={}
for ap in [pool/'index.json',Path('D:/CodexWork/a12-r8-morearchive/index.json'),Path('D:/CodexWork/a12-r8-spec-extra/index.json')]:
 for z in rd(ap):arc[(z['file'],z['oid'])]=z
def qa(dest):
 rp=dest/'A12_raport.json';doc=rd(rp);reg=rd(dest/'Registru_reexecutare_R8.json')['all_rows'];by={x['criterion']:x for x in reg};cat=rd(dest/'Dovezi_criterii.json');ev=cat['evidence'];inv=cat['inverse_task_requirement_links'];r7=rd(R7report);p7={x['task']:x for x in r7['records']};records=doc['records'];n=Counter();directmap=defaultdict(set);seen=set();regstatus=Counter();a11=rd(ER);badlinks={(c['criterion'],ref['id'])for c in a11['criteria']for ref in c['references']}
 assert len(records)==len(set(w['task']for w in records))==652 and len(reg)==len(by)==2619
 assert {rr['task']for rr in records}==set(p7) and len(list((dest/'taskuri').glob('*.json')))==652 and len(list((dest/'fise_html').glob('*.html')))==652
 for rr in records:
  k=rr['task'];f=dest/rr['file'];hh=dest/rr['html'];assert h(f)==rr['sha256']and h(hh)==rr['html_sha256'];assert rr['parent_R7']==p7[k]['sha256']==h(R7/p7[k]['file']);w=rd(f);w7=rd(R7/p7[k]['file']);assert w['task']==k and w['canonical']==w7['canonical']and w['state_at_new_capture']==w7['state_at_new_capture'];cur=criteria(w);prev=criteria(w7);assert [(c['id'],c['normative_content'])for c in cur]==[(c['id'],c['normative_content'])for c in prev]
  dom=DOM();dom.feed(hh.read_text(encoding='utf8'));assert dom.sections==[x['id']for x in cur]
  for uri in dom.href:
   from urllib.parse import unquote
   pp=hh.parent/unquote(uri.split('#',1)[0]);assert pp.exists() or (dest!=R and '../../'in uri and (E/unquote(uri).split('../../',1)[1]).exists()),(rr['html'],uri)
  for c in cur:
   id=c['id'];assert id not in seen and id in by;seen.add(id);row=by[id];sec=c['R8'];assert row['R8_status']==sec['effective_status']and row['normative_text']==c['normative_content']and row['task']==k and row['next_action'] and compact(row['next_action']).strip(),id
   regstatus[row['R8_status']]+=1
   for a in sec['effective_evidence_links']:
    eid=a['id'];assert eid in ev;directmap[eid].add((k,id,a['relation']));n['edges']+=1
    if (id,eid)in badlinks:assert a['relation']=='R7_corrected_context';n['erratum_edges']+=1
   for z in sec['proofs']:
    p=B/z['source']['file'];assert h(p)==z['source']['sha256'],p;assert z['id']in ev and ev[z['id']]==z and z['criterion']==id;d=ptr(obj(p),z['pointer']);assert d is not None
    n['new_link']+=1
    if z['source']['file'].endswith('Rezultate_A12_93_si_supliment.json'):
     for ref in d['references']:
      rn=ref.get('repository_file')or ref.get('path');oid=ref.get('git_blob')
      if oid:
       az=arc.get((rn,oid));assert az,(rn,oid);data=gzip.decompress(Path(az['storage']).read_bytes());assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid
       if 'matching_lines'in ref:
        ls=data.decode('utf8','replace').splitlines()
        for m in ref['matching_lines']:
         l=ls[m['line']-1];assert hashlib.sha256(l.encode()).hexdigest()==m['line_sha256'];n['historical_hashed_lines']+=1
       n['historical_git_ref']+=1
      if 'assertions'in ref:
       p2=B/ref['log']['file'];assert h(p2)==ref['log']['sha256'];ls=p2.read_text(encoding='utf8').splitlines();f2=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')/ref['test_source'];assert h(f2)==ref['test_source_sha']
       for s in ref['assertions']:
        l=ls[s['line']-1];assert hashlib.sha256(l.encode()).hexdigest()==s['hash_line'];n['assertion_lines_verified']+=1
   n['criteria']+=1
  n['html']+=1;n['dossier']+=1
 for eid,rels in inv.items():
  expected=set((z['task'],z['criterion'],z['relation']) for z in rels);assert len(expected)==len(rels);assert expected==directmap[eid],(eid,expected-directmap[eid],directmap[eid]-expected)
 assert set(directmap)==set(inv);assert n['erratum_edges']==10;assert dict(regstatus)==doc['scope']['R8_states'];assert set(by)==seen
 for f,x in doc['source_hashes'].items():assert h(B/f)==x
 for k,v in doc['assets'].items():assert h(dest/k)==v
 assert set(rr['criterion']for rr in reg if rr['in_467'])=={r['criterion']for r in (rd(R7/'Registru_reexecutare_R7.json')['records'])if r.get('R7_state')=='NEEXECUTAT' and r.get('R7_scope_mapped',{} ) and r['R7_scope_mapped']['category']=='FIXTURĂ_EXECUTABILĂ'}
 report={'utc':now(),'executed_by':'A12, control intern reproductibil; evaluarea de 10 aparține numai A11','report':{'file':'A12_raport.json','sha256':h(rp)},'checks':dict(n),'population':652,'criteria':2619,'bidirectional_edge_count':n['edges'],'source_catalog_and_runtime_assertion_integrity':'VERIFICAT','exact_467_records':sum(q['in_467']for q in reg),'still_NEEXECUTAT':regstatus['NEEXECUTAT'],'source_tree_delta':'T352 intră, T366 schimbă stare; canonicele și numărătoarea sunt cele din R3–R7.','implementation_score':None,'audit_score':None}
 wr(dest/'Verificare_R8.json',report);print('QA',h(dest/'Verificare_R8.json'),n,regstatus['NEEXECUTAT'])
if __name__=='__main__':qa(R if os.environ.get('A12_R8_PREVIEW')!='1'else Path('D:/CodexWork/a12-r8-preview'))

