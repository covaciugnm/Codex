from a12_r10_base import *
from a12_r8_arch_survs import a,txt
for item in a:
 if re.search(r'/T171-|/T06[-/]',item['file'])and re.search(r'(10_spec|03_|livrare|valid|audit|verdict|merge|dOVezi-.*C-24)',item['file'],re.I):
  st=txt(item)
  if 'merge-tree'in st or 'git show'in st:
   for i,l in enumerate(st.splitlines(),1):
    if re.search(r'merge-tree|[0-9a-f]{8,40}.*jar|jar.*[a-f0-9]{10,40}',l,re.I):
     print(item['file'],i,l[:160])

