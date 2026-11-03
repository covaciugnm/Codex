from pathlib import Path
# Resume the owned cluster after the recorded ownership-only setup failure. No new seed restore.
src=Path('D:/CodexWork/a05_n05_restore.py').read_text()
src=src.replace("assert not ROOT.exists();ROOT.mkdir()", "assert ROOT.is_dir() and not (ROOT/'pgdata/postmaster.pid').exists()")
start=src.index(" pw=ROOT/'synthetic_password.txt'")
end=src.index(' # Metadata synchronization')
src=src[:start]+" run('pg_start',[BIN/'pg_ctl.exe','-D',DATA,'-l',ROOT/'postgres.log','-w','start']);started=True\n"+src[end:]
src=src.replace('REASSIGN OWNED BY a05lab TO adempiere;', "DO $$ DECLARE r record; BEGIN FOR r IN SELECT relname,relkind FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='adempiere' AND relkind IN ('r','p','S','v','m') LOOP EXECUTE format('ALTER %s adempiere.%I OWNER TO adempiere', CASE r.relkind WHEN 'S' THEN 'SEQUENCE' WHEN 'v' THEN 'VIEW' WHEN 'm' THEN 'MATERIALIZED VIEW' ELSE 'TABLE' END,r.relname); END LOOP; END $$; ALTER SCHEMA adempiere OWNER TO adempiere;")
src=src.replace("so=OUT/(name+'.stdout.txt')", "name='v2_'+name;so=OUT/(name+'.stdout.txt')")
src=src.replace("'Izolare_seed_v1.json'", "'Izolare_seed_v2.json'").replace("'PG_restore_v1.json'", "'PG_resume_v2.json'")
exec(compile(src,'a05_n05_resume_generated','exec'))
