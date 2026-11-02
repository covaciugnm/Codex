from a12_r10_publish import *
p=E/'R10_pregatire/A07_T216/T216_raport.json';d=rd(p);affected=[]
for i,v in enumerate(d['criteria']):
 c=v['id'];a=r9[c]['R9'];der=v['r9_reference_status']
 if a!=der:affected.append({'criterion':c,'A07_encoded_historical_reference':der,'effective_immutable_R9':a,'primary_file':S(R9/'taskuri/Fisa_T216.json'),'A07_row_pointer':'/criteria/'+str(i),'current_A07_claim_unchanged':v['r10_scope']})
f=P10/'T216_metadate_R9_corectate.json';wr(f,{'utc':now(),'R9_manifest':S(R9/'MANIFEST_R9.json'),'A07':S(p),'differences':affected,'interpretation':'Citirea istorică folosește fișa R9 sigilată. Expresiile actuale din criteriile A07 rămân conforme cu precondiția neîndeplinită și limitele publicate.'});print(sha(f),[x['criterion']for x in affected])
