from a12_r10_lease import *
w=current();p=ssh('cd '+w+' && test -e bank-worker-stderr && tail -6 bank-worker-stderr');print(p.returncode,p.stdout.decode('utf8','replace')[-750:])
