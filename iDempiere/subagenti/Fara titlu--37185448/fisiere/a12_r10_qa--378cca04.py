from a12_r10_publish import *
from a12_r9_qa import Tags
from urllib.parse import unquote
def qa(dest):
 rr=rd(dest/'A12_raport.json');par=rd(R9/'A12_raport.json');old={r['task']:r for r in par['records']};register=rd(dest/'Registru_reexecutare_R10.json')['rows'];ix={v['criterion']:v for v in register};cat=rd(dest/'Dovezi_criterii.json');ev=cat['evidence'];inv=cat['inverse_task_requirement_links'];expected=collections.defaultdict(set);scores=Counter();visited=set()
 assert len(ix)==len(register)==2619 and len(rr['records'])==len(old)==652
 for v in rr['records']:
  p=old[v['task']];assert H(R9/p['file'])==p['sha256']==v['parent_R9_sha256'];w,pr=rd(dest/v['file']),rd(R9/p['file']);assert w['canonical']==pr['canonical']and w['state_at_new_capture']==pr['state_at_new_capture'];assert H(dest/v['file'])==v['sha256']and H(dest/v['html'])==v['html_sha256']
  c0,c1=criteria(pr),criteria(w);assert [(c['id'],c['normative_content'])for c in c0]==[(c['id'],c['normative_content'])for c in c1];h=Tags();h.feed((dest/v['html']).read_text(encoding='utf8'));assert h.sections==[c['id']for c in c1]
  for a in h.anchors:assert((dest/v['html']).parent/unquote(a.split('#')[0])).exists()or(dest!=R10 and a.startswith('../../')and(E/unquote(a[6:])).exists()),a
  for z,y in zip(c1,c0):
   c=z['id'];assert c not in visited and c in ix;visited.add(c);o=z['R10'];assert o['next']and ix[c]['next']==o['next']and ix[c]['R10']==o['effective_status']and o['prior']==y['R9']['effective_status'];assert z['R9']==y['R9']
   for a in o['effective_evidence_links']:eid=a['id'];assert eid in ev;expected[eid].add((c,w['task'],a['relation']));scores['edges']+=1
   for eid,d in o['observations']:
    assert ev[eid]==d and d['criterion']==c;ref=d['ref'];s=B/ref['path'];assert ref['sha256']==H(s);node=ptr(read(s),ref['pointer']);assert node is not None
    if isinstance(node,dict)and 'references'in node:
     for vr in node['references']:checkref(vr);scores['individual_file_or_line_pointers']+=1
    scores[d['relation']]+=1
   scores['criteria']+=1
  scores['dossiers_and_html']+=1
 assert set(inv)==set(expected)and len(visited)==len(ix)
 for eid,ls in inv.items():assert len(ls)==len(expected[eid])and {(q['criterion'],q['task'],q['relation'])for q in ls}==expected[eid]
 assert sum(x['R10']=='NEEXECUTAT'for x in ix.values())==rr['counts']['R10_NEEXECUTAT'];assert scores['edges']==rr['counts']['total_relations'];assert len(rr['all_ten_zones'])==10;assert [sum(int(z['R10_entry_cohorts'][q])for z in ix.values())for q in ['164','873','167']]==[164,873,167]
 for k,v in rr['input_files'].items():assert H(B/k)==v
 for k,v in rr['assets'].items():assert H(dest/k)==v
 f=dest/'Verificare_R10.json';wr(f,{'utc':now(),'report':{'filename':'A12_raport.json','sha256':H(dest/'A12_raport.json')},'source_R9':S(R9/'MANIFEST_R9.json'),'checked':scores,'only_QA_not_receipt':True});print('qa',sha(f),scores)
if __name__=='__main__':qa(Path('D:/CodexWork/a12-r10-preview')if os.environ.get('A12_R10_PREVIEW')=='1'else R10)
