from a12_r11x_base import *
p=O/'A10';print(read(p/'Raport_A10_R11.json'))
for f in p.rglob('Fisa*.json'):
 j=read(f);print(f.name,j)
print('fise',list((p/'fise').glob('*')))
print('manifest',str(read(p/'Manifest_A10_R11.json'))[:1700])
r=read(E/'R10/Registru_reexecutare_R10.json')['rows']
for x in r:
 if x['task']=='T32':print(x['criterion'],x['text'][:250])

