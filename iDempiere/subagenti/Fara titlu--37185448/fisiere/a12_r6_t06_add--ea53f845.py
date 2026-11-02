from a12_r6_exec import *
src=Path(__file__).parent/'a12_r6_t06_erp.py';s=src.read_text(encoding='utf8');j=plug/'src/com/eva/ro/contab/banca/CititorArhivaSaga.java'
pairs={a:re.findall('"([A-Z_]+)"',b)for a,b in re.findall(r'COLOANE\.put\("([A-Z_]+)", List\.of\((.*?)\)\)',j.read_text(encoding='utf8'),re.S)}
assert len(pairs)==7,pairs
s=s.replace("foreign=inspect(prefix+'_foreign.db',f.read_bytes())","with sqlite3.connect(f) as c:\n   for table,columns in "+repr(pairs)+".items():c.execute('create table '+table+' ('+','.join(z+' text' for z in columns)+')')\n  foreign=inspect(prefix+'_foreign.db',f.read_bytes())")
s=s.replace("for label,name,d in cases:","for label,name,d in cases[3:]:")
p=Path(__file__).parent/'a12_r6_t06_complete_schema.py';p.write_text(s,encoding='utf8')
z=sp.run(['ssh','-o','BatchMode=yes',server,'cd /tmp/eva-contab-codex-p01uizk-r5.vUjauFBh && python3 -'],input=p.read_bytes(),stdout=sp.PIPE,stderr=sp.PIPE,timeout=100);assert z.returncode==0,z.stderr.decode()[-400:]
data=json.loads(z.stdout);data['schema_source_sha']=sha(j);data['archive_columns']=pairs;wr(E6/'T06_proces_direct_GardenWorld_schema_completa.json',data);print([(v['case'],v['response'],v['delta'])for v in data['runs']])

