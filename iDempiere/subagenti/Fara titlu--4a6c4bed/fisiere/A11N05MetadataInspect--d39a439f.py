import pathlib,json,hashlib,collections
B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03')
f=json.loads((B/'Fise_sursee_N05_v1.json').read_text(encoding='utf8'))
print('keys',f.keys())
for r in f['files']:print(pathlib.PurePosixPath(r['path']).name,r['state'],r['phase'],r['methods_in_scope'],r['control'])
print('extras',[(k,v) for k,v in f.items() if k!='files'])
for n in ['Runtime_instalat_N05_v1.json','Anexa_reproducere_N05_v1.json','Oracle_independent_N05_v1.json']:
 p=B/n
 if not p.exists():print('missing',n);continue
 d=json.loads(p.read_text(encoding='utf8'));print(n, list(d) if isinstance(d,dict) else type(d),str(d)[:3500])
print('runtime paths',list(B.glob('*Runtime*')))
