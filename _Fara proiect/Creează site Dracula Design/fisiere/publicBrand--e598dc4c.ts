/**
 * Numele magazinului înainte de login (ecranul de autentificare nu poate citi `/settings`).
 *
 * Backend-ul nu expune încă o rută publică de tipul `GET /api/public/brand`. Sursa publică
 * existentă e antetul storefront-ului de pe aceeași gazdă: `<meta property="og:site_name">`
 * (și `<link rel="icon">`). Citim fluxul doar până la `</head>` și oprim descărcarea.
 * Rezerva finală: numele gazdei fără `www.`. Rezultatul se ține în `sessionStorage`.
 */
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

export interface PublicBrand {
  name: string;
  favicon: string | null;
  source: 'storefront' | 'hostname';
}

const CACHE_KEY = 'admin.public-brand';

export function hostnameBrand(): string {
  return (window.location.hostname || '').replace(/^www\./i, '');
}

function readCache(): PublicBrand | null {
  try {
    const raw = sessionStorage.getItem(CACHE_KEY);
    return raw ? (JSON.parse(raw) as PublicBrand) : null;
  } catch {
    return null;
  }
}

function writeCache(brand: PublicBrand): void {
  try {
    sessionStorage.setItem(CACHE_KEY, JSON.stringify(brand));
  } catch {
    /* storage indisponibil */
  }
}

function decode(text: string): string {
  const el = document.createElement('textarea');
  el.innerHTML = text;
  return el.value.trim();
}

/** Extrage numele și favicon-ul din `<head>`-ul storefront-ului. */
export function parseHead(head: string): { name: string | null; favicon: string | null } {
  const meta = (attr: string, value: string) => {
    const re = new RegExp(`<meta[^>]+${attr}=["']${value}["'][^>]*>`, 'i');
    const tag = head.match(re)?.[0];
    const content = tag?.match(/content=["']([^"']*)["']/i)?.[1];
    return content ? decode(content) : null;
  };
  const name = meta('property', 'og:site_name') || meta('name', 'application-name');
  const icon = head.match(/<link[^>]+rel=["'](?:shortcut )?icon["'][^>]*>/i)?.[0];
  const favicon = icon?.match(/href=["']([^"']+)["']/i)?.[1] ?? null;
  return { name, favicon };
}

async function fetchHead(): Promise<string> {
  const res = await fetch('/', { credentials: 'omit', headers: { Accept: 'text/html' } });
  if (!res.ok && res.status !== 404) throw new Error(String(res.status));
  if (!res.body) return (await res.text()).split(/<\/head>/i)[0];
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let html = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    html += decoder.decode(value, { stream: true });
    const end = html.search(/<\/head>/i);
    if (end >= 0 || html.length > 200_000) {
      void reader.cancel();
      return end >= 0 ? html.slice(0, end) : html;
    }
  }
  return html;
}

export async function loadPublicBrand(): Promise<PublicBrand> {
  const cached = readCache();
  if (cached) return cached;
  let brand: PublicBrand = { name: hostnameBrand(), favicon: null, source: 'hostname' };
  try {
    const response = await fetch('/api/public/brand');
    if (response.ok) {
      const data = await response.json();
      if (data.name) {
        brand = { name: data.name, favicon: data.logo_url || data.favicon_url || null, source: 'storefront' };
        writeCache(brand);
        return brand;
      }
    }
    const { name, favicon } = parseHead(await fetchHead());
    if (name) brand = { name, favicon, source: 'storefront' };
  } catch {
    /* storefront indisponibil — rămâne numele gazdei */
  }
  writeCache(brand);
  return brand;
}

/** Numele public al magazinului; inițial numele gazdei, apoi cel din storefront. */
export function usePublicBrand(): PublicBrand {
  const [brand, setBrand] = useState<PublicBrand>(() => readCache() ?? { name: hostnameBrand(), favicon: null, source: 'hostname' });
  useEffect(() => {
    let alive = true;
    void loadPublicBrand().then((b) => { if (alive) setBrand(b); });
    return () => { alive = false; };
  }, []);
  return brand;
}

/** Titlul ferestrei: „<magazin> · <Administrare magazin>” (fără nume scris în `index.html`). */
export function useDocumentTitle(storeName: string | undefined): void {
  const { t } = useTranslation();
  useEffect(() => {
    const suffix = t('app.title');
    document.title = storeName ? `${storeName} · ${suffix}` : suffix;
  }, [storeName, t]);
}
