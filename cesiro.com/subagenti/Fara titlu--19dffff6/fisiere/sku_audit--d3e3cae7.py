import openpyxl,collections,json,pathlib,re
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
w=openpyxl.load_workbook(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx",read_only=True,data_only=True)
names=['NOMEXP02','SORTAT','ARS','GLAZ','BISC','CRUD']
rs={n:list(w[n].iter_rows(values_only=True)) for n in names}
report={}
for n,rows in rs.items():
    rx=(r'^\d{4}_\d{4}_\d{4}_[A-Za-z0-9]+$' if n=='NOMEXP02' else r'^\d{4}_\d{4}_[BC]$' if n in ['BISC','CRUD'] else r'^\d{4}_\d{4}_[A-Za-z0-9]+_[SAG]$')
    data=[(i,r) for i,r in enumerate(rows[1:],2) if r[0] not in (None,'')]
    malformed=[[i,r[0],list(r[1:7])] for i,r in data if not re.fullmatch(rx,str(r[0]))]
    groups=collections.defaultdict(list)
    for i,r in data:groups[r[0]].append((i,r))
    dups=[]
    for k,v in groups.items():
        if len(v)<2:continue
        cols=(2,3,5,6,7,8,10,11,12,13,14,15,16,18,19,20,21,23,27,28,29,30) if n=='NOMEXP02' else tuple(range(1,7 if n in ['SORTAT','ARS','GLAZ'] else 5))
        variants=collections.defaultdict(list)
        for i,r in v: variants[tuple(r[c] for c in cols)].append(i)
        dups.append({'sku':k,'rows':[i for i,r in v],'identical_core':len(variants)==1,'variants':[{'rows':ii,'values':vals} for vals,ii in variants.items()]})
    report[n]={'rows':len(data),'valid_format':len(data)-len(malformed),'malformed':malformed,'duplicates':dups}
(out/'sku_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
for n,x in report.items():
    print(n,'rows',x['rows'],'valid',x['valid_format'],'bad',len(x['malformed']),'dups',len(x['duplicates']),'conflicts',sum(not d['identical_core'] for d in x['duplicates']))
    print('BAD EXAMPLES',x['malformed'][:20])
    print('DUP EXAMPLES',x['duplicates'][:5])
