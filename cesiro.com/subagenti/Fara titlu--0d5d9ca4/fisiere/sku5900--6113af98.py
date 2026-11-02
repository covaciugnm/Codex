exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
new=[]
forms=collections.defaultdict(set)
for s,code,name in [("ADAUGARE FORME 1","C","A"),("Codificare forme","C","A")]:
    for r in d[s]:
        k,n=v(s,r,code),v(s,r,name)
        if k and n and not n.startswith("#"):forms[k].add((n,s,r))
fixes=[];issues=[]
for r in d["NOMEXP02"]:
    sku=v("NOMEXP02",r,"A") or ""
    if not sku.startswith("5900_"):continue
    parts=sku.split("_");new.append((r,sku))
    if len(parts)!=4:
        issues.append({"r":r,"sku":sku,"issue":"SKU nu are 4 componente"});continue
    client,model,form,color=parts
    for col,part in [("U",model),("I",form),("F",color),("X",color),("AF",color)]:
        val=v("NOMEXP02",r,col)
        if val!=part:issues.append({"r":r,"sku":sku,"issue":"SKU versus "+col,"value":val,"part":part})
    desc=v("NOMEXP02",r,"D")
    base=[n for n,s,sr in forms[form]]
    stripdesc=desc.rsplit("-",1)[0] if desc and not desc.startswith("#") else None
    expected_set=int(form)>=9000
    if expected_set and v("NOMEXP02",r,"AD")!="SET":issues.append({"r":r,"sku":sku,"issue":"Set UM nonSET","um":v("NOMEXP02",r,"AD")})
    if expected_set and v("NOMEXP02",r,"H")!="PF.C":issues.append({"r":r,"sku":sku,"issue":"Set categoria nonPF.C","category":v("NOMEXP02",r,"H")})
    if base and desc and not desc.startswith("#") and not any(desc==n or desc.startswith(n+"-") for n in base):
        issues.append({"r":r,"sku":sku,"issue":"Descriere vs forma catalog","desc":desc,"forms":list(forms[form])})
    nums=set()
    for name,source,sr in forms[form]:
        match=re.match(r"SET\s+(\d+)\b",name)
        if match:nums.add(int(match.group(1)))
    if expected_set and len(nums)==1 and not v("NOMEXP02",r,"AE"):
        n=next(iter(nums))
        fixes.append({"sheet":"NOMEXP02","cell":"AE"+r,"old_formula":None,"old_value":None,"new_value":n,"reason":"Numar piese explicit si unic in denumirea formei din catalog.", "source":list(forms[form])})
(p/"audit5900.json").write_text(json.dumps({"count":len(new),"first_last":[new[0],new[-1]],"issues":issues,"piece_fixes":fixes},ensure_ascii=False,indent=2),encoding="utf-8")
print("rows",len(new),"range",new[0],new[-1],"issues",collections.Counter(x["issue"] for x in issues),"piecefill",len(fixes))
for x in issues:print(x)
