from pathlib import Path
import json, hashlib, shutil
from pypdf import PdfReader

ROOT = Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK = ROOT / '00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
DATE = '2026.10.13'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.relative_to(ROOT).as_posix()

def record(p, **extra):
    return {'cale': rel(p), 'sha256': sha(p), 'octeti': p.stat().st_size, **extra}

def write_new(p, text):
    assert not p.exists(), f'Fișierul există: {p}'
    p.write_text(text, encoding='utf-8')

freeze = json.loads((WORK / f'{DATE} Surse inghetate audit R05.json').read_text(encoding='utf-8-sig'))
contracts = []
for r in freeze['surse']:
    p = ROOT / r['cale']
    assert sha(p) == r['sha256'], f'Sursă contractuală modificată: {p}'
    contracts.append(record(p, prestator=r['prestator'], tip=r['tip']))
pdf_hashes = {'BERGER': '5b29581b6af90ec2413e491c0c4b28792bedd06e7cf2300a8eaf3898a8551d5b',
              'PECH': '60cac119f679cf699c1951d42a833339608d5929c730288f2965d11cf0d9dc3d'}
for r in freeze['surse']:
    if r['tip'] != 'docx':
        continue
    p = (ROOT / r['cale']).with_suffix('.pdf')
    assert sha(p) == pdf_hashes[r['prestator']]
    contracts.append(record(p, prestator=r['prestator'], tip='pdf', pagini=len(PdfReader(str(p)).pages)))

commercial_path = WORK / f'{DATE} Audit comercial comparativ R05 final.json'
commercial = json.loads(commercial_path.read_text(encoding='utf-8-sig'))
assert sha(commercial_path) == '0ab9f9510bd6e8a920a3bdecee3d18fe27221abde30f250d16b8c4835e927b8b'
legal_path = WORK / f'{DATE} Checklist juridic comparativ R05.json'
legal = json.loads(legal_path.read_text(encoding='utf-8-sig'))
assert len(commercial['checklist']) == 60 and len(commercial['mapare_inversa']) == 44
assert len(legal['checklist']) == 97 and len(legal['oferte_spre_contract']) == 80

reports = []
for title, stem, expected in [
    ('Audit comercial comparativ', f'{DATE} Audit comercial comparativ R05', 33),
    ('Audit juridic în ambele sensuri', f'{DATE} Audit juridic bidirectional R05 final', 46),
    ('Obiecții posibile separate', f'{DATE} Obiectii posibile BERGER PECH R05', 7),
]:
    for ext in ['.docx', '.pdf']:
        p = WORK / (stem + ext)
        n = len(PdfReader(str(p)).pages) if ext == '.pdf' else None
        assert n is None or n == expected
        reports.append(record(p, titlu=title, tip=ext[1:], pagini=n))

qa = WORK / f'{DATE} QA rapoarte comercial si obiectii root.txt'
write_new(qa, '''2026.10.13 | Verificare vizuală a rapoartelor, rol root
Audit comercial: paginile 21–33 inspectate individual la rezoluția originală, în completarea paginilor 1–20 atribuite auditorului comercial. Obiecții posibile: toate paginile 1–7 inspectate individual la rezoluția originală.
Rezultat: PASS aspect pentru paginile inspectate, fără text tăiat, suprapuneri, celule lipsă sau pagini goale. Aceasta este verificare de prezentare, nu aprobare contractuală ori confirmare a asigurării.
Imagini: C:/Users/User/.codex/visualizations/2026/10/01/01a0f6eb-c105-7760-973e-241d6f6be8c1/2026.10.13 QA rapoarte/Comercial și Obiectii. Numerotarea și footer-ele concordă cu PDF-urile de 33 și 7 pagini.
Raportul juridic de 46 pagini are note QA separate pentru 1–23 +44–46 și 24–43. Cele 6 aplicații OGH și cele 80+97 rânduri au fost controlate semantic de auditorul juridic.
Contractele R05 au rămas identice cu sursele înghețate; nu s-a introdus nicio recomandare în contracte. Nu se acordă o notă de 10/10 și nu se declară documentele pregătite pentru semnare.
''')

history = WORK / f'{DATE} Istoric jurnale inainte audit R05'
assert not history.exists()
history.mkdir()
partners = ROOT / '08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
registry_path = ROOT / f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/{DATE} Registru comunicatii.json'
targets = [ROOT / f'{DATE} Status proiect.txt', ROOT / f'{DATE} Log progres proiect.txt',
           partners / f'{DATE} Log discutii - Markus Berger.txt', partners / f'{DATE} Log discutii - Pech.txt',
           registry_path, ROOT / 'folder map/README.md']
backups = []
for p in targets:
    dest = history / (p.name if p.name.startswith(DATE) else f'{DATE} {p.name}')
    shutil.copy2(p, dest)
    assert sha(p) == sha(dest)
    backups.append({'original': rel(p), 'sha256_inainte': sha(p), 'copie_istorica': rel(dest)})

# Conservează exact versiunile jurnalelor citate în audit, înainte de completarea lor.
for src in commercial['documente_verificate']:
    source_path = src.get('cale', '')
    if source_path in [rel(targets[2]), rel(targets[3])]:
        expected = src.get('hash') or src.get('sha256')
        assert expected == sha(ROOT / source_path), f'Jurnalul citat s-a schimbat: {source_path}'

registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
communication_count = len(registry['comunicatii'])
entry = {
    'data': DATE, 'tip': 'audit_bidirectional_R05_DOAR_sesizari',
    'instructiune': 'Nu modifica contractul — DOAR sesizează',
    'auditori': ['auditor comercial independent AI', 'auditor juridic independent AI'],
    'surse_contractuale_inghetate': rel(WORK / f'{DATE} Surse inghetate audit R05.json'),
    'registru_audit': rel(WORK / f'{DATE} Registru audit comparativ final R05.json'),
    'rapoarte': [r['cale'] for r in reports],
    'contracte_modificate_dupa_inghetare': 0,
    'mesaje_noi': 0, 'originale_noi': 0, 'trimiteri': 0, 'semnaturi': 0, 'plati': 0,
    'statut': 'Contracte R05 NETRIMISE/NESEMNATE; acceptare și probe neconfirmate; observații exclusiv în rapoarte',
    'scor': None, 'motiv_scor': 'Nu se atribuie automat 10/10 și nu se transferă nota istorică R02.'
}
assert not any(x.get('tip') == entry['tip'] for x in registry.get('actualizari_punctuale', []))
registry.setdefault('actualizari_punctuale', []).append(entry)
assert len(registry['comunicatii']) == communication_count
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

common = '''2026.10.13 | Audit comparativ R05 în ambele sensuri — DOAR sesizări
Status scurt: doi auditori AI separați au comparat ofertele/documentația cu contractele și fiecare clauză/anexă cu sursa și cadrul juridic. Rapoarte finale: comercial 33 pagini, juridic 46 pagini, obiecții separate 7 pagini; toate paginile verificate vizual. Contractele R05 au rămas nemodificate după înghețarea pentru audit. Nu se acordă o notă forțată de 10/10; nota istorică R02 nu se transferă la R05.
Sume verificate: BERGER 45.000 EUR net /54.000 EUR cu TVA; PECH 69.300 EUR net /83.160 EUR cu TVA. Cu toate cele 6 opțiuni comandate și executate: BERGER 46.000 EUR net /55.200 EUR cu TVA; PECH 72.000 EUR net /86.400 EUR cu TVA. Acestea nu sunt plafonul oricăror costuri legal justificate. BERGER 2.000/12 per vizită suplimentară este propunere AG nouă; PECH 450 EUR net per vizită suplimentară este tarif ofertat.
Scop și durată: 18 luni de la B0 real, 12 vizite incluse și maximum 6 opționale, PI/BWB extinse sunt cerințe propuse, neacceptate. Oferta BERGER avea maximum 8 vizite și circa 12 luni; PECH avea 12 vizite fără durată fixă în luni. Proiectele rămân NETRIMISE/NESEMNATE; fără BauKG și management general REALIG.
Sesizări deschise: PECH Pos.04/05 — livrabile și numărarea vizitei comune; Materialprüfung față de încercări externe; versiunea cererii tehnice și limitele reziduale; autorizări, funcții și asigurarea actuală; valabilitatea BERGER expirată calculat la 2026.10.12, fără prelungire documentată. Nu este dovedită dublă facturare, lipsa absolută a asigurării ori nulitatea automată a pachetului. Nicio recomandare nu a fost implementată în contract.
Ultimul răspuns real: BERGER 2026.08.17; PECH 2026.09.17. Auditul este operațiune locală, nu răspuns nou al ofertanților. Nu este o nouă verificare generală zilnică EVA; reverificările punctuale ale mesajelor istorice sunt documentate separat.
Următorul pas: lectura checklisturilor și decizia utilizatorului asupra punctelor de clarificat. Orice modificare ulterioară a contractelor sau comunicare necesită instrucțiune nouă; această operațiune sesizează exclusiv.
Surse: 00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit/2026.10.13 Registru audit comparativ final R05.json; 2026.10.13 Audit comercial comparativ R05.docx/PDF; 2026.10.13 Audit juridic bidirectional R05 final.docx/PDF; 2026.10.13 Obiectii posibile BERGER PECH R05.docx/PDF. Sursele complete și citatele/clauzele germane se păstrează în JSON/TXT în același dosar.
Istoricul și sursele sunt păstrate. Nu s-au trimis emailuri, semnat sau efectuat plăți. Numărătorile centrale Eva 802 mesaje /826 originale /783 documentare rămân cele din registrul existent; auditul nu adaugă mesaje.
'''

def prepend(p, head):
    before = next(x for x in backups if x['original'] == rel(p))
    assert sha(p) == before['sha256_inainte'], f'Modificare concurentă: {p}'
    old = p.read_text(encoding='utf-8-sig')
    p.write_text(head.rstrip() + '\n\nISTORIC PĂSTRAT\n\n' + old, encoding='utf-8')

prepend(targets[0], common)
prepend(targets[1], common)
for p, who, last, specific in [
    (targets[2], 'BERGER', '2026.08.17', '45.000 EUR net, cu 6 opțiuni maximum 46.000 EUR net; formula 2.000/12 este propusă de AG, nu tarif primit. Oferta inițială: maximum 8 vizite și circa 12 luni; expirare calculată 2026.10.12. Declarația de asigurare 1 milion și polița istorică nu certifică acoperirea actuală pentru toate funcțiile.'),
    (targets[3], 'PECH', '2026.09.17', '69.300 EUR net, cu 6 opțiuni maximum 72.000 EUR net; 450 EUR net/vizită suplimentară este tarif ofertat. Oferta inițială: 12 vizite, fără durată în luni. Clarificări: Pos.04/05, vizita comună, Materialprüfung/laborator, documentația AG referită și probele profesionale/asigurarea actuală.'),
]:
    prepend(p, f'''2026.10.13 | {who} — audit R05, DOAR sesizări
Status scurt: audit comercial și juridic independent în ambele sensuri, cu checklisturi și obiecții separate; contractul R05 rămâne nemodificat, NETRIMIS/NESEMNAT. {specific}
Durata de 18 luni de la B0 real, 12 vizite incluse și maximum 6 opționale, funcțiile PI/BWB și derogările necesită acceptare. Nicio nouă ofertă sau confirmare de acceptare dedusă din audit.
Ultimul răspuns real: {last}; nu este primit un răspuns nou prin această operațiune locală.
Următorul pas: lectura rapoartelor și decizia utilizatorului asupra clarificărilor; nu se modifică și nu se trimite automat contractul.
Surse: {entry['registru_audit']}; rapoartele comercial, juridic și obiecții R05 în același dosar; sursele și istoricul exact al jurnalului auditat sunt păstrate în dosarul 2026.10.13 Istoric jurnale inainte audit R05.
Nota istorică R02 nu se transferă la R05. Nu s-a trimis email, semnat ori plătit.
''')

readme_head = '''# 2026.10.13 — Audit comparativ R05: DOAR sesizări, contracte nemodificate

Punctul curent de audit: ../00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit/. Începe cu `2026.10.13 Audit comercial comparativ R05.docx` sau PDF (33 pagini), `2026.10.13 Audit juridic bidirectional R05 final.docx` sau PDF (46 pagini) și `2026.10.13 Obiectii posibile BERGER PECH R05.docx` sau PDF (7 pagini). Registru de integritate și acoperire: `2026.10.13 Registru audit comparativ final R05.json`. Versiunea juridică publică fără cuvântul «final» în nume este intermediară și rămâne istoric.

Contractele auditate R05, nemodificate după cererea «DOAR sesizează»: ../00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Juristischer Werkvertrag/2026.10.13 Werkvertrag BERGER R05.docx și PDF; ../00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Juristischer Werkvertrag/2026.10.13 Werkvertrag PECH R05.docx și PDF. SHA-256 conservate. NETRIMISE/NESEMNATE. Acesta este reperul curent; nota istorică R02 10/10 nu se transferă și nu se acordă o nouă notă forțată.

Sume de bază BERGER/PECH: 45.000/69.300 EUR net. Cu maximum 6 vizite opționale reale: 46.000/72.000 EUR net, fără a plafona alte costuri legal justificate. BERGER 2.000/12 per supliment este propunere AG; PECH 450 EUR net este oferit. 18 luni de la B0 real, 12 vizite incluse, scop PI/BWB extins și clauzele noi necesită acceptare. Oferta BERGER originală avea maximum 8 vizite și circa 12 luni; expirare calculată 2026.10.12, fără prelungire documentată.

Observații rămase: PECH Pos.04/05 și numărare, Materialprüfung/laborator, referința tehnică și limitele reziduale, autorizări/asigurări actuale, reconfirmarea BERGER. Rapoartele propun exclusiv clarificări; contractele nu au fost corectate. Două oferte complete distincte, documentație conexă și 14 mesaje istorice arhivate citite; nu este pretins un nou scan general live EVA. Jurnalele proiectului și ale celor doi parteneri sunt actualizate cu istoricul păstrat. Numărătorile Eva nu sunt modificate; nicio trimitere, semnare sau plată.
'''
prepend(targets[5], readme_head)

manifest = {
    'data': DATE, 'statut': 'FINAL rapoarte; DOAR sesizări; contracte R05 nemodificate',
    'contracte': contracts, 'rapoarte': reports,
    'surse_auditori': [record(commercial_path), record(legal_path)],
    'acoperire': {'oferte_complete_distincte': 2, 'documente_comerciale_verificate': 28,
                 'mesaje_istorice_citite': 14, 'teme_comerciale': 60, 'grupuri_mapare_inversa': 44,
                 'unitati_comerciale_inverse': sum(len(x['componente']) for x in commercial['mapare_inversa']),
                 'repere_TOMS': 47, 'randuri_juridice_oferta_cerere_spre_contract': 80,
                 'randuri_juridice_contract_spre_sursa_lege': 97, 'obiectii_comerciale': 18,
                 'obiectii_juridice': 12, 'surse_normative_si_profesionale': len(legal['surse']['norme']),
                 'hotarari_OGH_aplicate': len(legal['surse']['jurisprudenta'])},
    'qa': [record(p) for p in sorted(WORK.glob(f'{DATE} QA raport*.txt'))],
    'istoric_jurnale': backups, 'jurnale_actualizate': [record(p) for p in targets],
    'recomandari_implementate_in_contracte_dupa_inghetare': 0,
    'mesaje_noi_adaugate': 0, 'emailuri_trimise': 0, 'semnaturi': 0, 'plati': 0,
    'nota': None, 'interpretare': 'Verificare AI documentară în două roluri independente; nu opinie semnată de avocat și nu confirmare a acceptării, registrelor profesionale, asigurătorilor ori capacității de livrare.',
    'limite': commercial['limite'] + legal['limite'],
}
write_new(WORK / f'{DATE} Registru audit comparativ final R05.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
write_new(WORK / f'{DATE} Jurnal inchidere audit comparativ R05.txt', common + '\nRegistrul de integritate include hash-uri înainte/după și copii istorice ale jurnalelor citate. Indexul incremental se actualizează separat după închiderea fișierelor.\n')
for r in contracts:
    assert sha(ROOT / r['cale']) == r['sha256']
print(json.dumps({'statut': 'PASS', 'contracte_fisiere_identice': len(contracts), 'rapoarte': reports,
                  'acoperire': manifest['acoperire'], 'jurnale_pastrate': len(backups),
                  'comunicatii_registru_neschimbate': communication_count}, ensure_ascii=False))
