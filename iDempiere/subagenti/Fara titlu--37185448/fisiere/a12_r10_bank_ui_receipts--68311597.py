from a12_r10_base import *
exec((Path(__file__).parent/'a12_r10_receipt.py').read_text(encoding='utf8').split("j=P10/")[0]);f=P10/'T06_UI/Rezultat.json';assert sha(f)=='090ba565629093ca34b866fec4b932b1d5833f229eaa514693441bdf747cb63c';d=rd(f);assert d['controls']['compared_cells']==4200 and d['controls']['different_cells']==0 and d['controls']['real_clicks']==2
for c,z in d['claims'].items():
 add(c,'ZK în browser, SQL și confirmarea pe aceeași origine',z['expected'],z['observed'],d['finding']if c.endswith('-022')else{'actual_real_clicks':2,'read_only_witness':'AD_PInstance 1003144 nu schimbă rândurile / hashul integral după 1003143.'},z['limit'],[jr(f,'/claims/'+c),jr(f,'/controls')]+([jr(f,'/finding')]if c.endswith('-022')else[]),'nominal_native_UI')
dest=P10/'Registru_SAGA_UI_A12.json';wr(dest,{'utc':now(),'fixed_head':BASE,'origin':jr(f),'receipts':out,'one_defect':jr(f,'/finding'),'returned':ab(P10/'T06_laborator_restituit.txt')});print(sha(dest),list(out))
