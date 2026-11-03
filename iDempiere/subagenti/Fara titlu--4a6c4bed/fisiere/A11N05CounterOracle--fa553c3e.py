import pathlib,json,hashlib,decimal,collections,re,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere');B=R/'A05_N05_lot03';O=R/'A11/Val03_loturi';D=decimal.Decimal
def ref(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(n):return json.loads((B/n).read_text(encoding='utf8'))
d=load('Readback_independent_final_v1.json')['rows'];pre=load('Readback_independent_dupa_business_v1.json')['rows'];log=(B/'business_v2.stdout.txt').read_text(encoding='utf8')
out=[]
for tag in ['serial','rollback','race']:
 products=[p for p in d['products'] if p['value'].startswith('N05_'+tag+'_')];assert len(products)==2
 piece=next(p for p in products if p['isbom']=='N');assembled=next(p for p in products if p['isbom']=='Y');pids={p['m_product_id'] for p in products}
 moves=[m for m in d['movements'] if m['m_product_id'] in pids];balances=collections.defaultdict(D)
 details=[]
 for m in moves:
  q=D(m['qty']);key=(m['m_product_id'],m['m_warehouse_id'])
  signed=q*(int(m['m_locatorto_id'] is not None)-int(m['m_locator_id'] is not None))
  balances[key]+=signed;details.append({'id':m['eva_miscarewms_id'],'product':m['m_product_id'],'type':m['eva_tipmiscarewms'],'signed_qty':str(signed),'record_id':m['record_id'],'table':m['ad_table_id']})
 stocks=[s for s in d['stock'] if s['m_product_id'] in pids];expected=collections.defaultdict(D)
 for s in stocks:expected[(s['m_product_id'],s['m_warehouse_id'])]+=D(s['qty'])
 assert balances==expected
 p=sum(q for (i,w),q in balances.items() if i==piece['m_product_id']);s=sum(q for (i,w),q in balances.items() if i==assembled['m_product_id']);initial=sum(D(m['qty']) for m in moves if m['eva_tipmiscarewms']=='ACTIVARE')
 consumed=sum(D(m['qty']) for m in moves if m['m_product_id']==piece['m_product_id'] and m['eva_tipmiscarewms']=='AMBALARE');restored=sum(D(m['qty']) for m in moves if m['m_product_id']==piece['m_product_id'] and m['eva_tipmiscarewms']=='DEZAMBALARE')
 conserved=p+s*D(2);assert (p,s)=={'serial':(D(10),D(0)),'rollback':(D(8),D(1)),'race':(D(11),D(0))}[tag]
 out.append({'fixture':tag,'piece':piece['m_product_id'],'set':assembled['m_product_id'],'identities_distinct':piece['m_product_id']!=assembled['m_product_id'],'journal_signed_rows':details,'ledger_recomputed_equals_stock':True,'initial_pieces':str(initial),'assembly_piece_debit':str(consumed),'disassembly_piece_credit':str(restored),'final_pieces':str(p),'final_sets':str(s),'initial_recipe_ratio':2,'equivalent_primary_units_at_original_recipe':str(conserved),'excess_over_initial':str(conserved-initial)})
serialpids={p['m_product_id'] for p in d['products'] if p['value'].startswith('N05_serial_')}
for k in ['stock','movements','native_stock']:
 before=[x for x in pre[k] if x['m_product_id'] in serialpids];after=[x for x in d[k] if x['m_product_id'] in serialpids];assert before==after
inst={i['ad_pinstance_id']:i for i in d['instances']};assert inst['1002649']['result']=='1';assert [m for m in d['movements'] if m['record_id']=='1002649']==[];assert len([m for m in d['movements'] if m['record_id']=='1002650'])==2
t1=re.search(r'COORDINATED_PROCESS\|tag=race\|.*?managedTrx=false\|(\d+)\|xid=(\d+)\|isolation=([^\r\n]+)',log).groups();t2=re.search(r'T2_START\|(\d+)\|xid=(\d+)\|isolation=([^|\r\n]+)',log).groups();assert t1[0]!=t2[0] and t1[1]!=t2[1] and t1[2]==t2[2]=='read committed'
assert log.index('barrier_T1_not_visible')<log.index('T2_START|')<log.index('T2_RESULT|COMMITTED_QTY3')<log.index('race_assembly_committed')<log.index('RACE_DEFECT_11_FROM_10')
assert d['native_facts']==[] and all(D(s['qtyonhand'])==10 for s in d['native_stock'])
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11','method':'Contraoracol propriu: reconstruirea independentă a balanțelor din mișcările persistente, folosind direcția locatorilor, nu eticheta FINDING a executorului. Intrările sunt exporturile readonly ale executorului; nu se revendică o rerulare A11 sau conectare SQL proprie.','inputs':[ref(B/n) for n in ['Readback_independent_final_v1.json','Readback_independent_dupa_business_v1.json','business_v2.stdout.txt','business_v2.A05N05Probe.java']], 'fixtures':out,'concurrent_sessions':{'T1':t1,'T2':t2,'distinct_PID_and_xid':True,'precommit_invisibility':'T1=8 piese; conexiune separată=10 piese/0 seturi; T2 rulează înainte de commitul T1','ordering_verified':True},'rollback_limit':{'rolled_back_instance':'1002649','persisted_native_result':'1','persisted_message':inst['1002649']['errormsg'],'WMS_movements_for_aborted_instance':0,'retry_instance':'1002650','retry_WMS_movements':2,'interpretation':'Metadatele procesului nu sunt rollback-uite împreună cu tranzacția externă managedTrx=false. Nu generaliza la atomicitate a tuturor metadatelor sau la defect al traseului normal.'},'N03_serial_persistent_rows_identical':True,'accounting_limit':'NativeQty10 și lipsa rândurilor Fact_Acct aferente sunt invarianți observați, nu execuție de postare contabilă, costuri cutii/manoperă sau DocAction.','conclusion':'Aceeași constatare N05 anterioară este întărită: procesul și garda PO originale permit BOM2→3 concurent, iar jurnalul persistat și stocul dau11 din10. Controlul serial dă10. Nu este un defect suplimentar în numărătoare.','resources':'Numai citire de artefacte și calcul în memorie; nicio modificare a laboratorului sau acces operațional.'}
p=O/'Contraoracol_A11_N05_persistenta_v1.json';assert not p.exists();p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(ref(p),ensure_ascii=False))
