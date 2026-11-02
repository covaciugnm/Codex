'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = __dirname;
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8').replace(/^\uFEFF/, ''));
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const build = read('reports/full/build-result.json');
const audit = read('reports/full/archive-audit.json');
const roundtrip = read('reports/full/roundtrip.json');
const device = fs.existsSync(path.join(root, 'reports/device-status.json')) ? read('reports/device-status.json') : {status:'NOT_CHECKED'};
const runtime = fs.existsSync(path.join(root, 'reports/device-test.json')) ? read('reports/device-test.json') : {};
const runtimeMatches = runtime.testedApkSha256 === build.outputSha256;
const installed = runtimeMatches && runtime.installationVerified;
const launched = runtimeMatches && runtime.launchVerified;
const apk = 'dist/iflytek-1.0.3899-full-rebuilt.apk';
const source = 'dist/iflytek-1.0.3899-editable-source.zip';
if (crypto.createHash('sha256').update(fs.readFileSync(path.join(root, apk))).digest('hex') !== build.outputSha256 || audit.rebuilt.sha256 !== build.outputSha256) {
  throw new Error('APK and verification reports do not describe the same artifact.');
}
const sourceReady = fs.existsSync(path.join(root, source + '.sha256')) && fs.existsSync(path.join(root, source));
const staticPass = audit.status === 'PASS' && roundtrip.status === 'PASS' && build.signatureVerified && build.zipAlignmentVerified && build.manifestValuesEquivalent && build.badgingEquivalentExceptResourcePaths;
const count = n => new Intl.NumberFormat('ro-RO').format(n);
const link = (href, title) => `<a href="${escape(href)}">${escape(title)}</a>`;
const sourceHash = sourceReady ? fs.readFileSync(path.join(root, source + '.sha256'), 'utf8').trim().split(/\s+/)[0] : '';
const roPath = 'variants/romania-40';
const roApk = 'dist/iflytek-1.0.3899-romania40.apk';
const roAudit = fs.existsSync(path.join(root, roPath, 'reports/archive-audit.json')) ? read(roPath+'/reports/archive-audit.json') : null;
const roDevice = fs.existsSync(path.join(root, roPath, 'reports/device-test.json')) ? read(roPath+'/reports/device-test.json') : null;
if (roAudit && crypto.createHash('sha256').update(fs.readFileSync(path.join(root,roApk))).digest('hex') !== roAudit.variantSha256) throw Error('Romania APK hash mismatch');
const roTested = roAudit && roDevice && roDevice.testedApkSha256 === roAudit.variantSha256;
const roSection = roAudit ? `<h2>Varianta cu România (+40)</h2><p class="status${roTested && roDevice.launchVerified ? '' : ' pending'}"><strong>APK construit și semnat.</strong> ${roTested && roDevice.installationVerified ? 'Instalare verificată pe Galaxy A14.' : 'Instalarea pe telefon nu este încă verificată.'} ${roTested && roDevice.countrySelectorVerified ? 'Lista cu patru țări a fost verificată pe telefon.' : 'Interfața trebuie verificată pe telefon.'}</p><p>${link(roApk,'Descarcă APK-ul cu România (+40)')} · ${link(roApk+'.sha256','SHA-256')} · ${link(roPath+'/README.md','Modificări, formatul numărului și limite')}.</p><p>Selectează +40 și introdu 9 cifre începând cu 7, fără zero inițial. Fluxul SDK existent transmite <code>ccode: "40"</code> separat de număr. Acceptarea numărului de către server nu este încă verificată.</p><p>22 de teste ARM64 trecute. Față de baza de mai jos, se modifică numai libapp.so; celelalte 79 de biblioteci, 6 DEX, 1.046 assets și manifestul sunt păstrate. ${link(roPath+'/reports/archive-audit.json','Audit APK')} · ${link(roPath+'/reports/native-tests.json','Teste ARM64')}${roTested ? ' · '+link(roPath+'/reports/device-test.json','Test pe telefon') : ''}.</p>` : '';
const html = `<!doctype html>
<html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>iFLYTEK 1.0.3899 — APK recompilat</title>
<style>body{font:17px/1.65 system-ui,sans-serif;max-width:960px;margin:40px auto;padding:0 24px;color:#172b39;background:#f6f8fa}h1,h2{line-height:1.25}h1{font-size:2rem}h2{margin-top:2rem;font-size:1.3rem}a{color:#005e96}code{overflow-wrap:anywhere;font-size:.85em}pre{white-space:pre-wrap;background:#e8edf1;padding:16px;border-radius:8px}.status{padding:18px;border-left:5px solid #18704c;background:#e5f3eb}.pending{border-left-color:#b06e00;background:#fff2d7}table{border-collapse:collapse;width:100%;background:white}td,th{padding:10px;text-align:left;border-bottom:1px solid #d8e1e8}.muted{color:#4b606e}li{margin:8px 0}</style>
<body><p class="muted">Proiect local · 31 octombrie 2026 · com.iflytek.translateapp</p>
<p>${link('../../../CONTINUARE-UBUNTU.md','Continuare pe Ubuntu și Codex CLI remote')} · ${link('https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-apk-romania40-2026-10-31','Release GitHub cu toate artefactele noi')} · ${link('release-assets.json','Manifest SHA-256')}.</p>
<p>După restaurarea release-ului: ${link('dist/iflytek-1.0.3899-aot-analysis.zip','Analiza AOT completă și patch-ul ARM64')} · ${link('dist/iflytek-20261031-analysis-toolchain.zip','Uneltele de analiză și compilare')}.</p>
${roSection}
<h1>APK recompilat din Smali și resurse</h1>
<p class="status${staticPass ? '' : ' pending'}"><strong>Verificări statice: ${staticPass ? 'trecute' : 'nevalidate'}.</strong> APK recompilat: instalare ${installed ? 'verificată' : 'neverificată'}, pornire ${launched ? 'verificată' : 'neverificată'}. Autentificarea și Bluetooth necesită teste separate.</p>
<p>Versiunea 1.0.3899 a fost reconstruită cu Apktool 3.0.3 și Android Build Tools 36.0.0. Toate cele șase DEX au fost reasamblate. Bibliotecile native și Flutter sunt păstrate ca binare.</p>
<h2>Fișiere disponibile</h2><ul>
<li>${link(apk, 'APK recompilat, semnat local')} · ${count(audit.rebuilt.bytes)} octeți · ${link(apk+'.sha256','SHA-256')}</li>
<li>${sourceReady ? link(source,'Arhivă cu proiectul editabil Smali și resurse')+' · '+link(source+'.sha256','SHA-256') : 'Exportul proiectului editabil este în curs.'}</li>
<li>${link('README.md','Instrucțiuni și limite')} · ${link('Build.ps1','Script de construire')} · ${link('Check-Device.ps1','Diagnostic ADB')}</li>
</ul><p><strong>APK SHA-256:</strong><br><code>${escape(build.outputSha256)}</code></p>
${sourceReady ? '<p><strong>Arhivă surse SHA-256:</strong><br><code>'+escape(sourceHash)+'</code></p>' : ''}
<p class="status pending">Certificatul este local, diferit de cel al producătorului. Acest APK nu se poate instala ca actualizare peste aplicația oficială. ${runtime.originalAppUninstalled ? 'Înlocuirea pe Galaxy A14 a fost autorizată explicit de utilizator; datele locale ale versiunii oficiale au fost șterse la dezinstalare. APK-ul oficial este păstrat pentru reinstalare.' : 'Aplicația existentă și datele telefonului au fost păstrate.'}</p>
<h2>Ce arată comparația</h2><table><thead><tr><th>Element</th><th>Rezultat</th></tr></thead><tbody>
<tr><td>Clase în 6 DEX</td><td>${count(audit.original.dex.reduce((sum,d)=>sum+d.classes,0))}; aceleași numere de clase, metode și câmpuri per DEX</td></tr>
<tr><td>Smali identic textual după re-decodare</td><td>${count(roundtrip.identicalSmaliFiles)} fișiere</td></tr>
<tr><td>Diferențe normalizate</td><td>${count(roundtrip.equivalent.length)} fișiere: valori implicite, intervale de tratare a excepțiilor și ordinea enum/flag; ${count(roundtrip.unresolved.length)} diferențe neexplicate</td></tr>
<tr><td>Biblioteci native / assets</td><td>80 / 1.046, identice octet cu octet</td></tr>
<tr><td>Resurse identice textual</td><td>${count(roundtrip.identicalResourceFiles)}; attrs.xml echivalent după ordonarea declarațiilor</td></tr>
<tr><td>Manifest / metadate</td><td>Valori echivalente; diferă numerele liniilor și unele căi de resurse</td></tr>
<tr><td>Semnătură / aliniere ZIP</td><td>Verificate cu apksigner / zipalign</td></tr>
</tbody></table>
<p>Aceste rezultate verifică reconstrucția statică, fără a demonstra funcționarea serviciilor cloud sau acceptarea noului certificat.</p>
<h2>Telefon și ochelari</h2><p>Galaxy A14 5G SM-A146P/DSN; Android ${escape(device.androidVersion || 'neconfirmat')}, API ${escape(device.apiLevel || 'neconfirmat')}. Ochelari comunicați de utilizator: XF-AIGlasses-01, firmware 1.0.01.88. Diagnosticul ADB de la testul bazei: <strong>${escape(device.status)}</strong>. ${runtimeMatches ? 'Starea testului APK-ului recompilat: <strong>'+escape(runtime.status)+'</strong>.' : 'APK-ul recompilat nu are încă un raport de test pe dispozitiv pentru această amprentă.'} Acest diagnostic istoric nu confirmă conectarea actuală; telefonul va fi reconectat ulterior, conform ghidului de continuare.</p>
<p>Aplicația oficială 1.0.3899 a fost verificată înaintea înlocuirii: pornea și afișa ecranele principale în engleză. Identitatea APK-ului și certificatul original sunt consemnate separat în raportul inițial.</p>
<h2>Reconstruire</h2><pre>.\\Build.ps1 -VerifyRoundTrip
.\\Export-Source.ps1
.\\Check-Device.ps1
node .\\Write-Report.cjs</pre>
<p>Necesită Windows, PowerShell 7, Node.js și JDK 21. ${link('tools.lock.json','Versiunile uneltelor și amprentele lor')} sunt fixate. Cheia privată de semnare rămâne în directorul local privat, în afara acestui pachet.</p>
<h2>Limite rămase</h2><ul><li>Sursele originale Dart și C/C++ nu au fost recuperate. Exportul Java/JADX cu erori rămâne material de analiză; acest build folosește Smali.</li><li>Autentificarea și regulile serverului sunt cele originale. Baza păstrează țările originale; varianta separată +40 modifică selectorul și validarea locală. Acceptarea României de către server rămâne necunoscută.</li><li>Profilurile ART originale pot să nu mai corespundă noilor DEX. Alinierea ZIP la 16 KiB nu modifică alinierea ELF a bibliotecilor.</li><li>Instalarea și pornirea bazei sunt verificate; cele ale variantei +40 necesită test pe telefon. Accesul cu contul existent, Bluetooth, audio, traducerea și OTA rămân netestate.</li></ul>
<h2>Dovezi</h2><ul>${[['reports/full/build-result.json','Rezultatul buildului'],['reports/full/archive-audit.json','Inventar și comparație APK'],['reports/full/roundtrip.json','Comparație Smali și resurse'],['reports/full/first-clean-build.log','Logul reasamblării inițiale'],['reports/full/signature.txt','Verificarea certificatului'],['reports/full/original-manifest-tree.txt','Manifest original'],['reports/full/rebuilt-manifest-tree.txt','Manifest reconstruit'],['test-verifier.cjs','Testele verificatorului']].map(([href,title])=>'<li>'+link(href,title)+'</li>').join('')}</ul>
<ul>${[['reports/source-export.json','Verificarea arhivei editabile'],['reports/device-status.json','Starea conexiunii ADB'],['reports/device-baseline.json','Verificarea aplicației oficiale'],['reports/device-test.json','Testul APK-ului recompilat pe telefon']].filter(([href])=>fs.existsSync(path.join(root,href))).map(([href,title])=>'<li>'+link(href,title)+'</li>').join('')}</ul>
<p class="muted">Raport generat din fișierele locale de verificare. Nicio validare statică nu este prezentată drept test pe dispozitiv.</p></body></html>`;
for (const match of html.matchAll(/href="([^"]+)"/g)) {
  if (/^https:\/\//.test(match[1])) continue;
  if (!fs.existsSync(path.join(root, match[1]))) throw new Error('Missing report link: '+match[1]);
}
fs.writeFileSync(path.join(root, 'index.html'), html, 'utf8');
console.log(JSON.stringify({report:path.join(root,'index.html'),staticPass,sourceReady,device:device.status,installed:!!installed,launched:!!launched}));
