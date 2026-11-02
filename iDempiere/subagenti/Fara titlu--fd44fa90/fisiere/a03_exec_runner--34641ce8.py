import pathlib as P, json, hashlib, subprocess as sp, re, os, datetime, zipfile, html, urllib.parse as U, concurrent.futures as cf
from lxml import etree
from urllib.request import urlopen,Request
base=P.Path('D:/CodexWork/eva-audit-p01-readonly-20261102'); sec=P.Path('D:/CodexWork/eva-audit-secondary-20261102')
audit=P.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01'); ex=audit/'executie'; o=ex/'A03'; o.mkdir(exist_ok=True); tmp=P.Path('D:/CodexWork/eva-a03-run-20261102'); tmp.mkdir(exist_ok=True)
plug=base/'idempiere/plugins/com.eva.ro.contab'; lib=P.Path('D:/CodexWork/eva-a01-java/lib'); java=P.Path('C:/Program Files/Java/jdk-21/bin'); plan=json.loads((audit/'A03_plan.json').read_text(encoding='utf-8-sig')); gate='df251d54425833e941ddf85ddf0e376ed7f2fb20312702919956a0b582f3b397'; sha=plan['repositories_and_shas'][0]['sha']
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def dump(name,x): (o/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def read(name): return json.loads((o/name).read_text(encoding='utf8'))
def dig(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(args,**kw):return sp.run([str(s) for s in args],capture_output=True,text=True,encoding='utf8',errors='replace',**kw)
names=['TestT153Interimar','TestTrezorerieValuta','TestT58Inchidere','TestT58Alarma','TestT194Salarii','TestT199Parametri','TestT256D394','TestEFacturaArhiva','TestT42Valute','TestT40L2Motor','TestT254EroriInchidere','TestT189Salarizare','TestT189Reges','TestT180D394','TestT154BilantCredite','TestT170Registru']
def java_tests():
    harness='''import java.math.*; import java.util.*; import java.time.*; import com.eva.ro.contab.date.BalantaService; import com.eva.ro.contab.fiscal.AmortizareFiscala; import com.eva.ro.contab.fiscal.MotorSalariiRO; import com.eva.ro.contab.process.AmortizareImobilizari; import java.sql.Timestamp; public class A03Fixture {
    static BigDecimal d(String x){return new BigDecimal(x);} static void check(String name,String want,String got){System.out.println(name+"|"+want+"|"+got+"|"+want.equals(got));}
    public static void main(String[] args)throws Exception{
    BalantaService.Rand row=new BalantaService.Rand(); row.simbol="4111.SYN";row.denumire="FX";row.si=d("100");row.rulajD=d("50");row.rulajC=d("30");check("balance_end","120",row.sfNet().toPlainString());
    BalantaService.Total t=new BalantaService.Total();t.ruD=d("10.004");t.ruC=d("10.000");check("currency_precision_3_difference_detected","false",Boolean.toString(t.egalitateRulaje()));
    check("asset_linear1200_12","100.00",AmortizareFiscala.amortizareLunaMetoda("LINIARA",d("1200"),12,3,LocalDate.of(2026,1,1)).toPlainString());check("asset_past_duration","0",AmortizareFiscala.amortizareLunaMetoda("LINIARA",d("1200"),12,12,LocalDate.of(2026,1,1)).toPlainString());
    var a=new AmortizareImobilizari.Activ();a.nume="SYN-A03";a.cost=d("1200");a.durata=12;a.pif=Timestamp.valueOf("2026-01-01 00:00:00");a.cumulat=d("0");a.descriere="";a.contAmortizare="2813";a.contCheltuiala="6811";var ev=AmortizareImobilizari.class.getDeclaredMethod("evalueaza",AmortizareImobilizari.Activ.class,YearMonth.class,Timestamp.class,boolean.class);ev.setAccessible(true);ev.invoke(null,a,YearMonth.of(2026,2),Timestamp.valueOf("2026-02-28 23:59:59"),false);check("asset_accounting_first_month","100.00",a.amortizareLuna.toPlainString());a.casat=true;a.dataCasare=Timestamp.valueOf("2026-02-20 00:00:00");a.motiv="";a.amortizareLuna=BigDecimal.ZERO;ev.invoke(null,a,YearMonth.of(2026,3),Timestamp.valueOf("2026-03-31 23:59:59"),false);check("disposed_subsequent_month","0",a.amortizareLuna.toPlainString());
    var sal=new MotorSalariiRO.Intrare();sal.brut=BigDecimal.ZERO;var result=MotorSalariiRO.calculeaza(sal);check("payroll_zero_net","0",result.net.stripTrailingZeros().toPlainString());
    }}'''
    fixture=tmp/'A03Fixture.java';fixture.write_text(harness,encoding='utf8');(o/'A03Fixture.java').write_text(harness,encoding='utf8')
    policy=tmp/'no-network.policy'; policy.write_text('grant { permission java.io.FilePermission "<<ALL FILES>>", "read"; permission java.io.FilePermission "'+tmp.as_posix()+'/-", "read,write,delete"; permission java.util.PropertyPermission "*","read,write"; permission java.lang.reflect.ReflectPermission "*"; permission java.lang.RuntimePermission "*"; permission java.util.logging.LoggingPermission "control"; permission java.security.SecurityPermission "getProperty.*"; permission java.io.SerializablePermission "*"; };',encoding='utf8')
    results=[]
    for target,jar in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
        dst=tmp/target;dst.mkdir(exist_ok=True);cp=';'.join(str(x) for x in [dst,sec/jar,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',lib/'*',plug/'src'])
        for nm in ['A03Fixture']+names:
            src=fixture if nm=='A03Fixture' else plug/'test'/(nm+'.java')
            if not src.exists():continue
            pkg=re.search(r'^package\s+([\w.]+);',src.read_text(encoding='utf8'),re.M);cl=(pkg[1]+'.' if pkg else '')+nm
            cc=cmd([java/'javac.exe','-J-Xmx256m','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dst,src],cwd=tmp,timeout=30)
            if cc.returncode:rr=cc
            else:
                try:rr=cmd([java/'java.exe','-Xmx320m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(tmp),'-Dfile.encoding=UTF-8','-cp',cp,cl],cwd=plug,timeout=26)
                except sp.TimeoutExpired as e:rr=type('Result',(),{'returncode':124,'stdout':(e.stdout or b'').decode(errors='replace') if isinstance(e.stdout,bytes) else (e.stdout or ''),'stderr':'timeout 26s'})()
            raw=(rr.stdout or '')+(rr.stderr or ''); log=o/(target+'_'+nm+'.txt');log.write_text(raw,encoding='utf8')
            results.append(dict(target=target,jar_sha256=dig(sec/jar),test=nm,fixture_path=str(src.relative_to(base)) if nm!='A03Fixture' else 'A03Fixture.java',fixture_sha256=dig(src),compiled=not cc.returncode,rc=rr.returncode,lines=raw.splitlines()[-4:],explicit_negative=[line for line in raw.splitlines() if '|false' in line and line.endswith('|false') or ('FAIL' in line and '0 FAIL' not in line) or 'Exception' in line][:10],log=log.name,log_sha256=dig(log),class_path=cp,network_policy='JVM SecurityManager avec FilePermission read, aucune SocketPermission. Aucun appel de service externe.'))
            dump('java_runs.json',{'utc':now(),'sha':sha,'runs':results,'policy':policy.read_text()})
def pg():
    # SQL product extracted from exact method, executed on synthetic CTE sources; no operational rows.
    src=(plug/'src/com/eva/ro/contab/date/BalantaService.java').read_text(encoding='utf8')
    sqlsrc=src.split('public static List<Rand> incarca(',1)[1].split('List<Rand> out',1)[0].split('String sql =',1)[1]
    chunks=re.findall(r'^\s*(?:\+\s*)?"([^"\n]*)"',sqlsrc,re.M);query=''.join(chunks)
    assert query.count('?')==7 and 'GROUP BY ev.value' in query
    for val in ["date '2026-10-01'","date '2026-10-01'","date '2026-10-31'","date '2026-10-01'","date '2026-10-31'",'12',"date '2026-10-31'"]:query=query.replace('?',val,1)
    shadow="""WITH fact_acct(ad_client_id,ad_org_id,c_acctschema_id,postingtype,dateacct,account_id,amtacctdr,amtacctcr) AS (VALUES (12,3,100,'A',date '2026-10-15',1,100::numeric,0::numeric),(12,3,200,'A',date '2026-10-15',1,20::numeric,0::numeric),(12,3,100,'B',date '2026-10-15',1,1000::numeric,0::numeric),(13,3,100,'A',date '2026-10-15',1,700::numeric,0::numeric)), c_elementvalue(c_elementvalue_id,value,name) AS (VALUES(1,'4111','SYN_CT')) """
    sql="BEGIN READ ONLY;\nSET LOCAL statement_timeout = '6500ms';\nSELECT 'transaction_read_only='||current_setting('transaction_read_only');\n"+shadow+query+';\n'+shadow+"SELECT c_acctschema_id,SUM(amtacctdr-amtacctcr) FROM fact_acct WHERE ad_client_id=12 AND postingtype='A' GROUP BY c_acctschema_id ORDER BY 1;\n"
    sql+="SELECT 'metadata',table_name,column_name,data_type FROM information_schema.columns WHERE table_schema='adempiere' AND table_name IN ('fact_acct','gl_journal','c_periodcontrol','a_asset','a_asset_disposed','a_depreciation_exp','amn_payroll','c_allocationline','c_currency','c_acctschema') AND column_name IN ('c_acctschema_id','c_currency_id','ad_client_id','ad_org_id','posted','docstatus','dateacct','amtacctdr','amtacctcr','stdprecision') ORDER BY table_name,column_name;\n"
    sql+="SELECT 'coa_schema_profile', count(*) AS clients_total, count(*) FILTER (WHERE n>1) AS clients_with_multiple_active_schemas FROM (SELECT count(*) n FROM adempiere.c_acctschema WHERE isactive='Y' GROUP BY ad_client_id) s;\n"
    sql+="SELECT 'precision_metadata', stdprecision, count(*) FROM adempiere.c_currency WHERE isactive='Y' GROUP BY stdprecision ORDER BY 2 DESC;\nROLLBACK;\n"
    (o/'metadata_and_fixture.sql').write_text(sql,encoding='utf8');res=cmd(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8','saga-server@192.168.100.151','docker exec -i eva-postgres-cesiro psql -X -qAt -F "|" -v ON_ERROR_STOP=1 -U adempiere -d idempiere'],input=sql,timeout=22)
    dump('readonly_database.json',{'utc':now(),'sha':sha,'command':'ssh -o BatchMode=yes saga-server@192.168.100.151 docker exec -i eva-postgres-cesiro psql -X -qAt -F | -v ON_ERROR_STOP=1 -U adempiere -d idempiere','rc':res.returncode,'query':'metadata_and_fixture.sql','sql_sha256':dig(o/'metadata_and_fixture.sql'),'results':res.stdout.splitlines(),'stderr':res.stderr,'fixture_expectation':'Sold separat pentru scheme 100/200: 100 și 20. Nici suma 700 alt client, nici bugetul 1000 nu intră.','restriction':'Documente reale și date personale necitite. SELECT-uri catalog + profiluri agregate configurare. Reproducerea SQL a produsului folosește exclusiv VALUES cu aliasuri care maschează tabelele.'})
def official():
    found=[]
    for form in ['300','112','406','394','390','100','101','205','700','710']:
        url=f'https://static.anaf.ro/static/10/Anaf/Declaratii_R/{form}.html';r={'form':form,'url':url,'retrieved_at':now()}
        try:
            with urlopen(Request(url,headers={'User-Agent':'EVA audit local read-only/1.0'}),timeout=12) as f:raw=f.read()
            (o/f'ANAF_D{form}.html').write_bytes(raw);r['page_sha256']=hashlib.sha256(raw).hexdigest();from lxml import html as H;doc=H.fromstring(raw)
            items=[(a.get('href'),re.sub(r'\s+',' ',' '.join(a.itertext())).strip()) for a in doc.xpath('//a[@href]')];r['links_metadata']=[{'url':U.urljoin(url,u),'label':txt} for u,txt in items if 'xsd' in u.lower()][:2];r['description_excerpt']=' '.join(' '.join(doc.itertext()).split())[:650]
            if form in ['300','112','406'] and r['links_metadata']:
                link=r['links_metadata'][0]['url']
                if U.urlsplit(link).hostname not in {'static.anaf.ro','www.anaf.ro'}:raise ValueError('host schema extern')
                with urlopen(Request(link,headers={'User-Agent':'Mozilla/5.0'}),timeout=12) as f:xs=f.read()
                schema_file=o/f'ANAF_D{form}.xsd';schema_file.write_bytes(xs);r['xsd_sha256']=dig(schema_file);schema=etree.XMLSchema(etree.fromstring(xs,base_url=schema_file.as_uri()));r['xsd_compiled']=True
                fx={'300':'D300_2025-04_sintetic.xml','406':'D406_sintetic.xml'}.get(form);p=plug/'test/fixtures/t16'/fx if fx else None
                if p and p.exists():
                    parser=etree.XMLParser(no_network=True,resolve_entities=False);v=schema.validate(etree.parse(str(p),parser));r['fixture_check']={'file':str(p.relative_to(base)),'hash':dig(p),'valid_for_downloaded_schema':v,'errors':[x.message[:430] for x in list(schema.error_log)[:4]],'limit':'Fixture historique du repository. La version de la période doit être rapprochée avant tout constat produit.'}
        except Exception as e:r['diagnostic']=str(e)[:800]
        found.append(r);dump('official_sources.json',{'sources':found,'limit':'L’index officiel documente les versions disponibles pour la période. Une validation XSD seule ne couvre ni DUK, ni validité métier/fiscale, ni soumission.'})
if __name__=='__main__':
    import sys
    {'java':java_tests,'pg':pg,'official':official}[sys.argv[1]]()
