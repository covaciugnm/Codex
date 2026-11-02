from a12_r10_lease import *
w=current();pr=ssh('cd '+w+' && cat supervisor-log|tail -7 && test ! -e ready || echo READY_SIGNAL');print(pr.stdout.decode()[-800:])

