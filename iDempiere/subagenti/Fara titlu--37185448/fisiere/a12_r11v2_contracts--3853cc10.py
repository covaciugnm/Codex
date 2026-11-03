from a12_r11x_base import *
j=read(P/'A12_inventar_si_receptie_v2.json')
for x in j['bidirectional_transactional_cases']:print(x.get('id'),x.keys(),str(x)[:550])

