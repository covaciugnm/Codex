"""Install the root dashboard without changing storefront routes or data."""
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/saga-server/site-uri/site-uri-wordpress/_motor')
STAGING = ROOT / 'domain-monitor/staging'
APP = ROOT / 'backend/app'
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup = ROOT / 'domain-monitor/backups' / stamp
backup.mkdir(parents=True, mode=0o700)
prefix = APP / 'wp_prefix.py'
source = prefix.read_text()
old_condition = 'elif path == "/" and method in ("GET", "HEAD") and "tenant=" not in environ.get("QUERY_STRING", ""):'
new_condition = 'elif path in ("/", "/_domain-status.json") and method in ("GET", "HEAD") and "tenant=" not in environ.get("QUERY_STRING", ""):'
old_response = 'resp = Response(_index_html(sorted(self.slugs)), mimetype="text/html")'
new_response = 'from .domain_dashboard import dashboard_response\n\n                resp = dashboard_response(path)'
if old_condition not in source or old_response not in source:
    raise SystemExit('Middleware changed or already installed; inspect before deploying.')
for name in ['wp_prefix.py', 'domain_dashboard.py', 'domain_dashboard.html']:
    path = APP / name
    if path.exists():
        shutil.copy2(path, backup / name)
cron = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
if cron.returncode not in (0, 1) or cron.returncode == 1 and 'no crontab' not in cron.stderr:
    raise SystemExit('Cannot read crontab safely.')
(backup / 'crontab.txt').write_text(cron.stdout)
for name in ['domain_dashboard.py', 'domain_dashboard.html']:
    temp = APP / (name + '.mutaresite-new')
    shutil.copyfile(STAGING / name, temp)
    os.chmod(temp, 0o644)
    os.replace(temp, APP / name)
new = source.replace(old_condition, new_condition, 1).replace(old_response, new_response, 1)
compile(new, str(prefix), 'exec')
temp = APP / 'wp_prefix.py.mutaresite-new'
temp.write_text(new)
os.chmod(temp, 0o644)
os.replace(temp, prefix)
marker = '# mutaresite-domain-monitor'
line = '*/5 * * * * /usr/bin/flock -n ' + str(ROOT / 'domain-monitor/monitor.lock') + ' /usr/bin/timeout 275 /usr/bin/python3 ' + str(ROOT / 'domain-monitor/monitor_domains.py') + ' >> ' + str(ROOT / 'domain-monitor/monitor.log') + ' 2>&1 ' + marker
new_cron = '\n'.join(x for x in cron.stdout.splitlines() if marker not in x).rstrip() + '\n' + line + '\n'
subprocess.run(['crontab', '-'], input=new_cron, text=True, check=True)
subprocess.run(['docker', 'kill', '--signal=HUP', 'wpsites-backend-1'], check=True)
print(json.dumps({'backup': str(backup), 'cron': line, 'deployment': 'installed'}))
