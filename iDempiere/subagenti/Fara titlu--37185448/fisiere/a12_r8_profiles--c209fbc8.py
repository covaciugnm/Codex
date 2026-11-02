from a12_r8_arch_survs import *
for task,pattern in [('T227-',r'probe_|proba.*\.txt|mutanti.*res|\bK1|\bK2'),('T224-',r'21|tabel|comit|eliber|inten|autostop|registru'),('T220-',r'.*'),('T04-',r'.*')]:
 m=search(task,pattern);print('\n',task,len(m));print('\n'.join(x['file'].split('/',3)[-1] for x in m if ('/trei_rulari'not in x['file'] and not x['file'].endswith('.py')and not x['file'].endswith('.sh')))[-4500:])

