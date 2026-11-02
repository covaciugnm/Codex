from a03_r8_base import *
import shutil
base=out.parents[2]; frozen=out/'Registru_A03_R8_final.json';r=json.loads(frozen.read_text(encoding='utf8'));assert H(frozen.read_bytes())=='7bdfc31bf06daed0f4f1c7bc19250981c787bf1cdbe13a677f63cf5ee9420e4d'
def main():
 refs={x['file']:x['sha256'] for c in r['r8'] for x in c['dovezi']}; refs.update({r[k]['file']:r[k]['sha256'] for k in ('base_queue','R4_unchanged','T191_amendament')})
 assert all(H((base/k).read_bytes())==s for k,s in refs.items());assert len(r['r8'])==len({x['criterion'] for x in r['r8']})==239
 repro=out/'reproducere';repro.mkdir(exist_ok=True)
 for f in P('D:/CodexWork').glob('a03_r8_*.py'):shutil.copyfile(f,repro/f.name)
 summary=P(out.parent/'T191/T191_supliment_sase_criterii.json');assert H(summary.read_bytes())=='92f6ea7e1727a8917f2e3cb7ca86e444f8c82555eee2e237fafcf7e8d019400f'
 pg=P('D:/CodexWork/p01-local-pg16');status=sp.run([pg/'pgsql/bin/pg_ctl.exe','-D',pg/'data','status'],capture_output=True);assert status.returncode==3
 w=(work/'remote.txt').read_text();assert re.fullmatch(r'/tmp/p01-a03r8-source-[A-Za-z0-9]{6}',w);code=f"""import pathlib,shutil
p=pathlib.Path('{w}').resolve()
assert p.parent==pathlib.Path('/tmp') and p.name.startswith('p01-a03r8-source-')
assert (p/'.git/refs/heads/audit-fixed').read_text().strip()=='{sha}'
assert (p/'frozen.jar').exists()
shutil.rmtree(p)
assert not p.exists()
print('temporary export removed')
"""; d=ssh("python3 -",code.encode());assert d.returncode==0,d.stderr
 allf=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='Manifest_A03_R8.json');manifest={'utc':UTC(),'main_registry':{'file':frozen.name,'sha256':H(frozen.read_bytes())},'crosscheck_t191_after_registry':{'file':str(summary.relative_to(base)).replace('\\','/'),'sha256':H(summary.read_bytes()),'note':'Suplimentul coordonatorului a fost adăugat după semnarea registrului A03. Arbitrajul nominal pentru aceste șase criterii aparține A12 și nu se numără de două ori în totalurile A03.'},'R7_population_verified':239,'distinct_references_rehashed':len(refs),'resource_check':{'postgres_local':'stopped, pg_ctl reports no server running','T256_databases':'new dedicated temporary databases were dropped; successful statements recorded','remote_temp':d.stdout.decode().strip(),'production_writes':0},'artifacts':[{'path':str(p.relative_to(out)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in allf],'scope':'Journaux de tentatives initiales, pas de changement de statut implicite: pytest-T58 échec transport/encodage Windows corrigé en UTF8/socketpair privé 36/36. Vérification du registre final et des références, sans auto-note.'};J(out/'Manifest_A03_R8.json',manifest);print('refs',len(refs),'files',len(allf),'manifest',H((out/'Manifest_A03_R8.json').read_bytes()))
if __name__=='__main__':main()

