"""Synthetic probe for coordinator's admitted p01uizkr5 cabinet; no other host."""
import argparse
import json
from decimal import Decimal
from pathlib import Path
from uuid import uuid4


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--admitted-owner", required=True, choices=["eva-contab-codex-p01uizkr5"])
    args.parse_args()
    import lab
    allowed = "eva-contab-codex-p01uizkr5"
    work = Path(lab.W)
    assert work.name.startswith("eva-contab-codex-p01uizk-r5.")
    for container in (lab.PG, lab.AP):
        label = lab.cmd(["docker", "inspect", "--format", '{{index .Config.Labels "eva.sesiune"}}', container])
        assert label == allowed, "Cabinet ownership mismatch"
    assert lab.sql("SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y'") == "0"
    assert lab.rows("SELECT ad_client_id,name FROM adempiere.ad_client ORDER BY 1") == [["0", "System"], ["11", "GardenWorld"]]

    tag = "R5W" + uuid4().hex[:8]
    tokens = lab.auth("GardenAdmin", 11, 102, 11)
    ids = {}
    report = {"id": tag, "utc": lab.now(), "ids": ids, "events": [], "states": [],
              "scope": "Single internal GardenWorld origin. Standard native SO, no website order. T337 and standard Pick/QA are scored separately. Foreign contacts, AWB and cash are outside this probe."}
    result_file = "a05-chain-" + tag + ".json"

    def flush():
        lab.save(result_file, report)

    def call(title, method, route, data=None):
        status, body = lab.api(tokens, method, route, data)
        raw = body.get("DocStatus")
        state = raw.get("id") if isinstance(raw, dict) else raw
        report["events"].append({"utc": lab.now(), "operation": title, "route": route,
                                 "request": data, "http": status, "id": body.get("id"),
                                 "docstatus": state, "process_error": body.get("isError"),
                                 "process_instance": body.get("adPInstanceId"),
                                 "detail": str(body.get("detail", body.get("summary", "")))[:1300]})
        flush()
        return status, body

    def make(label, table, data):
        code, body = call(label, "POST", "models/" + table, dict(AD_Org_ID=11, **data))
        assert code in (200, 201) and body.get("id"), (label, report["events"][-1])
        ids[label] = int(body["id"])
        return ids[label]

    def action(label, table, rid, code):
        return call(label, "PUT", "models/" + table + "/" + str(rid), {"doc-action": code})

    def state(table, rid):
        # Table and column names are hard-coded at every call site; identifiers originate in native API.
        return lab.sql(f"SELECT docstatus FROM adempiere.{table} WHERE {table}_id={int(rid)}")

    def snapshot(stage):
        g, w = ids.get("G1", -1), ids.get("G2", -1)
        items = f"123,124,{ids.get('S1_CPA',-1)}"
        so, io, rr = ids.get("SO", -1), ids.get("shipment", -1), ids.get("return_receipt", -1)
        docs = f"{io},{rr}"
        line = ids.get("shipment_line", -1)
        queries = {
            "g1_lot_locator": f"SELECT l.m_locator_id,s.m_product_id,s.m_attributesetinstance_id,sum(s.qtyonhand) FROM adempiere.m_storageonhand s JOIN adempiere.m_locator l USING(m_locator_id) WHERE s.ad_client_id=11 AND l.m_warehouse_id={g} AND s.m_product_id IN ({items}) GROUP BY 1,2,3 ORDER BY 1,2,3",
            "g2_lot_locator_recipe": f"SELECT m_locator_id,m_product_id,m_attributesetinstance_id,pp_product_bom_id,qty FROM adempiere.eva_stocwms WHERE ad_client_id=11 AND m_warehouse_id={w} AND m_product_id IN ({items}) ORDER BY 1,2,3,4",
            "wms_events": f"SELECT eva_miscarewms_id,eva_tipmiscarewms,ad_table_id,record_id,eva_liniesursa_id,c_order_id,m_locator_id,m_locatorto_id,m_product_id,m_attributesetinstance_id,qty,eva_faraculegere,eva_miscarewmsinversa_id FROM adempiere.eva_miscarewms WHERE ad_client_id=11 AND m_warehouse_id={w} ORDER BY 1",
            "so_and_reservation": f"SELECT o.c_order_id,o.docstatus,l.c_orderline_id,l.qtyordered,l.qtyreserved,l.qtydelivered FROM adempiere.c_order o JOIN adempiere.c_orderline l USING(c_order_id) WHERE o.c_order_id={so}",
            "reservations": f"SELECT issotrx,m_product_id,qty FROM adempiere.m_storagereservation WHERE ad_client_id=11 AND m_warehouse_id={g} AND m_product_id IN ({items}) ORDER BY 1,2",
            "shipment_lines_chain": f"SELECT io.m_inout_id,io.docstatus,io.posted,io.c_order_id,io.m_rma_id,io.reversal_id,il.m_inoutline_id,il.c_orderline_id,il.m_rmaline_id,il.m_product_id,il.movementqty FROM adempiere.m_inout io JOIN adempiere.m_inoutline il USING(m_inout_id) WHERE io.m_inout_id IN ({docs}) OR io.reversal_id IN ({docs}) ORDER BY 1,7",
            "t337_erp_staging_link": f"SELECT eva_comandasite_id,eva_comandasitelinie_id,c_order_id,m_inout_id FROM adempiere.eva_comandasitelinie WHERE ad_client_id=11 AND (m_inout_id={io} OR c_order_id={so}) ORDER BY 1,2",
            "pc": f"SELECT pc.m_inoutconfirm_id,pc.confirmtype,pc.docstatus,pcl.m_inoutlineconfirm_id,pcl.targetqty,pcl.confirmedqty FROM adempiere.m_inoutconfirm pc LEFT JOIN adempiere.m_inoutlineconfirm pcl USING(m_inoutconfirm_id) WHERE pc.m_inout_id={io}",
            "rma": f"SELECT r.m_rma_id,r.docstatus,l.m_rmaline_id,l.m_inoutline_id,l.qty,l.qtydelivered FROM adempiere.m_rma r JOIN adempiere.m_rmaline l USING(m_rma_id) WHERE l.m_inoutline_id={line} ORDER BY 1,3",
            "trx": f"SELECT t.m_transaction_id,t.m_inoutline_id,t.m_inventoryline_id,t.m_product_id,t.m_attributesetinstance_id,t.m_locator_id,t.movementqty FROM adempiere.m_transaction t JOIN adempiere.m_locator l USING(m_locator_id) WHERE t.ad_client_id=11 AND l.m_warehouse_id={g} AND t.m_product_id IN ({items}) ORDER BY 1",
            "cost": f"SELECT d.m_costdetail_id,d.m_product_id,d.m_inoutline_id,d.m_inventoryline_id,d.qty,d.amt FROM adempiere.m_costdetail d LEFT JOIN adempiere.m_inoutline il USING(m_inoutline_id) LEFT JOIN adempiere.m_inventoryline inv USING(m_inventoryline_id) WHERE d.ad_client_id=11 AND (il.m_inout_id IN (SELECT m_inout_id FROM adempiere.m_inout WHERE m_inout_id IN ({docs}) OR reversal_id IN ({docs})) OR inv.m_inventory_id IN ({ids.get('opening123',-1)},{ids.get('opening124',-1)})) ORDER BY 1",
            "facts": f"SELECT t.tablename,f.record_id,f.line_id,f.fact_acct_id,f.account_id,f.m_product_id,f.amtacctdr,f.amtacctcr FROM adempiere.fact_acct f JOIN adempiere.ad_table t USING(ad_table_id) WHERE f.ad_client_id=11 AND ((t.tablename='M_InOut' AND f.record_id IN (SELECT m_inout_id FROM adempiere.m_inout WHERE m_inout_id IN ({docs}) OR reversal_id IN ({docs}))) OR (t.tablename='M_Inventory' AND f.record_id IN ({ids.get('opening123',-1)},{ids.get('opening124',-1)}))) ORDER BY 1,2,3,4",
        }
        capture = {"stage": stage, "utc": lab.now(), "sql": queries}
        for label, query in queries.items():
            capture[label] = lab.rows(query)
        report["states"].append(capture)
        flush()
        return capture

    try:
        standard = lab.get(tokens, "M_Warehouse", 103)
        g = make("G1", "M_Warehouse", {"C_Location_ID": lab.ref(standard["C_Location_ID"]), "Value": tag, "Name": tag})
        gl = make("G1loc", "M_Locator", {"M_Warehouse_ID": g, "Value": tag+"G", "X": tag, "Y": "G", "Z": "1", "IsDefault": True})
        pi = int(lab.sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMI' AND docsubtypeinv='PI' AND isactive='Y'"))
        for product in (123, 124):
            inv = make("opening"+str(product), "M_Inventory", {"M_Warehouse_ID": g, "C_DocType_ID": pi, "MovementDate": "2026-11-02", "Description": tag})
            make("opening_line"+str(product), "M_InventoryLine", {"M_Inventory_ID": inv, "M_Product_ID": product, "M_Locator_ID": gl, "QtyBook": 0, "QtyCount": 1, "Line": 10})
            action("post opening", "M_Inventory", inv, "CO")
            assert state("m_inventory",inv) == "CO"
        c,b=call("activate pair","POST","processes/eva_activarewms",{"M_Warehouse_ID":g})
        assert c==200 and not b.get("isError")
        w,neutral,exp=map(int,lab.rows(f"SELECT eva_gestiunewms_id,eva_locatorneamplasat_id,eva_locatorexpediere_id FROM adempiere.eva_perechewms WHERE ad_client_id=11 AND m_warehouse_id={g}")[0])
        ids.update(G2=w,G2neutral=neutral,G2dispatch=exp)
        pickloc=make("G2pickloc","M_Locator",{"M_Warehouse_ID":w,"Value":tag+"P","X":tag,"Y":"P","Z":"1","IsDefault":False})
        sample=lab.get(tokens,"M_Product",123)
        s1=make("S1_CPA","M_Product",{"M_Product_Category_ID":lab.ref(sample["M_Product_Category_ID"]),"C_TaxCategory_ID":lab.ref(sample["C_TaxCategory_ID"]),"C_UOM_ID":100,"ProductType":"I","IsStocked":False,"IsBOM":True,"Value":tag+"S1","Name":tag+" S1"})
        bom=make("recipe","PP_Product_BOM",{"M_Product_ID":s1,"Name":tag,"Value":tag+"B","BOMType":"A","BOMUse":"A","C_UOM_ID":100})
        for i,product in enumerate((123,124),1):
            make("recipe_line"+str(product),"PP_Product_BOMLine",{"PP_Product_BOM_ID":bom,"M_Product_ID":product,"C_UOM_ID":100,"QtyBOM":1,"Line":10*i,"ComponentType":"CO"})
        snapshot("initial 1 CPP and 1 packaging in G1 and mirror; no note yet")
        def note(tip):
            c,b=call("pack" if tip==1 else "unpack for this order","POST","processes/eva_notasetwms",{"M_Warehouse_ID":g,"M_Product_ID":s1,"Qty":1,"M_Locator_ID":pickloc,"PP_Product_BOM_ID":bom,"EVA_TipNota":tip})
            assert c==200 and not b.get("isError")
            ids["pack_instance" if tip==1 else "unpack_instance"]=b.get("adPInstanceId")
        note(1)
        before_so=snapshot("all free CPP in G2 now assembled in S1")
        assert sum(Decimal(x[4]) for x in before_so["g2_lot_locator_recipe"] if x[1]=='123')==0
        assert sum(Decimal(x[4]) for x in before_so["g2_lot_locator_recipe"] if x[1]==str(s1))==1
        order=make("SO","C_Order",{"IsSOTrx":True,"C_DocTypeTarget_ID":132,"M_Warehouse_ID":g,"C_BPartner_ID":112,"C_BPartner_Location_ID":108,"M_PriceList_ID":101,"C_Currency_ID":100,"C_PaymentTerm_ID":106,"SalesRep_ID":100,"DateOrdered":"2026-11-02","DateAcct":"2026-11-02","DatePromised":"2026-11-02","Description":tag,"POReference":tag,"DeliveryRule":"A","DeliveryViaRule":"P","FreightCostRule":"I","InvoiceRule":"D"})
        ol=make("SO_line","C_OrderLine",{"C_Order_ID":order,"M_Product_ID":123,"C_UOM_ID":100,"QtyOrdered":1,"QtyEntered":1,"PriceActual":10,"PriceEntered":10,"PriceList":10,"C_Tax_ID":104,"Line":10})
        action("reserve ordered CPP", "C_Order",order,"CO")
        assert state("c_order",order)=="CO"
        snapshot("order open + standard SO reservation before unpack")
        note(2)
        n=snapshot("before pick; dismantled CPP on selected G2 shelf")
        assert any(x[0]==str(pickloc) and x[1]=='123' and Decimal(x[4])==1 for x in n["g2_lot_locator_recipe"])
        report["note_parameters"]=lab.rows("SELECT columnname,ismandatory FROM adempiere.ad_process_para WHERE ad_process_id=(SELECT ad_process_id FROM adempiere.ad_process WHERE value='EVA_NotaSetWms') ORDER BY seqno")
        report["note_link_limit"]="Both AD_PInstance effects are recorded. No original-note/order parameter is injected. Temporal association of unpack with SO is a harness correlation; a true reversal needs the original event FK."
        dtype=lab.sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND docbasetype='MMS' AND issotrx='Y' AND ispickqaconfirm='Y' AND isshipconfirm='N' AND isactive='Y'")
        if not dtype:
            parent=lab.get(tokens,"C_DocType",120)
            conf_type={"Name":tag+" pick","PrintName":tag,"DocBaseType":"MMS","IsSOTrx":True,"IsPickQAConfirm":True,"IsShipConfirm":False,"IsDocNoControlled":True,"DocNoSequence_ID":lab.ref(parent["DocNoSequence_ID"])}
            dtype=make("fixture_pick_doctype","C_DocType",conf_type)
        io=make("shipment","M_InOut",{"IsSOTrx":True,"C_DocType_ID":int(dtype),"C_Order_ID":order,"MovementType":"C-","M_Warehouse_ID":g,"C_BPartner_ID":112,"C_BPartner_Location_ID":108,"MovementDate":"2026-11-02","DateAcct":"2026-11-02","Description":tag})
        il=make("shipment_line","M_InOutLine",{"M_InOut_ID":io,"C_OrderLine_ID":ol,"M_Product_ID":123,"M_Locator_ID":gl,"MovementQty":1,"QtyEntered":1,"Line":10})
        action("prepare shipment", "M_InOut",io,"PR")
        at=snapshot("shipment prepared; seek exact native PC and EVA staging")
        assert at["pc"],"No pick confirmation generated for this shipment"
        pc=int(at["pc"][0][0]); ids["pick_confirmation"]=pc
        rev=lab.sql(f"""SELECT to_char(updated,'YYYY-MM-DD"T"HH24:MI:SS.MS') FROM adempiere.m_inoutconfirm WHERE m_inoutconfirm_id={pc}""")
        lines=";".join(row[3]+":"+row[4] for row in at["pc"])
        c,b=call("T337 on exact native shipment; no site header injected","POST","processes/eva_valideazacomenzi",{"Operatie":"CONFIRM_CULEGERE","Inregistrari":str(pc),"Revizie":rev,"Linii":lines})
        snapshot("T337 attempt before native PC")
        if state("m_inoutconfirm",pc)!="CO":
            report["pick_path"]="T337 did not complete. Continue separately through the native Pick/QA entry on this same SO and shipment; do not credit a G2 pick for native PC without CULEGERE journal."
            for row in at["pc"]:
                c,b=call("count pick native","PUT","models/M_InOutLineConfirm/"+row[3],{"ConfirmedQty":float(row[4])})
                assert c==200
            action("complete actual Pick/QA","M_InOutConfirm",pc,"CO")
        assert state("m_inoutconfirm",pc)=="CO"
        if state("m_inout",io)!="CO": action("complete shipment","M_InOut",io,"CO")
        assert state("m_inout",io)=="CO"
        snapshot("completed physical shipment; look for actual CULEGERE vs EVA_FaraCulegere")
        rt=int(lab.sql("SELECT min(m_rmatype_id) FROM adempiere.m_rmatype WHERE ad_client_id=11 AND isactive='Y'"))
        rd=int(lab.sql("SELECT min(c_doctype_id) FROM adempiere.c_doctype WHERE ad_client_id=11 AND lower(name)='customer return material' AND issotrx='Y'"))
        rma=make("RMA","M_RMA",{"IsSOTrx":True,"C_DocType_ID":rd,"M_RMAType_ID":rt,"InOut_ID":io,"C_BPartner_ID":112,"Name":tag+" RMA"})
        rl=make("RMA_line","M_RMALine",{"M_RMA_ID":rma,"M_InOutLine_ID":il,"M_Product_ID":123,"Line":10,"Qty":1,"Amt":10})
        action("authorize RMA","M_RMA",rma,"CO")
        assert state("m_rma",rma)=="CO"
        snapshot("RMA authorization only; receipt separate")
        dt=int(lab.sql(f"SELECT c_doctypeshipment_id FROM adempiere.c_doctype WHERE c_doctype_id={rd}"))
        rr=make("return_receipt","M_InOut",{"IsSOTrx":True,"M_RMA_ID":rma,"C_DocType_ID":dt,"MovementType":"C+","M_Warehouse_ID":g,"C_BPartner_ID":112,"C_BPartner_Location_ID":108,"MovementDate":"2026-11-02","DateAcct":"2026-11-02","Description":tag+" RMA receipt"})
        make("return_line","M_InOutLine",{"M_InOut_ID":rr,"M_RMALine_ID":rl,"M_Product_ID":123,"M_Locator_ID":gl,"MovementQty":1,"QtyEntered":1,"Line":10})
        action("physically receive authorized return","M_InOut",rr,"CO")
        assert state("m_inout",rr)=="CO"
        snapshot("returned physical CPP; only if receipt CO")
        action("reverse receipt with original native record link","M_InOut",rr,"RC")
        snapshot("after native linked return reversal")
        action("retry receipt reversal; count reversals","M_InOut",rr,"RC")
        snapshot("after retry; each reverse doc linked directly to original receipt")
        report["native_chain_completed"]=True
    except Exception as error:
        report["stopped_at"]={"stage":report["events"][-1]["operation"] if report["events"] else "preparation","message":str(error)[:1500]}
        if ids.get("G1"):
            try: snapshot("terminal observation after refusal")
            except Exception as snap_error: report["snapshot_error"]=str(snap_error)[:500]
    finally:
        report["interpretation"]="No automatic PASS. Check actual DocStatus, physical quantity, linkage, postings, G2 journals, authorized actor, and once-only packaging. A successful receipt reversal is not a reversal of the WMS note. Fact_Acct may await posting; no invented cost, no direct ledger writes."
        flush()
        print(json.dumps({"file":result_file,"stage":report.get("stopped_at"),"ids":ids},ensure_ascii=False))


if __name__=="__main__":
    main()
