"""Serve the dashboard and sanitized snapshot; no network or Docker operations."""
from pathlib import Path
import re

from flask import Response

HTML_PATH = Path(__file__).with_name('domain_dashboard.html')
DATA_PATH = Path('/app/data/domain-monitor.json')
PREVIEW_PATH = Path('/app/data/domain-previews')


def dashboard_response(path):
    if path.startswith('/_domain-preview/'):
        filename = path.removeprefix('/_domain-preview/')
        if not re.fullmatch(r'[0-9a-f]{64}\.jpg', filename):
            response = Response(status=404)
        else:
            try:
                response = Response((PREVIEW_PATH / filename).read_bytes(), mimetype='image/jpeg')
            except OSError:
                response = Response(status=404)
    elif path == '/_domain-previews.json':
        try:
            response = Response((PREVIEW_PATH / 'manifest.json').read_text(encoding='utf-8'), mimetype='application/json')
        except OSError:
            response = Response('{"schema_version":1,"previews":{}}', mimetype='application/json')
    elif path == '/_domain-status.json':
        try:
            body = DATA_PATH.read_text(encoding='utf-8')
            response = Response(body, mimetype='application/json')
        except OSError:
            response = Response('{"error":"Prima verificare este în curs. Reîncercați în câteva minute."}', status=503, mimetype='application/json')
    else:
        response = Response(HTML_PATH.read_text(encoding='utf-8'), mimetype='text/html')
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
