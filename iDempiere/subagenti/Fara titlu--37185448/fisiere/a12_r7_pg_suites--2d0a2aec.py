from a12_r7_pg_cui import *
from concurrent.futures import ThreadPoolExecutor
from datetime import date
P=E/'R5/sql_batch';out=RP/'SQL';out.mkdir(exist_ok=True);bin=Path('D:/CodexWork/p01-local-pg16/pgsql/bin/psql.exe');pgp='D:/CodexWork/p01-local-pg16/pgpass.conf'
specs={
'TestT159DSql':{'criteria':['T159-R2-032'],'mutation':'Filtrul Origine=SEED de pe UPDATE și DELETE de armonizare este eliminat; datele/oracolele rămân identice.','expected':'Doar SEED poate fi armonizat; rândul MANUAL deschis rămâne intact, repetarea nu modifică nimic.'},
'TestT190StudiiSql':{'criteria':['T190-R2-020','T190-R2-030'],'mutation':'Elimină filtrul de tenant numai în expresia ce citește studiile, nu în seed/în oracole.','expected':'Firma A are doar cele două niveluri proprii active, firma B numai valoarea sa; niciun rând din firma străină.'},
'TestT331Sql':{'criteria':['T331-R2-004','T331-R2-006'],'mutation':'Permite și tipul NC în filtrul listării destinațiilor; păstrează testele și datele.','expected':'Din cele patru tipuri inițiale rămân 3; NC nu trebuie oferit drept sursă contabilă.'},
'TestT354Sql':{'criteria':['T354-R2-013','T354-R2-019'],'mutation':'Dezactivează filtrul tenant al listei de rețete (numai SELECT pentru b.ad_client_id=11), păstrând selecția de produs și seed-ul inițial.','expected':'Sub firma 11 nu apar listele și/sau pozițiile companiei 12; o listă inactivă/invalidă se respinge distinct.'},
'TestT217FiltruSql':{'criteria':['T217-R2-004'],'mutation':'Elimină filtrul pe client în query-urile AWB izolate, fără a modifica parametrii fixture sau numărarea așteptată.','expected':'Lista AWB din C1 nu poate include AWB de la firma B.'}}
def mutate(n,txt):
 c=0;res=[]
 for ln in txt.splitlines():
  nl=ln
  if n=='TestT159DSql'and re.match(r'^(?:UPDATE|DELETE)',ln,re.I):nl=re.sub(r"\s+AND\s+Origine\s*=\s*'SEED'","",ln,flags=re.I)
  elif n=='TestT190StudiiSql'and ln.upper().startswith("SELECT CASE")and 'EVA_StudiiSalariat WHERE AD_Client_ID='in ln:nl=re.sub(r'FROM EVA_StudiiSalariat WHERE AD_Client_ID=(?:1000000|1000001|1000002) AND', 'FROM EVA_StudiiSalariat WHERE',ln)
  elif n=='TestT331Sql'and ln.upper().startswith('SELECT CASE'):nl=re.sub(r"COALESCE\(EVA_TipEvidenta,'CV'\)<>'NC'","1=1",ln,flags=re.I)
  elif n=='TestT354Sql'and ln.upper().startswith('SELECT CASE')and 'SQL_LISTE:'in ln:nl=re.sub(r'b\.ad_client_id=11 AND b\.m_product_id', '1=1 AND b.m_product_id',ln)
  elif n=='TestT217FiltruSql'and ln.upper().startswith('SELECT CASE')and '→ AWB:'in ln:nl=re.sub(r'e\.ad_client_id\s*=\s*(?:7|8)\b','1=1',ln,flags=re.I)
  c+=int(nl!=ln);res.append(nl)
 return '\n'.join(res)+'\n',c
def check(z):
 n,tag,variant=z;f=P/(tag+'_'+n+'.sql');raw=f.read_text(encoding='utf8');mod,changes=mutate(n,raw)
 if variant=='mutant'and not changes:return {'suite':n,'target':tag,'variant':variant,'guard':'INLOCUIRE_NEDISPONIBILĂ','count_changed':0}
 execbuf=(raw if variant=='original'else mod).encode();name='a12r7trial_'+uuid.uuid4().hex[:12];assert re.fullmatch(r'a12r7trial_[a-f0-9]{12}',name)
 with db('postgres',True)as c:c.execute('create database '+name+' template template0')
 try:
  rr=sp.run([bin,'-X','-v','ON_ERROR_STOP=1','-qAt','-h','127.0.0.1','-p','56481','-U','audit_owner','-d',name],env=dict(os.environ,PGPASSFILE=pgp,PGCLIENTENCODING='UTF8'),input=execbuf,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=35)
 finally:
  with db('postgres',True)as c:c.execute('drop database '+name)
 log=out/(tag+'_'+n+'_'+variant+'.pglog');data=rr.stdout.decode('utf8',errors='replace');log.write_text(data,encoding='utf8');wf=out/(tag+'_'+n+'_'+variant+'.sql');wf.write_bytes(execbuf);lines=data.splitlines();return {'suite':n,'target':tag,'variant':variant,'sql_original_sha':sha(f),'jar_sha':sha(sec/('cod-master-contab.jar'if tag=='git'else 'com.eva.ro.contab_13.0.0.jar')),'changed_lines':changes if variant=='mutant'else 0,'executed_sql':wf.name,'sql_sha':sha(wf),'exit':rr.returncode,'all_markers':[{'line':i,'value':s}for i,s in enumerate(lines,1)if re.match(r'^\s*(OK|FAIL)\b',s)],'OK':sum(s.lstrip().startswith('OK')for s in lines),'FAIL':sum(s.lstrip().startswith('FAIL')for s in lines),'errors':[s for s in lines if 'ERROR:'in s],'log':log.name,'logsha':sha(log),'external_writes':0,'fixture_dropped':True}
if __name__=='__main__':
 jobs=[(n,t,v)for n in specs for t in ['git','instalat']for v in ['original','mutant']]
 with ThreadPoolExecutor(max_workers=3)as px:rows=list(px.map(check,jobs))
 wr(out/'Matrice_SQL_reala_R7.json',{'utc':datetime.now(UTC).isoformat(),'expectations_before_mutation':specs,'engine':'PostgreSQL 16 local, baze separate pe încercare și target. Datele contabile sunt sintetice; în suita PG, markerul FAIL nu necesită return code nenul al psql.','rows':rows});print([(x['suite'],x['target'],x['variant'],x.get('OK'),x.get('FAIL'),x.get('errors'))for x in rows])

