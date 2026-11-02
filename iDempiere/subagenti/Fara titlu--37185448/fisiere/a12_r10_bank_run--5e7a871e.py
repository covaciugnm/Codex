from a12_r10_lease import *
import shutil
worker=Path(__file__).parent/'a12_r10_native_worker.py';w=current();q=ssh('cat > '+w+'/bank-worker.py',worker.read_bytes());q.check_returncode()
if __name__=='__main__':
 ex=ssh('cd '+w+' && test -e ready && python3 bank-worker.py >bank-worker-stdout 2>bank-worker-stderr',timeout=270)
 if ex.returncode:
  r=ssh('cd '+w+' && tail -12 bank-worker-stderr');print(r.stdout.decode('utf8','replace')[-1000:]);print('rc',ex.returncode)
 else:
  data=ssh('cat '+w+'/bank-result.json').stdout;p=P10/'T06_comparator_10conturi_168.json';p.write_bytes(data);print(sha(p),[(z['label'],z['native'])for z in json.loads(data)['attempts']])

