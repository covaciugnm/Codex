"""Mask authentication secrets in the publication copy, retaining local originals."""
import collections
import copy
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


# Additional credential formats seen in exported text; reports contain counts only.
TEXT_EXTENSIONS.update({'.jsonl','.log','.jsx','.tsx','.mjs','.cjs','.conf','.properties','.htm','.pem','.key','.env','.url'})
PATTERNS.update({
    'google_api_key': re.compile(rb'AIza[A-Za-z0-9_-]{35}'),
    'signed_query_sig': re.compile(rb'(?i:[?&]sig=)[A-Za-z0-9/%+=_-]{20,}'),
    'url_userinfo': re.compile(rb'://[^/\s:@"\x27\\<>]{1,100}:[^/\s@"\x27\\<>]{1,200}@'),
    'jwt': re.compile(rb'\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{12,}'),
    'bearer_token': re.compile(rb'(?i:\bBearer) +[A-Za-z0-9_./+=-]{24,}'),
    'slack_token': re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{15,}'),
    'gitlab_token': re.compile(rb'\bglpat-[A-Za-z0-9_-]{20,}'),
    'stripe_secret': re.compile(rb'\b(?:sk|rk)_live_[A-Za-z0-9]{16,}'),
    'telegram_token': re.compile(rb'\b[0-9]{7,12}:[A-Za-z0-9_-]{34,}'),
})

TEXT_EXTENSIONS.update({'.java','.properties','.conf','.config','.js','.jsx','.tsx','.xml','.cs','.kt','.kts','.rb','.php','.psm1','.gradle'})
LITERAL_CREDENTIAL = re.compile(rb"""(?i)(\b(?:password|passwd|api[_-]?key|client[_-]?secret|access[_-]?token)\b(?:\\*["'])?\s*[:=]\s*\\*["'])([A-Za-z0-9_./+=!@%:$-]{8,255})(\\*["'])""")

def mask(data):
    counts = collections.Counter()
    if any(k in data.lower() for k in (b'pass',b'api',b'client',b'access')):
        data,n=LITERAL_CREDENTIAL.subn(lambda m:m[1]+b'[CREDENTIAL_REDACTED]'+m[3],data)
        if n:
            counts['literal_authentication_value']=n
    for name, pattern in PATTERNS.items():
        data, count = pattern.subn(b'[CREDENTIAL_REDACTED]', data)
        if count:
            counts[name] += count
    return data, dict(counts)

CONTAINERS = {'.zip','.docx','.docm','.xlsx','.xlsm','.pptx','.pptm','.odt','.ods','.odp','.jar','.apk','.whl'}

def safe_text(data, suffix):
    clean, counts = mask(data)
    if counts and suffix in {'.json','.ipynb'}:
        # Never let a regex spanning two JSON fields damage the structured history.
        try:
            json.loads(clean)
        except ValueError:
            def walk(value):
                if isinstance(value,str):
                    return mask(value.encode('utf-8'))[0].decode('utf-8')
                if isinstance(value,list):
                    return [walk(x) for x in value]
                if isinstance(value,dict):
                    return {walk(k):walk(v) for k,v in value.items()}
                return value
            try:
                obj=json.loads(data)
            except ValueError:
                return clean, counts
            clean=json.dumps(walk(obj),ensure_ascii=False,indent=2).encode('utf-8')
    return clean,counts

def protect_container(path, level=0):
    import os, shutil, tempfile
    if level>8:
        raise ValueError('Too many nested ZIP containers')
    counts=collections.Counter()
    with tempfile.TemporaryDirectory(dir=path.parent) as td:
        base=pathlib.Path(td)
        replacements={}
        with zipfile.ZipFile(path) as src:
            infos=src.infolist()
            for n,info in enumerate(infos):
                suffix=pathlib.PurePosixPath(info.filename).suffix.lower()
                if info.is_dir() or suffix not in TEXT_EXTENSIONS | CONTAINERS:
                    continue
                stage=base/str(n)
                if suffix in CONTAINERS:
                    with src.open(info) as f, stage.open('wb') as g:
                        shutil.copyfileobj(f,g,1024*1024)
                    if zipfile.is_zipfile(stage):
                        inside=protect_container(stage, level+1)
                    else:
                        # Some vendor assets have a ZIP suffix but are opaque binary data.
                        # Never ignore a damaged ZIP, an encrypted archive, or a detected secret.
                        with stage.open('rb') as rawf:
                            magic=rawf.read(16)
                        if magic.startswith((b'PK',b'7z',b'Rar!',b'\x1f\x8b')) or stage.stat().st_size>64*1024*1024:
                            raise ValueError('Cannot inspect nested archive')
                        payload=stage.read_bytes()
                        if mask(payload)[1]:
                            raise ValueError('Credential detected in opaque nested asset')
                        inside={}
                    if inside:
                        replacements[n]=stage
                        counts.update(inside)
                else:
                    if info.file_size>512*1024*1024:
                        raise ValueError('Text member too large for safe credential inspection')
                    raw=src.read(info)
                    clean,found=safe_text(raw,suffix)
                    if found:
                        stage.write_bytes(clean)
                        replacements[n]=stage
                        counts.update(found)
            if not replacements:
                return {}
            out=base/'rebuilt'
            with zipfile.ZipFile(out,'w',allowZip64=True) as dst:
                dst.comment=src.comment
                for n,info in enumerate(infos):
                    with (replacements[n].open('rb') if n in replacements else src.open(info)) as f, dst.open(copy.copy(info),'w',force_zip64=True) as g:
                        shutil.copyfileobj(f,g,1024*1024)
        with zipfile.ZipFile(out) as check:
            if check.testzip() is not None:
                raise ValueError('Protected ZIP failed verification')
        os.replace(out,path)
    return dict(counts)

def protect_project(folder, source=None):
    folder = pathlib.Path(folder)
    changed = set()
    report = []
    for path in sorted(folder.rglob('*')):
        if not path.is_file():
            continue
        if path.suffix.lower() in CONTAINERS and path.parent.name == 'fisiere':
            counts=protect_container(path)
        elif path.suffix.lower() in TEXT_EXTENSIONS:
            original=path.read_bytes()
            clean,counts=safe_text(original,path.suffix.lower())
            if counts:
                path.write_bytes(clean)
        else:
            continue
        if counts:
            relative = path.relative_to(folder).as_posix()
            changed.add(relative)
            report.append({'path': relative, 'masked_values': counts})
    for archive_path in folder.glob('arhiva-*.zip'):
        with zipfile.ZipFile(archive_path) as packed:
            names = packed.namelist()
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
    if source is not None:
        from parti_lfs import LIMIT, split_public
        source = pathlib.Path(source)
        for original in source.rglob('*'):
            if original.is_file() and original.stat().st_size > LIMIT:
                copy = folder / original.relative_to(source)
                split_public(copy, original)
    hashes = []
    for path in sorted(folder.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS-PUBLIC.txt':
            with path.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            hashes.append(digest + '  ' + path.relative_to(folder).as_posix())
    (folder / 'SHA256SUMS-PUBLIC.txt').write_text('\n'.join(hashes) + '\n', encoding='utf-8')
    return report
