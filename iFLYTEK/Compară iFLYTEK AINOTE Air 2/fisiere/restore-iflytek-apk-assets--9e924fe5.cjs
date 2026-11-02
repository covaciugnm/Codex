#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const fsp = fs.promises;
const path = require('node:path');
const {spawn} = require('node:child_process');
const {root, resolveInside, check} = require('./iflytek-snapshot.cjs');
const project = 'iFLYTEK_XF-AIGlasses-01_Documentatie/Software/APK_Recompilabil_2026-10-31';

async function run(args) {
  await new Promise((resolve, reject) => {
    const child = spawn('gh', args, {stdio: 'inherit', windowsHide: true, shell: false});
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(Error(`gh exited with ${code}`)));
  });
}

async function main() {
  let from = null, apkOnly = false;
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--help') {
      console.log('node tools/restore-iflytek-apk-assets.cjs [--apk-only] [--from-dir DIRECTORY]\nDownloads the new APK/source/analysis/toolchain release, checks SHA-256 and restores project/dist.\n--apk-only restores the two signed APKs; --from-dir uses local files without networking.\nNode.js 18+; gh authenticated for the private repo when downloading. Different existing files are never overwritten.');
      return;
    }
    if (args[i] === '--apk-only') apkOnly = true;
    else if (args[i] === '--from-dir' && args[i + 1]) from = path.resolve(args[++i]);
    else throw Error('Unknown or incomplete argument; use --help');
  }
  const manifest = JSON.parse(await fsp.readFile(path.join(root, project, 'release-assets.json'), 'utf8'));
  if (manifest.schemaVersion !== 1 || manifest.repository !== 'covaciugnm/iFLYTEK' || manifest.releaseTag !== 'iflytek-apk-romania40-2026-10-31' || !Array.isArray(manifest.assets)) throw Error('Unsupported APK manifest');
  const seen = new Set();
  for (const asset of manifest.assets) {
    if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]+$/.test(asset.name) || seen.has(asset.name) || !/^[a-f0-9]{64}$/.test(asset.sha256) || !Number.isSafeInteger(asset.bytes) || asset.bytes < 1 || asset.path !== `${project}/dist/${asset.name}`) throw Error('Invalid APK asset');
    resolveInside(root, asset.path);
    seen.add(asset.name);
  }
  let restored = 0, present = 0;
  for (const asset of manifest.assets.filter(a => !apkOnly || a.name.endsWith('.apk'))) {
    const destination = resolveInside(root, asset.path);
    let exists = true;
    try {await fsp.lstat(destination);} catch (error) {if (error.code === 'ENOENT') exists = false; else throw error;}
    if (exists) {
      await check(destination, asset);
      present++;
    } else {
      let temporary;
      try {
        const sourceDir = from || (temporary = await fsp.mkdtemp(path.join(root, '.iflytek-download-')));
        if (!from) {
          console.log(`Downloading ${asset.name} (${asset.bytes} bytes)`);
          await run(['release', 'download', manifest.releaseTag, '--repo', manifest.repository, '--pattern', asset.name, '--dir', sourceDir]);
        }
        const source = resolveInside(sourceDir, asset.name);
        await check(source, asset);
        await fsp.mkdir(path.dirname(destination), {recursive: true});
        await fsp.copyFile(source, destination, fs.constants.COPYFILE_EXCL);
        await check(destination, asset);
        restored++;
      } finally {
        if (temporary) {
          await fsp.rm(resolveInside(temporary, asset.name), {force: true});
          await fsp.rmdir(temporary);
        }
      }
    }
    const sidecar = `${asset.sha256}  ${asset.name}\n`;
    try {await fsp.writeFile(destination + '.sha256', sidecar, {flag: 'wx'});}
    catch (error) {
      if (error.code !== 'EEXIST') throw error;
      const existing = (await fsp.readFile(destination + '.sha256', 'utf8')).replace(/^\uFEFF/, '').replace(/\r\n/g, '\n');
      if (existing !== sidecar) throw Error(`Different existing checksum: ${destination}.sha256`);
    }
    console.log(`Verified: ${asset.name}`);
  }
  console.log(JSON.stringify({restored, alreadyPresent: present, checked: restored + present}));
}
main().catch(error => {console.error(error.message); process.exitCode = 1;});
