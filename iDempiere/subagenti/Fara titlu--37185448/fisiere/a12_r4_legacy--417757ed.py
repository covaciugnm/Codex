from a12_r3_survey import *
import subprocess as sp,concurrent.futures as cf,urllib.request as ur,urllib.error,ssl,datetime
R4=E/'R4';pro=R4/'probe';pro.mkdir(parents=True,exist_ok=True);raw=rd(D/'legacy_r3.json');rpt=rd(E/'R3/A12_raport.json');reg=rd(B/'capturi/00_STATUS_TASKURI.json');reg=reg if isinstance(reg,list)else reg['taskuri'];ids=[s['task']for s in rpt['records']if s['unknown_functional_definition']]
def be(k,i):
 w=next(w for w in reg if w['id']==k);q=w.get('cerere_proprietar') or '';a=re.search(r'codul «([^»]+)»',q);alias=a[1]if a else w.get('id_vechi');rest=[]
 for v in raw.get(k,[]):
  if v['mode']=='exact_line':rows=[z for z in v['rows'] if v['orig_ref'].endswith(':'+str(z[0]))]
  elif v['mode']=='json_exact_id':rows=[z for z in v['rows'] if isinstance(z[1],dict) and z[1].get('id')==v['alias']]
  else:rows=[z for z in v['rows']if isinstance(z[1],str) and (z[1].startswith('# ')or z[1].startswith('def '))][:4]
  for j,lit in rows:rest.append({'alias':v['alias'],'matches_direct_alias':alias==v['alias'],'path':v['path'],'pointer':j,'source_original_pointer':v['orig_ref'],'oid':v['oid'],'source_revision':v['revision'],'content':lit})
 return {'task':k,'alias':alias,'authority_owner_quote':q,'anchors':rest,'title':w['nume_sugestiv']}
rdo={k:be(k,i)for i,k in enumerate(ids)};wr(pro/'25_aliasuri.json',rdo)
script="""import json,subprocess as sp
root='/home/saga-server/Documents/EvA-Contab'; sha='6df998aee0e514d30856c461962afe99ebd0d113'
def g(*a):
 p=sp.run(['git',*a],cwd=root,stdout=sp.PIPE,stderr=sp.PIPE);return p.returncode,p.stdout.decode(errors='replace')
r={}
for n,q in [('marker', ['grep','-l','-F','ciornă — de validat',sha,'--','*.tsv']),('native',['grep','-n','-e','--native','-e','SAGA_NATIVE_JAR',sha,'--','tools/teste/cabinet_test_jar_montat.sh']),('map',['ls-tree','-r','--name-only',sha,'--','frontend']),('diff',['show','--format=%H %P %s','--no-ext-diff','--find-renames','--unified=2','bfc6cd5278','--','idempiere/plugins']),('names',['diff-tree','--no-commit-id','--name-status','-r','bfc6cd5278']),('D6',['show','--format=%H %P %s','--name-only','d3042a2b69']),('tree_author',['show','--no-patch','--format=%H %P %s','9decf0a1c'])]:
 rc,s=g(*q);ls=s.splitlines(); 
 if n=='map':ls=[x for x in ls if 'map' in x.lower()or 'hart' in x.lower() or 'import' in x.lower()]
 if n=='diff':ls=[l[:580]for l in ls if l.startswith(('commit ','@@','diff --','+++','+')) or 'T36-L4 frontend' in l][:150]
 r[n]={'exit':rc,'rows':ls[:200]}
print(json.dumps(r,ensure_ascii=False))
""";q=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=script.encode(),capture_output=True,check=True,timeout=60);ww=json.loads(q.stdout);wr(pro/'25_Git_cautare.json',ww)
def get(l):
 url='https://acc.eva-org.com/?lang='+l
 try:
  op=ur.build_opener(ur.ProxyHandler({}));res=op.open(ur.Request(url,headers={'User-Agent':'Mozilla/5.0 EVA Audit P01 ReadOnly'}),timeout=7);body=res.read(3000000);lines=body.decode('utf8',errors='replace').splitlines();hits=[i for i,x in enumerate(lines,1) if re.search('saga|idempiere|copilot',x,re.I)];return {'lang':l or '(implicit)','http':res.status,'final_url':res.url,'original_requested':url,'body_length':len(body),'hash':hashlib.sha256(body).hexdigest(),'matched_line_count':len(hits),'matching_lines_only':hits,'title':(re.search(r'<title[^>]*>(.{0,170}?)</title>',body.decode(errors='replace'),re.I)or [None,None])[1]}
 except Exception as ex:return {'lang':l or '(implicit)','error':str(ex)[:220]}
with cf.ThreadPoolExecutor(max_workers=7)as pool:seven=list(pool.map(get,('ro','en','de','hu','bg','el','')))
wr(pro/'T07_03_7_GET.json',{'time':datetime.datetime.now(datetime.UTC).isoformat(),'method':'GET public fără autentificare. Oracolul inițial grep numără liniile HTML, nu expresiile individuale. Fără aprobarea istorică sau dovadă de UI autentificat.','rows':seven});print('7',[(x.get('http'),x.get('matched_line_count'),x.get('error'))for x in seven]);print('git',[(k,x['exit'],len(x['rows'])) for k,x in ww.items()])

