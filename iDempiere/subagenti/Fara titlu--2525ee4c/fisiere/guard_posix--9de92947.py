from lab import *
import tempfile,tarfile
tar=W/'guard_input.tgz'
with tempfile.TemporaryDirectory(dir=W,prefix='guard-R8-') as name:
 tgt=pathlib.Path(name)
 with tarfile.open(tar) as ar:
  for item in ar:
   p=tgt/item.name;assert not pathlib.PurePosixPath(item.name).is_absolute() and tgt in p.resolve().parents and item.isfile()
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(ar.extractfile(item).read())
 script=tgt/'tools/teste/garda_parteneri_scriere.py'; assert digest(script.read_bytes())==digest((W/'guard_original.py').read_bytes())
 proc=subprocess.run(['python3','-I',str(script)],cwd=tgt,capture_output=True,text=True,timeout=150)
 lines=proc.stdout.splitlines();summary=next(x for x in lines if x.startswith('garda_parteneri_scriere:'))
 save('guard_posix.json',{'rev':'6df998aee0e514d30856c461962afe99ebd0d113','utc':now(),'script_sha256':digest(script.read_bytes()),'tar_sha256':digest(tar.read_bytes()),'n_input_files':sum(p.is_file() for p in tgt.rglob('*')),'rc':proc.returncode,'summary':summary,'output_sha256':digest(proc.stdout.encode()),'scope':'Exact archive of tracked data/code extensions covered by original scanner, default POSIX invocation, no external request or allowlist edits.'})
