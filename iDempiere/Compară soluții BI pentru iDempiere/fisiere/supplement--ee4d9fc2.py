from research_bi import ROOT,S,page
import json,concurrent.futures,pathlib
extra={
'S38_Superset_security_current':'https://superset.apache.org/admin-docs/security/',
'S39_Superset_reports_current':'https://superset.apache.org/admin-docs/configuration/alerts-reports/',
'S40_Superset_API_current':'https://superset.apache.org/developer-docs/api/',
'S41_Lightdash_AI':'https://docs.lightdash.com/self-host/enterprise-features/ai-agents',
'S42_Lightdash_MCP':'https://docs.lightdash.com/self-host/enterprise-features/mcp',
'S43_AMERPSOFT_financial':'https://raw.githubusercontent.com/luisamesty/Amerpsoft-iDempiere-community/master/org.amerpsoft.com.idempiere.financial/README.md',
'S44_EGS_charts':'https://www.idempiereperu.org/2025/06/17/idempiere-charts-panels/',
'S45_SmallBI':'https://bitbucket.org/idplugin/th.motive.form.bi',
'S46_Knowage_docs_current':'https://knowage.readthedocs.io/en/latest/',
'S47_Knowage_sdk':'https://knowage.readthedocs.io/en/latest/user/JS/README/',
'S48_Knowage_pdf':'https://knowage-suite.readthedocs.io/_/downloads/en/latest/pdf/',
'S49_Kanban_source':'https://raw.githubusercontent.com/diego-ruiz/kanban-board/master/README.md',
'S50_Lightdash_embedding':'https://raw.githubusercontent.com/lightdash/mintlify-docs/main/snippets/embedding-availability.mdx',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(page,extra.items()))
f=ROOT/'06_Surse_oficiale/surse.json';existing=json.loads(f.read_text(encoding='utf-8'));existing=[r for r in existing if r['id'] not in [a['id'] for a in rows]];f.write_text(json.dumps(existing+rows,ensure_ascii=False,indent=2),encoding='utf-8')
rels=[]
for repo in ['apache/superset','metabase/metabase','getredash/redash','KnowageLabs/Knowage-Server','lightdash/lightdash']:
 r=S.get('https://api.github.com/repos/'+repo+'/releases/latest',timeout=30);j=r.json();rels.append({'repo':repo,'status':r.status_code,'tag':j.get('tag_name'),'published_at':j.get('published_at'),'url':j.get('html_url'),'prerelease':j.get('prerelease')})
(ROOT/'06_Surse_oficiale/releases.json').write_text(json.dumps(rels,indent=2),encoding='utf-8');print(rels)
print([(r['id'],r.get('http_status')) for r in rows])
