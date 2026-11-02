'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..'),base=path.join(root,'collection-2026-11-01');
const {records}=JSON.parse(fs.readFileSync(path.join(base,'manifest.json'),'utf8'));
const restore=process.argv.includes('--restore'),remote=process.argv.includes('--remote'),gitOnly=process.argv.includes('--git-only');
function hash(file){return new Promise((resolve,reject)=>{const h=crypto.createHash('sha256'),s=fs.createReadStream(file);s.on('data',d=>h.update(d));s.on('error',reject);s.on('end',()=>resolve(h.digest('hex')));});}
(async()=>{
 let count=0;for(const r of records.filter(r=>r.file)){
  const file=path.resolve(base,r.file);if(!file.startsWith(base+path.sep))throw Error('Unsafe manifest path');
  if(gitOnly&&r.storage==='release')continue;
  if(restore&&!fs.existsSync(file)&&r.storage==='release'){fs.mkdirSync(path.dirname(file),{recursive:true});execFileSync('gh',['release','download',r.releaseTag,'--repo','covaciugnm/iFLYTEK','--pattern',r.assetName,'--dir',path.dirname(file)],{stdio:'inherit'});}
  if(fs.statSync(file).size!==r.bytes||await hash(file)!==r.sha256)throw Error('Integrity mismatch: '+r.file);count++;
 }
 if(remote){const release=JSON.parse(execFileSync('gh',['release','view','iflytek-software-2026-11-01','--repo','covaciugnm/iFLYTEK','--json','assets'],{encoding:'utf8'}));for(const r of records.filter(r=>r.storage==='release')){const a=release.assets.find(a=>a.name===r.assetName);if(!a||a.size!==r.bytes||a.digest!=='sha256:'+r.sha256)throw Error('GitHub asset mismatch: '+r.file);}}
 console.log(JSON.stringify({verifiedFiles:count,githubReleaseVerified:remote}));
})().catch(e=>{console.error(e);process.exitCode=1;});
