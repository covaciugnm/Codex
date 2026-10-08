from pathlib import Path
import json,hashlib,html,re,gzip,zipfile
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from pypdf import PdfReader

BASE=Path(__file__).parent
ROOT=BASE/'Analiza_iDempiere_HR_SSM_SU_2026-10-08'
REG=ROOT/'08_Registre_si_verificari'
sources=json.loads((REG/'registru_surse.json').read_text(encoding='utf8'))
ok=[s for s in sources if s['stare']=='DESCARCAT']
bad=[s for s in sources if s['stare']!='DESCARCAT']
ROOT.joinpath('README.md').write_text('''# Analiză iDempiere, HR și SSM/SU pentru România

Data cercetării: **8 octombrie 2026**. Raport de **28 de pagini**, comparații tabelare și bibliotecă de **308 surse descărcate din 328 de înregistrări**. Cele 20 de încercări nereușite sunt explicate separat; două au alternative recuperate. Numărul include pagini de manual, cod, licențe, prezentări și acte normative, nu 308 manuale distincte.

## Începeți aici

- [Raport PDF](01_Raport/Analiza_iDempiere_HR_SSM_SU.pdf)
- [Raport HTML cu cuprins și surse](01_Raport/Analiza_iDempiere_HR_SSM_SU.html)
- [INDEX.html — bibliotecă filtrabilă și legături locale](INDEX.html)
- [Limite și materiale indisponibile](08_Registre_si_verificari/limite_si_materiale_indisponibile.html)
- [Registrul complet al surselor](08_Registre_si_verificari/registru_surse.json)

Descărcați și dezarhivați întregul pachet, apoi deschideți `INDEX.html` în browser. GitHub afișează unele fișiere HTML ca sursă; funcțiile de filtrare și fișele editabile se utilizează din copia locală. Legăturile externe necesită internet.

## Conținut

| Folder | Conținut |
|---|---|
| 01_Raport | Analiză în română, PDF și HTML, conținut structurat JSON |
| 02_iDempiere | Surse iDempiere și 25 de interfețe de model HR din release 13 |
| 03_HR | Frappe HR, Axelor și Apache OFBiz |
| 04_SSM_SU | SSM.ro, SSMatic și SafeHub |
| 05_Extensii_HR_iDempiere | Module și implementări HR internaționale |
| 06_Legislatie | Surse legislative publice și evidența limitelor de recuperare |
| 07_Anexe_tehnice | Cerințe, registru de acceptanță, întrebări furnizori, cost total, SQL de inventariere și inventar de 757 de modele iDempiere |
| 08_Registre_si_verificari | Proveniență, starea descărcărilor și verificarea integrității |

## Concluzii de lucru

Frappe HR este prima opțiune de pilot pentru o aplicație HR separată. Axelor și OFBiz sunt alternative Java, cu diferențe importante de acoperire și efort de integrare. Pentru păstrarea HR în iDempiere, evaluați întâi modulele CDSoftware; AMERPSOFT necesită clarificări distincte de licență și compatibilitate. Structurile HR existente în codul iDempiere nu dovedesc singure existența unui motor salarial complet.

SSM.ro are cea mai amplă documentație publică și un API documentat dintre cele trei soluții SSM selectate. Nu s-a confirmat o soluție SSM/SU completă, open source, gratuită integral și demonstrată ca acoperind toate obligațiile aplicabile firmei în România. Gratuitatea codului HR nu include automat găzduirea, implementarea, localizarea și mentenanța. Integrarea și compatibilitatea nu au fost testate într-un sistem de producție.

În tabele, **NC** înseamnă neconfirmat din sursele consultate; nu înseamnă automat că funcția lipsește. Funcțiile declarate comercial sunt diferențiate de cele descrise într-un manual sau confirmate structural în cod. Referința iDempiere este release 13; inventarul este legat de commitul indicat în anexă. Nu este un audit al instalării beneficiarului.

## Limba și documentația offline

Analiza, explicațiile, registrele și anexele create sunt în **română**. Documentele originale ale autorilor sunt păstrate în limba publicării, fără traducere integrală. Copiile HTML de lectură păstrează textul, tabelele și legăturile; elimină scripturile, imaginile externe și interfețele interactive. Originalele HTML comprimate `.original.html.gz` sunt păstrate pentru proveniență. PDF-urile originale sunt descărcate ca fișiere. Licențele și drepturile fiecărei surse rămân ale autorilor.

Biblioteca acoperă materialele publice identificate și accesibile, fără a pretinde toate edițiile istorice, limbile, manualele private sau conținutul blocat de servere. Registrul listează exact URL-urile, rezultatele, fișierele și hashurile. Actele și formele aplicabile, circuitul semnăturilor și cerințele concrete ale firmei se validează pentru implementarea efectivă.

## Utilizarea anexelor

Fișele HTML din `07_Anexe_tehnice` permit completare locală și salvare/printare. Registrul de acceptanță conține scenarii propuse, nu teste declarate executate. Întrebările pentru furnizori sunt pregătite, fără a fi trimise. Scriptul SQL efectuează interogări de dicționar în tranzacție read-only; nu a fost rulat pe baza firmei. Parcurgeți-l înainte de utilizare cu un cont de citire.

`SHA256SUMS.txt` conține hashurile tuturor fișierelor din dosar, cu excepția sa. Arhiva ZIP este livrată separat, pentru a evita includerea recursivă. Cheile SSH și credențialele nu fac parte din pachet.
''',encoding='utf8')
notes={'ID15':'Alternativă recuperată: ID15B, fișierul LICENSE.md din depozitul oficial.','LG04':'Alternativă recuperată: LG05, pagina oficială HG 1425/2006.','FRX002':'Legătură din manual care a returnat 404; nu există copie locală a acestei pagini.'}
rows=''.join('<tr><td>'+html.escape(s['id'])+'</td><td>'+html.escape(s['titlu'])+'</td><td>'+html.escape(s.get('eroare',''))+'</td><td><a href="'+html.escape(s['url'])+'">Sursă originală</a></td><td>'+html.escape(notes.get(s['id'],'Serverul a refuzat descărcarea automată. Legătura este păstrată pentru consultare online.'))+'</td></tr>' for s in bad)
(REG/'limite_si_materiale_indisponibile.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Limite și materiale indisponibile</title><style>body{font:16px Arial;margin:35px;line-height:1.5}table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:9px;text-align:left}th{background:#eee}</style><body><a href="../INDEX.html">Indexul dosarului</a><h1>Limite și materiale indisponibile</h1><p>308 surse recuperate și 20 de încercări nereușite. Aceste înregistrări nu sunt prezentate ca documentație descărcată. ID15 și LG04 au alternative recuperate. Erorile sunt cele constatate la data cercetării, nu o afirmație că materialul nu poate fi accesat niciodată.</p><table><tr><th>ID</th><th>Material</th><th>Rezultat</th><th>Legătură</th><th>Alternativă sau limită</th></tr>'+rows+'</table><p>SSMatic și SafeHub: sunt incluse paginile publice identificate; nu a fost găsit un manual tehnic public comparabil cu ghidul SSM.ro. Nu au fost descărcate materiale private sau autentificate. Documentațiile sunt instantanee; paginile online pot evolua.</p></body></html>',encoding='utf8')
ROOT.joinpath('NOTA_DREPTURI.txt').write_text('Materialele originale aparțin autorilor și furnizorilor indicați în registrul surselor. Copiile sunt colectate pentru documentarea și evaluarea proiectului. Disponibilitatea publică nu transferă drepturile de autor și nu acordă o licență suplimentară de reutilizare. Pentru cod și software se aplică licența exactă a proiectului și versiunii; pentru documentații se aplică condițiile autorilor. Nu este inclusă o licență globală care ar înlocui aceste condiții.\n',encoding='utf8')
index=ROOT/'INDEX.html'
txt=index.read_text(encoding='utf8')
if 'limite_si_materiale_indisponibile.html' not in txt:
    txt=txt.replace('<body>','<body><p><a href="README.md">Ghid de utilizare</a> · <a href="08_Registre_si_verificari/limite_si_materiale_indisponibile.html">Materiale indisponibile și alternative</a></p>',1)
    index.write_text(txt,encoding='utf8')
errors=[]; hashes=0; pdfs=0
for s in ok:
    for fkey,hkey in [('fisier','sha256'),('original','sha256_original')]:
        if s.get(fkey):
            p=ROOT/s[fkey]
            if not p.exists():errors.append('Lipsă: '+s[fkey]);continue
            payload=gzip.decompress(p.read_bytes()) if fkey=='original' else p.read_bytes()
            if hashlib.sha256(payload).hexdigest()!=s[hkey]:errors.append('Hash diferit: '+s[fkey])
            hashes+=1
links=0
own=[ROOT/'INDEX.html',ROOT/'01_Raport/Analiza_iDempiere_HR_SSM_SU.html',REG/'limite_si_materiale_indisponibile.html']+list((ROOT/'07_Anexe_tehnice').glob('*.html'))
for p in own:
    for a in BeautifulSoup(p.read_text(encoding='utf8'),'html.parser').find_all('a',href=True):
        h=a['href'];u=urlsplit(h)
        if u.scheme or h.startswith('#') or not u.path:continue
        target=(p.parent/unquote(u.path)).resolve();links+=1
        if not target.exists():errors.append('Legătură lipsă: '+str(p.relative_to(ROOT))+' -> '+h)
for p in ROOT.rglob('*.pdf'):
    n=len(PdfReader(p).pages);pdfs+=1
    if n==0:errors.append('PDF fără pagini: '+str(p))
secret_hits=[]
patterns=[rb'-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----',rb'ghp_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{40,}']
for p in ROOT.rglob('*'):
    if not p.is_file():continue
    b=p.read_bytes()
    if p.suffix=='.gz':b=gzip.decompress(b)
    if any(re.search(pat,b) for pat in patterns):secret_hits.append(str(p.relative_to(ROOT)))
assert not secret_hits,secret_hits
assert not errors,errors
report={'data':'2026-10-08','pagini_raport':28,'surse_recuperate':len(ok),'incercari_nereusite':len(bad),'hashuri_surse_verificate':hashes,'legaturi_locale_verificate':links,'pdf_uri_citite':pdfs,'erori':errors,'scanare_chei_private_si_tokenuri_github':'Nicio potrivire','verificare_vizuala':'Toate cele 27 pagini inițiale inspectate; după actualizare, paginile 15, 17 și 18 inspectate din nou. Pagina nouă 18 verificată fără suprapuneri sau decupări.','teste_aplicatii':'Nu au fost executate; dosarul conține cercetare documentară și scenarii de acceptanță.'}
(REG/'verificare_finala.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
manifest=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.txt':manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix())
ROOT.joinpath('SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n',encoding='utf8')
archive=BASE/(ROOT.name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for n in z.namelist():assert z.read(n)==(BASE/n).read_bytes(),n
print(json.dumps({'verificare':report,'fisiere':len(manifest)+1,'arhiva_octeti':archive.stat().st_size,'arhiva_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
