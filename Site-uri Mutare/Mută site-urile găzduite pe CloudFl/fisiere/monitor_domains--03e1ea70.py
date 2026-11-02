"""Read-only DNS/HTTP/Docker monitor. Fixed registry, no public scan endpoint.

Runs on the host, writes one atomic public snapshot; the web container never gets
the Docker socket. Browser refresh and this scheduled host job are independent.
"""
import argparse
import concurrent.futures
import datetime as dt
import functools
import ipaddress
import json
import os
import pathlib
import re
import subprocess
import tempfile
import time
from urllib.parse import urljoin, urlsplit

ROOT = pathlib.Path(__file__).resolve().parent
UA = 'Mozilla/5.0 (compatible; DomainInventory/1.0; +https://wordpress.alba-vision.ro/)'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


@functools.lru_cache(maxsize=4096)
def dns_query(domain, record):
    for resolver in ['1.1.1.1', '8.8.8.8']:
        try:
            p = subprocess.run(['dig', '@' + resolver, domain, record, '+time=2', '+tries=1', '+noall', '+answer', '+comments'],
                               capture_output=True, text=True, timeout=4)
            status = re.search(r'status: (\w+)', p.stdout)
            if not status or status.group(1) not in ('NOERROR', 'NXDOMAIN'):
                continue
            values = []
            for line in p.stdout.splitlines():
                bits = line.split()
                if len(bits) >= 5 and bits[3] == record:
                    values.append(bits[4].rstrip('.'))
            return {'status': status.group(1), 'values': sorted(set(values))}
        except (OSError, subprocess.TimeoutExpired):
            continue
    return {'status': 'ERROR', 'values': []}


def dns_info(domain):
    a, aaaa = dns_query(domain, 'A'), dns_query(domain, 'AAAA')
    labels = domain.split('.')
    nameservers, zone = [], None
    # Never attribute TLD authority servers (e.g. rotld.ro) to a missing domain.
    for i in range(len(labels) - 1):
        candidate = '.'.join(labels[i:])
        answer = dns_query(candidate, 'NS')
        if answer['values']:
            nameservers, zone = answer['values'], candidate
            break
    return {'ipv4': a['values'], 'ipv6': aaaa['values'], 'nameservers': nameservers, 'ns_zone': zone,
            'status': 'NOERROR' if a['values'] or aaaa['values'] else ('NXDOMAIN' if a['status'] == aaaa['status'] == 'NXDOMAIN' else 'ERROR' if 'ERROR' in (a['status'], aaaa['status']) else 'NOERROR')}


def one_http(url, timeout=10):
    with tempfile.TemporaryDirectory(prefix='domain-http-') as tmp:
        headerfile = pathlib.Path(tmp) / 'headers'
        try:
            p = subprocess.run(['curl', '--silent', '--show-error', '--noproxy', '*', '--connect-timeout', '4',
                                '--max-time', str(timeout), '--proto', '=http,https', '--user-agent', UA,
                                '--output', os.devnull, '--dump-header', str(headerfile), '--write-out', '%{json}', url],
                               capture_output=True, text=True, timeout=timeout + 2)
            data = json.loads(p.stdout or '{}')
            status = data.get('http_code') or None
            headers = headerfile.read_text(errors='replace') if headerfile.exists() else ''
            locations = re.findall(r'^location:\s*(.+)', headers, re.I | re.M)
            return {'status': status, 'ip': data.get('remote_ip') or None,
                    'location': locations[-1].strip() if locations else None,
                    'cloudflare': bool(re.search(r'^(?:server:\s*cloudflare|cf-ray:)', headers, re.I | re.M)),
                    'error': None if status else {6: 'Domeniul nu se rezolvă în DNS.', 7: 'Conexiunea a fost refuzată.',
                                                 28: 'Timpul de răspuns a fost depășit.', 60: 'Certificatul TLS nu este valid.'}.get(p.returncode, 'Conexiunea HTTPS/HTTP nu a reușit.')}
        except (OSError, subprocess.TimeoutExpired, ValueError):
            return {'status': None, 'ip': None, 'location': None, 'cloudflare': False, 'error': 'Verificarea HTTP nu a putut fi finalizată.'}


def http_info(url):
    started = time.monotonic()
    result = {'responds': False, 'status': None, 'final_url': url, 'initial_ip': None, 'remote_ip': None,
              'cloudflare': False, 'error': None, 'redirects': [], 'checked_at': now()}
    visited = set()
    current = url
    for i in range(6):
        if current in visited or time.monotonic() - started > 25:
            result['error'] = 'Buclă de redirecționare sau limită de timp depășită.'
            break
        response = one_http(current, max(2, min(10, int(26 - (time.monotonic() - started)))))
        if i == 0 and not response['status'] and current.startswith('https://'):
            result['https_error'] = response['error']
            current = 'http://' + current[8:]
            response = one_http(current, 6)
        result['cloudflare'] |= response['cloudflare']
        if response['status']:
            visited.add(current)
            if current.startswith('https://'):
                result.pop('https_error', None)
            result['responds'] = True
            result['initial_ip'] = result['initial_ip'] or response['ip']
            result.update(status=response['status'], remote_ip=response['ip'], final_url=current)
            result['redirects'].append({'url': current, 'status': response['status'], 'ip': response['ip'], 'location': response['location']})
        else:
            result['error'] = response['error']
            result['final_url'] = current
            break
        if response['status'] in (301, 302, 303, 307, 308) and response['location']:
            target = urljoin(current, response['location'])
            parsed = urlsplit(target)
            if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password:
                result['error'] = 'Redirecționarea nu poate fi verificată.'
                break
            current = target
        else:
            break
    else:
        result['error'] = 'Prea multe redirecționări.'
    result['checked_at'] = now()
    return result


def docker_states():
    try:
        names = subprocess.check_output(['docker', 'ps', '-aq'], text=True, timeout=15).split()
        if not names:
            return {}, None
        rows = json.loads(subprocess.check_output(['docker', 'inspect', *names], text=True, timeout=20))
        return {r['Name'].lstrip('/'): {'name': r['Name'].lstrip('/'), 'state': r['State']['Status'],
                                      'health': r['State'].get('Health', {}).get('Status')}
                for r in rows}, None
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}, 'Docker nu a putut fi interogat; starea containerelor este necunoscută.'


def docker_info(row, states, docker_error, checks):
    expected = row.get('container_names', [])
    containers = [states.get(n, {'name': n, 'state': 'unknown' if docker_error else 'absent', 'health': None}) for n in expected]
    exists = any(c['state'] != 'absent' for c in containers) if not docker_error else None
    active = bool(containers) and all(c['state'] == 'running' for c in containers) if not docker_error else None
    links = []
    for link in row.get('docker_links', []):
        check = checks[link['url']]
        links.append({**link, 'status': check['status'], 'responds': check['responds'], 'error': check['error'],
                      'https_error': check.get('https_error'),
                      'remote_ip': check['remote_ip'], 'final_url': check['final_url'],
                      'active': all(states.get(n, {}).get('state') == 'running' for n in link['containers']) if not docker_error else None})
    return {'exists': exists, 'active': active, 'containers': containers, 'links': links,
            'note': 'Containere comune pentru mai multe adrese; accesul fiecărei copii este verificat separat.' if expected else 'Niciun container asociat acestei adrese nu a fost identificat în configurațiile verificate.'}


def cf_ranges():
    # Public Cloudflare address ranges, periodically maintained by the operator.
    # HTTP cf-ray is the primary runtime evidence; these cover DNS-only checks.
    return [ipaddress.ip_network(n) for n in ('173.245.48.0/20','103.21.244.0/22','103.22.200.0/22','103.31.4.0/22','141.101.64.0/18','108.162.192.0/18','190.93.240.0/20','188.114.96.0/20','197.234.240.0/22','198.41.128.0/17','162.158.0.0/15','104.16.0.0/13','104.24.0.0/14','172.64.0.0/13','131.0.72.0/22','2400:cb00::/32','2606:4700::/32','2803:f800::/32','2405:b500::/32','2405:8100::/32','2a06:98c0::/29','2c0f:f248::/32')]


def collect(registry, previous=None):
    states, docker_error = docker_states()
    urls = sorted({r['public_url'] for r in registry['domains']} | {l['url'] for r in registry['domains'] for l in r.get('docker_links', [])})
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_http = {u: executor.submit(http_info, u) for u in urls}
        future_dns = {r['domain']: executor.submit(dns_info, r['domain']) for r in registry['domains']}
        checks = {u: f.result() for u, f in future_http.items()}
        dns_checks = {d: f.result() for d, f in future_dns.items()}
    previous_domains = {r['domain'] for r in (previous or {}).get('domains', [])}
    verified_path = ROOT / 'migration_verified.json'
    verified = json.loads(verified_path.read_text()) if verified_path.exists() else {}
    domains = []
    networks = cf_ranges()
    for source in registry['domains']:
        row = {k: v for k, v in source.items() if k not in ('container_names', 'docker_links', 'route', 'candidate_cloudflare')}
        domain = row['domain']
        row['dns'], row['http'] = dns_checks[domain], checks[row['public_url']]
        ips = row['dns']['ipv4'] + row['dns']['ipv6']
        cf = row['http']['cloudflare'] or any(any(ipaddress.ip_address(ip) in n for n in networks) for ip in ips)
        if source.get('candidate_cloudflare') and not cf and domain not in previous_domains:
            continue
        row['http']['cloudflare'] = bool(cf)
        row['docker'] = docker_info(source, states, docker_error, checks)
        if domain in verified.get('domains', {}):
            row.setdefault('migration', {}).update(verified['domains'][domain])
        elif row.get('migration', {}).get('category') == 'local_app':
            row['migration']['verification'] = {
                'checked_at': now(), 'status': 'confirmed' if row['docker']['exists'] and cf else 'partial',
                'note': 'Adresa este configurată în rutarea locală. Containerele și răspunsul public sunt verificate în acest ciclu; categoria nu afirmă că este o clonă WordPress.',
                'products': None, 'published_products': None, 'paths': []}
        row['checked_at'] = now()
        domains.append(row)
    return {'schema_version': 1, 'generated_at': now(), 'refresh_seconds': 300, 'server_ip': registry['server_ip'],
            'docker_error': docker_error, 'reference': registry.get('reference', {}), 'domains': sorted(domains, key=lambda r: r['domain']),
            'monitor': {'checked_urls': len(urls), 'registry_domains': len(registry['domains']), 'dns_resolvers': ['1.1.1.1', '8.8.8.8']}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--registry', default=str(ROOT / 'registry.json'))
    parser.add_argument('--output', default=str(ROOT.parent / 'data/domain-monitor.json'))
    args = parser.parse_args()
    output = pathlib.Path(args.output)
    registry = json.loads(pathlib.Path(args.registry).read_text(encoding='utf-8-sig'))
    previous = json.loads(output.read_text()) if output.exists() else None
    snapshot = collect(registry, previous)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.domain-monitor-', suffix='.json', dir=str(output.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(temp, 0o644)
        os.replace(temp, output)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    print(json.dumps({'generated_at': snapshot['generated_at'], 'domains': len(snapshot['domains']), 'docker_error': snapshot['docker_error']}))


if __name__ == '__main__':
    main()
