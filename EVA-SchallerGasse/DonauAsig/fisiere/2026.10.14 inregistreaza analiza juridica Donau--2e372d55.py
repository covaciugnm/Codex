from pathlib import Path
import json, shutil, hashlib

root = Path(__file__).resolve().parent.parent
case = root / '05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau'
archive = root / '08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
marker = '2026.10.14 — DONAU: două analize juridice și audit'
pdfs = sorted(case.glob('2026.10.14 0*.pdf'))
assert len(pdfs) == 2, 'Lipsesc cele două PDF-uri finale'
audit = case / '2026.10.14 Audit juridic si editorial.txt'
assert audit.exists()
status = ('Analiză documentară a încetării și a primelor în perioada în care DONAU invocă lipsa acoperirii. '
          'Nu este confirmată încetarea poliței. Durata comercială până în 2036 poate fi valabilă, dar acordul, mandatul și cadrul trebuie justificate. '
          'Obiecție nouă: ABS art. 4.5 și §91 VersVG indică termenul de o lună pentru componenta incendiu-clădire; somația identificată acordă două săptămâni. '
          'Aceasta corectează omisiunea studiului din 2026.10.07; nu dovedește automat acoperirea întregului pachet și nu șterge primele.')
next_step = ('Cerere completă de documente și justificare pe ramuri a lipsei acoperirii; dovada acordului pentru 2036, contractul-cadru, toate somațiile și recepțiile, '
             'decont și condiții de restabilire. Menținerea declarației trimise la 2026.10.01; completarea documentelor tehnice pentru reducere și negocierea ieșirii. '
             'Cererea nouă este pregătită local, NETRIMISĂ. Ciorna Eva-Mail din 2026.10.07 rămâne NETRIMISĂ.')
sources = [p.relative_to(root).as_posix() for p in pdfs] + [audit.relative_to(root).as_posix()]
note = (marker + '\n\nStatus scurt: ' + status + '\n\nUltimul răspuns verificat: DONAU, 2026.10.06, '
        'ID 2c273256-a0bf-408b-bb22-09718372e888; refuză încetarea și afirmă lipsa acoperirii pentru prime restante. '
        'Ultima pretenție Commerz: 5.326,15 EUR, termen 2026.10.12; fără reconciliere bancară.\n\nUrmătorul pas: '
        + next_step + '\n\nSurse:\n' + '\n'.join(sources) + '\n\n')

def preserve(path):
    dest = case / 'Istoric' / path.relative_to(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not dest.exists():
        shutil.copy2(path, dest)

def prepend(path):
    old = path.read_text(encoding='utf-8-sig') if path.exists() else ''
    if marker in old:
        return
    preserve(path)
    path.write_text(note + 'ISTORIC PĂSTRAT\n\n' + old, encoding='utf-8-sig')

for name in ['2026.10.14 Status proiect.txt', '2026.10.14 Log progres proiect.txt']:
    prepend(root / name)
for partner in ['Donau Versicherung', 'Maritczak - Commerz Inkasso', 'CERHA HEMPEL']:
    prepend(archive / 'Parteneri' / f'2026.10.14 Log discutii - {partner}.txt')

registry_path = archive / '2026.10.14 Registru comunicatii.json'
preserve(registry_path)
registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
updates = registry.setdefault('actualizari_punctuale', [])
if not any(x.get('subiect') == marker for x in updates):
    updates.append({'data': '2026.10.14', 'subiect': marker, 'status': status,
                    'urmatorul_pas': next_step, 'surse': sources,
                    'nota': 'Cercetare și documente locale; zero emailuri noi trimise, zero plăți, fără modificarea numărătorilor de comunicări.'})
for entry in registry['statusuri']:
    if entry.get('partener') == 'Donau Versicherung':
        entry['analiza_juridica_2026_10_14'] = {'status': status, 'urmatorul_pas': next_step, 'surse': sources}
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')

readme = root / 'folder map/README.md'
old = readme.read_text(encoding='utf-8-sig')
if marker not in old:
    preserve(readme)
    readme.write_text('# ' + marker + '\n\nDosar: `../05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau/`. '
                      'Citește cele două PDF-uri 01/02 și auditul final. Sursele oficiale și originale sunt identificate în bibliografii și în subfolderul Surse. '
                      + status + '\n\n' + next_step + '\n\nISTORIC PĂSTRAT\n\n' + old, encoding='utf-8')

(case / '2026.10.14 Jurnal actualizare.txt').write_text(note, encoding='utf-8-sig')
manifest = [{'fisier': p.relative_to(root).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
             'bytes': p.stat().st_size, 'data_lizibila': '2026.10.14'} for p in pdfs + [audit]]
(case / '2026.10.14 Manifest livrabile finale.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': 'jurnale actualizate', 'livrabile': manifest}, ensure_ascii=False))
