from pathlib import Path
import fitz,json
ROOT=Path(__file__).resolve().parent.parent
doc=fitz.open(ROOT/"Manual_operational_atelier_Dracula_Book.pdf")
bounds=[]; selected=[]
for i,page in enumerate(doc):
    for block in page.get_text("blocks"):
        if block[0]<0 or block[1]<0 or block[2]>page.rect.width+0.5 or block[3]>page.rect.height+0.5:
            bounds.append({"page":i+1,"bbox":block[:4]})
    if any(x in page.get_text() for x in ["Matrice de trasabilitate","Sursele de inspirație","Regula editorială","Regula r03"]):
        selected.append(i)
out=ROOT/"06_REGISTRU/REZULTATE/VIZUAL_R03_v02"
out.mkdir(exist_ok=False)
samples=sorted(set([0]+selected+[len(doc)-1]))
for i in samples:
    doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(out/f"pagina-{i+1}.png")
result={"pages":len(doc),"out_of_page_blocks":bounds,"sample_pages":[i+1 for i in samples],"scope":"Text bounds and rendered samples; not a literary audit. New output only; r02 preserved."}
with (out/"control.json").open("x",encoding="utf-8") as f:
    json.dump(result,f,indent=2)
print(json.dumps(result))
