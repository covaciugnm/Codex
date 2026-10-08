"""Publish verified Codex snapshots to the user-designated GitHub repository."""
import argparse
import datetime as dt
import json
import os
import pathlib
import shutil
import stat
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from protejeaza_publicarea import protect_project

def copy_public_file(source, destination):
    # Source attributes must not prevent later updates or credential masking.
    target = pathlib.Path(destination)
    if target.is_file() and not target.stat().st_mode & stat.S_IWRITE:
        target.chmod(target.stat().st_mode | stat.S_IWRITE)
    result = shutil.copy2(source, destination)
    target.chmod(target.stat().st_mode | stat.S_IWRITE)
    return result

REMOTE = 'git@github.com:covaciugnm/Codex.git'
parser = argparse.ArgumentParser()
parser.add_argument('snapshot', type=pathlib.Path)
parser.add_argument('--repo', type=pathlib.Path, default=pathlib.Path(__file__).parent / 'GitHub-Codex')
parser.add_argument('--allow-public', action='store_true', help='Only after explicit user authorization to publish publicly.')
parser.add_argument('--ssh-key', type=pathlib.Path, help='Private key corresponding to the github-codex-deploy public key.')
parser.add_argument('--plan', action='store_true', help='Read-only local comparison; no network, clone, commit or push.')
args = parser.parse_args()
snapshot = args.snapshot.resolve()
repo = args.repo.resolve()
manifest = json.loads((snapshot / 'manifest.json').read_text(encoding='utf-8'))
index_name = '.codex-backup-index.json'
previous = json.loads((repo / index_name).read_text(encoding='utf-8')) if (repo / index_name).exists() else {'projects': {}}

def project_key(project):
    return project['id'] or '_Fara proiect'

def changes():
    return [p for p in manifest['projects'] if previous.get('projects', {}).get(project_key(p), {}).get('content_sha256') != p['content_sha256']]

if args.plan:
    print(json.dumps({'changed_projects': [p['name'] for p in changes()], 'repository': REMOTE, 'no_changes_made': True}, ensure_ascii=True))
    sys.exit(0)

config_path = pathlib.Path(__file__).with_name('conexiune-github.json')
config = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
key_path = args.ssh_key or (pathlib.Path(config['ssh_key_path']) if config.get('ssh_key_path') else None)
git_options = []
if config.get('transport') == 'https' and not args.ssh_key:
    gh = config.get('gh_executable') or shutil.which('gh')
    if not gh or not pathlib.Path(gh).is_file():
        raise SystemExit('GitHub CLI nu este disponibil la calea configurata.')
    probe = subprocess.run([gh, 'api', 'repos/covaciugnm/Codex'], capture_output=True, text=True, timeout=30)
    if probe.returncode or not json.loads(probe.stdout).get('permissions', {}).get('push'):
        raise SystemExit('PUSH OPRIT: contul GitHub CLI nu are drept de scriere in covaciugnm/Codex. Finalizati autentificarea contului autorizat.')
    REMOTE = 'https://github.com/covaciugnm/Codex.git'
    helper = '!' + shlex.quote(pathlib.Path(gh).as_posix()) + ' auth git-credential'
    git_options = ['-c', 'credential.helper=', '-c', 'credential.helper=' + helper]
else:
    if not key_path or not key_path.is_file():
        raise SystemExit('PUSH OPRIT: lipseste calea cheii private github-codex-deploy. Cheia implicita apartine altui depozit.')
    public_path = pathlib.Path(str(key_path) + '.pub')
    if public_path.is_file():
        public_key = public_path.read_text(encoding='utf-8').split()
    else:
        public_key = subprocess.check_output(['ssh-keygen', '-y', '-f', str(key_path)], text=True, timeout=20).split()
    if len(public_key) < 2 or public_key[1] != 'AAAAC3NzaC1lZDI1NTE5AAAAIKOQEAtQpWAsn3k33qc4sDC7bf3r26hAiV7vOjK9uEuf':
        raise SystemExit('Cheia configurata nu corespunde cheii publice furnizate pentru acest backup.')

subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name('verifica_arhiva.py')), str(snapshot)], check=True)
request = urllib.request.Request('https://api.github.com/repos/covaciugnm/Codex', headers={'User-Agent': 'Codex-Conversation-Backup', 'Accept': 'application/vnd.github+json'})
try:
    with urllib.request.urlopen(request, timeout=20) as response:
        remote_info = json.load(response)
    if not remote_info.get('private') and not (args.allow_public or config.get('public_upload_authorized') is True):
        raise SystemExit('PUSH OPRIT: depozitul este public; este necesara alegerea utilizatorului privind publicarea.')
except urllib.error.HTTPError as exc:
    if exc.code != 404:
        raise
    # Private repositories are not visible to anonymous API calls. Authenticated
    # SSH below must still establish access to this exact, user-selected repo.

environment = dict(os.environ)
environment['GIT_TERMINAL_PROMPT'] = '0'
if key_path:
    environment['GIT_SSH_COMMAND'] = 'ssh -i ' + shlex.quote(key_path.resolve().as_posix()) + ' -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=15'

def git(*arguments, check=True):
    result = subprocess.run(['git', *git_options, '-C', str(repo), *arguments], capture_output=True, text=True, encoding='utf-8', errors='replace', env=environment, timeout=3600 if arguments[0] == 'push' else 300)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result

if not (repo / '.git').is_dir():
    if repo.exists() and any(repo.iterdir()):
        raise SystemExit('Directorul de destinatie nu este gol si nu este un checkout Git.')
    subprocess.run(['git', *git_options, 'clone', REMOTE, str(repo)], check=True, env=environment, timeout=300)
if git('remote', 'get-url', 'origin').stdout.strip() not in {REMOTE, 'https://github.com/covaciugnm/Codex.git'}:
    raise SystemExit('Origin diferit de destinatia autorizata.')
git('config', 'core.longpaths', 'true')
if git('status', '--porcelain').stdout.strip():
    raise SystemExit('Checkout-ul are modificari locale; inspectati-le inainte de sincronizare.')
remote_main = git('ls-remote', 'origin', 'refs/heads/main').stdout.strip()
if remote_main:
    git('fetch', 'origin', 'main')
    git('merge', '--ff-only', 'origin/main')
else:
    git('symbolic-ref', 'HEAD', 'refs/heads/main')
if git('branch', '--show-current').stdout.strip() != 'main':
    raise SystemExit('Checkout-ul trebuie sa foloseasca ramura main.')
previous = json.loads((repo / index_name).read_text(encoding='utf-8')) if (repo / index_name).exists() else {'projects': {}}
changed = changes()
print(json.dumps({'changed_projects': [p['name'] for p in changed]}, ensure_ascii=True), flush=True)
staged_paths = []
large_paths = []
for project in changed:
    folder_name = pathlib.PurePosixPath(project['archives'][0]['path']).parts[0]
    source = snapshot / folder_name
    large_paths.extend(p.relative_to(snapshot).as_posix() for p in source.rglob('*') if p.is_file() and (p.stat().st_size >= 5 * 1024 * 1024 or p.suffix.lower() == '.zip'))
if large_paths:
    if git('lfs', 'version', check=False).returncode:
        raise SystemExit('Git LFS este necesar pentru fisierele mai mari de 100 MiB. Nu s-a omis niciun fisier.')
    git('lfs', 'install', '--local')
    for path in large_paths:
        git('lfs', 'track', '--filename', path)
    staged_paths.append('.gitattributes')
for project in changed:
    folder_name = pathlib.PurePosixPath(project['archives'][0]['path']).parts[0]
    source = snapshot / folder_name
    shutil.copytree(source, repo / folder_name, dirs_exist_ok=True, copy_function=copy_public_file)
    masked = protect_project(repo / folder_name)
    print(json.dumps({'prepared_project': project['name'], 'credential_files_masked': len(masked)}, ensure_ascii=True), flush=True)
    staged_paths.append(folder_name)
    previous.setdefault('projects', {})[project_key(project)] = {'name': project['name'], 'content_sha256': project['content_sha256'], 'snapshot_utc': manifest['export_started_at_utc'], 'folder': folder_name}
if changed:
    previous['updated_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    (repo / index_name).write_text(json.dumps(previous, ensure_ascii=False, indent=2), encoding='utf-8')
    staged_paths.append(index_name)
    for filename in ['PROTOCOL-SALVARE.md', 'Salveaza-Codex.ps1', 'export_codex.py', 'verifica_arhiva.py', 'sincronizeaza_github.py', 'protejeaza_publicarea.py']:
        shutil.copy2(pathlib.Path(__file__).parent / filename, repo / filename)
        staged_paths.append(filename)
    lines = ['# Arhive Codex', '', 'Conversații, rezultate și fișiere organizate după proiect. Fiecare proiect este actualizat numai când conținutul său se schimbă.', '', 'Salvarea automată rulează la 6 ore. Versiunile precedente rămân în istoricul Git. Consultați PROTOCOL-SALVARE.md și indexurile proiectelor pentru acoperire și fișiere indisponibile.', '']
    from urllib.parse import quote
    for project in previous['projects'].values():
        lines.append('- [' + project['name'] + '](' + quote(project['folder']) + '/README.md)')
    (repo / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    staged_paths.append('README.md')
    git('add', '--', *staged_paths)
    if git('diff', '--cached', '--quiet', check=False).returncode:
        identity = []
        if not git('config', 'user.name', check=False).stdout.strip():
            identity += ['-c', 'user.name=Codex Backup']
        if not git('config', 'user.email', check=False).stdout.strip():
            identity += ['-c', 'user.email=codex-backup@localhost']
        git(*identity, 'commit', '-m', 'Salvare Codex: ' + manifest['export_started_at_utc'] + ' (' + str(len(changed)) + ' proiecte)')
local_head = git('rev-parse', 'HEAD', check=False)
if local_head.returncode:
    print('Nicio modificare si niciun commit de incarcat.')
    sys.exit(0)
head = local_head.stdout.strip()
remote_head = remote_main.split()[0] if remote_main else None
if head != remote_head:
    # Also retries a previously committed but not yet pushed snapshot.
    print('PUSH_STARTED ' + head, flush=True)
    git('push', 'origin', 'HEAD:main')
verified = git('ls-remote', 'origin', 'refs/heads/main').stdout.split()[0]
if verified != head:
    raise SystemExit('Commitul distant nu corespunde commitului local.')
receipt = {'verified_remote_commit': head, 'repository': REMOTE, 'changed_projects': [p['name'] for p in changed], 'verified_at_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
(pathlib.Path(__file__).parent / 'ultima-incarcare.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=True))
