from pathlib import Path
import json,shutil,textwrap
I=Path('00.Proiect/09. Vertraege/2026.10.13 PECH R09 - intern')
P=Path('00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Werkvertrag R09')
src=I/'2026.10.13 Werkvertrag PECH R09.json'
shutil.copy2(src,I/'2026.10.13 Werkvertrag PECH R09 sursa initiala.json')
d=json.loads(src.read_text(encoding='utf-8'))
d['annexes'][3]['paragraphs'][4]=d['annexes'][3]['paragraphs'][4].replace('im Grundhonorar sind zwölf','im Grundhonorar zwölf')
d['sections'][6]['paragraphs'][2]+=' Der eigene Abnahmevermerk wird binnen zwei Werktagen nach dem jeweiligen Termin übermittelt.'
src.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(src,P/src.name)
body=I/'2026.10.13 Email PECH R09 body fara semnatura.txt'
text=body.read_text(encoding='utf-8').strip()
body.write_text('\n\n'.join(textwrap.fill(p,width=88,break_long_words=False,break_on_hyphens=False) for p in text.split('\n\n'))+'\n',encoding='utf-8')
shutil.move(str(P/'2026.10.13 Werkvertrag PECH R09.pdf'),str(I/'2026.10.13 Werkvertrag PECH R09 PDF initial.pdf'))
print('Two audit corrections; body wrapped at 88 characters; initial PDF preserved.')
