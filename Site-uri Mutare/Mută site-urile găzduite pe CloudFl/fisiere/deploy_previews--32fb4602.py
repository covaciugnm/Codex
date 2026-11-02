"""Deploy homepage previews and preserve existing schedules and storefronts."""
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/saga-server/site-uri/site-uri-wordpress/_motor')
APP = ROOT / 'backend/app'
STAGING = ROOT / 'domain-monitor/staging'
backup = ROOT / 'domain-monitor/backups' / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-previews')
backup.mkdir(parents=True, mode=0o700)
prefix = APP / 'wp_prefix.py'
source = prefix.read_text()
old = 'elif path in ("/", "/_domain-status.json") and method in ("GET", "HEAD") and "tenant=" not in environ.get("QUERY_STRING", ""):'
new = 'elif (path in ("/", "/_domain-status.json", "/_domain-previews.json") or path.startswith("/_domain-preview/")) and method in ("GET", "HEAD") and "tenant=" not in environ.get("QUERY_STRING", ""):'
if old not in source:
    raise SystemExit('Middleware changed; inspect before deployment.')
for name in ['wp_prefix.py', 'domain_dashboard.py', 'domain_dashboard.html']:
    shutil.copy2(APP / name, backup / name)
cron = subprocess.check_output(['crontab', '-l'], text=True)
(backup / 'crontab.txt').write_text(cron)
for name in ['domain_dashboard.py', 'domain_dashboard.html']:
    temp = APP / (name + '.preview-new')
    shutil.copyfile(STAGING / name, temp)
    os.chmod(temp, 0o644)
    os.replace(temp, APP / name)
updated = source.replace(old, new, 1)
compile(updated, str(prefix), 'exec')
temp = APP / 'wp_prefix.py.preview-new'
temp.write_text(updated)
os.chmod(temp, 0o644)
os.replace(temp, prefix)
marker = '# mutaresite-domain-previews'
line = '1-59/5 * * * * /usr/bin/flock -n ' + str(ROOT / 'domain-monitor/previews.lock') + ' /usr/bin/timeout 275 /usr/bin/python3 ' + str(ROOT / 'domain-monitor/capture_previews.py') + ' >> ' + str(ROOT / 'domain-monitor/previews.log') + ' 2>&1 ' + marker
updated_cron = '\n'.join(x for x in cron.splitlines() if marker not in x).rstrip() + '\n' + line + '\n'
subprocess.run(['crontab', '-'], input=updated_cron, text=True, check=True)
subprocess.run(['docker', 'kill', '--signal=HUP', 'wpsites-backend-1'], check=True)
print(json.dumps({'backup': str(backup), 'schedule': line, 'status': 'installed'}))
