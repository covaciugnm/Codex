import ast, json, pathlib, re, typing
r=pathlib.Path(__file__).resolve().parent
p=r/'source/backend/app/api/v1/endpoints/eva_chat.py'
t=ast.parse(p.read_text(encoding='utf-8'))
nodes=[n for n in t.body if (isinstance(n,ast.FunctionDef) and n.name in ('_sql_string_mask','assert_readonly_sql')) or (isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_WRITE_KW_RE' for x in n.targets))]
env={'re':re,'List':typing.List}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),env)
out=[]
for sql in ['SELECT email, hashed_password FROM public.users', "SELECT pg_read_file('/etc/hostname')", 'DELETE FROM public.users']:
    try: env['assert_readonly_sql'](sql); accepted=True
    except ValueError: accepted=False
    out.append({'check':'actual_sql_guard_offline','sql':sql,'accepted':accepted,'executed_against_database':False})
syntax=[]
for p in (r/'source/backend/app').rglob('*.py'):
    try: ast.parse(p.read_text(encoding='utf-8-sig'))
    except SyntaxError as e: syntax.append({'file':str(p.relative_to(r)),'line':e.lineno,'error':e.msg})
out.append({'check':'python_syntax','files':len(list((r/'source/backend/app').rglob('*.py'))),'errors':syntax})
(r/'extended-checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
