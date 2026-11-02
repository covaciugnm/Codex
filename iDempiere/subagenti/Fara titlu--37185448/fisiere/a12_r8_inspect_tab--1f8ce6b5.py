from a12_r8_cases import *
z=next(x for x in rd(Path('D:/CodexWork/a12-r8-spec-extra/index.json')) if '/T224-'in x['file']and x['file'].endswith('10_audit_lot_A_r1.md'));print('\n'.join(txt(z).splitlines()[130:140]));print(z['oid'])

