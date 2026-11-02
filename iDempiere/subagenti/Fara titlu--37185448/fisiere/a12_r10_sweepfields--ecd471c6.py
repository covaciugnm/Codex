from a12_r10_base import *
d=rd(E/'R10_pregatire/A05/T330_numitor_declarat.json')
print(type(d['classes']),[(k,len(v),str(list(v)[:4])[:180])for k,v in d['classes'].items()]if isinstance(d['classes'],dict)else d['classes'][:2])
for p in [E/'R5_pregatire/JVM/Executii_JVM_R5.json',E/'R5_pregatire/JVM/Calibrare_JVM_R5_2.json',E/'R5_pregatire/JVM/Calibrare_JVM_R5_3.json']:
 a=rd(p);print(p.name,list(a),list((a.get('runs')or a.get('attempts')or [{}])[0]),str((a.get('runs')or a.get('attempts')or [{}])[0].get('log',''))[:175])

