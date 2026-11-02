exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
forms=collections.defaultdict(set)
formloc=collections.defaultdict(list)
for s,code,name in [("ADAUGARE FORME 1","C","A"),("Codificare forme","C","A")]:
    for r in d[s]:
        k,n=v(s,r,code),v(s,r,name)
        if k and n and not n.startswith("#"):
            forms[k].add(n);formloc[k].append([s,r])
mixes={}
for r in d["GLAZURI SETURI"]:
    code=v("GLAZURI SETURI",r,"A")
    if code in ["S039","S040","S041"]:
        vals=[v("GLAZURI SETURI",r,c) for c in "BCDEFGHIJKL"]
        mixes[code]=(", ".join(x for x in vals if x),r)
changes=[];missing=[]
def add(r,col,value,reason,source):
    c=d["NOMEXP02"][r][col+r]
    if c["v"]!=value:changes.append({"sheet":"NOMEXP02","cell":col+r,"old_formula":("="+c["f"]) if c["f"] else None,"old_value":c["v"],"new_value":value,"reason":reason,"source":source})
for r in d["NOMEXP02"]:
    sku=v("NOMEXP02",r,"A") or ""
    if not sku.startswith("5900_"):continue
    color=(v("NOMEXP02",r,"F") or "").replace(" ","")
    form=v("NOMEXP02",r,"I")
    if color in mixes:
        label,sr=mixes[color]
        reason="Compozitie exacta a setului de glazuri recuperata din GLAZURI SETURI."
        sources=[["GLAZURI SETURI",sr]]
    elif color=="356L":
        label="Verde";reason="Cod356L are descrierea Verde explicita pe articole existente, inclusiv NOMEXP02 G2706."
        sources=[["NOMEXP02","G2706"],["NOMEXP02","G2944"]]
    elif color=="324L":
        missing.append({"r":r,"sku":sku,"base_names":list(forms[form]),"source":formloc[form],"issue":"Cod culoare324L fara inregistrare exacta in cataloage. Regula existenta din G2951 clasifica prefix3 ca Verde, dar nu confirma validitatea codului324L."})
        continue
    else:continue
    add(r,"G",label,reason,sources)
    adaug_names={v("ADAUGARE FORME 1",rr,"A") for rr in d["ADAUGARE FORME 1"] if v("ADAUGARE FORME 1",rr,"C")==form}
    old_desc=v("NOMEXP02",r,"D")
    if old_desc and not old_desc.startswith("#") and old_desc.endswith("-356L"):
        base=old_desc[:-len("-356L")]
    elif len(adaug_names)==1:
        base=next(iter(adaug_names))
    elif len(forms[form])==1:
        base=next(iter(forms[form]))
    else:
        base=None
    if base:
        for col in ["C","D","J","S","V"]:
            add(r,col,base+"-"+label,"Denumire set din catalog + descriere glazura recuperata.",formloc[form]+sources)
(p/"color5900_fixes.json").write_text(json.dumps({"fixes":changes,"unresolved":missing},ensure_ascii=False,indent=2),encoding="utf-8")
print("changes",len(changes),collections.Counter(x["cell"][0] for x in changes),"missing",len(missing),"mixes",mixes)
print("unresolved",[x["r"] for x in missing])
