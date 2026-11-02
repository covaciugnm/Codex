import pathlib,json,hashlib,collections,re,decimal,statistics,datetime
O=pathlib.Path(__file__).parent; E=O.parent;R=E.parent; BASE=E/'supliment_CESIRO1'; D=BASE/'probe'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
def maybe_value(a,ns):
 for name in ns:
  if a.get(name) is not None:return a[name]
 return None
plan=rd(BASE/'Plan_CESIRO1_R3.json'); basic=E/'A11_gate_CESIRO1_R3.json'; assert h(basic)=='20c9fe20ac028bb7876a261ceed63a9e3617ba413456c080e001f3d46b77ff8c'; Peers=['A08','A08','A06','A02','A05','A09','A03','A12']; record={}
for i,peer in enumerate(Peers,1):
 id=f'EX{i:02d}';f=D/(id+'.json');pf=D/(id+'_peer_'+peer+'.json');x=rd(f);y=rd(pf);seen={};missing=[];fields=[]
 def inc(n,sha,where):
  if not isinstance(n,str)or not isinstance(sha,str)or not re.fullmatch('[0-9a-fA-F]{64}',sha):return
  n=n.strip()
  if n.startswith('http') or '#'in n:return
  exts=('.json','.py','.html','.sql','.log','.txt','.png','.java','.jar','.cjs','.js','.ts','.csv','.gz','.xlsx','.sh','.md','.webp','.xml','.out','.lock')
  if not n.lower().endswith(exts):return
  opt=[D/n, BASE/n, E/n,R/n,O/n, D/(id+'-evidence')/n,D/(id+'-peer-'+peer+'-evidence')/n]
  work=pathlib.Path('D:/CodexWork');eva=work/'eva-audit-p01-readonly-20261102';cs=work/'eva-cesiro1-contract-20261102';opt.extend([work/n,eva/n,eva/'frontend/storefront'/n,cs/n,cs/'backend'/n,cs/'frontend'/n,eva/'idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/corelare'/n,work/'a08-cesiro-deps'/n]);
  if pathlib.Path(n).is_absolute():opt=[pathlib.Path(n)]
  hit=next((p for p in opt if p.is_file()and h(p)==sha.lower()),None)
  key=(n,sha.lower());seen[key]=('VERIFIED'if hit else 'UNRESOLVED')
  if not hit:missing.append([where,n,sha,[(p.as_posix(),h(p))for p in opt if p.is_file()]])
 def scan(v,prefix,where):
  if isinstance(v,dict):
   sha=next((v.get(a) for a in ('sha256','sha256_verified','expected_sha256','file_sha256') if isinstance(v.get(a),str)),None)
   n=next((v.get(a) for a in ('file','path','source','artifact','report') if isinstance(v.get(a),str)),None)
   if n and sha:inc(n,sha,where)
   for k,xx in v.items():
    if isinstance(xx,str):inc(k,xx,where)
    else:scan(xx,k,where)
  elif isinstance(v,list):
   for xx in v:scan(xx,prefix,where)
 for a1,label in [(x,'primary'),(y,'peer')]:scan(a1,'',label)
 candidates=[(k,v)for k,v in y.items() if isinstance(v,str) and h(f)==v]; 
 if id=='EX06':link=(y.get('source_input')or{});assert h(f) in json.dumps(link)
 else:assert candidates or h(f) in json.dumps(y),id
 record[id]={'producer_sha':h(f),'consumer_sha':h(pf),'consumer':peer,'producer_file':f.name,'consumer_file':pf.name,'peer_binds_exact_subject':True,'source_hash_pairs_checked':len(seen),'files_unresolved':missing,'peer_decision':maybe_value(y,['acceptance','peer_verdict','decision','outcome']),'preparation':plan['controls'][i-1]['objective']}
 print(id,len(seen),len(missing),[(m[0],m[1])for m in missing][:5])
for label,sha in [('EX06_erratum_A08.json','1d00f21beb0e69ee459dd3683f0b2298ccbbfb02752bf16773aae28a3fcda983'),('EX06_acceptare_erata_A09.json','e51d8ae5ad0baeacd48eb1d8e6c15a14cd05ea1566ba1c1a1da668bccf0d9fef')]:assert h(D/label)==sha;record['EX06'].setdefault('erratum_chain',{})[label]=sha
w=rd(D/'EX03_C_Q_raw.json'); rows=w['cases']; first=rows[0]; assert first['http']==201 and first['external_detail']['http']==200 and first['external_detail']['body']['total_ron']==87.88
t={r['case']:r for r in rows};assert t['first']['external_detail']['body']['id']!=t['replay_new_app']['external_detail']['body']['id'] and t['zero']['http']==t['negative']['http']==201
raw=D/'EX05-peer-A05-evidence/db-read.json';capt=rd(raw);p05=rd(D/'EX05_peer_A05.json')
a03=rd(D/'EX07_peer_A03.json'); vals=a03['cash_reconciliation'];assert round(float(vals['total'])-float(vals['paid']),2)==57.87;assert abs(sum(float(x['cod'])for x in vals['parcels'])-float(vals['cod_total']))<0.00001
for j in ['git','installed']:
 orig=(O/(j+'-Q.txt')).read_text(encoding='utf-8-sig');foreign=(O/(j+'-foreign.txt')).read_text(encoding='utf-8-sig');ctr=(O/(j+'-without.txt')).read_text(encoding='utf-8-sig')
 assert 'lines=2 total=87.88 seller_present=false' in orig and 'EXT7 2 0.21' in orig and 'EXT8 1 0.21' in orig and 'B-TRACK-for-A-order' in foreign and 'B-TRACK-for-A-order' not in ctr
cx=rd(D/'EX06_acceptare_erata_A09.json'); ex8=rd(D/'EX08_peer_A12.json');record['EX06']['final_technical_corrections']=cx['normative_corrections'];record['EX08']['limits_from_independent_peer']=ex8['limits']
wr(O/'proof_register.json',record);print('record',h(O/'proof_register.json'))

