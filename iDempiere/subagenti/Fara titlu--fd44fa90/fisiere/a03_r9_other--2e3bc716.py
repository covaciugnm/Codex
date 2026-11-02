from a03_r9_trace import *
def form():
 plan=path('T256','02_plan.md');cat='Documentatie/echipa-2026-10-09/00_CHECKLIST_DEFECTE.json';checker='tools/status/checklist_defecte.py';d=wrk/'criterion23';d.mkdir(exist_ok=True)
 rr=[]; 
 for name,planv,scriptv,catv in [('T256_handover_actual_catalog_md5','77e32a4b72','77e32a4b72','bea580e3c6e945488935d144460b66f9183831b7'),('catalog_X191_104006','77e32a4b72','77e32a4b72','d9db5518f68'),('master_audit_R1_1234','77e32a4b72','77e32a4b72','be7279cc24'),('merged_branch_same_blob_negative','77e32a4b72','77e32a4b72','be40731e33'),('integrated_with_old_declared_catalog',sha,sha,'be40731e33'),('integrated_current_catalog',sha,sha,sha)]:
  maps=batch([planv+':'+plan,scriptv+':'+checker,scriptv+':tools/status/status_comun.py',catv+':'+cat]);(d/'status_comun.py').write_bytes(maps[scriptv+':tools/status/status_comun.py'][1]);sc=d/'checklist_defecte.py';sc.write_bytes(maps[scriptv+':'+checker][1]);fc=d/'catalog.json';fc.write_bytes(maps[catv+':'+cat][1]);fp=d/'02_plan.md';b=maps[planv+':'+plan][1];fp.write_bytes(b)
  # Change only the first X1 checklist row; identical bytes elsewhere. The date of plan is retained.
  s=b.decode('utf8');line=next(l for l in s.splitlines() if re.match(r'^\| X\d+ \|',l)); mut=s.replace(line+'\n','',1).encode();assert mut!=b
  trials=[]
  for kind,b0 in [('original',b),('remove_one_required_X_control',mut)]:
   fp.write_bytes(b0);v=sp.run([sys.executable,'-I','-X','utf8',sc,'valideaza',fp,'--catalog',fc,'--auto-audit','--faza','plan'],cwd=d,capture_output=True,timeout=35)
   tx=(v.stdout+v.stderr).decode('utf8',errors='replace').splitlines();trials.append({'trial':kind,'document_sha256':H(b0),'rc':v.returncode,'diagnostic':tx[:12]})
  rr.append({'scenario':name,'objects':{f:{'blob':x[0],'sha256':H(x[1])} for f,x in maps.items()},'tests':trials,'origin':'Catalogul efectiv este determinat din MD5 publicat în plan, 8c716e7e9f0332a62385bbb06897522e, blob 7508a55422fac74465c9305431149edbeee7867e (istoric 178 bloburi distincte). Masterul îmbinat be40731e33 are același blob, nu este un martor independent. Commit d9db5518f68 introduce X191 la 10:40:06; documentul declară 10:40, iar proba K23 este datată 12:11.'})
 J(out/'T256_R2_023_validator.json',{'utc':UTC(),'sha':sha,'criterion':'T256-R2-023','scope':'Scriptul, catalogul și planul identificate în Git. Nu se creează date contabile; comparatorul validează forma și checklistul planului, nu implementarea declarației D394.','inputs':rr});print([(v['scenario'],[t['rc'] for t in v['tests']]) for v in rr])
def merge():
 d=path('T256','');reports=['06_audit_cod_r1.md','06_audit_cod_r2.md','05_raport_executant.md','LOG_MODIFICARI.md']
 refs={f:H(get(d+f)) for f in reports};pairs=[('primul audit, intrare','be7279cc24','2e20fce5a7'),('audit r2, intrare','4eb0274efb','5d8e2c8777'),('audit r2, verdict','371a520fdb','5d8e2c8777')];results=[]
 # Use source objects read-only via alternates, all generated trees live in a fresh temp repo on the same host.
 script="""import json,tempfile,subprocess as sp,os,pathlib
src='"""+repo+"""'
def run(cmd, cwd, input=None):return sp.run(['git']+cmd,input=input,cwd=cwd,capture_output=True)
with tempfile.TemporaryDirectory(prefix='p01-a03r9-merge-') as z:
 w=pathlib.Path(z);run(['init','-q'],w); obj=run(['rev-parse','--path-format=absolute','--git-path','objects'],src).stdout; (w/'.git/objects/info/alternates').write_bytes(obj); result=[]
 for tag,left,right in """+repr(pairs)+""":
  a=run(['rev-parse',left],w).stdout.decode().strip();b=run(['rev-parse',right],w).stdout.decode().strip();r=run(['merge-tree','--write-tree',a,b],w);result.append({'tag':tag,'left':a,'right':b,'rc':r.returncode,'tree_first_line':r.stdout.decode(errors='replace').splitlines()[0],'errors':r.stderr.decode(errors='replace')[:100]})
 # Synthetic conflict control; commits opt-in explicitly scoped to isolated repository.
 (w/'r9.txt').write_text('base\\n');run(['add','r9.txt'],w)
 def com(msg):q=run(['-c','user.name=Audit','-c','user.email=audit@example.invalid','commit','-qm',msg],w);assert q.returncode==0;return run(['rev-parse','HEAD'],w).stdout.decode().strip()
 common=com('base');(w/'r9.txt').write_text('left\\n');run(['add','r9.txt'],w);first=com('left');run(['checkout','-q','--detach',common],w);(w/'r9.txt').write_text('right\\n');run(['add','r9.txt'],w);second=com('right');r=run(['merge-tree','--write-tree',first,second],w);print(json.dumps({'historical':result,'witness':{'rc':r.returncode,'conflict_name':'r9.txt' in r.stdout.decode()}}))
"""
 z=ssh('python3 -',script.encode());assert z.returncode==0,z.stderr[:400];q=json.loads(z.stdout);assert [a['rc'] for a in q['historical']]==[0,0,0] and q['witness']['rc']==1; J(out/'T256_R2_001_merge.json',{'utc':UTC(),'sha':sha,'criterion':'T256-R2-001','input_reports':refs,**q,'scope':'Trei perechi distincte din rapoartele R1/R2 au fost recalculate în Git. Raportul de predare nu identifică masterul din fiecare minut. R1 menționează o repetare la verdict fără o pereche distinctă. Nu se demonstrează toate momentele din cerință.'});print('merge',[r['rc'] for r in q['historical']],q['witness'])
def journal():
 sections=['dovezi-04-executant/buton','dovezi-66-aud-cod-r1/buton']; ss=[]
 for s in sections:
  ff=[path('T156',s+'/p03_'+q+'.txt') for q in ('inainte','dupa')];agg=path('T156',('dovezi-04-executant/auto-verificare' if s.startswith('dovezi-04') else 'dovezi-66-aud-cod-r1/auto-verificare-rulata-de-auditor')+'/C-7.txt')
  ds=batch([sha+':'+f for f in ff+[agg]])
  def parse(b):return {x.split('|')[0]:x.split('|')[1:] for x in b.decode().splitlines() if x.startswith('Q-')}
  fr,to=[parse(ds[sha+':'+f][1]) for f in ff];pop=int(fr['Q-A-IN'][-1]);head0,head1=int(fr['Q-JRN'][0]),int(to['Q-JRN'][0]);summary=ds[sha+':'+agg][1].decode();aggs=re.findall(r'^Q-JRN\|(\d+)$',summary,re.M);agr=int(re.search(r'(\d+) înregistrări',summary)[1]);assert head1-head0==1 and int(to['Q-A-IN'][-1])==0
  ss.append({'snapshot':s,'inputs':{f:{'blob':ds[sha+':'+f][0],'sha256':H(ds[sha+':'+f][1])} for f in ff+[agg]},'actual_source_rows':pop,'account_A_dr_cr_n_before':fr['Q-A-IN'],'account_A_dr_cr_n_after':to['Q-A-IN'],'account_B_dr_cr_n_before':fr['Q-B-IN'],'account_B_dr_cr_n_after':to['Q-B-IN'],'account_B_delta_matches_A':all(__import__('decimal').Decimal(to['Q-B-IN'][i])-__import__('decimal').Decimal(fr['Q-B-IN'][i])==__import__('decimal').Decimal(fr['Q-A-IN'][i]) for i in range(3)),'journal_before':head0,'journal_after':head1,'journal_delta':head1-head0,'auto_verification_journal':aggs,'auto_verification_mutated_rows':agr,'summary_matches_own_inputs':aggs==[str(head0),str(head1)] and pop==agr})
 sql=path('T156','dovezi-02-plan/scripturi/criterii_clona.sql');tx=get(sql);src=original(('fiscal/MutareContMotor.java',''));code=get(src).decode().splitlines();assert 'SELECT \'Q-JRN\', count(*) FROM eva_mutarecont WHERE' in tx.decode()
 # Two in-memory relational states with identical original Q-JRN, different child count.
 import sqlite3
 cx=sqlite3.connect(':memory:');cx.executescript("CREATE TABLE eva_mutarecont(ad_client_id INTEGER,id INTEGER); CREATE TABLE eva_mutarecontlinie(hdr INTEGER,line_id INTEGER); INSERT INTO eva_mutarecont VALUES(11,1)"); N=28; trials=[]
 for count in (N,N-1):
  cx.execute('DELETE FROM eva_mutarecontlinie');cx.executemany('INSERT INTO eva_mutarecontlinie VALUES (1,?)',[(i,) for i in range(count)]);h=cx.execute("SELECT 'Q-JRN', count(*) FROM eva_mutarecont WHERE ad_client_id=?",(11,)).fetchone()[1];ch=cx.execute('SELECT count(*),count(distinct line_id) FROM eva_mutarecontlinie WHERE hdr=1').fetchone();trials.append({'expected_source_rows':N,'actual_children':[int(x) for x in ch],'existing_header_query':h,'stronger_witness':ch==(N,N)})
 cx.close();assert trials[0]['stronger_witness'] and not trials[1]['stronger_witness'] and trials[0]['existing_header_query']==trials[1]['existing_header_query'];J(out/'T156_R2_010_jurnal.json',{'utc':UTC(),'sha':sha,'criterion':'T156-R2-010','snapshots':ss,'source_sql_sha256':H(tx),'source_sql':sql,'actual_Q_JRN':next(x for x in tx.decode().splitlines() if x.startswith("SELECT 'Q-JRN'")),'negative_control':trials,'scope':'Recalcul pe fișierele istorice din Git și martor SQLite sintetic pentru ce poate observa contorul inițial. Proba integrală cere cheile distincte, contul vechi al fiecărui copil și utilizatorul, ora, conturile și perioada operației reale. Fotografiile brute aparțin unor scenarii diferite. Cele două sumare derivate nu sunt numărători independente ale copiilor.'});print('journal',[(r['journal_before'],r['journal_after'],r['actual_source_rows'],r['summary_matches_own_inputs']) for r in ss])
if __name__=='__main__':form();merge();journal()

