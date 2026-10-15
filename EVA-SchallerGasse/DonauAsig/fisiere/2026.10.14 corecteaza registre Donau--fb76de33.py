from pathlib import Path
import json, hashlib, shutil
root=Path(__file__).resolve().parent.parent
case=root/'05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau'
archive=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
marker='2026.10.14 — CORECȚIE DONAU: somația de o lună; durata X712 neidentificată'
status=('Corecție materială: somația DONAU din 2026.05.20 acordă o lună; a fost adresată fostului titular prin Hofhans, ștampilată la 2026.05.26 și retransmisă de Capra la 2026.05.27. '
        'Se retrage premisa din analiza anterioară că singura somație cunoscută acordă două săptămâni. Nu se poate deduce nerespectarea termenului de o lună numai din somația din iunie. '
        'Rămân de verificat recepția, mandatul Hofhans, cunoașterea transferului de către DONAU și efectele somațiilor pe fiecare ramură. '
        'Polița X712.261-2 propriu-zisă nu a fost identificată; durata sa rămâne necunoscută. Expirarea 2036.01.01 apare deja în polița emisă fostului titular la 2026.02.03. '
        'Transferul nu reîncepe automat durata (§69); prelungirea tacită este de cel mult un an (§8(1), ABS14). Temeiul unui acord valabil pentru 2036 trebuie documentat, inclusiv eventualul §5.')
next_step=('Obținerea poliței X712 integrale, a ultimelor acte anterioare anului 2026, a acordului și mandatului pentru expirarea 2036 și a dovezilor de comunicare; '
           'verificarea celor două somații și a situației de plată. Cererea locală și ciorna Eva-Mail din 2026.10.07 sunt NETRIMISE; această actualizare nu trimite emailuri și nu confirmă plăți.')
source_names=['2026.10.14 Concluzie auditata durata X712 si 2036.txt','2026.10.14 01 Incetarea politei Donau.pdf','2026.10.14 02 Neplata si acoperirea Donau.pdf','2026.10.14 Audit juridic si editorial.txt']
sources=[(case/n).relative_to(root).as_posix() for n in source_names]
note=(marker+'\n\nStatus scurt: '+status+'\n\nUltimul răspuns verificat: DONAU 2026.10.06, ID 2c273256-a0bf-408b-bb22-09718372e888; '
      'menține contractul și afirmă lipsa acoperirii. Această actualizare reverifică documente anterioare; nu reprezintă un răspuns nou al DONAU.\n\nUrmătorul pas: '+next_step+
      '\n\nSursă nou identificată în dosarul juridic: 05. Asigurari/Asigurare cladire/20260526163520179.pdf; SHA-256 8402921829c72536eabb94f8770ca913f7eefcfec1fe584206c62eea4415c791. '
      'Email primit 2026.05.27, Eva-Mail cb505d08-3562-4ad6-a659-ed10ce34b02d; JSON cu expeditor, destinatari, CC și atașamente salvat în Surse.\n\nSurse curente:\n'+'\n'.join(sources)+'\n\n')
def preserve(p):
    dest=case/'Istoric'/'2026.10.14 Inainte de corectia somatiei mai'/p.relative_to(root)
    dest.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and not dest.exists(): shutil.copy2(p,dest)
def prepend(p,prefix=''):
    old=p.read_text(encoding='utf-8-sig') if p.exists() else ''
    if marker in old:return
    preserve(p)
    p.write_text(prefix+note+'ISTORIC DEPĂȘIT ÎN PRIVINȚA SOMAȚIEI DIN MAI — corecția de mai sus prevalează\n\n'+old,encoding='utf-8-sig')
for n in ['2026.10.14 Status proiect.txt','2026.10.14 Log progres proiect.txt']:prepend(root/n)
for partner in ['Donau Versicherung','Maritczak - Commerz Inkasso','CERHA HEMPEL']:
    prepend(archive/'Parteneri'/f'2026.10.14 Log discutii - {partner}.txt')
prepend(root/'folder map/README.md', '# ')
prepend(case/'2026.10.14 Jurnal actualizare.txt')
prepend(root/'05. Asigurari/Asigurare cladire/2026.10.14 Situatie Donau/2026.10.14 Situatie actuala Donau.txt')
registry_path=archive/'2026.10.14 Registru comunicatii.json'
preserve(registry_path)
registry=json.loads(registry_path.read_text(encoding='utf-8-sig'))
updates=registry.setdefault('actualizari_punctuale',[])
if not any(x.get('subiect')==marker for x in updates):updates.append({'data':'2026.10.14','subiect':marker,'status':status,'urmatorul_pas':next_step,'surse':sources,'nota':'Reverificare documentară; zero mesaje trimise, zero plăți; numărătorii emailurilor nu se modifică.'})
for entry in registry.get('statusuri',[]):
    if entry.get('partener')=='Donau Versicherung':entry['analiza_juridica_2026_10_14']={'status':status,'urmatorul_pas':next_step,'surse':sources}
registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[{'fisier':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'data_lizibila':'2026.10.14'} for p in [case/n for n in source_names]]
(case/'2026.10.14 Manifest livrabile finale.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'corectie inregistrata','livrabile':manifest},ensure_ascii=False))
