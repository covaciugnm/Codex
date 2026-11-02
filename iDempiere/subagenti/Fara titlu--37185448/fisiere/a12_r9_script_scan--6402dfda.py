from a12_r9_orig import *
from a12_r8_arch_survs import a,txt
for k,mask in [('T06-',r'bloc.*171|garda|11_test_bloc|40-audit.+bloc'),('T314-',r'criterii_statice|t0_lr4|inainte|K-26_q31'),('T204-',r't204_ferestre|garda'),('T224-',r'clasa.*mut|rezultat|10b.*garzi|G-00/rezultat'),('T220-',r'K-09|K-08|detectie_|retest|garzi')]:
 h=[z for z in a if '/'+k in z['file']and re.search(mask,z['file'].split('/',3)[-1],re.I)];print(k,[(z['file'].split('/',3)[-1],z['oid'])for z in h[:8]])
f=next(x for x in a if '/T06-'in x['file']and x['file'].endswith('scripturi/bloc_t171.py'));print(txt(f)[:2400])
f=next((x for x in a if '/T314-'in x['file']and x['file'].endswith('criterii_statice.sh')),None);print(txt(f)[:1200]if f else'none')

