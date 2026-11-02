from pathlib import Path
import subprocess,json,datetime,hashlib
B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');E=B/'executie';D=Path(r'D:\CodexWork\eva-audit-p01-readonly-20261102')
q="""BEGIN READ ONLY;
SET LOCAL statement_timeout = '10s';
SELECT jsonb_build_object(
'forms',(SELECT coalesce(jsonb_agg(to_jsonb(a)),'[]') FROM (SELECT f.ad_form_id,f.name,f.classname,f.isactive,(SELECT count(*) FROM adempiere.ad_form_access fa WHERE fa.ad_form_id=f.ad_form_id AND fa.isactive='Y') active_role_links,(SELECT count(*) FROM adempiere.ad_menu m WHERE m.ad_form_id=f.ad_form_id AND m.isactive='Y') active_menu_links FROM adempiere.ad_form f ORDER BY f.ad_form_id)a),
'processes',(SELECT coalesce(jsonb_agg(to_jsonb(a)),'[]') FROM (SELECT p.ad_process_id,p.name,p.classname,p.isactive,(SELECT count(*) FROM adempiere.ad_process_access pa WHERE pa.ad_process_id=p.ad_process_id AND pa.isactive='Y') active_role_links FROM adempiere.ad_process p ORDER BY p.ad_process_id)a),
'tables',(SELECT jsonb_agg(to_jsonb(a)) FROM (SELECT t.tablename,t.isactive,t.isview FROM adempiere.ad_table t ORDER BY t.tablename)a),
'comparison_tables',(SELECT jsonb_agg(to_jsonb(a)) FROM (SELECT table_name,column_name,data_type FROM information_schema.columns WHERE table_schema='adempiere' AND lower(table_name) IN ('eva_sagaimportrow','eva_sagacong','eva_sagascinit','eva_sagascrulaj','eva_neconcordanta','fact_acct','c_bpartner','c_invoice','m_transaction') ORDER BY table_name,ordinal_position)a)
);
ROLLBACK;
"""
rs=subprocess.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151',"""docker exec -i eva-postgres-cesiro sh -c 'exec psql -X -qAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere'"""],input=q.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False);print('live rc',rs.returncode,rs.stderr.decode()[:250]);assert rs.returncode==0
data=json.loads(rs.stdout);m={'id':'EV-A12-DB-01','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'level':'LIVE_READ_ONLY','cabinet':'CESIRO','db':'idempiere','schema':'adempiere','statement':q,'counts':{k:len(v) for k,v in data.items()},'rows':data,'limit':'Prezența în dicționar, existența de legături meniu/rol și coloane nu certifică executarea formei/procesului sau identitatea buildului. Nu s-au citit valori de business, utilizatori ori numele rolurilor.'}
(E/'A12_DB_metadate_CESIRO.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8');print(m['counts']);print('T227', [x for x in data['forms'] if 'VerificareImport' in str(x)])
py=Path(r'C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
cmd=[str(py),'-I',str(D/'tools/teste/t227/test_bilant.py'),str(D/'tools/teste/t227/proba_fe.py')];t=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
(E/'A12_test_local_T227.json').write_text(json.dumps({'evidence_id':'EV-A12-T227-LOCAL-01','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'level':'LOCAL_ISOLATED_TEST','cabinet':'Niciun cabinet: Python local, fără DB sau browser.','command':cmd,'rc':t.returncode,'stdout':t.stdout.decode('utf-8','replace'),'stderr':t.stderr.decode('utf-8','replace'),'assertion':'Bilanțul probei trebuie să numere un pas întrerupt și să mascheze canarul. Proba verifică instrumentul de test, nu comparația contabilă de la ecran la rezultat.'},ensure_ascii=False,indent=2),encoding='utf8')
print('T227 harness rc',t.returncode, t.stdout.decode('utf8','replace')[-90:])

