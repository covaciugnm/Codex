exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
for s in ["NOMEXP02","SORTAT","ARS","GLAZ","BISC","CRUD"]:
    wrong=[]
    for r,vs in records(s,["A"]) if "records" in globals() else []:pass
    for r,rs in d[s].items():
        if int(r)<2: continue
        a=v(s,r,"A")
        n=5 if s=="NOMEXP02" else 4 if s in ["SORTAT","ARS","GLAZ"] else 3
        if a and len(a.split("_"))!=n:wrong.append((r,a))
    print(s,len(wrong),wrong[:30])
print("Tail source")
for s in ["NOMEXP02","SORTAT","GLAZ"]:
    end=max(map(int,d[s]))
    for r in range(end-12,end+1):print(s,r,row(s,r))
for s in ["SORTAT","GLAZ","BISC","CRUD"]:
    print("Malformed",s)
    for r,rs in d[s].items():
        a=v(s,r,"A")
        if a and (len(a.split("_"))<3 or a.startswith("394_") or a.startswith("0394_")):print(r,row(s,r))
