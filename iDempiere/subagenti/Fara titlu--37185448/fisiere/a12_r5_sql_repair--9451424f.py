from pathlib import Path
p=Path(__file__).parent/'a12_r5_sql_suite.py';s=p.read_text(encoding='utf8')
s=s.replace("out=E/'R5/sql_batch';out.mkdir(exist_ok=True)","out=E/'R5/sql_batch/recalibrare';out.mkdir(exist_ok=True)")
s=s.replace("cls,tp[tag],deps]","cls,(plug/re.search(r'/plug/(src/[^\"\\n]+)',body)[1] if n in ('TestT58Sql','TestT29Sql') else tp[tag]),deps]")
s=s.replace("ss=sorted((plug/'test/sql').glob('*.java'));","previous=rd(E/'R5/sql_batch/executii.json');allowed={(v['target'],v['task_suite'])for v in previous if v['psql_exit'] is None};ss=sorted((plug/'test/sql').glob('*.java'));")
s=s.replace("for z in ('git','instalat')]))","for z in ('git','instalat') if (z,f.stem) in allowed]))")
(p.parent/'a12_r5_sqlsecond.py').write_text(s,encoding='utf8')

