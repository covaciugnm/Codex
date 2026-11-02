from a03_exec_runner import *
from lxml import html as H
import io
def retry_java():
  old=read('java_runs.json');pol=tmp/'no-net-2.policy'; pol.write_text((tmp/'no-network.policy').read_text().replace('permission java.util.logging.LoggingPermission','permission java.sql.SQLPermission "setLog"; permission java.util.logging.LoggingPermission'),encoding='utf8')
  out=[]
  for target,jar in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
    dst=tmp/target; cp=';'.join(str(x) for x in [dst,sec/jar,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',lib/'*',plug/'src'])
    for h in ['TestT16Declaratii','TestT159LotC','TestT159LotA','TestT29Perioade','TestT189Salarizare','TestT194Salarii']:
      q=cmd([java/'javac.exe','-proc:none','-encoding','UTF-8','-cp',cp,'-sourcepath','','-d',dst,plug/'test'/(h+'.java')],cwd=tmp,timeout=25)
    for row in [r for r in old['runs'] if r['target']==target and r['rc']]:
      nm=row['test']; rr=cmd([java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+pol.as_uri(),'-Djava.io.tmpdir='+str(tmp),'-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-Dfile.encoding=UTF-8','-cp',cp,nm],cwd=plug,timeout=35)
      txt=rr.stdout+rr.stderr; log=o/(target+'_retry2_'+nm+'.txt');log.write_text(txt,encoding='utf8');out.append(dict(test=nm,target=target,rc=rr.returncode,log=log.name,log_sha256=dig(log),first_attempt=row['log'],lines=txt.splitlines()[-3:],fails=[l for l in txt.splitlines() if re.match(r'^\s*FAIL\b',l)][:7],errors=[l for l in txt.splitlines() if 'Caused by' in l or 'Exception in thread' in l][:3]));dump('java_retry2.json',{'utc':now(),'reason':'JDBC native logger needs SQLPermission setLog. TestT159/TestT16 helpers were missing from harness. No network permissions were granted. Previous results retained.','runs':out,'policy':pol.read_text()})
def xsd():
  entries={}
  for code in ['300','406','112','394','390','100','101','205','700','710']:
    f=o/f'ANAF_D{code}.html';doc=H.fromstring(f.read_bytes());anchors=doc.xpath('//tr[td[1][contains(normalize-space(string(.)),"'+code+'")]][1]//a[@href]');anchors=[a for a in anchors if re.search('schem',a.text_content(),re.I) or re.search(r'\.(?:xsd|xml)$',a.get('href'),re.I)];opts=[U.urljoin(f'https://static.anaf.ro/static/10/Anaf/Declaratii_R/{code}.html',a.get('href')) for a in anchors];r={'index_url':f'https://static.anaf.ro/static/10/Anaf/Declaratii_R/{code}.html','index_sha256':dig(f),'official_schema_href':opts[:2]};entries[code]=r
    if not opts:continue
    try:
      u=opts[0];raw=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=14).read();dest=o/f'D{code}_index_first_schema.xsd';dest.write_bytes(raw);r.update(xsd_sha256=dig(dest),xsd_url=u,locator=dest.name);schema=etree.XMLSchema(etree.fromstring(raw,base_url=dest.as_uri()));r['compiled']=True
      if code=='300':
        for name in ['d300_cunoscut_bun.xml','d300_stricat.xml']:
          pp=base/'idempiere/anaf-schemas/test'/name;dom=etree.parse(str(pp));ok=schema.validate(dom);r.setdefault('cases',[]).append({'fixture':str(pp.relative_to(base)),'sha256':dig(pp),'valid':ok,'first_error':str(schema.error_log.last_error.message)[:300] if schema.error_log.last_error else None})
    except Exception as e:r['diagnostic']=str(e)[:300]
  url='https://static.anaf.ro/static/10/Anaf/AsistentaContribuabili_r/Cotele_de_TVA_09.2025.pdf';raw=urlopen(url,timeout=15).read();pdf=o/'ANAF_cote_TVA_2025_09.pdf';pdf.write_bytes(raw);import fitz;txt='\n'.join(p.get_text() for p in fitz.open(pdf));(o/'ANAF_cote_TVA_text.txt').write_text(txt,encoding='utf8');entries['TVA']={'url':url,'sha256':dig(pdf),'actual_text_excerpt':' '.join(txt.split())[:420],'application':'operațiunea internă românească supusă cotei standard la 2025-09-15, fără regim derogatoriu. Document consultat ca explicație oficială pentru acest caz datat.'};dump('schemas_rechecked.json',{'utc':now(),'purpose':'Rândul oficial al versiunii curente din tabelul ANAF. Prima încercare D300 selectase o extensie veche .xsd, în timp ce versiunea v12 este livrată cu extensia .xml. Păstrăm ambele rezultate cu domeniul lor distinct.','items':entries})
def more_db():
  src=(plug/'src/com/eva/ro/contab/fiscal/NotaInchidere.java').read_text(encoding='utf8');method=src.split('private static Map<String, BigDecimal> net(',1)[1].split('Map<String, BigDecimal> net = ',1)[0]
  assert 'GROUP BY ev.value HAVING ABS(SUM(f.amtacctdr - f.amtacctcr)) >= 0.005' in method and 'f.c_acctschema_id' not in method
  query="""SELECT ev.value, SUM(f.amtacctdr-f.amtacctcr) FROM fact_acct f JOIN c_elementvalue ev ON ev.c_elementvalue_id=f.account_id WHERE f.ad_client_id=12 AND f.postingtype='A' AND (ev.value LIKE '7%') AND f.dateacct BETWEEN date '2026-10-01' AND date '2026-10-31' GROUP BY ev.value HAVING ABS(SUM(f.amtacctdr-f.amtacctcr)) >= 0.005 ORDER BY ev.value"""
  rows="""WITH fact_acct(ad_client_id,ad_org_id,c_acctschema_id,postingtype,dateacct,account_id,amtacctdr,amtacctcr) AS (VALUES(12,3,100,'A',date '2026-10-11',1,0::numeric,100::numeric),(12,3,200,'A',date '2026-10-11',1,0::numeric,20::numeric)),c_elementvalue(c_elementvalue_id,value) AS (VALUES(1,'707.SYN')) """
  sql='BEGIN READ ONLY;\nSET LOCAL statement_timeout=\'5s\';\n'+rows+query+';\n'+rows+'SELECT c_acctschema_id, SUM(amtacctdr-amtacctcr) FROM fact_acct GROUP BY c_acctschema_id ORDER BY 1;\nROLLBACK;';p=o/'closing_synthetic.sql';p.write_text(sql,encoding='utf8');res=cmd(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','docker exec -i eva-postgres-cesiro psql -X -qAt -F "|" -v ON_ERROR_STOP=1 -U adempiere -d idempiere'],input=sql,timeout=15);dump('closing_synthetic.json',{'utc':now(),'sha':sha,'sql_file':p.name,'rc':res.returncode,'results':res.stdout.splitlines(),'stderr':res.stderr,'source_method':'fiscal/NotaInchidere.java net: 221–249, appel InchidereVenituri 174 et InchidereTVA 152, PO journal 361–399','scope':'SQL auxiliaire réellement exécuté après remplacement des paramètres/LIKE. La note réelle n’a pas été créée.'})
if __name__=='__main__':
  import sys
  {'java':retry_java,'xsd':xsd,'sql':more_db}[sys.argv[1]]()
