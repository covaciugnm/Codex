'use strict';
const fs = require('node:fs');
const {execFileSync} = require('node:child_process');
const root = 'D:/CodexWork/iFLYTEK-publish-20261031';
const manifest = JSON.parse(fs.readFileSync(root+'/iflytek-manifest-sha256.json', 'utf8'));
const raw = execFileSync('git', ['-C',root,'ls-files','--stage','-z'], {encoding: 'utf8',maxBuffer: 30*1024*1024});
const index = new Map(raw.split('\0').filter(Boolean).map(line => {const [info,name] = line.split('\t'); return [name,info.split(' ')[1]];}));
for (const file of manifest.files) {
  if (file.storage === 'git' && index.get(file.path) !== file.gitBlobSha1) throw new Error(`Git bytes differ: ${file.path}`);
  if (file.storage === 'release' && index.has(file.path)) throw new Error(`Large asset staged: ${file.path}`);
}
const originals = [...index.keys()].filter(p => p.startsWith(manifest.sourceRoot+'/'));
if (originals.length !== manifest.summary.gitFiles) throw new Error('Unexpected staged original file count');
const oldTree = execFileSync('git', ['-C',root,'rev-parse','HEAD:AI_Glasses_2026'], {encoding:'utf8'}).trim();
const stagedTree = execFileSync('git', ['-C',root,'write-tree'], {encoding:'utf8'}).trim();
const newTree = execFileSync('git', ['-C',root,'rev-parse',stagedTree+':AI_Glasses_2026'], {encoding:'utf8'}).trim();
if (oldTree !== newTree) throw new Error('Existing AI_Glasses_2026 content changed');
console.log(JSON.stringify({originalGitFilesVerified: originals.length, releasePathsExcludedFromGit: manifest.summary.releasePaths, existingCatalogTreePreserved: oldTree, stagedTree},null,2));
