const cp=require('child_process'),fs=require('fs'),p=require('path'),crypto=require('crypto');
const bin='D:/CodexWork/p01-local-pg16/pgsql/bin/psql.exe',argv=['-X','-h','127.0.0.1','-p','56481','-U','audit_owner','-d','a05_r2','-q','-A','-t','-v','ON_ERROR_STOP=1'];const env={...process.env,PGPASSFILE:'D:/CodexWork/p01-local-pg16/pgpass.conf'};
function open(tag){
 const child=cp.spawn(bin,argv,{env:{...env,PGAPPNAME:tag},windowsHide:true});let buf='',stderr='';let awaiting=null;
 child.stdout.on('data',x=>{buf+=x.toString();if(awaiting&&buf.includes(awaiting.end)) {let text=buf.slice(0,buf.indexOf(awaiting.end)).trim();buf=buf.slice(buf.indexOf(awaiting.end)+awaiting.end.length);const done=awaiting.resolve;awaiting=null;done(text);}});
 child.stderr.on('data',x=>{stderr+=x.toString()});child.on('close',code=>{if(awaiting)awaiting.reject(Error('SQL '+code+' '+stderr.slice(-400)));});
 return {send(sql){const end='END_'+crypto.randomUUID();return new Promise((resolve,reject)=>{awaiting={end,resolve,reject};child.stdin.write(sql+'\nSELECT '+ "'"+end+"';\n");});},end(){child.stdin.end('\\q\n')}}
}
(async()=>{const a=open('A05-T1-activation'),b=open('A05-T2-adjust'),observer=open('A05-read-observer');
const out={category:'RECONSTRUCTION_SQL_MODEL',description:'Intercalare controlată a două tranzacții în PostgreSQL local. Tabelele sunt numai ale modelului sintetic, nu au fost apelate PO sau DocAction. R1 furnizează proba separată a fluxului real. Commiturile sunt observate printr-o a treia conexiune.',server:'127.0.0.1:56481/a05_r2',native_source_sha:'6df998aee0e514d30856c461962afe99ebd0d113',history:[]};
const e=async(label,session,sql)=>{const t=new Date().toISOString(),observed=await session.send(sql);out.history.push({label,utc:t,sql,observed});return observed};
try{
await e('create isolated test tables',observer,'CREATE SCHEMA IF NOT EXISTS a05_model; CREATE TABLE IF NOT EXISTS a05_model.g1(product int primary key,qty int); CREATE TABLE IF NOT EXISTS a05_model.pair(g1 int primary key,g2 int); CREATE TABLE IF NOT EXISTS a05_model.g2(product int primary key,qty int); CREATE TABLE IF NOT EXISTS a05_model.journal(event text primary key,delta int);');
for(const mode of ['interval-snapshot-activare','activation-committed-before-adjustment','adjustment-committed-before-snapshot']){
 await e(mode+'/reset synthetic model',observer,'TRUNCATE a05_model.g1,a05_model.pair,a05_model.g2,a05_model.journal; INSERT INTO a05_model.g1 VALUES (123,20);');
 const stock='SELECT (SELECT qty FROM a05_model.g1),(SELECT qty FROM a05_model.g2),(SELECT count(*) FROM a05_model.pair),(SELECT count(*) FROM a05_model.journal),txid_current_snapshot();';
 const begin=async()=>{await e(mode+'/activate begin and materialize cut',a,'BEGIN; CREATE TEMP TABLE base AS SELECT product,qty FROM a05_model.g1; SELECT * FROM base;')};
 const finish=async()=>{await e(mode+'/activate install and commit',a,'INSERT INTO a05_model.pair VALUES(1,2); INSERT INTO a05_model.g2 SELECT * FROM base; DROP TABLE base; COMMIT;')};
 const adjust=async()=>{await e(mode+'/stock document adjustment and mirror guard in one transaction',b,"BEGIN; UPDATE a05_model.g1 SET qty=qty-2 WHERE product=123; INSERT INTO a05_model.journal SELECT 'inv42',-2 FROM a05_model.pair WHERE g1=1 ON CONFLICT DO NOTHING; UPDATE a05_model.g2 SET qty=qty-2 WHERE EXISTS(SELECT 1 FROM a05_model.journal WHERE event='inv42'); COMMIT;")};
 if(mode==='interval-snapshot-activare'){await begin();await adjust();await e(mode+'/independent visibility after G1 commit',observer,stock);await finish();}
 if(mode==='activation-committed-before-adjustment'){await begin();await finish();await e(mode+'/independent visibility before G1',observer,stock);await adjust();}
 if(mode==='adjustment-committed-before-snapshot'){await adjust();await e(mode+'/independent visibility before snapshot',observer,stock);await begin();await finish();}
 await e(mode+'/observed durable result',observer,stock);
}
}finally{a.end();b.end();observer.end();}
const f='Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R2_zone/A05/F10_local_db_protocol.json';fs.writeFileSync(f,JSON.stringify(out,null,2));console.log(out.history.filter(x=>x.label.includes('durable')).map(x=>x.observed));})().catch(e=>{console.error(e);process.exitCode=1})

