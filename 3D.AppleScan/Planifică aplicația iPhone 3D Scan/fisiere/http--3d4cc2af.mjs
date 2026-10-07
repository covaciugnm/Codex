import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { readFile, realpath, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { normalizeLocale } from './config.mjs';
import { validEmail, validPassword, normalizeEmail } from './auth.mjs';
import { publicRoutes, publicOrigin, renderSeo, robots, sitemap } from './seo.mjs';

const defaultPublic = fileURLToPath(new URL('../public/', import.meta.url));
const routes = new Set(publicRoutes);
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml; charset=utf-8', '.pdf': 'application/pdf' };
function json(res, status, body, headers = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers });
  res.end(JSON.stringify(body));
}
function etagMatches(header, etag) {
  const value = etag.replace(/^W\//, '');
  return header?.split(',').some(candidate => candidate.trim() === '*' || candidate.trim().replace(/^W\//, '') === value);
}
function baseUrl() { return process.env.PUBLIC_BASE_URL || 'https://3dscan.eva-org.com'; }
function bearer(req) { const m = /^Bearer\s+(.+)$/i.exec(req.headers['authorization'] || ''); return m ? m[1] : null; }
async function readJson(req, limit = 1_000_000) {
  const chunks = []; let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > limit) { const e = new Error('too_large'); e.code = 'TOO_LARGE'; throw e; }
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}
function verifyPage(ok) {
  const title = ok ? 'Cont confirmat' : 'Link invalid sau expirat';
  const body = ok
    ? 'Adresa ta de email a fost confirmată. Te poți autentifica acum în aplicația EVA 3D Scan.'
    : 'Linkul de confirmare este invalid sau a expirat. Cere un link nou din aplicație.';
  return `<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title></head><body><main><h1>${title}</h1><p>${body}</p><p><a href="/">Înapoi la 3dscan.eva-org.com</a></p></main></body></html>`;
}
// Trimiterea efectivă a emailului necesită credențiale SMTP (server Stalwart).
// Până la configurarea lor, linkul de verificare este consemnat în jurnal.
async function sendVerificationEmail(email, verifyUrl) {
  console.log(JSON.stringify({ event: 'auth_verification_link', email, verifyUrl }));
}
async function handleAuth(req, res, url, auth) {
  const path = url.pathname;
  try {
    if (path === '/api/auth/register' && req.method === 'POST') {
      let body; try { body = await readJson(req); } catch (e) { return json(res, e.code === 'TOO_LARGE' ? 413 : 400, { error: 'invalid_body' }); }
      if (!validEmail(body.email)) return json(res, 400, { error: 'invalid_email' });
      if (!validPassword(body.password)) return json(res, 400, { error: 'invalid_password' });
      try {
        const { verificationToken } = await auth.register(body.email, body.password);
        const verifyUrl = `${baseUrl()}/api/auth/verify?token=${verificationToken}`;
        await sendVerificationEmail(normalizeEmail(body.email), verifyUrl);
        const payload = { status: 'verification_required' };
        if (process.env.AUTH_EXPOSE_VERIFY === '1') payload.verifyUrl = verifyUrl;
        return json(res, 201, payload);
      } catch (e) {
        if (e.code === 'EMAIL_TAKEN') return json(res, 409, { error: 'email_taken' });
        throw e;
      }
    }
    if (path === '/api/auth/verify' && (req.method === 'GET' || req.method === 'POST')) {
      const user = await auth.verify(url.searchParams.get('token'));
      if (req.method === 'GET') {
        res.writeHead(user ? 200 : 400, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
        return res.end(verifyPage(!!user));
      }
      return user ? json(res, 200, { status: 'verified' }) : json(res, 400, { error: 'invalid_or_expired' });
    }
    if (path === '/api/auth/login' && req.method === 'POST') {
      let body; try { body = await readJson(req); } catch { return json(res, 400, { error: 'invalid_body' }); }
      try {
        const result = await auth.login(body.email, body.password, req.headers['user-agent']);
        return json(res, 200, result);
      } catch (e) {
        if (e.code === 'INVALID_CREDENTIALS') return json(res, 401, { error: 'invalid_credentials' });
        if (e.code === 'EMAIL_NOT_VERIFIED') return json(res, 403, { error: 'email_not_verified' });
        throw e;
      }
    }
    if (path === '/api/auth/me' && req.method === 'GET') {
      const user = await auth.userForToken(bearer(req));
      return user ? json(res, 200, { user: { id: user.id, email: user.email } }) : json(res, 401, { error: 'unauthorized' });
    }
    if (path === '/api/auth/logout' && req.method === 'POST') {
      await auth.logout(bearer(req));
      return json(res, 200, { status: 'ok' });
    }
    return json(res, 404, { error: 'not_found' });
  } catch (error) {
    console.error(JSON.stringify({ event: 'auth_error', code: error.code || 'ERROR' }));
    return json(res, 500, { error: 'server_error' });
  }
}
async function handleProjects(req, res, url, projectStore, authStore) {
  if (!projectStore || !authStore) return json(res, 404, { error: 'not_found' });
  const user = await authStore.userForToken(bearer(req));
  if (!user) return json(res, 401, { error: 'unauthorized' });
  const path = url.pathname;
  try {
    if (path === '/api/projects') {
      if (req.method === 'GET') {
        const rows = await projectStore.list(user.id);
        return json(res, 200, { projects: rows.map(toRemoteProject) });
      }
      if (req.method === 'POST' || req.method === 'PUT') {
        let body; try { body = await readJson(req); } catch (e) { return json(res, e.code === 'TOO_LARGE' ? 413 : 400, { error: 'invalid_body' }); }
        if (!body.clientId) return json(res, 400, { error: 'invalid_body' });
        const row = await projectStore.upsert(user.id, {
          clientId: body.clientId,
          name: body.name ?? null,
          mode: body.mode ?? null,
          unit: body.unit ?? null,
          scaleStatus: body.scaleStatus ?? null,
          notes: body.notes ?? null,
          payload: body.payload && typeof body.payload === 'object' ? body.payload : {},
          revision: body.revision,
        });
        return json(res, 200, { project: toRemoteProject(row) });
      }
      return json(res, 405, { error: 'method_not_allowed' }, { Allow: 'GET, POST, PUT' });
    }
    const match = /^\/api\/projects\/([^/]+)$/.exec(path);
    if (match) {
      if (req.method === 'DELETE') {
        await projectStore.remove(user.id, decodeURIComponent(match[1]));
        return json(res, 200, { status: 'ok' });
      }
      return json(res, 405, { error: 'method_not_allowed' }, { Allow: 'DELETE' });
    }
    return json(res, 404, { error: 'not_found' });
  } catch (error) {
    console.error(JSON.stringify({ event: 'projects_error', code: error.code || 'ERROR' }));
    return json(res, 500, { error: 'server_error' });
  }
}
function toRemoteProject(row) {
  return {
    clientId: row.client_id,
    name: row.name ?? '',
    mode: row.mode ?? '',
    unit: row.unit ?? '',
    scaleStatus: row.scale_status ?? '',
    notes: row.notes ?? '',
    revision: Number(row.revision),
    updatedAt: (row.updated_at instanceof Date ? row.updated_at.toISOString() : String(row.updated_at)),
  };
}
export function createApp({ store, authStore = null, projectStore = null, appI18nStore = null, publicDir = defaultPublic, publicBaseUrl }) {
  const origin = publicOrigin(publicBaseUrl);
  const clients = new Set();
  const broadcast = payload => {
    for (const client of clients) {
      if (!client.write(`event: content\ndata: ${JSON.stringify(payload)}\n\n`)) client.destroy();
    }
  };
  store.on('content', broadcast);
  const heartbeat = setInterval(() => {
    for (const client of clients) if (!client.write(': heartbeat\n\n')) client.destroy();
  }, 25000);
  heartbeat.unref();
  const server = createServer(async (req, res) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
    res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'");
    let url;
    try { url = new URL(req.url, 'http://localhost'); } catch { return json(res, 400, { error: 'invalid_url' }); }
    if (url.pathname.startsWith('/api/auth/') || url.pathname === '/api/projects' || url.pathname.startsWith('/api/projects/')) res.setHeader('X-Robots-Tag', 'noindex, nofollow');
    if (authStore && url.pathname.startsWith('/api/auth/')) return handleAuth(req, res, url, authStore);
    if (url.pathname === '/api/projects' || url.pathname.startsWith('/api/projects/')) return handleProjects(req, res, url, projectStore, authStore);
    if (!['GET', 'HEAD'].includes(req.method)) return json(res, 405, { error: 'method_not_allowed' }, { Allow: 'GET, HEAD' });
    if (url.pathname === '/healthz') return json(res, 200, { status: 'ok' });
    if (url.pathname === '/readyz') {
      try { await store.ready(); return json(res, 200, { status: 'ready' }); }
      catch { return json(res, 503, { status: 'unavailable' }); }
    }
    if (url.pathname === '/api/app/i18n') {
      if (!appI18nStore) return json(res, 503, { error: 'i18n_unavailable' });
      try {
        const bundle = await appI18nStore.get(url.searchParams.get('lang'));
        const representation = createHash('sha256').update(JSON.stringify(bundle)).digest('base64url');
        const etag = `"i18n-${representation}"`;
        const headers = { ETag: etag, 'Cache-Control': 'no-cache', 'Content-Language': bundle.locale };
        if (etagMatches(req.headers['if-none-match'], etag)) { res.writeHead(304, headers); return res.end(); }
        return json(res, 200, bundle, headers);
      } catch { return json(res, 503, { error: 'i18n_unavailable' }); }
    }
    if (url.pathname === '/api/content') {
      try {
        const bundle = await store.get(normalizeLocale(url.searchParams.get('lang')));
        const representation = createHash('sha256').update(JSON.stringify(bundle)).digest('base64url');
        const etag = `"content-${representation}"`;
        const headers = { ETag: etag, 'Cache-Control': 'no-cache', 'Content-Language': bundle.locale };
        if (etagMatches(req.headers['if-none-match'], etag)) {
          res.writeHead(304, headers); return res.end();
        }
        return json(res, 200, bundle, headers);
      } catch { return json(res, 503, { error: 'content_unavailable' }); }
    }
    if (url.pathname === '/api/events') {
      try {
        const revision = await store.revision();
        res.writeHead(200, { 'Content-Type': 'text/event-stream; charset=utf-8', 'Cache-Control': 'no-cache, no-transform', Connection: 'keep-alive', 'X-Accel-Buffering': 'no' });
        if (req.method === 'HEAD') return res.end();
        clients.add(res);
        res.write(`retry: 3000\nevent: content\ndata: ${JSON.stringify({ revision })}\n\n`);
        req.on('close', () => clients.delete(res));
        return;
      } catch { return json(res, 503, { error: 'content_unavailable' }); }
    }
    if (url.pathname.startsWith('/api/')) return json(res, 404, { error: 'not_found' });
    if (url.pathname === '/robots.txt' || url.pathname === '/sitemap.xml') {
      const isSitemap = url.pathname === '/sitemap.xml';
      const body = isSitemap ? sitemap(origin) : robots(origin);
      const etag = `"discovery-${createHash('sha256').update(body).digest('base64url')}"`;
      const headers = { ETag: etag, 'Cache-Control': 'public, max-age=0, must-revalidate' };
      if (etagMatches(req.headers['if-none-match'], etag)) { res.writeHead(304, headers); return res.end(); }
      res.writeHead(200, { ...headers, 'Content-Type': isSitemap ? 'application/xml; charset=utf-8' : 'text/plain; charset=utf-8', 'Content-Length': Buffer.byteLength(body) });
      return res.end(req.method === 'HEAD' ? undefined : body);
    }
    try {
      let path = decodeURIComponent(url.pathname);
      if (path.includes('\\') || path.includes('\0') || path.split('/').some(part => part.startsWith('.'))) return json(res, 404, { error: 'not_found' });
      if (path.length > 1) path = path.replace(/\/$/, '');
      const root = await realpath(publicDir);
      const target = resolve(root, routes.has(path) ? 'index.html' : `.${path}`);
      if (!target.startsWith(`${root}${sep}`)) return json(res, 404, { error: 'not_found' });
      const actual = await realpath(target);
      if (!actual.startsWith(`${root}${sep}`)) return json(res, 404, { error: 'not_found' });
      const info = await stat(actual, { bigint: true });
      if (!info.isFile()) return json(res, 404, { error: 'not_found' });
      if (routes.has(path) || path === '/index.html') {
        try {
          const bundle = await store.get(normalizeLocale(url.searchParams.get('lang')));
          const template = await readFile(actual, 'utf8');
          const rendered = renderSeo(template, bundle, path === '/index.html' ? '/' : path, origin);
          const etag = `"page-${createHash('sha256').update(rendered.html).update(JSON.stringify(bundle)).digest('base64url')}"`;
          const headers = { ETag: etag, 'Cache-Control': 'no-cache', 'Content-Language': rendered.locale };
          res.setHeader('Content-Security-Policy', res.getHeader('Content-Security-Policy').replace("script-src 'self';", `script-src 'self' 'sha256-${rendered.scriptHash}';`));
          if (etagMatches(req.headers['if-none-match'], etag)) { res.writeHead(304, headers); return res.end(); }
          res.writeHead(200, { ...headers, 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': Buffer.byteLength(rendered.html) });
          return res.end(req.method === 'HEAD' ? undefined : rendered.html);
        } catch {
          return json(res, 503, { error: 'content_unavailable' }, { 'Retry-After': '30' });
        }
      }
      // Isolated SVG policy permits artwork animation, with all scripts disabled.
      if (extname(actual) === '.svg') res.setHeader('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; script-src 'none'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'");
      // Nanosecond timestamps plus inode catch same-size edits and atomic replacements.
      // Weak validation is appropriate for a validator derived from filesystem metadata.
      const etag = `W/"asset-${info.size.toString(16)}-${info.mtimeNs.toString(16)}-${info.ctimeNs.toString(16)}-${info.ino.toString(16)}"`;
      const headers = {
        ETag: etag,
        'Last-Modified': info.mtime.toUTCString(),
        'Cache-Control': extname(actual) === '.html' ? 'no-cache' : 'public, max-age=0, must-revalidate',
      };
      if (etagMatches(req.headers['if-none-match'], etag)) {
        res.writeHead(304, headers);
        return res.end();
      }
      res.writeHead(200, { ...headers, 'Content-Type': mime[extname(actual)] || 'application/octet-stream', 'Content-Length': info.size.toString() });
      res.end(req.method === 'HEAD' ? undefined : await readFile(actual));
    } catch (error) {
      if (!res.headersSent) return json(res, error instanceof URIError ? 400 : 404, { error: 'not_found' });
      res.destroy();
    }
  });
  server.on('close', () => { clearInterval(heartbeat); store.off('content', broadcast); });
  server.closeEvents = () => { for (const client of clients) client.end(); clients.clear(); };
  return server;
}
