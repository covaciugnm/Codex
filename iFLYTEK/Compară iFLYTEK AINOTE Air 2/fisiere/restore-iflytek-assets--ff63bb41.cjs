#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const fsp = fs.promises;
const path = require('node:path');
const {spawn} = require('node:child_process');
const {root, resolveInside, loadManifest, check} = require('./iflytek-snapshot.cjs');
async function run(command, args) {
  await new Promise((resolve, reject) => {
    const child = spawn(command, args, {stdio: 'inherit', windowsHide: true, shell: false});
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`${command} exited with ${code}`)));
  });
}
async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('node tools/restore-iflytek-assets.cjs [--from-dir DIRECTORY]\nRequires Node.js 18+ and gh authenticated with read access to the private repository.\nWith --from-dir, uses already downloaded release assets and does not access the network.\nExisting files are checked; differing files are never overwritten.');
    return;
  }
  if (args.length && !(args.length === 2 && args[0] === '--from-dir')) throw new Error('Unknown arguments; use --help');
  const from = args.length ? path.resolve(args[1]) : null;
  const manifest = loadManifest();
  let restored = 0, present = 0;
  for (const asset of manifest.assets) {
    const entries = manifest.files.filter(f => f.storage === 'release' && f.asset === asset.name);
    const missing = [];
    for (const entry of entries) {
      const destination = resolveInside(root, entry.path);
      try {await fsp.lstat(destination);}
      catch (error) {if (error.code === 'ENOENT') {missing.push(entry); continue;} throw error;}
      await check(destination, entry);
      present++;
    }
    if (!missing.length) continue;
    let temporary;
    try {
      let source;
      if (from) source = resolveInside(from, asset.name);
      else {
        temporary = await fsp.mkdtemp(path.join(root, '.iflytek-download-'));
        console.log(`Downloading ${asset.name} (${asset.bytes} bytes)`);
        await run('gh', ['release', 'download', manifest.releaseTag, '--repo', manifest.repository, '--pattern', asset.name, '--dir', temporary]);
        source = resolveInside(temporary, asset.name);
      }
      await check(source, asset);
      for (const entry of missing) {
        const destination = resolveInside(root, entry.path);
        await fsp.mkdir(path.dirname(destination), {recursive: true});
        await fsp.copyFile(source, destination, fs.constants.COPYFILE_EXCL);
        await check(destination, entry);
        restored++;
        console.log(`Restored: ${entry.path}`);
      }
    } finally {
      if (temporary) {
        // Only the newly created, single-asset download directory is removed.
        await fsp.rm(resolveInside(temporary, asset.name), {force: true});
        await fsp.rmdir(temporary);
      }
    }
  }
  console.log(JSON.stringify({restored, alreadyPresent: present, releasePaths: restored + present}, null, 2));
}
main().catch(error => {console.error(error.message); process.exitCode = 1;});
