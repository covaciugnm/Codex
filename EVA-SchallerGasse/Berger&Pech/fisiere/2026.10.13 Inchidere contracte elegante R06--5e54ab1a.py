from pathlib import Path
import json, hashlib, shutil
from pypdf import PdfReader

ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
DATE='2026.10.13'
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
BASE=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH'
OUT=BASE/f'{DATE} R06 propuneri negociere'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def rec(p): return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,s): assert not p.exists(),p; p.write_text(s,encoding='utf-8')

previous=read(WORK/f'{DATE} Registru audit comparativ final R05.json')
for r in previous['contracte']: assert sha(ROOT/r['cale'])==r['sha256'],r['cale']
deliverables=[]
for provider,domain in [('BERGER','bmberger.at'),('PECH','zt-pech.at')]:
    source=OUT/f'{DATE} Werkvertrag {provider} R06 Entwurf.json'
    pdf=ROOT/f'00.Proiect/09. Vertraege/{domain}/{DATE} Verhandlungsentwurf R06/{DATE} Werkvertrag {provider} R06.pdf'
    doc=read(source); assert doc['provider']==provider
    qa=read(OUT/f'{DATE} QA text {provider} R06.json')
    assert qa['text_status']=='PASS' and qa['source_sha256']==sha(source) and qa['pdf_sha256']==sha(pdf)
    assert (OUT/f'{DATE} QA vizual {provider} R06.txt').exists()
    editable=pdf.with_suffix('.json')
    if editable.exists(): assert sha(editable)==sha(source)
    else: shutil.copy2(source,editable); assert sha(editable)==sha(source)
    deliverables.append({'prestator':provider,'pdf':{**rec(pdf),'pagini':len(PdfReader(pdf).pages)},'sursa_editabila':rec(editable),'sursa_canonica':rec(source),'qa_text':rec(OUT/f'{DATE} QA text {provider} R06.json'),'qa_vizual':rec(OUT/f'{DATE} QA vizual {provider} R06.txt')})

audits=list(OUT.glob(f'{DATE} Audit*R06*.txt'))
assert len(audits)>=2,'Doua audituri independente sunt necesare'
for stem in ['Propunere economica comuna R06','Audit economic independent R06']:
    for suffix in ['.json','.txt']:
        p=WORK/f'{DATE} {stem}{suffix}'
        if p.exists():
            q=OUT/p.name
            if q.exists(): assert sha(p)==sha(q)
            else: shutil.copy2(p,q)

partners=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
regpath=ROOT/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/{DATE} Registru comunicatii.json'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',partners/f'{DATE} Log discutii - Markus Berger.txt',partners/f'{DATE} Log discutii - Pech.txt',regpath,ROOT/'folder map/README.md']
history=OUT/f'{DATE} Istoric jurnale inainte PDF R06'
assert not history.exists(); history.mkdir()
backups=[]
for p in targets:
    dest=history/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}')
    shutil.copy2(p,dest); assert sha(p)==sha(dest)
    backups.append({'original':rel(p),'sha256_inainte':sha(p),'copie':rel(dest)})

pdf_paths='\n'.join(d['pdf']['cale'] for d in deliverables)
entry=f'''2026.10.13 | Contracte BERGER și PECH — PDF elegant R06, bază comună de negociere
Status scurt: două propuneri noi în germană, fără introducere în română, cu chenare fine, clauze numerotate, antet/subsol și tabele pentru servicii, termene și plăți. Documentele sunt VERHANDLUNGSENTWURF, NETRIMISE și NESEMNATE; nu acceptare comercială. R05 și ofertele originale rămân neschimbate.
Cerințe comune: structură și documentație completă, PI până la final și contribuții § 128, Bauwerksbuch pentru existent și intervenții noi, verificarea calificărilor pe funcții; fără BauKG și management general REALIG. Două repere distincte T0/B0. 12 vizite fizice B0 incluse, până la 6 suplimentare numai comandate; inspecția profesională inițială T0 este inclusă separat. Cadru de execuție 18 luni B0, fără adaos lunar automat. D1–D5: 3/6/8/10/12 săptămâni T0, noduri cu elementul, verificarea atelierelor și ulterior inclusă înainte de fabricație. Asigurarea rămâne completare administrativă, fără nouă cerință numerică AG.
Sume BERGER: 45.000 EUR net, 54.000 EUR brut la 20% TVA. Șase opțiuni la raportul exact 2.000/12: 1.000 EUR net; total condiționat 46.000 EUR net/55.200 EUR brut. Tariful este propunere AG, originalul avea maximum 8 vizite.
Sume PECH: 69.300 EUR net, 83.160 EUR brut la 20% TVA. Șase opțiuni la tariful original 450 EUR net: 2.700 EUR net; total condiționat 72.000 EUR net/86.400 EUR brut. Alte schimbări și deconturi legal justificate rămân distincte.
Facturare: aceleași șapte repere E1–E7 și procente 10/20/25/15/10/10/10, propunere AG. Pozițiile originale sunt reconciliate integral fără majorarea totalului. Partea PI cere raport profesional efectiv; planurile proprii nu generează avans PI. Teren PECH 800 EUR facturat o singură dată după Befund complet; E6 după prestație reală; Bauwerksbuch existent anticipat numai din partea exact convenită E7, fără preț nou inventat. Modelul încărcat spre proiectare și condițiile noi necesită acceptarea ofertantului.
Audit și verificare: două controale independente de agenți pe conținut/economie/legalitate, control root, fidelitate text și fiecare pagină nouă inspectată vizual. Verificările nu constituie un aviz emis de un avocat autorizat și nu garantează acceptarea ori rezultatul unui litigiu. Registrele conțin observațiile și limitele concrete; nu se atribuie o notă juridică forțată.
Ultimul răspuns real: BERGER 2026.08.17; PECH 2026.09.17. Acesta este lucru local de redactare/negociere, nu scan general zilnic EVA sau răspuns comercial nou.
Următorul pas: lectura celor două PDF-uri și definirea poziției finale de negociere, cu completarea actuală a persoanelor, dovezilor și datelor înainte de orice semnare. Nicio trimitere, semnare sau plată.
Surse PDF curente:
{pdf_paths}
Registru: {rel(OUT/f'{DATE} Registru contracte elegante R06.json')}
Matricea de 100 criterii și cele 16 puncte de negociere rămân în dosarul bazei comune. Istoricul și copiile originale sunt păstrate.
'''
def prepend(p,s):
    old=p.read_text(encoding='utf-8-sig');p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
for p in targets[:4]: prepend(p,entry)
reg=read(regpath); count=len(reg['comunicatii'])
reg.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'PDF_contracte_R06_cerinte_comune_negociere','registru':rel(OUT/f'{DATE} Registru contracte elegante R06.json'),'livrabile':[d['pdf']['cale'] for d in deliverables],'statut':'VERHANDLUNGSENTWURF, NETRIMIS/NESEMNAT; R05 nemodificat','mesaje_noi':0,'trimiteri':0,'semnaturi':0,'plati':0})
assert len(reg['comunicatii'])==count
regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[5],f'''# 2026.10.13 — Contracte germane R06 în PDF elegant

Punctul curent pentru lectură sunt cele două propuneri VERHANDLUNGSENTWURF:

- ../{deliverables[0]['pdf']['cale']}
- ../{deliverables[1]['pdf']['cale']}

Registru: ../{rel(OUT/f'{DATE} Registru contracte elegante R06.json')}. Cerințe tehnice și juridice comune; prețurile și tarifele rămân distincte. 18 luni de execuție de la B0 real, 12 vizite fizice plus până la 6 opționale, T0 inițial separat și inclus; PI/§ 128 și Bauwerksbuch întregul existent/nou. Fără BauKG sau management general REALIG. Asigurare administrativă, fără prag numeric AG nou.

PDF-urile sunt în germană, cu clauze delimitate prin chenare fine și tabele de livrabile/termene/plăți. Copiile sursă editabile JSON și ofertele originale Anlage 5 sunt în aceleași foldere ale prestatorilor. Două audituri independente, control numeric, text și toate paginile vizuale sunt în dosarul R06. Cerințele extinse și noua grilă de plată sunt poziții AG pentru negociere, nu acorduri deja primite. Modelul de facturare cere prestații PI reale, nu avans pentru planurile proprii.

R05 și ofertele originale sunt păstrate neschimbate. NETRIMIS/NESEMNAT. Nu există mesaje comerciale noi sau scan general zilnic EVA în această operațiune; jurnalele păstrează ultimul răspuns real și istoricul. Matricea de 100 criterii și obiecțiile reformulate rămân bază comparativă.
''')
registry={'data':DATE,'statut':'VERHANDLUNGSENTWURF — NETRIMIS/NESEMNAT','livrabile':deliverables,'audituri':[rec(p) for p in audits],'baza_comuna':rec(BASE/f'{DATE} Registru baza negociere final.json'),'oferte_originale':[rec(ROOT/f'00.Proiect/09. Vertraege/{domain}/{DATE} Verhandlungsentwurf R06/{DATE} Anlage 5 Originalangebot {provider} {offdate}.pdf') for provider,domain,offdate in [('BERGER','bmberger.at','2026.08.17'),('PECH','zt-pech.at','2026.09.17')]],'contracte_R05_frozen':previous['contracte'],'istoric_jurnale':backups,'jurnale_actualizate':[rec(p) for p in targets],'mesaje_noi':0,'contracte_R05_modificate':0,'trimiteri':0,'semnaturi':0,'plati':0}
fresh(OUT/f'{DATE} Registru contracte elegante R06.json',json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
fresh(OUT/f'{DATE} Jurnal PDF contracte elegante R06.txt',entry)
for r in previous['contracte']:assert sha(ROOT/r['cale'])==r['sha256']
print(json.dumps({'statut':'PASS','PDF':[d['pdf'] for d in deliverables],'R05_intacte':len(previous['contracte']),'comunicatii_neschimbate':count},ensure_ascii=False))
