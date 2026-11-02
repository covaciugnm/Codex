exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
def records(s,cols):
    for r in d[s]:
        if int(r)>1:yield int(r),[v(s,r,c) for c in cols]

names=collections.defaultdict(lambda:collections.defaultdict(list))
for s,code,name in [("NOMEXP02","O","P"),("FINAL_NOMEXP","Q","R"),("SEMIF.ARS","O","P"),("SEMIF.GLAZ","P","Q"),("SEMIF.BISC","K","L"),("SEMIF.CRUD","K","L"),("5358","O","P")]:
    for r,vs in records(s,[code,name]):
        if vs[0] and vs[1]:names[vs[1]][vs[0]].append((s,r))
lis=collections.Counter(v("LISGL1",r,"D") for r in d["LISGL1"] if int(r)>1)
print("LIS mapping",[{"name":n,"count":c,"codes":dict(names[n]) if len(names[n])!=1 else [(code,locs[0]) for code,locs in names[n].items()]} for n,c in lis.items()])
print("NOMEXP02 2747 matches")
for s in ["NOMEXP02","Codificare forme","ADAUGARE FORME 1","FINAL_NOMEXP"]:
    for r,rs in d[s].items():
        if any(c["v"] and ("SET 6 BOL13" in c["v"] or c["v"]=="61268") for c in rs.values()): print(s,r,row(s,r))
print("Static B errors")
for s in ["SORTAT","GLAZ"]:
    for r,rs in d[s].items():
        if rs.get("B"+r,{}).get("type")=="e":print(s,r,row(s,r))
print("Greutati names missing")
for s in ["SORTAT","BISC","CRUD"]:
    errcol="E" if s=="SORTAT" else "C"
    missing=collections.Counter(v(s,r,"B") for r,rs in d[s].items() if rs.get(errcol+r,{}).get("type")=="e")
    print(s,missing)
(p/"customer_mappings.json").write_text(json.dumps({"names":names,"lis":lis},ensure_ascii=False,indent=2),encoding="utf-8")
