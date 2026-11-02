from a12_r9_orig import *
from collections import Counter,defaultdict
R9=E/'R9';P10=E/'R10_pregatire/A12';P10.mkdir(parents=True,exist_ok=True);r9reg=rd(R9/'Registru_reexecutare_R9.json')['rows'];r9={r['criterion']:r for r in r9reg};plan9=rd(P9/'Repartizare_177_R9.json');p177={w['criterion']:w for w in plan9['assigned_cases']};pr8={w['criterion']:w for w in r8};missing=[z for z in r9reg if z['R9']=='NEEXECUTAT'];f164=[z for z in missing if z['cohorts']['earlier_177']];nw873=[z for z in missing if z['cohorts']['without_oracle_R8_882']];his167=[z for z in missing if not z['cohorts']['earlier_177']and not z['cohorts']['without_oracle_R8_882']];assert(len(f164),len(nw873),len(his167))==(164,873,167);A11=rd(E/'A11_control_A12_R9.json')
if __name__=='__main__':
 print(Counter(z['owner']for z in f164));print([(z['criterion'],z['text'][:83])for z in f164 if z['owner']in ['A07','A04','A09','A06']]);print([(z['criterion'],z['text'][:75])for z in nw873 if z['task'].startswith(('T04.','T22.','T35.'))][:22])

