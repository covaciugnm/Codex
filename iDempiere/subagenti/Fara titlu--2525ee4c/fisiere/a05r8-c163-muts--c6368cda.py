from pathlib import Path
import ast,subprocess as sp,json,sys,os,hashlib,io,tarfile,uuid,concurrent.futures,datetime,re
sys.argv.append('noboot')
import importlib.machinery
git=importlib.machinery.SourceFileLoader('gitx','D:/CodexWork/a05r8-git.py').load_module()
r=importlib.machinery.SourceFileLoader('rx','D:/CodexWork/a05r8-run.py').load_module()
scratch=r.scratch/'C163_mutants';scratch.mkdir(parents=True,exist_ok=True)
out=r.out/'T163_mutanti';out.mkdir(exist_ok=True)
gx='Documentatie/echipa-2026-10-09/T163-plus-minus-inventar/dovezi-08-cod/mutanti/genereaza_mutanti_A.py';gs=r.scratch/'guard-tree'/gx
prefix='idempiere/plugins/com.eva.ro.contab/'
mod=ast.parse(gs.read_text(encoding='utf8'));fis=next(x for x in mod.body if isinstance(x,ast.Assign) and hasattr(x.targets[0],'id') and x.targets[0].id=='FIS')
relatives=[b.right.value for b in fis.value.values];srcpaths=['src/com/eva/ro/contab/'+k for k in relatives]+['test/TestT163ArticoleDiverse.java','com.eva.ro.contab_13.0.0.jar']
sources={}; bases=['9980254afc56f7a852e8b7c90dc6b3ba1d81f491',r.cut]
program=git.header+'import tarfile,io\npaths='+repr([prefix+k for k in srcpaths]+[gx])+'\nrevs='+repr(bases)+"""
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as ar:
 for rev in revs:
  for p in paths:
   oid=g('rev-parse',rev+':'+p);b=blob(oid);ti=tarfile.TarInfo(rev+'/'+p);ti.size=len(b);ar.addfile(ti,io.BytesIO(b))
"""
artifact=scratch/'inputs.tar.gz'
if not artifact.exists():artifact.write_bytes(git.remote(program))
with tarfile.open(artifact) as ar:ar.extractall(scratch/'input',filter='data')
env={**os.environ,'PATH':str(r.jd)+';'+os.environ['PATH'],'PYTHONIOENCODING':'utf-8'}
def exe(arg,cwd,limit=40):
 cp=sp.run(arg,cwd=cwd,env=env,capture_output=True,timeout=limit);return cp.returncode,(cp.stdout+cp.stderr).decode('utf8','replace')
for rev in bases:
 plug=scratch/'input'/rev/prefix;gen=scratch/'input'/rev/gx
 assert gen.read_bytes()==gs.read_bytes(), 'unreviewed generator'
 # A fresh exclusive output makes the historical generator's optional rmtree branch unreachable.
 destination=(scratch/('generated_'+uuid.uuid4().hex)).resolve();assert destination.parent==scratch.resolve() and not destination.exists()
 rc,log=exe([sys.executable,'-X','utf8','-I',str(gen),str(plug),str(destination)],scratch)
 (out/(rev[:10]+'-generator.txt')).write_text(log,encoding='utf8')
 basecp=';'.join(map(str,[plug/'com.eva.ro.contab_13.0.0.jar',r.deps/'org.adempiere.base_13.0.0.202603090043.jar',r.deps/'org.adempiere.base.process_13.0.0.202603090043.jar','D:/CodexWork/a05-support-jars/*','D:/CodexWork/a12-r5-classes/all_deps/*','D:/CodexWork/eva-a01-java/lib/*']))
 tests=destination/'compiled-test';tests.mkdir()
 rc0,diag=exe([r.jd/'javac.exe','--release','17','-encoding','UTF-8','-cp',basecp,'-d',tests,plug/'test/TestT163ArticoleDiverse.java'],plug)
 assert rc0==0,diag[:400]
 spec={'version':rev,'generator_oid':r.bo(gen.read_bytes()),'jar_sha256':r.sha(plug/'com.eva.ro.contab_13.0.0.jar'),'jar_blob':r.bo((plug/'com.eva.ro.contab_13.0.0.jar').read_bytes()),'test_blob':r.bo((plug/'test/TestT163ArticoleDiverse.java').read_bytes()),'generator_rc':rc,'scope':'Exécuté locally with original Git sources/JAR and installed core deps, JVM network-disabled; compile each actual changed Java class and use own bytecode first. Flags adapting the original Docker orchestration; no product source changes. A red mutant must actually fail the original suite; missed anchors never count.','mutants':[]}
 ids=[d for d in sorted(destination.iterdir()) if (d/'regula.txt').exists()]
 def test(d):
  logs=log.splitlines(); skipped=[l for l in logs if l.startswith('EROARE '+d.name+':')]
  files=(d/'compileaza.txt').read_text().splitlines()
  cl=d/'cls';cl.mkdir()
  ret={'id':d.name,'rule':(d/'regula.txt').read_text(encoding='utf8').strip(),'mutated_paths':files,'changes':[{'file':f,'base_blob':r.bo((plug/f).read_bytes()),'mutated_blob':r.bo((d/f).read_bytes())} for f in files],'generator_errors':skipped}
  if skipped:return {**ret,'verdict':'UNAPPLIED_ANCHOR'}
  mutated=[d/f for f in files if f.endswith('.java')]
  if mutated:
   rb,dev=exe([r.jd/'javac.exe','--release','17','-encoding','UTF-8','-cp',basecp,'-d',cl,*mutated],d,50)
   if rb:return {**ret,'verdict':'COMPILE_BLOCK','detail':dev.splitlines()[:6]}
  cp=';'.join(map(str,[cl,tests,plug/'src',basecp]))
  try:rx,l=exe([r.jd/'java.exe','-Djava.security.manager','-Djava.security.policy=='+r.pol.as_posix(),'-Dstdout.encoding=UTF-8','-Dline.separator=\n','-cp',cp,'TestT163ArticoleDiverse'],d)
  except sp.TimeoutExpired:return {**ret,'verdict':'TIMEOUT'}
  fail=[s.strip() for s in l.splitlines() if re.match(r'^\s*FAIL\s',s)]
  ref=out/(rev[:10]+'-'+d.name+'.log');ref.write_text(l,encoding='utf8')
  verdict='BASE_GREEN' if d.name=='orig' and rx==0 else 'BASE_RED' if d.name=='orig' else 'KILLED' if rx!=0 and fail else 'SURVIVES' if rx==0 else 'HARNESS_FAIL'
  return {**ret,'verdict':verdict,'rc':rx,'fails':fail[:3],'proof':ref.name,'sha256':r.sha(ref)}
 with concurrent.futures.ThreadPoolExecutor(2) as pool:
  for v in pool.map(test,ids):
   spec['mutants'].append(v);r.dump(out/(rev[:10]+'.json'),spec)
 print(rev,{k:sum(x['verdict']==k for x in spec['mutants']) for k in sorted(set(x['verdict'] for x in spec['mutants']))},flush=True)
