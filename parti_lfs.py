"""Lossless LFS chunks for files above the portable single-object limit."""
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

LIMIT = 1_900_000_000
PART_SIZE = 512 * 1024 * 1024
BLOCK = 4 * 1024 * 1024

def verify_or_restore(index, output=None):
    index = Path(index)
    data = json.loads(index.read_text(encoding='utf-8'))
    combined = hashlib.sha256()
    total = 0
    for part in data['parts']:
        name = part['file']
        if Path(name).name != name or not name.endswith('.codex-lfs-part'):
            raise ValueError('Invalid part path')
        piece = hashlib.sha256()
        count = 0
        with (index.parent / name).open('rb') as src:
            while block := src.read(BLOCK):
                piece.update(block)
                combined.update(block)
                count += len(block)
                if output is not None:
                    output.write(block)
        if (piece.hexdigest(), count) != (part['sha256'], part['bytes']):
            raise ValueError('Invalid part: ' + name)
        total += count
    if (combined.hexdigest(), total) != (data['sha256'], data['bytes']):
        raise ValueError('Reconstruction hash mismatch')
    return data

def split_public(path, source, limit=LIMIT, part_size=PART_SIZE):
    path = Path(path)
    if path.stat().st_size <= limit:
        return []
    if not source.is_file() or path.samefile(source):
        raise ValueError('Split only a publication copy')
    with path.open('rb') as f:
        full = hashlib.file_digest(f, 'sha256').hexdigest()
    book = {'filename': path.name, 'bytes': path.stat().st_size, 'sha256': full, 'parts': []}
    pieces = []
    with path.open('rb') as src:
        while src.tell() < book['bytes']:
            piece = hashlib.sha256()
            n = 0
            with NamedTemporaryFile(dir=path.parent, delete=False) as dest:
                tmp = Path(dest.name)
                while n < part_size and (block := src.read(min(part_size-n, BLOCK))):
                    piece.update(block)
                    dest.write(block)
                    n += len(block)
            name = full + '-' + str(len(pieces)+1).zfill(4) + '.codex-lfs-part'
            target = path.parent / name
            os.replace(tmp, target)
            pieces.append(target)
            book['parts'].append({'file': name, 'bytes': n, 'sha256': piece.hexdigest()})
    index = path.with_name(path.name + '.codex-parts.json')
    index.write_text(json.dumps(book, indent=2), encoding='utf-8')
    verify_or_restore(index)
    path.unlink()  # Only the temporary full publication copy; verified source stays intact.
    return pieces

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Restore one large file from its downloaded Git LFS parts.')
    ap.add_argument('index', type=Path)
    ap.add_argument('destination', type=Path)
    args = ap.parse_args()
    with args.destination.open('xb') as out:
        try:
            verify_or_restore(args.index, out)
        except BaseException:
            out.close()
            args.destination.unlink()
            raise

