"""Mask authentication secrets in the publication copy, retaining local originals."""
import collections
import hashlib
import json
import pathlib
import re
import zipfile

TEXT_EXTENSIONS = {'.md', '.json', '.txt', '.py', '.js', '.ts', '.yaml', '.yml', '.toml', '.env', '.csv', '.tsv', '.html', '.sh', '.ps1', '.xml', '.ini', '.cfg', '.sql'}
PATTERNS = {
    'private_key': re.compile(rb'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----.*?-----END (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----', re.S),
    'github_token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,255}|github_pat_[A-Za-z0-9_]{40,255})\b'),
    'openai_key': re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,255}\b'),
    'aws_access_key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'signed_url_credential': re.compile(rb'(?i)(?:AWSAccessKeyId|X-Amz-Credential|X-Amz-Signature|X-Amz-Security-Token|Signature)=[^&\s"\x27<>\\]+'),
}

def mask(data):
    counts = collections.Counter()
    for name, pattern in PATTERNS.items():
        data, count = pattern.subn(b'[CREDENTIAL_REDACTED]', data)
        if count:
            counts[name] += count
    return data, dict(counts)

def protect_project(folder):
    folder = pathlib.Path(folder)
    changed = set()
    report = []
    for path in sorted(folder.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        original = path.read_bytes()
        clean, counts = mask(original)
        if counts:
            path.write_bytes(clean)
            relative = path.relative_to(folder).as_posix()
            changed.add(relative)
            report.append({'path': relative, 'masked_values': counts})
    for archive_path in folder.glob('arhiva-*.zip'):
        with zipfile.ZipFile(archive_path) as source:
            names = source.namelist()
        if not changed.intersection(names):
            continue
        # Generated ZIP volumes mirror files in this folder. Rebuild affected
        # volumes from the sanitized counterparts, never from the source backup.
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as target:
            for name in names:
                path = (folder / name).resolve()
                if not path.is_relative_to(folder.resolve()) or not path.is_file():
                    raise ValueError('Unsafe or missing archive member: ' + name)
                target.write(path, name)
        with zipfile.ZipFile(archive_path) as check:
            if check.testzip() is not None:
                raise ValueError('ZIP verification failed: ' + str(archive_path))
    (folder / 'mascari-publicare.json').write_text(json.dumps({'local_originals_preserved': True, 'masked_files': report}, ensure_ascii=False, indent=2), encoding='utf-8')
    hashes = []
    for path in sorted(folder.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS-PUBLIC.txt':
            with path.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            hashes.append(digest + '  ' + path.relative_to(folder).as_posix())
    (folder / 'SHA256SUMS-PUBLIC.txt').write_text('\n'.join(hashes) + '\n', encoding='utf-8')
    return report
