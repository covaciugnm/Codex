import pathlib,json,hashlib,re,datetime,decimal
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
G=R/'executie/R12_fisiere/A05_G3_nativ_lot04';O=R/'executie/R12_fisiere/A11/Val04_loturi'
D=decimal.Decimal
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
checks=[]
def ck(n,b,detail=None):
 checks.append({'check':n,'ok':bool(b),'detail':detail})
 assert b,(n,detail)
snapshots={};numeric=[];case_lines=[]
for v in [2,3]:
 m=j(G/f'business_g3_v{v}.json');text=(G/f'business_g3_v{v}.stdout.txt').read_text(encoding='utf-8-sig')
 ck(f'v{v} harness identity',all(sha(G/f'business_g3_v{v}.{n}')==h for n,h in m['sources'].items()))
 for r in m['readbacks']:
  p=G/r['path'];ck('readback SHA '+p.name,sha(p)==r['sha256']);x=j(p)
  ck('readonly '+p.name,x['read_only'] is True and x['rows']['session'][0]['readonly']=='on')
  ck('fresh handshake '+p.name,f"PYTHON_READBACK_ACK|{x['token']}|{x['tag']}|{x['case']}" in text)
  snapshots[(v,x['case'])]=(p,x)
 for line in text.splitlines():
  if line.startswith('CASE_G3|'):
   pieces=line.split('|');values=dict(t.split('=',1) for t in pieces[2:] if '=' in t);case=pieces[1]
   case_lines.append({'version':v,'case':case,'values':values})
   if 'nativeAvailable' not in values or (v,case) not in snapshots:continue
   p,x=snapshots[(v,case)];rows=x['rows'];reservations=rows['reservation'];stock=rows['stock']
   ck('ownership '+case,all(int(z['ad_client_id'])==11 and int(z['m_product_id'])==x['product'] and int(z['m_warehouse_id'])==x['warehouse'] for z in reservations+stock))
   native_stock=sum((D(z['qtyonhand']) for z in stock if z['eligible']=='Y'),D(0))
   all_stock=sum((D(z['qtyonhand']) for z in stock),D(0))
   so=sum((D(z['qty']) for z in reservations if z['issotrx']=='Y'),D(0));po=sum((D(z['qty']) for z in reservations if z['issotrx']=='N'),D(0))
   active=sum((D(z['qty']) for z in reservations if z['isactive']=='Y'),D(0))
   active_so=sum((D(z['qty']) for z in reservations if z['isactive']=='Y' and z['issotrx']=='Y'),D(0))
   native=native_stock-so;eva=all_stock-active;fisa=max(D(0),eva).to_integral_value(rounding=decimal.ROUND_FLOOR)
   expected={'SO':so,'PO':po,'nativeAvailable':native,'EVAreserved':active,'RezervareStoc':eva,'FisaCanal':fisa}
   ck('independent sums '+case,all(D(values[k])==v for k,v in expected.items()),{'expected':{k:str(v) for k,v in expected.items()},'observed':values})
   a=rows['auxiliary'][0];ck('zero other terms '+case,a['site_rows']==a['order_lines']==a['fixture_facts']==0 and a['global_fact_count']==308)
   ck('source ownership and reserve '+case,len(rows['source'])==1 and int(rows['source'][0]['ad_client_id'])==11 and D(rows['source'][0]['eva_stocrezerva'])==0)
   numeric.append({'case':case,'version':v,'raw_readback':ref(p),'expected_from_raw':{k:str(v) for k,v in expected.items()},'SO_only_with_active_policy':str(all_stock-active_so),'kind':'characterization of policy differences' if 'inactive' in case.lower() else 'arithmetic reconciliation of native and EVA readers'})
# The critical metamorphic sequence changes only PO, preserving the exact same SO UUID, quantity and stock.
seq=[snapshots[(2,k)] for k in ['G3-S01','G3-C01','G3-C02']]
def so_rows(x):return [r for r in x['rows']['reservation'] if r['issotrx']=='Y']
ck('SO unchanged across critical sequence',so_rows(seq[0][1])==so_rows(seq[1][1])==so_rows(seq[2][1]))
ck('stock unchanged across critical sequence',seq[0][1]['rows']['stock']==seq[1][1]['rows']['stock']==seq[2][1]['rows']['stock'])
ck('PO alone changes 0 5 15',[sum((D(r['qty']) for r in x['rows']['reservation'] if r['issotrx']=='N'),D(0)) for p,x in seq]==[D(0),D(5),D(15)])
# Disentangle product and warehouse sentinels rather than treating a two-coordinate change as two independent controls.
target=snapshots[(3,'G3-F01-product-isolated')][1];prod=snapshots[(3,'G3-F01-product-sentinel')][1];wh=snapshots[(2,'sameP_otherWarehouse')][1]
ck('product isolated',target['warehouse']==prod['warehouse'] and target['product']!=prod['product'] and any(D(z['qty'])>0 for z in prod['rows']['reservation']))
ck('warehouse isolated',target['warehouse']!=wh['warehouse'] and target['product']==wh['product'] and any(D(z['qty'])>0 for z in wh['rows']['reservation']))
# The new-PO flag is already durable before the reader call. This is a reader-policy fixture, not commercial editing permission.
for pre,post in [('G3-F03-POinactive-before-read','G3-F03-POinactive-newPO'),('G3-F03-bothInactive-before-read','G3-F03-bothInactive-newPO')]:
 a=snapshots[(3,pre)][1];b=snapshots[(3,post)][1]
 ck('inactive persisted before read '+post,a['rows']['reservation']==b['rows']['reservation'] and any(z['isactive']=='N' for z in a['rows']['reservation']))
# Rollback must remove the row, not merely leave a zero balance.
before=snapshots[(3,'before_rollback_invisible')][1];after=snapshots[(3,'G3-R01-rollback')][1];retry=snapshots[(3,'G3-R01-retry')][1]
ck('rollback external PO row absent',all(not any(z['issotrx']=='N' for z in x['rows']['reservation']) for x in [before,after]))
ck('retry one PO row Qty5',len([z for z in retry['rows']['reservation'] if z['issotrx']=='N'])==1 and sum((D(z['qty']) for z in retry['rows']['reservation'] if z['issotrx']=='N'),D(0))==5)
txt=(G/'business_g3_v3.stdout.txt').read_text(encoding='utf-8-sig');bar=re.search(r'ROLLBACK_BARRIER\|(\d+)\|xid=(\d+)\|isolation=read committed\|trx=([^|]+)\|newPOuuid=([^\r\n]+)',txt)
ck('independent rollback connection',bool(bar) and before['rows']['session'][0]['pg_backend_pid']!=int(bar[1]))
ck('retry UUID differs from rolled back row',bar[4] not in [z['m_storagereservation_uu'] for z in retry['rows']['reservation']])
# ASI rollup versus native specific-lot reads; all are the same physical reservation population.
lot=snapshots[(3,'G3-F04-ASIall')][1];asis=sorted({int(z['m_attributesetinstance_id']) for z in lot['rows']['stock']});lot_out=[]
for asi in asis:
 st=sum((D(z['qtyonhand']) for z in lot['rows']['stock'] if int(z['m_attributesetinstance_id'])==asi),D(0));so=sum((D(z['qty']) for z in lot['rows']['reservation'] if int(z['m_attributesetinstance_id'])==asi and z['issotrx']=='Y'),D(0));lot_out.append({'ASI':asi,'stock':str(st),'SO':str(so),'native_available':str(st-so)})
ck('two ASI 5 and3',len(asis)==2 and [D(z['native_available']) for z in lot_out]==[D(5),D(3)])
specific=next(c for c in case_lines if c['case']=='G3-F04-ASIspecific')['values'];ck('native specific log matches independent raw',int(specific['ASI1'])==asis[0] and int(specific['ASI2'])==asis[1] and D(specific['available1'])==5 and D(specific['available2'])==3)
norm=snapshots[(3,'G3-F04-normalize')][1];ck('no-attribute normalization persisted',all(int(z['m_attributesetinstance_id'])==0 for z in norm['rows']['reservation']) and norm['rows']['product'][0]['m_attributeset_id']=='0')
ck('newPO gate precedes continuation',j(R/'executie/R12_fisiere/A11/Val04_preflight/Addendum_A11_G3_F03_F01_v1.json')['utc']<j(G/'business_g3_v3.json')['utc'])
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'A11 independent','method':'Recalculare proprie Decimal pe rândurile brute recitite din PG prin conexiunile readonly ale executorului. Fără copierea SQL-ului EVA, fără rerulare a produsului sau acces la laborator. Captura rămâne a executorului; oracolul numeric și reconcilierea sunt A11.','snapshots_verified':sum(len(j(G/f'business_g3_v{v}.json')['readbacks']) for v in [2,3]),'numeric_checkpoint_comparisons':len(numeric),'numeric':numeric,'ASI_counteroracle':lot_out,'checks':checks,'accepted_finding':'R12-STOC-SO-PO-01: aceeași rezervare SO și același stoc, numai PO schimbat; nativ 8/8/8, EVA 8/3/-7, fișa 8/3/0. Extindere nativă a constatării SQL existente, nu defect nou.','limits':['Nu reprezintă o nouă execuție independentă a JVM sau o recitire A11 a bazei.','F03 caracterizează diferența de politică IsActive; nu justifică substituția oarbă cu getQty nativ.','Retry după rollback nu demonstrează idempotența după commit.','F02 este limită de parametru client și ownership al fixturei, nu autentificare ori RBAC.','Numărătorul comparațiilor nu înseamnă scenarii unice de produs și nu se adună la cele 10 scenarii executor.']}
p=O/'Contraoracol_A11_G3_readback_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'output':ref(p),'checks':len(checks),'numeric':len(numeric)}))
