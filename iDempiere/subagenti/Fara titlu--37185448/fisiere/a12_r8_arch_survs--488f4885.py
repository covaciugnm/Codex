from a12_r8_arch import *
a=rd(pool/'index.json')
def txt(r):return gzip.decompress(Path(r['storage']).read_bytes()).decode('utf8','replace')
def search(task,pattern):
 return [r for r in a if re.search('/'+task+'[^/]*/',r['file'],re.I)and re.search(pattern,r['file'].split('/')[-1],re.I)]
def show(task,pattern):
 rr=search(task,pattern);print(task,pattern,'count',len(rr));print('\n'.join(x['file'].split('/',3)[-1] for x in rr[-95:]))
if __name__=='__main__':
 for t,pat in [('T06-',r'K-|^C[0-9-]|tinte|rezult|_verdict|_log|reprob'),('T201-',r'K-?0?[0-9]|K-1[5]|K-20|K-2[2459]|K-29|verdict|autoaudit'),('T204-',r'C[-_]|PB01|verdict'),('T220-',r'k12|pas0|reprodus|auto.audit|garda|registru|slot'),('T224-',r'K-?[0-9]|G-00|G00|21.comit|verdict'),('T227-',r'K-|K[0-9]|audit.*final|predare|^00_|verdict'),('T314-',r'K2[0-9]|K-|t0_lr4|verdict')]:
  show(t,pat)

