BEGIN READ ONLY;
SET LOCAL statement_timeout='12s';
SELECT 'db',current_database(),current_setting('transaction_read_only');
SELECT 'table',t.tablename,t.isactive FROM adempiere.ad_table t WHERE lower(t.tablename) IN('m_inout','m_inoutline','m_matchinv','m_matchpo','c_order','c_invoice','c_landedcost','c_landedcostallocation','m_rma','m_requisition','eva_sagacong','i_bpartner','i_invoice') ORDER BY 2;
SELECT 'window',w.name,w.isactive FROM adempiere.ad_window w WHERE w.name IN ('Requisition','Purchase Order','Material Receipt','Invoice (Vendor)','Matched Purchase Orders','Matched Invoices') ORDER BY 2;
SELECT 'form',f.classname,f.isactive FROM adempiere.ad_form f WHERE lower(f.classname) ~ '(wsagafurnizori|wsagasituatiefurnizori|wsagaintrari|verificareimportsaga|pornirefirma)' ORDER BY 2;
SELECT 'process',p.classname,p.isactive FROM adempiere.ad_process p WHERE lower(p.classname) ~ '(importsagafirma|importbpartner|importinvoice|matchinv|matchpo)' ORDER BY 2;
SELECT 'counts', (SELECT count(*) FROM adempiere.m_matchinv), (SELECT count(*) FROM adempiere.m_matchpo), (SELECT count(*) FROM adempiere.m_inout WHERE issotrx='N'), (SELECT count(*) FROM adempiere.c_order WHERE issotrx='N');
ROLLBACK;
