from pathlib import Path
import json,requests,hashlib,concurrent.futures
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie\BI_iDempiere');L=Path(__file__).parent
urls=[('S51','Metabase_AI_settings','https://www.metabase.com/docs/latest/ai/settings'),('S52','Metabase_MCP','https://www.metabase.com/docs/latest/ai/mcp'),('S53','Metabase_AI_providers','https://www.metabase.com/docs/latest/ai/providers'),('S54','Metabase_Metabot','https://www.metabase.com/docs/latest/ai/metabot'),('S55','Superset_MCP_6_1','https://raw.githubusercontent.com/apache/superset/6.1.0/docs/admin_docs/configuration/mcp-server.mdx')]
def fetch(v):
 id,name,url=v;r=requests.get(url,timeout=80);o=dict(id=id,title=id+'_'+name,url=url,access_date='2026-10-08',http_status=r.status_code)
 if r.ok:
  p=R/'06_Surse_oficiale'/('Metabase' if 'Metabase' in name else 'Superset')/(id+'_'+name+('.txt' if 'raw.' in url else '.html'));p.write_bytes(r.content);o.update(local=p.relative_to(R).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content),final_url=r.url)
 else:o['error']='HTTP '+str(r.status_code)
 return o
src=json.loads((R/'06_Surse_oficiale/surse.json').read_text(encoding='utf-8'));src=[s for s in src if s['id'] not in [u[0] for u in urls]]
src+=list(concurrent.futures.ThreadPoolExecutor(5).map(fetch,urls));(R/'06_Surse_oficiale/surse.json').write_text(json.dumps(src,ensure_ascii=False,indent=2),encoding='utf-8')
p=L/'report_content.txt';t=p.read_text(encoding='utf-8')
t=t.replace('Release-urile găsite prin API sunt salvate în releases.json;', 'Release-urile identificate pe paginile oficiale GitHub sunt salvate în versiuni_identificate.json; interogările API nereușite sunt păstrate separat în releases.json;')
t=t.replace('Matricea CSV permite filtrare pe categorie și produs.','Excelul include 64 de funcții, coloane pe produse și foi dedicate componentelor native și extensiilor. Bifele separă Da, Parțial, Nu și Neconfirmat.')
t=t.replace('Pentru candidații BI, echipa va alege ultimul release stabil compatibil', 'Versiunile identificate sunt Superset 6.1.0, Metabase OSS v0.64.1, Knowage v9.0.11, Redash v26.9.0 și Lightdash 2.423.2. Pentru candidații BI, echipa va alege release-ul stabil compatibil')
t=t.replace('Configuratorul AI local rămâne dezvoltare Eva; nu se punctează Metabot comercial ca avantaj gratuit. [S09]', 'Metabot, NLQ și MCP sunt disponibile în oferta open source curentă cu provider propriu; documentația include vLLM local. Acesta este un avantaj AI real, fără a presupune inferență fără cost de resurse. Profilul complet Eva, publicarea controlată și integrarea drepturilor ERP rămân dezvoltare. Metabase este principalul contracandidat pentru pilotul AI. [S51–S54]')
t=t.replace('Golul pentru Eva este adaptorul OSGi și serviciul de configurare AI.', 'Superset 6.1 documentează un server MCP inclus pentru queryuri, grafice și dashboarduri, cu client AI extern. MCP trebuie securizat separat; setarea de utilizator de dezvoltare nu se utilizează în producție. [S55]\n\nGolul pentru Eva este adaptorul OSGi și serviciul de configurare AI.')
t=t.replace('Metabase pierde la embedding self-service gratuit și câștigă la utilizare și existența pluginului.', 'Metabase pierde la embedding self-service gratuit și câștigă la utilizare, Metabot/MCP gratuit cu provider propriu și existența pluginului.')
t=t.replace('Surse principale: S01–S17, S35–S42, S50;', 'Surse principale: S01–S17, S35–S42, S50–S55;')
t=t.replace('depozzit','depozit')
p.write_text(t,encoding='utf-8')
print([(s['id'],s['http_status']) for s in src[-5:]])
