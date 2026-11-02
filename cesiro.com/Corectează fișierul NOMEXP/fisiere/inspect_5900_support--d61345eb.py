from read_model import load_model,P
import re,json,collections
m=load_model()
for sn,col,codes in [("GLAZURI SETURI","A",["S039","S040","S041"]),("Codificare 1 Glazuri","A",["356L","324L","722L","248L","244L"]),("NOMEXP02","A",["5900_3070_9043"])]:
    print(sn)
    s=m[sn]["cells"]
    for a,c in s.items():
        if re.fullmatch(col+r"\d+",a) and any(str(c["v"]).startswith(k) for k in codes):
            r=int(re.search(r"\d+",a)[0])
            print(r,json.dumps({b:d["v"] for b,d in s.items() if b.endswith(str(r)) and int(re.search(r"\d+",b)[0])==r},ensure_ascii=False))
for r in [3284,3520,3307,3308,3309]:
    s=m["NOMEXP02"]["cells"]
    print("ROW",r,json.dumps({a:c["v"] for a,c in s.items() if int(re.search(r"\d+",a)[0])==r},ensure_ascii=False))
