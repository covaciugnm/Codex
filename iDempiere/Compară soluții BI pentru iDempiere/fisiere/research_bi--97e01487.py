import requests, pathlib, json, hashlib, concurrent.futures, zipfile, io, re, datetime
ROOT=pathlib.Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie\BI_iDempiere')
ROOT.mkdir(parents=True,exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='BI-documentation-research/1.0'
pages={
'S01_Superset_overview':'https://superset.apache.org/',
'S02_Superset_security':'https://superset.apache.org/docs/6.0.0/security/',
'S03_Superset_reports':'https://superset.apache.org/docs/6.0.0/configuration/alerts-reports/',
'S04_Superset_embed':'https://raw.githubusercontent.com/apache/superset/master/superset-embedded-sdk/README.md',
'S05_Superset_api':'https://superset.apache.org/docs/6.0.0/api/',
'S06_Metabase_embedding':'https://www.metabase.com/docs/latest/embedding/introduction',
'S07_Metabase_permissions':'https://www.metabase.com/docs/latest/permissions/row-and-column-security',
'S08_Metabase_licence':'https://www.metabase.com/license/',
'S09_Metabase_features':'https://www.metabase.com/docs/latest/paid-features',
'S10_Knowage_editions':'https://www.knowage-suite.com/editions/',
'S11_Knowage_docs':'https://knowage-suite.readthedocs.io/en/latest/',
'S12_Redash_permissions':'https://redash.io/help/user-guide/users/permissions-groups/',
'S13_Redash_embedding':'https://redash.io/help/user-guide/dashboards/sharing-dashboards/',
'S14_Redash_alerts':'https://redash.io/help/user-guide/alerts/',
'S15_Lightdash_license':'https://raw.githubusercontent.com/lightdash/lightdash/main/LICENSE',
'S16_Lightdash_enterprise':'https://docs.lightdash.com/self-host/enterprise-on-prem',
'S17_Lightdash_docs_index':'https://docs.lightdash.com/llms.txt',
'S18_iDempiere_manual':'https://wiki.idempiere.org/en/Manual',
'S19_iDempiere_plugins':'https://wiki.idempiere.org/en/Category:Available_Plugins',
'S20_BX_Metabase':'https://wiki.idempiere.org/en/Plugin:_BX_Service_Metabase',
'S21_Chart_Maker':'https://wiki.idempiere.org/en/Plugin:_Chart_Maker',
'S22_JasperReports':'https://wiki.idempiere.org/en/Plugin:_JasperReports',
'S23_JasperFreiBier':'https://wiki.idempiere.org/en/JasperReportsFreiBier',
'S24_Kanban':'https://wiki.idempiere.org/en/Plugin:_Kanban_Dashboard',
'S25_CashForecast':'https://wiki.idempiere.org/en/Plugin:_CashForecasting',
'S26_Gadget':'https://wiki.idempiere.org/en/Plugin:_Information_Gadget',
'S27_Report_View':'https://wiki.idempiere.org/en/Report_View',
'S28_Jasper_deployment':'https://docs.idempiere.org/docs/new-features/v9/jasper-report-deployment-refactoring-and-improvement',
'S29_iDempiere_Metabase_pdf':'https://wiki.idempiere.org/w-en/images/6/67/Metabase.pdf',
'S30_CashForecast_pdf':'https://raw.githubusercontent.com/pshepetko/org.idempiere.cashforecasting/master/downloads/CashForecasting_v1.0.1a.pdf',
'S31_Ollama_license':'https://raw.githubusercontent.com/ollama/ollama/main/LICENSE',
'S32_vLLM_docs':'https://docs.vllm.ai/en/latest/',
'S33_Qwen_model':'https://huggingface.co/Qwen/Qwen3-8B/raw/main/README.md',
'S34_Postgres_RLS':'https://www.postgresql.org/docs/current/ddl-rowsecurity.html',
'S35_Superset_license':'https://raw.githubusercontent.com/apache/superset/master/LICENSE.txt',
'S36_Redash_license':'https://raw.githubusercontent.com/getredash/redash/master/LICENSE',
'S37_Knowage_license':'https://raw.githubusercontent.com/KnowageLabs/Knowage-Server/master/LICENSE',
}
def page(kv):
 k,u=kv; d=ROOT/'06_Surse_oficiale'/k.split('_',1)[1].split('_')[0];d.mkdir(parents=True,exist_ok=True)
 row={'id':k.split('_')[0],'title':k,'url':u,'access_date':'2026-10-08'}
 try:
  r=S.get(u,timeout=55);row['http_status']=r.status_code;r.raise_for_status()
  ext='.pdf' if r.content[:4]==b'%PDF' else '.html' if 'html' in r.headers.get('content-type','') else '.txt'
  p=d/(k+ext);p.write_bytes(r.content);row.update(local=str(p.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content),final_url=r.url)
 except Exception as e:row['error']=str(e)[:180]
 return row
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(page,pages.items()))
 (ROOT/'06_Surse_oficiale'/'surse.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps([{'id':x['id'],'status':x.get('http_status'),'bytes':x.get('bytes')} for x in rows]))
