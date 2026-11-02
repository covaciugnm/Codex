"""Offline reproductions against copied production functions; no real accounts or network."""
import ast, asyncio, json, pathlib, re, types, uuid
from unittest.mock import AsyncMock

root=pathlib.Path(__file__).resolve().parent
deps=root/'source/backend/app/api/deps.py'
tree=ast.parse(deps.read_text(encoding='utf-8'))
chosen=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in ('get_schema_name','get_current_user','get_client_ip')]
for n in chosen:
    n.decorator_list=[]
    n.args.defaults=[]
    n.returns=None
    for a in n.args.args: a.annotation=None
class Query:
    def where(self,*args): return self
class HTTPException(Exception):
    def __init__(self,**kw): self.status_code=kw.get('status_code'); super().__init__(kw)
class User: id='id'
user=types.SimpleNamespace(id=uuid.uuid4(),email='audit@example.com',is_active=True)
payload={'sub':str(user.id),'sid':'synthetic-session','type':'refresh'}
env={'re':re,'UUID':uuid.UUID,'HTTPException':HTTPException,'status':types.SimpleNamespace(HTTP_401_UNAUTHORIZED=401,HTTP_403_FORBIDDEN=403),'decode_token':lambda _:payload,'text':lambda x:x,'select':lambda _:Query(),'User':User,'session_exists':AsyncMock(return_value=True),'touch_session':AsyncMock()}
exec(compile(ast.Module(body=chosen,type_ignores=[]),str(deps),'exec'),env)
results=[]
for a,b in [('a.b@example.com','a-b@example.com'),('ab@example.com','a+b@example.com'),('a'*56+'@one.example','a'*56+'@two.example')]:
    x,y=env['get_schema_name'](a),env['get_schema_name'](b)
    results.append({'test':'tenant_collision','a':a,'b':b,'same_schema':x==y,'schema':x})
async def run():
    db=types.SimpleNamespace(execute=AsyncMock(return_value=types.SimpleNamespace(scalar_one_or_none=lambda:user)))
    got=await env['get_current_user'](types.SimpleNamespace(credentials='synthetic-refresh-token'),db)
    results.append({'test':'refresh_type_passes_access_dependency','accepted':got is user,'queries':db.execute.await_count})
    payload['type']='access'
    env['session_exists']=AsyncMock(return_value=None)
    got=await env['get_current_user'](types.SimpleNamespace(credentials='synthetic-revoked-token'),db)
    results.append({'test':'redis_failure_bypasses_session_revocation_check','accepted':got is user})
asyncio.run(run())
request=types.SimpleNamespace(headers={'CF-Connecting-IP':'203.0.113.99'},client=types.SimpleNamespace(host='192.0.2.15'))
results.append({'test':'client_ip_trusts_header_without_proxy_check','returned':env['get_client_ip'](request),'peer':request.client.host})
out=json.dumps(results,ensure_ascii=False,indent=2)
(root/'security-reproductions.json').write_text(out,encoding='utf-8')
print(out)
