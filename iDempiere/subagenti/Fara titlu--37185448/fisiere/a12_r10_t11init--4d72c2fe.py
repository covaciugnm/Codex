from a12_r10_base import *
from a12_r8_arch_survs import a,txt
for v in a:
 if '/T11-'in v['file']and re.search(r'/(1\d|2\d|3\d|4\d|5\d)_|T11.*(mergetree|R-13|R-03)',v['file']):
  st=txt(v);ls=st.splitlines();hits=[(i+1,s[:185])for i,s in enumerate(ls)if re.search(r'((baza|bază|vârf|REV|HEAD|master).{0,12}[0-9a-f]{8,40}\b|R-0?3.{0,45}(AD|dicționar)|R-13.{0,40}jar)',s,re.I)]
  if hits:print(v['file'],hits[:3])

