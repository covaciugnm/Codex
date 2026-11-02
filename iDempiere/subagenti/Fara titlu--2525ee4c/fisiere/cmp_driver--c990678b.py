from lab import *
from t326_driver import env
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-a05r8'
assert rows("SELECT ad_client_id,name FROM adempiere.ad_client ORDER BY 1")==[['0','System'],['11','GardenWorld']]
out={'utc':now(),'scope':'Adaptarea comparatorului istoric T0 păstrează 10@10,10@14 pe L1 și 5@20 pe L2, ieșire 5 L1; pune setul de lot nominal EVA și schema fiscală nativă GardenWorld. Secțiunea de scenariu identică. Caz de probă, nu execuție din ecranul românesc.','actions':[]}
keys="'EVA_STRATURI_DE_LA','EVA_STRATURI_GENERATIE','EVA_METODA_DESCARCARE','EVA_URMARIRE_LOTURI'"
out['before']=rows(f"SELECT ad_sysconfig_id,name,value,isactive FROM adempiere.ad_sysconfig WHERE ad_client_id=11 AND name IN ({keys}) ORDER BY 1")
def qp(q):return int(sql(q))
dtpo=qp("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='POO' AND isactive='Y'")
mmr=122
iu=qp("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMI' AND docsubtypeinv='IU' AND isactive='Y'")
prl=qp("SELECT min(m_pricelist_id) FROM adempiere.m_pricelist WHERE ad_client_id=11 AND issopricelist='N' AND isactive='Y'")
ch=qp("SELECT min(c_charge_id) FROM adempiere.c_charge WHERE ad_client_id=11 AND isactive='Y'")
src=(W/'tools/teste/t329/pas0_cmp.py').read_text()
src=src.replace("'eva-test-p01-t329-'","'eva-test-p01-t163-'").replace('1000000, 1000000, 1000000, 1000001, 1000001, 1000073','11, 102, 11, 103, 101, 120').replace('1000016, 1000014, 1000026, 1000000, 1000002, 1000000, 1000000',f'{dtpo}, {mmr}, {iu}, {prl}, 110, 107, {ch}')
at=src.index('    aL = post(');end=src.index('    pZ = ',at);src=src[:at]+"""    aL = int(q("SELECT min(m_attributeset_id) FROM m_attributeset WHERE ad_client_id=11 AND description='EVA-P01.T329-LOT' AND islot='Y'"))
"""+src[end:]
source=W/'tools/teste/t329/pas0_cmp_adapted.py';source.write_text(src)
env.update(T329_PG=PG,T329_ID=AP)
try:
 proc=subprocess.run(['python3','-I',str(source)],cwd=W,capture_output=True,text=True,env=env,timeout=165)
 stdout=proc.stdout+'\n'+proc.stderr
 out.update(rc=proc.returncode,script_original_sha=digest((W/'tools/teste/t329/pas0_cmp.py').read_bytes()),adapted_sha=digest(src.encode()),observed=[x[:1450] for x in stdout.splitlines() if x.startswith(('RAND ','# clona','AssertionError:','RuntimeError:','ValueError:'))],last=stdout.strip().splitlines()[-1][:300])
 p=qp("SELECT max(m_product_id) FROM adempiere.m_product WHERE ad_client_id=11 AND value LIKE 'T329-Z-%'");out['cmp_product']=p
 out['current_config']=rows(f"SELECT name,value,isactive FROM adempiere.ad_sysconfig WHERE ad_client_id=11 AND name IN ({keys}) ORDER BY name")
 out['layer_detail']=rows(f"SELECT m_attributesetinstance_id,sursa,cantitateramasa,valoareramasa FROM adempiere.eva_stratstoc WHERE ad_client_id=11 AND m_product_id={p} ORDER BY 1")
except Exception as e:out['error']=str(e)[:650]
save('cmp_result.json',out);print(out.get('observed'),out.get('error'),flush=True)
try:
 t=auth('GardenAdmin',11,102,11)
 original=json.loads((W/'lots_native.json').read_text())
 p=original['ids']['product']; source=original['ids']['NIR_without_ASI']
 def state():return {'doccount':sql(f"SELECT count(*) FROM adempiere.m_inoutline l JOIN adempiere.m_inout d USING(m_inout_id) WHERE d.ad_client_id=11 AND d.docstatus='CO' AND l.m_product_id={p}"),'qtyzero':sql(f"SELECT coalesce(sum(t.movementqty),0) FROM adempiere.m_transaction t WHERE t.ad_client_id=11 AND t.m_attributesetinstance_id=0 AND t.m_product_id={p}")}
 before=state(); seed=get(t,'M_InOut',source)
 did=new(t,'M_InOut',{'AD_Org_ID':11,'M_Warehouse_ID':103,'C_BPartner_ID':120,'C_BPartner_Location_ID':ref(seed['C_BPartner_Location_ID']),'MovementType':'V+','IsSOTrx':False,'C_DocType_ID':122,'MovementDate':'2026-11-02','DateAcct':'2026-11-02','Description':'R8 engine-active missing ASI'})
 li=new(t,'M_InOutLine',{'AD_Org_ID':11,'M_InOut_ID':did,'M_Product_ID':p,'M_Locator_ID':101,'QtyEntered':10,'MovementQty':10,'C_UOM_ID':100,'Line':10})
 act=doc(t,'M_InOut',did,'CO');r={'doc':did,'line':li,'product':p,'before':before,'resp':act,'after':state(),'state':rows(f"SELECT docstatus,processed,posted FROM adempiere.m_inout WHERE m_inout_id={did}"),'config':out.get('current_config')}
 save('engine-missing-lot.json',r)
except Exception as e:save('engine-missing-lot.json',{'setup_error':str(e)[:450]})
