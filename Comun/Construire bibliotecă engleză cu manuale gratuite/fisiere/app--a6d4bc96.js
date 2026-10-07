/* app.js — EVA · English Voice Assistant
 * UI tip MESSENGER, un singur pas pe ecran (foolproof): „Pasul X din N", progres,
 * corecte/greșite, o singură acțiune de învățare + buton de ieșire.
 * Router: #/ (meniu unități) · #/unit/<COD> (parcurgere liniară, reia de unde ai rămas)
 */
(function () {
  'use strict';
  const $ = (sel, el = document) => el.querySelector(sel);
  const app = $('#app');
  const escapeHtml = (s) => MD.esc(s);

  const S = {
    unitsIndex: [],
    units: {},
    config: { hasKey: false, model: '', effort: 'low', demo: true, providers: [], provider: 'demo', providerLabel: '' },
    user: null, // { email, name } — setat după autentificare
    authCfg: { googleClientId: '', facebookAppId: '' },
    moduleTitles: {}, // {A1:{1:'…'}, A2:{…}, …}
    navToken: 0,
    busy: false,
  };

  // emoji „ilustrativ" per unitate (poze la nivel de prototip)
  const UNIT_EMOJI = {
    'A1-U01': '👋', 'A1-U02': '🧑', 'A1-U03': '🔤', 'A1-U04': '👉',
    'A1-U05': '👨‍👩‍👧', 'A1-U06': '🔢', 'A1-U07': '🕐', 'A1-U08': '☀️',
    'A1-U09': '💼', 'A1-U10': '🏠', 'A1-U11': '🍎', 'A1-U12': '🛒',
    'A1-U13': '👕', 'A1-U14': '🌦️', 'A1-U15': '🏙️', 'A1-U16': '🗺️', 'A1-U17': '🚌',
    'A1-U18': '🚗', 'A1-U19': '💻', 'A1-U20': '📞', 'A1-U21': '✉️', 'A1-U22': '🧹',
    'A1-U23': '👀', 'A1-U24': '😊', 'A1-U25': '❤️', 'A1-U26': '⚽', 'A1-U27': '🎵',
    'A1-U28': '🏊', 'A1-U29': '🙋', 'A1-U30': '📚', 'A1-U31': '🏢', 'A1-U32': '📅',
    'A1-U33': '👟', 'A1-U34': '🖼️', 'A1-U35': '🏡', 'A1-U36': '📦', 'A1-U37': '🎉',
    'A1-U38': '🍳', 'A1-U39': '🥗', 'A1-U40': '🥛', 'A1-U41': '🍽️', 'A1-U42': '☕',
    'A1-U43': '🤒', 'A1-U44': '🩺', 'A1-U45': '💊', 'A1-U46': '🦷', 'A1-U47': '🚨',
    'A1-U48': '🏨', 'A1-U49': '✈️', 'A1-U50': '🧳', 'A1-U51': '🚆', 'A1-U52': '📮',
    'A1-U53': '📍', 'A1-U54': '🗓️', 'A1-U55': '🏃', 'A1-U56': '📖', 'A1-U57': '👶',
    'A1-U58': '🧭', 'A1-U59': '😲', 'A1-U60': '📰', 'A1-U61': '🕵️', 'A1-U62': '📸',
    'A1-U63': '🔮', 'A1-U64': '📆', 'A1-U65': '🤖', 'A1-U66': '🌱', 'A1-U67': '🏆',
    'A1-U68': '🌍', 'A1-U69': '🚙', 'A1-U70': '💡', 'A1-U71': '📋', 'A1-U72': '🌟',
  };
  const emojiOf = (code) => UNIT_EMOJI[code] || '📗';
  const MODULE_TITLES = {
    1: 'A1.1 — Primii pași', 2: 'A1.2 — Viața de zi cu zi', 3: 'A1.3 — Oameni, abilități și activități',
    4: 'A1.4 — Acțiuni care se petrec acum', 5: 'A1.5 — Sănătate, servicii și situații practice',
    6: 'A1.6 — Trecutul', 7: 'A1.7 — Viitor, comparații și conversații mai complexe',
  };

  // ---------- persistență ----------
  // device-level (rămâne local pe dispozitiv): preferințe TTS/voce
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { localStorage.setItem(k, JSON.stringify(v)); },
  };
  // user-level (persistat în PostgreSQL prin /api/state): progres, chat, SRS.
  // Cache în memorie, umplut la login; scrierile merg imediat la server (write-through).
  let remoteState = {};
  const ustore = {
    get(k, d) { return Object.prototype.hasOwnProperty.call(remoteState, k) ? remoteState[k] : d; },
    set(k, v) { remoteState[k] = v; API.stateSet(k, v).catch(() => {}); },
  };
  // expus pentru srs.js (care persistă tot prin acest store)
  window.EVA_USTORE = ustore;
  async function loadUserState() {
    try { remoteState = (await API.state()) || {}; } catch { remoteState = {}; }
  }
  const progKey = (code) => `prog.${code}`;
  const getProg = (code) => ustore.get(progKey(code), { i: 0, total: 0, correct: 0, wrong: 0, done: false });
  const setProg = (code, p) => ustore.set(progKey(code), p);
  const autoTts = () => store.get('eva.autoTts', true);

  // =========================================================================
  //  MENIU (acasă) — o singură alegere: ce unitate începi · + ⚙️ · fără altceva
  // =========================================================================
  const LEVEL_ORDER = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
  const LEVEL_META = {
    A1: { emoji: '🌱', name: 'Începător absolut' }, A2: { emoji: '🌿', name: 'Elementar' },
    B1: { emoji: '🌳', name: 'Intermediar' }, B2: { emoji: '🏔️', name: 'Intermediar-avansat' },
    C1: { emoji: '🚀', name: 'Avansat' }, C2: { emoji: '🏆', name: 'Măiestrie' },
  };
  const cardHtml = (u) => {
    const p = getProg(u.code);
    const pct = p.total ? Math.round((p.i / Math.max(1, p.total - 1)) * 100) : 0;
    const state = p.done ? 'Terminat ✓' : p.total ? `${pct}% · pasul ${p.i + 1}/${p.total}` : 'Neînceput';
    return `<button class="big-card" data-open="${escapeHtml(u.code)}">
      <div class="big-emoji" aria-hidden="true">${emojiOf(u.code)}</div>
      <div class="big-meta">
        <div class="big-t">${escapeHtml(u.title)}</div>
        <div class="big-s">${escapeHtml(u.titleRo || '')}</div>
        <div class="big-bar"><i style="width:${pct}%"></i></div>
        <div class="big-state ${p.done ? 'ok' : ''}">${state}</div>
      </div>
      <div class="big-go">${p.done ? '↺' : '▶'}</div>
    </button>`;
  };

  // MENIU: carduri de NIVEL (A1 … C2)
  function viewHome() {
    VOICE.stopSpeaking();
    const byLevel = {};
    S.unitsIndex.forEach((u) => { const L = u.level || 'A1'; (byLevel[L] = byLevel[L] || []).push(u); });
    const levels = LEVEL_ORDER.filter((L) => byLevel[L]);
    const cards = levels.map((L) => {
      const list = byLevel[L];
      const done = list.filter((u) => getProg(u.code).done).length;
      const pct = Math.round((done / list.length) * 100);
      const meta = LEVEL_META[L] || { emoji: '📗', name: '' };
      return `<button class="big-card level-card" data-level="${L}">
        <div class="big-emoji" aria-hidden="true">${meta.emoji}</div>
        <div class="big-meta">
          <div class="big-t">Nivel ${L}</div>
          <div class="big-s">${escapeHtml(meta.name)}</div>
          <div class="big-bar"><i style="width:${pct}%"></i></div>
          <div class="big-state ${done === list.length ? 'ok' : ''}">${done}/${list.length} unități</div>
        </div>
        <div class="big-go">▶</div>
      </button>`;
    }).join('');
    app.innerHTML = `
      ${topbarHtml()}
      <main class="home">
        <section class="hero-card">
          <h1>Bună, ${escapeHtml((S.user && S.user.name) || '')}! 👋 Alege un nivel.</h1>
          <p>Fiecare nivel are mai multe module, iar fiecare modul mai multe lecții. Alege de unde pornești. 👇</p>
        </section>
        <div class="modules">${cards}</div>
        <p class="hint" style="text-align:center">${S.config.demo
          ? 'Mod demo (fără AI). Din ⚙️ poți alege <b>Qwen local</b> sau <b>Claude</b>.'
          : 'Motor AI: <b>' + escapeHtml(S.config.providerLabel || shortProvider()) + '</b>'}</p>
      </main>`;
    wireTopbar(app);
    app.querySelectorAll('[data-level]').forEach((b) => b.addEventListener('click', () => { location.hash = '#/level/' + b.dataset.level; }));
  }

  // NIVEL: modulele nivelului, cu lecțiile grupate
  function viewLevel(lvl) {
    VOICE.stopSpeaking();
    const list = S.unitsIndex.filter((u) => (u.level || 'A1') === lvl);
    if (!list.length) { location.hash = '#/'; return; }
    const titles = (S.moduleTitles && S.moduleTitles[lvl]) || {};
    const byModule = {};
    list.forEach((u) => { const m = u.module || 1; (byModule[m] = byModule[m] || []).push(u); });
    const cards = Object.keys(byModule).sort((a, b) => a - b).map((m) => {
      const ml = byModule[m];
      const done = ml.filter((u) => getProg(u.code).done).length;
      return `<section class="module-block">
        <h2 class="module-h"><span>${escapeHtml(titles[m] || (lvl + '.' + m))}</span>
          <span class="module-count ${done === ml.length ? 'ok' : ''}">${done}/${ml.length}</span></h2>
        <div class="cards">${ml.map(cardHtml).join('')}</div>
      </section>`;
    }).join('');
    const doneAll = list.filter((u) => getProg(u.code).done).length;
    app.innerHTML = `
      ${topbarHtml()}
      <main class="home">
        <section class="hero-card">
          <button class="btn ghost lvl-back" id="backLevels">◀ Toate nivelele</button>
          <h1>${LEVEL_META[lvl] ? LEVEL_META[lvl].emoji : ''} Nivel ${escapeHtml(lvl)}</h1>
          <div class="hero-stats"><span class="hstat">✅ ${doneAll}/${list.length} lecții terminate</span></div>
        </section>
        <div class="modules">${cards}</div>
      </main>`;
    wireTopbar(app);
    $('#backLevels', app).addEventListener('click', () => { location.hash = '#/'; });
    app.querySelectorAll('[data-open]').forEach((b) => b.addEventListener('click', () => { location.hash = '#/unit/' + encodeURIComponent(b.dataset.open); }));
  }
  function shortProvider() { return String(S.config.providerLabel || '').replace(/\s*\(.*$/, '').trim() || 'AI'; }

  // ===== Carnet de note (progres pe module + cel mai bun scor la teste) =====
  function scoreCell(pct) { const cls = pct >= 80 ? 'ok' : pct >= 50 ? 'mid' : 'low'; return `<span class="gr-score ${cls}">${pct}%</span>`; }
  function viewGrades() {
    VOICE.stopSpeaking();
    const byLevel = {};
    S.unitsIndex.forEach((u) => { const L = u.level || 'A1'; (byLevel[L] = byLevel[L] || {}); const m = u.module || 1; (byLevel[L][m] = byLevel[L][m] || []).push(u); });
    const levels = LEVEL_ORDER.filter((L) => byLevel[L]);
    const sections = levels.map((L) => {
      const titles = (S.moduleTitles && S.moduleTitles[L]) || {};
      const mods = Object.keys(byLevel[L]).sort((a, b) => a - b);
      let lvlDone = 0, lvlTotal = 0;
      const modBlocks = mods.map((m) => {
        const list = byLevel[L][m];
        const done = list.filter((u) => getProg(u.code).done).length;
        lvlDone += done; lvlTotal += list.length;
        const pct = Math.round((done / list.length) * 100);
        const rows = list.map((u) => {
          const p = getProg(u.code);
          const tb = (p.testBest != null) ? scoreCell(p.testBest) : '—';
          const matches = p.match ? Object.values(p.match) : [];
          const mAvg = matches.length ? scoreCell(Math.round(matches.reduce((a, b) => a + b, 0) / matches.length)) : '—';
          return `<tr class="${p.done ? 'gr-done' : ''}">
            <td class="gr-u">${escapeHtml(u.code)} · ${escapeHtml(u.title)}</td>
            <td class="gr-c">${p.done ? '✓' : '·'}</td>
            <td class="gr-c">${tb}</td>
            <td class="gr-c">${mAvg}</td></tr>`;
        }).join('');
        return `<details class="gr-module"${pct > 0 ? ' open' : ''}>
          <summary><span class="gr-mtitle">${escapeHtml(titles[m] || (L + '.' + m))}</span>
            <span class="gr-mprog ${done === list.length ? 'ok' : ''}">${done}/${list.length} = ${pct}%</span></summary>
          <table class="gr-table"><thead><tr><th>Lecție</th><th>✔</th><th>Test</th><th>Echiv.</th></tr></thead><tbody>${rows}</tbody></table>
        </details>`;
      }).join('');
      const lpct = lvlTotal ? Math.round((lvlDone / lvlTotal) * 100) : 0;
      return `<section class="gr-level">
        <h2 class="gr-lh">${LEVEL_META[L] ? LEVEL_META[L].emoji : ''} Nivel ${escapeHtml(L)}
          <span class="gr-lprog ${lvlDone === lvlTotal ? 'ok' : ''}">${lvlDone}/${lvlTotal} = ${lpct}%</span></h2>
        ${modBlocks}</section>`;
    }).join('');
    app.innerHTML = `
      ${topbarHtml()}
      <main class="home">
        <section class="hero-card">
          <button class="btn ghost lvl-back" id="grBack">◀ Meniu</button>
          <h1>📒 Carnet de note</h1>
          <p>Progresul pe capitole și subcapitole + cel mai bun scor la teste (inclusiv reluările).</p>
        </section>
        ${sections}
      </main>`;
    wireTopbar(app);
    $('#grBack', app).addEventListener('click', () => { location.hash = '#/'; });
  }

  // Antet global (logo + provider + user + logout + setări) — folosit peste tot.
  function topbarHtml() {
    const mode = S.config && S.config.demo
      ? '<span class="badge-demo">MOD DEMO</span>'
      : (S.config && (S.config.providerLabel || S.config.provider))
        ? `<span class="badge-live" title="${escapeHtml(S.config.providerLabel || '')}">${escapeHtml(shortProvider())}</span>` : '';
    const userBits = S.user
      ? `<span class="user-chip" title="${escapeHtml(S.user.email)}">👤 ${escapeHtml(S.user.name)}</span>
         <button class="iconbtn" id="gradesBtn" title="Carnet de note" aria-label="Carnet de note">📒</button>
         <button class="iconbtn" id="logoutBtn" title="Ieși din cont" aria-label="Ieși din cont">⎋</button>
         <button class="iconbtn" id="openSettings" title="Setări" aria-label="Setări">⚙️</button>`
      : '';
    return `<header class="topbar">
      <button class="brand brand-btn" id="brandHome" title="Meniu" aria-label="Meniu principal">
        <div class="logo">EVA</div>
        <div><div class="t">EVA</div><div class="s">Învață engleză pas cu pas</div></div>
      </button>
      <div class="spacer"></div>
      ${mode}
      ${userBits}
    </header>`;
  }
  function wireTopbar(root = document) {
    root.querySelector('#openSettings')?.addEventListener('click', openSettings);
    root.querySelector('#gradesBtn')?.addEventListener('click', () => { VOICE.stopSpeaking(); location.hash = '#/grades'; });
    root.querySelector('#logoutBtn')?.addEventListener('click', doLogout);
    root.querySelector('#brandHome')?.addEventListener('click', () => {
      if (S.user) { VOICE.stopSpeaking(); VOICE.stopListening(); location.hash = '#/'; }
    });
  }

  // =========================================================================
  //  PARCURGERE LINIARĂ (wizard tip messenger)
  // =========================================================================
  const P = { unit: null, steps: [], i: 0 };
  let _lastActivitySig = ''; // evită logări duplicate de istoric pe re-randări identice

  function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  // reacții audio scurte, VARIATE, în engleză — obișnuiesc elevul cu limba (textul scris rămâne în română)
  const PRAISE_EN = ["Perfect! You're the best!", "Excellent! Well done!", "Great job!", "Awesome! Keep it up!", "Brilliant! That's correct!", "Wonderful! You nailed it!", "Fantastic! Right on!", "Amazing! You've got it!", "Superb! Keep going!", "Very good! You're improving!", "Yes! That's right!", "Nice work! You're a star!"];
  const ENCOURAGE_EN = ["Wrong. Please try again.", "Sorry, you can do better.", "Not quite. Try once more.", "Almost! Give it another go.", "Oops! Try again.", "Close! One more time.", "Don't worry. Try again.", "Keep trying, you can do it!", "Not yet. Try again, please.", "Nice try! Once more.", "Hmm, not exactly. Try again.", "Take your time and try again."];
  const speakReact = (good) => { const a = good ? PRAISE_EN : ENCOURAGE_EN; VOICE.speak(a[Math.floor(Math.random() * a.length)], { rate: 0.95 }); };

  function buildSteps(u) {
    const steps = [{ type: 'intro' }];
    const vocab = u.vocab || [];
    let chunk = [];
    vocab.forEach((_, wi) => {
      steps.push({ type: 'vocab', wi, k: wi + 1, total: vocab.length });
      chunk.push(wi);
      // test de echivalare auditivă după fiecare 10 cuvinte
      if (chunk.length === 10) { steps.push({ type: 'match', group: chunk.slice() }); chunk = []; }
    });
    if (chunk.length >= 4) steps.push({ type: 'match', group: chunk.slice() }); // restul, dacă e substanțial
    if (u.dialogue?.lines?.length) steps.push({ type: 'dialogue' });
    if (u.grammarNoteRo) steps.push({ type: 'grammar' });
    if (u.listening?.script) steps.push({ type: 'listen' });
    (u.pronunciation?.targets || []).forEach((_, ti) => steps.push({ type: 'pron', ti }));
    if (u.exercisesMd) steps.push({ type: 'practice' });
    steps.push({ type: 'chat' });
    const items = u.test?.items || [];
    if (items.length) {
      steps.push({ type: 'testIntro', n: items.length });
      items.forEach((_, ti) => steps.push({ type: 'testItem', ti }));
      steps.push({ type: 'testResult' });
    }
    steps.push({ type: 'done' });
    return steps;
  }

  async function startUnit(code) {
    const myNav = ++S.navToken;
    VOICE.stopSpeaking(); VOICE.stopListening();
    if (!S.units[code]) {
      app.innerHTML = `<div class="boot"><div class="boot-logo">EVA</div><p>Se încarcă…</p></div>`;
      let data;
      try { data = await API.unit(code); } catch { app.innerHTML = errScreen('Nu găsesc lecția.'); return; }
      if (myNav !== S.navToken) return;
      S.units[code] = data;
      SRS.seed(code, data.srs);
    }
    if (myNav !== S.navToken) return;
    P.unit = S.units[code];
    P.steps = buildSteps(P.unit);
    const prog = getProg(code);
    // reia de unde a rămas (dar nu pe un pas dispărut)
    P.i = Math.min(Math.max(0, prog.i || 0), P.steps.length - 1);
    prog.total = P.steps.length;
    setProg(code, prog);
    playStep();
  }

  function saveI() { const p = getProg(P.unit.code); p.i = P.i; p.total = P.steps.length; setProg(P.unit.code, p); }
  function scoreCounts() {
    const ta = getProg(P.unit.code).testAnswers || {};
    const vals = Object.values(ta);
    const correct = vals.filter(Boolean).length;
    return { correct, wrong: vals.length - correct, answered: vals.length };
  }

  function next() {
    if (P.i < P.steps.length - 1) { P.i++; saveI(); playStep(); }
    else { location.hash = '#/'; }
  }
  function prev() { if (P.i > 0) { P.i--; saveI(); playStep(); } }

  // structura de pagină: antet (ieșire + progres + scor) · corp · o singură acțiune · Înapoi/Continuă
  function frame(bodyHtml, opts = {}) {
    const u = P.unit;
    const n = P.steps.length;
    const pct = Math.round((P.i / Math.max(1, n - 1)) * 100);
    const sc = scoreCounts();
    const score = sc.answered
      ? `<div class="wiz-score"><span class="ok">✓ ${sc.correct}</span> <span class="no">✗ ${sc.wrong}</span></div>` : '';
    const showBack = P.i > 0;
    app.innerHTML = `
      ${topbarHtml()}
      <header class="wiz-top">
        <button class="wiz-exit" id="wizExit" title="Ieși din lecție" aria-label="Ieși din lecție">✕</button>
        <div class="wiz-progwrap">
          <div class="wiz-steplbl">${escapeHtml(u.code)} · Pasul ${P.i + 1} din ${n}</div>
          <div class="wiz-bar"><i style="width:${pct}%"></i></div>
        </div>
        ${score}
      </header>
      <main class="wiz-body" id="wizbody">${bodyHtml}</main>
      ${(opts.action || showBack) ? `<footer class="wiz-foot">
        ${showBack ? '<button class="wiz-back" id="wizBack" aria-label="Pasul anterior">◀ Înapoi</button>' : ''}
        ${opts.action ? `<button class="wiz-next" id="wizNext">${opts.action}</button>` : ''}
      </footer>` : ''}`;
    wireTopbar(app);
    $('#wizExit').addEventListener('click', () => { location.hash = '#/'; });
    $('#wizBack')?.addEventListener('click', () => prev());
    if (opts.action && !opts.holdNext) $('#wizNext').addEventListener('click', () => next());
    return $('#wizbody');
  }
  function updateHeaderScore() {
    const sc = scoreCounts();
    if (!sc.answered) return;
    const html = `<span class="ok">✓ ${sc.correct}</span> <span class="no">✗ ${sc.wrong}</span>`;
    const el = $('.wiz-score');
    if (el) el.innerHTML = html; else $('.wiz-top')?.insertAdjacentHTML('beforeend', `<div class="wiz-score">${html}</div>`);
  }

  // bulă EVA cu instrucțiune simplă (RO) + emoji-ghid
  function evaSay(text, emoji) {
    return `<div class="eva-guide"><div class="eva-ava" aria-hidden="true">${emoji || '🐢'}</div>
      <div class="eva-bubble">${text}</div></div>`;
  }

  function playStep() {
    VOICE.stopSpeaking(); VOICE.stopListening();
    const st = P.steps[P.i];
    (RENDER[st.type] || RENDER.done)(st);
    saveI();
  }

  // buton play/stop real (apeși din nou = oprește, nu reia de la zero)
  let activeToggle = null;
  function wirePlayToggle(btn, start, playLabel, stopLabel) {
    if (!btn) return;
    btn._reset = () => { btn.innerHTML = playLabel; if (activeToggle === btn) activeToggle = null; };
    btn.addEventListener('click', () => {
      if (activeToggle === btn) { VOICE.stopSpeaking(); btn._reset(); return; }
      if (activeToggle) { VOICE.stopSpeaking(); activeToggle._reset(); }
      activeToggle = btn; btn.innerHTML = stopLabel;
      start(() => { if (activeToggle === btn) btn._reset(); });
    });
  }
  // indiciu corect în funcție de sistemul de operare al dispozitivului
  function osHint() {
    const ua = navigator.userAgent || '';
    if (/Android/i.test(ua)) return 'Pe <b>Android</b>: Setări → Accesibilitate → <b>Text-to-speech</b> (motorul Google) → instalează limba <b>Română</b>.';
    if (/iPhone|iPad|iPod/i.test(ua)) return 'Pe <b>iPhone/iPad</b>: Setări → Accesibilitate → Conținut vorbit → Voci → adaugă <b>Română</b>.';
    if (/Windows/i.test(ua)) return 'Pe <b>Windows</b>: Setări → Oră și limbă → Limbă → Română → Opțiuni → adaugă pachetul de <b>voce</b>.';
    if (/Macintosh|Mac OS X/i.test(ua)) return 'Pe <b>Mac</b>: Setări → Accesibilitate → Conținut vorbit → adaugă voce <b>Română</b>.';
    if (/Linux/i.test(ua)) return 'Pe <b>Linux</b>: instalează <code>speech-dispatcher</code> + o voce românească (ex. espeak-ng ro).';
    return 'Instalează o voce <b>ro-RO</b> în setările sistemului tău de operare.';
  }

  // ---------- randări per pas ----------
  const RENDER = {
    intro(st) {
      const u = P.unit;
      const intro = u.intro || {};
      const goals = (intro.goals && intro.goals.length) ? intro.goals : (u.objectives || []).map((o) => ({ ro: o.canDo, en: '' }));
      const roText = intro.ro || `În această lecție „${u.title}" vei învăța lucruri noi și utile.`;
      const enText = intro.en || '';
      const goalsHtml = goals.map((g) => `<li>✅ ${escapeHtml(g.ro)}</li>`).join('');
      const host = frame(
        `<div class="big-hero-emoji">${emojiOf(u.code)}</div>
         ${evaSay(`Bună! 👋 Sunt <b>EVA</b>.<br>${escapeHtml(roText)}`, '🐢')}
         <div class="playrow">
           <button class="btn solid" id="listenRo">🔊 Ascultă în română</button>
           <button class="btn ghost" id="listenEn">🔊 Listen in English</button>
         </div>
         <div class="notice" id="roTip"></div>
         <div class="card"><b>Ce vei putea face:</b><ul class="intro-obj">${goalsHtml}</ul></div>
         ${evaSay('Sunt <b>' + P.steps.length + '</b> pași scurți. Poți merge <b>înainte</b> și <b>înapoi</b>, și ieși oricând (✕) — progresul se salvează. 💾', '👇')}`,
        { action: 'Începem! ▶' });
      const roSeq = [{ text: roText, lang: 'ro' }, ...goals.map((g) => ({ text: g.ro, lang: 'ro' }))];
      const enSeq = [{ text: enText, lang: 'en' }, ...goals.map((g) => ({ text: g.en, lang: 'en' }))].filter((x) => x.text);
      wirePlayToggle($('#listenRo', host), (onend) => {
        if (!VOICE.roSupported()) $('#roTip', host).innerHTML = '🔈 Nu găsesc o voce <b>românească</b> pe acest dispozitiv. ' + osHint() + ' <br>(Engleza merge oricum.)';
        else $('#roTip', host).textContent = '';
        VOICE.speakSequence(roSeq, { onend });
      }, '🔊 Ascultă în română', '⏹ Oprește');
      wirePlayToggle($('#listenEn', host), (onend) => VOICE.speakSequence(enSeq, { onend }), '🔊 Listen in English', '⏹ Stop');
    },

    vocab(st) {
      const u = P.unit; const th = u.pronunciation?.threshold || 80;
      const v = (u.vocab || [])[st.wi] || { en: '', ipa: '', ro: '' };
      const prog = getProg(u.code); const best = (prog.vocab && prog.vocab[v.en]);
      const hasEn = !!(v.defEn && String(v.defEn).trim());
      const hasRo = !!(v.defRo && String(v.defRo).trim());
      const posEn = v.posEn ? ` · <span class="pos">${escapeHtml(v.posEn)}</span>` : '';
      const explain = `
        <div class="metro-explain">
          <div class="explain-h">📖 Explicații <span class="explain-note">apasă ca să le auzi</span></div>
          <button class="explain-tile en" id="expEn" ${hasEn ? '' : 'disabled'} title="Ascultă explicația în engleză">
            <div class="explain-lang">🇬🇧 English (OED)${posEn}<span class="explain-play">🔊</span></div>
            <div class="explain-def">${hasEn ? escapeHtml(v.defEn) : '<i>Definiție în curs de generare…</i>'}</div>
            ${v.exEn ? `<div class="explain-ex">„${escapeHtml(v.exEn)}"</div>` : ''}
          </button>
          <button class="explain-tile ro" id="expRo" ${hasRo ? '' : 'disabled'} title="Ascultă explicația în română">
            <div class="explain-lang">🇷🇴 Română (DEX)<span class="explain-play">🔊</span></div>
            <div class="explain-def">${hasRo ? escapeHtml(v.defRo) : '<i>Definiție în curs de generare…</i>'}</div>
            ${v.exRo ? `<div class="explain-ex">„${escapeHtml(v.exRo)}"</div>` : ''}
          </button>
        </div>`;
      const host = frame(
        `${evaSay(`Cuvântul <b>${st.k} din ${st.total}</b>. Ascultă 🔊, <b>spune tu</b> 🎙️, iar în dreapta ai <b>explicațiile</b> (apasă ca să le auzi). ✅`, '🗣️')}
         <div class="metro-vocab">
           <div class="metro-word">
             <div class="word-en">${escapeHtml(v.en)}</div>
             <div class="word-ipa">${escapeHtml(v.ipa || '')}</div>
             <div class="word-ro">${escapeHtml(v.ro)}</div>
             <div class="word-actions">
               <button class="btn solid big" id="wsay">🔊 Ascultă</button>
               ${VOICE.sttSupported ? '<button class="btn coral big" id="wtry">🎙️ Spune tu</button>' : ''}
             </div>
             ${VOICE.sttSupported ? '' : `<div class="selfcheck">
               <p class="hint">🔊 Ascultă, apoi <b>spune cuvântul cu voce tare</b>. Ai reușit?</p>
               <div class="sc-row"><button class="btn ghost" id="wretry">🔁 Mai exersez</button><button class="btn coral" id="wgot">✅ Am reușit</button></div>
             </div>`}
             <div class="word-fb" id="wfb">${best != null ? wordBadge(best, th) : ''}</div>
           </div>
           ${explain}
         </div>`,
        { action: st.k < st.total ? 'Următorul cuvânt →' : 'Continuă →' });

      const fb = $('#wfb', host);
      const wsay = $('#wsay', host), wtry = $('#wtry', host), expEn = $('#expEn', host), expRo = $('#expRo', host);
      // coordonare audio: o singură activitate odată; explicațiile sunt inactive cât timp merge alt audio
      const audioBtns = [wsay, wtry, expEn, expRo].filter(Boolean);
      const wtryReset = () => { if (wtry) { wtry.dataset.busy = ''; wtry.classList.remove('rec'); wtry.innerHTML = '🎙️ Spune tu'; } };
      let activeAudio = null;
      const lock = (active) => { activeAudio = active; audioBtns.forEach((b) => { if (b !== active) b.disabled = true; }); };
      const unlock = () => {
        activeAudio = null; wtryReset();
        audioBtns.forEach((b) => { b.disabled = false; });
        if (expEn && !hasEn) expEn.disabled = true;
        if (expRo && !hasRo) expRo.disabled = true;
      };

      // „Ascultă" cuvântul (start/stop, voce EN)
      wsay?.addEventListener('click', () => {
        if (activeAudio === wsay) { VOICE.stopSpeaking(); wsay.innerHTML = '🔊 Ascultă'; unlock(); return; }
        if (activeAudio) return;
        lock(wsay); wsay.innerHTML = '⏹ Oprește';
        VOICE.speak(v.en, { rate: 0.8, onend: () => { wsay.innerHTML = '🔊 Ascultă'; unlock(); } });
      });

      // explicații = butoane care CITESC conținutul (EN în engleză, RO în română)
      const wireExplain = (btn, text, lang) => {
        if (!btn) return;
        btn.addEventListener('click', () => {
          if (btn.disabled) return;
          if (activeAudio === btn) { VOICE.stopSpeaking(); btn.classList.remove('reading'); unlock(); return; }
          if (activeAudio) return;
          lock(btn); btn.classList.add('reading');
          const done = () => { btn.classList.remove('reading'); unlock(); };
          if (lang === 'ro') VOICE.speakRo(text, { onend: done });
          else VOICE.speak(text, { rate: 0.9, onend: done });
        });
      };
      wireExplain(expEn, [v.defEn, v.exEn].filter(Boolean).join('. '), 'en');
      wireExplain(expRo, [v.defRo, v.exRo].filter(Boolean).join('. '), 'ro');

      // validare la microfon (Chrome/Edge desktop/Android)
      wtry?.addEventListener('click', () => {
        if (wtry.dataset.busy === '1') { VOICE.stopListening(); return; } // a doua apăsare = oprește
        if (activeAudio && activeAudio !== wtry) return;
        VOICE.stopSpeaking();
        wtry.dataset.busy = '1'; wtry.classList.add('rec'); wtry.innerHTML = '🔴 Ascult… (apasă să opresc)';
        lock(wtry);
        fb.innerHTML = `🎙️ Spune acum: „${escapeHtml(v.en)}"…`;
        VOICE.listen({
          onresult: (text, alts) => {
            const score = VOICE.scoreAgainst(v.en, alts);
            const p = getProg(u.code); p.vocab = p.vocab || {}; p.vocab[v.en] = Math.max(p.vocab[v.en] || 0, score); setProg(u.code, p);
            const good = score >= th;
            fb.innerHTML = `<div class="wtry-res ${good ? 'ok' : 'bad'}">${good ? '✅ Corect! Bravo!' : '🔁 Aproape — mai încearcă'}<br><span class="wtry-heard">am auzit: „${escapeHtml(text)}" · scor ${score}</span></div>`;
            setTimeout(() => speakReact(good), 250); // reacție audio VARIATĂ în engleză (după eliberarea microfonului)
          },
          onerror: (m) => { fb.innerHTML = `<span class="hint">${escapeHtml(m)}</span>`; },
          onend: () => { unlock(); },
        });
      });
      // autoevaluare (iPhone/iPad)
      $('#wgot', host)?.addEventListener('click', () => {
        const p = getProg(u.code); p.vocab = p.vocab || {}; p.vocab[v.en] = 100; setProg(u.code, p);
        fb.innerHTML = `<div class="wtry-res ok">✅ Bravo! Marcat ca știut.</div>`;
        speakReact(true);
      });
      $('#wretry', host)?.addEventListener('click', () => {
        fb.innerHTML = `<div class="wtry-res bad">🔁 Ascultă din nou și mai spune-l o dată. Nu te grăbi!</div>`;
        speakReact(false);
      });
    },

    // test de echivalare auditivă: auzi cuvântul EN (doar audio) și-l potrivești cu traducerea RO
    match(st) {
      const u = P.unit;
      const words = st.group.map((wi) => (u.vocab || [])[wi]).filter((w) => w && w.en && w.ro);
      const N = words.length;
      const key = 'm' + st.group[0]; // cheia grupului pt. scor
      const numToWord = shuffle(words.map((_, i) => i)); // numToWord[num-1] = index în words (audio EN)
      const roOrder = shuffle(words.map((_, i) => i));    // roOrder[j] = index în words (scris RO)
      const assign = {};   // num(1..N) -> j
      const roToNum = {};  // j -> num
      let active = null, scored = false;

      const leftHtml = numToWord.map((_, k) => `<button class="mt-num" data-num="${k + 1}" aria-label="Ascultă cuvântul ${k + 1}">🔊 <b>${k + 1}</b></button>`).join('');
      const rightHtml = roOrder.map((wIdx, j) => `<button class="mt-ro" data-j="${j}"><span class="mt-badge" id="mtb${j}"></span><span class="mt-ro-txt">${escapeHtml(words[wIdx].ro)}</span></button>`).join('');

      const host = frame(
        `${evaSay(`🎧 <b>Test de echivalare</b>. Apasă un <b>număr</b> (stânga) → auzi cuvântul în engleză (fără să-l vezi scris) → apasă <b>traducerea</b> potrivită (dreapta). Numărul apare în dreptul ei. Poți corecta reapăsând numărul. Când ai potrivit toate ${N}, apasă <b>Află scorul</b>.`, '🎧')}
         <div class="match-grid">
           <div class="match-col"><div class="match-h">🔊 Ascultă (EN)</div><div class="mt-nums">${leftHtml}</div></div>
           <div class="match-col"><div class="match-h">Traducerea (RO)</div><div class="mt-ros">${rightHtml}</div></div>
         </div>
         <div class="match-foot">
           <button class="btn solid big" id="mtScore" disabled>Află scorul</button>
           <div class="mt-result" id="mtResult" aria-live="polite"></div>
         </div>`,
        { action: 'Continuă →' });

      const leftBtns = [...host.querySelectorAll('.mt-num')];
      const roBtns = [...host.querySelectorAll('.mt-ro')];
      const scoreBtn = $('#mtScore', host);
      const resultEl = $('#mtResult', host);

      const refresh = () => {
        roBtns.forEach((b) => { const j = Number(b.dataset.j); $('#mtb' + j, host).textContent = roToNum[j] || ''; b.classList.toggle('assigned', roToNum[j] != null); });
        leftBtns.forEach((b) => { const num = Number(b.dataset.num); b.classList.toggle('done', assign[num] != null); b.classList.toggle('active', active === num); });
        scoreBtn.disabled = scored || Object.keys(assign).length < N;
      };
      const clearNum = (num) => { const j = assign[num]; if (j != null) { delete roToNum[j]; delete assign[num]; } };

      leftBtns.forEach((b) => b.addEventListener('click', () => {
        if (scored) return;
        const num = Number(b.dataset.num);
        if (assign[num] != null) clearNum(num); // reapăsare = corectare (eliberează)
        active = num;
        VOICE.stopSpeaking();
        VOICE.speak(words[numToWord[num - 1]].en, { rate: 0.85 });
        refresh();
      }));
      roBtns.forEach((b) => b.addEventListener('click', () => {
        if (scored) return;
        const j = Number(b.dataset.j);
        if (active == null) { if (roToNum[j] != null) { clearNum(roToNum[j]); refresh(); } return; }
        if (roToNum[j] != null) delete assign[roToNum[j]]; // RO-ul avea alt număr → îl eliberez
        if (assign[active] != null) delete roToNum[assign[active]]; // numărul era pe alt RO
        assign[active] = j; roToNum[j] = active; active = null;
        refresh();
      }));
      scoreBtn.addEventListener('click', () => {
        if (!scored) {
          let correct = 0;
          roBtns.forEach((b) => {
            const j = Number(b.dataset.j); const num = roToNum[j];
            const good = num != null && numToWord[num - 1] === roOrder[j];
            if (good) correct++;
            b.classList.add(good ? 'mt-ok' : 'mt-bad');
          });
          scored = true;
          const pct = Math.round((correct / N) * 100);
          resultEl.innerHTML = `<b>${correct}/${N}</b> corecte · ${pct}%`;
          const p = getProg(u.code); p.match = p.match || {}; p.match[key] = Math.max(p.match[key] || 0, pct); setProg(u.code, p);
          API.logActivity(u.code, 'match_result', { group: st.group[0], correct, total: N, percent: pct }).catch(() => {});
          scoreBtn.textContent = '🔁 Reia testul';
          scoreBtn.disabled = false;
        } else {
          playStep(); // reia = re-randare
        }
      });
      refresh();
    },

    dialogue(st) {
      const u = P.unit;
      const dlg = (u.dialogue.lines || []).map((l) => {
        const isEva = /eva/i.test(l.speaker);
        return `<div class="line ${isEva ? 'eva' : 'other'}"><div class="who">${escapeHtml(l.speaker)}</div>${escapeHtml(l.text)}</div>`;
      }).join('');
      const gloss = (u.dialogue.gloss || []).map((g) => `<div><b>${escapeHtml(g.en)}</b> — ${escapeHtml(g.ro)}</div>`).join('');
      const host = frame(
        `${evaSay('Ascultă și citește dialogul 💬. Apasă ▶ ca să-l auzi.', '💬')}
         <div class="playrow"><button class="btn solid" id="playDlg">▶️ Ascultă dialogul</button></div>
         <div class="dlg">${dlg}</div>
         ${gloss ? `<div class="gloss"><b>Expresii utile:</b><br>${gloss}</div>` : ''}`,
        { action: 'Continuă →' });
      const dlgScript = (u.dialogue.lines || []).map((l) => `${l.speaker}: ${l.text}`).join('\n');
      wirePlayToggle($('#playDlg', host), (onend) => VOICE.speakScript(dlgScript, { onend }), '▶️ Ascultă dialogul', '⏹ Oprește');
    },

    grammar(st) {
      const host = frame(
        `${evaSay('Un pic de gramatică 📘, explicată <b>în română</b>. Citește liniștit — apoi mergem mai departe.', '📘')}
         <div class="card">${MD.render(P.unit.grammarNoteRo)}</div>`,
        { action: 'Am înțeles →' });
    },

    listen(st) {
      const u = P.unit; const L = u.listening;
      const qs = (L.items || []).map((it, i) => `
        <div class="qa-item" id="li${i}"><div>${i + 1}. ${escapeHtml(it.q)}</div>
        <button class="rev" data-li="${i}">Arată răspunsul</button><div class="a">✔ ${escapeHtml(it.a)}</div></div>`).join('');
      const host = frame(
        `${evaSay('Ascultă cu atenție 🎧 (poți asculta de 1–2 ori), apoi verifică-ți răspunsurile.', '🎧')}
         <div class="playrow"><button class="btn solid" id="lPlay">▶️ Redă</button></div>
         <div class="qa">${qs}</div>`,
        { action: 'Continuă →' });
      wirePlayToggle($('#lPlay', host), (onend) => VOICE.speakScript(L.script, { onend }), '▶️ Redă', '⏹ Oprește');
      host.querySelectorAll('[data-li]').forEach((b) => b.addEventListener('click', () => $('#li' + b.dataset.li, host).classList.add('revealed')));
    },

    pron(st) {
      const u = P.unit; const th = u.pronunciation?.threshold || 80;
      const t = (u.pronunciation?.targets || [])[st.ti] || { sound: '', words: [] };
      const words = (t.words || []).map((w, wi) => `
        <span class="pword" id="pw${wi}">
          <span class="pword-w">${escapeHtml(w)}</span>
          <button class="mini l" data-listen="${escapeHtml(w)}" aria-label="Ascultă ${escapeHtml(w)}">🔊</button>
          ${VOICE.sttSupported ? `<button class="mini m" data-try="${escapeHtml(w)}" data-wi="${wi}" aria-label="Încearcă tu ${escapeHtml(w)}">🎙️</button>` : ''}
        </span>`).join('');
      const host = frame(
        `${evaSay(`Exersează sunetul <b>${escapeHtml(t.sound)}</b> 🗣️.${t.tip ? '<br>💡 ' + escapeHtml(t.tip) : ''}<br>Apasă 🔊 să auzi, apoi 🎙️ să încerci tu.`, '🗣️')}
         <div class="pwords">${words}</div>
         ${VOICE.sttSupported ? '' : '<p class="hint">🎧 Ascultă modelul și repetă cu voce tare. (Scorul automat la microfon există pe Chrome/Edge desktop sau Android — pe iPhone/iPad nu e disponibil.)</p>'}
         <div class="notice" id="pn"></div>`,
        { action: 'Continuă →' });
      host.querySelectorAll('[data-listen]').forEach((b) => b.addEventListener('click', () => VOICE.speak(b.dataset.listen, { rate: 0.8 })));
      const notice = $('#pn', host);
      const resetTryBtns = () => host.querySelectorAll('[data-try]').forEach((x) => { x.dataset.busy = ''; x.classList.remove('rec'); x.textContent = '🎙️'; });
      host.querySelectorAll('[data-try]').forEach((b) => b.addEventListener('click', () => {
        if (b.dataset.busy === '1') { VOICE.stopListening(); return; } // a doua apăsare = oprește
        resetTryBtns();                 // oprește vizual orice alt buton pornit
        const word = b.dataset.try; VOICE.stopSpeaking();
        b.dataset.busy = '1'; b.classList.add('rec'); b.textContent = '🔴';
        notice.textContent = `🎙️ Spune acum: „${word}"…`;
        VOICE.listen({
          onresult: (text, alts) => {
            const score = VOICE.scoreAgainst(word, alts);
            const span = $('#pw' + b.dataset.wi, host); const good = score >= th;
            span.classList.remove('ok', 'bad'); span.classList.add(good ? 'ok' : 'bad');
            let sc = span.querySelector('.pscore');
            if (!sc) { sc = document.createElement('span'); sc.className = 'pscore'; span.appendChild(sc); }
            sc.className = 'pscore ' + (good ? 'ok' : 'bad'); sc.textContent = score;
            notice.textContent = good ? `✅ „${word}" — scor ${score}. Bravo!` : `🔁 Am auzit „${text}" — scor ${score}. Ascultă modelul și mai încearcă.`;
          },
          onerror: (m) => { notice.textContent = m; },
          onend: () => { b.dataset.busy = ''; b.classList.remove('rec'); b.textContent = '🎙️'; },
        });
      }));
    },

    practice(st) {
      const parts = splitAnswers(P.unit.exercisesMd);
      const host = frame(
        `${evaSay('Exerciții de exersat ✍️. Încearcă în minte, apoi apasă „Arată răspunsurile".', '✍️')}
         <div class="card">${MD.render(parts.ex)}
           <details class="answers"><summary>Arată răspunsurile</summary>${MD.render(parts.ans || '_(mai sus)_')}</details>
         </div>`,
        { action: 'Continuă →' });
    },

    chat(st) {
      const u = P.unit;
      const key = `chat.${u.code}`;
      let history = ustore.get(key, []);
      let realTurns = history.filter((m) => m.role === 'user' && !m.content.startsWith('[AJUTOR RO]')).length;
      const host = frame(
        `${evaSay('Acum <b>vorbește cu mine</b> 💬! Scrie sau apasă 🎙️. Te corectez cu blândețe. După câteva schimburi apare butonul de continuare.', '💬')}
         <div class="chat" id="chat"></div>
         <div class="notice" id="cn"></div>
         <div class="composer">
           <button class="helpbtn" id="helpRo" aria-label="Ajutor în română">🇷🇴</button>
           <textarea id="cin" rows="1" placeholder="Scrie în engleză…" aria-label="Mesajul tău"></textarea>
           ${VOICE.sttSupported ? '<button class="cbtn mic" id="mic" aria-label="Vorbește">🎙️</button>' : ''}
           <button class="cbtn send" id="send" aria-label="Trimite">➤</button>
         </div>`,
        { action: 'Am vorbit destul → Continuă', holdNext: true });

      const chatEl = $('#chat', host), input = $('#cin', host), notice = $('#cn', host);
      const nextBtn = $('#wizNext'); // ascuns până la 3 schimburi
      function refreshNext() {
        realTurns = history.filter((m) => m.role === 'user' && !m.content.startsWith('[AJUTOR RO]')).length;
        nextBtn.style.display = realTurns >= 3 ? '' : 'none';
        if (realTurns < 3) nextBtn.title = 'Mai vorbește puțin cu EVA';
      }
      nextBtn.addEventListener('click', () => next());

      function draw() {
        chatEl.innerHTML = history.map((m, i) => {
          if (m.role === 'user') return m.content.startsWith('[AJUTOR RO]')
            ? `<div class="notice">🇷🇴 Ai cerut ajutor în română</div>`
            : `<div class="msg me">${escapeHtml(m.content)}</div>`;
          return `<div class="msg eva">${MD.render(m.content)}<button class="speak" data-i="${i}" aria-label="Ascultă">🔊</button></div>`;
        }).join('');
        chatEl.querySelectorAll('.speak').forEach((b) => b.addEventListener('click', () => VOICE.speak(history[b.dataset.i].content)));
        chatEl.scrollTop = chatEl.scrollHeight;
      }
      function kickoff() {
        if (!history.length) {
          const opener = u.flow?.guided?.[0]?.eva || "Hello! I'm EVA. What's your name?";
          history.push({ role: 'assistant', content: opener });
          ustore.set(key, history); draw();
          if (autoTts()) VOICE.speak(opener);
        } else draw();
        refreshNext();
      }
      async function send(text) {
        if (S.busy || !text) return;
        history.push({ role: 'user', content: text }); ustore.set(key, history); draw();
        S.busy = true; notice.textContent = '';
        chatEl.insertAdjacentHTML('beforeend', '<div class="typing" id="typing">EVA scrie<i>.</i><i>.</i><i>.</i></div>');
        chatEl.scrollTop = chatEl.scrollHeight;
        try {
          const res = await API.chat(u.code, 'guided', history);
          history.push({ role: 'assistant', content: res.reply }); ustore.set(key, history); draw();
          if (autoTts()) VOICE.speak(res.reply);
        } catch (e) {
          notice.textContent = (e.message || 'Eroare.') + ' — mesajul e pus înapoi în casetă.';
          notice.classList.add('err'); history.pop(); if (!text.startsWith('[AJUTOR RO]')) input.value = text;
          ustore.set(key, history); draw();
        } finally { S.busy = false; $('#typing', chatEl)?.remove(); refreshNext(); }
      }
      function submit() { const t = input.value.trim(); if (!t) return; input.value = ''; send(t); }
      $('#send', host).addEventListener('click', submit);
      input.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); } });
      $('#helpRo', host).addEventListener('click', () => send('[AJUTOR RO] Explică-mi pe scurt în română ultimul tău mesaj și cum pot răspunde.'));
      const mic = $('#mic', host);
      mic?.addEventListener('click', () => {
        if (mic.classList.contains('rec')) { VOICE.stopListening(); mic.classList.remove('rec'); return; }
        VOICE.stopSpeaking(); mic.classList.add('rec'); notice.textContent = '🎙️ Te ascult… vorbește în engleză.';
        VOICE.listen({
          onresult: (t) => { input.value = t; notice.textContent = `Am auzit: „${t}". Apasă ➤.`; },
          onerror: (m) => { notice.textContent = m; notice.classList.add('err'); },
          onend: () => mic.classList.remove('rec'),
        });
      });
      kickoff();
    },

    testIntro(st) {
      frame(
        `<div class="big-hero-emoji">✅</div>
         ${evaSay(`Acum un <b>test scurt</b> ✅ — <b>${st.n} întrebări</b>, câte una pe ecran.<br>Îți spun imediat dacă e corect. Nu-ți face griji, poți relua oricând!`, '✅')}`,
        { action: 'Începe testul →' });
    },

    testItem(st) {
      const items = P.unit.test?.items || [];
      const it = items[st.ti];
      const idxInTest = st.ti + 1;
      const prog = getProg(P.unit.code);
      // idempotent: dacă a răspuns deja (venit înapoi), arată doar rezultatul
      if (prog.testAnswers && (st.ti in prog.testAnswers)) {
        const ok = prog.testAnswers[st.ti];
        frame(
          `${evaSay(`Întrebarea <b>${idxInTest} din ${items.length}</b> — ai răspuns deja.`, ok ? '✅' : '❌')}
           <div class="card"><div class="q">${escapeHtml(it.question)}</div>
             <div class="${ok ? 'test-ok' : 'test-no'}" style="margin-top:12px">${ok ? '✅ Ai răspuns corect' : '❌ Răspuns corect: ' + escapeHtml(it.answer.split('|')[0].trim())}</div></div>
           <p class="hint">Poți merge <b>◀ Înapoi</b> să revezi, sau <b>Continuă →</b>.</p>`,
          { action: 'Continuă →' });
        return;
      }
      const host = frame(
        `${evaSay(`Întrebarea <b>${idxInTest} din ${items.length}</b>. Alege sau scrie răspunsul, apoi apasă <b>Verifică</b>.`, '❓')}
         <form id="titemForm">${renderItem(it, 0)}<div id="tfb"></div></form>`,
        { action: 'Verifică ✔', holdNext: true });
      wireReorder(host);
      const btn = $('#wizNext');
      let checked = false;
      btn.addEventListener('click', () => {
        if (!checked) {
          const el = $('#ti0', host);
          const t = effType(it);
          let given = '';
          if (t === 'mcq') given = (host.querySelector('input[name="q0"]:checked') || {}).value || '';
          else if (t === 'reorder') given = $('#ro-out-0', host)?.dataset.v || '';
          else given = ($('#in0', host) || {}).value || '';
          if (t === 'mcq' && !given) { $('#tfb', host).innerHTML = '<div class="notice err">Alege un răspuns 🙂</div>'; return; }
          const ok = checkAnswer(it, given);
          el.classList.add(ok ? 'correct' : 'wrong');
          el.querySelector('.fb.no').textContent = `✘ Corect: ${it.answer.split('|')[0].trim()}`;
          host.querySelectorAll('input,button.w,.reorder-pool .w').forEach((x) => { x.disabled = true; });
          const p = getProg(P.unit.code); p.testAnswers = p.testAnswers || {}; p.testAnswers[st.ti] = ok; setProg(P.unit.code, p);
          $('#tfb', host).innerHTML = ok ? '<div class="test-ok">✅ Corect!</div>' : '<div class="test-no">❌ Data viitoare! Vezi răspunsul corect mai sus.</div>';
          btn.textContent = 'Continuă →'; checked = true;
          updateHeaderScore();
        } else next();
      });
    },

    testResult(st) {
      const u = P.unit; const items = u.test?.items || [];
      const total = items.length;
      const ta = getProg(u.code).testAnswers || {};
      const correct = Object.values(ta).filter(Boolean).length;
      const pct = total ? Math.round((correct / total) * 100) : 0;
      const th = u.test?.passThreshold || 80;
      const passed = pct >= th;
      // cel mai bun scor la testul unității (pentru carnetul de note) + trecut
      { const pr = getProg(u.code); pr.testBest = Math.max(pr.testBest || 0, pct); if (passed) pr.passed = true; setProg(u.code, pr); }
      // istoric: rezultatul testului (append-only, pt. afișare viitoare) — dedup pe re-randări identice
      const sig = `${u.code}:test:${pct}:${correct}`;
      if (_lastActivitySig !== sig) { _lastActivitySig = sig; API.logActivity(u.code, 'test_result', { correct, total, percent: pct, passed }).catch(() => {}); }
      frame(
        `<div class="big-hero-emoji">${passed ? '🎉' : '💪'}</div>
         <div class="test-result ${passed ? 'pass' : 'fail'}">${pct}% · ${correct} din ${total} corecte</div>
         ${evaSay(passed
            ? `Felicitări! Ai trecut testul (prag ${th}%). Ești gata pentru pasul următor! 🎉`
            : `Ai ${pct}% (prag ${th}%). Nicio grijă — reia lecția și încearcă din nou. Fiecare încercare te ajută! 💪`, passed ? '🎉' : '💪')}`,
        { action: 'Continuă →' });
    },

    done(st) {
      const u = P.unit;
      const p = getProg(u.code); const wasDone = p.done; p.done = true; p.i = P.steps.length - 1; setProg(u.code, p);
      const sc = scoreCounts();
      if (!wasDone) API.logActivity(u.code, 'unit_done', { correct: sc.correct, wrong: sc.wrong }).catch(() => {}); // istoric: unitate terminată

      const i = S.unitsIndex.findIndex((x) => x.code === u.code);
      const nx = S.unitsIndex[i + 1];
      const host = frame(
        `<div class="big-hero-emoji">🏆</div>
         ${evaSay(`Ai terminat lecția <b>${escapeHtml(u.title)}</b>! 🏆<br>La test: corecte <b>${sc.correct}</b> · de reluat <b>${sc.wrong}</b>.<br>Sunt mândră de tine! 🌟`, '🏆')}
         <div class="done-actions">
           ${nx ? `<button class="wiz-next" id="goNext">Lecția următoare: ${escapeHtml(nx.title)} →</button>` : ''}
           <button class="btn ghost" id="goHome">Înapoi la meniu</button>
         </div>`,
        {});
      $('#goHome', host).addEventListener('click', () => { location.hash = '#/'; });
      $('#goNext', host)?.addEventListener('click', () => { location.hash = '#/unit/' + encodeURIComponent(nx.code); });
    },
  };

  function wordBadge(score, th) {
    const g = score >= th;
    return `<div class="wtry-res ${g ? 'ok' : 'bad'}">${g ? '✅ Știut' : '🔁 De repetat'}<br><span class="wtry-heard">scor anterior ${score}</span></div>`;
  }

  // ---------- helpers test (mcq/cloze/translate/reorder/short) ----------
  function effType(it) { return (it.type === 'mcq' && !(it.options && it.options.length > 1)) ? 'short' : it.type; }
  function normAns(s) { return String(s).toLowerCase().replace(/[.,!?;:'"„”‘’]/g, '').replace(/\s+/g, ' ').trim(); }
  function checkAnswer(it, given) { return String(it.answer).split('|').map(normAns).includes(normAns(given)); }
  function renderItem(it, i) {
    const head = `<div class="titem" id="ti${i}"><div class="q">${escapeHtml(it.question)}</div>`;
    const foot = `<div class="fb ok">✔ Corect!</div><div class="fb no"></div></div>`;
    if (effType(it) === 'mcq') {
      const opts = it.options.map((o) => o.trim());
      return head + `<div class="opts">${opts.map((o) => `<label class="opt"><input type="radio" name="q${i}" value="${escapeHtml(o)}"> ${escapeHtml(o)}</label>`).join('')}</div>` + foot;
    }
    if (it.type === 'reorder') {
      const words = String(it.question).includes('/') ? it.question.split('/').map((w) => w.trim()).filter(Boolean) : String(it.answer).split(' ');
      return head + `<div class="reorder-pool" data-i="${i}">${words.map((w) => `<button type="button" class="w">${escapeHtml(w)}</button>`).join('')}</div>
        <div class="reorder-out" id="ro-out-${i}" data-v=""></div><button type="button" class="rev" id="ro-reset-${i}">↺ Resetează</button>` + foot;
    }
    const ph = it.type === 'translate' ? 'Tradu în engleză…' : 'Răspunsul tău…';
    return head + `<input type="text" id="in${i}" placeholder="${ph}" autocomplete="off">` + foot;
  }
  function wireReorder(host) {
    host.querySelectorAll('.reorder-pool').forEach((pool) => {
      const out = host.querySelector(`#ro-out-${pool.dataset.i}`);
      pool.querySelectorAll('.w').forEach((w) => w.addEventListener('click', () => {
        if (w.classList.contains('used') || w.disabled) return;
        w.classList.add('used'); w.style.opacity = '.35';
        out.textContent = (out.textContent + ' ' + w.textContent).trim(); out.dataset.v = out.textContent;
      }));
      host.querySelector(`#ro-reset-${pool.dataset.i}`)?.addEventListener('click', () => {
        out.textContent = ''; out.dataset.v = '';
        pool.querySelectorAll('.w').forEach((w) => { w.classList.remove('used'); w.style.opacity = '1'; });
      });
    });
  }
  function splitAnswers(md) {
    const m = String(md).match(/^([\s\S]*?)(\*\*?R[ăa]spunsuri[\s\S]*)$/im);
    return m ? { ex: m[1], ans: m[2] } : { ex: md, ans: '' };
  }
  function errScreen(msg) {
    return `<div class="boot"><div class="boot-logo">EVA</div><p>${escapeHtml(msg)}<br><a href="#/">← Înapoi la meniu</a></p></div>`;
  }

  // =========================================================================
  //  SETĂRI (provider LLM: Qwen local / Claude / Demo)
  // =========================================================================
  function reflectProvider() {
    const provs = S.config.providers || [];
    const prov = provs.find((x) => x.id === $('#providerSelect').value) || {};
    $('#anthropicBox').style.display = prov.kind === 'anthropic' ? '' : 'none';
    const li = $('#localInfo');
    if (prov.kind === 'ollama') { li.style.display = ''; li.innerHTML = `Model local: <code>${escapeHtml(prov.model || '')}</code>. Fără cheie. Apasă <b>Testează</b> ca să verifici conexiunea.`; }
    else if (prov.kind === 'demo') { li.style.display = ''; li.textContent = 'Mod demo — răspunsuri din lecție, fără AI (offline).'; }
    else li.style.display = 'none';
    $('#pingResult').textContent = '';
  }
  function openSettings() {
    const dlg = $('#settings');
    $('#modeRow').innerHTML = S.config.demo
      ? '⚠️ <b>Mod demo</b>. Alege un motor AI pentru conversație reală.'
      : `✅ <b>Conectat</b> — ${escapeHtml(S.config.providerLabel || '')}`;
    $('#providerSelect').innerHTML = (S.config.providers || []).map((pr) =>
      `<option value="${pr.id}" ${pr.id === S.config.provider ? 'selected' : ''}>${escapeHtml(pr.label)}</option>`).join('');
    $('#modelSelect').innerHTML = (S.config.models || []).map((m) =>
      `<option value="${m}" ${m === S.config.model ? 'selected' : ''}>${m}${m === 'claude-opus-5' ? ' (recomandat)' : ''}</option>`).join('');
    $('#effortSelect').value = S.config.effort || 'low';
    $('#apiKeyInput').value = '';
    $('#apiKeyInput').placeholder = S.config.hasKey ? '•••••••• (cheie salvată)' : 'sk-ant-…';
    reflectProvider();
    const vs = $('#voiceSelect'); const list = VOICE.getVoices();
    vs.innerHTML = '<option value="">(automat)</option>' + list.map((v) => `<option value="${escapeHtml(v.voiceURI)}" ${v.voiceURI === VOICE.getVoice() ? 'selected' : ''}>${escapeHtml(v.name)}</option>`).join('');
    $('#rateInput').value = VOICE.getRate(); $('#rateVal').textContent = VOICE.getRate();
    $('#autoTts').checked = autoTts();
    $('#googleClientId').value = S.authCfg.googleClientId || '';
    $('#facebookAppId').value = S.authCfg.facebookAppId || '';
    $('#facebookAppSecret').value = '';
    $('#facebookAppSecret').placeholder = S.config.hasFbSecret ? '•••••••• (secret salvat)' : 'secretul aplicației Facebook';
    dlg.showModal();
  }
  function wireSettings() {
    $('#rateInput').addEventListener('input', (e) => { $('#rateVal').textContent = e.target.value; });
    $('#settingsClose').addEventListener('click', () => $('#settings').close());
    $('#providerSelect').addEventListener('change', reflectProvider);
    $('#pingBtn').addEventListener('click', async () => {
      const id = $('#providerSelect').value; const r = $('#pingResult');
      r.textContent = '⏳ Testez conexiunea…'; r.style.color = 'var(--muted)';
      try { const res = await API.ping(id); r.textContent = res.message || (res.ok ? 'OK' : 'Indisponibil'); r.style.color = res.ok ? 'var(--good-ink)' : 'var(--weak-ink)'; }
      catch (e) { r.textContent = 'Eroare: ' + e.message; r.style.color = 'var(--weak-ink)'; }
    });
    $('#settingsForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      VOICE.setVoice($('#voiceSelect').value); VOICE.setRate($('#rateInput').value); store.set('eva.autoTts', $('#autoTts').checked);
      const body = { provider: $('#providerSelect').value, model: $('#modelSelect').value, effort: $('#effortSelect').value };
      const key = $('#apiKeyInput').value.trim(); if (key) body.apiKey = key;
      body.googleClientId = $('#googleClientId').value.trim();
      body.facebookAppId = $('#facebookAppId').value.trim();
      const fbSecret = $('#facebookAppSecret').value.trim(); if (fbSecret) body.facebookAppSecret = fbSecret;
      try {
        await API.saveConfig(body); S.config = await API.config();
        try { const ac = await API.authConfig(); S.authCfg = { googleClientId: ac.googleClientId || '', facebookAppId: ac.facebookAppId || '' }; } catch {}
        $('#settings').close(); route();
      } catch (err) { alert('Nu am putut salva: ' + err.message); }
    });
  }

  // ---------- router ----------
  function route() {
    if (!S.user) return viewAuth('login');
    const h = location.hash || '#/';
    let m;
    if (h === '#/grades') return viewGrades();
    if ((m = h.match(/^#\/unit\/([^/]+)/))) return startUnit(decodeURIComponent(m[1]));
    if ((m = h.match(/^#\/level\/([^/]+)/))) return viewLevel(decodeURIComponent(m[1]));
    return viewHome();
  }

  // =========================================================================
  //  AUTENTIFICARE — ecran de intrare (login / cont nou) · Google · Facebook
  // =========================================================================
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const s = document.createElement('script');
      s.src = src; s.async = true; s.defer = true;
      s.onload = () => resolve(); s.onerror = () => reject(new Error('script'));
      document.head.appendChild(s);
    });
  }
  // câmp de parolă cu buton „ochi" (arată/ascunde)
  function pwField(id, ph) {
    return `<div class="pwrow">
      <input id="${id}" type="password" autocomplete="off" placeholder="${ph}" />
      <button type="button" class="pw-eye" data-for="${id}" aria-label="Arată parola" title="Arată parola">👁</button>
    </div>`;
  }
  function wireEyes(root) {
    root.querySelectorAll('.pw-eye').forEach((b) => b.addEventListener('click', () => {
      const inp = root.querySelector('#' + b.dataset.for);
      if (!inp) return;
      const show = inp.type === 'password';
      inp.type = show ? 'text' : 'password';
      b.textContent = show ? '🙈' : '👁';
      b.setAttribute('aria-label', show ? 'Ascunde parola' : 'Arată parola');
      b.setAttribute('title', show ? 'Ascunde parola' : 'Arată parola');
      inp.focus();
    }));
  }

  function viewAuth(tab) {
    VOICE.stopSpeaking();
    const t = tab === 'signup' ? 'signup' : 'login';
    const gc = S.authCfg.googleClientId;
    const fb = S.authCfg.facebookAppId;
    const oauth = (gc || fb) ? `
        <div class="auth-or"><span>sau</span></div>
        <div class="oauth">
          ${gc ? '<div id="gbtn" class="gbtn-slot"></div>' : ''}
          ${fb ? '<button type="button" id="fbBtn" class="oauth-btn fb">f  Continuă cu Facebook</button>' : ''}
        </div>` : '';

    const loginForm = `
      <form id="loginForm" class="auth-form" novalidate>
        <label>Email <input id="lgEmail" type="email" inputmode="email" autocomplete="username" placeholder="nume@email.com" /></label>
        <label>Parolă ${pwField('lgPass', 'parola ta')}</label>
        <div class="auth-err" id="authErr" role="alert"></div>
        <button type="submit" class="btn big auth-submit">Intră în cont →</button>
      </form>`;

    const signupForm = `
      <form id="signupForm" class="auth-form" novalidate>
        <label>Email <input id="suEmail" type="email" inputmode="email" autocomplete="username" placeholder="nume@email.com" /></label>
        <label>Numele tău <span class="lbl-hint">(așa îți va spune EVA)</span>
          <input id="suName" type="text" autocomplete="off" maxlength="40" placeholder="ex. Andrei" /></label>
        <label>Parolă ${pwField('suPass', 'minim 6 caractere')}</label>
        <label>Repetă parola ${pwField('suPass2', 'aceeași parolă')}</label>
        <div class="auth-err" id="authErr" role="alert"></div>
        <button type="submit" class="btn big auth-submit">Creează cont →</button>
      </form>`;

    app.innerHTML = `
      <main class="auth-wrap">
        <div class="auth-card">
          <div class="auth-brand"><div class="logo">EVA</div>
            <div><div class="t">EVA</div><div class="s">English Voice Assistant</div></div>
          </div>
          <div class="auth-tabs">
            <button class="auth-tab ${t === 'login' ? 'on' : ''}" data-tab="login">Intră în cont</button>
            <button class="auth-tab ${t === 'signup' ? 'on' : ''}" data-tab="signup">Cont nou</button>
          </div>
          ${t === 'login' ? loginForm : signupForm}
          ${oauth}
        </div>
        <p class="auth-foot">Fără verificare de email — intri direct. Datele stau pe acest calculator.</p>
      </main>`;

    wireEyes(app);
    app.querySelectorAll('.auth-tab').forEach((b) => b.addEventListener('click', () => viewAuth(b.dataset.tab)));

    const errBox = $('#authErr');
    const showErr = (m) => { errBox.textContent = m; };

    if (t === 'login') {
      $('#loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = $('#lgEmail').value.trim();
        const pass = $('#lgPass').value;
        if (!email || !pass) return showErr('Completează email și parola.');
        try {
          const u = await API.login(email, pass);
          await onLoggedIn(u);
        } catch (err) { showErr(err.message || 'Nu am putut intra.'); }
      });
    } else {
      $('#signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = $('#suEmail').value.trim();
        const name = $('#suName').value.trim();
        const pass = $('#suPass').value;
        const pass2 = $('#suPass2').value;
        if (!email) return showErr('Scrie o adresă de email.');
        if (!name) return showErr('Alege un nume pentru EVA.');
        if (pass.length < 6) return showErr('Parola: minim 6 caractere.');
        if (pass !== pass2) return showErr('Cele două parole nu sunt identice.');
        try {
          const u = await API.signup(email, name, pass, pass2);
          await onLoggedIn(u);
        } catch (err) { showErr(err.message || 'Nu am putut crea contul.'); }
      });
    }

    // Google Identity Services
    if (gc) {
      loadScript('https://accounts.google.com/gsi/client').then(() => {
        if (!window.google || !google.accounts || !google.accounts.id) return;
        google.accounts.id.initialize({
          client_id: gc,
          callback: async (resp) => {
            try { const u = await API.googleLogin(resp.credential); await onLoggedIn(u); }
            catch (err) { showErr(err.message || 'Autentificare Google eșuată.'); }
          },
        });
        const slot = $('#gbtn');
        if (slot) google.accounts.id.renderButton(slot, { theme: 'outline', size: 'large', width: 280, text: t === 'signup' ? 'signup_with' : 'signin_with', locale: 'ro' });
      }).catch(() => { const s = $('#gbtn'); if (s) s.innerHTML = '<span class="oauth-off">Google indisponibil (fără internet?)</span>'; });
    }
    // Facebook JS SDK
    if (fb) {
      const fbBtn = $('#fbBtn');
      if (fbBtn) fbBtn.addEventListener('click', async () => {
        try {
          await loadScript('https://connect.facebook.net/en_US/sdk.js');
          window.FB || (await new Promise((r) => { window.fbAsyncInit = r; setTimeout(r, 1500); }));
          if (!window.FB) return showErr('Facebook indisponibil (fără internet?).');
          FB.init({ appId: fb, cookie: false, xfbml: false, version: 'v19.0' });
          FB.login((resp) => {
            if (resp.authResponse) {
              API.facebookLogin(resp.authResponse.accessToken).then(onLoggedIn).catch((err) => showErr(err.message || 'Autentificare Facebook eșuată.'));
            } else { showErr('Autentificare Facebook anulată.'); }
          }, { scope: 'public_profile,email' });
        } catch { showErr('Facebook indisponibil (fără internet?).'); }
      });
    }
  }

  async function onLoggedIn(u) {
    S.user = { email: u.email, name: u.name };
    // reîncarcă configul + progresul din DB, apoi pornește aplicația
    try { S.config = await API.config(); } catch {}
    await loadUserState();
    if (location.hash && location.hash !== '#/') route(); else viewHome();
  }
  async function doLogout() {
    try { await API.logout(); } catch {}
    S.user = null;
    remoteState = {}; // uită progresul din memorie
    location.hash = '#/';
    viewAuth('login');
  }

  // ---------- boot ----------
  (async function init() {
    try {
      const [units, config, me, authCfg, modTitles] = await Promise.all([API.units(), API.config(), API.me().catch(() => ({ authenticated: false })), API.authConfig().catch(() => ({})), API.moduleTitles().catch(() => ({}))]);
      S.unitsIndex = units; S.config = config; S.moduleTitles = modTitles || {};
      S.authCfg = { googleClientId: (authCfg && authCfg.googleClientId) || '', facebookAppId: (authCfg && authCfg.facebookAppId) || '' };
      if (me && me.authenticated) S.user = { email: me.email, name: me.name };
    } catch {
      app.innerHTML = errScreen('Nu mă pot conecta la server. Pornește EVA.bat sau node server.js.');
      return;
    }
    if (!S.unitsIndex.length) { app.innerHTML = errScreen('Serverul rulează, dar lipsește conținutul (content/units/).'); return; }
    wireSettings();
    window.addEventListener('hashchange', route);
    if (!S.user) { viewAuth('login'); return; }
    await loadUserState(); // progres/chat/SRS din DB
    route();
  })();
})();
