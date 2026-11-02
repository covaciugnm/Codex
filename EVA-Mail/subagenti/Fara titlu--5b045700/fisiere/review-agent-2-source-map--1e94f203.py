"""Candidate dependency map from historical snapshot; does not execute app code."""
import ast, re, pathlib, json, hashlib, datetime
R=pathlib.Path(__file__).resolve().parent
S=R.parent/'audit-2026-10-30/source'
front=S/'frontend/src'
app=(front/'App.tsx').read_text(encoding='utf-8-sig')
app=re.sub(r'\{/\*.*?\*/\}','',app,flags=re.S)
routes=[]
blocks=re.split(r'(?=<Route\b)',app)
for b in blocks:
    route=re.search(r'\bpath=[\"\']([^\"\']+)',b)
    if not b.startswith('<Route') or not route: continue
    pages=re.findall(r'<([A-Za-z]+Page)\b',b)
    redirect=re.search(r'<Navigate\s+to=[\"\']([^\"\']+)',b)
    routes.append({'route':route.group(1),'pages':sorted(set(pages)),'redirect_candidate':redirect.group(1) if redirect else None})
pages=[]
for p in sorted((front/'pages').glob('*.tsx')):
    t=p.read_text(encoding='utf-8-sig')
    imported_services=sorted(set(re.findall(r'from\s+[\"\']\.\./services/([^\"\']+)',t)))
    invoked=sorted(set(re.findall(r'\b([A-Za-z]\w*Service)\.(\w+)\s*\(',t)))
    direct=[]
    for m in re.finditer(r'\bapi\.(get|post|put|patch|delete)\s*(?:<[^>]+>)?\s*\(\s*([\"\'`])(.+?)\2',t,re.S):
        path=m.group(3)
        if len(path)<240: direct.append({'verb':m.group(1).upper(),'path_candidate':path,'line':t[:m.start()].count('\n')+1})
    pages.append({'page':p.stem,'source':str(p.relative_to(S)),'routes':[x['route'] for x in routes if p.stem in x['pages']],'service_modules':imported_services,'service_invocations':['.'.join(x) for x in invoked],'direct_api_candidates':direct,'not_runtime_proof':True})
services=[]
for p in sorted((front/'services').glob('*.ts')):
    t=p.read_text(encoding='utf-8-sig')
    calls=[]
    for m in re.finditer(r'\bapi\.(get|post|put|patch|delete)\s*(?:<[^>]+>)?\s*\(\s*([\"\'`])(.+?)\2',t,re.S):
        path=m.group(3)
        if len(path)<240: calls.append({'verb':m.group(1).upper(),'path_candidate':path,'line':t[:m.start()].count('\n')+1})
    services.append({'module':p.stem,'source':str(p.relative_to(S)),'api_call_candidates':calls})
router=S/'backend/app/api/v1/router.py'
tree=ast.parse(router.read_text(encoding='utf-8-sig'))
aliases={}
for n in ast.walk(tree):
    if isinstance(n,ast.ImportFrom) and n.module=='app.api.v1.endpoints':
        for x in n.names: aliases[x.asname or x.name]=x.name
prefixes={}
for n in ast.walk(tree):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='include_router' and n.args:
        obj=n.args[0]
        if isinstance(obj,ast.Attribute) and isinstance(obj.value,ast.Name):
            pre=next((x.value.value for x in n.keywords if x.arg=='prefix' and isinstance(x.value,ast.Constant)),'')
            prefixes.setdefault((aliases.get(obj.value.id,obj.value.id),obj.attr),[]).append(pre)
endpoints=[]
for p in sorted((S/'backend/app/api/v1/endpoints').glob('*.py')):
    t=p.read_text(encoding='utf-8-sig'); tr=ast.parse(t)
    for n in ast.walk(tr):
        if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)): continue
        for d in n.decorator_list:
            if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and isinstance(d.func.value,ast.Name) and d.func.attr in ('get','post','put','patch','delete','websocket') and d.args and isinstance(d.args[0],ast.Constant):
                prefs=prefixes.get((p.stem,d.func.value.id),[])
                endpoints.append({'source':str(p.relative_to(S)),'line':n.lineno,'function':n.name,'router':d.func.value.id,'verb':d.func.attr.upper(),'suffix':d.args[0].value,'path_candidates':['/api/v1'+x+d.args[0].value for x in prefs],'registration_known':bool(prefs),'authorization_not_inferred':True})
out={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'HISTORICAL_SNAPSHOT_CANDIDATES_ONLY','snapshot_date':'2026-10-30','head_historical':'d7040dc21a64dfcfda660b7c8eda4a7ca9812e45','app_sha256':hashlib.sha256((front/'App.tsx').read_bytes()).hexdigest(),'limitations':['Regex frontend candidates may omit dynamic URLs, fetch/SSE and nested callbacks; not a complete control count.','Backend AST captures decorators and aggregator prefixes; router-internal prefixes, main/proxy/MCP routes and runtime registration need reconciliation.','No authentication or effectiveness conclusion follows from endpoint presence.','No live requests, user data reads or UI actions performed.'],'routes':routes,'pages':pages,'services':services,'endpoints':endpoints}
(R/'review-agent-2-historical-dependency-candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'route_candidates':len(routes),'pages':len(pages),'service_modules':len(services),'endpoint_decorators':len(endpoints),'unregistered_in_v1_aggregator':sum(not x['registration_known'] for x in endpoints)},indent=2))
