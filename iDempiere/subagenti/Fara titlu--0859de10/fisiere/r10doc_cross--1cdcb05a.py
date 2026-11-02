from pathlib import Path
import json,hashlib,re
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');F=B/'executie/R10_pregatire/A12/R10_documentar_supliment';S=F/'Rezultat.json';E=F/'Extras_Git.json'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads(E.read_bytes())['extracts'];t22=x['require_T22.15']['extracts'][0]['parsed']['titlu'];gate=x['T22Verdict']['extracts'][0]['text']
def reconcile(title,line):
 mt=re.search(r't22-site-backend\s+([0-9a-f]{7,40})',title);m1=re.search(r'c1-integrare-b[^@]+@\x60([0-9a-f]{7,40})',line);m2=re.search(r'Pasul 2 .*?rămâne BLOCAT[^.]+?codul \x60([0-9a-f]{7,40})',line)
 old=mt[1]if mt else None;k1=m1[1]if m1 else None;k2=m2[1]if m2 else None
 return {'historic_lost':old,'step_1_integration':k1,'step_2_lost_ref':k2,'same_lost_hash_and_distinct_integration_hash':bool(old and k1 and k2 and old==k2 and k1!=old)}
obs=reconcile(t22,gate);neg=reconcile(t22,gate.replace('039a336fec','59d88ca'));assert obs['same_lost_hash_and_distinct_integration_hash'] and not neg['same_lost_hash_and_distinct_integration_hash']
p=F/'T22_15_hashuri_etalon.json';p.write_text(json.dumps({'parent':{'file':S.relative_to(B).as_posix(),'sha256':h(S),'pointer':'/rows/1'},'criterion':'T22.15-R3-001','purpose':'Rafinarea verificării identității hashurilor din surse: câmpul forbidden_old_hash_conflation din registrul preliminar citează două constante prestabilite. Acest comparator extrage independent toate cele trei valori din textul fizic păstrat și respinge substituția la etapa1.','input':{'file':E.relative_to(B).as_posix(),'sha256':h(E),'pointers':['/extracts/require_T22.15/extracts/0/parsed/titlu','/extracts/T22Verdict/extracts/0/text']},'measured':obs,'mutant_new_equals_old':neg,'full_product':None},ensure_ascii=False,indent=2),encoding='utf8');print(p.name,h(p),obs,neg)
