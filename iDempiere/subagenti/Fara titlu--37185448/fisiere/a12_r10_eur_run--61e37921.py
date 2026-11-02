from a12_r10_lease import *
w=current();xx=Path(__file__).parent/'a12_r10_eur_worker.py';q=ssh('cat > '+w+'/eur-worker.py',xx.read_bytes());q.check_returncode();q=ssh('cd '+w+' && python3 eur-worker.py >eur-worker-log 2>&1',timeout=180);res=ssh('cd '+w+' && tail -10 eur-worker-log');print(q.returncode,res.stdout.decode('utf8','replace')[-500:])
fj=ssh('cat '+w+'/eur-result.json');f=P10/'T06_EUR_sans_SumaVal.json';f.write_bytes(fj.stdout);print(sha(f))
