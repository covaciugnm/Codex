'use strict';
// Fetches only Git blobs explicitly referenced by the Android analysis manifests.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const repo=path.resolve(__dirname,'..'),root=path.join(repo,'apk-analysis-2026-11-01');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
function main(){
 const catalog=read(path.join(root,'catalog.json')),paths=new Set(),pointers=[],decomp=new Set();
 function collect(entries){for(const r of entries||[]){const e=r.storage==='existing'?r.existing:null;if(e?.path&&(!e.storage||e.storage==='git')){paths.add(e.path);pointers.push(e);}}}
 for(const v of catalog.versions){const m=read(path.join(root,v.manifest));collect(m.entries);collect(m.outerEntries);for(const c of m.decompilation?.components||[])decomp.add(c.manifest);}
 for(const file of decomp){const d=read(path.join(root,file));collect(d.entries);collect(d.logs);}
 const tree=cp.execFileSync('git',['ls-tree','-rz','HEAD'],{cwd:repo,maxBuffer:128*1024*1024,windowsHide:true}).toString('utf8'),byPath=new Map();
 for(const item of tree.split('\0')){const m=/^[0-7]{6} blob ([a-f0-9]{40})\t([\s\S]+)$/.exec(item);if(m)byPath.set(m[2],m[1]);}
 const ids=new Set();for(const e of pointers){const id=e.gitBlobSha1||byPath.get(e.path);if(!id||!/^[a-f0-9]{40}$/.test(id))throw Error('Missing/invalid Git blob pointer '+e.path);ids.add(id);}
 const list=[...ids],check=cp.spawnSync('git',['cat-file','--batch-check=%(objectname) %(objecttype)'],{cwd:repo,input:list.join('\n')+'\n',encoding:'utf8',env:{...process.env,GIT_NO_LAZY_FETCH:'1'},maxBuffer:128*1024*1024,windowsHide:true});if(check.status!==0)throw Error(check.stderr);
 const missing=check.stdout.split('\n').filter(s=>s.endsWith(' missing')).map(s=>s.split(' ')[0]);
 if(missing.length){const result=cp.spawnSync('git',['fetch','--no-tags','--no-write-fetch-head','--recurse-submodules=no','--filter=blob:none','--stdin','origin'],{cwd:repo,input:missing.join('\n')+'\n',encoding:'utf8',maxBuffer:128*1024*1024,windowsHide:true});if(result.status!==0)throw Error(result.stderr||'Git blob fetch failed');}
 console.log(JSON.stringify({paths:paths.size,uniqueGitBlobs:ids.size,fetched:missing.length}));
}
if(require.main===module)try{main();}catch(e){console.error(e);process.exitCode=1;}
