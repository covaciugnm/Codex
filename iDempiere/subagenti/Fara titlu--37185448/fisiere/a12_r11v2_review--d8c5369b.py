from a12_r11v2_tasklinks import *
reviewcases=[];reviews=[]
map_by_case={'A06.GIT.1':[cont+'src/com/eva/ro/contab/corelare/ValideazaComenzi.java',cont+'src/com/eva/ro/contab/corelare/ValidareComanda.java'],
'A06.GIT.2':[cont+'src/com/eva/ro/contab/corelare/ValideazaComenzi.java',cont+'src/com/eva/ro/contab/corelare/DetaliuComanda.java'],
'A06.GIT.3':[cont+'src/com/eva/ro/contab/corelare/PreiaDinSite.java'],
'XSD.D101-D112':['idempiere/anaf-schemas/xsd/d101_20250214.xsd','idempiere/anaf-schemas/xsd/d112_10102024.xsd'],
'A01.F01':['frontend/app.py'],'A01.F02-O03-O04':['frontend/app.py','proxy/dynamic/_erp-admin-blocat.yml'],
'A12.T201/T232/T171':[cont+'test/TestT201Registre.java',cont+'test/TestComparatieSaga.java','idempiere/plugins/com.eva.ro.saga.native/test/TestT232GardaConsola.java']}
for i in range(1,4):
 sf=O/f'A11/Sigiliu_A11_R11_lot_0{i}_v1.json';j=source(sf);reviews.append(ref(sf));print('seal',i,j)
 verdict=O/f'A11/Verdict_A11_R11_lot_0{i}_v1.json';j=source(verdict);hash=sha(verdict)
 # Independent conclusions use an explicit existing file path. The reviewer decides scope, never the grade of the product.
 conc=j['concluzii']if 'concluzii'in j else[j]
 for k,c in enumerate(conc):
  cid=c.get('id','A05.G2.BOM.CONCURRENCY');pl=map_by_case.get(cid,[])
  if 'sursa'in c:
   pl=[re.sub(r':\d.*$','',p)for p in c['sursa']]
  if i==3:pl=[cont+'src/com/eva/ro/contab/wms/NotaSetWms.java',cont+'src/com/eva/ro/contab/wms/StocWms.java',cont+'src/com/eva/ro/contab/component/EvaNotaSetBomEvents.java']
  exists=[p for p in dict.fromkeys(pl)if p in R];missing=[p for p in pl if p not in R]
  pr={**ref(verdict),'pointer':'/concluzii/'+str(k)if 'concluzii'in j else''};row={'case':cid,'independent_verdict':pr,'files':exists,'unresolved_paths':missing,'disposition':c.get('verdict',c.get('decizie')),'limit':c.get('limita',c.get('frontiera',c.get('urmator'))),'next':c.get('urmator',c.get('retur',c.get('receptie_urmatoare'))),'scope':'Recepție parțială; zero extindere implicită la task.'};reviewcases.append(row)
  for p in exists:
   R[p].setdefault('independent_reviews',[]).append(row)
 if 'dovezi_verificate'in j or'dovezi'in j:
  for p,h in j.get('dovezi_verificate',j.get('dovezi',{})).items():
   q=O/p
   # immutable review input validation at read-time
   assert q.exists()and sha(q)==h,(p,h)
# T234 has a suggested association, authority remains unresolved.
unassigned.append({'case':'A09.BOOTSTRAP','proof':evidence('A09/Raport_A09_R11.json',''),'disposition':'A09 propune T234/P01.C13.T0003 ca context. Legătura la criteriul original trebuie verificată semantic înaintea oricărui credit de task.','whole_task_credit':False})
if __name__=='__main__':print('reviewcase',len(reviewcases),'tasklinks',len(links))

