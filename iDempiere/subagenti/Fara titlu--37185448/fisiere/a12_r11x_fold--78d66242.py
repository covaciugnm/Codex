from a12_r11x_base import *
sources={}
def get(f,hsh=None):
 r=ref(f)
 if hsh:assert r['sha256']==hsh,str(f)
 sources[r['path']]=r
 return read(f)
first=A/'Registru_6709_initial.jsonl.gz';raw=lines(first);R={z['path']:z for z in raw}
def addr(z):return z.get('path')or z.get('file')
def add(path,oid,error,who,pointer,source,axis,scope,sub=None):
 assert path in R and R[path]['git_oid']==oid,(path,oid)
 rr=R[path];display={'executor':who,'source_file':rel(source),'source_sha256':sources[rel(source)]['sha256'],'pointer':pointer,'scope':scope,'result':error,'axes':axis}
 if sub:display['limits_and_own_axis_values']=sub
 rr['evidence'].append(display)
 for name in axis:
  assert name in axes
  rr['axis'][name]='OBSERVED_ONLY_AT_LINKED_SCOPE'
 rr['qualifying_executor']=sorted({e['executor']for e in rr['evidence']})
for filename,hsh,key in [('Python/Registru_Python.json','72280f397ff0b576b9b7013f15b86b389621c0b8ac3b9b730e52f1c0745b6726','git_oid'),('Surse_web_si_config/Registru_sintaxa_si_controle.json','ee5431e29d72fd8f82d48ba9690db71bf3a8d473d7a33ed5eff0194903b26f70','git_oid'),('Java/Registru_sintaxa_Java.json','550ce1a4ce0933dc074aa57f2da4c560371cb37e1bad8a929fcfb0d7b0f4c604','git_object')]:
 sf=O/filename;j=get(sf,hsh);assert j.get('head',j.get('target'))==head
 for i,row in enumerate(j['rows']):add(row['path'],row[key],row['result'],'COORDONATOR','/rows/'+str(i),sf,['static'],'Parser/compiler-front-end with negative; does not execute application.')
for filename,hsh,k,uid in [('Surse_web_si_config/Triaj_cinci_fisiere.json','28a91f8ca4987442c4993d411ddc52abffaffd9cd04d2e061c49bf8500dd5d90','rows','git_oid'),('Surse_web_si_config/Martori_lexicali_XSD.json','da0c78fcaee0757bb6e8b57b09b69cee1ef4124c61305cf42afb765ac0e22486','cases','oid')]:
 sf=O/filename;j=get(sf,hsh)
 for i,z in enumerate(j[k]):add(z['file'],z[uid],z.get('classification','REPRODUCED_LEXICALLY'),'COORDONATOR','/'+k+'/'+str(i),sf,['static','inspected'] if k=='rows'else['static','inspected','reproduced'],'Triage to distinguish known negative fixtures and defective XSD copies. Lexical reproduction is not ERP runtime.')
for zone in ['A01','A06']:
 root=O/zone;mf=root/('Manifest_A01_R11.json'if zone=='A01'else'Manifest_A06_R11_Git.json');m=get(mf,'ced5f42a858ee706f1c76b871276574cbc3a606cfbb50dff4379bffe186f044b'if zone=='A01'else'02346069023d89b46da4a6779c49ddb4164217cb7e3d8902ec47731292ec8243'); v=m.get('artifacts',m.get('files',{}))
 for nm,hs in v.items():
  p=root/nm;assert sha(p)==(hs if isinstance(hs,str)else hs['sha256']),(p,hs)
 files=list((root/'fise').glob('*.json'))if zone=='A01'else list(root.glob('Fisa_*.json'))
 assert len(files)==5
 for p in files:
  j=get(p);fv=j['file'];path=fv['path_exact'];assert fv['ref_sha']==head and fv['git_oid']==d[path]['git_object']
  for i,c in enumerate(j['controls']):
   a=c['axes']
   if zone=='A01':ax=[k for k,v in a.items()if isinstance(v,dict)and v.get('observed')is True]
   else:ax=[k for k in ['static','inspected','exercised','bindingVerified','reproduced']if a.get(k)] # scopes and limits come from nominal owner; blocked text is boundary only
   add(path,fv['git_oid'],c.get('verdict'),zone,'/controls/'+str(i),p,ax,c.get('normative_ref',c.get('purpose','')),a)
index=A/'A12_index_probe_nominale_01.json';j=get(index,'834b8d0f1feaf8bf49bd0c396480644bd63ab1a48482a73ece3efbdfd6d0c026')
primary={}
def pointer(data,addr):
 for f in addr.strip('/').split('/'):
  data=data[int(f)]if isinstance(data,list)else data[f]
 return data
for x in j['inputs']:
 f=B/x['path'];j1=get(f,x['sha256'])
 for pr in j1['inputs']:
  z=B/pr['path'];primary.setdefault(pr['path'],get(z,pr['sha256']));assert pointer(primary[pr['path']],pr['pointer'])is not None
 add(j1['path'],j1['git_oid'],'OBSERVATION_LIMITEE', 'A12','/inputs',f,j1['axis_positive_for_exact_scope_only'],j1['entry_and_extent'],j1['limit'])
# Cross-validate raw logs of all A12 primary artifacts. Primary records never substitute logs.
def checkraw(v):
 if isinstance(v,dict):
  if 'path'in v and 'sha256'in v and isinstance(v['path'],str)and v['path'].startswith('executie/'):
   assert sha(B/v['path'])==v['sha256'],v['path']
  for e in v.values():checkraw(e)
 if isinstance(v,list):
  for e in v:checkraw(e)
for j in primary.values():checkraw(j)
review={k:sum(r['axis'][k]!='UNVERIFIED'for r in R.values())for k in axes};by={o:{'total':sum(r['owner']==o for r in R.values()),'with_evidence':sum(r['owner']==o and bool(r['evidence'])for r in R.values()),'functional_axis_at_bound_scope':sum(r['owner']==o and r['axis']['exercised']!='UNVERIFIED'for r in R.values())}for o in sorted({r['owner']for r in R.values()})}
out=A/'Registru_6709_val_01.jsonl.gz';assert not out.exists()
with out.open('wb')as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0)as s:
  for z in R.values():s.write((json.dumps(z,ensure_ascii=False,separators=(',',':'))+'\n').encode())
q=lines(out);assert len(q)==6709 and {r['id']for r in q}=={r['id']for r in raw};assert all(z['file_verdict']is None for z in q)
meth=A/'Metoda_val_01';meth.mkdir(exist_ok=True)
import shutil
for s in ['base','fetch','fetch_social','register','java','pg','cal','win','t232','cases','fold']:
 fn='a12_r11x_'+s+'.py';shutil.copyfile(Path(os.environ['TEMP'])/fn,meth/fn)
count=sum(bool(r['evidence'])for r in R.values());sf=A/'Handoff_registru_val_01.json';save(sf,{'utc':now(),'head':head,'gate':ref(gate),'plan':ref(plan),'previous':ref(first),'current':ref(out),'source_artifacts':list(sources.values()),'sources_for_reproduction':[ref(f)for f in sorted(meth.glob('*.py'))],'structure_checked':{'files':6709,'unique_ids':len({r['id']for r in R.values()}),'zones':by,'at_least_one_observation_by_file':count,'no_observation_yet':6709-count,'distinct_files_by_axis':review,'no_complete_file_verdict':True},'limits':['Registre cumulativ de execuție intermediară. În acest val au semnat dovezi coordonatorul, A01, A06, A12. Propunerea owner/peer rămâne, dar apare distinct executorul real.','Axele pentru teste, fixtures și JAR-uri se referă la intrarea sau partea exactă, uneori la consumarea unei fixturi. Nu sunt produs integral, demonstrație de deployment sau aprobare independentă.','Un rând fără probe își păstrează explicit toate axele neverificate. Fișierele fizic exportate din Git pentru calcul au exclusiv proveniență, nu credit.','Preluarea loturilor suplimentare ale celor 10 zone continuă incremental fără schimbarea acestui val. Nu este acordată nicio notă.']});print(ref(sf),ref(out),count,review)

