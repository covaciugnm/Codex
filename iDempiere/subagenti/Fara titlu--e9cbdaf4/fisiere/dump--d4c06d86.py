import pathlib,subprocess,json,re,hashlib,datetime
O=pathlib.Path(__file__).parent;dump='/tmp/codex-a07-handoff-6kab32p2/GardenWorld-A07.dump'
tables={'m_rma':('m_rma_id','docstatus','m_inout_id'),'m_rmaline':('m_rmaline_id','m_rma_id','m_inoutline_id','qty','m_product_id'),'m_inoutline':('m_inoutline_id','movementqty','m_product_id'),'c_invoice':('c_invoice_id','docstatus','grandtotal'),'c_payment':('c_payment_id','docstatus','payamt'),'c_allocationhdr':('c_allocationhdr_id','docstatus'),'c_allocationline':('c_allocationline_id','c_allocationhdr_id','c_invoice_id','c_payment_id','amount')}
cmd=['ssh','-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','saga-server@192.168.100.151']
h=subprocess.check_output(cmd+['sha256sum '+dump],timeout=20).decode().split()[0];assert h=='54d2a646a663949df78e24206a4dc2a30b7eab609aafba1229c1e6c28e97c6a4'
q='docker exec -i eva-postgres-cesiro pg_restore --data-only --file=- '+' '.join('-t '+t for t in tables)+' < '+dump
p=subprocess.run(cmd+[q],capture_output=True,timeout=90);assert not p.returncode,p.stderr[:300]
groups={};group=None
for line in p.stdout.decode('utf8').splitlines():
 if line.startswith('COPY '):
  m=re.match(r'^COPY (?:adempiere\.)?([a-z0-9_]+) \((.+)\) FROM stdin',line);group=m.group(1) if m else None;cols=m.group(2).split(', ') if m else []; continue
 if line==chr(92)+'.': group=None;continue
 if group not in tables:continue
 row=dict(zip(cols,line.split(chr(9))))
 if row.get('ad_client_id')!='11':continue
 wanted={'m_rma':['1000000','1000001'],'m_rmaline':['1000000','1000001'],'m_inoutline':['100'],'c_invoice':['1000001'],'c_payment':['1000000'],'c_allocationhdr':['1000000'],'c_allocationline':['1000000']}[group]
 if row.get(tables[group][0]) not in wanted:continue
 groups.setdefault(group,[]).append({k:row.get(k) for k in tables[group]})
assert len(groups)==7,str(groups)
def by(t,id):return next(x for x in groups[t] if x[tables[t][0]]==str(id))
from decimal import Decimal
a,b=by('m_rmaline',1000000),by('m_rmaline',1000001)
flags={'shipped_1':Decimal(by('m_inoutline',100)['movementqty'])==1,'return_2_without_reference_CO':Decimal(a['qty'])==2 and a['m_inoutline_id'] in (None,chr(92)+'N','0') and by('m_rma',a['m_rma_id'])['docstatus']=='CO','positive_return_1_with_reference_CO':Decimal(b['qty'])==1 and b['m_inoutline_id']=='100' and by('m_rma',b['m_rma_id'])['docstatus']=='CO','native_allocation_CO_30_on_DR':by('c_invoice',1000001)['docstatus']=='DR' and by('c_payment',1000000)['docstatus']=='CO' and by('c_allocationhdr',1000000)['docstatus']=='CO' and by('c_allocationline',1000000)['c_invoice_id']=='1000001' and Decimal(by('c_allocationline',1000000)['amount'])==30}
assert all(flags.values()),flags
result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_sha256':h,'copied_data_stream_sha256':hashlib.sha256(p.stdout).hexdigest(),'command':q,'checks':flags,'evidence':groups,'scope':'Independent interrogation of frozen synthetic backup using pg_restore to stdout, no database connection or restore/mutation. Independently verifies persisted rows. It is not a second live execution of transitions; HTTP refusals or creation chronology are not determined from the final rows.'}
(O/'A07_native_dump_invariants.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(flags)

