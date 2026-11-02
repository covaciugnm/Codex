from pathlib import Path
import hashlib, json, shutil, requests
root=Path.cwd()
folder=root/'05. Asigurari/Asigurare cladire/2026.10.29 Renuntare componente Donau'
backup=folder/'Istoric jurnale'
backup.mkdir(exist_ok=True)
entry='''2026.10.29 — DONAU: drepturi pentru eliminarea componentelor
Status scurt: analiză legală și contractuală; nu există drept general de rescriere unilaterală a pachetului. Ramurile pot fi independente, dar termenul propriu rămâne aplicabil. §41a/§42 pot impune reducerea primei pentru perioade viitoare dacă dispar împrejurările tarifare; §68/§68a privesc dispariția reală a interesului. Clauzele1242K/3031K conțin drepturi parțiale de încetare pentru suplimentele vizate, distincte de Leitungswasser/Mieten-BU.
Ultimul răspuns: PRIMIT DONAU2026.10.29, Eva8f1be79a-83fc-4713-9ff0-bc5e3e4f4cd7, confirmă plata primită și acoperirea actuală. Propunerea Pfeiffer2026.07.14 permite excluderea apei și Mieten-BU pentru Risikowegfall, condiționat de probe; nu confirmă eliminarea sau creditul. Corespondența și anexele sunt păstrate în dosarul2026.10.29 Raspuns Donau; verificarea de față reutilizează aceste surse, fără o nouă sincronizare email.
Următorul pas: cerere motivată către DONAU pe fiecare ramură — clauza de separare/încetare, faptele tarifare, probe relevante sau echivalente, data efectului și calculul. Nu se condiționează automat pierderea chiriilor de certificatul pentru apă. Pentru acoperiri noi este necesară oferta și acceptarea, fără resetarea tacită a duratei. Nicio notificare sau modificare nu a fost trimisă/acceptată prin această analiză.
Sursă: 05. Asigurari/Asigurare cladire/2026.10.29 Renuntare componente Donau/2026.10.29 Concluzie juridica - eliminarea componentelor.txt; note de cercetare, contract și audit; surse RIS integrale cu registre și hashuri. Paginile1–3 RV rămân lipsă. Datele de valabilitate și sumele nu sunt schimbate de raport.
'''
targets=[root/'2026.10.29 Status proiect.txt',root/'2026.10.29 Log progres proiect.txt',root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - Donau Versicherung.txt']
for p in targets:
    old=p.read_text(encoding='utf-8-sig')
    if entry.splitlines()[0] in old: continue
    dest=backup/(p.stem+' - inainte componente'+p.suffix)
    if dest.exists(): raise RuntimeError('Backup exists: '+str(dest))
    shutil.copy2(p,dest)
    p.write_text(entry+'\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
readme=root/'folder map/README.md'
old=readme.read_text(encoding='utf-8-sig')
heading='## 2026.10.29 — DONAU: eliminarea componentelor'
if heading not in old:
    shutil.copy2(readme,backup/'2026.10.29 README inainte componente.md')
    addition=heading+'\n\nAnaliza și auditul sunt în `05. Asigurari/Asigurare cladire/2026.10.29 Renuntare componente Donau`. Intrare: `2026.10.29 Concluzie juridica - eliminarea componentelor.txt`. Distinge încetarea parțială, reducerea legală a primei, dispariția interesului și modificarea prin acord. Drepturile1242K/3031K nu se transferă automat ramurii apă din conducte sau chiriilor. Niciun email expediat și nicio componentă eliminată prin raport. Sursele email rămân în dosarul răspunsului DONAU din aceeași dată; precedentele RIS sunt salvate integral.\n\n'
    readme.write_text(addition+old,encoding='utf-8')
(folder/'2026.10.29 Jurnal actualizare componente.txt').write_text(entry,encoding='utf-8')
url='https://ris.bka.gv.at/eli/jgs/1811/946/P879/NOR12018602'
r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=45)
r.raise_for_status()
p=folder/'Surse/2026.10.29 ABGB 879.html'
p.write_bytes(r.content)
(folder/'Surse/2026.10.29 Registru sursa ABGB.json').write_text(json.dumps({'url':url,'consultat':'2026.10.29','path':str(p.relative_to(root)),'sha256':hashlib.sha256(r.content).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
print('Jurnale și README actualizate; istoricul păstrat; sursa ABGB salvată.')
