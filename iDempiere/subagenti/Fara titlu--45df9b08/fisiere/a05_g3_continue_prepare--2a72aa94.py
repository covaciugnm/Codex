from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04');W=Path('D:/CodexWork/a05-g3-harness')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
previous=[]
for p in O.glob('business_g3_v2.readback_*.json'):
 d=json.loads(p.read_text(encoding='utf8'))
 if d['case'] in ['G3-F01','other_product']:previous.append(d)
target=next(x for x in previous if x['case']=='G3-F01');other=next(x for x in previous if x['case']=='other_product')
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempt':'business_g3_v2','attempt_sha256':sha(O/'business_g3_v2.json'),'retained_error':'IsActive este readonly după creare; setterul original loghează ColumnReadonly și flagul rămâneY. saveEx/commit nu transformă acest refuz în dezactivare. Oracolul F03 inițial a fost invalid și nu primește credit.',
 'F03_amendment':{'path':'MStorageReservation(ctx,0,trx) original, AD_Org11/product/warehouse/ASI0/IsSOTrx/Qty/IsActive=false prin setteri înainte de primul saveEx; commit. Fără SQL write/set_ValueNoCheck/AD change.',
  'families':['SO2 activ prin add nativ + PO5 inactiv prin PO nou; EVA8/native8','SO2 inactiv și PO5 inactiv, ambele PO noi; EVA10/native8'],
  'gate':'Readback SQL Python readonly confirmă IsActive=N și cheile/UUID înainte de comparație; dacă setter/saveEx refuză, consemnează cazul neexecutat fără forțare.',
  'limit':'Caracterizarea cititorilor pe date sintetice create nativ, nu dovadă că o comandă comercială poate produce rânduri inactive.'},
 'F01_completion':{'existing_fixture':{'target_product':target['product'],'target_warehouse':target['warehouse'],'other_product':other['product']},'case':'Creează SO4/PO7 pentru other.product în warehouse al target, cu native add; verifică ținta neschimbată, cititorii originali și ambele chei readback. Izolează produsul; proba sameP_otherW existentă izolează depozitul.'},
 'continuation':'Nu repetă S01/C01/C02/C03 ori F02. Completează F01/F03, apoi ASI/rollback/retry/floor conform protocolului; revalidează toate bindingurile și canarii în noua JVM.',
 'before_resume':'Se așteaptă sigiliul aprobării nominale A11; pregătire numai.'}
f=O/'Addendum_F03_F01_G3_v1.json';assert not f.exists();f.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
s=(W/'A05G3Probe.java').read_text(encoding='utf-8-sig')
s=s.replace('if(System.getProperty("A05_G3_MODE").equals("business"))business();','if(System.getProperty("A05_G3_MODE").startsWith("business"))business();')
s=s.replace('int facts=DB.getSQLValueEx(null,"SELECT count(*) FROM fact_acct");F main=', 'int facts=DB.getSQLValueEx(null,"SELECT count(*) FROM fact_acct");if(!System.getProperty("A05_G3_MODE").equals("business_continuation")){F main=')
needle='  F lot=fixture("lot",true,"10");'
assert needle in s
def bound(d,tag):
 return f'F {tag}=new F("{tag}",{d["warehouse"]},{d["rows"]["stock"][0]["m_locator_id"]},{d["product"]},{d["source"]},0,0,0);check(new MProduct(actor,{tag}.product,null).getValue().equals("{d["rows"]["product"][0]["value"]}"),"continuation product identity");check(new MWarehouse(actor,{tag}.warehouse,null).getValue().equals("{d["rows"]["warehouse"][0]["value"]}"),"continuation warehouse identity");'
continuation='''  }else{
  '''+bound(target,'filterBound')+bound(other,'otherBound')+'''
  F cross=new F("otherP_sameW",filterBound.warehouse,filterBound.locator,otherBound.product,filterBound.source,0,0,0);committedAdd(cross,0,"4",true);committedAdd(cross,0,"7",false);readback(cross,"G3-F01-product-sentinel");observe(filterBound,"G3-F01-product-isolated","2","0","8","2","8",8,null);
  F inactivePO=fixture("inactivePO",false,"10");committedAdd(inactivePO,0,"2",true);newInactive(inactivePO,false,"5");readback(inactivePO,"G3-F03-POinactive-before-read");observe(inactivePO,"G3-F03-POinactive-newPO","2","5","8","2","8",8,null);
  F inactiveBoth=fixture("inactiveBoth",false,"10");newInactive(inactiveBoth,true,"2");newInactive(inactiveBoth,false,"5");readback(inactiveBoth,"G3-F03-bothInactive-before-read");observe(inactiveBoth,"G3-F03-bothInactive-newPO","2","5","8","0","10",10,null);
  }
'''
s=s.replace(needle,continuation+needle)
needle2=' void business()throws Exception{'
newmethod=''' void newInactive(F f,boolean so,String qty)throws Exception{
  Trx tx=Trx.get(Trx.createTrxName("G3_inactive_fixture"),true);boolean ok=false;
  try{MStorageReservation r=new MStorageReservation(actor,0,tx.getTrxName());r.setAD_Org_ID(11);r.setM_Product_ID(f.product);r.setM_Warehouse_ID(f.warehouse);r.setM_AttributeSetInstance_ID(0);r.setIsSOTrx(so);r.setQty(bd(qty));r.setIsActive(false);check(!r.isActive(),"new PO accepts inactive; otherwise stop without forcing");r.saveEx();tx.commit(true);ok=true;}finally{if(!ok)tx.rollback();tx.close();}
  check(DB.getSQLValueEx(null,"SELECT count(*) FROM m_storagereservation WHERE m_product_id=? AND m_warehouse_id=? AND issotrx=? AND isactive='N'",f.product,f.warehouse,so?"Y":"N")==1,"inactive row independently persisted");
 }
'''
assert needle2 in s;s=s.replace(needle2,newmethod+needle2);(W/'A05G3Probe.java').write_text(s,encoding='utf8')
r=Path('D:/CodexWork/a05_g3_run_barrier.py');text=r.read_text();text=text.replace("label=sys.argv[1];assert", "label=sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'business';assert").replace("'56455','business',str(W/", "'56455',mode,str(W/");r.write_text(text,encoding='utf8')
print(json.dumps(dict(addendum_sha256=sha(f),continuation_prepared=True,not_started=True)))
