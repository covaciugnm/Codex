'use strict';
const fs = require('node:fs');
const fsp = fs.promises;
const path = require('node:path');
const crypto = require('node:crypto');
const { Transform } = require('node:stream');
const { pipeline } = require('node:stream/promises');
const inventory = JSON.parse(fs.readFileSync('C:/Users/User/AppData/Local/Temp/iflytek-upload-inventory-20261031.json', 'utf8').replace(/^\uFEFF/, ''));
const repo = 'D:/CodexWork/iFLYTEK-publish-20261031';
const assetsDir = 'D:/CodexWork/iflytek-release-assets-20261031';
const prefix = 'iFLYTEK_XF-AIGlasses-01_Documentatie';
const threshold = 25 * 1024 * 1024;
const tag = 'iflytek-documentation-2026-10-31';
const repository = 'covaciugnm/iFLYTEK';

async function digest(file, bytes, blob = false) {
  const hash = crypto.createHash('sha256');
  const git = blob ? crypto.createHash('sha1').update(`blob ${bytes}\0`) : null;
  let actual = 0;
  for await (const chunk of fs.createReadStream(file)) {
    actual += chunk.length;
    hash.update(chunk);
    if (git) git.update(chunk);
  }
  if (actual !== bytes) throw new Error(`Size mismatch: ${file}`);
  return {sha256: hash.digest('hex'), ...(git ? {gitBlobSha1: git.digest('hex')} : {})};
}
async function main() {
  await fsp.mkdir(assetsDir, {recursive: true});
  const entries = [...inventory.all].sort((a,b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  const known = new Set();
  for (const entry of entries) {
    if (!entry.path || entry.path.includes('\\') || entry.path.split('/').some(p => !p || p === '..' || p === '.') || path.isAbsolute(entry.path)) throw new Error('Unsafe inventory path');
    if (known.has(entry.path.toLowerCase())) throw new Error(`Case collision: ${entry.path}`);
    known.add(entry.path.toLowerCase());
  }
  let cursor = 0, finished = 0;
  const output = new Array(entries.length);
  const timer = setInterval(() => console.log(`Verified original bytes: ${finished}/${entries.length}`), 15000);
  try {
    await Promise.all(Array.from({length: 12}, async () => {
      while (cursor < entries.length) {
        const index = cursor++;
        const entry = entries[index];
        const source = path.join(inventory.root, entry.path);
        const before = await fsp.stat(source);
        if (!before.isFile() || before.size !== entry.bytes) throw new Error(`Source changed: ${entry.path}`);
        if (entry.bytes < threshold) {
          const local = path.join(repo, prefix, entry.path);
          const [original, staged] = await Promise.all([digest(source, entry.bytes), digest(local, entry.bytes, true)]);
          if (original.sha256 !== staged.sha256) throw new Error(`Copy mismatch: ${entry.path}`);
          output[index] = {path: `${prefix}/${entry.path}`, bytes: entry.bytes, ...staged, storage: 'git'};
        } else {
          const temporary = path.join(assetsDir, `staging-${index}.partial`);
          const hash = crypto.createHash('sha256');
          let bytes = 0;
          const meter = new Transform({transform(chunk, encoding, callback) {bytes += chunk.length; hash.update(chunk); callback(null, chunk);}});
          await pipeline(fs.createReadStream(source), meter, fs.createWriteStream(temporary, {flags: 'wx'}));
          const sha256 = hash.digest('hex');
          const copied = await digest(temporary, entry.bytes);
          if (bytes !== entry.bytes || copied.sha256 !== sha256) throw new Error(`Asset copy mismatch: ${entry.path}`);
          output[index] = {path: `${prefix}/${entry.path}`, bytes: entry.bytes, sha256, storage: 'release', temporary};
        }
        const after = await fsp.stat(source);
        if (before.size !== after.size || before.mtimeMs !== after.mtimeMs) throw new Error(`Source changed while reading: ${entry.path}`);
        finished++;
      }
    }));
  } finally { clearInterval(timer); }
  const assets = new Map();
  for (const entry of output) {
    if (entry.storage !== 'release') continue;
    let asset = assets.get(entry.sha256);
    if (!asset) {
      const basename = path.basename(entry.path).replace(/[^a-zA-Z0-9._-]/g, '_');
      const name = `${entry.sha256.slice(0,16)}-${basename}`;
      asset = {name, bytes: entry.bytes, sha256: entry.sha256, downloadUrl: `https://github.com/${repository}/releases/download/${tag}/${name}`, paths: []};
      await fsp.rename(entry.temporary, path.join(assetsDir, name));
      assets.set(entry.sha256, asset);
    } else {
      await fsp.unlink(entry.temporary);
    }
    asset.paths.push(entry.path);
    delete entry.temporary;
    entry.asset = asset.name;
  }
  const summary = {
    files: output.length,
    bytes: output.reduce((n,e) => n+e.bytes, 0),
    gitFiles: output.filter(e => e.storage === 'git').length,
    gitBytes: output.filter(e => e.storage === 'git').reduce((n,e) => n+e.bytes, 0),
    releasePaths: output.filter(e => e.storage === 'release').length,
    releaseUniqueAssets: assets.size,
    releaseUniqueBytes: [...assets.values()].reduce((n,e) => n+e.bytes, 0)
  };
  const manifest = {schemaVersion: 1, createdAt: new Date().toISOString(), repository, sourceRoot: prefix, releaseTag: tag, releaseUrl: `https://github.com/${repository}/releases/tag/${tag}`, thresholdBytes: threshold, summary, assets: [...assets.values()], files: output};
  await fsp.writeFile(path.join(repo, 'iflytek-manifest-sha256.json'), JSON.stringify(manifest, null, 2)+'\n');
  console.log(JSON.stringify(summary, null, 2));
}
main().catch(error => {console.error(error.message); process.exitCode = 1;});
