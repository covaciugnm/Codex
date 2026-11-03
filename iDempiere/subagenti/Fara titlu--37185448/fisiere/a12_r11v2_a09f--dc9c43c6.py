from a12_r11x_base import *
for f in sorted((O/'A09/fise').glob('*.json')):
 j=read(f);print(f.name,json.dumps(j,ensure_ascii=False)[:4200])

