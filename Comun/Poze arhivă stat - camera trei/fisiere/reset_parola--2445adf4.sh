#!/bin/bash
# Reseteaza parola unui cont de pe ac-wohnart.at. Utilizare: bash reset_parola.sh email@exemplu.com
# Parola se cere interactiv (nu apare pe ecran si nu ramane in istoricul shell-ului).
set -e
[ -z "$1" ] && { echo "Utilizare: bash $0 email"; exit 1; }
cd ~/site-uri/schallergasse35
docker compose exec -e RESET_EMAIL="$1" app python -c '
import os, getpass
import psycopg
from backend.app import hash_password
email = os.environ["RESET_EMAIL"].strip().lower()
p1 = getpass.getpass("Parola noua: "); p2 = getpass.getpass("Repeta parola: ")
if p1 != p2: raise SystemExit("Parolele nu coincid.")
if len(p1) < 8: raise SystemExit("Minim 8 caractere.")
with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    n = conn.execute("UPDATE users SET password_hash = %s WHERE lower(email) = %s", (hash_password(p1), email)).rowcount
    conn.commit()
print("OK - parola schimbata pentru " + email if n else "Contul " + email + " nu exista.")
'
