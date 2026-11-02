'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const root = 'D:/CodexWork/iFLYTEK-publish-20261031';
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'iflytek-manifest-sha256.json'), 'utf8'));
const lines = ['# Atașamentele arhivei iFLYTEK', '', `Snapshot: ${manifest.createdAt}. [Release privat](${manifest.releaseUrl}).`, '', 'Toate căile de mai jos se restaurează cu `node tools/restore-iflytek-assets.cjs`. Numele atașamentelor includ un prefix SHA-256; verificarea folosește întregul hash din manifest.', '', '| Atașament | Octeți | Căi originale în repository |', '| --- | ---: | --- |'];
for (const a of manifest.assets) lines.push(`| [${a.name}](${a.downloadUrl}) | ${a.bytes} | ${a.paths.map(p => '`'+p+'`').join('<br>')} |`);
lines.push('', 'Celelalte fișiere sunt păstrate în Git. Cele două căi ale APK-ului oficial sunt identice byte cu byte și folosesc același atașament.', '');
fs.writeFileSync(path.join(root, 'IFLYTEK_RELEASE_ASSETS.md'), lines.join('\n'));
const ignored = ['','\n# Large iFLYTEK files live in the release; restore with tools/restore-iflytek-assets.cjs.','/.iflytek-download-*/', ...manifest.files.filter(f => f.storage === 'release').map(f => '/'+f.path),''];
fs.appendFileSync(path.join(root, '.gitignore'), ignored.join('\n'));
const additions = ['.gitignore','README.md','IFLYTEK_RELEASE_ASSETS.md','iflytek-manifest-sha256.json','tools/iflytek-snapshot.cjs','tools/verify-iflytek-snapshot.cjs','tools/restore-iflytek-assets.cjs'];
const paths = [...additions,...manifest.files.filter(f => f.storage === 'git').map(f => f.path)];
fs.writeFileSync('D:/CodexWork/iflytek-stage-paths.nul', paths.map(p => ':(literal)'+p+'\0').join(''));
const notes = [
  '# Arhiva completă iFLYTEK — 31 octombrie 2026', '',
  `${manifest.summary.files} de fișiere originale, ${manifest.summary.bytes} de octeți. ${manifest.summary.gitFiles} de fișiere sunt în Git, iar ${manifest.summary.releasePaths} de căi mari sunt acoperite de ${manifest.summary.releaseUniqueAssets} de atașamente distincte în acest release.`, '',
  'Conține documentații originale și traduceri, aplicații, arhive de cod și SDK, APK extras/reconstituit, clase Java/Smali, inventare, dicționare, protocol și rapoarte de audit. Catalogul AI Glasses 2026 existent este păstrat.', '',
  '## Restaurare', '',
  'Cu Node.js 18+ și GitHub CLI autentificat cu acces de citire la repository, rulează din clona repository-ului:', '',
  '```sh', 'node tools/restore-iflytek-assets.cjs', 'node tools/verify-iflytek-snapshot.cjs', '```', '',
  'Apoi deschide local `iFLYTEK_XF-AIGlasses-01_Documentatie/INDEX.html`. Un simplu clone sau Download ZIP nu include atașamentele acestui release.', '',
  '`iflytek-manifest-sha256.json` documentează fiecare cale, dimensiune și SHA-256. Scriptul restaurează și copiile duplicate la căile originale. Nu au fost modificate documentele auditate; verificarea uploadului privește integritatea datelor, nu validarea hardware.', ''
];
fs.writeFileSync('D:/CodexWork/iflytek-release-notes-20261031.md', notes.join('\n'));
console.log(JSON.stringify({stagedPaths: paths.length, ...manifest.summary}, null, 2));
