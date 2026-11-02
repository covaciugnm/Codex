from pathlib import Path
import json,re,datetime,hashlib,subprocess
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');F=Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102\idempiere\plugins\com.eva.ro.contab\src\com\eva\ro\contab\form\VerificareImportSaga.java');s=F.read_text(encoding='utf8')
def extract(code):
 if code.startswith('SQL_'):m=re.search(r'static final String '+code+r'\s*=\s*(.*?);',s,re.S)
 else:m=re.search(r'static String '+code+r'\(\)\s*\{\s*return (.*?);',s,re.S)
 assert m;return ''.join(json.loads(i) for i in re.findall(r'"(?:\\.|[^"\\])*"',m[1])),s[:m.start()].count('\n')+1
def bind(s,args):
 for a in args:s=s.replace('?',a,1)
 assert '?' not in s;return s
fx1="WITH EVA_SagaConG(AD_Client_ID,Cont,Analitic,Fin_D,Fin_C) AS (VALUES (101,'411',' A ',100::numeric,0),(101,'411','B',40::numeric,0),(101,'411','  ',77::numeric,0),(202,'411','C',999::numeric,0))"
fx2="WITH C_Payment(AD_Client_ID,DocStatus,Posted,DateAcct) AS (VALUES(101,'CO','N',DATE '2026-01-10'),(101,'CO','Y',DATE '2026-01-10'),(202,'CO','N',DATE '2026-01-10'),(101,'CO','N',DATE '2026-01-11')), C_Invoice(AD_Client_ID,DocStatus,Posted,DateAcct) AS (VALUES(101,'CL','N',DATE '2026-01-10'),(101,'DR','N',DATE '2026-01-10'))"
fx3="WITH M_Transaction(AD_Client_ID,M_Locator_ID,M_Product_ID,MovementDate,MovementQty) AS (VALUES(101,11,21,DATE '2026-01-10',5),(101,11,21,DATE '2026-01-11',31),(202,11,21,DATE '2026-01-10',900)), M_Locator(M_Locator_ID,M_Warehouse_ID) AS (VALUES(11,31)), M_Warehouse(M_Warehouse_ID,Value,Name) AS (VALUES(31,'G1','G1')), M_Product(M_Product_ID,Value) AS (VALUES(21,'P1')), M_Cost(AD_Client_ID,M_Product_ID,CurrentCostPrice) AS (VALUES(101,21,3),(101,21,5),(202,21,999))"
tests=[('SAGA_PARTENERI','sqlSagaConG',fx1,['101'],[['411','A','100','0'],['411','B','40','0']]),('DOCUMENTE_NEPOSTATE','SQL_NEPOSTATE',fx2,['101',"DATE '2026-01-11'",'101',"DATE '2026-01-11'"],[['1','1']]),('STOC_COST_MULTIPLU','SQL_EVA_STOC',fx3,['101','101',"DATE '2026-01-11'","'Standard'","'IMOBILIZARI-SAGA'","'Standard'","'Standard'"],[['G1','P1','5','5','31','21']])]
out=[]
for name,sym,fx,args,expected in tests:
 sql,ln=extract(sym);q=fx+'\n'+bind(sql,args)+';';cmd='BEGIN READ ONLY;\nSET LOCAL statement_timeout=\'5s\';\n'+q+'\nROLLBACK;';r=subprocess.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151',"""docker exec -i eva-postgres-cesiro sh -c 'exec psql -X -qAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere'"""],input=cmd.encode(),capture_output=True)
 obs=[l.split('|') for l in r.stdout.decode().splitlines()];out.append({'id':name,'source_symbol':sym,'line':ln,'sql_literal':sql,'typed_parameters':args,'synthetic_CTE':fx,'expected':expected,'observed':obs,'rc':r.returncode,'stderr':r.stderr.decode(),'result':'PASS_DOVEDIT' if r.returncode==0 and sorted(obs)==sorted(expected) else 'FAIL_DOVEDIT'})
data={'id':'EV-A12-T227-CTE','sha':'6df998aee0e514d30856c461962afe99ebd0d113','captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':str(F),'source_sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'method':'SQL Java extras din sursa fixată, legarea parametrilor în ordinea declarată, CTE sintetice umbrează exclusiv tabelele referite, BEGIN READ ONLY, nicio scriere și niciun rând real folosit. Motor PostgreSQL CESIRO, dar este o probă izolată a query-ului pe date sintetice și nu o probă E2E în ERP.','tests':out}
(B/'executie/A12_T227_SQL_sintetic.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print([(x['id'],x['result']) for x in out])

