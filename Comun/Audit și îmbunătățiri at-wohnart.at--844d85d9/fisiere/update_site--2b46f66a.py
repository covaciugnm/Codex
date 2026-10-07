import os, re, glob
from PIL import Image

os.chdir(r'\\192.168.100.151\site-uri\schallergasse35\public')
BASE = 'https://www.ac-wohnart.at'


def rw(path, fn):
    s = open(path, encoding='utf-8').read()
    n = fn(s)
    if n != s:
        open(path, 'w', encoding='utf-8', newline='\n').write(n)
        print('updated', path)


# ---------- 1. imagini: max 1600 px, JPEG q80 progresiv ----------
dims = {}
for f in glob.glob('images/*.jp*g'):
    im = Image.open(f)
    w, h = im.size
    if max(w, h) > 1600 or os.path.getsize(f) > 250_000:
        im = im.convert('RGB')
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(f, 'JPEG', quality=80, optimize=True, progressive=True)
        print('img', f, (w, h), '->', im.size, os.path.getsize(f))
    dims[os.path.basename(f)] = Image.open(f).size

# favicon din logo
logo = Image.open('images/logo-ac-wohnart.jpeg').convert('RGB')
logo.save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
logo.resize((180, 180), Image.LANCZOS).save('apple-touch-icon.png')

LEGAL_DE = ' &nbsp;&middot;&nbsp; <a href="/impressum">Impressum</a> &nbsp;&middot;&nbsp; <a href="/datenschutz">Datenschutz</a>'
LEGAL_EN = ' &nbsp;&middot;&nbsp; <a href="/imprint">Imprint</a> &nbsp;&middot;&nbsp; <a href="/privacy">Privacy</a>'

# pagini publice: (fisier, url propriu, url DE, url EN, indexabil)
PUBLIC = {
    'index.html': ('/', '/', '/en'),
    'index_en.html': ('/en', '/', '/en'),
    'projekte.html': ('/projekte', '/projekte', '/projects'),
    'projects_en.html': ('/projects', '/projekte', '/projects'),
    'portal.html': ('/portal', '/portal', '/portal-en'),
    'portal_en.html': ('/portal-en', '/portal', '/portal-en'),
}
TITLES_OG = {}


def common(path):
    def fn(s):
        en = 'lang="en"' in s[:200]
        # an infiintare corect: 03.12.2025
        s = s.replace('Est. MMXX<', 'Est. MMXXV<')
        # linkuri legale in footer (o singura data)
        if '/impressum"' not in s and '/imprint"' not in s:
            s = re.sub(r'(<footer>\s*<p>.*?)(</p>)', lambda m: m.group(1) + (LEGAL_EN if en else LEGAL_DE) + m.group(2),
                       s, count=1, flags=re.S)
        # meniu: link duplicat catre /
        s = re.sub(r'\n\s*<a href="/">(Startseite|Home)</a>', '', s)
        # imagini: dimensiuni + lazy (fara hero/logo)
        def img(m):
            tag = m.group(0)
            name = os.path.basename(m.group(1))
            if name in dims and 'width=' not in tag:
                w, h = dims[name]
                extra = f' width="{w}" height="{h}"'
                if 'logo-img' not in tag and 'hero' not in s[max(0, m.start() - 120):m.start()]:
                    extra += ' loading="lazy" decoding="async"'
                tag = tag[:-1] + extra + '>'
            return tag
        s = re.sub(r'<img [^>]*src="([^"]+)"[^>]*>', img, s)
        # head: canonical / hreflang / favicon / OG
        if path in PUBLIC and 'rel="canonical"' not in s:
            own, de, enu = PUBLIC[path]
            title = re.search(r'<title>(.*?)</title>', s).group(1)
            desc = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
            head = (f'<link rel="canonical" href="{BASE}{own}">\n'
                    f'<link rel="alternate" hreflang="de" href="{BASE}{de}">\n'
                    f'<link rel="alternate" hreflang="en" href="{BASE}{enu}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{BASE}{de}">\n'
                    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
                    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                    '<meta property="og:type" content="website">\n'
                    '<meta property="og:site_name" content="A&amp;C Wohnart Immobilien">\n'
                    f'<meta property="og:title" content="{title}">\n'
                    f'<meta property="og:description" content="{desc}">\n'
                    f'<meta property="og:url" content="{BASE}{own}">\n'
                    f'<meta property="og:image" content="{BASE}/images/fassade-schallergasse-35.jpg">\n'
                    f'<meta property="og:locale" content="{"en_GB" if en else "de_AT"}">\n')
            s = s.replace('<link href="fonts/fonts.css"', head + '<link href="fonts/fonts.css"', 1)
        elif path not in PUBLIC and 'rel="icon"' not in s:
            s = s.replace('<link href="fonts/fonts.css"', '<link rel="icon" href="/favicon.ico" sizes="any">\n<link href="fonts/fonts.css"', 1)
        s = s.replace('href="style.css"', 'href="style.css?v=2"')
        s = s.replace('/portal.js?v=11', '/portal.js?v=12')
        return s
    return fn


for f in glob.glob('*.html'):
    rw(f, common(f))

# ---------- texte portal: inregistrarea e dezactivata ----------
rw('index.html', lambda s: s.replace(
    'Melden Sie sich an oder legen Sie ein Konto an, um Dateien hochzuladen\n      und wieder herunterzuladen.',
    'Melden Sie sich mit den Zugangsdaten an, die Sie von uns erhalten haben.'))
rw('index_en.html', lambda s: s.replace(
    'Sign in or create an account to upload your files and download them again.',
    'Sign in with the access details you have received from us.'))
rw('portal.html', lambda s: s.replace('Melden Sie sich an oder legen Sie ein Konto an.',
                                      'Melden Sie sich mit den Zugangsdaten an, die Sie von uns erhalten haben.'))
rw('portal_en.html', lambda s: s.replace('Please sign in or create an account.',
                                         'Please sign in with the access details you have received from us.'))


# portalul: mutat dupa prezentarea firmei (inainte de contact)
def move_portal(s):
    m = re.search(r'\n  <!-- (DATEIPORTAL|FILE PORTAL) -->\n  <section id="portal">.*?</section>\n', s, re.S)
    if not m:
        return s
    block = m.group(0)
    s = s.replace(block, '\n', 1)
    anchor = re.search(r'\n  <section id="(kontakt|contact)" class="contact">', s)
    return s[:anchor.start()] + block + s[anchor.start():]


rw('index.html', move_portal)
rw('index_en.html', move_portal)


# ---------- portal.js ----------
def pj(s):
    s = s.replace("gate: 'Anmelden / Registrieren',", "gate: 'Anmelden',")
    s = s.replace("gate: 'Sign in / Register',", "gate: 'Sign in',")
    if 'tooMany' not in s:
        s = s.replace("netErr: 'Verbindungsfehler. Bitte erneut versuchen.',",
                      "netErr: 'Verbindungsfehler. Bitte erneut versuchen.',\n      tooMany: 'Zu viele Fehlversuche. Bitte in 15 Minuten erneut versuchen.',")
        s = s.replace("netErr: 'Connection error. Please try again.',",
                      "netErr: 'Connection error. Please try again.',\n      tooMany: 'Too many failed attempts. Please try again in 15 minutes.',")
        s = s.replace("msg(authMsg, err.message || T.netErr, true);",
                      "msg(authMsg, err.status === 429 ? T.tooMany : (err.message || T.netErr), true);")
    return s


rw('portal.js', pj)

# ---------- pagina proiecte: nota de unverbindlichkeit ----------
rw('projekte.html', lambda s: s if 'notice legal-note' in s else s.replace(
    'aller Wohnungen.</p>',
    'aller Wohnungen.</p>\n    <p class="notice legal-note">Alle Angaben zu Wohnungen, Flächen und Ausstattung sind unverbindlich und stellen kein Angebot dar. Visualisierungen und Pläne dienen der Veranschaulichung; Änderungen bleiben vorbehalten.</p>', 1))
rw('projects_en.html', lambda s: s if 'notice legal-note' in s else re.sub(
    r'(<p class="notice">.*?</p>)',
    r'\1\n    <p class="notice legal-note">All information on apartments, floor areas and fittings is non-binding and does not constitute an offer. Visualisations and plans are for illustration only; subject to change.</p>',
    s, count=1, flags=re.S))

# ---------- CSS pagini legale + 404 ----------
CSS = '''
/* width/height pe <img> doar pentru rezervarea spatiului (fara deformare) */
:where(img[height]) { height: auto; }

/* --- pagini legale (Impressum / Datenschutz) + 404 --- */
.legal section { max-width: 780px; margin: 0 auto; padding-bottom: 48px; }
.legal .legal-title { font-family: 'Cinzel', serif; font-weight: 400; font-size: 2rem; letter-spacing: 0.08em; color: #2c2a26; margin: 0.4rem 0 1.6rem; }
.legal h3 { font-family: 'Cinzel', serif; font-weight: 400; font-size: 1.05rem; letter-spacing: 0.06em; color: #8a7433; margin: 2rem 0 0.6rem; }
.legal p { font-size: 0.92rem; line-height: 1.75; color: #4a4741; margin-bottom: 0.8rem; }
.legal a { color: #8a7433; }
.legal .legal-stand { margin-top: 2rem; font-size: 0.8rem; color: #8a867e; }
.notice.legal-note { font-size: 0.78rem; color: #8a867e; }
'''
rw('style.css', lambda s: s if '.legal-title' in s else s + CSS)

# ---------- robots + sitemap ----------
open('robots.txt', 'w', newline='\n').write(
    'User-agent: *\nDisallow: /admin\nDisallow: /pages\nDisallow: /api/\nDisallow: /dl-eva-9f3k2/\n\n'
    f'Sitemap: {BASE}/sitemap.xml\n')
urls = [('/', '/', '/en'), ('/en', '/', '/en'), ('/projekte', '/projekte', '/projects'),
        ('/projects', '/projekte', '/projects'), ('/impressum', '/impressum', '/imprint'),
        ('/imprint', '/impressum', '/imprint'), ('/datenschutz', '/datenschutz', '/privacy'),
        ('/privacy', '/datenschutz', '/privacy')]
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for own, de, en in urls:
    xml.append(f'  <url><loc>{BASE}{own}</loc>'
               f'<xhtml:link rel="alternate" hreflang="de" href="{BASE}{de}"/>'
               f'<xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/></url>')
xml.append('</urlset>')
open('sitemap.xml', 'w', newline='\n').write('\n'.join(xml) + '\n')

# ---------- pagina 404 ----------
open('404.html', 'w', encoding='utf-8', newline='\n').write('''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Seite nicht gefunden &ndash; A&amp;C Wohnart Immobilien</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="any">
<link href="/fonts/fonts.css" rel="stylesheet">
<link href="/style.css?v=2" rel="stylesheet">
</head>
<body data-lang="de">
<header>
  <img class="logo-img" src="/images/logo-ac-wohnart.jpeg" alt="A&amp;C Wohnart Immobilien Wien" width="%d" height="%d">
  <p class="tagline">Immobilien &nbsp;&middot;&nbsp; Wien &nbsp;&middot;&nbsp; Est. MMXXV</p>
  <div class="divider"></div>
</header>
<div class="wrap legal" style="text-align:center">
  <section>
    <p class="kicker">Fehler 404 &middot; Error 404</p>
    <h1 class="legal-title">Seite nicht gefunden</h1>
    <p>Die gewünschte Seite existiert nicht oder wurde verschoben.<br>The page you requested does not exist.</p>
    <p><a class="btn" href="/">Zur Startseite</a> &nbsp; <a class="btn" href="/en">Home (EN)</a></p>
  </section>
</div>
<footer>
  <p>&copy; MMXXVI A&amp;C Wohnart Immobilien GmbH''' % dims['logo-ac-wohnart.jpeg'] + LEGAL_DE + '''</p>
</footer>
</body>
</html>
''')
print('done')
