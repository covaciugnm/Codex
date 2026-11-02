'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {zipEntries}=require('./inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'..'),root=path.join(repo,'apk-analysis-2026-11-01'),work=process.env.IFLYTEK_APK_WORK_ROOT||path.join(root,'.work');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function get(release,asset,folder,repository='covaciugnm/iFLYTEK'){fs.mkdirSync(folder,{recursive:true});const r=cp.spawnSync('gh',['release','download',release,'--repo',repository,'--pattern',asset,'--dir',folder],{stdio:'inherit',windowsHide:true});if(r.status!==0)throw Error('Could not download '+asset);}
const catalog=JSON.parse(fs.readFileSync(path.join(root,'catalog.json')));
for(const v of catalog.versions){const m=JSON.parse(fs.readFileSync(path.join(root,v.manifest))),r=m.source.references[0],name=r.asset||path.basename(r.path),p=path.join(work,'inputs',name);fs.mkdirSync(path.dirname(p),{recursive:true});
 if(!fs.existsSync(p)){
  const local=r.path?path.join(repo,r.path):null;if(local&&fs.existsSync(local))fs.copyFileSync(local,p);
  else if(r.storage==='release')get(r.release,r.asset,path.dirname(p));
  else {if(r.gitBlobSha1&&!/^[a-f0-9]{40}$/.test(r.gitBlobSha1))throw Error('Invalid Git blob ID');const x=cp.spawnSync('git',['show',r.gitBlobSha1||'HEAD:'+r.path],{cwd:repo,encoding:null,maxBuffer:512*1024*1024,windowsHide:true});if(x.status!==0)throw Error('Missing source Git file '+r.path);fs.writeFileSync(p,x.stdout);}
 }
 const b=fs.readFileSync(p);if(b.length!==m.source.bytes||hash(b)!==m.source.sha256)throw Error('Input integrity mismatch '+p);console.log('Verified input',name);
}
const t=JSON.parse(fs.readFileSync(path.join(root,'toolchain.json'))),zip=path.join(work,'jadx-1.5.6.zip');if(!fs.existsSync(zip))get('v1.5.6','jadx-1.5.6.zip',work,'skylot/jadx');const b=fs.readFileSync(zip);if(hash(b)!==t.jadx.archiveSha256)throw Error('Tool archive mismatch');
const e=zipEntries(b).find(e=>e.name==='lib/jadx-1.5.6-all.jar');if(!e)throw Error('Missing CLI JAR');const jar=e.read();if(hash(jar)!==t.jadx.jarSha256)throw Error('Tool JAR mismatch');const p=path.join(work,'jadx/lib/jadx-1.5.6-all.jar');fs.mkdirSync(path.dirname(p),{recursive:true});if(!fs.existsSync(p))fs.writeFileSync(p,jar);else if(hash(fs.readFileSync(p))!==t.jadx.jarSha256)throw Error('Existing CLI JAR differs');console.log('Verified JADX 1.5.6 toolchain.');
