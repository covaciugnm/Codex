from pathlib import Path
import json,subprocess
from PIL import Image,ImageOps,ImageDraw,ImageFont
root=Path.cwd();out=root/'08. Corespondenta/2026.10.26 Emailuri primite PDF'
m=json.loads((out/'2026.10.26 Registru conversii email PDF.json').read_text(encoding='utf-8'))
qa=root/'folder map/2026.10.26 QA emailuri PDF';qa.mkdir(exist_ok=True)
pop='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
pages=[]
for x in m['conversii']:
    prefix=qa/f"{x['firma']} {x['data_mesaj']} {x['id_eva'][:8]}"
    subprocess.run([pop,'-scale-to','1400','-png',str(root/x['cale_pdf']),str(prefix)],check=True,capture_output=True)
    for i in range(1,x['pagini']+1):pages.append((qa/(prefix.name+f'-{i}.png'),f"{x['firma']} {x['data_mesaj']} | {i}/{x['pagini']}"))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for n in range(0,len(pages),6):
    sheet=Image.new('RGB',(1220,2670),'#DCE4E8');draw=ImageDraw.Draw(sheet)
    for j,(path,label) in enumerate(pages[n:n+6]):
        im=Image.open(path);im.thumbnail((590,835))
        cx=10+(j%2)*610;cy=10+(j//2)*890
        draw.text((cx,cy),label,fill='#15394D',font=font)
        sheet.paste(im,(cx,cy+27))
    target=qa/f'2026.10.26 Contact {n//6+1}.png';sheet.save(target)
print(json.dumps({'pagini':len(pages),'planse':[str(p) for p in qa.glob('*Contact*.png')]},ensure_ascii=False))
