exec(open(str(__import__("pathlib").Path(__file__).parent/"query.py"),encoding="utf-8").read().split('for s in ["NOMEXP02"')[0])
manifest=[]
def add(s,a,new,reason,expected=None):
    c=d[s][re.search(r"\d+",a).group()][a]
    manifest.append({"sheet":s,"cell":a,"old_formula":("="+c["f"]) if c["f"] else None,"old_value":c["v"],"new_formula":new,"reason":reason,"expected_value":expected})

for r,rs in d["NOMEXP02"].items():
    c=rs.get("G"+r,{})
    f=c.get("f") or ""
    if c.get("v")=="#REF!" and "VLOOKUP" in f and re.search(r"A\d+:B\d+,3,0",f):
        key=v("NOMEXP02",r,"F")
        colormatch=[(cr,v("Codificare 1 Glazuri",cr,"B")) for cr in d["Codificare 1 Glazuri"] if v("Codificare 1 Glazuri",cr,"A")==key]
        add("NOMEXP02","G"+r,"="+re.sub(r"A\d+:B\d+,3,0",r"$A$4:$B$188,2,0",f),"Tabelul de glazuri are doua coloane. Indicele 3 produce #REF!; descrierea este coloana 2. Ancora repara deplasarea intervalului copiat.",colormatch[0][1] if colormatch else None)
add("NOMEXP02","I2747","=INDEX('Codificare forme'!$C$4:$C$211,MATCH(D2747,'Codificare forme'!$A$4:$A$211,0))","Forma SET 6 BOL13 2996 exista exact in Codificare forme A182, cod 9049. Acelasi produs 61268 are cod9049 si pe randul1487.",9049)
add("BISC","B320","=VLOOKUP(VALUE(MID(A320,FIND(\"_\",A320)+1,FIND(\"_\",A320,FIND(\"_\",A320)+1)-FIND(\"_\",A320)-1)),'ADAUGARE FORME 1'!$C$2:$D$1620,2,0)","Modelul 394 are trei cifre. Extragerea formei intre delimitatori recupereaza codul4010, confirmat de celelalte etape.", "SUPORT OU")

customers=collections.defaultdict(set)
for r in d["NOMEXP02"]:
    code,name=v("NOMEXP02",r,"O"),v("NOMEXP02",r,"P")
    if code and name and int(r)>1:customers[name].add(code)
for r in d["LISGL1"]:
    if int(r)<2:continue
    key=v("LISGL1",r,"D")
    if len(customers[key])==1:
        add("LISGL1","Q"+r,f"=INDEX('NOMEXP02'!$O$2:$O$3615,MATCH(D{r},'NOMEXP02'!$P$2:$P$3615,0))","Beneficiar exact, cu cod unic, recuperat din NOMEXP02 coloanele P si O.",int(next(iter(customers[key]))))

(p/"certain_fixes.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("certain",len(manifest),collections.Counter(x["sheet"] for x in manifest))
print("color unmatched",[(x["cell"],x["old_value"]) for x in manifest if x["sheet"]=="NOMEXP02" and x["cell"].startswith("G") and x["expected_value"] is None])

op_skufixes=[]
for s in ["SORTAT","ARS","GLAZ"]:
    for r in d[s]:
        a=v(s,r,"A")
        if a and re.fullmatch(r"3070_9174_.+_[SAG]",a):
            rr=int(r)
            expected_desc=["FARFURIE DESERT 20","FARFURIE INTINSA 26","BOL 15"]
            if [v(s,rr+k,"B") for k in range(3)]==expected_desc and len({v(s,rr+k,"C") for k in range(3)})==1:
                for k,(model,form) in enumerate([("3070","6003"),("3070","7004"),("3147","1006")]):
                    rn=rr+k
                    suffix=a[-1]
                    new=f"{model}_{form}_{v(s,rn,'C')}_{suffix}"
                    op_skufixes.append({"sheet":s,"cell":"A"+str(rn),"old_formula":None,"old_value":v(s,rn,"A"),"new_formula":f'="{model}_{form}_"&C{rn}&"_{suffix}"',"expected_value":new,"reason":"Componentele setului 9174 sunt ID3070/B3147/1 (ADAUGARE FORME 1 A409). Formele componentelor sunt confirmate exact in NOMU pentru modele3070 si3147."})
(p/"sku_9174_candidates.json").write_text(json.dumps(op_skufixes,ensure_ascii=False,indent=2),encoding="utf-8")
print("sku9174",len(op_skufixes),collections.Counter(x["sheet"] for x in op_skufixes))
for r in d["NOMU"]:
    if v("NOMU",r,"C") in ["3070","3147"] and v("NOMU",r,"D") in ["FARFURIE DESERT 20","FARFURIE INTINSA 26","BOL 15"]:print("NOMU",r,row("NOMU",r))
