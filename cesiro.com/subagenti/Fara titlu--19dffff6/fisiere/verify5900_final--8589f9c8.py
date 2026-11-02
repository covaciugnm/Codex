import openpyxl,json,pathlib,collections,re,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
dst=pathlib.Path(r"Z:\00.Roboti\cesiro.com\outputs\nomexp_5900_20261020\NOMEXP_SKU_5900_corectat.xlsx")
control=json.loads((p/'sku5900_expected_control.json').read_text(encoding='utf-8'))
manifest=json.loads((p/'sku5900_manifest.json').read_text(encoding='utf-8'))
wv=openpyxl.load_workbook(dst,read_only=True,data_only=True)
wf=openpyxl.load_workbook(dst,read_only=True,data_only=False)
src=openpyxl.load_workbook(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx",read_only=True,data_only=True)
expected=set(control['expected_sku_sorted'])
source={i:list(r[:32]) for i,r in enumerate(src['NOMEXP02'].iter_rows(values_only=True),1) if isinstance(r[0],str) and r[0].startswith('5900_')}
main=list(wv['SKU_5900'].iter_rows(min_row=7,max_row=372,max_col=21,values_only=True))
exp=list(wv['NOMEXP02_5900'].iter_rows(min_row=2,max_row=367,max_col=32,values_only=True))
original=list(wv['Original_5900'].iter_rows(min_row=7,max_row=373,max_col=33,values_only=True))
errors=[]; stats={}
stats['main_count']=len(main);stats['export_count']=len(exp);stats['source_count']=len(original)
for tag,rs in [('main',main),('export',exp)]:
    keys=[r[0] for r in rs]
    if set(keys)!=expected:errors.append([tag,'wrong_skus',sorted(expected-set(keys)),sorted(set(keys)-expected)])
    if len(keys)!=len(set(keys)):errors.append([tag,'duplicates'])
    if any(not re.fullmatch(r'5900_\d{4}_\d{4}_[A-Z0-9]+',str(k)) for k in keys):errors.append([tag,'invalid_format'])
for i,r in enumerate(main,7):
    parts=r[0].split('_')
    if [str(r[2]),str(r[3]),r[4]]!=parts[1:]:errors.append(['main',i,'sku_components',r[:5]])
    if r[9]!=5900 or r[7]!='PF.C' or r[8]!='SET' or r[10]!='EUR':errors.append(['main',i,'classification'])
    if any(r[j] is not None for j in [11,12,13,14]):errors.append(['main',i,'price_weight_invented',r[11:15]])
    if r[18]!='Cod valid':errors.append(['main',i,'invalid_status',r[18]])
mainmap={r[0]:r for r in main}
for i,r in enumerate(exp,2):
    m=mainmap[r[0]]
    mapping={0:0,5:4,6:5,7:7,8:3,10:11,11:12,12:13,13:14,14:9,15:17,16:16,19:15,20:2,27:10,28:11,29:8,30:6}
    for j,k in mapping.items():
        if r[j]!=m[k]:errors.append(['export_vs_main',i,openpyxl.utils.get_column_letter(j+1),r[j],m[k]])
    if not all(r[j]==r[2] for j in [3,9,18,21]):errors.append(['export',i,'description_inconsistent'])
    if r[23]!=r[5] or r[31]!=r[5]:errors.append(['export',i,'color_inconsistent'])
for row in original:
    sr=row[0];values=list(row[1:])
    if sr not in source:errors.append(['original','unexpected_row',sr]);continue
    if values!=source[sr]:
        for j,(a,b) in enumerate(zip(values,source[sr])):
            if a!=b:errors.append(['original',sr,openpyxl.utils.get_column_letter(j+1),a,b])
if {r[0] for r in original}!=set(source):errors.append(['original','missing_source_rows'])
expected_pieces={r['normalized_sku']:r['values'][30] for r in manifest['records_after_certain_corrections']}
for r in main:
    if r[6]!=expected_pieces[r[0]]:errors.append(['main',r[0],'piece_count',r[6],expected_pieces[r[0]]])
for n in ['SKU_5900','NOMEXP02_5900','Cataloage','Corectii']:
    for row in wv[n].iter_rows():
        for c in row:
            if c.data_type=='e':errors.append(['excel_error',n,c.coordinate,c.value])
stats['original_values_equal']=not any(e[0]=='original' for e in errors)
stats['model_distribution']=dict(collections.Counter(str(r[2]) for r in main))
stats['piece_distribution']=dict(collections.Counter(r[6] for r in main))
stats['main_last_row']=main[-1][0]
stats['formulas_by_sheet']={s.title:sum(c.data_type=='f' for row in s.iter_rows() for c in row) for s in wf}
stats['file_sha256']=hashlib.sha256(dst.read_bytes()).hexdigest()
result={'file':str(dst),'stats':stats,'errors':errors}
(p/'sku5900_final_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
