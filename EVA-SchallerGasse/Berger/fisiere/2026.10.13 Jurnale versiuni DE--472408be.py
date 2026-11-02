from pathlib import Path
import json,hashlib,shutil
ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
V=ROOT/'00.Proiect/09. Vertraege'
H=V/'2026.10.13 Istoric inainte versiune DE'
H.mkdir(parents=True,exist_ok=True)
def rel(p):return p.relative_to(ROOT).as_posix()
def readj(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def writej(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def backup(p):
 target=H/p.name
 if target.exists(): assert target.read_bytes()==p.read_bytes(),'Backup existent diferit'
 else:shutil.copy2(p,target)
def prepend(p,text):
 backup(p)
 p.write_text(text+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
manifest=V/'2026.10.13 Versiuni contracte numai germana.json'
m=readj(manifest)
for row in m['documente']:
 provider=row['prestator']
 assert hashlib.sha256((ROOT/row['docx']).read_bytes()).hexdigest()==row['sha256']
 assert hashlib.sha256((ROOT/row['pdf']).read_bytes()).hexdigest()==row['pdf_sha256']
 row.update(verificare_vizuala='PASS; fiecare pagină verificată individual la rezoluție originală',pagini_verificate=list(range(1,row['pagini']+1)),pret_net_EUR=45000 if provider=='BERGER' else 69300,pret_brut_EUR=54000 if provider=='BERGER' else 83160)
 dest=(ROOT/row['docx']).parent
 registry=dest/'2026.10.13 Registru salvare contract.json'
 rr=readj(registry)
 rr.update(versiune_curenta=row,limba='Versiune curentă numai în germană; versiunea anterioară cu sinteză română păstrată',verificare_text='Toate blocurile germane și tabelele identice cu sursa; eliminată numai introducerea RO',audit=rel(V/'2026.10.13 Audit versiuni germane.txt'))
 for format,key in [('docx','sha256'),('pdf','pdf_sha256')]:
  p=ROOT/row[format]
  rr['fisiere'].append(dict(fisier=p.name,cale=rel(p),sha256=row[key],octeti=p.stat().st_size,tip='Contract doar germană'))
 writej(registry,rr)
writej(manifest,m)
audit=(
'2026.10.13 | Verificare versiuni contracte numai în germană\n\n'
'BERGER: eliminate15 paragrafe introductive românești. Păstrate134 blocuri incl.sectPr și5 tabele. Textul german și tabelele sunt identice cu sursa. '
'16 pagini PDF verificate individual la rezoluție originală de auditor_juridic; fără defecte vizuale.\n'
'PECH: eliminate12 paragrafe introductive românești. Păstrate159 blocuri incl.sectPr și7 tabele. Textul german și tabelele sunt identice cu sursa. '
'22 pagini PDF verificate individual la rezoluție originală de contract_pech; fără defecte vizuale.\n'
'Prima pagină începe cu Werkvertrag; eliminată proprietatea de salt înaintea titlului inițial. Footerul este numerotat de la1; toate paginile sunt consecutive.\n'
'PDFurile provin din DOCXurile finale exportate în Microsoft Word, read-only, cu macrocomenzile dezactivate; paginile PNG sunt generate prin rendererul skill Documents cu adaptor nativePDF și Poppler la135dpi. '
'Prima încercare rasterizare nu avea Poppler în PATH; reluarea cu calea runtimebundled a reușit.\n'
'Corelarea SHA-256, verificarea corpului/tabelelor și prezența/numărătoarea paginilor au trecut. '
'Nicio schimbare a sumelor, clauzelor sau termenelor contractuale. Denumirile fișierelor ofertei originale citate în Anlage5 sunt păstrate ca referințe bibliografice. '
'Anlage5 se află separat în fiecare dosar și are hash identic cu sursa.\n'
'Statut: propuneri NETRIMISE și NESEMNATE; acceptarea nu este confirmată. Niciun email ori original Eva nou; numărătorile802/826/783 neschimbate.\n'
f'Registru: {rel(manifest)}\n')
(V/'2026.10.13 Audit versiuni germane.txt').write_text(audit,encoding='utf-8')
intro=(
'2026.10.13 | Contracte BERGER și PECH numai în germană în dosarele aferente\n'
'Status scurt: salvate și verificate versiunile doar în germană, fără introducerea/sinteza română. BERGER16 pagini și PECH22 pagini în PDF; Word editabil. '
'Sumele, textul german, tabelele, clauzele și termenele sunt păstrate integral față de propunerile2026.10.12. '
'BERGER45.000 EUR net/54.000 EUR brut; PECH69.300 EUR net/83.160 EUR brut. '
'Ambele rămân NETRIMISE și NESEMNATE; nicio acceptare dedusă.\n'
'Ultimul răspuns: această operațiune este locală, fără comunicare nouă de la prestatori; ultimele răspunsuri externe sunt păstrate în istoricul de mai jos.\n'
'Următorul pas: lectura versiunilor germane și completarea/confirmarea punctelor deschise înaintea eventualei semnări.\n'
f'Sursă: {rel(manifest)}; {rel(V/"2026.10.13 Audit versiuni germane.txt")}\n'
'Dosare: 00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Propunere contract; 00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Propunere contract. '
'În fiecare sunt contractul Word/PDF, oferta originală Anlage5, mesajul primit și auditul. Versiunile anterioare și sursele comune sunt păstrate.\n'
'Numărători arhivă Eva neschimbate802mesaje/826originale/783documentare. Nicio trimitere, semnare sau plată.')
for suffix in ['Status proiect.txt','Log progres proiect.txt']: prepend(ROOT/('2026.10.13 '+suffix),intro)
BASE=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
reg=BASE/'2026.10.13 Registru comunicatii.json'
backup(reg); r=readj(reg)
r['actualizari_punctuale'].append(dict(data='2026.10.13',tip='organizare_si_versiuni_contracte_DE',sursa=rel(manifest),mesaje_noi=0,originale_noi=0,trimiteri=0,semnaturi=0,plati=0,statut='NETRIMISE/NESEMNATE; eliminată numai introducerea română',destinatii={x['prestator']:x['docx'] for x in m['documente']}))
writej(reg,r)
for provider,pname,last in [('BERGER','Markus Berger','2026.08.17'),('PECH','Pech','2026.09.17')]:
 row=next(x for x in m['documente'] if x['prestator']==provider)
 p=BASE/'Parteneri'/('2026.10.13 Log discutii - '+pname+'.txt')
 block=(f'2026.10.13 | {provider} versiune de contract doar în germană\n'
 f'Status scurt: Word și PDF salvate în dosarul propriu, fără introducerea în română;{row["pagini"]}pagini PDF. Textul contractual și tabelele identice cu sursa. '
 'Propunere NETRIMISĂ și NESEMNATĂ; acceptare neconfirmată.\n'
 f'Ultimul răspuns extern: {last}; acest pas nu adaugă niciun mesaj primit/trimis.\n'
 'Următorul pas: lectura variantei germane, confirmarea condițiilor și punctelor deschise înaintea eventualei semnări.\n'
 f'Surse: {row["docx"]}; {row["pdf"]}; {rel(manifest)}\n')
 prepend(p,block)
README=ROOT/'folder map/README.md'
backup(README)
header=(
'# 2026.10.13 — Contracte BERGER și PECH numai în germană\n\n'
'Versiuni curente fără introducerea română: ../00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Propunere contract/2026.10.13 Werkvertrag BERGER DE.docx și PDF(16pagini); '
'../00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Propunere contract/2026.10.13 Werkvertrag PECH DE.docx și PDF(22pagini). '
'În fiecare dosar sunt și oferta originală Anlage5, mesajul sursă și auditul. Sumele și întregul contract german sunt păstrate identic; doar sinteza română este eliminată. '
'NETRIMISE/NESEMNATE. Registru: ../00.Proiect/09. Vertraege/2026.10.13 Versiuni contracte numai germana.json. '
'Jurnalele și registrul proiectului sunt actualizate; istoricul, versiunea cu sinteză română și sursele comune sunt păstrate. Nu sunt comunicări noi sau plăți.\n')
README.write_text(header+'\nISTORIC PĂSTRAT\n\n'+README.read_text(encoding='utf-8-sig'),encoding='utf-8')
print(json.dumps(dict(status='PASS',documente=m['documente'],arhiva_Eva=r['acoperire']['mesaje_salvate']),ensure_ascii=False,indent=2))

