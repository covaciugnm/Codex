"""Snapshots and verifies audit evidence; never awards an editorial score."""
import argparse, hashlib, json, pathlib, shutil, datetime

ROOT = pathlib.Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS')
CORE = ['01_CANON/00_CANON_NUCLEU.md', '00_STUDIO/01_ECHIPA_SI_ROADMAP.md',
        '00_STUDIO/03_JURNAL_PROGRES.md', '00_STUDIO/rapoarte/S_showrunner.md']
REFS = ['01_CANON/01_DECIZII_PRODUCATOR.md',
        '00_STUDIO/audit/00_CONTRASEMNARI_PRODUCATOR.md',
        '00_STUDIO/audit/00_REGISTRU_AUDIT.md']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def freeze(dest):
    dest.mkdir(parents=True, exist_ok=False)
    paths = CORE + REFS
    paths += [str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT/'00_STUDIO/02_BRIEFURI').glob('*.md')]
    manifest = {'created': datetime.datetime.now().astimezone().isoformat(), 'files': {}}
    for rel in paths:
        src, out = ROOT/rel, dest/rel
        before = sha(src)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        if sha(out) != before or sha(src) != before:
            raise RuntimeError('Concurrent edit: ' + rel)
        manifest['files'][rel] = {'sha256': before, 'bytes': out.stat().st_size,
                                  'kind': 'deliverable' if rel in CORE else 'reference'}
    (dest/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'snapshot':str(dest),'files':len(paths)},ensure_ascii=False))

def verify(dest, live=False):
    m = json.loads((dest/'manifest.json').read_text(encoding='utf-8'))
    errors=[]
    for rel, info in m['files'].items():
        if not (dest/rel).exists() or sha(dest/rel)!=info['sha256']:
            errors.append('Snapshot changed: '+rel)
        if live and info['kind']=='deliverable' and sha(ROOT/rel)!=info['sha256']:
            errors.append('Live deliverable changed: '+rel)
    print(json.dumps({'ok':not errors,'errors':errors},ensure_ascii=False))
    return not errors

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['freeze','verify'])
    ap.add_argument('folder',type=pathlib.Path)
    ap.add_argument('--live',action='store_true')
    a=ap.parse_args()
    if a.action=='freeze': freeze(a.folder)
    elif not verify(a.folder,a.live): raise SystemExit(1)
