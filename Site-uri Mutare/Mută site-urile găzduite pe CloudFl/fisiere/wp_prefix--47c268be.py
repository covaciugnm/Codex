"""Tenantul din PREFIXUL DE CALE (https://<host>/<slug>/...), pentru găzduirea mai multor magazine
pe un singur domeniu (site-urile WordPress: https://wordpress.alba-vision.ro/bonna/, /calphalon/, ...).

Adăugat în `_motor` (stack-ul `wpsites`); NU face parte din codul cesiro1. Activ DOAR dacă
`WP_PATH_TENANTS` (slug-uri separate prin virgulă) e setat; altfel `install()` nu face nimic.

Cum funcționează
  1. Middleware WSGI: dacă prima componentă a căii e unul din slug-uri, o scoate din PATH_INFO
     și face cererea să pară venită de pe `<slug>.local` (domeniu mapat în `core.tenant_domains`),
     deci tot restul motorului (tenant, tema, catalogul, coșul) rămâne neschimbat.
     `/<slug>` fără slash final → 301 la `/<slug>/`.
  2. `after_request`: pe răspunsurile text (HTML, CSS, JS, JSON, XML) prefixează TOATE căile
     interne de rădăcină (/p/, /static/, /media/, /api/, /checkout, /account, ... — lista vine din
     `app.url_map`, deci urmărește rutele motorului), URL-urile absolute ale `PUBLIC_BASE_URL`
     (canonical, hreflang, sitemap, OG), antetul `Location` și `Path=` din `Set-Cookie`
     (cookie-urile de coș/temă/cont rămân separate pe magazin).
  3. `/` pe gazdele din `WP_INDEX_HOSTS` (fără `?tenant=`) = pagina-index cu toate magazinele.

Variabile: WP_PATH_TENANTS, WP_INDEX_HOSTS (implicit: gazda din PUBLIC_BASE_URL, 127.0.0.1, localhost).
"""
from __future__ import annotations

import html
import os
import re
from urllib.parse import urlparse

from flask import Response, request

_TEXT_TYPES = {
    "text/html", "text/css", "text/javascript", "application/javascript", "application/json",
    "application/xml", "text/xml", "application/rss+xml", "text/plain", "application/ld+json",
}


def _public_base() -> str:
    base = (os.environ.get("PUBLIC_BASE_URL") or "").strip().rstrip("/")
    if base and "//" not in base:
        base = f"https://{base}"
    return base


def _host_only(host: str) -> str:
    return (host or "").split(",")[0].strip().lower().split(":")[0]


class _Segments:
    """Primele segmente statice de rută ale motorului (calculate leneș, după ce rutele există)."""

    def __init__(self, app):
        self.app = app
        self._re = None

    def regex(self):
        if self._re is None:
            segs = set()
            for rule in self.app.url_map.iter_rules():
                first = rule.rule.lstrip("/").split("/", 1)[0]
                if first and not first.startswith("<") and first != "admin":
                    segs.add(first)
            alt = "|".join(re.escape(s) for s in sorted(segs, key=len, reverse=True))
            end = r"""(?:[/?#"'`)\\<>\s]|$)"""
            self._re = (
                re.compile(rf"""(?<=["'`(])/(?=(?:{alt}){end})"""),
                re.compile(rf"""(?<=[\s,])/(?=(?:{alt}){end})"""),
            )
        return self._re


def rewrite_text(text: str, prefix: str, base: str, segs: _Segments, is_html: bool) -> str:
    quoted, spaced = segs.regex()
    text = quoted.sub(prefix + "/", text)
    if is_html:
        text = re.sub(r"""((?:href|action|formaction)=["'])/(?=["'#?])""", rf"\1{prefix}/", text)

        def _srcset(m):
            parts = []
            for tok in m.group(2).split(","):
                t = tok.strip()
                if t.startswith("/") and not t.startswith("//"):
                    t = prefix + t
                parts.append(t)
            return m.group(1) + ", ".join(parts) + m.group(3)

        text = re.sub(r'(srcset=")([^"]*)(")', _srcset, text)
    if base:
        slug = prefix.strip("/")
        text = re.sub(re.escape(base) + rf"""/(?!{re.escape(slug)}(?:[/"'<>\s?#]|$))""", f"{base}{prefix}/", text)
        text = re.sub(re.escape(base) + r"""(?=["'<>\s])""", f"{base}{prefix}/", text)
    return text


def _fix_location(loc: str, prefix: str, base: str, segs: _Segments) -> str:
    if base and loc.startswith(base):
        rest = loc[len(base):]
        if not rest.startswith(prefix + "/") and rest != prefix:
            return base + prefix + (rest if rest.startswith("/") else "/" + rest)
        return loc
    if loc.startswith("/") and not loc.startswith("//") and not loc.startswith(prefix + "/"):
        quoted, _ = segs.regex()
        probe = f'"{loc}"'
        if quoted.search(probe) or loc == "/" or loc[1:2] in ("?", "#"):
            return prefix + loc
    return loc


_INDEX_CSS = (
    "body{font-family:system-ui,sans-serif;margin:0;background:#f6f6f4;color:#1c1c1c}"
    "main{max-width:880px;margin:0 auto;padding:40px 16px}h1{font-size:1.6rem;margin:0 0 24px}"
    "ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}"
    "a{display:block;padding:16px;border:1px solid #d8d8d2;border-radius:8px;background:#fff;color:inherit;text-decoration:none}"
    "a:hover{border-color:#555}small{display:block;color:#666;margin-top:4px}"
)


def _index_html(slugs: list[str]) -> str:
    names: dict[str, str] = {}
    try:
        from sqlalchemy import text

        from .db import session_scope

        with session_scope() as session:
            for row in session.execute(text("SELECT slug, display_name FROM core.tenants WHERE status = 'active'")):
                names[row.slug] = row.display_name or row.slug
    except Exception:                                        # noqa: BLE001 - indexul merge și fără nume
        pass
    items = "".join(
        f'<li><a href="/{html.escape(s)}/">{html.escape(names.get(s, s))}<small>/{html.escape(s)}/</small></a></li>'
        for s in sorted(slugs)
    )
    return (
        '<!doctype html><html lang="ro"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Site-uri WordPress</title><style>{_INDEX_CSS}</style></head>"
        f"<body><main><h1>Site-uri WordPress</h1><ul>{items}</ul></main></body></html>"
    )


class _PathTenantMiddleware:
    def __init__(self, wsgi_app, slugs: list[str], index_hosts: set[str]):
        self.wsgi_app = wsgi_app
        self.slugs = set(slugs)
        self.index_hosts = index_hosts

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "") or "/"
        seg = path.lstrip("/").split("/", 1)[0]
        method = environ.get("REQUEST_METHOD", "GET")
        if seg in self.slugs:
            if path.rstrip("/") == "/" + seg and path == "/" + seg:
                qs = environ.get("QUERY_STRING", "")
                resp = Response(status=301, headers={"Location": f"/{seg}/" + (f"?{qs}" if qs else "")})
                return resp(environ, start_response)
            environ["PATH_INFO"] = path[len(seg) + 1:] or "/"
            environ["wp.prefix"] = "/" + seg
            environ["HTTP_HOST"] = f"{seg}.local"
            environ.pop("HTTP_X_FORWARDED_HOST", None)
            prefix = "/" + seg

            def _sr(status, headers, exc_info=None):
                # aici (nu în after_request) ca să prindă și cookie-urile puse de alte after_request (ex. CSRF)
                headers = [(k, re.sub(r"(?i);\s*Path=/(?=;|$)", f"; Path={prefix}/", v) if k.lower() == "set-cookie" else v)
                           for k, v in headers]
                return start_response(status, headers, exc_info)

            return self.wsgi_app(environ, _sr)
        elif (path in ("/", "/_domain-status.json", "/_domain-previews.json") or path.startswith("/_domain-preview/")) and method in ("GET", "HEAD") and "tenant=" not in environ.get("QUERY_STRING", ""):
            host = _host_only(environ.get("HTTP_X_FORWARDED_HOST") or environ.get("HTTP_HOST", ""))
            if host in self.index_hosts:
                from .domain_dashboard import dashboard_response

                resp = dashboard_response(path)
                return resp(environ, start_response)
        return self.wsgi_app(environ, start_response)


def install(app) -> None:
    slugs = [s.strip() for s in os.environ.get("WP_PATH_TENANTS", "").split(",") if s.strip()]
    if not slugs:
        return
    base = _public_base()
    index_hosts = {_host_only(h) for h in os.environ.get("WP_INDEX_HOSTS", "").split(",") if h.strip()}
    index_hosts |= {_host_only(urlparse(base).netloc)} if base else set()
    index_hosts |= {"127.0.0.1", "localhost"}
    index_hosts.discard("")
    app.wsgi_app = _PathTenantMiddleware(app.wsgi_app, slugs, index_hosts)
    segs = _Segments(app)

    @app.after_request
    def _prefix_response(resp):
        prefix = request.environ.get("wp.prefix")
        if not prefix:
            return resp
        loc = resp.headers.get("Location")
        if loc:
            resp.headers["Location"] = _fix_location(loc, prefix, base, segs)
        mime = (resp.mimetype or "").lower()
        if mime in _TEXT_TYPES and resp.status_code not in (204, 304):
            resp.direct_passthrough = False
            body = resp.get_data(as_text=True)
            if body:
                resp.set_data(rewrite_text(body, prefix, base, segs, mime == "text/html"))
        return resp
