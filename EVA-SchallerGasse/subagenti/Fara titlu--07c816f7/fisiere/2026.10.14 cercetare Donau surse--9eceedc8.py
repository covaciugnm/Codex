from pathlib import Path
import fitz, hashlib, json, urllib.request, re
base=Path.cwd(); out=base/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau/Surse'; out.mkdir(parents=True,exist_ok=True)
items=[]
for name,tag in [('814BC40FC7831FE197E21FDA1089ECC3_Polizzenkopie.pdf','Polita curenta'),('Schalle_1080_DON_SHU_2044001194_2939905718.pdf','Polita istorica conditii')]:
 p=base/'05. Asigurari/Asigurare cladire'/name; d=fitz.open(p); pages=[x.get_text() for x in d]
 (out/f'2026.10.14 {tag} text integral.txt').write_text('\n\n'.join(f'--- PDF PAGINA {i+1} ---\n'+s for i,s in enumerate(pages)),encoding='utf-8')
 items.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'pages':len(d)})
 chosen=[0,5,6,7,8] if len(d)==9 else [0,8,11,34,36,40,41,71,72,73]
 for idx in chosen:
  if idx<len(d): d[idx].get_pixmap(matrix=fitz.Matrix(1,1)).save(out/f'2026.10.14 {tag} p{idx+1}.png')
idx=json.loads((base/'folder map/inventar.json').read_text(encoding='utf-8'))
(out/'2026.10.14 Verificare hash originale cercetare.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(items,ensure_ascii=False))
