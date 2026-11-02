from a12_r10_base import *
exec((Path(__file__).parent/'a12_r10_receipt.py').read_text(encoding='utf8').split("j=P10/")[0]);cfg=[
 ('A11_control_supliment_T216_R10.json','3c1c56a04ec0a9babe3fa6debe8293d9a17d91e0cf62c67f9e6b6d9603958c67',['T216-R2-001','T216-R2-007'],['input_lines','inserted_lines','after_counterexamples','same_staging_after_retry','scoped_counts']),
 ('A11_control_supliment_T216_R10.json','3c1c56a04ec0a9babe3fa6debe8293d9a17d91e0cf62c67f9e6b6d9603958c67',['T216-R2-002','T216-R2-005','T216-R2-006'],['scoped_counts']),
 ('A11_control_cititori_T216_R10.json','4105d8ec341f73b56b7f3677a44e670a85f292099fdb834c4ce985c6b27c7609',['T216-R2-001','T216-R2-007'],['controls','conclusion']),
 ('A11_control_supliment_T329_R10.json','fe2fcfbe25f075a8cb8670176be3796373de9d3f3e18c8230d35b24838321a11',['T329-R2-012'],['nominal','contrasting_cases']),
 ('A11_control_supliment_T06_UX_R10.json','e4eac1e6712360c1940f33b3e50a323424cc306caa61165799deae33d61a0d9f',['T06-R2-022'],['dom_rows','export_rows','comparable_cells','mismatched_cells','altered_copy_one_cell_detected','negative_filter','count_from_database_control'])]
for name,h,ids,fields in cfg:
 f=E/name;assert sha(f)==h;d=rd(f);assert d['reviewer']=='A11'
 for c in ids:add(c,'A11 · control independent suplimentar',r9[c]['text'],{t:d[t]for t in fields},'Contraprobele și limitele proprii sunt în controlul independent semnat; fără notă globală.',d.get('scope',d.get('conclusion','')), [jr(f,'/'+t)for t in fields], 'independent_control_only')
f=P10/'Controale_independente_A11.json';wr(f,{'utc':now(),'receipts':out,'counts':{'reports':4,'distinct_criteria':len(out)},'none_duplicate_execution_credit':True});print(sha(f),len(out))

