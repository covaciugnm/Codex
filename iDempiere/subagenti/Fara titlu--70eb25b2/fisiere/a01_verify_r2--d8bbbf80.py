"""Read-only verification. Usage: python verifica_R2.py <executie-dir> <report-path>."""
import sys,pathlib,json,hashlib
ex=pathlib.Path(sys.argv[1]);path=pathlib.Path(sys.argv[2]);rd=lambda f:json.loads(f.read_text(encoding='utf-8-sig')); h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();r=rd(path);prior=rd(ex/'A01_raport.json');checks=[]
def test(ok,name):
 if not ok:raise AssertionError(name)
 checks.append(name)
test(r['git_sha']=='6df998aee0e514d30856c461962afe99ebd0d113','git cutoff');test(h(ex/'A01_raport.json')==r['R1']['sha256'],'R1 immutable');
for k,v in r['evidence_manifest_external'].items():test(h(ex/v['path_relative_to_executie'])==v['sha256'],'external '+k)
for k,v in r['local_artifacts'].items():test(h(path.parent/k)==v['sha256'],'local '+k)
for key,n in [('controls',38),('pipelines',9),('findings',14)]:
 rows=r[key];test(len(rows)==n and [q['id'] for q in rows]==[q['id'] for q in prior[key]],key+' IDs');
 for q in rows:
  for e in q['R2_evidence_refs']:test(e in r['evidence_manifest_external'] or e in r['local_evidence_aliases'],q['id']+' '+e)
fx=rd(path.parent/r['local_evidence_aliases']['PG16']);test(fx['postgres_cleanup_verified'] and fx['DB_cleanup'],'PG cleanup');test(len(fx['checks'])==62 and len(fx['frontend'])==11,'PG cases'); ir=rd(ex/r['evidence_manifest_external']['IR']['path_relative_to_executie']);test({c['id'] for c in ir['cases']}=={'A01.F01','A01.F02','A01.F04','A01.F05'},'A11 P0 set');f=next(x for x in r['findings'] if x['id']=='A01.F06');test(f['severity'] is None,'policy separated');test(r['quality_score'] is None and r['product_score'] is None,'no self grading');print(json.dumps({'checks_passed':len(checks),'report_sha256':h(path),'errors':[]}))
