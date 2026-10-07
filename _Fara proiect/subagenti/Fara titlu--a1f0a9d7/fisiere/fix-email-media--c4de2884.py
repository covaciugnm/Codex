from pathlib import Path
for root in [Path('outputs/dracula-design-office'),Path('outputs/dracula-food')]:
 p=root/'backend/app/mail/sender.py';s=p.read_text(encoding='utf-8')
 s=s.replace('MAX_SOURCE_BYTES = 2 * 1024 * 1024','MAX_SOURCE_BYTES = 12 * 1024 * 1024')
 needle='    path = urlparse(url).path if "://" in url else url\n'
 replacement='''    parsed = urlparse(url)
    public = urlparse(os.environ.get("PUBLIC_BASE_URL", ""))
    if parsed.netloc and parsed.netloc != public.netloc:
        return None
    path = parsed.path
    if path.startswith("/assets/"):
        from pathlib import Path
        root = Path(__file__).resolve().parents[2] / "public" / "assets"
        candidate = (root / unquote(path[len("/assets/"):])).resolve()
        if root.resolve() in candidate.parents and candidate.is_file():
            return str(candidate)
        return None
'''
 s=s.replace(needle,replacement).replace('or "https://cesiro.com"','or "http://127.0.0.1"').replace('"cesiro-mailer/1.0"','"dracula-mailer/1.0"')
 p.write_text(s,encoding='utf-8')
 p=root/'backend/app/mail/render.py';s=p.read_text(encoding='utf-8')
 s=s.replace('def _account_url(base_url: str) -> str:', 'def _account_url(base_url: str, locale: str = "ro") -> str:').replace('return f"{_base(base_url)}/ro/account"','return f"{_base(base_url)}/{quote(locale)}/account"')
 s=s.replace('def _order_url(base_url: str, number: str) -> str:','def _order_url(base_url: str, number: str, locale: str = "ro") -> str:').replace('return _account_url(base_url)','return _account_url(base_url, locale)')
 s=s.replace('_order_url(base_url, number)','_order_url(base_url, number, locale)').replace('account_url = _account_url(base_url)','account_url = _account_url(base_url, locale)')
 s=s.replace('    import os\n\n    from .. import cms','''    image = str(item.get("image_url") or item.get("image") or "")
    if image.startswith("/assets/"):
        return _abs_url(base_url, image)
    import os

    from .. import cms''')
 s=s.replace('link = f"{_base(base_url)}/p/{quote(slug)}" if slug else ""','external_id = str(item.get("external_id") or "")\n        link = f"{_base(base_url)}/{quote(locale)}/product/{quote(external_id)}" if external_id else f"{_base(base_url)}/{quote(locale)}/collection"')
 p.write_text(s,encoding='utf-8')
print('Local email images and locale links corrected.')
