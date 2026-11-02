from a12_r10_publish import *
import gzip
p=E/'R11_plan_delta';d=rd(p/'Inventar_delta_1632.json');print(list(d));rows=d.get('rows',d.get('paths',[]));print('rows',len(rows),str(rows[:1])[:450]);print([z for z in rows if any(k in str(z)for k in ['SursaCesiro1.java','FisaCanalProces.java'])][:1]);print('live tech',list(rd(B/'Inventar_tehnic.json')));f=next((p).glob('Catalog_Git_integral*.gz'));print('catalog',gzip.open(f,'rt',encoding='utf8').readline()[:540]);print('history',list(rd(E/'A12_istoric_git_stari.json')),str(rd(E/'A12_istoric_git_stari.json'))[:350])

