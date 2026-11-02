from pathlib import Path
import json
ROOT=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
OUT=ROOT/'08. Corespondenta/2026.10.11 Verificare zilnica'
p=OUT/'2026.10.11 Dovezi cautari si audit.json';j=json.loads(p.read_text(encoding='utf-8'))
j['audit_local']['new_pdf']['verificare_finala']={'data_lizibila':'2026.10.11','pagini_identificate_vizual':39,'pagini_citite_detaliat':[1,2,3,4,5,6,10,11,16,18,22,26,30,34,37],'rezultat':'Compilație istorică mixtă. Nu au fost identificate acte ori decizii după2026.10.08. OfertaREALIG2026.03.26 există deja separat; restul documentelor observate nu sunt comunicări noi de proiect. FormularWienerWasser necompletat. Nu este audit juridic/financiar al altor dosare.'}
p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
extra='\n2026.10.11 | Completare audit local\nAu fost identificate vizual toate39pagini ale Inbox/Documente-germana.pdf, cu citire detaliată a paginilor1–6,10–11,16,18,22,26,30,34 și37. Nu sunt identificate acte după2026.10.08. Este compilație istorică mixtă; ofertaREALIG2026.03.26 există deja separat. FormularulWienerWasser este necompletat. Fișierul nu constituie o comunicare externă nouă. Auditul privește identificarea documentelor, nu evaluarea juridică/financiară a altor dosare.\n'
for path in [OUT/'2026.10.11 Raport verificare.txt',ROOT/'2026.10.11 Status proiect.txt',ROOT/'2026.10.11 Log progres proiect.txt']:
    text=path.read_text(encoding='utf-8');path.write_text(extra+'\n'+text,encoding='utf-8')
print('Audit local completat; originalele nemodificate.')
