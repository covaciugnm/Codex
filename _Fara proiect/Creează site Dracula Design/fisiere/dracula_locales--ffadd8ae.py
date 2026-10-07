"""Enabled languages are tenant data; there is no closed language enum."""
import re
from flask import g, has_request_context
from sqlalchemy import text
from .config import get_settings
from .db import session_scope, set_session_context
from .repositories.tenant_repo import get_tenant_id

def valid_locale(code):
    return isinstance(code, str) and bool(re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*', code))

def enabled_locales():
    if has_request_context() and hasattr(g, 'dracula_locales'):
        return g.dracula_locales
    with session_scope() as session:
        tenant = get_tenant_id(session, get_settings().default_tenant)
        set_session_context(session, tenant_id=tenant)
        values = tuple(session.execute(text('SELECT locale FROM core.tenant_locales WHERE tenant_id=:t AND is_enabled ORDER BY position,locale'), {'t':tenant}).scalars())
    if has_request_context():
        g.dracula_locales = values
    return values

class LocaleRegistry:
    def __iter__(self):
        return iter(enabled_locales())
    def __contains__(self, value):
        return valid_locale(value)
    def __len__(self):
        return len(enabled_locales())

LOCALES = LocaleRegistry()
