"""Local video concatenation, upload API and background processing."""
import json
import re
import shutil
import subprocess
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from flask import Blueprint, jsonify, request

EXTENSIONS = {'.mp4', '.mkv', '.mov', '.avi', '.webm', '.m4v', '.mpeg', '.mpg', '.ts'}
MAX_FILE = 4 * 1024**3


def probe_video(ffmpeg, path):
    result = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path)], capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=60)
    text = result.stderr
    duration = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', text)
    if not duration or not re.search(r'Stream .*Video:', text):
        raise ValueError(f'Videoclip invalid sau durată necunoscută: {path.name}')
    h, m, s = map(float, duration.groups())
    seconds = h * 3600 + m * 60 + s
    if seconds <= 0:
        raise ValueError('Videoclipul are durată zero.')
    return seconds, bool(re.search(r'Stream .*Audio:', text))


def run_ffmpeg(args, log_path, duration, progress):
    with log_path.open('w', encoding='utf-8') as log:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=log, text=True, encoding='utf-8', errors='replace') as process:
            for line in process.stdout:
                if line.startswith('out_time_us='):
                    try:
                        progress(min(99, max(0, int(float(line.split('=')[1]) / 1000000 / duration * 100))))
                    except ValueError:
                        pass
            code = process.wait()
    if code:
        raise RuntimeError('FFmpeg: ' + log_path.read_text(encoding='utf-8', errors='replace')[-2000:])


def concatenate_videos(ffmpeg, sources, output, work, progress):
    """Normalize mixed clips, adding silence when absent, then join in input order."""
    if len(sources) < 2 or len(sources) > 100:
        raise ValueError('Alege între 2 și 100 de videoclipuri.')
    if output.exists():
        raise ValueError('Fișierul destinație există deja.')
    work.mkdir(parents=True, exist_ok=True)
    parts, total_duration = [], 0
    for index, source in enumerate(sources):
        progress(index, 0, f'Pregătesc videoclipul {index + 1}/{len(sources)}…')
        duration, has_audio = probe_video(ffmpeg, source)
        total_duration += duration
        part = work / f'part-{index:04d}.mp4'
        args = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', str(source)]
        if not has_audio:
            args += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        args += ['-map', '0:v:0', '-map', '0:a:0' if has_audio else '1:a:0',
                 '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30',
                 '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-threads', '2', '-pix_fmt', 'yuv420p',
                 '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-af', 'apad',
                 '-t', str(duration), '-map_metadata', '-1', '-progress', 'pipe:1', '-nostats', str(part)]
        run_ffmpeg(args, work / 'ffmpeg.log', duration,
                   lambda percent: progress(index, percent, f'Convertesc videoclipul {index + 1}/{len(sources)}…'))
        parts.append(part)
    listing = work / 'concat.txt'
    # Generated relative names only: no user path is interpreted by the concat demuxer.
    listing.write_text(''.join(f"file '{p.name}'\n" for p in parts), encoding='utf-8')
    temporary = work / 'combined.mp4'
    progress(len(sources), 0, 'Unesc videoclipurile și finalizez MP4-ul…')
    run_ffmpeg([ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-f', 'concat', '-safe', '1',
                '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', '-progress', 'pipe:1', '-nostats', str(temporary)],
               work / 'ffmpeg.log', total_duration, lambda percent: progress(len(sources), percent, 'Finalizez MP4-ul…'))
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary.replace(output)


def create_merge_blueprint(output_root, runtime_root, ffmpeg_provider):
    blueprint = Blueprint('video_merge', __name__)
    uploads, jobs = {}, {}
    lock = threading.RLock()
    executor = ThreadPoolExecutor(max_workers=1)
    upload_root = runtime_root / 'merge-uploads'

    @blueprint.before_request
    def upload_limit():
        if request.path == '/api/merge/uploads':
            request.max_content_length = MAX_FILE + 1024 * 1024

    @blueprint.post('/api/merge/uploads')
    def upload():
        file = request.files.get('file')
        if not file or Path(file.filename or '').suffix.lower() not in EXTENSIONS:
            return jsonify(error='Alege un videoclip MP4, MKV, MOV, AVI, WEBM, M4V, MPEG, MPG sau TS.'), 400
        with lock:
            if len(uploads) >= 100:
                return jsonify(error='Maximum 100 de videoclipuri încărcate. Elimină fișiere sau finalizează unirea.'), 400
        token = uuid.uuid4().hex
        upload_root.mkdir(parents=True, exist_ok=True)
        path = upload_root / (token + Path(file.filename).suffix.lower())
        size = 0
        try:
            with path.open('xb') as destination:
                while chunk := file.stream.read(1024 * 1024):
                    size += len(chunk)
                    if size > MAX_FILE:
                        raise ValueError('Maximum 4 GB pentru fiecare videoclip.')
                    if shutil.disk_usage(upload_root).free < len(chunk) + 512 * 1024**2:
                        raise ValueError('Spațiu insuficient pe disc pentru încărcare.')
                    destination.write(chunk)
            if size == 0:
                raise ValueError('Fișierul este gol.')
        except (ValueError, OSError) as exc:
            path.unlink(missing_ok=True)
            return jsonify(error=str(exc)), 400
        name = file.filename.replace('\\', '/').split('/')[-1]
        with lock:
            uploads[token] = {'path': path, 'name': name, 'size': size, 'in_use': False}
        return jsonify(id=token, name=name, size=size), 201

    @blueprint.post('/api/merge/uploads/<token>/remove')
    def remove(token):
        with lock:
            item = uploads.get(token)
            if item and item['in_use']:
                return jsonify(error='Videoclipul este folosit de o unire în curs.'), 409
            if item:
                item['path'].unlink(missing_ok=True)
                uploads.pop(token)
        return jsonify(ok=True)

    def worker(job, items, name):
        work = runtime_root / 'merge-work' / job
        target = output_root / 'Videoclipuri unite' / (name + ' [' + job[:8] + '].mp4')
        def progress(index, percent, message):
            with lock:
                jobs[job].update(status='running', message=message,
                                 percent=round((index + percent / 100) / (len(items) + 1) * 100, 1))
        try:
            concatenate_videos(ffmpeg_provider(), [item['path'] for item in items], target, work, progress)
            target.with_suffix('.json').write_text(json.dumps({'files_in_order': [i['name'] for i in items]}, ensure_ascii=False, indent=2), encoding='utf-8')
            with lock:
                jobs[job].update(status='done', percent=100, message='Videoclipul unit este gata.', file=str(target.relative_to(output_root)))
        except Exception as exc:
            with lock:
                jobs[job].update(status='failed', message=str(exc))
        finally:
            with lock:
                for item in items:
                    item['in_use'] = False
                if jobs[job]['status'] == 'done':
                    for token, item in list(uploads.items()):
                        if any(item is used for used in items):
                            item['path'].unlink(missing_ok=True)
                            uploads.pop(token)
            # Keep uploaded copies for retry; discard only this job's generated intermediates.
            resolved = work.resolve()
            if resolved.is_relative_to((runtime_root / 'merge-work').resolve()) and resolved.exists():
                shutil.rmtree(resolved)

    @blueprint.post('/api/merge/jobs')
    def start():
        payload = request.get_json(silent=True)
        ids = payload.get('ids') if isinstance(payload, dict) else None
        if not isinstance(ids, list) or not 2 <= len(ids) <= 100 or not all(isinstance(i, str) for i in ids) or len(set(ids)) != len(ids):
            return jsonify(error='Alege între 2 și 100 de videoclipuri distincte.'), 400
        name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(payload.get('name') or 'Videoclip unit')).strip(' .')[:70] or 'Videoclip unit'
        if re.match(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', name, re.I):
            name = '_' + name
        with lock:
            if any(j['status'] in {'queued', 'running'} for j in jobs.values()):
                return jsonify(error='O unire este deja în lucru.'), 409
            if any(i not in uploads for i in ids):
                return jsonify(error='Un fișier a expirat. Adaugă videoclipurile din nou.'), 400
            items = [uploads[i] for i in ids]
            for item in items:
                item['in_use'] = True
            job = uuid.uuid4().hex
            jobs.clear()
            jobs[job] = {'id': job, 'status': 'queued', 'percent': 0, 'message': 'În așteptare…'}
        executor.submit(worker, job, items, name)
        return jsonify(id=job), 202

    @blueprint.get('/api/merge/jobs/<job>')
    def status(job):
        with lock:
            return (jsonify(jobs[job]) if job in jobs else (jsonify(error='Unirea nu mai există în această sesiune.'), 404))

    return blueprint
