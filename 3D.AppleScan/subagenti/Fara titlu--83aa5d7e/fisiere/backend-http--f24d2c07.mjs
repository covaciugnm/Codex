import test from 'node:test';
import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { mkdtemp, mkdir, writeFile, rm, utimes } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createApp } from '../server/http.mjs';
import { normalizeLocale, locales, variables } from '../server/config.mjs';
import { validateMessages } from '../scripts/shared.mjs';
import { parseVariableValue } from '../scripts/set-variable.mjs';
import { ContentStore } from '../server/content.mjs';

test('locale normalization and content validation', () => {
  for (const locale of locales) assert.equal(normalizeLocale(locale), locale);
  assert.equal(normalizeLocale('sp'), 'es');
  assert.equal(normalizeLocale('RO'), 'ro');
  assert.equal(normalizeLocale('xx'), 'en');
  assert.equal(normalizeLocale(null), 'en');
  assert.throws(() => validateMessages({ title: 42 }, 'ro'));
  assert.throws(() => validateMessages({}, 'en'));
  assert.deepEqual(validateMessages({ messages: { title: 'EVA' } }, 'en'), { title: 'EVA' });
  assert.equal(parseVariableValue('89'), 89);
  assert.equal(parseVariableValue('"EVA 3D Scan"'), 'EVA 3D Scan');
  assert.equal(parseVariableValue('false'), false);
  for (const raw of ['null', '[]', '{}', 'unquoted text', '1e999', JSON.stringify('a'.repeat(16385))]) assert.throws(() => parseVariableValue(raw));
});

test('database values cannot serialize nonfinite numbers or nonscalar variables into the API', async t => {
  const store = new ContentStore();
  t.after(() => store.close());
  for (const value of [Infinity, -Infinity, NaN, null, [], {}]) {
    store.pool.query = async () => ({ rows: [{ revision: '1', base_count: 1, messages: { title: 'EVA' }, variables: { invalid: value } }] });
    await assert.rejects(store.get('en'), /not a finite JSON scalar/);
  }
  store.pool.query = async () => ({ rows: [{ revision: '1', base_count: 1, messages: { title: 'EVA' }, variables: { maximum: Number.MAX_VALUE, minimum: -Number.MAX_VALUE } }] });
  const bundle = await store.get('en');
  assert.equal(bundle.variables.maximum, Number.MAX_VALUE);
  assert.equal(JSON.parse(JSON.stringify(bundle)).variables.minimum, -Number.MAX_VALUE);
});

test('HTTP contract: caching, aliases, private files, SPA routes, readiness, SSE', async t => {
  const directory = await mkdtemp(join(tmpdir(), 'eva-http-'));
  const publicDir = join(directory, 'public');
  await mkdir(publicDir);
  await writeFile(join(publicDir, 'index.html'), '<!doctype html><html lang="en"><head><title>EVA test fixture</title></head><body><!-- EVA test fixture --><div id="app"></div></body></html>');
  const asset = join(publicDir, 'app.js');
  await writeFile(asset, 'const value = 1;');
  await writeFile(join(directory, '.env'), 'PRIVATE_SENTINEL');
  await mkdir(join(directory, 'docs'));
  await writeFile(join(directory, 'docs', 'private.txt'), 'PRIVATE_SENTINEL');
  class FakeStore extends EventEmitter {
    down = false;
    variables = variables;
    async ready() { if (this.down) throw new Error('offline'); }
    async revision() { await this.ready(); return '9'; }
    async get(locale) { await this.ready(); return { locale, revision: '9', variables: this.variables, messages: { title: 'EVA' } }; }
  }
  const store = new FakeStore();
  const server = createApp({ store, publicDir });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(async () => {
    server.closeEvents();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
    await rm(directory, { recursive: true, force: true });
  });
  const base = `http://127.0.0.1:${server.address().port}`;
  for (const [input, expected] of [['ro','ro'], ['sp','es'], ['unknown','en']]) {
    const res = await fetch(`${base}/api/content?lang=${input}`);
    assert.equal(res.status, 200);
    assert.equal(res.headers.get('content-language'), expected);
    assert.equal((await res.json()).locale, expected);
    const cached = await fetch(`${base}/api/content?lang=${input}`, { headers: { 'If-None-Match': res.headers.get('etag') } });
    assert.equal(cached.status, 304);
    assert.equal(await cached.text(), '');
  }
  const beforeConfigChange = await fetch(`${base}/api/content?lang=en`);
  const beforeEtag = beforeConfigChange.headers.get('etag');
  store.variables = { ...variables, docsPages: 90 };
  const afterConfigChange = await fetch(`${base}/api/content?lang=en`, { headers: { 'If-None-Match': beforeEtag } });
  assert.equal(afterConfigChange.status, 200, 'changed variables invalidate ETag even with unchanged database revision');
  assert.notEqual(afterConfigChange.headers.get('etag'), beforeEtag);
  assert.equal((await afterConfigChange.json()).variables.docsPages, 90);
  store.variables = variables;
  for (const path of ['/', '/objects', '/measure', '/spaces', '/technology', '/documentation', '/about', '/objects/']) {
    const res = await fetch(`${base}${path}?lang=de`);
    assert.equal(res.status, 200, path);
    assert.match(await res.text(), /EVA test fixture/);
  }
  const assetResponse = await fetch(`${base}/app.js`);
  assert.equal(assetResponse.status, 200);
  const assetEtag = assetResponse.headers.get('etag');
  assert.ok(assetEtag);
  assert.equal(await assetResponse.text(), 'const value = 1;');
  const unchangedAsset = await fetch(`${base}/app.js`, { headers: { 'If-None-Match': assetEtag } });
  assert.equal(unchangedAsset.status, 304);
  assert.equal(await unchangedAsset.text(), '');
  const assetHead = await fetch(`${base}/app.js`, { method: 'HEAD' });
  assert.equal(assetHead.status, 200);
  assert.equal(assetHead.headers.get('content-length'), '16');
  assert.equal(assetHead.headers.get('etag'), assetEtag);
  assert.equal(await assetHead.text(), '');
  assert.equal((await fetch(`${base}/app.js`, { method: 'HEAD', headers: { 'If-None-Match': assetEtag } })).status, 304);
  await writeFile(asset, 'const value = 2;');
  // Ensure timestamp change on filesystems with coarse timestamps, keeping byte count fixed.
  await utimes(asset, new Date(), new Date(Date.now() + 2000));
  const changedAsset = await fetch(`${base}/app.js`, { headers: { 'If-None-Match': assetEtag } });
  assert.equal(changedAsset.status, 200);
  assert.notEqual(changedAsset.headers.get('etag'), assetEtag);
  assert.equal(await changedAsset.text(), 'const value = 2;');
  const htmlResponse = await fetch(`${base}/objects`);
  const htmlCached = await fetch(`${base}/objects`, { headers: { 'If-None-Match': htmlResponse.headers.get('etag') } });
  assert.equal(htmlCached.status, 304);
  for (const path of ['/.env', '/docs/private.txt', '/deploy/secret', '/server/config.mjs', '/content/locales/en.json', '/%2e%2e/.env', '/%5c..%5c.env']) {
    const res = await fetch(`${base}${path}`);
    assert.equal(res.status, 404, path);
    assert.doesNotMatch(await res.text(), /PRIVATE_SENTINEL/);
  }
  assert.equal((await fetch(`${base}/api/content`, { method: 'POST' })).status, 405);
  assert.equal((await fetch(`${base}/api/edit`)).status, 404);
  const abort = new AbortController();
  const events = await fetch(`${base}/api/events`, { signal: abort.signal });
  assert.equal(events.headers.get('content-type'), 'text/event-stream; charset=utf-8');
  const reader = events.body.getReader();
  assert.match(new TextDecoder().decode((await reader.read()).value), /event: content[\s\S]*"revision":"9"/);
  store.emit('content', { revision: '10' });
  assert.match(new TextDecoder().decode((await reader.read()).value), /"revision":"10"/);
  abort.abort();
  store.down = true;
  assert.equal((await fetch(`${base}/healthz`)).status, 200);
  assert.equal((await fetch(`${base}/readyz`)).status, 503);
  assert.equal((await fetch(`${base}/api/content`)).status, 503);
  assert.equal((await fetch(`${base}/api/events`)).status, 503);
});
