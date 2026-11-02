"""Combine the user's hosting inventory, supplied map and observed routing."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
WP = 'https://wordpress.alba-vision.ro/'
ACCOUNTS = {
    'cesiro.ro': '''alba-vision.ro black-robot.ro cesiro.ro cesiro.ro.91-188-227-120.cpanel.site
innovation.cesiro.ro innovationecosystem.red-robot.ro jinko.ro nova-robotics.ro old.cesiro.ro
production.cesiro.ro red-robot.ro red.red-robot.ro sales.cesiro.ro wild-motion.ro'''.split(),
    'cesiro.com': '''ac-wohnart.at andowl.ro bonna.ro calphalon.ro cesiro.com democratia-adevarata.ro
doi.cesiro.ro fisher-price.ro ghirardelli.ro go-pro.ro hairmaster.ro kivicare.cesiro.com leapfrog.ro
melissaanddoug.ro model2.bonna.ro ninjakitchen.ro opticosmetics.ro pluginuri.fisher-price.ro
set-farfurii.ro set-vesela.ro tartecosmetics.ro'''.split(),
}
SLUGS = dict(zip('cesiro.ro old.cesiro.ro bonna.ro calphalon.ro fisher-price.ro ghirardelli.ro go-pro.ro leapfrog.ro melissaanddoug.ro ninjakitchen.ro opticosmetics.ro set-farfurii.ro tartecosmetics.ro'.split(),
                'cesiro old-cesiro bonna calphalon fisher-price ghirardelli go-pro leapfrog melissa-doug ninja-kitchen opticosmetics set-farfurii tarte-cosmetics'.split()))


def main():
    reference = json.loads((ROOT / 'reference.json').read_text(encoding='utf-8-sig'))
    routes = {r['domain']: r for r in json.loads((ROOT / 'routes.json').read_text(encoding='utf-8-sig'))['routes']}
    registry = {}
    for account, domains in ACCOUNTS.items():
        for domain in domains:
            registry[domain] = {'domain': domain, 'hosting_account': account,
                                'document_root': '/public_html' if domain in ('cesiro.ro', 'cesiro.com', 'cesiro.ro.91-188-227-120.cpanel.site') else '/' + domain}
    for domain, migration in reference['domains'].items():
        registry.setdefault(domain, {'domain': domain, 'hosting_account': migration['hosting_account'], 'document_root': None})
        registry[domain]['migration'] = migration
    for domain, route in routes.items():
        # Only names in known owned zones or explicit tunnel configurations.
        # Bare example Host rules (3d.ro, market.ro, production.ro) are not ownership proof.
        if domain not in registry and not (domain.endswith(('.eva-contab.ro', '.eva-org.com')) or route.get('tunnel') or route.get('publication') == 'Cloudflare Tunnel'):
            continue
        registry.setdefault(domain, {'domain': domain, 'hosting_account': 'În afara listelor Hosterion', 'document_root': None,
                                      'candidate_cloudflare': not bool(route.get('tunnel')),
                                      'migration': {'category': 'local_app', 'source': 'Configurația locală', 'source_date': '2026-10-21',
                                                    'notes': ['Adresă suplimentară identificată în configurația de publicare. Nu este atribuită unui cont Hosterion din listele primite.'],
                                                    'paths': [], 'admin_urls': [], 'products': None}})
        registry[domain]['route'] = route
    for domain, row in registry.items():
        links = []
        if domain in SLUGS:
            links.append({'label': 'Copie locală WordPress / motor comun', 'url': WP + SLUGS[domain] + '/',
                          'containers': ['wpsites-admin-1', 'wpsites-backend-1']})
        for url in row.get('migration', {}).get('copy_urls', []):
            if any(x['url'].rstrip('/') == url.rstrip('/') for x in links):
                continue
            route = routes.get(urlsplit(url).hostname, {})
            if route:
                links.append({'label': 'Copie / aplicație locală', 'url': url.rstrip('/') + '/', 'containers': route['containers']})
        route = row.get('route')
        if route and not any(x['url'].rstrip('/') == ('https://' + domain) for x in links):
            links.append({'label': 'Acces prin Cloudflare', 'url': 'https://' + domain + '/', 'containers': route['containers']})
        if domain == 'cesiro.com':
            for link in links:
                if urlsplit(link['url']).hostname == domain:
                    link['containers'] = ['cesiro1-admin-1', 'cesiro1-backend-1']
            row.setdefault('notes', []).append('Ruta publică a fost confirmată prin resursele paginii: motorul cesiro1 (:4121). Există și o regulă Traefik mai veche către storefront (:4020).')
        if domain == 'cesiro.ro.91-188-227-120.cpanel.site':
            row['migration'] = {'category': 'alias', 'source': 'Lista Hosterion furnizată', 'source_date': '2026-10-21',
                                'notes': ['Alias cPanel pentru cesiro.ro, cu aceeași rădăcină /public_html; nu este o clonă separată.'], 'paths': [], 'admin_urls': []}
            links.append({'label': 'Copia domeniului cesiro.ro (alias)', 'url': WP + 'cesiro/', 'containers': ['wpsites-admin-1', 'wpsites-backend-1']})
        row['docker_links'] = links
        row['container_names'] = sorted({c for link in links for c in link['containers']})
        row['public_url'] = 'https://' + domain + '/'
        row['historical_redirect'] = 'https://cesiro.ro/' if domain == 'cesiro.com' else None
        row.setdefault('notes', [])
        if row.get('route'):
            row['notes'].append(row['route']['publication'])
            if row['route'].get('note'):
                row['notes'].append(row['route']['note'])
    out = {'server_ip': '192.168.100.151', 'refresh_seconds': 300,
           'reference': {k: v for k, v in reference.items() if k != 'domains'},
           'domains': sorted(registry.values(), key=lambda x: x['domain'])}
    (ROOT / 'registry.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Registry: {len(out["domains"])} addresses; {sum(r["hosting_account"] != "În afara listelor Hosterion" for r in out["domains"])} from user lists/map.')


if __name__ == '__main__':
    main()
