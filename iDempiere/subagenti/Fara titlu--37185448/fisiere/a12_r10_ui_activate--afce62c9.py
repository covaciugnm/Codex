from a12_r10_lease import *
import sys
assert sys.argv[1]in ['prepare','restore'];w=current();f=Path(__file__).parent/'a12_r10_ui_config.py';qq=ssh('cat > '+w+'/ui-config.py',f.read_bytes());qq.check_returncode();q=ssh('cd '+w+' && python3 ui-config.py '+sys.argv[1]);print(q.returncode,q.stdout.decode('utf8','replace'),q.stderr.decode('utf8','replace')[-350:]);q.check_returncode()
