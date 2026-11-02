from a12_r6_exec import *
p=E/'R6_pregatire/Calibrare_SQL_Rest2/Reluare_T36Rest_oracol_pozitional.json';assert sha(p)=='3663f6e320618de2730dab635055cd8cb8d4c77c2224a2bc9e8785bc58b421d0';q=rd(p);rows=[]
for i,v in enumerate(q['runs']):
 f=v['result'];assert f['OK']==36 and f['FAIL']==0 and f['rc']==0
 for j,line in enumerate(f['markers']):
  if j in [0,1,2,6,7,8,9,13,22,23,29,30]:
   rows.append({'criterion':'T36.31-R3-001','related_parent_scope':'T36-R3-001 (doar cazul facturi plătite/rest), T36-R2-002 (funcția transferată, nu închiderea transferului)','target':v['target'],'source_file':p.relative_to(B).as_posix(),'pointer':'/runs/'+str(i)+'/result/markers/'+str(j),'sha256':sha(p),'source_software_sql_sha':v['original_sql_sha'],'test_sql_predeclared_oracle':v['sql_target_sha'],'observed':line,'scope':'SQL produs în baza recreată; nu este executarea ferestrei Scadențar pe un rol ERP și nu închide celelalte nouă defecte ale părintelui.'})
r=E/'R6_supliment';r.mkdir(exist_ok=True);out=r/'A12_T36_T36_31.json';wr(out,{'utc':datetime.now(UTC).isoformat(),'immutable_report_sha':sha(E/'R6/A12_raport.json'),'origin':sha(p),'row_count':len(rows),'claim_scope':'Semnul restului și citirea confirmării sunt măsurate pe cazurile nominale. Prima încercare fără POReference și încercarea fără alias numeric rămân arhivate.','rows':rows,'independent_score':None});print(sha(out))

