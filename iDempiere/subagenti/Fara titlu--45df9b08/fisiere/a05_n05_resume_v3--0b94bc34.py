from pathlib import Path
r=Path('D:/CodexWork/a05-r12-native-lab-n05-20261103/pgdata').resolve()
assert r.parent.name=='a05-r12-native-lab-n05-20261103' and not(r/'postmaster.pid').exists()
with(r/'postgresql.conf').open('a')as f:f.write('\nmax_locks_per_transaction=1024\n')
s=Path('D:/CodexWork/a05_n05_resume.py').read_text().replace("name='v2_'", "name='v3_'").replace('Izolare_seed_v2','Izolare_seed_v3').replace('PG_resume_v2','PG_resume_v3')
exec(compile(s,'a05_n05_resume_v3_generated','exec'))
