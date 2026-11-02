#!/usr/bin/env node
'use strict';
const {root, resolveInside, loadManifest, check} = require('./iflytek-snapshot.cjs');
async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {console.log('node tools/verify-iflytek-snapshot.cjs [--git-only]'); return;}
  if (args.some(a => a !== '--git-only')) throw new Error('Unknown argument');
  const manifest = loadManifest();
  const files = manifest.files.filter(f => !args.includes('--git-only') || f.storage === 'git');
  const errors = [];
  let next = 0, checked = 0;
  await Promise.all(Array.from({length: 8}, async () => {
    while (next < files.length) {
      const file = files[next++];
      try {await check(resolveInside(root, file.path), file); checked++;}
      catch (error) {errors.push({path: file.path, error: error.message});}
    }
  }));
  console.log(JSON.stringify({mode: args.includes('--git-only') ? 'git-only' : 'complete', expected: files.length, checked, failed: errors.length, errors: errors.slice(0,30)}, null, 2));
  if (errors.length) process.exitCode = 1;
}
main().catch(error => {console.error(error.message); process.exitCode = 1;});
