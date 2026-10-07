import test from 'node:test';
import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { createApp } from '../server/http.mjs';
import { locales } from '../server/config.mjs';
import { publicRoutes, publicOrigin, pageUrl } from '../server/seo.mjs';

const origin = 'https://3dscan.eva-org.com';
const seeds = Object.fromEntries(await Promise.all(locales.map(async locale => [locale, JSON.parse(await readFile(new URL(`../content/locales/${locale}.json`, import.meta.url), 'utf8'))])));
class SeoStore extends EventEmitter {
  revisionValue = '10';
  down = false;
  variables = { product: 'EVA-3dScan', languages: 7, modules: 3, docsPages: 89 };
  overrides = {};
  async ready() { if (this.down) throw new Error('offline'); }
  async revision() { await this.ready(); return this.revisionValue; }
  async get(locale) {
    await this.ready();
    return { locale, revision: this.revisionValue, variables: this.variables, messages: {
      ...seeds[locale],
      'uses.title': `${locale} use cases`, 'uses.intro': `${locale} planned use cases for {{product}}`,
      'uses.metaTitle': `${locale} use cases · {{product}}`, 'uses.metaDescription': `${locale} find a use case for {{product}}`,
      'people.title': `${locale} people`, 'people.intro': `${locale} capture people only with consent`,
      'people.metaTitle': `${locale} people · {{product}}`, 'people.metaDescription': `${locale} people capture concept`,
      'people.consentTitle': `${locale} consent`, 'people.consentText': `${locale} ask for permission`,
      'nav.uses': `${locale} uses`, 'nav.people': `${locale} people`,
      'usecase.spare_part.title': `${locale} spare part`, 'usecase.spare_part.description': `${locale} inspect a prototype before further work`,
      'usecase.room_plan.title': `${locale} room plan`, 'usecase.room_plan.description': `${locale} plan the space with separate checks`,
      ...this.overrides,
    } };
  }
}

async function app(t) {
  const store = new SeoStore();
  const authStore = {
    async userForToken(token) { return token === 'valid' ? { id: 'user-1', email: 'test@example.test' } : null; },
    async login() { return { token: 'valid', user: { id: 'user-1' } }; },
    async logout() {},
  };
  const projectStore = { async list(userId) { assert.equal(userId, 'user-1'); return [{ client_id: 'one', name: 'Private project', revision: 1, updated_at: new Date(0) }]; } };
  const server = createApp({ store, authStore, projectStore, publicBaseUrl: origin });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(async () => { server.closeEvents(); server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); });
  return { store, base: `http://127.0.0.1:${server.address().port}` };
}

test('SEO: all nine public routes have localized SSR, canonical URLs, reciprocal alternatives and JSON-LD', async t => {
  const { base } = await app(t);
  for (const route of publicRoutes) for (const locale of locales) {
    const response = await fetch(`${base}${route}?lang=${locale}&tracking=ignored`);
    assert.equal(response.status, 200, `${route} ${locale}`);
    assert.equal(response.headers.get('content-language'), locale);
    const html = await response.text();
    assert.match(html, new RegExp(`<html lang="${locale}">`));
    assert.match(html, /<div id="app" data-ssr="true">/);
    assert.equal((html.match(/<h1>/g) || []).length, 1);
    assert.equal((html.match(/rel="canonical"/g) || []).length, 1);
    assert.ok(html.includes(`id="seo-canonical" rel="canonical" href="${pageUrl(origin, route, locale)}"`));
    const head = html.split('</head>')[0];
    assert.equal((head.match(/rel="alternate"/g) || []).length, 8);
    for (const language of locales) assert.ok(head.includes(`hreflang="${language}" href="${pageUrl(origin, route, language)}"`));
    assert.ok(head.includes(`hreflang="x-default" href="${pageUrl(origin, route, 'en')}"`));
    assert.ok(html.includes(`href="/documentation?lang=${locale}"`));
    assert.doesNotMatch(head, /tracking=|undefined|usecase\.[a-z_]+\.title/);
    const jsonText = /<script id="seo-jsonld" type="application\/ld\+json">([\s\S]*?)<\/script>/.exec(head)[1];
    const data = JSON.parse(jsonText);
    assert.equal(data['@type'], 'SoftwareApplication');
    assert.equal(data.inLanguage, locale);
    assert.equal(data.operatingSystem, 'iOS');
    assert.equal(data.creativeWorkStatus, seeds[locale]['status.development']);
    assert.equal(data.offers, undefined);
    assert.equal(data.aggregateRating, undefined);
    assert.equal(data.downloadUrl, undefined);
    assert.ok(response.headers.get('content-security-policy').includes(`'sha256-${createHash('sha256').update(jsonText).digest('base64')}'`));
    if (route === '/uses') {
      assert.ok(html.includes(`<h1>${locale} use cases</h1>`));
      assert.ok(html.includes(`${locale} inspect a prototype before further work`));
      assert.ok(html.includes(`href="/uses?lang=${locale}#usecase-spare_part"`));
      assert.doesNotMatch(html, /<noscript\b|<[^>]+\shidden(?:\s|=|>)/i);
    }
    if (route === '/people') assert.ok(html.includes(`${locale} ask for permission`));
  }
});

test('SEO: bundle edits invalidate HTML, conditional HEAD works, aliases are canonical, outages return 503', async t => {
  const { base, store } = await app(t);
  const first = await fetch(`${base}/uses?lang=ro`);
  const etag = first.headers.get('etag');
  assert.equal((await fetch(`${base}/uses?lang=ro`, { headers: { 'If-None-Match': etag } })).status, 304);
  assert.equal((await fetch(`${base}/uses?lang=ro`, { method: 'HEAD', headers: { 'If-None-Match': etag } })).status, 304);
  store.variables = { ...store.variables, product: 'Updated product', docsPages: 90 };
  const updated = await fetch(`${base}/uses?lang=ro`, { headers: { 'If-None-Match': etag } });
  assert.equal(updated.status, 200);
  assert.notEqual(updated.headers.get('etag'), etag);
  assert.match(await updated.text(), /ro use cases · Updated product/);
  const translated = await fetch(`${base}/uses?lang=de`, { headers: { 'If-None-Match': updated.headers.get('etag') } });
  assert.equal(translated.status, 200);
  const alias = await fetch(`${base}/people?lang=sp`);
  const spanish = await fetch(`${base}/people?lang=es`);
  assert.equal(alias.headers.get('etag'), spanish.headers.get('etag'));
  assert.match(await alias.text(), /people\?lang=es/);
  const head = await fetch(`${base}/uses?lang=ro`, { method: 'HEAD' });
  assert.equal(head.status, 200);
  assert.ok(Number(head.headers.get('content-length')) > 1000);
  assert.equal(await head.text(), '');
  store.down = true;
  const unavailable = await fetch(`${base}/uses?lang=ro`, { headers: { 'If-None-Match': updated.headers.get('etag') } });
  assert.equal(unavailable.status, 503);
  assert.equal(unavailable.headers.get('cache-control'), 'no-store');
  assert.equal(unavailable.headers.get('etag'), null);
});

test('SEO: edited text and language input cannot inject HTML or executable scripts', async t => {
  const { base, store } = await app(t);
  store.overrides = { 'uses.title': '</h1><script>alert(7)</script>', 'uses.metaDescription': '"><img src=x onerror=alert(8)>', 'status.development': '</script><script>alert(9)</script>' };
  const response = await fetch(`${base}/uses?lang=${encodeURIComponent('"><script>alert(1)</script>')}`);
  const html = await response.text();
  assert.match(html, /<html lang="en">/);
  assert.ok(html.includes('&lt;script&gt;alert(7)&lt;/script&gt;'));
  assert.doesNotMatch(html, /<script>alert|<img src=x/);
  const jsonText = /<script id="seo-jsonld" type="application\/ld\+json">([\s\S]*?)<\/script>/.exec(html)[1];
  assert.equal(JSON.parse(jsonText).creativeWorkStatus, store.overrides['status.development']);
  assert.match(jsonText, /\\u003c\/script>/);
  assert.throws(() => publicOrigin('javascript:alert(1)'));
  assert.throws(() => publicOrigin('https://user:password@example.com'));
  assert.throws(() => publicOrigin('https://example.com/extra/path'));
});

test('SEO discovery excludes private routes and preserves account/project API behavior', async t => {
  const { base } = await app(t);
  const response = await fetch(`${base}/sitemap.xml`);
  const xml = await response.text();
  const urls = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map(match => match[1]);
  assert.equal(urls.length, 63);
  assert.equal(new Set(urls).size, 63);
  for (const route of publicRoutes) for (const locale of locales) assert.ok(urls.includes(pageUrl(origin, route, locale)));
  assert.doesNotMatch(xml, /\/api\/|\/account|\/projects|\/login|\/register|lastmod/);
  assert.equal((await fetch(`${base}/sitemap.xml`, { headers: { 'If-None-Match': response.headers.get('etag') } })).status, 304);
  const text = await (await fetch(`${base}/robots.txt`)).text();
  assert.ok(text.includes('Sitemap: https://3dscan.eva-org.com/sitemap.xml'));
  assert.ok(text.includes('Disallow: /api/auth/'));
  assert.ok(text.includes('Disallow: /api/projects'));
  assert.doesNotMatch(text, /Disallow: \/api\/\s|Disallow: \/api\/content/);
  const anonymous = await fetch(`${base}/api/projects`);
  assert.equal(anonymous.status, 401);
  assert.equal(anonymous.headers.get('x-robots-tag'), 'noindex, nofollow');
  const projects = await fetch(`${base}/api/projects`, { headers: { Authorization: 'Bearer valid' } });
  assert.equal(projects.status, 200);
  assert.equal((await projects.json()).projects[0].name, 'Private project');
  assert.equal((await fetch(`${base}/api/auth/me`, { headers: { Authorization: 'Bearer valid' } })).status, 200);
  assert.equal((await fetch(`${base}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'test@example.test', password: 'test-only' }) })).status, 200);
  assert.equal((await fetch(`${base}/api/auth/logout`, { method: 'POST' })).status, 200);
});
