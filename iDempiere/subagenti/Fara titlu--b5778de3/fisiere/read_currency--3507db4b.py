from lab import *
import json,datetime
assert W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh' and str(PG).startswith('eva-test-')
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-p01uizkr5'
q="""SELECT i.C_Invoice_ID,i.DocumentNo,i.AD_Client_ID,i.AD_Org_ID,i.DocStatus,i.C_Currency_ID,cur.ISO_Code,i.TotalLines,i.GrandTotal,l.Line,l.QtyInvoiced,l.PriceActual,l.LineNetAmt FROM adempiere.C_Invoice i JOIN adempiere.C_Currency cur ON cur.C_Currency_ID=i.C_Currency_ID JOIN adempiere.C_InvoiceLine l ON l.C_Invoice_ID=i.C_Invoice_ID WHERE i.C_Invoice_ID=1000002 AND i.AD_Client_ID=11 ORDER BY l.Line;"""
res=cmd(['docker','exec','-i',PG,'psql','-v','ON_ERROR_STOP=1','-X','-qAt','-U','postgres','-d','idempiere'], 'BEGIN READ ONLY; SELECT current_setting(\'transaction_read_only\');'+q+'ROLLBACK;')
lines=res.splitlines();assert lines[0]=='on';w=[x.split('|') for x in lines[1:]];assert len(w)==2 and all(x[5]=='100' and x[6]=='USD' and float(x[7])==570 for x in w)
print(json.dumps({'utc':now(),'tag':'E-A04-R3-CURRENCY','read_only':True,'container':PG,'actor':'auditor via PostgreSQL read-only în clona izolată','columns':['invoice','document','client','org','status','currency_id','iso','total_lines','grand_total','line','qty','price_actual','line_net'],'query':q,'rows':w},ensure_ascii=False,indent=2))
