'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
function resolveInside(base, relative) {
  if (typeof relative !== 'string' || !relative || relative.includes('\\') || relative.includes(':') || relative.split('/').some(s => !s || s === '..' || s === '.')) throw new Error('Unsafe manifest path');
  const target = path.resolve(base, relative);
  if (!target.startsWith(path.resolve(base) + path.sep)) throw new Error('Path outside destination');
  return target;
}
function loadManifest() {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'iflytek-manifest-sha256.json'), 'utf8'));
  if (manifest.schemaVersion !== 1 || manifest.repository !== 'covaciugnm/iFLYTEK' || manifest.sourceRoot !== 'iFLYTEK_XF-AIGlasses-01_Documentatie') throw new Error('Unsupported snapshot');
  const names = new Set();
  for (const file of manifest.files) {
    resolveInside(root, file.path);
    if (!file.path.startsWith(manifest.sourceRoot + '/') || names.has(file.path) || !Number.isSafeInteger(file.bytes) || file.bytes < 0 || !/^[a-f0-9]{64}$/.test(file.sha256) || !['git','release'].includes(file.storage)) throw new Error('Invalid manifest entry');
    names.add(file.path);
  }
  for (const asset of manifest.assets) {
    if (!/^[a-f0-9]{16}-[a-zA-Z0-9._-]+$/.test(asset.name) || !/^[a-f0-9]{64}$/.test(asset.sha256)) throw new Error('Invalid asset');
    for (const item of manifest.files.filter(f => f.asset === asset.name)) {
      if (item.sha256 !== asset.sha256 || item.bytes !== asset.bytes) throw new Error('Inconsistent asset mapping');
    }
  }
  for (const file of manifest.files.filter(f => f.storage === 'release')) {
    if (!manifest.assets.some(a => a.name === file.asset)) throw new Error('Missing release asset');
  }
  return manifest;
}
async function check(file, entry) {
  const stat = await fs.promises.lstat(file);
  if (!stat.isFile() || stat.size !== entry.bytes) throw new Error(`Size/type mismatch: ${file}`);
  const hash = crypto.createHash('sha256');
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  if (hash.digest('hex') !== entry.sha256) throw new Error(`SHA-256 mismatch: ${file}`);
}
module.exports = {root, resolveInside, loadManifest, check};
