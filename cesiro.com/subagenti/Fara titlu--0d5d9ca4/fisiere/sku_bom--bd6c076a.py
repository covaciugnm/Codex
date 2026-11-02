exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
formdefs=collections.defaultdict(set)
for r in d["ADAUGARE FORME 1"]:
    code,name=v("ADAUGARE FORME 1",r,"C"),v("ADAUGARE FORME 1",r,"A")
    if code and name:formdefs[code].add(name)
nomu=collections.defaultdict(set)
nomusrc=collections.defaultdict(list)
for r in d["NOMU"]:
    code,model,desc=v("NOMU",r,"A"),v("NOMU",r,"C"),v("NOMU",r,"D")
    if code and model and desc and re.fullmatch(r"\d+_\d+_C",code):
        nomu[model,desc].add("_".join(code.split("_")[:2]))
        nomusrc[model,desc].append(r)
fixes=[];unknown=[];groups=[]
for s in ["SORTAT","ARS","GLAZ"]:
    rr=sorted(map(int,d[s]))
    for i,r in enumerate(rr):
        a=v(s,r,"A")
        if not a or not re.fullmatch(r"\d+_9\d{3}_.+_[SAG]",a):continue
        parts=a.split("_")
        if len(parts)!=4:continue
        model,form,color,suffix=parts
        definitions=sorted(formdefs.get(form,[]))
        namedmodels=set(m for n in definitions for m in re.findall(r"\d{4}",n))
        group=[r]
        while group[-1]+1 in rr:
            nr=group[-1]+1
            na=v(s,nr,"A") or ""
            if len(na.split("_"))!=2 or v(s,nr,"C")!=color:break
            group.append(nr)
        if len(group)<2:continue
        component={}
        for nr in group:
            desc=v(s,nr,"B")
            choices=set()
            for m in namedmodels:choices.update(nomu.get((m,desc),set()))
            component[nr]=sorted(choices)
        reason=f"Forma set {form}: {'; '.join(definitions)}. Modele explicite {','.join(sorted(namedmodels))}; potrivire exacta model+denumire in NOMU."
        groups.append({"sheet":s,"start":r,"form":form,"definitions":definitions,"models":sorted(namedmodels),"component_candidates":component})
        for nr,choices in component.items():
            if len(choices)==1:
                code=choices[0]
                old=v(s,nr,"A")
                new=f"{code}_{color}_{suffix}"
                if new!=old:
                    mod=code.split("_")[0];desc=v(s,nr,"B")
                    fixes.append({"sheet":s,"cell":"A"+str(nr),"old_formula":None,"old_value":old,"new_formula":f'="{code}_"&C{nr}&"_{suffix}"',"expected_value":new,"reason":reason,"source_NOMU_rows":nomusrc[mod,desc]})
            else:unknown.append({"sheet":s,"cell":"A"+str(nr),"old":v(s,nr,"A"),"desc":v(s,nr,"B"),"choices":choices,"reason":reason})
(p/"sku_bom_candidates.json").write_text(json.dumps({"fixes":fixes,"unknown":unknown,"groups":groups},ensure_ascii=False,indent=2),encoding="utf-8")
print("Unique fixes",len(fixes),collections.Counter(x["sheet"] for x in fixes),"unknown",len(unknown))
print("Forms",collections.Counter(g["form"] for g in groups))
for x in groups:
    if x["sheet"]=="SORTAT":print(x)
