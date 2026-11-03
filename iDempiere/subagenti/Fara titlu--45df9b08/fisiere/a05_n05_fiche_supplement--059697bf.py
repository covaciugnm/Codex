from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'MANIFEST_A05_N05_lot03_v1.json').read_text());bad=[x['path']for x in m['files']if sha(O/x['path'])!=x['sha256']];assert not bad
rows=json.loads((O/'Fise_sursee_N05_v1.json').read_text())['files'];fixed=[]
for x in rows:
 if x['path'].endswith('/JobFundal.java'):
  x['normal_path']='DialogNotaSetWms.inregistreaza → JobFundal.pornesteProces → ProceseEcran.ruleaza; numai citire statică JobFundal, fără executarea UI sau a jobului în fundal.';fixed.append(x)
 if x['path'].endswith('/ProceseEcran.java'):
  x['normal_path']='DialogNotaSetWms → JobFundal → ProceseEcran.ruleaza → ruleazaIntern/lanseaza → MProcess.processIt(pi,trx) managedTrx=true; metoda originală ProceseEcran executată, fără click ZK.';fixed.append(x)
keys=['oid','owner','peer','role','normal_path','requirement','positive','counterexample','persistent_effect','limit'];assert all(all(x.get(k)for k in keys)for x in rows)
p=O/'Fise_supliment_cale_normala_v1.json';assert not p.exists();p.write_text(json.dumps({'reason':'Autoverificarea găsește câmpul normal_path absent la două fișe suplimentare, deși calea era descrisă în protocol și raport. Completează nominal fără rescrierea manifestului sigilat. Niciun credit nou.','supersedes_only_fields':'normal_path pentru cele două surse de mai jos; restul fișelor sigilate rămân valabile','files':fixed},ensure_ascii=False,indent=2),encoding='utf8')
q=O/'QA_autoverificare_N05_v1.json';q.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sealed_manifest_sha256':sha(O/'MANIFEST_A05_N05_lot03_v1.json'),'rehash_files':len(m['files']),'bad_hashes':bad,'required_fields':keys,'fiches_checked':len(rows),'detected_and_corrected':'normal_path lipsă în JobFundal/ProceseEcran; completare aditivă','supplement_sha256':sha(p),'remaining_missing_fields':[]},ensure_ascii=False,indent=2),encoding='utf8')
s=O/'SIGILIU_supliment_N05_v1.json';s.write_text(json.dumps({'files':[{'path':p.name,'sha256':sha(p)},{'path':q.name,'sha256':sha(q)}],'base_manifest_sha256':sha(O/'MANIFEST_A05_N05_lot03_v1.json')},indent=2),encoding='utf8')
print('supplement',sha(p),'qa',sha(q),'seal',sha(s))
