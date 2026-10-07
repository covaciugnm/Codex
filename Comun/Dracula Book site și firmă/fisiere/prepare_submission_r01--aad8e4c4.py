from pathlib import Path
import sys,json,hashlib,subprocess,datetime
sys.stdout.reconfigure(encoding='utf-8')
root=Path(r'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000')
rub=json.loads((root/'06_REGISTRU/rubrics.json').read_text(encoding='utf-8'))['rubrics']
items=[]
core=['00_CONDUCERE/MANUAL_ATELIER.md','00_CONDUCERE/TRASABILITATE.md','00_CONDUCERE/ROADMAP.md','00_CONDUCERE/RUBRICI.md','00_CONDUCERE/PROTOCOL_ARHIVARE.md','00_CONDUCERE/policy.json','06_REGISTRU/roadmap.json','06_REGISTRU/roles.json','06_REGISTRU/rubrics.json']
core += [p.relative_to(root).as_posix() for d in ['01_ECHIPA','03_MODELE','04_INSTRUMENTE'] for p in (root/d).iterdir() if p.is_file() and p.suffix in ['.md','.json','.csv','.py']]
core += ['Manual_operational_atelier_Dracula_Book.pdf','Manual_operational_atelier_Dracula_Book.docx']
for id,paths,producers,roles,deps in [
('SYS-001',core,['01a07b90-9d07-7e72-8eb7-8439e985b9ba','01a0d0d9-1f95-7211-8093-c26e28e6ebee'],['A-GOVERNANCE','A-SYSTEMS'],[]),
('SEL-001',['02_DOCUMENTARE/CANON_EXISTENT.md'],['01a0d0d7-e865-7b71-9707-be8786099512'],['A-GOVERNANCE','A-CANON'],['SYS-001']),
('RES-001',['02_DOCUMENTARE/REPERE_SI_MECANISME.md','02_DOCUMENTARE/BANCA_MECANISME_EXTINSA.md'],['01a0d0d8-0415-77a3-88c6-755ad2530f62'],['A-GOVERNANCE','A-SOURCES'],['SYS-001'])]:
    files=[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in sorted(set(paths))]
    items.append(dict(id=id,stage='G00',status='DEPUS-r01',files=files,producer_agent_ids=producers,required_audit_roles=roles,dependencies=deps,requirements={},criteria=[{'id':c['id'],'weight':c['weight']} for c in rub[id]],audits=[]))
(root/'06_REGISTRU/deliverables.json').write_text(json.dumps({'deliverables':items},ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(root/'04_INSTRUMENTE'),'-p','test_*.py','-v'],capture_output=True,text=True,encoding='utf-8')
(root/'06_REGISTRU/TESTE_CONFIGURARE_r01.txt').write_text('Data UTC: '+now+'\nTeste executate de coordonator; nu audit literar.\n'+p.stdout+p.stderr,encoding='utf-8')
assert p.returncode==0
print(json.dumps({'manifest':[(i['id'],len(i['files'])) for i in items],'tests_exit':p.returncode,'tests_tail':p.stderr[-160:]},ensure_ascii=False))

