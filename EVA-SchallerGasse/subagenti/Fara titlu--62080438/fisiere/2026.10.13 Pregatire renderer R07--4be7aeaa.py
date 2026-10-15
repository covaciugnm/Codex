from pathlib import Path
import hashlib

vis = Path(__file__).resolve().parent
source = vis / '2026.10.13 Renderer contracte elegante.py'
target = vis / '2026.10.13 Renderer contracte elegante R07.py'
assert not target.exists(), 'Use a new path; do not replace an existing edition.'
original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
text = source.read_text(encoding='utf-8')
replacements = {
    'VERHANDLUNGSENTWURF': 'VERTRAGSVORSCHLAG',
    "author='A&C Wohnart', subject='Verhandlungsentwurf'": "author='A&C Wohnart Immobilien GmbH', subject='Vertragsvorschlag'",
    'Die Angaben dieser Übersicht ersetzen keine Bestimmung des Entwurfs.': 'Die Angaben dieser Übersicht ersetzen keine Bestimmung dieses Vertragsvorschlags.',
    "{'renderer':'2026.10.13','contracts':results}": "{'renderer':'2026.10.13 R07','contracts':results}",
}
for before, after in replacements.items():
    assert before in text, before
    text = text.replace(before, after)
compile(text, str(target), 'exec')
target.write_text(text, encoding='utf-8')
assert hashlib.sha256(source.read_bytes()).hexdigest() == original_hash
print('R07 renderer SHA-256:', hashlib.sha256(target.read_bytes()).hexdigest())
print('R06 renderer unchanged SHA-256:', original_hash)
