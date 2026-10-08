"""Local YouTube audio library. Run with python app.py."""
import csv
import io
import json
import os
import re
import shutil
import threading
import uuid
import time
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image
from mutagen.id3 import ID3, APIC, COMM, TALB, TCON, TCOP, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK, TXXX, WOAS
from yt_dlp import YoutubeDL
import imageio_ffmpeg
from excel_import import read_excel

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'downloads'
OUTPUT.mkdir(exist_ok=True)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 11 * 1024 * 1024
pool = ThreadPoolExecutor(max_workers=1)
lock = threading.RLock()
jobs = {}
imports = {}
next_request_at = 0.0
COOLDOWN_FILE = ROOT / '.runtime' / 'youtube-cooldown.json'


def cooldown_remaining():
    try:
        until = float(json.loads(COOLDOWN_FILE.read_text())['until'])
        return max(0, int(until - time.time() + 1))
    except (OSError, ValueError, KeyError, TypeError):
        return 0


def stop_if_limited(job, error):
    message = str(error).lower().replace('’', "'")
    signals = ('429', 'too many requests', 'not a bot', 'captcha', 'unusual traffic', 'rate limit')
    if not any(signal in message for signal in signals):
        return False
    reason = 'YouTube a cerut verificare sau a limitat cererile. Descărcarea este oprită; pauză de minimum 30 de minute, fără reluare automată.'
    update(job, stop_reason=reason)
    COOLDOWN_FILE.parent.mkdir(exist_ok=True)
    COOLDOWN_FILE.write_text(json.dumps({'until': time.time() + 1800}), encoding='utf-8')
    return True


@contextmanager
def paced_request(job):
    global next_request_at
    while time.monotonic() < next_request_at:
        remaining = max(1, int(next_request_at - time.monotonic() + 1))
        update(job, message=f'Pauză între accesări YouTube: {remaining} secunde…')
        time.sleep(min(1, max(0, next_request_at - time.monotonic())))
    update(job, message='Accesez YouTube în ritm redus…')
    try:
        yield
    finally:
        next_request_at = time.monotonic() + 20


def finish_job(job, label='Gata'):
    with lock:
        state = jobs[job]
        files, errors = state['files'], state['errors']
        stopped = state.get('stop_reason')
        status = ('partial' if files else 'failed') if errors or stopped else 'done'
        message = f'{label}: {len(files)} salvate, {len(errors)} erori.'
        update(job, status=status, message=f'{stopped} {message}' if stopped else message)
FIELDS = ['file', 'artist', 'title', 'album', 'album_artist', 'genre', 'release_date', 'track', 'disc', 'youtube_title', 'channel', 'url', 'id', 'duration', 'upload_date', 'license', 'description', 'tags', 'categories', 'artist_source', 'album_source', 'cover', 'downloaded_at']
FIELDS += ['source_file', 'source_sheet', 'source_row', 'excel_values']


def safe_name(value, limit=85):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(value or '')).strip(' .')[:limit].rstrip(' .')
    if not name:
        name = 'Necunoscut'
    if re.match(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', name, re.I):
        name = '_' + name
    return name


def youtube_url(value):
    if not isinstance(value, str) or len(value) > 2048:
        raise ValueError('Introdu un link YouTube valid.')
    p = urlparse(value.strip())
    if p.scheme != 'https' or p.hostname not in {'youtube.com', 'www.youtube.com', 'music.youtube.com', 'm.youtube.com', 'youtu.be'} or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Sunt acceptate doar linkuri HTTPS YouTube / YouTube Music / youtu.be.')
    q = parse_qs(p.query)
    if p.hostname == 'youtu.be':
        video = p.path.strip('/')
    elif p.path == '/watch':
        video = q.get('v', [''])[0]
    elif p.path.startswith(('/shorts/', '/live/')):
        video = p.path.split('/')[2]
    else:
        video = ''
    playlist = q.get('list', [''])[0]
    if playlist and re.fullmatch(r'[\w-]{10,100}', playlist):
        return 'https://www.youtube.com/playlist?list=' + playlist
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', video):
        return 'https://www.youtube.com/watch?v=' + video
    raise ValueError('Linkul trebuie să indice o piesă sau un playlist, nu un canal.')


def metadata(info, playlist='', index=None):
    original = info.get('title') or info['id']
    artist = info.get('artist') or ', '.join(info.get('artists') or [])
    title = info.get('track') or original
    source = 'YouTube: artist'
    if not artist:
        parts = re.split(r'\s+[-–—]\s+', original, maxsplit=1)
        if len(parts) == 2 and all(parts):
            artist, parsed_title = parts
            title = info.get('track') or parsed_title
            source = 'dedus din titlul YouTube'
        else:
            artist = 'Artist necunoscut'
            source = 'indisponibil (canalul nu este presupus artist)'
    album = info.get('album') or playlist or ''
    return dict(artist=artist, title=title, album=album,
                album_artist=info.get('album_artist') or artist, genre=info.get('genre') or '',
                release_date=info.get('release_date') or info.get('release_year') or '',
                track=info.get('track_number') or index or '', disc=info.get('disc_number') or '',
                youtube_title=original, channel=info.get('channel') or info.get('uploader') or '',
                url='https://www.youtube.com/watch?v=' + info['id'], id=info['id'],
                duration=info.get('duration') or '', upload_date=info.get('upload_date') or '',
                license=info.get('license') or '', description=info.get('description') or '',
                tags=json.dumps(info.get('tags') or [], ensure_ascii=False),
                categories=json.dumps(info.get('categories') or [], ensure_ascii=False),
                artist_source=source, album_source='YouTube: album' if info.get('album') else ('playlist' if playlist else 'indisponibil'),
                cover=False, downloaded_at=datetime.now(timezone.utc).isoformat())


def write_tags(path, data, cover=None):
    tags = ID3()
    for key, frame in [('title', TIT2), ('artist', TPE1), ('album', TALB), ('album_artist', TPE2), ('genre', TCON), ('track', TRCK), ('disc', TPOS), ('license', TCOP)]:
        if data.get(key):
            tags.add(frame(encoding=1, text=[str(data[key])]))
    date = str(data.get('release_date') or '')
    if len(date) == 8 and date.isdigit():
        date = f'{date[:4]}-{date[4:6]}-{date[6:]}'
    if date:
        tags.add(TDRC(encoding=1, text=[date]))
    tags.add(WOAS(url=data['url']))
    tags.add(COMM(encoding=1, lang='ron', desc='Descriere YouTube', text=[data['description']]))
    for key in ['youtube_title', 'channel', 'id', 'upload_date', 'tags', 'categories', 'artist_source', 'album_source', 'downloaded_at']:
        tags.add(TXXX(encoding=1, desc=key, text=[str(data[key])]))
    if cover:
        tags.add(APIC(encoding=1, mime='image/jpeg', type=3, desc='Cover', data=cover))
    tags.save(path, v2_version=3, v1=2)


def csv_value(value):
    text = str(value)
    return "'" + text if text.lstrip().startswith(('=', '+', '-', '@')) or text.startswith(('\t', '\r', '\n')) else text


def write_catalog(path, row):
    rows = []
    if path.exists():
        with path.open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))
    rows = [r for r in rows if r['file'] != csv_value(row['file'])]
    rows.append({key: csv_value(row.get(key, '')) for key in FIELDS})
    temp = path.with_suffix('.csv.tmp')
    with temp.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def ffmpeg_path():
    return shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()


def update(job, **values):
    with lock:
        jobs[job].update(values)


class Log:
    def __init__(self, job):
        self.job = job
    def debug(self, message):
        pass
    def warning(self, message):
        with lock:
            jobs[self.job]['warnings'] = (jobs[self.job]['warnings'] + [str(message)])[-30:]
    def error(self, message):
        self.warning(message)


def run_job(job, url, quality, source=None, finalize=True):
    try:
        update(job, status='running', message='Citesc informațiile YouTube…')
        base = {'quiet': True, 'no_warnings': False, 'logger': Log(job), 'socket_timeout': 30,
                'retries': 0, 'fragment_retries': 0, 'extractor_retries': 0,
                'sleep_interval_requests': 2, 'sleep_interval': 8, 'max_sleep_interval': 8,
                'concurrent_fragment_downloads': 1,
                'ffmpeg_location': ffmpeg_path(), 'noplaylist': True, 'cachedir': str(ROOT / '.runtime' / 'yt-dlp'),
                'js_runtimes': {'node': {}} if shutil.which('node') else {'deno': {}}}
        with paced_request(job), YoutubeDL({**base, 'extract_flat': 'in_playlist', 'skip_download': True, 'ignoreerrors': False}) as ydl:
            listing = ydl.extract_info(url, download=False)
        if not listing:
            raise RuntimeError('YouTube nu a furnizat informații pentru acest link.')
        is_playlist = listing.get('_type') == 'playlist'
        entries = list(listing.get('entries') or []) if is_playlist else [listing]
        if not entries:
            raise RuntimeError('Playlistul este gol sau nu este accesibil.')
        playlist = listing.get('title', '') if is_playlist else ''
        folder = OUTPUT / (safe_name(playlist, 65) + ' [' + safe_name(listing['id'], 45) + ']' if is_playlist else 'Piese individuale')
        if source:
            folder = OUTPUT / source['folder']
            if is_playlist:
                folder = folder / (safe_name(playlist, 65) + ' [' + safe_name(listing['id'], 45) + ']')
        folder.mkdir(parents=True, exist_ok=True)
        update(job, total=len(entries), folder=str(folder.relative_to(OUTPUT)))
        for index, entry in enumerate(entries, 1):
            try:
                if not entry or not re.fullmatch(r'[A-Za-z0-9_-]{11}', entry.get('id', '')):
                    raise RuntimeError('Piesă indisponibilă sau eliminată din playlist.')
                video_url = 'https://www.youtube.com/watch?v=' + entry['id']
                update(job, current=index, percent=0, message=entry.get('title') or video_url)
                def progress(d):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        update(job, percent=round(100 * d.get('downloaded_bytes', 0) / total, 1) if total else 0)
                    elif d['status'] == 'finished':
                        update(job, percent=100, message='Conversie MP3 și scriere metadate…')
                staging = folder / '.work' / (entry['id'] + '-' + job[:8])
                staging.mkdir(parents=True, exist_ok=True)
                opts = {**base, 'format': 'bestaudio/best', 'outtmpl': str(staging / '%(id)s.%(ext)s'),
                        'writethumbnail': True, 'progress_hooks': [progress],
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': quality}],
                        'postprocessor_args': {'extractaudio+ffmpeg_o': ['-ar', '44100', '-ac', '2']}}
                with paced_request(job), YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    clean_info = ydl.sanitize_info(info)
                mp3 = staging / (entry['id'] + '.mp3')
                if not mp3.exists():
                    raise RuntimeError('Conversia nu a produs un fișier MP3.')
                data = metadata(info, playlist, index if is_playlist else None)
                if source:
                    data.update(source_file=source['file'], source_sheet=source['sheet'], source_row=source['row'],
                                excel_values=json.dumps(source['values'], ensure_ascii=False))
                cover = None
                for thumb in staging.iterdir():
                    if thumb.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
                        try:
                            with Image.open(thumb) as picture:
                                picture = picture.convert('RGB')
                                picture.thumbnail((600, 600))
                                buffer = io.BytesIO()
                                picture.save(buffer, 'JPEG', quality=85)
                                cover = buffer.getvalue()
                            break
                        except (OSError, ValueError):
                            continue
                data['cover'] = bool(cover)
                write_tags(mp3, data, cover)
                stem = safe_name(data['artist'], 60) + ' - ' + safe_name(data['title'], 90)
                target = folder / (stem + '.mp3')
                # Never replace an existing user file, even on repeat downloads.
                counter = 1
                while target.exists():
                    suffix = f' [{entry["id"]}]' + (f' ({counter})' if counter > 1 else '')
                    target = folder / (stem + suffix + '.mp3')
                    counter += 1
                mp3.replace(target)
                data['file'] = str(target.relative_to(OUTPUT))
                target.with_suffix('.info.json').write_text(json.dumps({'metadata': data, 'youtube': clean_info}, ensure_ascii=False, indent=2), encoding='utf-8')
                if cover:
                    target.with_suffix('.jpg').write_bytes(cover)
                write_catalog(folder / 'catalog.csv', data)
                write_catalog(OUTPUT / 'catalog.csv', data)
                with lock:
                    jobs[job]['files'].append(data)
                # Only remove files inside this job's known staging directory.
                for temporary in staging.iterdir():
                    if temporary.is_file():
                        temporary.unlink()
                staging.rmdir()
            except Exception as exc:
                with lock:
                    jobs[job]['errors'].append({'index': index, 'title': (entry or {}).get('title', ''), 'error': str(exc),
                                               'source': f"{source['sheet']} / rând {source['row']}" if source else ''})
                if stop_if_limited(job, exc):
                    break
        if not finalize:
            return
        finish_job(job)
    except Exception as exc:
        stop_if_limited(job, exc)
        if finalize:
            update(job, status='failed', message=jobs[job].get('stop_reason') or str(exc))
        else:
            with lock:
                jobs[job]['errors'].append({'index': 0, 'title': url, 'error': str(exc),
                                           'source': f"{source['sheet']} / rând {source['row']}"})


def import_folders(imported, create=False):
    root = 'Excel - ' + safe_name(Path(imported['filename']).stem, 65)
    folders = {}
    for sheet in imported['sheets']:
        if sheet['skipped']:
            continue
        name = f"{len(folders) + 1:02d} - {safe_name(sheet['name'], 50)}"
        folders[sheet['name']] = str(Path(root) / name)
        if create:
            (OUTPUT / folders[sheet['name']]).mkdir(parents=True, exist_ok=True)
    return folders


def run_import(job, imported, quality):
    try:
        run_import_links(job, imported, quality)
    except Exception as exc:
        update(job, status='failed', message=f'Import întrerupt: {exc}')


def run_import_links(job, imported, quality):
    folders = import_folders(imported, create=True)
    for number, entry in enumerate(imported['entries'], 1):
        update(job, batch_current=number, batch_total=len(imported['entries']), current=0, total=0,
               source_label=f"{entry['sheet']} · rândul {entry['row']}")
        source = {**entry, 'file': imported['filename'], 'folder': folders[entry['sheet']]}
        run_job(job, entry['url'], quality, source=source, finalize=False)
        if jobs[job].get('stop_reason'):
            break
    finish_job(job, 'Import terminat')


def new_job():
    # Caller holds lock so single-link and Excel starts cannot race.
    if any(j['status'] in {'queued', 'running'} for j in jobs.values()):
        return None
    job = uuid.uuid4().hex
    jobs.clear()
    jobs[job] = dict(id=job, status='queued', total=0, current=0, percent=0, files=[], errors=[], warnings=[], message='În așteptare…')
    return job


@app.errorhandler(413)
def too_large(_):
    return jsonify(error='Fișierul este prea mare. Maximum 10 MB.'), 413


@app.post('/api/imports')
def preview_import():
    upload = request.files.get('file')
    if not upload or not upload.filename.lower().endswith('.xlsx'):
        return jsonify(error='Alege un fișier Excel .xlsx. Pentru .xls, salvează-l mai întâi ca .xlsx.'), 400
    try:
        imported = read_excel(upload.read(), youtube_url)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    imported['filename'] = upload.filename.replace('\\', '/').split('/')[-1]
    imported['folders'] = import_folders(imported)
    token = uuid.uuid4().hex
    with lock:
        while len(imports) >= 5:
            imports.pop(next(iter(imports)))
        imports[token] = imported
    return jsonify(id=token, **imported)


@app.post('/api/imports/<token>/start')
def start_import(token):
    payload = request.get_json(silent=True) or {}
    quality = str(payload.get('quality', '192')) if isinstance(payload, dict) else ''
    if quality not in {'128', '192', '256', '320'}:
        return jsonify(error='Calitate MP3 invalidă.'), 400
    with lock:
        imported = imports.get(token)
        if not imported:
            return jsonify(error='Importul a expirat. Încarcă din nou fișierul.'), 404
        if not imported['entries']:
            return jsonify(error='Fișierul nu conține linkuri YouTube valide.'), 400
        job = new_job()
        if not job:
            return jsonify(error='O descărcare este deja în lucru. Așteaptă finalizarea.'), 409
        imports.pop(token)
    pool.submit(run_import, job, imported, quality)
    return jsonify(id=job), 202


@app.before_request
def local_only():
    if request.host.split(':')[0] not in {'127.0.0.1', 'localhost'}:
        return jsonify(error='Acces doar local.'), 403
    if request.method == 'POST':
        if request.headers.get('X-MP3-App') != 'local' or (request.headers.get('Origin') and request.headers['Origin'] != request.host_url.rstrip('/')):
            return jsonify(error='Cerere neautorizată.'), 403
        if request.path == '/api/jobs' or (request.path.startswith('/api/imports/') and request.path.endswith('/start')):
            remaining = cooldown_remaining()
            if remaining:
                return jsonify(error=f'Pauză după limitarea YouTube: mai sunt {(remaining + 59) // 60} minute. Nu reluăm automat.'), 429, {'Retry-After': str(remaining)}


@app.get('/')
def home():
    return render_template('index.html')


@app.get('/api/status')
def status():
    return jsonify(output=str(OUTPUT), ffmpeg=bool(Path(ffmpeg_path()).exists()), javascript=bool(shutil.which('deno') or shutil.which('node')))


@app.post('/api/jobs')
def create_job():
    payload = request.get_json(silent=True) or {}
    try:
        url = youtube_url(payload.get('url', ''))
        quality = str(payload.get('quality', '192'))
        if quality not in {'128', '192', '256', '320'}:
            raise ValueError('Calitate MP3 invalidă.')
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    with lock:
        job = new_job()
        if not job:
            return jsonify(error='O descărcare este deja în lucru. Așteaptă finalizarea.'), 409
    pool.submit(run_job, job, url, quality)
    return jsonify(id=job), 202


@app.get('/api/jobs/<job>')
def get_job(job):
    with lock:
        if job not in jobs:
            return jsonify(error='Sesiune inexistentă.'), 404
        return jsonify(jobs[job])


@app.get('/files/<path:name>')
def files(name):
    if any(part.startswith('.') for part in Path(name).parts):
        return jsonify(error='Fișier indisponibil.'), 404
    return send_from_directory(OUTPUT, name, as_attachment=True)


if __name__ == '__main__':
    print('MP3 Varvi: http://127.0.0.1:8765', flush=True)
    app.run(host='127.0.0.1', port=8765, debug=False)
