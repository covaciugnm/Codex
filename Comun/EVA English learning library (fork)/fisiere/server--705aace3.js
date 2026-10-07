#!/usr/bin/env node
/**
 * EVA — English Voice Assistant · Prototip server
 * Zero dependențe: Node.js >= 18 (fetch nativ). Rulează: node server.js
 * Servește UI-ul din /public, conținutul din /content și expune /api/*.
 * Cheia API Anthropic stă DOAR aici (config.local.json) — nu ajunge în browser.
 */
'use strict';

const http = require('http');
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const db = require('./db');

const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, 'public');
const CONTENT_DIR = path.join(ROOT, 'content'); // sursa JSON de seed pt. baza de date

const PORT = Number(process.env.EVA_PORT || 3311);
// Implicit: doar local (127.0.0.1). Pentru acces din LAN pornește cu EVA_HOST=0.0.0.0 (vezi EVA-LAN.bat).
const HOST = process.env.EVA_HOST || '127.0.0.1';
const LAN_MODE = !(HOST === '127.0.0.1' || HOST === 'localhost');

function lanIPs() {
  const out = [];
  const ifs = os.networkInterfaces();
  for (const name of Object.keys(ifs)) for (const ni of ifs[name] || [])
    if (ni.family === 'IPv4' && !ni.internal) out.push(ni.address);
  return out;
}

// HTTPS (opțional) — necesar pentru microfon pe telefoane (Android/iOS)
function loadCert() {
  try {
    return {
      key: fs.readFileSync(path.join(ROOT, 'certs', 'key.pem')),
      cert: fs.readFileSync(path.join(ROOT, 'certs', 'cert.pem')),
    };
  } catch { return null; }
}
const CERT = process.env.EVA_HTTPS === '1' ? loadCert() : null;
const SCHEME = CERT ? 'https' : 'http';

// ---------- provideri LLM ----------
// Ollama local (native /api/chat) + Claude (Anthropic) + Demo (offline).
// Endpoint-urile Qwen pot fi suprascrise cu variabile de mediu.
const PROVIDERS = {
  demo: { label: 'Demo (fără AI — răspunsuri din lecție)', kind: 'demo' },
  qwen27: {
    label: 'Qwen 27B (local)', kind: 'ollama',
    base: process.env.EVA_QWEN27_URL || 'http://192.168.100.151:11436',
    model: process.env.EVA_QWEN27_MODEL || 'qwen3.6:27b',
  },
  qwen35: {
    label: 'Qwen 35B (local)', kind: 'ollama',
    base: process.env.EVA_QWEN35_URL || 'http://192.168.100.151:11438',
    model: process.env.EVA_QWEN35_MODEL || 'batiai/qwen3.6-35b:q6',
  },
  anthropic: {
    label: 'Claude (Anthropic — necesită cheie)', kind: 'anthropic', needsKey: true,
    models: ['claude-opus-5', 'claude-sonnet-5', 'claude-haiku-4-5'],
  },
};
const ALLOWED_MODELS = PROVIDERS.anthropic.models;
const ALLOWED_EFFORT = ['low', 'medium', 'high'];
const DEFAULTS = { provider: 'qwen27', model: 'claude-opus-5', effort: 'low' };
// Allowlist strict (evită chei moștenite din Object.prototype: __proto__, constructor, toString…)
function hasProvider(id) { return typeof id === 'string' && Object.prototype.hasOwnProperty.call(PROVIDERS, id); }

// ---------- config (persistat în DB, cache sincron în memorie) ----------
let settingsCache = {}; // umplut la pornire din tabelul settings
function validateSettings(raw) {
  raw = raw || {};
  return {
    provider: hasProvider(raw.provider) ? raw.provider : DEFAULTS.provider,
    apiKey: typeof raw.apiKey === 'string' ? raw.apiKey : '',
    model: ALLOWED_MODELS.includes(raw.model) ? raw.model : DEFAULTS.model,
    effort: ALLOWED_EFFORT.includes(raw.effort) ? raw.effort : DEFAULTS.effort,
    googleClientId: typeof raw.googleClientId === 'string' ? raw.googleClientId : '',
    facebookAppId: typeof raw.facebookAppId === 'string' ? raw.facebookAppId : '',
    facebookAppSecret: typeof raw.facebookAppSecret === 'string' ? raw.facebookAppSecret : '',
  };
}
function loadConfig() { return validateSettings(settingsCache); }
async function saveConfig(cfg) {
  settingsCache = validateSettings(cfg);
  await db.saveSettings(settingsCache);
}
function apiKey() {
  return process.env.ANTHROPIC_API_KEY || loadConfig().apiKey || '';
}
/** Va face un apel LLM real (nu demo) pentru configul curent? */
function isLive(cfg) {
  const prov = PROVIDERS[cfg.provider];
  if (!prov || prov.kind === 'demo') return false;
  if (prov.kind === 'anthropic') return Boolean(apiKey());
  return true; // provideri locali — încercăm mereu (eroarea se raportează dacă nu răspund)
}

// ---------- utilizatori & sesiuni (în PostgreSQL) ----------
function hashPw(pw, salt) {
  return crypto.scryptSync(String(pw), salt, 64).toString('hex');
}
function makeUser(email, name, pw, provider) {
  const salt = crypto.randomBytes(16).toString('hex');
  return {
    email, name: String(name || '').slice(0, 40) || email,
    provider: provider || 'local',
    salt: pw ? salt : '',
    hash: pw ? hashPw(pw, salt) : '',
    createdAt: new Date().toISOString(),
  };
}
function verifyPw(user, pw) {
  if (!user || !user.hash) return false;
  const h = hashPw(pw, user.salt);
  const a = Buffer.from(h, 'hex');
  const b = Buffer.from(user.hash, 'hex');
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
function validEmail(e) {
  return typeof e === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e) && e.length <= 190;
}

const SESSION_MAX_MS = 30 * 24 * 3600 * 1000; // 30 zile — aliniat cu Max-Age al cookie-ului
function parseCookies(req) {
  const out = {};
  (req.headers.cookie || '').split(';').forEach((p) => {
    const i = p.indexOf('=');
    if (i > 0) { try { out[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim()); } catch {} }
  });
  return out;
}
async function setSessionCookie(res, email) {
  const t = crypto.randomBytes(32).toString('hex');
  await db.createSession(t, email, Date.now());
  const sec = SCHEME === 'https' ? '; Secure' : '';
  res.setHeader('Set-Cookie', `eva_session=${t}; HttpOnly; SameSite=Lax; Path=/; Max-Age=2592000${sec}`);
}
async function sessionUser(req) {
  const t = parseCookies(req).eva_session;
  if (!t) return null;
  const s = await db.getSession(t);
  if (!s) return null;
  // expirare server-side reală (nu doar Max-Age pe cookie)
  if ((Date.now() - (Number(s.created) || 0)) > SESSION_MAX_MS) { try { await db.deleteSession(t); } catch {} return null; }
  const u = await db.getUser(s.email);
  return u ? { email: u.email, name: u.name } : null;
}
async function clearSessionCookie(req, res) {
  const t = parseCookies(req).eva_session;
  if (t) { try { await db.deleteSession(t); } catch {} }
  res.setHeader('Set-Cookie', 'eva_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0');
}

// Utilizator implicit (creat o singură dată, dacă nu există) — apelat la pornire.
async function seedDefaultUser() {
  const email = 'cesiro.horeca@gmail.com';
  if (!(await db.getUser(email))) await db.insertUser(makeUser(email, 'Cesiro', 'Cesiro121', 'local'));
}

// User „momeală" cu hash real → login-ul rulează scrypt și când emailul NU există,
// astfel timpul de răspuns nu trădează dacă un cont există (anti-enumerare).
const DECOY_USER = makeUser('decoy@eva.local', 'decoy', crypto.randomBytes(24).toString('hex'), 'local');
/** Verifică parola în timp ~constant. Întoarce userul real doar dacă parola e corectă. */
async function authenticateLocal(email, pw) {
  const user = await db.getUser(email);
  const hasPw = !!(user && user.hash);           // conturile OAuth n-au parolă
  const match = verifyPw(hasPw ? user : DECOY_USER, pw); // scrypt rulează în ambele cazuri
  return (hasPw && match) ? user : null;
}

async function verifyGoogle(credential) {
  const cid = loadConfig().googleClientId;
  // Client ID OBLIGATORIU: fără el, un id_token de la ORICE aplicație Google ar fi acceptat (audience confusion).
  if (!cid) throw new Error('Login Google neconfigurat (lipsește Google Client ID în Setări).');
  const r = await fetch('https://oauth2.googleapis.com/tokeninfo?id_token=' + encodeURIComponent(String(credential || '')));
  if (!r.ok) throw new Error('Token Google invalid');
  const d = await r.json();
  // tokeninfo verifică semnătura/expirarea, dar NU că tokenul e pentru noi → verificăm aud + iss + email_verified
  if (d.aud !== cid) throw new Error('Token Google emis pentru altă aplicație.');
  const iss = String(d.iss || '');
  if (iss !== 'accounts.google.com' && iss !== 'https://accounts.google.com') throw new Error('Emitent Google invalid.');
  if (String(d.email_verified) !== 'true') throw new Error('Emailul Google nu este verificat.');
  if (!d.email) throw new Error('Google nu a returnat email.');
  return { email: String(d.email).toLowerCase(), name: d.name || d.email };
}
async function verifyFacebook(token) {
  const cfg = loadConfig();
  const appId = cfg.facebookAppId;
  const appSecret = cfg.facebookAppSecret;
  // App ID + App Secret OBLIGATORII: altfel un token de la ORICE aplicație Facebook ar fi acceptat.
  if (!appId || !appSecret) throw new Error('Login Facebook neconfigurat (lipsește App ID / App Secret în Setări).');
  const appToken = encodeURIComponent(appId + '|' + appSecret);
  // debug_token confirmă că tokenul e valid ȘI emis pentru aplicația noastră
  const dbg = await fetch(`https://graph.facebook.com/debug_token?input_token=${encodeURIComponent(String(token || ''))}&access_token=${appToken}`);
  const dj = await dbg.json();
  const data = dj && dj.data;
  if (!data || data.is_valid !== true || String(data.app_id) !== String(appId)) throw new Error('Token Facebook invalid pentru această aplicație.');
  const r = await fetch('https://graph.facebook.com/me?fields=id,name,email&access_token=' + encodeURIComponent(String(token || '')));
  const d = await r.json();
  if (!d || d.error || !d.id) throw new Error('Token Facebook invalid');
  return { email: d.email ? String(d.email).toLowerCase() : (d.id + '@facebook.local'), name: d.name || 'Utilizator Facebook' };
}
async function upsertOAuthUser(profile, provider) {
  const existing = await db.getUser(profile.email);
  // Legare cont↔provider: nu lăsăm un login OAuth să intre într-un cont creat altfel (parolă/alt provider).
  // Previne bypass de parolă și pre-hijacking prin coliziune de email.
  if (existing && existing.provider !== provider) {
    throw new Error('Există deja un cont cu acest email, creat prin altă metodă. Folosește metoda inițială de conectare.');
  }
  if (!existing) await db.insertUser(makeUser(profile.email, profile.name, '', provider));
  const u = existing || (await db.getUser(profile.email));
  return { email: u.email, name: u.name };
}

// ---------- conținut (cache în memorie, alimentat din DB la pornire) ----------
let moduleTitlesCache = {}; // {A1:{1:'…'}, A2:{1:'…'}, …} pt. antetele de modul din UI
function buildModuleTitles() {
  const map = { A1: { ...db.MODULE_TITLES } };
  try {
    const f = path.join(CONTENT_DIR, 'curriculum-a2-c2.json');
    if (fs.existsSync(f)) {
      const arch = JSON.parse(fs.readFileSync(f, 'utf8'));
      for (const lvl of arch) { map[lvl.level] = {}; for (const m of lvl.modules) map[lvl.level][m.n] = m.title; }
    }
  } catch (e) { console.error('[EVA] curriculum-a2-c2.json invalid:', e.message); }
  moduleTitlesCache = map;
}
let unitsCache = new Map(); // Map<code, unit>
let levelTestsCache = null;
function loadUnits() { return unitsCache; }
/** Reîncarcă în memorie unitățile și testele de nivel din PostgreSQL. */
async function refreshContentCache() {
  const units = await db.allUnits();
  const map = new Map();
  for (const u of units) if (u && u.code) map.set(u.code, u);
  unitsCache = map;
  levelTestsCache = await db.getLevelTests();
}
function unitIndex() {
  return [...loadUnits().values()]
    .sort((a, b) => a.code.localeCompare(b.code))
    .map((u) => ({
      code: u.code, title: u.title, titleRo: u.titleRo,
      level: db.levelOf(u.code),      // A1 / A2 / B1 / B2 / C1 / C2
      module: db.moduleOf(u.code),    // 1..N în cadrul nivelului
      durationMin: u.durationMin || 25,
      counts: { vocab: (u.vocab || []).length, srs: (u.srs || []).length, test: (u.test?.items || []).length },
    }));
}

// ---------- motor demo (fără cheie API) ----------
function demoReply(unit, stage, messages) {
  const flow = unit.flow || { guided: [], semiGuided: [], free: {} };
  const last = (messages[messages.length - 1]?.content || '').trim();
  // numărăm doar turele reale ale utilizatorului (fără cererile de ajutor)
  const real = messages.filter((m) => m.role === 'user' && !m.content.startsWith('[AJUTOR RO]')).length;

  // ajutor în română — nu avansează fluxul
  if (last.startsWith('[AJUTOR RO]')) {
    const step = (stage === 'semi' ? flow.semiGuided : flow.guided)[Math.max(0, real - 1)] || flow.guided[0];
    const model = step?.model ? `Poți răspunde, de exemplu: **„${step.model}"**. ` : '';
    return `Sigur! 🇷🇴 ${model}Scrie sau spune varianta ta în engleză — te corectez cu blândețe, fără note.`;
  }
  const praise = ['Great! 👏', 'Well done!', 'Perfect! ⭐', 'Nice!'];
  const p = praise[real % praise.length];

  if (stage === 'guided') {
    const step = flow.guided[real]; // opener = guided[0] (deja afișat); după replica reală #k → guided[k]
    if (step) return `${p} ${step.eva}`;
    return `${p} Am terminat partea ghidată. 🎉 Treci la **Semi-ghidat** pentru întrebări deschise!`;
  }
  if (stage === 'semi') {
    const step = flow.semiGuided[real]; // opener = semiGuided[0]; apoi semiGuided[k]
    if (step) return `${p} ${step.eva}${step.hint ? `\n\n_(indiciu: ${step.hint})_` : ''}`;
    return `${p} Ai exersat toate întrebările. 🎉 Treci la **Liber** pentru un scenariu real!`;
  }
  // free: openerul (scenariul) e deja afișat; continuăm conversația
  return `${p} Tell me more! _(mod demo — adaugă cheia API în ⚙️ Setări pentru conversație reală cu EVA)_`;
}

// ---------- asamblarea system promptului ----------
const STAGE_DIRECTIVES = {
  guided: (u) => `ETAPA CURENTĂ: GHIDAT. Urmează fluxul ghidat al unității pas cu pas — pune întrebările în ordinea de mai jos, câte UNA pe mesaj, și elicită structura-țintă:\n${(u.flow?.guided || [])
    .map((g, i) => `${i + 1}. EVA: "${g.eva}"${g.model ? ` (răspuns model: "${g.model}")` : ''}`)
    .join('\n')}`,
  semi: (u) => `ETAPA CURENTĂ: SEMI-GHIDAT. Pune întrebări deschise pe tema unității; dacă elevul se blochează, oferă indicii scurte ("prompts"), nu răspunsul întreg. Exemple de întrebări:\n${(u.flow?.semiGuided || [])
    .map((s) => `- "${s.eva}"${s.hint ? ` (indiciu: ${s.hint})` : ''}`)
    .join('\n')}`,
  free: (u) => `ETAPA CURENTĂ: LIBER (scenariu). Joacă scenariul: ${u.flow?.free?.scenario || ''}\nObiectiv: ${u.flow?.free?.objective || 'conversație naturală pe tema unității'}. Fără model afișat — elevul produce singur; recast la nevoie.`,
};

function buildSystem(unit, stage, userName) {
  const base = unit.systemPrompt || `Ești EVA, tutore prietenos de engleză pentru un vorbitor de română, nivel A1. Corectezi prin recast, mesaje scurte, sprijin în română la nevoie.`;
  const directive = (STAGE_DIRECTIVES[stage] || STAGE_DIRECTIVES.guided)(unit);
  const ui = `REGULI DE FORMAT (chat): mesaje scurte (1-3 rânduri), marchează corecțiile prin recast cu **bold**, un singur pas/întrebare pe mesaj. Dacă utilizatorul scrie "[AJUTOR RO] ...", explică pe scurt ÎN ROMÂNĂ ce a spus EVA și cum poate răspunde, apoi revino la engleză.`;
  const who = userName ? `\n\nUTILIZATOR: pe cursant îl cheamă ${String(userName).slice(0, 40)}. Adresează-i-te pe nume, cald și prietenos (ex. „Great job, ${String(userName).slice(0, 40)}!").` : '';
  return `${base}\n\n${directive}\n\n${ui}${who}`;
}

// modelele Qwen „gânditoare" pot emite blocuri de reflecție — le ascundem
function stripThinking(s) {
  return String(s)
    .replace(/<think>[\s\S]*?<\/think>/gi, '')
    .replace(/<thinking>[\s\S]*?<\/thinking>/gi, '')
    .trim();
}

// ---------- apel Ollama local (Qwen) · endpoint nativ /api/chat ----------
async function ollamaChat(prov, unit, stage, messages, userName) {
  const body = {
    model: prov.model,
    stream: false,
    messages: [{ role: 'system', content: buildSystem(unit, stage, userName) }, ...messages],
    options: {
      num_ctx: 8192,
      temperature: 0.6,
      top_p: 0.9,
      top_k: 25,
      repeat_penalty: 1.05,
    },
  };
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 180_000); // modelele locale pot fi lente
  let res;
  try {
    res = await fetch(prov.base + '/api/chat', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
  } catch (e) {
    const err = new Error(`Nu pot contacta ${prov.label} la ${prov.base}. Verifică dacă serverul Qwen (Ollama) e pornit și accesibil în rețea.`);
    err.status = 502; throw err;
  } finally {
    clearTimeout(timer);
  }
  if (!res.ok) {
    let detail = '';
    try { detail = (await res.json())?.error || ''; } catch {}
    const err = new Error(`Eroare ${prov.label} (${res.status})${detail ? ': ' + detail : ''}`);
    err.status = 502; throw err;
  }
  const data = await res.json();
  const reply = stripThinking(data?.message?.content || '');
  return { reply: reply || '…' };
}

// ---------- dispecer conversație (după provider) ----------
async function chatWith(cfg, unit, stage, messages, userName) {
  const prov = PROVIDERS[cfg.provider] || PROVIDERS.demo;
  if (prov.kind === 'anthropic') return anthropicChat(unit, stage, messages, userName);
  return ollamaChat(prov, unit, stage, messages, userName);
}

// ---------- apel Anthropic ----------
async function anthropicChat(unit, stage, messages, userName) {
  const cfg = loadConfig();
  const key = apiKey();
  // API-ul cere ca primul mesaj să fie 'user'; openerul EVA e 'assistant' → prepend un user-turn
  const apiMessages = messages[0] && messages[0].role === 'assistant'
    ? [{ role: 'user', content: "Let's start the lesson." }, ...messages]
    : messages;
  const body = {
    model: cfg.model,
    max_tokens: 1024,
    system: [
      { type: 'text', text: buildSystem(unit, stage, userName), cache_control: { type: 'ephemeral' } },
    ],
    messages: apiMessages,
  };
  // 'effort' e respins pe Haiku 4.5 — îl trimitem doar pe modelele care îl acceptă
  if (cfg.model !== 'claude-haiku-4-5') body.output_config = { effort: cfg.effort };
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 60_000);
  let res;
  try {
    res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
  } finally {
    clearTimeout(timer);
  }
  if (!res.ok) {
    const status = res.status;
    let detail = '';
    try { detail = (await res.json())?.error?.message || ''; } catch {}
    const friendly =
      status === 401 ? 'Cheia API pare invalidă. Verifică-o în Setări.' :
      status === 429 ? 'Prea multe cereri — așteaptă câteva secunde și reîncearcă.' :
      status === 529 ? 'Serviciul e aglomerat momentan. Reîncearcă imediat.' :
      `Eroare API (${status}).`;
    const err = new Error(friendly + (detail ? ` [${detail}]` : ''));
    err.status = status;
    throw err;
  }
  const data = await res.json();
  if (data.stop_reason === 'refusal') {
    return { reply: 'Hmm, nu pot răspunde la asta. 🙂 Hai să revenim la lecția noastră! Ready to continue?', usage: data.usage };
  }
  const reply = (data.content || [])
    .filter((b) => b.type === 'text')
    .map((b) => b.text)
    .join('')
    .trim();
  return { reply: reply || '…', usage: data.usage };
}

// ---------- helpers HTTP ----------
function send(res, status, data, type = 'application/json') {
  const payload = type === 'application/json' ? JSON.stringify(data) : data;
  res.writeHead(status, {
    'content-type': `${type}; charset=utf-8`,
    'cache-control': 'no-store',
    'x-content-type-options': 'nosniff',
  });
  res.end(payload);
}
function readBody(req, limit = 256 * 1024) {
  return new Promise((resolve, reject) => {
    let size = 0, aborted = false;
    const chunks = [];
    req.on('data', (c) => {
      if (aborted) return;
      size += c.length;
      if (size > limit) {
        aborted = true;
        const err = new Error('Corpul cererii e prea mare'); err.status = 413;
        reject(err);
      } else chunks.push(c);
    });
    req.on('end', () => {
      if (aborted) return;
      try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}')); }
      catch { const err = new Error('JSON invalid'); err.status = 400; reject(err); }
    });
    req.on('error', (e) => { const err = new Error('Eroare la citirea cererii'); err.status = 400; reject(err); });
  });
}

const MIME = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.ico': 'image/x-icon', '.woff2': 'font/woff2',
};
function serveStatic(res, urlPath) {
  const rel = urlPath === '/' ? '/index.html' : urlPath;
  const filePath = path.normalize(path.join(PUBLIC_DIR, rel));
  if (!filePath.startsWith(PUBLIC_DIR + path.sep) && filePath !== path.join(PUBLIC_DIR, 'index.html')) {
    return send(res, 403, { error: 'Interzis' });
  }
  fs.readFile(filePath, (err, buf) => {
    if (err) return send(res, 404, { error: 'Nu există' });
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'content-type': `${MIME[ext] || 'application/octet-stream'}; charset=utf-8`,
      'x-content-type-options': 'nosniff',
      'cache-control': 'no-store', // prototip: mereu versiunea cea mai nouă
    });
    res.end(buf);
  });
}

// ---------- rutare ----------
// Allowlist explicit de Host/Origin (localhost + IP-urile LAN reale + hostname).
// NU acceptăm „orice Host cu portul corect" → blochează DNS-rebinding din LAN.
// Gazde permise explicit (ex. un domeniu): din EVA_ALLOWED_HOSTS="app.exemplu.ro,eva.local"
const EXTRA_HOSTS = new Set(
  String(process.env.EVA_ALLOWED_HOSTS || '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean)
);
function isPrivateIPv4(s) {
  const m = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.exec(s);
  if (!m) return false;
  const p = m.slice(1).map(Number);
  if (p.some((n) => n > 255)) return false;
  const [a, b] = p;
  return a === 10 || a === 127 || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || (a === 169 && b === 254);
}
/** Host acceptat? localhost + orice IP LAN privat (merge prin Docker/rețea) + gazde din EVA_ALLOWED_HOSTS.
 *  Domeniile arbitrare sunt RESPINSE → oprește DNS-rebinding (care folosește un domeniu). */
function hostAllowed(hostHeader) {
  const host = String(hostHeader || '').toLowerCase();
  if (!host) return false;
  const i = host.lastIndexOf(':');
  const name = i >= 0 ? host.slice(0, i) : host;
  // domeniile permise explicit (ex. prin Cloudflare Tunnel) sunt acceptate pe orice port —
  // proxy-ul servește pe 443 și trimite Host fără portul intern
  if (EXTRA_HOSTS.has(name)) return true;
  const port = i >= 0 ? host.slice(i + 1) : (SCHEME === 'https' ? '443' : '80');
  if (port !== String(PORT)) return false;
  if (name === 'localhost' || name === '[::1]' || name === '::1') return true;
  return isPrivateIPv4(name);
}
function originAllowed(origin) {
  try {
    const u = new URL(origin);
    // domeniile permise explicit vin prin proxy pe HTTPS chiar dacă originea locală e HTTP
    if (EXTRA_HOSTS.has(u.hostname.toLowerCase()) && (u.protocol === 'https:' || u.protocol === 'http:')) return true;
    return u.protocol === `${SCHEME}:` && hostAllowed(u.host);
  } catch { return false; }
}

async function handler(req, res) {
  // Verificare Host: localhost / IP LAN privat / gazde permise. Domeniile arbitrare → 421 (anti-rebinding).
  if (!hostAllowed(req.headers.host)) { res.writeHead(421, { 'content-type': 'text/plain' }); res.end('Host neacceptat'); return; }

  // URL cu bază fixă (Host malformat nu mai poate arunca)
  let url;
  try { url = new URL(req.url, `http://127.0.0.1:${PORT}`); }
  catch { return send(res, 400, { error: 'URL invalid' }); }
  const p = url.pathname;

  // CSRF: cererile care schimbă starea trebuie să fie same-origin + JSON
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    const sfs = req.headers['sec-fetch-site'];
    const origin = req.headers.origin;
    const originOk = !origin || originAllowed(origin); // Origin (dacă e prezent) trebuie să fie o gazdă permisă
    const siteOk = !sfs || sfs === 'same-origin' || sfs === 'none';
    const ctOk = (req.headers['content-type'] || '').includes('application/json');
    if (!originOk || !siteOk || !ctOk) return send(res, 403, { error: 'Cerere blocată (verificare same-origin)' });
  }

  try {
    // ----- Autentificare -----
    if (p === '/api/auth/me' && req.method === 'GET') {
      const u = await sessionUser(req);
      return send(res, 200, u ? { authenticated: true, email: u.email, name: u.name } : { authenticated: false });
    }
    if (p === '/api/auth/config' && req.method === 'GET') {
      const c = loadConfig();
      return send(res, 200, { googleClientId: c.googleClientId || '', facebookAppId: c.facebookAppId || '' });
    }
    if (p === '/api/auth/signup' && req.method === 'POST') {
      const b = await readBody(req);
      const email = String(b.email || '').trim().toLowerCase();
      const name = String(b.name || '').trim().slice(0, 40);
      const pw = String(b.password || '');
      const confirm = String(b.confirm || '');
      if (!validEmail(email)) return send(res, 400, { error: 'Adresa de email nu pare validă.' });
      if (!name) return send(res, 400, { error: 'Alege un nume cu care să ți se adreseze EVA.' });
      if (pw.length < 6) return send(res, 400, { error: 'Parola trebuie să aibă cel puțin 6 caractere.' });
      if (pw.length > 128) return send(res, 400, { error: 'Parola e prea lungă (maxim 128 de caractere).' });
      if (pw !== confirm) return send(res, 400, { error: 'Cele două parole nu sunt identice.' });
      if (await db.getUser(email)) return send(res, 409, { error: 'Există deja un cont cu acest email. Conectează-te.' });
      await db.insertUser(makeUser(email, name, pw, 'local'));
      await setSessionCookie(res, email);
      return send(res, 200, { email, name });
    }
    if (p === '/api/auth/login' && req.method === 'POST') {
      const b = await readBody(req);
      const email = String(b.email || '').trim().toLowerCase();
      const pw = String(b.password || '');
      if (pw.length > 128) return send(res, 401, { error: 'Email sau parolă greșită.' });
      const user = await authenticateLocal(email, pw); // timp ~constant (rulează scrypt și dacă emailul nu există)
      if (!user) return send(res, 401, { error: 'Email sau parolă greșită.' });
      await setSessionCookie(res, email);
      return send(res, 200, { email: user.email, name: user.name });
    }
    if (p === '/api/auth/logout' && req.method === 'POST') {
      await clearSessionCookie(req, res);
      return send(res, 200, { ok: true });
    }
    if (p === '/api/auth/google' && req.method === 'POST') {
      const b = await readBody(req);
      try {
        const prof = await verifyGoogle(String(b.credential || ''));
        const u = await upsertOAuthUser(prof, 'google');
        await setSessionCookie(res, u.email);
        return send(res, 200, u);
      } catch (e) { return send(res, 401, { error: e.message || 'Autentificare Google eșuată.' }); }
    }
    if (p === '/api/auth/facebook' && req.method === 'POST') {
      const b = await readBody(req);
      try {
        const prof = await verifyFacebook(String(b.accessToken || ''));
        const u = await upsertOAuthUser(prof, 'facebook');
        await setSessionCookie(res, u.email);
        return send(res, 200, u);
      } catch (e) { return send(res, 401, { error: e.message || 'Autentificare Facebook eșuată.' }); }
    }
    // stare per-utilizator (progres, chat, SRS) — persistată în DB
    if (p === '/api/state' && req.method === 'GET') {
      const user = await sessionUser(req);
      if (!user) return send(res, 401, { error: 'Autentificare necesară.' });
      return send(res, 200, await db.getUserState(user.email));
    }
    if (p === '/api/state' && req.method === 'POST') {
      const user = await sessionUser(req);
      if (!user) return send(res, 401, { error: 'Autentificare necesară.' });
      const b = await readBody(req);
      const k = String(b.k || '');
      if (!k || k.length > 200) return send(res, 400, { error: 'cheie invalidă' });
      await db.setUserState(user.email, k, b.v);
      return send(res, 200, { ok: true });
    }
    // istoric append-only: progres + rezultate (pt. afișare viitoare)
    if (p === '/api/activity' && req.method === 'POST') {
      const user = await sessionUser(req);
      if (!user) return send(res, 401, { error: 'Autentificare necesară.' });
      const b = await readBody(req);
      const kind = String(b.kind || '').slice(0, 40);
      if (!kind) return send(res, 400, { error: 'kind lipsă' });
      const unitCode = b.unitCode ? String(b.unitCode).slice(0, 32) : null;
      const id = await db.appendActivity(user.email, unitCode, kind, b.data, Date.now());
      return send(res, 200, { ok: true, id });
    }
    if (p === '/api/history' && req.method === 'GET') {
      const user = await sessionUser(req);
      if (!user) return send(res, 401, { error: 'Autentificare necesară.' });
      const unitCode = url.searchParams.get('unitCode');
      const limit = url.searchParams.get('limit');
      return send(res, 200, await db.getActivity(user.email, unitCode, limit));
    }
    // rezumat pe niveluri (pt. gruparea în UI)
    if (p === '/api/modules' && req.method === 'GET') {
      return send(res, 200, await db.moduleSummary());
    }
    // titluri de module pe niveluri (A1 + A2–C2 din arhitectură)
    if (p === '/api/module-titles' && req.method === 'GET') {
      return send(res, 200, moduleTitlesCache);
    }
    // dicționar: definiția EN (oed) + corespondentul RO (dex) pt. un cuvânt
    if (p === '/api/dict' && req.method === 'GET') {
      const word = url.searchParams.get('word') || '';
      const e = await db.getDictEntry(word);
      return e ? send(res, 200, e) : send(res, 404, { error: 'Cuvânt negăsit în dicționar' });
    }

    // API
    if (p === '/api/units' && req.method === 'GET') return send(res, 200, unitIndex());

    if (p.startsWith('/api/units/') && req.method === 'GET') {
      const code = decodeURIComponent(p.slice('/api/units/'.length));
      const unit = loadUnits().get(code);
      return unit ? send(res, 200, unit) : send(res, 404, { error: 'Unitate necunoscută' });
    }

    if (p === '/api/level-tests' && req.method === 'GET') {
      if (!levelTestsCache) return send(res, 404, { error: 'Lipsesc testele' });
      return send(res, 200, levelTestsCache);
    }

    if (p === '/api/config' && req.method === 'GET') {
      const cfg = loadConfig();
      const prov = PROVIDERS[cfg.provider] || PROVIDERS.demo;
      return send(res, 200, {
        provider: cfg.provider,
        providers: Object.entries(PROVIDERS).map(([id, pr]) => ({
          id, label: pr.label, kind: pr.kind, needsKey: !!pr.needsKey, model: pr.model || null,
        })),
        providerLabel: prov.label,
        hasKey: Boolean(apiKey()),
        model: cfg.model,
        effort: cfg.effort,
        models: ALLOWED_MODELS,
        efforts: ALLOWED_EFFORT,
        demo: !isLive(cfg),
        hasFbSecret: Boolean(cfg.facebookAppSecret), // doar dacă e setat, NU secretul în sine
      });
    }

    if (p === '/api/config' && req.method === 'POST') {
      // Modificarea configului (cheie API, provider, ID-uri OAuth) cere sesiune — nu doar same-origin.
      if (!(await sessionUser(req))) return send(res, 401, { error: 'Autentificare necesară pentru a schimba setările.' });
      const body = await readBody(req);
      const cfg = loadConfig();
      if (hasProvider(body.provider)) cfg.provider = body.provider;
      if (typeof body.apiKey === 'string') cfg.apiKey = body.apiKey.trim();
      if (ALLOWED_MODELS.includes(body.model)) cfg.model = body.model;
      if (ALLOWED_EFFORT.includes(body.effort)) cfg.effort = body.effort;
      if (typeof body.googleClientId === 'string') cfg.googleClientId = body.googleClientId.trim().slice(0, 200);
      if (typeof body.facebookAppId === 'string') cfg.facebookAppId = body.facebookAppId.trim().slice(0, 64);
      if (typeof body.facebookAppSecret === 'string' && body.facebookAppSecret.trim()) cfg.facebookAppSecret = body.facebookAppSecret.trim().slice(0, 128);
      await saveConfig(cfg);
      return send(res, 200, { ok: true, provider: cfg.provider, hasKey: Boolean(apiKey()), model: cfg.model, effort: cfg.effort, demo: !isLive(cfg) });
    }

    // test de conexiune la un provider (fără a salva nimic) — doar autentificat (folosit din Setări)
    if (p === '/api/ping' && req.method === 'POST') {
      if (!(await sessionUser(req))) return send(res, 401, { error: 'Autentificare necesară.' });
      const body = await readBody(req);
      const prov = hasProvider(body.provider) ? PROVIDERS[body.provider] : null;
      if (!prov) return send(res, 400, { error: 'provider necunoscut' });
      if (prov.kind === 'demo') return send(res, 200, { ok: true, message: 'Mod demo — fără AI.' });
      if (prov.kind === 'anthropic') return send(res, 200, { ok: Boolean(apiKey()), message: apiKey() ? 'Cheie configurată.' : 'Lipsește cheia API.' });
      // ollama: listăm modelele
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 8000);
        const r = await fetch(prov.base + '/api/tags', { signal: ctrl.signal }).finally(() => clearTimeout(timer));
        if (!r.ok) return send(res, 200, { ok: false, message: `Server accesibil dar a răspuns ${r.status}.` });
        const t = await r.json();
        const names = (t.models || []).map((m) => m.name);
        const has = names.includes(prov.model);
        return send(res, 200, { ok: true, message: `✅ Conectat la ${prov.base}. Model „${prov.model}": ${has ? 'disponibil' : 'NEGĂSIT în listă'}.`, models: names });
      } catch {
        return send(res, 200, { ok: false, message: `❌ Nu răspunde la ${prov.base}. E pornit Ollama/Qwen și accesibil în rețea?` });
      }
    }

    if (p === '/api/chat' && req.method === 'POST') {
      const user = await sessionUser(req);
      if (!user) return send(res, 401, { error: 'Autentificare necesară. Conectează-te.' });
      const body = await readBody(req);
      const unit = loadUnits().get(String(body.unitCode || ''));
      if (!unit) return send(res, 400, { error: 'unitCode invalid' });
      const stage = ['guided', 'semi', 'free'].includes(body.stage) ? body.stage : 'guided';

      // igienizare istoric: doar user/assistant, text, limite stricte
      const messages = (Array.isArray(body.messages) ? body.messages : [])
        .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
        .slice(-40)
        .map((m) => ({ role: m.role, content: m.content.slice(0, 2000) }));
      if (!messages.length || messages[messages.length - 1].role !== 'user') {
        return send(res, 400, { error: 'Ultimul mesaj trebuie să fie al utilizatorului' });
      }

      const cfg = loadConfig();
      if (!isLive(cfg)) {
        return send(res, 200, { reply: demoReply(unit, stage, messages), demo: true });
      }
      try {
        const out = await chatWith(cfg, unit, stage, messages, user.name);
        return send(res, 200, { reply: out.reply, demo: false, usage: out.usage, provider: cfg.provider });
      } catch (e) {
        return send(res, e.status || 502, { error: e.message || 'Eroare la apelul AI' });
      }
    }

    if (p.startsWith('/api/')) return send(res, 404, { error: 'Endpoint necunoscut' });

    // static
    if (req.method === 'GET') return serveStatic(res, p);
    return send(res, 405, { error: 'Metodă nepermisă' });
  } catch (e) {
    return send(res, e.status || 500, { error: e.message || 'Eroare internă' });
  }
}

if (process.env.EVA_HTTPS === '1' && !CERT) {
  console.warn('⚠ EVA_HTTPS=1 dar lipsesc certificatele din certs/. Pornesc pe HTTP. Rulează mai întâi Gen-Cert.bat.');
}
const server = CERT ? https.createServer(CERT, handler) : http.createServer(handler);

/** Încarcă în DB unitățile + testele de nivel din fișierele JSON (sursa versionată în git). */
async function seedContentFromJson() {
  const dir = path.join(CONTENT_DIR, 'units');
  let n = 0;
  if (fs.existsSync(dir)) {
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json')).sort()) {
      try {
        const u = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
        if (u && u.code) { await db.upsertUnit(u); n++; }
      } catch (e) { console.error(`[EVA] JSON invalid: ${f}: ${e.message}`); }
    }
  }
  const lt = path.join(CONTENT_DIR, 'level-tests.json');
  if (fs.existsSync(lt)) {
    try { await db.setLevelTests(JSON.parse(fs.readFileSync(lt, 'utf8'))); } catch (e) { console.error(`[EVA] level-tests invalid: ${e.message}`); }
  }
  return n;
}

/** Populează oed/dex din content/dictionary.json (dacă există). */
async function seedDictionaryFromJson() {
  const f = path.join(CONTENT_DIR, 'dictionary.json');
  if (!fs.existsSync(f)) { console.log('[EVA] dictionary.json lipsește — dicționarul e gol (rulează generarea).'); return; }
  try {
    const entries = JSON.parse(fs.readFileSync(f, 'utf8'));
    const r = await db.seedDictionary(entries);
    console.log(`[EVA] Dicționar sincronizat în DB: ${r.oed} intrări EN (oed) + ${r.dex} RO (dex).`);
  } catch (e) { console.error('[EVA] dictionary.json invalid:', e.message); }
}
/** Atașează la fiecare cuvânt de vocabular definițiile EN(OED)/RO(DEX) din tabele. */
async function enrichUnitsWithDict() {
  let map = {};
  try { map = await db.dictEnrichMap(); } catch { map = {}; }
  for (const u of unitsCache.values()) {
    for (const v of (u.vocab || [])) {
      const d = map[String(v.en || '').trim().toLowerCase()];
      if (d) { v.defEn = d.defEn; v.exEn = d.exEn; v.posEn = d.posEn; v.defRo = d.defRo; v.exRo = d.exRo; v.roWord = d.roWord; }
    }
  }
}

function printBanner() {
  const n = loadUnits().size;
  console.log('╔══════════════════════════════════════════════╗');
  console.log('║  EVA — English Voice Assistant · Prototip    ║');
  console.log('╚══════════════════════════════════════════════╝');
  console.log(`  Local:   ${SCHEME}://127.0.0.1:${PORT}`);
  if (LAN_MODE) {
    const ips = lanIPs();
    if (ips.length) ips.forEach((ip) => console.log(`  În LAN:  ${SCHEME}://${ip}:${PORT}   (deschide de pe alt dispozitiv)`));
    else console.log('  În LAN:  (nu am găsit un IP de rețea)');
    console.log('  ⚠ Mod LAN activ — oricine din rețea poate accesa aplicația.');
  } else {
    console.log('  (doar local · pentru LAN pornește EVA-LAN.bat)');
  }
  if (SCHEME === 'https') console.log('  🔒 HTTPS activ (certificat propriu) — pe telefon acceptă avertismentul „Nesigur". Microfonul va merge.');
  else if (LAN_MODE) console.log('  ℹ Pentru MICROFON pe telefon: pornește EVA-LAN-HTTPS.bat (necesită Gen-Cert.bat o dată).');
  console.log(`  Unități încărcate: ${n}${n === 0 ? '  (⚠ verifică seed-ul de conținut!)' : ''}`);
  const cfg = loadConfig();
  const prov = PROVIDERS[cfg.provider] || PROVIDERS.demo;
  console.log(`  Provider: ${prov.label}${prov.base ? ' → ' + prov.base : ''}`);
  console.log(`  Mod: ${isLive(cfg) ? 'LIVE' : 'DEMO (răspunsuri din lecție)'} · schimbă din ⚙ Setări`);
}

async function start() {
  console.log('[EVA] Conectare la PostgreSQL…');
  await db.connect();
  await db.init();
  // seed conținut: la prima pornire (tabel gol) sau la fiecare pornire dacă EVA_SEED_CONTENT != 0 (implicit).
  const reseed = process.env.EVA_SEED_CONTENT !== '0';
  if (reseed || (await db.countUnits()) === 0) {
    const n = await seedContentFromJson();
    console.log(`[EVA] Conținut sincronizat în DB: ${n} unități.`);
  }
  await seedDefaultUser();
  await db.pruneSessions(Date.now() - SESSION_MAX_MS); // curăță sesiunile expirate
  settingsCache = validateSettings(await db.getSettings());
  await db.saveSettings(settingsCache); // asigură existența rândului de settings
  await seedDictionaryFromJson();       // populează oed/dex din content/dictionary.json
  buildModuleTitles();                   // titluri module (A1 + A2–C2)
  await refreshContentCache();
  await enrichUnitsWithDict();           // atașează definițiile EN/RO la vocabular

  server.listen(PORT, HOST, printBanner);
}

// oprire curată (Docker stop / Ctrl+C)
function shutdown() {
  server.close(() => { db.end().finally(() => process.exit(0)); });
  setTimeout(() => process.exit(0), 4000).unref();
}
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// Pornire doar când e rulat direct (nu la require din teste).
if (require.main === module) {
  start().catch((e) => {
    console.error('[EVA] Pornire eșuată:', e && e.message ? e.message : e);
    process.exit(1);
  });
}

module.exports = { handler, start, server };
