from pathlib import Path
import ast,re,json,hashlib
import fitz
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/"04_INSTRUMENTE/export_documente.py").read_text(encoding="utf-8")
tree=ast.parse(source)
env={"re":re}
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {"clean","blocks"}]
exec(compile(ast.Module(body=defs,type_ignores=[]),"<selected-pure-parser-functions>","exec"),env)
inputs=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="files" for t in n.targets))
expected=[]
for name in inputs:
    for kind,value in env["blocks"]((ROOT/name).read_text(encoding="utf-8")):
        if kind=="heading":expected.append(value[1])
        elif kind=="paragraph":expected.append(value)
        else:expected.extend(cell for row in value for cell in row)
doc=Document(ROOT/"Manual_operational_atelier_Dracula_Book.docx")
actual=[]
for child in doc.element.body:
    if child.tag.endswith("}p"):
        value=Paragraph(child,doc).text
        if value:actual.append(value)
    elif child.tag.endswith("}tbl"):
        actual.extend(cell.text for row in Table(child,doc).rows for cell in row.cells)
pdf=fitz.open(ROOT/"Manual_operational_atelier_Dracula_Book.pdf")
norm=lambda s:re.sub(r"\s+","",s)
pdf_text=norm("".join(page.get_text() for page in pdf))
missing=[x for x in expected if norm(x) not in pdf_text]
result={"source_units":len(expected),"docx_body_units":len(actual),"cover_units_excluded":5,"docx_source_order_exact":actual[5:]==expected,"pdf_pages":len(pdf),"pdf_missing_units":missing,"scope":"Structural text comparison, not a literary judgment; parser functions executed without running exporter."}
dest=ROOT/"06_REGISTRU/REZULTATE/COMPARATIE_DOCUMENTE_r03.json"
with dest.open("x",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
if missing or not result["docx_source_order_exact"]:raise SystemExit(2)
