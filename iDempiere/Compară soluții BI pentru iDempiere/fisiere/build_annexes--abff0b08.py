from pathlib import Path
import json,csv,re,hashlib,html,shutil
def validate_profile(obj,schema):
 assert set(obj)==set(schema['required'])
 assert obj['schema_version']=='1.0' and type(obj['profile_version']) is int and obj['profile_version']>=1
 assert type(obj['synthetic']) is bool and obj['company_key'] and obj['owner']
 assert obj['industry'] in ['manufacturing','distribution','services'] and obj['locale']=='ro-RO'
 assert re.fullmatch('[A-Z]{3}',obj['currency']) and 1<=obj['fiscal_year_start_month']<=12
 assert len(obj['modules'])==len(set(obj['modules'])) and all(isinstance(v,str) for v in obj['modules'])
 assert obj['objectives'] and all(isinstance(v,str) for v in obj['objectives'])
 assert all(set(v)=={'id','status'} and isinstance(v['id'],str) and v['status'] in ['available','missing','unverified'] for v in obj['data_sources'])
 assert all(isinstance(v,str) for v in obj['field_provenance'].values())
R=Path(r'\\192.168.100.169\Comun\00.Roboti\iDempiere\Documentatie\BI_iDempiere');L=Path(__file__).parent
def write(path,text):p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def js(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2))
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Profil BI companie — contract propus','type':'object','additionalProperties':False,'required':['schema_version','profile_version','synthetic','company_key','industry','locale','currency','fiscal_year_start_month','modules','objectives','data_sources','owner','field_provenance'],'properties':{
'schema_version':{'const':'1.0'},'profile_version':{'type':'integer','minimum':1},'synthetic':{'type':'boolean'},'company_key':{'type':'string','minLength':1},'industry':{'enum':['manufacturing','distribution','services']},'locale':{'const':'ro-RO'},'currency':{'type':'string','pattern':'^[A-Z]{3}$'},'fiscal_year_start_month':{'type':'integer','minimum':1,'maximum':12},'modules':{'type':'array','uniqueItems':True,'items':{'type':'string'}},'objectives':{'type':'array','minItems':1,'items':{'type':'string'}},'data_sources':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['id','status'],'properties':{'id':{'type':'string'},'status':{'enum':['available','missing','unverified']}}}},'owner':{'type':'string'},'field_provenance':{'type':'object','additionalProperties':{'type':'string'}}}}
js('04_Arhitectura_AI/company_profile.schema.json',schema)
for industry,mods,objectives,sources in [('manufacturing',['GL','Sales','Inventory','Production'],['net_revenue','unit_cost','scrap_rate','energy_per_unit'],[('fact_gl','available'),('fact_production','unverified'),('energy_meter','missing')]),('distribution',['GL','Sales','Purchasing','Inventory'],['gross_margin','inventory_turnover','overdue_receivables'],[('fact_gl','available'),('fact_invoice_line','available'),('cost','unverified')]),('services',['GL','Projects','Sales'],['project_margin','billable_hours','overdue_receivables'],[('fact_gl','available'),('timesheets','unverified')])]:
 obj=dict(schema_version='1.0',profile_version=1,synthetic=True,company_key='demo_'+industry,industry=industry,locale='ro-RO',currency='RON',fiscal_year_start_month=1,modules=mods,objectives=objectives,data_sources=[dict(id=a,status=b) for a,b in sources],owner='owner_demo',field_provenance={'industry':'exemplu sintetic','modules':'ipoteză de pilot, neconfirmată în Eva','currency':'exemplu sintetic'})
 validate_profile(obj,schema);js('04_Arhitectura_AI/profile_'+industry+'.json',obj)
plan={'schema_version':'1.0','status':'proposal_not_deployed','synthetic':True,'profile_version':1,'company_key':'demo_distribution','security_context_source':'server_session_only','dashboard_id':'distribution_overview','audience':'management','widgets':[{'metric_id':'net_revenue','dataset_id':'fact_gl','chart_type':'time_series','filter_refs':['date_range'],'formula_ref':'approved_catalog/net_revenue/v1'},{'metric_id':'overdue_receivables','dataset_id':'fact_open_item_snapshot','chart_type':'table','filter_refs':['as_of_date'],'formula_ref':'approved_catalog/overdue_receivables/v1'}],'blocked_metrics':[{'metric_id':'gross_margin','reason':'cost_source_unverified'}],'publish_requires':['schema_validation','catalog_reference_validation','authorization','reconciliation','owner_approval'],'rollback_ref':'previous_approved_configuration'}
js('04_Arhitectura_AI/dashboard_plan.example.json',plan)
write('04_Arhitectura_AI/README.md','''# Configurator AI bazat pe profilul companiei

Contracte de proiect, fără plugin implementat sau instalat. Profilele sunt sintetice și nu reprezintă date confirmate despre CESIRO.

1. Validați profilul cu JSON Schema. Cele trei exemple au fost validate structural.
2. Rezolvați identitatea, cabinetul, firma și organizațiile din sesiunea server Eva. Acestea nu se preiau din textul modelului.
3. Selectați numai metrici și dataseturi din catalogul aprobat. `formula_ref` este o referință logică propusă, nu o formulă implementată.
4. Generați un plan JSON și validați-l semantic. Lipsa costului sau a datelor OEE trebuie să blocheze indicatorul afectat.
5. Previzualizați diferențele și publicați prin API numai după verificări și aprobarea definițiilor. Păstrați versiunea și rollbackul.

Superset 6.1 are MCP documentat; Metabase OSS are Metabot/MCP și provider propriu, inclusiv vLLM în manualul curent. Aceste mecanisme reduc efortul instrumentelor, fără să implementeze automat modelul de autorizare și profilul Eva.

```mermaid
flowchart LR
  ERP[iDempiere și Eva] --> MART[Mart PostgreSQL validat]
  MART --> BI[Superset]
  SESSION[Sesiune ERP autorizată] --> ADAPTER[Adaptor OSGi]
  ADAPTER --> BI
  PROFILE[Profil companie] --> AI[Model local]
  CATALOG[Catalog KPI aprobat] --> AI
  AI --> PLAN[Plan JSON]
  PLAN --> VALIDATOR[Validator independent]
  VALIDATOR --> REVIEW[Previzualizare și aprobare]
  REVIEW --> API[API BI și registru versiuni]
  API --> BI
```

Interfețe propuse: `POST /bi/proposals` primește profil/version și returnează plan; `POST /bi/proposals/{id}/validate` returnează erori; `POST /bi/proposals/{id}/publish` cere rol de publicare, versiune așteptată și cheie de idempotentă. Contractul nu acceptă SQL liber, credențiale sau reguli de acces furnizate de AI. Endpointurile nu există prin această livrare.
''')
text=(L/'report_content.txt').read_text(encoding='utf-8');testrows=[]
for line in text.splitlines():
 if re.match(r'^\|T\d\d\|',line):
  x=line.strip('|').split('|');testrows.append(x+['Neexecutat','De desemnat','',''])
with (R/'05_Pilot_si_operare/teste_acceptanta.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','Scenariu','Rezultat_asteptat','Status','Responsabil','Rezultat_obtinut','Dovada']);w.writerows(testrows)
write('01_iDempiere/inventar_read_only.sql','''-- Propunere de inventar PostgreSQL iDempiere. Nu a fost executată pe producție.
-- Rulați cu un cont autorizat read-only. Nicio extragere de tranzacții sau credențiale.
BEGIN TRANSACTION READ ONLY;
SET LOCAL statement_timeout = '30s';
SELECT tablename FROM ad_table WHERE isactive='Y' AND
 (tablename LIKE 'PA_%' OR tablename IN ('AD_Chart','AD_ChartDatasource','AD_ReportView','AD_PrintFormat','AD_Alert','AD_Scheduler')) ORDER BY tablename;
SELECT ad_form_id, name, classname, isactive FROM ad_form ORDER BY name;
SELECT ad_process_id, value, name, classname, jasperreport, isreport, isactive FROM ad_process
 WHERE isreport='Y' OR lower(name) LIKE '%dashboard%' OR lower(name) LIKE '%performance%' ORDER BY name;
SELECT ad_menu_id, name, action, ad_window_id, ad_process_id, ad_form_id, isactive FROM ad_menu ORDER BY name;
SELECT ad_window_id, name, windowtype, isactive FROM ad_window ORDER BY name;
-- Configurațiile suplimentare PA_DashboardContent, drepturi și bundle-uri se inventariază
-- după validarea coloanelor din versiunea reală. Nu exportați secrete din SysConfig.
ROLLBACK;
''')
write('05_Pilot_si_operare/README.md','''# Pilot și operare

Pilot propus: două firme și două organizații, dashboard financiar, comercial și stoc. Niciun test de aici nu a fost executat pe producție. CSV-ul conține 16 scenarii cu rubrici pentru responsabil, rezultat și dovadă.

Ordine: inventar și metrici aprobate; mart reconciliat; integrare ERP; configurare AI; teste de izolare; performanță; restaurare; decizie de producție. Estimarea de 43–77 zile om din raport este o ipoteză inginerească, nu ofertă sau măsurare.

În manifestul de implementare fixați versiunile și digesturile imaginilor, schema metadatelor, driverul PostgreSQL, SDK-ul, versiunea pluginului OSGi și revizia modelului AI. Nu folosiți `latest` în producție.

Backup: DB metadate BI, catalog KPI, profile, configurație și mappinguri. Restaurare într-un mediu separat, urmată de reconciliere și teste de acces. Cheile se păstrează în managerul de secrete, separat de documentație.

Disponibilitatea AI nu condiționează afișarea dashboardurilor existente. Mockurile sunt interzise în rezultatele manageriale. Concurența, p95 și prospețimea se măsoară pe date și volume aprobate.
''')
mods=json.loads((R/'01_iDempiere/inventar_module.json').read_text(encoding='utf-8'))
write('01_iDempiere/README.md','# Inventar BI iDempiere\n\n'+str(len(mods))+' componente și familii documentate. Versiunile sunt repere din surse, nu inventar al instalării Eva. CSV/Excel separă disponibilitatea de confirmarea în runtime.\n\n|Componentă|Tip|Versiune|Rol|Surse|\n|---|---|---|---|---|\n'+'\n'.join('|'+ '|'.join(str(m[k]) for k in ['name','kind','version','role','source'])+'|' for m in mods)+'\n\nRulați inventarul read-only numai după verificarea schemei și a drepturilor. Exportul OSGi și drepturile efective necesită o verificare suplimentară în instalare.\n')
src=json.loads((R/'06_Surse_oficiale/surse.json').read_text(encoding='utf-8'))
write('06_Surse_oficiale/README.md','# Surse oficiale și starea descărcărilor\n\nConsultați `surse.json` pentru URL, HTTP, hash și fișier. Unele pagini wiki resping descărcarea cu 403; nu sunt prezentate drept manuale salvate. S02/S03/S05 sunt redirecționări scurte, înlocuite de S38/S39/S40 și manualul Superset. S11 și S49 sunt referințe nerecuperate. Versiunile release sunt în `versiuni_identificate.json`; API GitHub a returnat 403 pentru unele interogări păstrate în `releases.json`.\n\n|ID|Document|Sursă / descărcare|Copie locală|\n|---|---|---|---|\n'+'\n'.join(f"|{s['id']}|{s['title']}|[Oficial]({s['url']})|"+(f"[Fișier](../{s['local']})" if s.get('local') else 'Indisponibilă')+'|' for s in src))
manual=json.loads((R/'07_Manuale_complete/manifest.json').read_text(encoding='utf-8'))
write('07_Manuale_complete/README.md','# Manuale și surse documentare complete pe repository\n\nInstantanee ale directoarelor documentare selectate, cu imagini incluse unde aparțin acelor directoare. Nu sunt copii executabile ale site-urilor, nici distribuții instalabile ale aplicațiilor. Paginile pot descrie ediții Enterprise sau funcții în dezvoltare; evaluarea gratuită este în raport și Excel. Nu se presupune că SHA-ul documentației este SHA-ul release-ului recomandat.\n\n|Bibliotecă|Commit documentație|Fișiere|Arhivă oficială completă|\n|---|---|---|---|\n'+'\n'.join(f"|[{m['name']}]({m['name']}/)|{m.get('commit','neconfirmat')}|{m.get('files',0)}|[Download]({m.get('download_url','')})|" for m in manual)+'\n\nSelecția exactă de fișiere și hashul arhivei descărcate sunt în fiecare PROVENIENTA.json și în manifest.json. Pentru iDempiere este salvat directorul docs; resursele din afara acestuia și wiki-ul istoric pot necesita acces online. Licențele și atribuirile originale sunt păstrate. Manualul PDF Knowage este în 06_Surse_oficiale/Knowage.\n')
write('02_Matrice/README.md','''# Matrice comparativă

[Descarcă Excelul](Comparatie_BI_iDempiere_Eva.xlsx?raw=true)

64 de funcții comparate pe cinci aplicații BI, iDempiere și codul Eva. Foile Module native și Extensii pun fiecare componentă pe coloană. Catalogul include versiuni, licențe și limite. Note functii și Surse permit verificarea evaluărilor.

✓ Da = nativ sau cod observat; ◐ Parțial = configurare, limită sau componentă dormantă; ✕ Nu = necesită dezvoltare ori ediție plătită; ? Neconfirmat = dovadă insuficientă; — N/A = în afara rolului componentei. Nu numărați mecanic N/A ca lipsă.

`matrice_64_functii.csv` păstrează codurile tehnice din raport, iar `scoruri.csv` conține judecățile ponderate ale autorului, fără a pretinde benchmark. Scorul este suma (notă × pondere) / 5; ponderile însumează 100.
''')
write('README.md','''# Business Intelligence pentru Eva Accounting și iDempiere

Evaluare tehnică și managerială, 8 octombrie 2026. Recomandare: pilot Apache Superset, rapoarte ERP păstrate și configurator AI local după profilul companiei. Metabase OSS este principalul contracandidat, inclusiv datorită Metabot/MCP gratuit cu provider propriu; embeddingul și securitatea avansată au limite de ediție.

## Documente de descărcat

- [Excel comparativ: aplicații, module, versiuni și bife](02_Matrice/Comparatie_BI_iDempiere_Eva.xlsx?raw=true)
- [Raport PDF](00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.pdf?raw=true)
- [Raport Word editabil](00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.docx?raw=true)
- [Raport pentru citire în GitHub](00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.md)
- [Raport HTML offline](00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.html?raw=true)

## Capitole și anexe

- [Inventarul iDempiere](01_iDempiere/README.md)
- [Matrice și metodă](02_Matrice/README.md)
- [Audit Eva fixat la commit](03_Audit_Eva_Accounting/commit_si_fisiere.json)
- [Arhitectură și exemple AI](04_Arhitectura_AI/README.md)
- [Pilot și teste de acceptanță](05_Pilot_si_operare/README.md)
- [Registrul surselor oficiale](06_Surse_oficiale/README.md)
- [Manuale, fișiere locale și linkuri de download](07_Manuale_complete/README.md)

Comparația include cinci aplicații, 64 de funcții BI și 36 de componente/familii iDempiere identificate. Nu certifică toate extensiile private sau istorice. Versiunea găsită nu confirmă instalarea sau compatibilitatea cu Eva. Funcțiile comerciale și cele neconfirmate sunt marcate explicit.

Auditul de cod folosește commitul Eva `1c039193e0c1626cb03fb8ca37f9980a1703fd0c`. Nu s-a accesat baza de producție, nu s-au instalat motoare BI și nu s-au executat testele pilotului. Profilele AI sunt sintetice. Costul licenței poate fi zero; integrarea, infrastructura și operarea consumă resurse.

Originalele descărcate își păstrează licențele și atribuirea. SHA-256 și proveniența sunt în manifestele din bibliotecă. Cheile GitHub nu sunt incluse.
''')
links=[('Excel comparativ','02_Matrice/Comparatie_BI_iDempiere_Eva.xlsx'),('Raport PDF','00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.pdf'),('Raport Word','00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.docx'),('Raport HTML','00_Raport/Raport_BI_iDempiere_Eva_2026-10-08.html')]
write('index.html','<!doctype html><html lang="ro"><meta charset="utf-8"><title>BI Eva iDempiere</title><style>body{font:18px/1.6 Arial;max-width:950px;margin:60px auto;color:#183044}a{color:#174f79}li{margin:14px 0}td,th{padding:10px;border-bottom:1px solid #ccc;text-align:left}</style><h1>Business Intelligence pentru Eva și iDempiere</h1><p>Evaluare 8 octombrie 2026. Documentație locală și comparație pentru decizia de integrare.</p><ul>'+''.join(f'<li><a href="{u}">{n}</a></li>' for n,u in links)+'</ul><h2>Manuale și downloaduri oficiale</h2><table><tr><th>Produs</th><th>Fișiere locale</th><th>Download oficial</th></tr>'+''.join(f'<tr><td>{m["name"]}</td><td><a href="07_Manuale_complete/{m["name"]}/">{m.get("files",0)} fișiere</a></td><td><a href="{html.escape(m.get("download_url",""))}">Arhivă repository la commit</a></td></tr>' for m in manual)+'</table><p>Licențele, limitele edițiilor și incertitudinile sunt explicate în raport. Nu este o instalare sau un test de producție.</p></html>')
print('Annexes created; profiles validated:',3,'pilot tests:',len(testrows))
