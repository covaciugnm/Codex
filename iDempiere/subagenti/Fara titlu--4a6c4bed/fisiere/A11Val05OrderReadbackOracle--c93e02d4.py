import pathlib,json,hashlib,datetime,decimal
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';L=B/'A05_Comanda_rezervare_lot05';O=B/'A11/Val05_loturi'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
checks=[]
def ck(n,b):checks.append({'check':n,'ok':bool(b)});assert b,n
def num(v):return decimal.Decimal(str(v or 0))
expected=[('native_order_A_v2.readback_01_fixture.json',None,0,0),('native_order_A_v2.readback_02_draft_committed.json','DR',0,0),('native_order_A_v2.readback_03_O01_prepare_before_commit.json','DR',0,0),('native_order_A_v2.readback_04_O01_prepare_committed.json','IP',2,1),('native_order_A_v3.readback_01_O01_continue_IP.json','IP',2,1),('native_order_A_v3.readback_02_O01_complete_before_commit.json','IP',2,1),('native_order_A_v3.readback_03_O01_complete_committed.json','CO',2,1),('native_order_A_v3.readback_04_fixture.json',None,0,0),('native_order_A_v3.readback_05_draft_committed.json','DR',0,0),('native_order_A_v3.readback_06_O02_first_before_commit.json','DR',0,0),('native_order_A_v3.readback_07_O02_first_rolled_back.json','DR',0,0),('native_order_A_v3.readback_08_O02_retry_before_commit.json','DR',0,0),('native_order_A_v3.readback_09_O02_retry_committed.json','CO',2,1),('native_order_A_v3.readback_10_O03_void_before_commit.json','CO',2,1),('native_order_A_v3.readback_11_O03_void_committed.json','VO',0,2)]
summary=[];data={}
for name,state,qty,nlogs in expected:
 p=L/name;a=j(p);data[name]=a;r=a['rows'];ids=a['ids'];label=a['case']+'/'+a['tag'];orders=r['orders'];lines=r['orderlines'];logs=r['reservation_logs'];res=r['reservations']
 ck(label+' readonly',a['session']['readonly']=='on' and a['session']['isolation']=='read committed')
 ck(label+' state',[x['docstatus'] for x in orders]==([] if state is None else [state]))
 ck(label+' stock10',sum(num(x['qtyonhand']) for x in r['stock'])==10)
 ck(label+' SO/PO',sum(num(x['qty']) for x in res if x['issotrx']=='Y')==qty and not [x for x in res if x['issotrx']=='N'])
 ck(label+' logs',len(logs)==nlogs and sum(num(x['deltaqty']) for x in logs)==qty)
 ck(label+' no deliveries/invoices',all(not r[k] for k in ['inouts','inoutlines','confirmations','confirmationlines','invoices','invoice_lines','inoutline_ma']))
 ck(label+' no quantity/cost movements',not r['transactions'] and not r['cost_details'])
 ck(label+' limited facts',not r['facts'] and a['session']['global_facts']==308)
 ck(label+' site absent',not r['site'] and not r['site_lines'])
 for rows in [r['product'],r['warehouse'],r['source'],orders,lines,res,logs]:
  ck(label+' ownership set '+str(len(checks)),all(x['ad_client_id']==11 and x['ad_org_id']==11 for x in rows))
 for x in lines:
  ck(label+' line quantities',num(x['qtyreserved'])==qty and num(x['qtydelivered'])==num(x['qtyinvoiced'])==0)
  ck(label+' line links',x['c_order_id']==orders[0]['c_order_id'] and x['m_product_id']==ids['product'] and x['m_warehouse_id']==ids['warehouse'])
 for x in logs:
  line=next(z for z in lines if z['c_orderline_id']==x['record_id']);order=next(z for z in orders if z['c_order_id']==line['c_order_id'])
  ck(label+' trace arithmetic '+str(x['m_storagereservationlog_id']),num(x['oldqty'])+num(x['deltaqty'])==num(x['newqty']))
  ck(label+' trace link '+str(x['m_storagereservationlog_id']),x['ad_table_id']==260 and x['documentno']==order['documentno'] and x['lineno']==line['line'] and x['m_product_id']==ids['product'] and x['m_warehouse_id']==ids['warehouse'] and x['issotrx']=='Y' and x['m_attributesetinstance_id']==0)
 if qty==0 and nlogs==0:ck(label+' no new reservation row',not res)
 summary.append({'evidence':ref(p),'scenario_context':a['case'],'checkpoint':a['tag'],'state':state,'reserved':qty,'reservation_rows':len(res),'trace_rows':nlogs,'posted':[x['posted'] for x in orders],'docaction':[x['docaction'] for x in orders],'stock':10,'external_reader_pid':a['session']['pid']})
dr=data['native_order_A_v3.readback_05_draft_committed.json']['rows'];rb=data['native_order_A_v3.readback_07_O02_first_rolled_back.json']['rows']
for k in ['orders','orderlines','reservations','reservation_logs','stock','inouts','facts']:ck('O02 rollback exact '+k,dr[k]==rb[k])
ip=data['native_order_A_v2.readback_04_O01_prepare_committed.json']['rows'];co=data['native_order_A_v3.readback_03_O01_complete_committed.json']['rows'];ck('O01 sans double reservation',ip['reservations']==co['reservations'] and ip['reservation_logs']==co['reservation_logs'])
vo=data['native_order_A_v3.readback_11_O03_void_committed.json']['rows'];ck('O03 exact deltas',sorted(num(x['deltaqty']) for x in vo['reservation_logs'])==[-2,2]);ck('O03 zero row retained',len(vo['reservations'])==1 and num(vo['reservations'][0]['qty'])==0)
out={'schema':'A11.R12.Val05.order.readback.oracle.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','decision':'CONTRAORACOL READBACK A CONFORM PENTRU O01/O02/O03; RECEPȚIA FINALĂ A LOTULUI RĂMÂNE SEPARATĂ.','method':'Lectură și recalcul propriu pe rândurile externe arhivate, fără importul funcțiilor executorului, fără conexiune DB nouă și fără repetarea celor trei scenarii. Acestea sunt 15 checkpointuri, nu 15 scenarii.','checks':checks,'checkpoints':summary,'accepted_observations':['O01: DR/SO0 extern înainte de Prepare commit, apoi IP/SO2/log +2; Complete după selectarea acțiunii CO păstrează exact rezerva și logul.','O02: readback după rollback egal cu draftul pentru rândurile comparate; retry produce CO/SO2 și o singură urmă nativă +2.','O03: extern înainte de commit încă CO/SO2; după commit VO/SO0, rândul de rezervare rămâne cu zero și jurnalul are +2/−2.','Jurnalul se leagă de C_OrderLine prin tabel260/Record_ID/DocumentNo/LineNo și aceeași identitate client/org/product/warehouse/ASI.'],'limits':['Familia A nu conține linie site, generator, UI/login sau proces AD.','A selectează DocAction prin setter nativ; nu modifică DocStatus/Processed. Generatorul B rămâne original și nu primește această intervenție.','Doc.postImmediate a rulat efectiv pentru C_Order în core13. Posted=Y și Fact_Acct gol pe produs nu sunt validare contabilă.','Facts din aceste 15 capturi sunt filtrate pe produs și au contor global308; nu demonstrează singure lipsa modificărilor altor rânduri. Comparația globală și legăturile pe document se vor primi aditiv.','Readback-urile sunt conexiunea separată a executorului. Acest contraoracol A11 este recalcul independent al dovezilor, nu o a doua execuție nativă a scenariilor.','Data fixturei 2006-12-15 aparține perioadei seed; nu validează perioada operațională 2026.','Nu postări valorice, costuri G1, stoc contabil G2, idempotență după succes comis sau conservare pentru seturi complexe.'],'new_scenarios':0,'new_product_executions':0,'product_score':None,'whole_acceptance':False}
for c in checks:c['check']=c['check'].replace('sans double reservation','fără rezervare dublă')
op=O/'Contraoracol_A11_comenzi_A_v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');rp=O/'Runner_A11_comenzi_A_v1.py';assert not rp.exists();rp.write_bytes(pathlib.Path(__file__).read_bytes());sp=O/'SIGILIU_A11_comenzi_A_v1.json';assert not sp.exists();sp.write_text(json.dumps({'utc':out['utc'],'files':[ref(op),ref(rp)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'verdict':ref(op),'seal':ref(sp),'checks':len(checks)},ensure_ascii=False))
