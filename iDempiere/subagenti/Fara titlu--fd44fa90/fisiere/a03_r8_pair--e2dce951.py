from a03_r8_jvm import *
import io,tarfile,collections
def go():
 p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab';d=work/'pair186';d.mkdir(exist_ok=True);detpath=path('T186','dovezi-20-plan/detector_catch_t186.py');det=d/'detector_catch_t186.py';det.write_bytes(get(detpath));iv=path('T186','20a_inventar.tsv');inv=get(iv);source=plug/'test/TestT186CatchGoale.java';comp=sp.run([jdk/'javac.exe','-encoding','UTF-8','-d',d,source],capture_output=True);assert comp.returncode==0,comp.stderr
 ins={(r[0],int(r[1])) for x in inv.decode().splitlines() if (r:=x.split('\t')) and len(r)>1 and r[1].isdigit()};ss=[]
 for label,rev in [('arhiva_ante_implementare','1b9a18466d'),('integrare_task','57f8d6836c4'),('curent',sha)]:
  r=ssh('cd '+repo+' && git archive '+rev+' -- '+p);assert r.returncode==0,r.stderr;target=d/label;target.mkdir(exist_ok=True)
  with tarfile.open(fileobj=io.BytesIO(r.stdout),mode='r:') as ar:
   for m in ar:
    if not m.isfile() or not m.name.startswith(p+'/') or not m.name.endswith('.java'):continue
    f=target/m.name[len(p)+1:];assert f.resolve().is_relative_to(target.resolve());f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(ar.extractfile(m).read())
  jr=sp.run([jdk/'java.exe','-Xmx512m','-Dstdout.encoding=UTF-8','-cp',d,'TestT186CatchGoale','--raport',target],cwd=work,capture_output=True,timeout=75);py=sp.run([sys.executable,'-I','-X','utf8',det,target,'--tsv'],cwd=work,capture_output=True,timeout=75)
  parse=lambda b:{(a[0].replace('\\','/'),int(a[1])) for l in b.decode('utf8',errors='replace').splitlines() if len(a:=l.split('\t'))>=2 and a[1].isdigit()}
  j0=parse(jr.stdout);p0=parse(py.stdout);diff=sorted(j0^p0)
  ss.append({'scope':label,'revision':ssh('cd '+repo+' && git rev-parse '+rev).stdout.decode().strip(),'archive_sha256':H(r.stdout),'java_source_sha256':H(source.read_bytes()),'detector_sha256':H(det.read_bytes()),'java_rc':jr.returncode,'py_rc':py.returncode,'java_n':len(j0),'py_n':len(p0),'symmetric_difference':len(diff),'first_difference':diff[:8],'original_inventory_n':len(ins),'inventory_vs_py_delta':len(ins^p0),'java_output_sha256':H(jr.stdout),'py_output_sha256':H(py.stdout),'diagnostic':(jr.stderr+py.stderr).decode('utf8',errors='replace')[:320]});print(label,ss[-1]['java_n'],ss[-1]['py_n'],len(diff),ss[-1]['inventory_vs_py_delta'],flush=True)
 J(out/'T186_detectori_independenti.json',{'utc':UTC(),'sha':sha,'inventory_at_current_sha256':H(inv),'results':ss})
if __name__=='__main__':go()

