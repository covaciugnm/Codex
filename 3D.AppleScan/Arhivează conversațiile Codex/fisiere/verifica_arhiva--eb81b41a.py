import hashlib
import json
import pathlib
import sys
import zipfile

root = pathlib.Path(sys.argv[1]).resolve()
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
count = 0
for line in (root / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    expected, relative = line.split('  ', 1)
    p = (root / relative).resolve()
    if not p.is_relative_to(root):
        raise ValueError('Cale in afara arhivei: ' + relative)
    with p.open('rb') as f:
        actual = hashlib.file_digest(f, 'sha256').hexdigest()
    if expected != actual:
        raise ValueError('SHA-256 incorect: ' + relative)
    count += 1
for p in root.rglob('arhiva-*.zip'):
    with zipfile.ZipFile(p) as archive:
        error = archive.testzip()
        if error:
            raise ValueError('ZIP deteriorat: ' + str(p) + ': ' + error)
ids = set()
for thread in manifest['threads']:
    if thread['id'] in ids:
        raise ValueError('ID conversatie duplicat: ' + thread['id'])
    ids.add(thread['id'])
    folder = root / thread['folder']
    data = json.loads((folder / 'istoric.json').read_text(encoding='utf-8'))
    messages = sum(x['item'].get('type') in ('userMessage', 'agentMessage') for x in data['items'])
    if messages != thread['message_count']:
        raise ValueError('Numar mesaje inconsistent: ' + thread['id'])
    for item in data['items']:
        if item['item'].get('type', '').lower() in ('reasoning', 'contextcompaction'):
            raise ValueError('Eveniment intern in export: ' + thread['id'])
    for filename in ('conversatie.md', 'rezultate.md', 'fisiere-index.json', 'metadate.json'):
        if not (folder / filename).is_file():
            raise ValueError('Fisier lipsa: ' + str(folder / filename))
print(json.dumps({'verified_files': count, 'verified_threads': len(ids), 'totals': manifest['totals']}, ensure_ascii=True))
