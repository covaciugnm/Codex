from pathlib import Path
import fitz,json
ROOT=Path(__file__).resolve().parent.parent
doc=fitz.open(ROOT/"Manual_operational_atelier_Dracula_Book.pdf")
bounds=[];selected=[]
for i,page in enumerate(doc):
    for block in page.get_text("blocks"):
        if block[0]<0 or block[1]<0 or block[2]>page.rect.width+0.5 or block[3]>page.rect.height+0.5:
            bounds.append({"page":i+1,"bbox":block[:4]})
    text=page.get_text()
    if any(x in text for x in ["Matrice de trasabilitate","Sursele de inspirație","Regula editorială"]):selected.append(i)
out=ROOT/"06_REGISTRU/REZULTATE/VIZUAL_R02"
out.mkdir(exist_ok=True)
for i in [0]+selected[:3]:
    doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(out/f"pagina-{i+1}.png")
result={"pages":len(doc),"out_of_page_blocks":bounds,"sample_pages":[i+1 for i in [0]+selected[:3]],"scope":"Text bounds and rendered samples, not literary audit."}
(out/"control.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result))

