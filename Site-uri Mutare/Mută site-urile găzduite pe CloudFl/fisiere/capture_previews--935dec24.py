"""Capture public homepages in fresh, unauthenticated browser contexts.

Only URLs already in the inventory are considered. There is no public capture
endpoint. One cached image per URL, with atomic image/manifest replacement.
"""
import argparse
import asyncio
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
from urllib.parse import urlsplit

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def age(timestamp):
    try:
        return (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(timestamp)).total_seconds()
    except (TypeError, ValueError):
        return float('inf')


def atomic_json(path, data):
    fd, name = tempfile.mkstemp(prefix='.manifest-', suffix='.json', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        os.chmod(name, 0o644)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def preferred_copy(row):
    public = row['public_url'].rstrip('/')
    links = [l for l in row.get('docker', {}).get('links', []) if l['url'].rstrip('/') != public]
    return next((l for l in links if l.get('responds') and 200 <= (l.get('status') or 0) < 400 and not l.get('error') and not l.get('https_error')), links[0] if links else None)


def capture_targets(snapshot):
    targets = {}
    for row in snapshot['domains']:
        priority = 0 if row.get('hosting_account') != 'În afara listelor Hosterion' else 1
        candidates = [(row['public_url'], row.get('http', {}))]
        clone = preferred_copy(row)
        if clone:
            candidates.append((clone['url'], clone))
        for url, check in candidates:
            parsed = urlsplit(url)
            if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
                continue
            target = {'url': url, 'check': check, 'priority': priority}
            if url not in targets or priority < targets[url]['priority']:
                targets[url] = target
    return targets


def unavailable(entry, message):
    entry['checked_at'] = now()
    entry['error'] = message
    entry['status'] = 'ready' if entry.get('image_url') else 'unavailable'
    return entry


async def run(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / 'manifest.json'
    snapshot = json.loads(Path(args.snapshot).read_text())
    targets = capture_targets(snapshot)
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    previews = {}
    queue = []
    for url, target in targets.items():
        entry = dict(previous.get('previews', {}).get(url) or {'url': url, 'status': 'pending', 'image_url': None, 'captured_at': None, 'checked_at': None, 'error': None})
        check = target['check']
        entry['http_status'] = check.get('status')
        entry['final_url'] = check.get('final_url') or url
        if check.get('responds') is False:
            unavailable(entry, 'Adresa nu răspunde la ultima verificare. ' + (check.get('error') or ''))
        elif args.force or (entry.get('image_url') and age(entry.get('captured_at')) >= args.ttl) or (not entry.get('image_url') and (args.retry_failed or age(entry.get('checked_at')) >= 300)):
            queue.append(target)
        previews[url] = entry
    manifest = {'schema_version': 1, 'generated_at': now(), 'refresh_seconds': 300,
                'capture_refresh_seconds': args.ttl, 'previews': previews}

    def save():
        manifest['generated_at'] = now()
        atomic_json(manifest_path, manifest)

    save()
    started = time.monotonic()
    queue.sort(key=lambda t: (bool(previews[t['url']].get('image_url')), t['priority'], t['url']))
    tasks = asyncio.Queue()
    for target in queue:
        tasks.put_nowait(target)
    counters = {'ready': 0, 'failed': 0, 'queued': len(queue)}
    if queue:
        async with async_playwright() as p:
            browser = await p.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True, args=['--disable-dev-shm-usage'])

            async def worker():
                while not tasks.empty() and time.monotonic() - started < args.budget:
                    try:
                        target = tasks.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    url = target['url']
                    entry = previews[url]
                    context = await browser.new_context(viewport={'width': 1280, 'height': 800}, device_scale_factor=1, locale='ro-RO',
                                                        color_scheme='light', reduced_motion='reduce', accept_downloads=False,
                                                        service_workers='block')
                    page = await context.new_page()
                    try:
                        # Video/audio loading is unnecessary for a still homepage preview.
                        async def resource_filter(route):
                            if route.request.resource_type == 'media':
                                await route.abort()
                            else:
                                await route.continue_()
                        await page.route('**/*', resource_filter)
                        response = await page.goto(url, wait_until='domcontentloaded', timeout=15000)
                        if response is None:
                            raise RuntimeError('No response')
                        await page.wait_for_timeout(1200)
                        await page.locator('body').wait_for(timeout=3000)
                        key = hashlib.sha256(url.encode()).hexdigest()
                        temp = output / (key + '.tmp.jpg')
                        await page.screenshot(path=str(temp), type='jpeg', quality=70, full_page=False, animations='disabled', timeout=8000)
                        os.chmod(temp, 0o644)
                        os.replace(temp, output / (key + '.jpg'))
                        captured = now()
                        entry.update(status='ready', image_url='/_domain-preview/' + key + '.jpg?v=' + str(int(time.time())),
                                     captured_at=captured, checked_at=captured, http_status=response.status, final_url=page.url,
                                     error=None if response.status < 400 else 'Captura arată răspunsul HTTP ' + str(response.status) + ' al adresei.')
                        counters['ready'] += 1
                    except Exception as exc:
                        message = str(exc)
                        reason = 'Captura nu a putut fi obținută.'
                        if 'Timeout' in type(exc).__name__ or 'Timeout' in message:
                            reason = 'Pagina nu s-a încărcat în timpul alocat capturii.'
                        elif 'ERR_CERT' in message or 'SSL' in message:
                            reason = 'Certificatul HTTPS nu permite încărcarea paginii.'
                        elif 'ERR_NAME_NOT_RESOLVED' in message:
                            reason = 'Domeniul nu se rezolvă în DNS.'
                        unavailable(entry, reason)
                        counters['failed'] += 1
                    finally:
                        await context.close()
                        tasks.task_done()
                        save()
            await asyncio.gather(*(worker() for _ in range(args.workers)))
            await browser.close()
    manifest['summary'] = {**counters, 'remaining': tasks.qsize(), 'total': len(targets)}
    save()
    print(json.dumps({'generated_at': manifest['generated_at'], **manifest['summary']}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', default=str(DATA / 'domain-monitor.json'))
    parser.add_argument('--output', default=str(DATA / 'domain-previews'))
    parser.add_argument('--ttl', type=int, default=1800)
    parser.add_argument('--budget', type=int, default=240)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--retry-failed', action='store_true')
    asyncio.run(run(parser.parse_args()))


if __name__ == '__main__':
    main()
