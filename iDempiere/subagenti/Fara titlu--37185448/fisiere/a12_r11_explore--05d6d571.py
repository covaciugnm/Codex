from a12_r10_publish import *
P=E/'R11_plan_delta'; prev=rd(B/'capturi/MANIFEST.json');print('files',str(prev['files'])[:510])
for name in ['Inventar_P01.json','A12_plan_taskuri.json','Matrice_interfete.json','Plan_director.json','Manifest_plan.json','A11_verdict_plan.json','A03_plan.json','A04_plan.json','A05_plan.json','A07_plan.json','A08_plan.json']:
 p=B/name;d=rd(p);print(name,type(d).__name__,list(d)[:11]if isinstance(d,dict)else'', )
for f in ['00_STATUS_TASKURI.json','00_CORESPONDENTA_COD_CAPITOL.json','00_STARI_TASKURI.json','00_STATUS_FINALIZATE.json','00_CAPITOLE_PROIECTE.json','00_STATUS_RAMASE.json']:
 d=rd(B/'capturi'/f);q=d[0]if isinstance(d,list)else next(iter(d.values()));print(f,(list(d)[:6]if isinstance(d,dict)else[len(d)]),str(q)[:230])
d=rd(B/'Inventar_P01.json');print('INVKEYS',list(d));e=rd(E/'A11_control_A12_R10.json');print('R10 audit',list(e),{k:v for k,v in e.items()if isinstance(v,(float,int,str))and k in ['score','decision','quality_score','audit_quality_score','result']})
for n in ['A03','A04','A05','A07','A08']:
 d=rd(B/(n+'_plan.json'))
 for k,v in d.items():
  if 'pipeline'in k.lower()or 'check' in k.lower():print(n,k,str(v[0])[:330]if isinstance(v,list)and v else list(v)[:4]if isinstance(v,dict)else str(v)[:65])

