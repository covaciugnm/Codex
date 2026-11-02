import openpyxl, collections, json, pathlib
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
w=openpyxl.load_workbook(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx",read_only=True,data_only=True)
mp=collections.defaultdict(set)
for n in ['DubluriLinii','NOMEXP02']:
    for r in w[n].iter_rows(min_row=2,values_only=True):
        if r[15] and r[14]: mp[str(r[15]).strip().upper()].add(r[14])
lis=collections.defaultdict(list)
for i,r in enumerate(w['LISGL1'].iter_rows(min_row=2,values_only=True),2):lis[str(r[3]).strip().upper()].append(i)
result=[{'name':n,'rows':ix,'candidate_codes':list(mp[n])} for n,ix in lis.items()]
(out/'customer_candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print([(x['name'],len(x['rows']),x['candidate_codes']) for x in result])
