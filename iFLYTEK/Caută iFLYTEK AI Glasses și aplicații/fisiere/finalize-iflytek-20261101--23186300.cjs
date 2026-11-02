'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const {inspect}=require('./inspect-android-archive.cjs');
const root=path.resolve(__dirname,'..'),base=path.join(root,'collection-2026-11-01');
const mp=path.join(base,'manifest.json'),manifest=JSON.parse(fs.readFileSync(mp,'utf8'));
const invalidResourceResolutions=manifest.records.filter(r=>/\.js$/.test(r.url)&&r.contentType?.includes('text/html'));
manifest.records=manifest.records.filter(r=>!invalidResourceResolutions.includes(r));
fs.writeFileSync(path.join(base,'discarded-resource-resolutions.json'),JSON.stringify({note:'Discarded non-JavaScript fallback URLs encountered during resource discovery; not downloadable app versions.',records:invalidResourceResolutions},null,2)+'\n');
const assets=JSON.parse(execFileSync('gh',['release','view','iflytek-software-2026-11-01','--repo','covaciugnm/iFLYTEK','--json','assets'],{encoding:'utf8'})).assets;
const metadata=[];
for(const r of manifest.records.filter(r=>r.file)){
 if(r.bytes>=25*1024*1024){r.storage='release';r.releaseTag='iflytek-software-2026-11-01';r.assetName=path.basename(r.file);r.githubUrl='https://github.com/covaciugnm/iFLYTEK/releases/download/'+r.releaseTag+'/'+r.assetName;const a=assets.find(a=>a.name===r.assetName);if(!a||a.digest!=='sha256:'+r.sha256||a.size!==r.bytes)throw Error('Upload not verified: '+r.file);}else r.storage='git';
 if(r.kind==='application'){const info=inspect(path.join(base,r.file));r.android={package:info.package||info.manifest.package_name,versionName:info.versionName||info.manifest.version_name,versionCode:info.versionCode||info.manifest.version_code,format:info.format};if(r.package&&r.package!==r.android.package)throw Error('Unexpected package');if(r.claimedVersion&&r.claimedVersion!==r.android.versionName)throw Error('Version mismatch');metadata.push({file:r.file,...info});}
}
fs.writeFileSync(path.join(base,'android-metadata.json'),JSON.stringify(metadata,null,2)+'\n');
fs.writeFileSync(mp,JSON.stringify(manifest,null,2)+'\n');
const bins=manifest.records.filter(r=>r.file&&['application','installer'].includes(r.kind));
const docs=manifest.records.filter(r=>r.file&&r.kind==='documentation');
const unavailable=manifest.records.filter(r=>r.status==='unavailable');
const duplicates=manifest.records.filter(r=>r.status==='already-in-github');
const lines=['# Aplicații și documentație iFLYTEK — 1 noiembrie 2026','',
 'Colecție suplimentară pentru iFLYTEK AI Glasses XF-AIGlasses-01 și aplicațiile asociate iFLYTEK Translate, Bavvo și Loomy. Fișierele au fost descărcate, fără instalare sau testare pe ochelari. Nu este confirmată o versiune APK destinată exclusiv UE, nici conectarea Bavvo la acest model de ochelari.','',
 `Au fost adăugate ${bins.length} arhive/instalatoare și ${docs.length} pagini sau resurse de documentație. ${duplicates.length} surse au fost recunoscute după SHA-256 ca duplicate ale arhivei GitHub sau ale fișierelor deja colectate. ${unavailable.length} URL-uri au rămas indisponibile ori au returnat conținut necorespunzător.`, '',
 '## Descărcări','',
 '| Fișier | Versiune verificată | Octeți | Descărcare |','| --- | --- | ---: | --- |',
 ...bins.map(r=>`| ${path.basename(r.file)} | ${r.android?.versionName||r.claimedVersion||'vezi sursa'} | ${r.bytes} | [GitHub](${r.githubUrl||r.file}) |`),'',
 'Bavvo este păstrat în format XAPK, cu APK-ul principal și pachetele split originale. Versiunile au fost verificate în manifestele Android din interior. Variantele FY100300xx sunt canale de distribuție ale aceleiași aplicații chinezești; nu constituie dovezi pentru o ediție UE. Versiunea 1.0.3949 provine de la XLHS, iar APK-ul 1.0.3899 de pe pagina oficială implicită exista deja în Release-ul din 31 octombrie.','',
 '## Restaurare și verificare','',
 'Fișierele mari sunt în Release, nu în istoricul Git. Copia locală creată în această sesiune conține fișierele noi. După un clone nou:','',
 '```sh','node tools/verify-collection-20261101.cjs --restore','node tools/verify-collection-20261101.cjs --remote','```','',
 'Verificarea utilizează SHA-256 și dimensiunea fiecărui fișier, inclusiv digestul calculat de GitHub pentru atașamente. Nu certifică siguranța sau autenticitatea semnăturii editorului.','',
 '## iOS','',
 'Paginile App Store, istoricul public al versiunilor și linkurile sunt arhivate în sources. Nu au fost găsite fișiere IPA publice oferite pentru descărcare de editor; instalarea și accesul la versiuni istorice depind de App Store și de contul Apple. Nu au fost fabricate arhive IPA.','',
 '## SDK și documentație','',
 'Nu a fost identificat un SDK public nou, specific XF-AIGlasses-01. Fișierul existing-sdk-and-documentation.json inventariază 207 fișiere relevante deja prezente în GitHub. Codul reconstruit/experimental și SDK-urile pentru HeyCyan, Eyevue sau Rokid rămân etichetate după proveniență; nu sunt un SDK oficial pentru acești ochelari. Au fost păstrate paginile oficiale Bavvo, ghidurile și resursele JavaScript care conțin textele de ajutor. Paginile HTML dinamice pot necesita site-ul original pentru afișare completă.','',
 'Căutări efectuate: iFLYTEK AI Glasses SDK/manual/download, XF-AIGlasses-01 GitHub, 讯飞AI眼镜 SDK/说明书, com.iflytek.translateapp versions/download, Bavvo APK/version history. Nu a fost găsit un manual PDF nou pentru modelul exact.','',
 '## Surse indisponibile','',
 ...unavailable.map(r=>`- ${r.url} — ${r.error}`),'',
 'Acoperirea este limitată la resursele public descoperite și accesibile la data colectării. O versiune menționată într-un titlu de site, fără binar descărcabil, nu este prezentată ca descărcată. Inventarul complet cu URL-uri, rezultate, duplicate și SHA-256 este în manifest.json.',''];
fs.writeFileSync(path.join(base,'README.md'),lines.join('\n'));
fs.writeFileSync(path.join(base,'SHA256SUMS.txt'),manifest.records.filter(r=>r.file).map(r=>r.sha256+'  '+r.file).join('\n')+'\n');
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
fs.writeFileSync(path.join(base,'INDEX.html'),'<!doctype html><html lang="ro"><meta charset="utf-8"><title>iFLYTEK — colecție software</title><style>body{font:16px system-ui;max-width:1400px;margin:36px auto;padding:0 20px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd;padding:10px;text-align:left}small{word-break:break-all}a{color:#1559ae}</style><h1>iFLYTEK — colecție 1 noiembrie 2026</h1><p>Arhive originale, surse și verificări. Compatibilitatea Bavvo cu ochelarii și o versiune UE distinctă rămân neconfirmate.</p><p><a href="README.md">Raport și limite</a> · <a href="manifest.json">Inventar complet</a> · <a href="android-metadata.json">Manifestele Android</a></p><table><tr><th>Fișier / sursă</th><th>Stare</th><th>Versiune</th><th>SHA-256</th></tr>'+manifest.records.map(r=>'<tr><td><a href="'+escape(r.file||r.url)+'">'+escape(r.file||r.url)+'</a><br><small><a href="'+escape(r.url)+'">Sursă</a>'+(r.githubUrl?' · <a href="'+escape(r.githubUrl)+'">GitHub Release</a>':'')+'</small></td><td>'+escape(r.status)+(r.error?'<br>'+escape(r.error):'')+'</td><td>'+escape(r.android?.versionName||r.claimedVersion||'')+'</td><td><small>'+escape(r.sha256||'')+'</small></td></tr>').join('')+'</table></html>');
console.log(JSON.stringify({binaries:bins.length,documentationFiles:docs.length,duplicates:duplicates.length,unavailable:unavailable.length}));
