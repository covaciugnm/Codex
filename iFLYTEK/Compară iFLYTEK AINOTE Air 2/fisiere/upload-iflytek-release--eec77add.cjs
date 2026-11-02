'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');
const {check} = require('./iFLYTEK-publish-20261031/tools/iflytek-snapshot.cjs');
const root = 'D:/CodexWork/iFLYTEK-publish-20261031';
const assetsDir = 'D:/CodexWork/iflytek-release-assets-20261031';
const manifest = JSON.parse(fs.readFileSync(root+'/iflytek-manifest-sha256.json','utf8'));
function gh(args) {
  return new Promise((resolve,reject) => {
    const child = spawn('gh',args,{windowsHide:true,shell:false});
    let out='', err='';
    child.stdout.on('data',chunk => out+=chunk);
    child.stderr.on('data',chunk => err+=chunk);
    child.on('error',reject);
    child.on('exit',code => code===0 ? resolve(out) : reject(new Error(`gh ${args.slice(0,2).join(' ')}: ${err.trim() || code}`)));
  });
}
async function api(route) {return JSON.parse(await gh(['api',route]));}
async function main() {
  // Draft tags are not published Git refs yet; find the draft in the authenticated list.
  const releases = await api(`repos/${manifest.repository}/releases?per_page=100`);
  const release = releases.find(r => r.tag_name === manifest.releaseTag);
  if (!release || !release.draft) throw new Error('Expected a draft release for upload');
  const route = `repos/${manifest.repository}/releases/${release.id}/assets?per_page=100`;
  const existing = await api(route);
  let cursor=0, completed=0;
  await Promise.all(Array.from({length:2},async () => {
    while (cursor < manifest.assets.length) {
      const asset = manifest.assets[cursor++];
      const present = existing.find(a => a.name === asset.name);
      if (present) {
        if (present.size !== asset.bytes || present.digest !== 'sha256:'+asset.sha256 || present.state !== 'uploaded') throw new Error(`Existing asset differs: ${asset.name}`);
        completed++;
        console.log(`Already uploaded ${completed}/${manifest.assets.length}: ${asset.name}`);
        continue;
      }
      await check(path.join(assetsDir,asset.name),asset);
      console.log(`Uploading: ${asset.name} (${asset.bytes} bytes)`);
      await gh(['release','upload',manifest.releaseTag,path.join(assetsDir,asset.name),'--repo',manifest.repository]);
      completed++;
      console.log(`Uploaded ${completed}/${manifest.assets.length}: ${asset.name}`);
    }
  }));
  const remote = await api(route);
  const results=[];
  for (const asset of manifest.assets) {
    const found = remote.find(a => a.name === asset.name);
    if (!found || found.size !== asset.bytes || found.state !== 'uploaded') throw new Error(`Missing or incomplete remote asset: ${asset.name}`);
    let verification = 'github-sha256';
    if (found.digest) {
      if (found.digest !== 'sha256:'+asset.sha256) throw new Error(`Remote SHA-256 mismatch: ${asset.name}`);
    } else {
      verification = 'download-sha256';
      const downloadDir = await fs.promises.mkdtemp('D:/CodexWork/iflytek-verify-download-');
      await gh(['release','download',manifest.releaseTag,'--repo',manifest.repository,'--pattern',asset.name,'--dir',downloadDir]);
      const file = path.join(downloadDir,asset.name);
      await check(file,asset);
      await fs.promises.unlink(file);
      await fs.promises.rmdir(downloadDir);
    }
    results.push({name:asset.name,id:found.id,bytes:found.size,sha256:asset.sha256,verification});
  }
  if (remote.length !== manifest.assets.length) throw new Error('Unexpected release asset count');
  const report={checkedAt:new Date().toISOString(),repository:manifest.repository,releaseId:release.id,tag:manifest.releaseTag,files:manifest.summary.files,pathsInRelease:manifest.summary.releasePaths,assets:results};
  await fs.promises.writeFile('D:/CodexWork/iflytek-upload-verification-20261031.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({releaseId:release.id,verifiedAssets:results.length,verifiedBytes:results.reduce((n,a)=>n+a.bytes,0),allDigestsVerified:true},null,2));
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
