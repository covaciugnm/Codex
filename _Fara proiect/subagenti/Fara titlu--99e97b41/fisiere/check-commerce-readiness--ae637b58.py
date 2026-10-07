#!/usr/bin/env python3
"""Run inside backend: python - < ops/check-commerce-readiness.py.

Exit 0 means merchant data is complete; exit 2 means incomplete. Does not
activate commerce, send email, charge cards, or display credential values.
"""
import json
import os
import sys
from pathlib import Path

if Path('/app/app').is_dir():
    sys.path.insert(0, '/app')
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from app.db import session_scope, set_session_context
from app.repositories.tenant_repo import get_tenant_id
from app.commerce_readiness import database_readiness


def main():
    with session_scope(role='admin') as session:
        tid = get_tenant_id(session, os.environ['DEFAULT_TENANT'])
        if not tid:
            print(json.dumps({'ready': False, 'error': 'tenant_not_found'}))
            return 2
        set_session_context(session, tenant_id=tid, admin='on')
        result = database_readiness(session, tid)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
