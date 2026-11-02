from a12_r9_publish import *
from html.parser import HTMLParser
from urllib.parse import unquote
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.anchors=[];self.sections=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a':self.anchors.append(d.get('href'))
  if t=='section':self.sections.append(d['id'])
def qa(dest):
 rp=dest/'A12_raport.json';r=rd(rp);par=rd(R8/'A12_raport.json');pidx={z['task']:z for z in par['records']};sub=r['records'];reg0=rd(dest/'Registru_reexecutare_R9.json')['rows'];reg={v['criterion']:v for v in reg0};cat=rd(dest/'Dovezi_criterii.json');ev=cat['evidence'];inv=cat['inverse_task_requirement_links'];links=collections.defaultdict(set);q=collections.Counter();visited=set()
 assert len(sub)==len(pidx)==652 and len(reg)==len(reg0)==2619
 for z in sub:
  k=z['task'];old=pidx[k];pf=R8/old['file'];assert old['sha256']==z['parent_R8_sha256']==H(pf);f,hf=dest/z['file'],dest/z['html'];w,prior=rd(f),rd(pf);assert H(f)==z['sha256']and H(hf)==z['html_sha256']and w['canonical']==prior['canonical']and w['state_at_new_capture']==prior['state_at_new_capture']
  xx,pp=criteria(w),criteria(prior);assert [(a['id'],a['normative_content'])for a in xx]==[(a['id'],a['normative_content'])for a in pp];doc=Tags();doc.feed(hf.read_text(encoding='utf8'));assert doc.sections==[a['id']for a in xx]
  for url in doc.anchors:
   t=hf.parent/unquote(url.split('#')[0]);assert t.exists()or(dest!=R9 and url.startswith('../../')and(E/unquote(url[6:])).exists()),url
  for a in xx:
   c=a['id'];o=a['R9'];assert c not in visited and c in reg;visited.add(c);s=reg[c];assert s['R9']==o['effective_status']and s['next']and s['text']==a['normative_content'];q['criteria']+=1
   for l in o['effective_evidence_links']:
    eid=l['id'];assert eid in ev;links[eid].add((c,k,l['relation']));q['edges']+=1
   for eid,v in o['observations']:
    assert ev[eid]==v and v['criterion']==c;ref=v['ref'];p=B/ref['path'];assert ref['sha256']==H(p);data=ptr(read(p),ref['pointer'])if p.suffix=='.json'else p.read_text(encoding='utf8');assert data is not None
    if ref['path'].endswith('A12_receptii_R9_faza1.json'):
     raw=data;sf=B/raw['proof']['file'];assert sha(sf)==raw['proof']['sha256'];assert (ptr(read(sf),raw['pointer']) is not None if sf.suffix=='.json'else sf.read_text(encoding='utf8')!='');q['primary_A12_A03_receipts']+=1
     if sf.suffix=='.log' and isinstance(raw['observed'],list):
      ls=sf.read_text(encoding='utf8').splitlines()
      for oa in raw['observed']:
       if isinstance(oa,dict)and 'hash_line'in oa:assert hashlib.sha256(ls[oa['line']-1].encode()).hexdigest()==oa['hash_line'];q['script_atomic_lines']+=1
    q['r9_links']+=1
  q['dossiers_and_html']+=1
 assert len(inv)==len(links)
 for eid,rels in inv.items():
  ss={(v['criterion'],v['task'],v['relation'])for v in rels};assert len(ss)==len(rels)and ss==links[eid],eid
 q['177']=sum(x['cohorts']['earlier_177']for x in reg0);q['218']=sum(x['cohorts']['separate_partial_218']for x in reg0);q['38']=sum(x['cohorts']['external_38']for x in reg0);q['882']=sum(x['cohorts']['without_oracle_R8_882']for x in reg0);q['overlap_177_38']=sum(x['cohorts']['external_38']and x['cohorts']['earlier_177']for x in reg0);assert (q['177'],q['218'],q['38'],q['882'],q['overlap_177_38'])==(177,218,38,882,2)
 assert sum(x['R9']=='NEEXECUTAT'for x in reg0)==r['counts']['R9_NEEXECUTAT'];assert q['edges']==r['counts']['total_relations']
 for p,h in r['input_files'].items():assert H(B/p)==h
 for p,h in r['assets'].items():assert H(dest/p)==h
 qc=dest/'Verificare_R9.json';wr(qc,{'utc':now(),'report':{'filename':rp.name,'sha256':H(rp)},'source_R8_immutable':source(R8/'MANIFEST_R8.json'),'checked':q,'qa_only_no_grade':True,'product_acceptance_not_inferred':True});print(H(qc),q,r['counts']['R9_NEEXECUTAT'])
if __name__=='__main__':qa(Path('D:/CodexWork/a12-r9-preview')if os.environ.get('A12_R9_PREVIEW')=='1'else R9)

