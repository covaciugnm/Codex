from a12_r11x_base import *
for f in sorted((O/'A11').glob('Verdict*.json')):
 j=read(f);print('\n'+f.name,sha(f));print(json.dumps(j,ensure_ascii=False)[:21000])
for a in ['A02','A03','A04','A05','A07','A08']:
 ps=sorted((O/a).glob('Manifest*.json'));print('\n',a)
 for p in ps:
  j=read(p);print(p.name,sha(p),str(j)[:1600])

