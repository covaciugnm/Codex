import openpyxl,collections,json,pathlib,re
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
src=r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx"
w=openpyxl.load_workbook(src,read_only=True,data_only=True)
data={s.title:list(s.iter_rows(values_only=True)) for s in w}
rows=[(i,r) for i,r in enumerate(data['NOMEXP02'][1:],2) if isinstance(r[0],str) and r[0].startswith('5900_')]
clean=lambda v:re.sub(r'(?<=\d)\s+(?=[LMA](?:_|$))','',v) if isinstance(v,str) else v
groups=collections.defaultdict(list)
for i,r in rows:groups[clean(r[0])].append(i)
cols={openpyxl.utils.get_column_letter(j+1):{'header':data['NOMEXP02'][0][j],
      'missing_rows':[i for i,r in rows if r[j] in (None,'')],
      'zero_rows':[i for i,r in rows if r[j]==0]}
      for j in range(32)}
shapegroups=collections.defaultdict(list)
for i,r in rows:shapegroups[str(r[8])].append((i,r))
definitions=collections.defaultdict(list)
for n,start,col in [('Codificare forme',4,2),('Adaugare forme',1,2),('ADAUGARE FORME 1',2,2)]:
    for i,r in enumerate(data[n][start-1:],start):
        if isinstance(r[col],(int,float)) and r[col]>=9000:definitions[str(r[col])].append({'sheet':n,'row':i,'label':r[0]})
shapes=[]
for shape,rs in shapegroups.items():
    oldmodels=collections.Counter(str(r[20]) for i,r in enumerate(data['NOMEXP02'][1:],2) if str(r[8])==shape and i not in [ii for ii,rr in rows])
    shapes.append({'shape':shape,'models':dict(collections.Counter(str(r[20]) for i,r in rs)),
       'rows':[i for i,r in rs],'labels':sorted(set(r[3] for i,r in rs)),
       'definitions':definitions[shape],'other_customer_models':dict(oldmodels)})
exact_matches=[]
sku_set=set(r[0] for i,r in rows)
for n,rs in data.items():
    if n=='NOMEXP02':continue
    for i,r in enumerate(rs,1):
        for j in [0,1]:
            if len(r)>j and r[j] in sku_set:
                exact_matches.append({'sheet':n,'row':i,'cell':f'{openpyxl.utils.get_column_letter(j+1)}{i}','sku':r[j]})
report={'count':len(rows),'first_row':rows[0][0],'last_row':rows[-1][0],
        'distinct_raw':len(set(r[0] for i,r in rows)),'distinct_normalized':len(groups),
        'duplicate_normalized':[{'sku':k,'rows':v} for k,v in groups.items() if len(v)>1],
        'spaces':[{'row':i,'sku':r[0],'normalized':clean(r[0])} for i,r in rows if r[0]!=clean(r[0])],
        'column_missing':cols,'shapes':shapes,'exact_matches_other_sheets':exact_matches}
(out/'sku5900_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print('COUNT',report['count'],'RANGE',report['first_row'],report['last_row'],'DISTINCT',report['distinct_raw'],report['distinct_normalized'],'DUP',report['duplicate_normalized'],'SPACES',len(report['spaces']),'EXACT_OTHER',exact_matches)
print('MISSING',[(c,x['header'],len(x['missing_rows']),len(x['zero_rows'])) for c,x in cols.items() if x['missing_rows'] or x['zero_rows']])
for s in shapes:print(s['shape'],s['models'],s['definitions'],s['other_customer_models'])
