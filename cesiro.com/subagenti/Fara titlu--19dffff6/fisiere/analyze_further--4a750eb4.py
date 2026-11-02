import openpyxl, collections, json, pathlib, math, re
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
w=openpyxl.load_workbook(r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx",read_only=True,data_only=True)
rs={s.title:list(s.iter_rows(values_only=True)) for s in w}
report={}

def group_rows(rows, col):
    g=collections.defaultdict(list)
    for i,r in enumerate(rows[1:],2):
        if r[col] not in (None,""):g[r[col]].append((i,r))
    return g
final=rs["FINAL_NOMEXP"]
g=group_rows(final,0)
mins={k:min(r[12] for i,r in v if isinstance(r[12],(float,int))) for k,v in g.items()}
report["final_min_cost_mismatches"]=[[i,r[0],r[13],mins[r[0]]] for i,r in enumerate(final[1:],2) if r[0] in mins and not math.isclose(r[13],mins[r[0]],abs_tol=1e-10)]
report["final_dupe_examples"]=[{"key":k,"rows":[{"row":i,"client":r[16],"name":r[17],"article":r[18],"price":r[11],"minimum":r[13],"currency":r[29],"weight":r[14]} for i,r in v]} for k,v in g.items() if len(v)>1][:10]
report["final_same_code_different_weights"]=[{"key":k,"rows":[[i,r[14]] for i,r in v]} for k,v in g.items() if len(set(r[14] for i,r in v))>1]
report["final_same_code_different_currency"]=[{"key":k,"rows":[[i,r[29]] for i,r in v]} for k,v in g.items() if len(set(r[29] for i,r in v))>1]

for n in ['NOMEXP02','DubluriLinii','NOMEXP02 - PRET','NOMEXP02 - GLAZ','NOMEXP02 - DEC','FINAL_NOMEXP']:
    data=rs[n]; offset=2 if n=='FINAL_NOMEXP' else 0
    # Offset not uniform: Final added a leading code and an extra min column.
    code,model,desc,price,currency,unit,pieces=(21,22,23,30,29,31,32) if offset else (19,20,21,28,27,29,30)
    actual=[(i,r) for i,r in enumerate(data[1:],2) if isinstance(r[14+offset],(int,float))]
    report[n]={
        "actual_rows":len(actual),"code_zero":sum(r[code] in (None,0,'0') for i,r in actual),
        "model_zero":sum(r[model] in (None,0,'0') for i,r in actual),
        "description_blank":sum(r[desc] in (None,"",0,'0') for i,r in actual),
        "currency":dict(collections.Counter(str(r[currency]) for i,r in actual)),
        "unit":dict(collections.Counter(str(r[unit]) for i,r in actual)),
        "price_zero":[i for i,r in actual if r[price] in (None,0,'0')],
        "price_negative":[[i,r[price]] for i,r in actual if isinstance(r[price],(int,float)) and r[price]<0],
        "unit_inconsistency":[[i,r[unit],r[pieces]] for i,r in actual if (str(r[unit]).upper()=='PCS' and r[pieces]!=1) or (str(r[unit]).upper()=='SET' and isinstance(r[pieces],(int,float)) and r[pieces]<2)]
    }
report["LISGL1_quantity_reconciliation"]=[[i,r[9],r[10],r[11]] for i,r in enumerate(rs["LISGL1"][1:],2) if all(isinstance(r[c],(int,float)) for c in (9,10,11)) and r[9]-r[10]!=r[11]]

# Mapping alterations across shape tables
fm={}
for n,cstart,cdesc,ccode in [('Codificare forme',4,0,2),('Adaugare forme',1,0,2),('ADAUGARE FORME 1',2,0,2)]:
    fm[n]={r[cdesc]:r[ccode] for r in rs[n][cstart-1:] if r[cdesc] is not None}
report["shape_cross_table_conflicts"]=[]
for n,m in fm.items():
    for desc,cod in m.items():
        if n!="Codificare forme" and desc in fm["Codificare forme"] and cod!=fm["Codificare forme"][desc]:
            report["shape_cross_table_conflicts"].append([n,desc,cod,fm["Codificare forme"][desc]])
report["model_identifiers_as_text"]={n:[c for c in collections.Counter(str(r[22 if n=="FINAL_NOMEXP" else 20]) for r in rs[n][1:] if isinstance(r[22 if n=="FINAL_NOMEXP" else 20],str))] for n in ["NOMEXP02","FINAL_NOMEXP"]}

(out/'further.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
for k,v in report.items():
    print(k, len(v) if isinstance(v,list) else v)
print("MIN MISMATCH EXAMPLES",report["final_min_cost_mismatches"][:20])
print("WEIGHT CONFLICTS",report["final_same_code_different_weights"][:20])
