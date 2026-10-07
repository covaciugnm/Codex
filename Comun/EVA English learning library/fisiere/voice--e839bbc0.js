/* voice.js — TTS (speechSynthesis) + STT (Web Speech API) + scor de pronunție (prototip).
 * Global: VOICE. Punct de inserție viitor: Azure Pronunciation Assessment (înlocuiește scoreAgainst). */
(function () {
  'use strict';

  // ---------- TTS ----------
  let voices = [];
  let chosenVoiceURI = localStorage.getItem('eva.voice') || '';
  let rate = Number(localStorage.getItem('eva.rate') || 0.9);

  let allVoices = [];
  function refreshVoices() {
    allVoices = window.speechSynthesis?.getVoices?.() || [];
    voices = allVoices.filter((v) => v.lang?.toLowerCase().startsWith('en'));
  }
  if ('speechSynthesis' in window) {
    refreshVoices();
    window.speechSynthesis.onvoiceschanged = refreshVoices;
  }
  function pickVoice() {
    if (!voices.length) refreshVoices();
    if (chosenVoiceURI) {
      const v = voices.find((v) => v.voiceURI === chosenVoiceURI);
      if (v) return v;
    }
    // preferă vocile „naturale" Microsoft/Google, apoi orice en-US, apoi orice en
    return voices.find((v) => /natural|neural/i.test(v.name) && v.lang === 'en-US')
        || voices.find((v) => v.lang === 'en-US')
        || voices[0] || null;
  }
  function speak(text, opts = {}) {
    if (!('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel();
    // curăță markdown-ul simplu pentru vorbire
    const clean = String(text).replace(/\*\*|__|`|_/g, '').replace(/\[AJUTOR RO\]/g, '');
    const u = new SpeechSynthesisUtterance(clean);
    const v = pickVoice();
    if (v) u.voice = v;
    u.lang = (v && v.lang) || 'en-US';
    u.rate = opts.rate ?? rate;
    if (opts.onend) u.onend = opts.onend;
    window.speechSynthesis.speak(u);
  }
  let speakRun = 0; // fiecare oprire/pornire invalidează lanțul anterior
  function stopSpeaking() { speakRun++; try { window.speechSynthesis.cancel(); } catch {} }

  // există voce românească instalată?
  function roVoice() {
    if (!allVoices.length) refreshVoices();
    return allVoices.find((v) => v.lang?.toLowerCase().startsWith('ro')) || null;
  }
  const roSupported = () => Boolean(roVoice());
  /** Citește text în ROMÂNĂ (dacă există voce ro-RO). onend opțional. */
  function speakRo(text, opts = {}) {
    if (!('speechSynthesis' in window) || !text) { opts.onend?.(); return; }
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(String(text).replace(/\*\*|__|`|_/g, ''));
    const v = roVoice();
    if (v) u.voice = v;
    u.lang = 'ro-RO';
    u.rate = opts.rate ?? 0.95;
    if (opts.onend) u.onend = opts.onend;
    window.speechSynthesis.speak(u);
  }
  /** Citește o listă de fraze pe rând (fiecare cu limba ei: {text, lang:'ro'|'en'}). */
  function speakSequence(items, opts = {}) {
    if (!('speechSynthesis' in window)) { opts.onend?.(); return; }
    stopSpeaking();
    const myRun = speakRun;
    let i = 0;
    (function nxt() {
      if (myRun !== speakRun) return;
      if (i >= items.length) { opts.onend?.(); return; }
      const it = items[i];
      const u = new SpeechSynthesisUtterance(String(it.text).replace(/\*\*|`|_/g, ''));
      const v = it.lang === 'ro' ? roVoice() : pickVoice();
      if (v) u.voice = v;
      u.lang = it.lang === 'ro' ? 'ro-RO' : ((v && v.lang) || 'en-US');
      u.rate = it.lang === 'ro' ? 0.95 : 0.85;
      u.onend = () => { i++; setTimeout(nxt, 300); };
      window.speechSynthesis.speak(u);
    })();
  }

  // Redă un script de dialog "Speaker: text" linie cu linie, cu pauze
  function speakScript(script, opts = {}) {
    if (!('speechSynthesis' in window)) { opts.onend?.(); return; }
    stopSpeaking();
    const myRun = speakRun;
    const lines = String(script).split('\n').map((l) => l.trim()).filter(Boolean)
      .map((l) => { const m = l.match(/^([^:]{1,24}):\s*(.+)$/); return m ? m[2] : l; });
    let i = 0;
    (function next() {
      if (myRun !== speakRun) return;
      if (i >= lines.length) { opts.onend?.(); return; }
      const u = new SpeechSynthesisUtterance(lines[i].replace(/\*\*|`/g, ''));
      const v = pickVoice();
      if (v) u.voice = v;
      u.lang = (v && v.lang) || 'en-US';
      u.rate = opts.rate ?? Math.min(rate, 0.85); // ascultare = mai lent
      u.onend = () => { i++; setTimeout(next, 380); };
      window.speechSynthesis.speak(u);
    })();
  }

  // ---------- STT ----------
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition || null;
  const sttSupported = Boolean(SR);
  let activeRec = null;      // recunoașterea în curs (null când microfonul e liber)
  let pendingStart = null;   // pornire amânată până se eliberează microfonul

  /** Ascultă o singură replică. cb: {onresult(text), onerror(msg), onend()} */
  function listen(cb = {}, lang = 'en-US') {
    if (!SR) { cb.onerror?.('Recunoașterea vocală nu e disponibilă în acest browser. Folosește Chrome sau Edge.'); return null; }

    const begin = () => {
      const rec = new SR();
      activeRec = rec;
      rec.lang = lang;
      rec.interimResults = false;
      rec.maxAlternatives = 3;
      rec.onresult = (e) => {
        const alts = [...(e.results[0] || [])].map((a) => a.transcript);
        cb.onresult?.(alts[0] || '', alts);
      };
      rec.onerror = (e) => {
        // „aborted" = am oprit/repornit noi înșine microfonul → benign, nu e o eroare reală
        if (e.error === 'aborted') return;
        const msg = (e.error === 'not-allowed' || e.error === 'service-not-allowed')
            ? 'Permite accesul la microfon pentru a vorbi cu EVA.'
          : e.error === 'no-speech' ? 'Nu am auzit nimic — mai încearcă. 🙂'
          : e.error === 'audio-capture' ? 'Nu găsesc microfonul. Verifică-l și încearcă din nou.'
          : `Eroare microfon: ${e.error}`;
        cb.onerror?.(msg);
      };
      rec.onend = () => {
        if (activeRec === rec) activeRec = null;
        cb.onend?.();
        // dacă un start era în așteptare (o nouă apăsare), pornește-l acum că microfonul e liber
        if (!activeRec && pendingStart) { const f = pendingStart; pendingStart = null; f(); }
      };
      try {
        rec.start();
      } catch (err) {
        // microfonul e încă ocupat o clipă → resetăm, îl anunțăm blând (poate reapăsa)
        if (activeRec === rec) activeRec = null;
        cb.onerror?.('Microfonul e ocupat o clipă — mai apasă o dată. 🎙️');
        cb.onend?.();
      }
    };

    if (activeRec) {
      // o recunoaștere e încă activă → o oprim și pornim DUPĂ ce microfonul se eliberează (onend)
      pendingStart = begin;
      try { activeRec.abort(); } catch { pendingStart = null; begin(); }
      return null;
    }
    begin();
    return activeRec;
  }
  function stopListening() {
    pendingStart = null;
    const r = activeRec;
    if (r) { try { r.abort(); } catch {} }
    // activeRec se anulează în onend
  }

  // ---------- scor pronunție (prototip: transcript vs țintă) ----------
  function norm(s) {
    return String(s).toLowerCase()
      .replace(/[^a-z0-9' ]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }
  function lev(a, b) {
    const m = a.length, n = b.length;
    if (!m) return n; if (!n) return m;
    let prev = Array.from({ length: n + 1 }, (_, j) => j);
    for (let i = 1; i <= m; i++) {
      const cur = [i];
      for (let j = 1; j <= n; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      }
      prev = cur;
    }
    return prev[n];
  }
  /** 0–100: cât de aproape e ce s-a auzit de țintă (pe cea mai bună alternativă). */
  function scoreAgainst(target, heardAlternatives) {
    const t = norm(target);
    if (!t) return 0;
    let best = 0;
    for (const alt of heardAlternatives || []) {
      const h = norm(alt);
      if (!h) continue;
      if (h === t || h.includes(t) || t.includes(h)) { best = Math.max(best, 100); continue; }
      const d = lev(h, t);
      best = Math.max(best, Math.round(100 * (1 - d / Math.max(t.length, h.length))));
    }
    return Math.max(0, Math.min(100, best));
  }

  window.VOICE = {
    ttsSupported: 'speechSynthesis' in window,
    sttSupported,
    speak, speakScript, speakRo, speakSequence, stopSpeaking,
    roSupported,
    listen, stopListening,
    scoreAgainst,
    getVoices: () => voices.slice(),
    setVoice: (uri) => { chosenVoiceURI = uri || ''; localStorage.setItem('eva.voice', chosenVoiceURI); },
    getVoice: () => chosenVoiceURI,
    setRate: (r) => { rate = Number(r) || 0.9; localStorage.setItem('eva.rate', String(rate)); },
    getRate: () => rate,
  };
})();
