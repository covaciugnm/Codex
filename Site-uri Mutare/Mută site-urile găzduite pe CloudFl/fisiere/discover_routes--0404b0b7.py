"""Read routing metadata only. Never export container environment or tunnel tokens."""
import json
import pathlib
import re
import subprocess
from urllib.parse import urlsplit

import yaml


def run(args):
    return subprocess.check_output(args, text=True, timeout=60)


def discover():
    ids = run(['docker', 'ps', '-aq']).split()
    containers = json.loads(run(['docker', 'inspect', *ids]))
    safe = {}
    for c in containers:
        name = c['Name'].lstrip('/')
        safe[name] = {
            'name': name, 'image': c['Config']['Image'],
            'state': c['State']['Status'],
            'networks': {k: v.get('Aliases') or [] for k, v in c['NetworkSettings']['Networks'].items()},
            'ports': c['NetworkSettings']['Ports'] or {},
        }

    def resolve(service, tunnel=None):
        parsed = urlsplit(service)
        host = parsed.hostname
        if not host:
            return []
        if host in safe:
            return [host]
        tunnel_networks = set(safe.get(tunnel, {}).get('networks', {}))
        matches = []
        for name, c in safe.items():
            if host in ('localhost', '127.0.0.1', '192.168.100.151'):
                if any(str(parsed.port) == p['HostPort'] for ports in c['ports'].values() for p in (ports or [])):
                    matches.append(name)
            for network, aliases in c['networks'].items():
                if host in aliases and (not tunnel_networks or network in tunnel_networks):
                    matches.append(name)
        if not matches and host.startswith(('eva-', 'spree-', 'stalwart')):
            return [host]  # Preserve configured-but-absent targets as inactive.
        return sorted(set(matches))

    services, routers = {}, []
    root = pathlib.Path('/home/saga-server/Documents/EvA-Contab/proxy/traefik/dynamic')
    for p in sorted(root.glob('*.y*ml')):
        data = yaml.safe_load(p.read_text()) or {}
        http = data.get('http') or {}
        services.update(http.get('services') or {})
        for name, router in (http.get('routers') or {}).items():
            if not isinstance(router, dict):
                continue
            for host in re.findall(r'Host\(`([^`]+)`\)', router.get('rule', '')):
                routers.append({'domain': host.lower(), 'service': router.get('service', ''),
                                'rule': router.get('rule', ''), 'source': str(p),
                                'priority': router.get('priority', 0)})
    routes = {}
    # Root routes take precedence over /admin or other path-only services.
    for r in sorted(routers, key=lambda r: ('Path' not in r['rule'], r['priority'])):
        service = services.get(r['service'].split('@')[0], {})
        urls = [s['url'] for s in service.get('loadBalancer', {}).get('servers', []) if 'url' in s]
        names = sorted({n for u in urls for n in resolve(u)})
        routes[r['domain']] = {'domain': r['domain'], 'containers': names, 'service_urls': urls,
                               'source': r['source'], 'publication': 'Rută Traefik; publicarea se verifică prin DNS/HTTP'}
    tunnels = []
    for name, c in safe.items():
        if 'cloudflared' not in c['image']:
            continue
        logs = subprocess.run(['docker', 'logs', '--tail', '25000', name], capture_output=True, text=True, timeout=30)
        ingress = None
        for line in reversed((logs.stdout + logs.stderr).splitlines()):
            if 'Updated to new configuration' not in line:
                continue
            m = re.search(r'config=("(?:[^"\\]|\\.)*")', line)
            if m:
                try:
                    ingress = json.loads(json.loads(m.group(1))).get('ingress', [])
                    break
                except (ValueError, TypeError):
                    continue
        # Locally configured tunnels, if present. Read only ingress, omit credentials.
        if ingress is None:
            raw = next(x for x in containers if x['Name'].lstrip('/') == name)
            for mount in raw.get('Mounts', []):
                p = pathlib.Path(mount['Source'])
                candidates = [p] if p.is_file() and p.suffix in ('.yml', '.yaml') else list(p.glob('config.y*ml')) if p.is_dir() else []
                for f in candidates:
                    try:
                        data = yaml.safe_load(f.read_text()) or {}
                        if 'ingress' in data:
                            ingress = data['ingress']
                    except (OSError, ValueError, yaml.YAMLError):
                        pass
        tunnels.append({'name': name, 'configuration_found': ingress is not None})
        if ingress is None:
            # Only the most recent Quick Tunnel URL, never historical URLs.
            latest = re.findall(r'https://([a-z0-9-]+\.trycloudflare\.com)', logs.stdout + logs.stderr)
            raw = next(x for x in containers if x['Name'].lstrip('/') == name)
            command = raw['Config'].get('Cmd') or []
            upstream = next((command[i + 1] for i, arg in enumerate(command[:-1]) if arg == '--url'), None)
            if latest and upstream:
                routes[latest[-1]] = {'domain': latest[-1], 'containers': resolve(upstream, name),
                                      'service_urls': [upstream], 'source': 'Quick Tunnel ' + name,
                                      'publication': 'Cloudflare Quick Tunnel (adresă temporară)', 'tunnel': name,
                                      'note': 'Tunel local ' + name + '; destinația configurată: ' + upstream}
        for item in ingress or []:
            host, service = item.get('hostname'), item.get('service', '')
            if not host or '*' in host or not re.fullmatch(r'[a-zA-Z0-9.-]+', host):
                continue
            names = resolve(service, name)
            if any('traefik' in n for n in names) and host in routes:
                if routes[host].get('publication') != 'Cloudflare Tunnel':
                    routes[host]['tunnel'] = name
                    routes[host]['publication'] = 'Cloudflare Tunnel + Traefik'
            else:
                routes[host] = {'domain': host, 'containers': names, 'service_urls': [service],
                                'source': 'Configurație ingress ' + name, 'tunnel': name,
                                'publication': 'Cloudflare Tunnel'}
    return {'routes': sorted(routes.values(), key=lambda x: x['domain']), 'tunnels': tunnels}


if __name__ == '__main__':
    print(json.dumps(discover(), ensure_ascii=False, indent=2))
