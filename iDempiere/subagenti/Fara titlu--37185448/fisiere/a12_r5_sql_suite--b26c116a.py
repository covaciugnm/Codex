from a12_r5_calibrated import *
import subprocess as sp, gzip,uuid,os,concurrent.futures as cf,shutil,datetime
out=E/'R5/sql_batch';out.mkdir(exist_ok=True);pgdir=Path('D:/CodexWork/p01-local-pg16');pg=pgdir/'pgsql/bin/psql.exe';env=dict(os.environ,PGPASSFILE=str(pgdir/'pgpass.conf'),PGCLIENTENCODING='UTF8',PGCONNECT_TIMEOUT='4')
def sql(db,s,timeout=55):
 return sp.run([str(pg),'-X','-qAt','-F','|','-v','ON_ERROR_STOP=1','-U','audit_owner','-h','127.0.0.1','-p','56481','-d',db],input=s.encode('utf8'),capture_output=True,env=env,timeout=timeout)
deps=temp/'all_deps';deps.mkdir(exist_ok=True)
for p in [base,next(sec.glob('org.adempiere.base.process_*.jar')),*Path('D:/CodexWork/eva-a01-java/lib').glob('*.jar'),*Path('D:/CodexWork/a05-support-jars').glob('*.jar')]:
 if not(deps/p.name).exists():(deps/p.name).hardlink_to(p)
tp={}
for tag,j in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]:
 plugdir=temp/('plugin_'+tag);plugdir.mkdir(exist_ok=True);target=plugdir/'com.eva.ro.contab_13.0.0.jar'
 if not target.exists():target.hardlink_to(j)
 tp[tag]=plugdir
def each(data):
 tag,src=data;n=src.stem;j=tp[tag]/'com.eva.ro.contab_13.0.0.jar';dst=temp/('sql_'+tag+n);dst.mkdir(exist_ok=True);cp=';'.join([str(dst),str(j),str(base),str(next(sec.glob('org.adempiere.base.process_*.jar'))),str(deps/'*'),str(plug/'src')]);cc=cmd([java/'javac.exe','-J-Xmx180m','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dst,src]);body=src.read_text(encoding='utf8');m=re.search(r'^package ([\w.]+);',body,re.M);cls=(m[1]+'.'if m else '')+n;build=cmd([java/'java.exe','-Xmx190m','-Djava.security.manager','-Djava.security.policy=='+pol.as_uri(),'-Dline.separator=\n','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dfile.encoding=UTF-8','-cp',cp,cls,tp[tag],deps]) if cc.returncode==0 else None
 # cmd merges stdout and stderr, remove only exact JVM diagnostics preceding the generated SQL. Preserve complete raw output separately.
 log=out/(tag+'_'+n+'.generator.log');raw=cc.stdout+'\n'+(build.stdout if build else '');log.write_text(raw,encoding='utf8');res={'task_suite':n,'target':tag,'java_source':str(src.relative_to(repo)).replace('\\','/'),'java_sha':sha(src),'plugin_sha':sha(j),'generator_exit':build.returncode if build else None,'compile_exit':cc.returncode,'gen_log':log.name,'gen_log_sha':sha(log),'psql_exit':None,'actual_assertions':[],'raw_scope':'Test de proiect pe o bază PostgreSQL izolată template0; se generează SQL folosind sursa/Java și, unde proiectul o face, interogările din JAR. Un SQL generat din constante statice nu este o execuție a ERP.'}
 if cc.returncode or not build or build.returncode:return res
 lines=build.stdout.splitlines();start=next((i for i,l in enumerate(lines)if re.match(r'^\s*(?:\\(?:set|echo|pset)|--|CREATE|BEGIN|SET |WITH |SELECT |DROP |DO |INSERT |PREPARE |ALTER )',l,re.I)),None)
 if start is None:res['skip']='Niciun flux SQL identificabil';return res
 text='\n'.join(lines[start:])+'\n'
 if not re.search(r'\b(?:SELECT|CREATE|INSERT|DO)\b',text,re.I):res['skip']='Numai comentariu de emitere, nu execuție';return res
 sf=out/(tag+'_'+n+'.sql');sf.write_text(text,encoding='utf8');res['sql']=sf.name;res['sql_sha']=sha(sf)
 forbidden=re.search(r'\\!|\\i(?:r|\s)|\\connect|\\copy\s.*(?:FROM|TO)\s+[\'"]|\b(?:(?:DROP|ALTER|CREATE)\s+(?:USER\b|ROLE\b|SYSTEM\b|DATABASE\b)|COPY\b[^;]{0,450}\bPROGRAM\b|lo_import\s*\(|pg_read_file\s*\(|pg_write_file\s*\()',text,re.I)
 if forbidden:res['skip']='Generatorul include operație în afara fixture-ului independent: '+forbidden[0];return res
 db='a12r5sql_'+uuid.uuid4().hex[:13];assert re.fullmatch('a12r5sql_[a-f0-9]{13}',db)
 old="host=/tmp dbname=postgres user=postgres";mode=''
 if old in text:
  mode='transport dblink către aceeași bază UUID prin 127.0.0.1 în locul socketului /tmp; se păstrează toate aserțiunile.';text=text.replace(old,'host=127.0.0.1 port=56481 dbname='+db+' user=audit_owner passfile=D:/CodexWork/p01-local-pg16/pgpass.conf')
 # Other hardcoded db links must never escape our own database.
 if re.search(r"dblink_connect\s*\(",text,re.I) and not mode:res['skip']='dblink diferit de transportul verificat';return res
 cr=sql('postgres','CREATE DATABASE '+db+' OWNER audit_owner TEMPLATE template0;');assert not cr.returncode,cr.stderr
 try:
  so=sql(db,"SET statement_timeout='14s';\n"+text);v=so.stdout.decode('utf8',errors='replace');er=so.stderr.decode('utf8',errors='replace');lo=out/(tag+'_'+n+'.pglog');lo.write_text(v+'\n'+er,encoding='utf8');rr=[]
  for i,l in enumerate(v.splitlines(),1):
   matches=re.match(r'^\s*(OK|PASS|FAIL|NOK)\b[\s|:–-]*(.*)',l,re.I)
   if matches:rr.append({'line':i,'state':matches[1].upper(),'assertion_and_observed':matches[2][:520]})
  res.update(psql_exit=so.returncode,pglog=lo.name,pglog_sha=sha(lo),actual_assertions=rr,errors=[l[:200]for l in er.splitlines()if re.search('ERROR|FATAL',l,re.I)][:5],transport_change=mode or None,unique_temp_fixture=db)
 finally:
  chk=sql('postgres',"select count(*) from pg_database where datname='"+db+"' and pg_get_userbyid(datdba)='audit_owner';");assert chk.stdout.strip()==b'1'
  dl=sql('postgres','DROP DATABASE '+db+';');res['fixture_closed']=not dl.returncode
 return res
if __name__=='__main__':
 ss=sorted((plug/'test/sql').glob('*.java'));ss=[p for p in ss if p.stem not in ('TestT366Sql','TestT352Sql') and 'static void main(' in p.read_text(encoding='utf8',errors='replace')];ar=[]
 with cf.ThreadPoolExecutor(max_workers=4) as px:
  for i,v in enumerate(px.map(each,[(z,f) for f in ss for z in ('git','instalat')])):
   ar.append(v)
   if i%8==0:wr(out/'progress.json',{'cases':len(ar),'total':len(ss)*2,'postgres_cases':sum(w['psql_exit']is not None for w in ar)})
 wr(out/'executii.json',ar);print(len(ar),sum(v['psql_exit'] is not None for v in ar),sum(v['psql_exit']==0 for v in ar),sum(len(v['actual_assertions'])for v in ar))

