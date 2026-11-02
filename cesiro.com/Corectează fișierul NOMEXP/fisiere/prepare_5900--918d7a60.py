from read_model import load_model,P
import json,re,collections
m=load_model()
data=json.loads((P/"data_5900.json").read_text(encoding="utf8"))
man=json.loads((P/"audit_date"/"sku5900_manifest.json").read_text(encoding="utf8"))
colors=json.loads((P/"audit_flux"/"color5900_fixes.json").read_text(encoding="utf8"))
rows={r["source_row"]:dict(r["values"]) for r in data["rows"]}
changes=[]
for x in man["changes"]+colors["fixes"]:
    row=int(re.search(r"\d+",x["cell"])[0]);col=re.match("[A-Z]+",x["cell"])[0]
    assert rows[row][col]==x["old_value"],(row,col,rows[row][col],x["old_value"])
    rows[row][col]=x["new_value"]
    source=x.get("evidence") or "; ".join(f"{s[0]}!rând {s[1]}" for s in x.get("source",[]))
    changes.append([x["cell"],x["old_value"],x["new_value"],x["reason"],source])
# The exact glaze 324L has no description in the supplied file.
for x in colors["unresolved"]:
    r=int(x["r"]);base=x["base_names"][0]
    for col in ["C","D","J","S","V"]:
        val=base+"-324L"
        changes.append([f"{col}{r}",rows[r][col],val,"Denumire set recuperată; glazura 324L rămâne explicit de confirmat.","; ".join(f"{s[0]}!rând {s[1]}" for s in x["source"])])
        rows[r][col]=val
    changes.append([f"G{r}",rows[r]["G"],"Descriere lipsă: 324L","Eroare înlocuită cu semnalarea exactă a informației lipsă.","Nicio descriere exactă în fișierul sursă."])
    rows[r]["G"]="Descriere lipsă: 324L"
groups=collections.OrderedDict()
for r,v in rows.items():
    sku=v["A"]
    if sku in groups:
        old=groups[sku]
        assert v==old["values"],sku
        old["source_rows"].append(r)
        changes.append([f"A{r}",sku,sku,"Înregistrare identică după normalizare; consolidată în catalog, păstrată în foaia Original_5900.",f"NOMEXP02!A{old['source_rows'][0]}:AF{old['source_rows'][0]} și A{r}:AF{r}"])
    else:groups[sku]={"values":v,"source_rows":[r]}
assert len(groups)==366
expected=json.loads((P/"audit_date"/"sku5900_expected_control.json").read_text(encoding="utf8"))
assert sorted(groups)==expected["expected_sku_sorted"]
forms=[];glazes=[]
for form in sorted({v["values"]["I"] for v in groups.values()}):
    r=next(r for r in groups.values() if r["values"]["I"]==form)
    choices=[]
    cat=m["ADAUGARE FORME 1"]["cells"]
    for a,c in cat.items():
        if re.fullmatch(r"C\d+",a) and c["v"]==form:
            rr=int(a[1:]);label=cat.get("A"+str(rr),{}).get("v")
            if label:choices.append((label,rr))
    assert choices,form
    label,rr=choices[0]
    pieces=r["values"]["AE"]
    assert int(re.match(r"SET\s*(\d+)",label,re.I)[1])==pieces,(form,label,pieces)
    forms.append([form,label,str(r["values"]["U"]),pieces,f"ADAUGARE FORME 1!A{rr}:C{rr}"])
for glaze in sorted({v["values"]["F"] for v in groups.values()}):
    relevant=[v for v in groups.values() if v["values"]["F"]==glaze]
    descriptions=set(v["values"]["G"] for v in relevant)
    assert len(descriptions)==1,(glaze,descriptions)
    desc=next(iter(descriptions))
    rr=relevant[0]["source_rows"][0]
    src=f"NOMEXP02!F{rr}:G{rr}"
    status="Documentată"
    if glaze in ["S039","S040","S041"]:src=f"GLAZURI SETURI!A{dict(S039=40,S040=41,S041=42)[glaze]}:C{dict(S039=40,S040=41,S041=42)[glaze]}"
    if glaze=="356L":src="NOMEXP02!F2706:G2706; F2944:G2944"
    if glaze=="324L":desc=None;status="De completat";src="Cod existent în NOMEXP02; descriere absentă în cataloage."
    glazes.append([glaze,desc,status,src])
out={"records":list(groups.values()),"original":data,"forms":forms,"glazes":glazes,"changes":changes,
     "stats":{"source_rows":367,"unique_sku":366,"space_sku":18,"model_corrections":3,"merged_duplicates":1,"unresolved_glaze":14,"forms":len(forms),"glazes":len(glazes),"changes":len(changes)}}
(P/"build_5900_data.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(out["stats"],ensure_ascii=False))
