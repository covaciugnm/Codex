import collections
import argparse
import base64
import datetime as dt
import hashlib
import json
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys
import zipfile
from urllib.parse import quote, unquote

parser = argparse.ArgumentParser(description='Export conversații Codex, rezultate și fișiere, fără modificarea istoricului sursă.')
parser.add_argument('--codex-home', type=pathlib.Path, default=pathlib.Path.home() / '.codex')
parser.add_argument('--output', type=pathlib.Path, required=True, help='Director nou, inexistent, pentru această salvare.')
args = parser.parse_args()
BASE = args.codex_home.resolve()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=False)
STAMP = dt.datetime.now(dt.timezone.utc).isoformat()

def read_db(name):
    source = sqlite3.connect((BASE / name).as_uri() + '?mode=ro', uri=True)
    dest = sqlite3.connect(':memory:')
    source.backup(dest)
    source.close()
    dest.row_factory = sqlite3.Row
    return dest

state = read_db('state_5.sqlite')
history = read_db('thread_history_1.sqlite')
settings = json.loads((BASE / '.codex-global-state.json').read_text(encoding='utf-8'))
projects = {k: v for k, v in settings['local-projects'].items() if not k.startswith('g-p-')}
assignments = settings.get('thread-project-assignments', {})
new_to_old = {}
for mapping in settings.get('app-server-project-id-by-legacy-project-id-by-host', {}).values():
    new_to_old.update({v: k for k, v in mapping.items()})
# New projects may exist in the current database before legacy desktop settings
# are backfilled. Rediscover both sources on every run, including empty projects.
for record in state.execute('SELECT id, name FROM projects'):
    pid = new_to_old.get(record['id'], record['id'])
    roots = [r['path'] for r in state.execute('SELECT path FROM project_roots WHERE project_id=? ORDER BY position', (record['id'],))]
    if pid.startswith('g-p-') or any('\\.chatgpt-projects\\' in root for root in roots):
        continue
    projects[pid] = {**projects.get(pid, {}), 'id': pid, 'name': record['name'], 'rootPaths': roots or projects.get(pid, {}).get('rootPaths', [])}
threads = {r['id']: dict(r) for r in state.execute('SELECT * FROM threads')}
parents = {r['child_thread_id']: r['parent_thread_id'] for r in state.execute('SELECT * FROM thread_spawn_edges')}
for tid, row in threads.items():
    try:
        parent = json.loads(row['source']).get('subagent', {}).get('thread_spawn', {}).get('parent_thread_id')
        if parent:
            parents[tid] = parent
    except (ValueError, AttributeError):
        pass

def norm(path):
    path = path.replace('/', '\\')
    if path.lower().startswith('\\\\?\\unc\\'):
        path = '\\\\' + path[8:]
    elif path.startswith('\\\\?\\'):
        path = path[4:]
    aliases = {'z:': r'\\192.168.100.169\Comun', 's:': r'\\192.168.100.151\site-uri'}
    if path[:2].lower() in aliases:
        path = aliases[path[:2].lower()] + path[2:]
    return path.rstrip('\\').casefold()

def resolve_project(tid, visited=None):
    visited = set() if visited is None else visited
    if tid in visited or tid not in threads:
        return None, 'unresolved'
    visited.add(tid)
    row = threads[tid]
    pid = assignments.get(tid, {}).get('projectId')
    if pid in projects:
        return pid, 'app_assignment'
    pid = new_to_old.get(row.get('project_id'), row.get('project_id'))
    if pid in projects:
        return pid, 'database_assignment'
    if tid in parents:
        pid, _ = resolve_project(parents[tid], visited)
        if pid:
            return pid, 'parent_thread'
    if tid in settings.get('projectless-thread-ids', []):
        return None, 'explicitly_projectless'
    cwd = norm(row['cwd'])
    matches = []
    for pid, p in projects.items():
        for root in p['rootPaths']:
            root = norm(root)
            if cwd == root or cwd.startswith(root + '\\'):
                matches.append((len(root), pid))
    if matches:
        return max(matches)[1], 'workspace_path'
    return None, 'unassigned'

def safe(text):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', text).strip(' .')[:80].rstrip(' .') or 'Fara titlu'
    if name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1,10)), *('LPT'+str(i) for i in range(1,10))}:
        name = '_' + name
    return name

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def text_content(item):
    if item.get('type') == 'agentMessage':
        return item.get('text', '')
    chunks = []
    for part in item.get('content', []):
        if isinstance(part, str):
            chunks.append(part)
        elif part.get('text') is not None:
            chunks.append(part['text'])
        else:
            chunks.append('[Atașament / conținut non-text: ' + json.dumps(part, ensure_ascii=False) + ']')
    return '\n\n'.join(chunks)

EXCLUDED_TYPES = {'reasoning', 'contextCompaction'}
def normalize_item(item):
    item = dict(item)
    typ = item.get('type', '')
    item['type'] = typ[:1].lower() + typ[1:]
    if item['type'] == 'extension':
        item['type'] = item.get('kind', 'extension')
    if item['type'] == 'agentMessage' and 'text' not in item:
        item['text'] = '\n'.join(p.get('text', '') for p in item.get('content', []) if isinstance(p, dict))
    return item

def visible(item):
    return item.get('type') not in EXCLUDED_TYPES and item.get('phase') not in {'analysis', 'justify', 'confidence'}

def load_items(row):
    items = collections.OrderedDict()
    legacy = []
    invalid = 0
    path = pathlib.Path(row['rollout_path'])
    file_size = path.stat().st_size if path.exists() else 0
    if file_size:
        with path.open('rb') as stream:
            data = stream.read(file_size)
        for ordinal, line in enumerate(data.splitlines()):
            try:
                record = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                invalid += 1
                continue
            p = record.get('payload', {})
            if record.get('type') == 'event_msg' and p.get('type') == 'item_completed':
                item = normalize_item(p.get('item', {}))
                if visible(item):
                    key = item.get('id') or str(ordinal)
                    items[key] = {'ordinal': ordinal, 'timestamp': record.get('timestamp'), 'turn_id': p.get('turn_id'), 'item': item}
            elif record.get('type') == 'event_msg' and p.get('type') in {'user_message', 'agent_message'}:
                kind = 'userMessage' if p['type'] == 'user_message' else 'agentMessage'
                item = {'type': kind, 'id': 'legacy-' + str(ordinal)}
                if kind == 'userMessage':
                    item['content'] = [{'type': 'text', 'text': p.get('message', '')}]
                    for attachment in p.get('images', []) + p.get('local_images', []):
                        item['content'].append({'type': 'attachmentReference', 'reference': attachment})
                else:
                    item.update(text=p.get('message', ''), phase=p.get('phase'))
                if visible(item):
                    legacy.append({'ordinal': ordinal, 'timestamp': record.get('timestamp'), 'item': item})
    for r in history.execute('SELECT * FROM thread_items WHERE thread_id=? ORDER BY rollout_ordinal', (row['id'],)):
        item = normalize_item(json.loads(r['item_json']))
        if visible(item):
            existing = items.get(r['item_id'], {})
            items[r['item_id']] = {**existing, 'ordinal': r['rollout_ordinal'], 'created_at_ms': r['created_at_ms'], 'turn_id': r['turn_id'], 'item': item}
    result = sorted(items.values(), key=lambda x: x['ordinal']) if items else legacy
    return result, {'source_bytes': file_size, 'invalid_json_lines': invalid, 'history_source': 'items' if items else 'legacy_events', 'rollout_exists': path.exists()}

LINK = re.compile(r'\]\(<?([^\n]+?)>?\)')
QUOTED_PATH = re.compile(r'["`\']((?:[A-Za-z]:[\\/]|\\\\)[^\n"`\']+)["`\']')
reachable = {}
file_totals = collections.Counter()

def root_available(path):
    root = pathlib.PureWindowsPath(str(path)).anchor
    if root not in reachable:
        try:
            result = subprocess.run([sys.executable, '-c', 'import os,sys;sys.exit(0 if os.path.isdir(sys.argv[1]) else 1)', root], timeout=4, capture_output=True)
            reachable[root] = result.returncode == 0
        except subprocess.TimeoutExpired:
            reachable[root] = False
    return reachable[root]

def candidate_path(raw, cwd):
    raw = unquote(raw).strip().strip('<>')
    raw = re.sub(r':\d+(?::\d+)?$', '', raw)
    if raw.startswith('file:///'):
        raw = raw[8:]
    if raw.startswith(('https://', 'http://', 'sandbox:', 'project-file:', 'library-file:', 'visualize:')):
        return None, 'referinta_externa_necopiata'
    if raw.startswith('/') and not raw.startswith('//'):
        return None, 'cale_linux_indisponibila'
    if re.match(r'^[zs]:[\\/]', raw, re.I):
        raw = {'z': r'\\192.168.100.169\Comun', 's': r'\\192.168.100.151\site-uri'}[raw[0].lower()] + raw[2:]
    p = pathlib.Path(raw)
    if not p.is_absolute():
        if not p.suffix or not ('/' in raw or '\\' in raw):
            return None, 'referinta_relativa_neconfirmata'
        p = pathlib.Path(cwd) / p
    lowered = str(p).replace('/', '\\').casefold()
    if p.suffix.lower() in {'.exe', '.dll', '.sys', '.msi'} or '\\appdata\\local\\docker\\run\\' in lowered:
        return None, 'program_sau_endpoint_tehnic_exclus'
    if any(x in lowered for x in ['\\.ssh\\', '\\.aws\\', '\\.git\\', '\\.sandbox-secrets\\', '\\.codex\\auth.json', '\\.codex\\config.toml', '\\.codex\\skills\\', '\\.codex\\plugins\\']):
        return None, 'configuratie_sau_credentiale_excluse'
    if '\\.codex\\' in lowered and not any(x in lowered for x in ['\\generated_images\\', '\\attachments\\', '\\visualizations\\']):
        return None, 'stare_interna_aplicatie_exclusa'
    if str(OUT).casefold() in lowered or 'codex-arhive-2026-10-07' in lowered or '\\codex-arhiva\\' in lowered:
        return None, 'export_curent_exclus_pentru_a_evita_recursia'
    return p, None

def file_candidates(items):
    found = set()
    for event in items:
        item = event['item']
        typ = item.get('type')
        if typ in {'userMessage', 'agentMessage'}:
            text = text_content(item)
            found.update(LINK.findall(text))
            found.update(QUOTED_PATH.findall(text))
            for c in item.get('content', []):
                if isinstance(c, dict) and c.get('path'):
                    found.add(c['path'])
        if typ in {'imageGeneration', 'imageView'}:
            for k in ['savedPath', 'path']:
                if item.get(k):
                    found.add(item[k])
        if typ == 'fileChange':
            changes = item.get('changes', [])
            if isinstance(changes, dict):
                found.update(changes.keys())
            else:
                for change in changes:
                    if isinstance(change, dict) and change.get('path'):
                        found.add(change['path'])
        if typ == 'mcpToolCall':
            # Save explicit result links, not arbitrary filesystem reads or shell command arguments.
            result = json.dumps(item.get('result', {}), ensure_ascii=False)
            found.update(LINK.findall(result.replace('\\n', '\n').replace('\\\\', '\\').replace('\\"', '"')))
    return found

def copy_files(items, row, destination):
    candidates = file_candidates(items)
    for root in [BASE / 'generated_images' / row['id'], BASE / 'attachments' / row['id']]:
        if root.is_dir():
            candidates.update(str(p) for p in root.rglob('*') if p.is_file())
    report = []
    localdir = destination / 'fisiere'
    localdir.mkdir(exist_ok=True)
    for raw in sorted(candidates):
        p, reason = candidate_path(raw, row['cwd'])
        item = {'source_reference': raw}
        try:
            if not reason and not root_available(p):
                reason = 'unitate_sau_server_inaccesibil'
            if not reason and not p.is_file():
                reason = 'fisier_inexistent_sau_director'
            if reason:
                item['status'] = reason
            else:
                filename = safe(p.stem)[:55] + '--' + hashlib.sha256(str(p).encode()).hexdigest()[:8] + p.suffix[:16]
                target = localdir / filename
                shutil.copy2(p, target)
                with target.open('rb') as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                item.update(status='copiat', saved_path='fisiere/' + filename, bytes=target.stat().st_size, sha256=digest)
        except (OSError, ValueError) as exc:
            item.update(status='eroare_copiere', error=str(exc))
        report.append(item)
        file_totals[item['status']] += 1
    write_json(destination / 'fisiere-index.json', report)
    return report

def zip_project(folder):
    # Independent valid ZIP volumes, each below 90 MiB of input where possible.
    files = [p for p in sorted(folder.rglob('*')) if p.is_file() and not p.name.startswith('arhiva-')]
    packs, batch, size = [], [], 0
    for p in files:
        amount = p.stat().st_size
        if batch and size + amount > 90 * 1024 * 1024:
            packs.append(batch); batch = []; size = 0
        batch.append(p); size += amount
    if batch:
        packs.append(batch)
    records = []
    for number, batch in enumerate(packs, 1):
        target = folder / f'arhiva-{number:03d}.zip'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in batch:
                z.write(p, p.relative_to(folder).as_posix())
        with zipfile.ZipFile(target) as z:
            assert z.testzip() is None
        with target.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        records.append({'path': target.relative_to(OUT).as_posix(), 'bytes': target.stat().st_size, 'sha256': digest})
    return records

manifest = {'format_version': 2, 'export_started_at_utc': STAMP, 'repository': 'https://github.com/covaciugnm/Codex', 'upload_status': 'not_uploaded', 'projects': [], 'threads': [], 'excluded_internal_sessions': [], 'limitations': ['Export al istoricului local Codex; conversațiile ChatGPT din cloud nu sunt incluse.', 'Fișierele referite sunt copiate în versiunea disponibilă la data exportului; versiunile istorice care nu mai există nu pot fi reconstruite.', 'Linkurile externe, fișierele Linux și fișierele de pe unități inaccesibile sunt consemnate în fișiere-index.json, nu declarate salvate.', 'Instrucțiunile de sistem și raționamentul intern nu sunt exportate. Mesajele vizibile și rezultatele instrumentelor sunt păstrate.', 'Conversațiile active sunt capturate până la citirea lor; salvați din nou după finalizarea lor.', 'Încadrarea prin director sau conversație-părinte este marcată în manifest.']}
groups = collections.defaultdict(list)
for tid, row in threads.items():
    if 'guardian' in row['source']:
        manifest['excluded_internal_sessions'].append(tid)
        continue
    pid, method = resolve_project(tid)
    groups[pid].append((row, method))

used_project_names = set()
for pid, project in list(projects.items()) + [(None, {'name': '_Fara proiect', 'rootPaths': []})]:
    folder_name = safe(project['name'])
    if folder_name.casefold() in used_project_names:
        folder_name += '--' + (pid or 'neatribuit')[-8:]
    used_project_names.add(folder_name.casefold())
    folder = OUT / folder_name
    folder.mkdir(exist_ok=True)
    entries, used_names = [], set()
    for row, method in sorted(groups[pid], key=lambda pair: (pair[0]['created_at'], pair[0]['id'])):
        items, diagnostics = load_items(row)
        is_subagent = row['id'] in parents or 'subagent' in row['source']
        title = row.get('name') or row['title'] or 'Fara titlu'
        dirname = safe(title)
        if dirname.casefold() in used_names or dirname in {'README.md', 'index.json', 'subagenti'}:
            dirname += '--' + row['id'][-8:]
        used_names.add(dirname.casefold())
        subdir = folder / ('subagenti' if is_subagent else '') / dirname
        subdir.mkdir(parents=True, exist_ok=False)
        metadata = {k: row[k] for k in ['id', 'cwd', 'created_at', 'updated_at', 'archived', 'source']}
        metadata.update(title=title, project_id=pid, project=project['name'], assignment_method=method, parent_thread_id=parents.get(row['id']), export_started_at_utc=STAMP, **diagnostics)
        messages = [x for x in items if x['item'].get('type') in {'userMessage', 'agentMessage'}]
        metadata.update(item_count=len(items), message_count=len(messages))
        metadata['content_sha256'] = hashlib.sha256(json.dumps(items, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
        assert all(visible(x['item']) for x in items)
        write_json(subdir / 'istoric.json', {'metadata': metadata, 'items': items})
        parts = [f'# {title}', f"ID: `{row['id']}`  \nProiect: {project['name']}  \nExport UTC: {STAMP}", 'Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.']
        output_parts = [f'# Rezultate — {title}', 'Răspunsuri și rezultate disponibile în istoricul local; fără limită de lungime aplicată de export.']
        for event in items:
            item = event['item']
            typ = item.get('type')
            if typ in {'userMessage', 'agentMessage'}:
                label = 'Utilizator' if typ == 'userMessage' else 'Asistent'
                parts.extend([f'## {label}', text_content(item)])
                if typ == 'agentMessage':
                    output_parts.extend(['## Asistent', text_content(item)])
            else:
                body = json.dumps(item, ensure_ascii=False, indent=2)
                fence = '`' * max(4, max((len(x.group()) for x in re.finditer(r'`+', body)), default=0) + 1)
                output_parts.extend(['## ' + str(typ), fence + 'json\n' + body + '\n' + fence])
        if not messages:
            parts.append('Nu există mesaje conversaționale în istoricul local al acestei sesiuni.')
        (subdir / 'conversatie.md').write_text('\n\n'.join(parts) + '\n', encoding='utf-8')
        (subdir / 'rezultate.md').write_text('\n\n'.join(output_parts) + '\n', encoding='utf-8')
        files = copy_files(items, row, subdir)
        metadata.update(files_copied=sum(f['status'] == 'copiat' for f in files), references_not_copied=sum(f['status'] != 'copiat' for f in files))
        write_json(subdir / 'metadate.json', metadata)
        entry = {**metadata, 'subagent': is_subagent, 'folder': subdir.relative_to(OUT).as_posix()}
        entries.append(entry)
        manifest['threads'].append(entry)
    info = {'id': pid, 'name': project['name'], 'roots': project['rootPaths'], 'conversations': sum(not e['subagent'] for e in entries), 'subagents': sum(e['subagent'] for e in entries), 'messages': sum(e['message_count'] for e in entries), 'files_copied': sum(e['files_copied'] for e in entries)}
    info['folder'] = folder_name
    signature = []
    for e in entries:
        file_index = json.loads((OUT / e['folder'] / 'fisiere-index.json').read_text(encoding='utf-8'))
        signature.append({'id': e['id'], 'title': e['title'], 'content_sha256': e['content_sha256'], 'files': [{k: v for k, v in f.items() if k in {'source_reference', 'status', 'sha256'}} for f in file_index]})
    info['content_sha256'] = hashlib.sha256(json.dumps(signature, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    write_json(folder / 'index.json', {'project': info, 'threads': entries})
    lines = [f"# {project['name']}", f"Conversații: {info['conversations']}; subagenți: {info['subagents']}; mesaje: {info['messages']}; fișiere copiate: {info['files_copied']}.", '| Conversație | Tip | Mesaje |', '|---|---|---|']
    for e in entries:
        title = e['title'].replace('\n', ' ').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')
        relative = pathlib.PurePosixPath(e['folder']).relative_to(folder.name).as_posix() + '/conversatie.md'
        lines.append(f"| [{title}]({quote(relative)}) | {'Subagent' if e['subagent'] else 'Conversație'} | {e['message_count']} |")
    if not entries:
        lines.append('\nNicio conversație locală asociată acestui proiect la momentul exportului.')
    (folder / 'README.md').write_text('\n\n'.join(lines[:2]) + '\n\n' + '\n'.join(lines[2:]) + '\n', encoding='utf-8')
    info['archives'] = zip_project(folder)
    manifest['projects'].append(info)
    print(json.dumps({k: v for k, v in info.items() if k not in {'roots', 'archives'}}, ensure_ascii=True), flush=True)

manifest['totals'] = {'projects': len(projects), 'conversations': sum(not t['subagent'] for t in manifest['threads']), 'subagents': sum(t['subagent'] for t in manifest['threads']), 'messages': sum(t['message_count'] for t in manifest['threads']), 'internal_sessions_excluded': len(manifest['excluded_internal_sessions']), 'missing_rollouts': sum(not t['rollout_exists'] for t in manifest['threads']), 'invalid_json_lines': sum(t['invalid_json_lines'] for t in manifest['threads']), 'files_copied': file_totals['copiat'], 'file_reference_statuses': dict(file_totals)}
manifest['export_completed_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
write_json(OUT / 'manifest.json', manifest)
root_lines = ['# Arhive conversații Codex', f'Export început la {STAMP}.', f"{manifest['totals']['conversations']} conversații principale și {manifest['totals']['subagents']} sesiuni de subagenți; {manifest['totals']['messages']} mesaje; {file_totals['copiat']} fișiere copiate.", 'Fiecare proiect conține subfoldere denumite după conversații. Titlurile incompatibile cu Windows sunt normalizate, cele lungi sunt scurtate, iar duplicatele primesc un sufix ID. Titlurile originale complete și ID-urile sunt păstrate în metadate.', 'Stare GitHub: neîncărcat. Nu încărcați într-un depozit public fără acceptarea explicită a publicării datelor.', '| Proiect | Conversații | Subagenți | Fișiere |', '|---|---:|---:|---:|']
for p in manifest['projects']:
    root_lines.append(f"| [{p['name']}]({quote(p['folder'])}/README.md) | {p['conversations']} | {p['subagents']} | {p['files_copied']} |")
root_lines.extend(['', '## Acoperire și limite', ''] + ['- ' + x for x in manifest['limitations']])
(OUT / 'README.md').write_text('\n\n'.join(root_lines[:5]) + '\n\n' + '\n'.join(root_lines[5:]) + '\n', encoding='utf-8')
checksums = []
for path in sorted(OUT.rglob('*')):
    if path.is_file() and path.name != 'SHA256SUMS.txt':
        with path.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        checksums.append(digest + '  ' + path.relative_to(OUT).as_posix())
(OUT / 'SHA256SUMS.txt').write_text('\n'.join(checksums) + '\n', encoding='utf-8')
print('TOTALS', json.dumps(manifest['totals']))
print('OUTPUT', str(OUT))

