import json,zipfile,hashlib,shutil,datetime
from pathlib import Path
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A11/Val03_loturi')
paths=[Path('D:/CodexWork/a11-r12-mutator-20261103'),Path('D:/CodexWork/a11-r12-mutator-20261103-v2')]
archive=O/'Fixture_mutator_attempt01.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(paths[0].rglob('*')):
  if p.is_file():z.write(p,p.relative_to(paths[0]))
runner=O/'Runner_mutator_independent_v1.py';assert not runner.exists();shutil.copyfile('D:/CodexWork/A11R12MutatorIndependent.py',runner)
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cleanup_status':'RETAINED_AFTER_AUTOMATIC_APPROVAL_REJECTION','reason':'exec_command Remove-Item for both exact owned directories rejected before command start: blocked by policy. No retry, shell change, deletion API or workaround used.','targets':[{'path':str(p),'exists':p.exists(),'files':sum(x.is_file() for x in p.rglob('*'))} for p in paths],'persistent_processes_or_databases_started':0,'calibration':'Attempt01 denied py_compile fdopen because integer descriptor was not resolved. Attempt02 resolves the actual Windows handle path via GetFinalPathNameByHandleW and allows only scratch writes. Two canaries deny outside write and loopback connect. No product code changed.','masini_scratch':'Untouched','artifact_retention':'ZIP evidence and runners retained deliberately; scratch retention is an unresolved resource-cleanup limitation, not full restitution.'}
p=O/'Cleanup_mutator_independent_v1.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'targets':d['targets']}))
