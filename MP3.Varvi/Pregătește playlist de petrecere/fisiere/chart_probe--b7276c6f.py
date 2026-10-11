import requests,urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings()
r=requests.get('https://www.officialcharts.com/artist/21275/queen/',verify=False,timeout=30)
s=BeautifulSoup(r.text,'html.parser')
a=next(a for a in s.select('a[href]') if '/songs/queen-seven-seas-of-rhye/' in a['href'])
for p in list(a.parents)[:6]:print(p.name,p.get('class'),p.get_text(' ',strip=True)[:400])
