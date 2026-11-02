from a12_r8_jvm import *
ss=['TestT211Adaptoare','TestT211Garda','TestT35Canale','TestT353Trimitere','TestT22VanzariOnline','TestT22Ecran','TestT22Mapare']; 
with ThreadPoolExecutor(max_workers=4)as px:values=list(px.map(go,[(t,n)for n in ss for t in ('git','instalat')]))
wr(J/'Executii_supliment.json',values);print(len(values),sum(x['traced']for x in values),sum(x['exit']==0 for x in values))

