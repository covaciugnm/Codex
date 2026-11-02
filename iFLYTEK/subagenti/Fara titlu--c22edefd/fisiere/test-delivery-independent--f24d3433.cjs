'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pack,restore,checkedManifest,objectMap}=require('../../tools/deliver-decompilation-repair-20261101.cjs');
const root=fs.mkdtempSync('D:/independent-repair-delivery-'),meta=path.join(root,'meta'),source=path.join(root,'source'),target=path.join(root,'target'),sha=b=>crypto.createHash('sha256').update(b).digest('hex');fs.mkdirSync(meta);fs.mkdirSync(path.join(source,'cas'),{recursive:true});
const values=[Buffer.from('independent repair delivery'),Buffer.alloc(513,71),Buffer.alloc(1000000,83)],objects=values.map(b=>({sha256:sha(b),bytes:b.length}));for(let i=0;i<values.length;i++)fs.writeFileSync(path.join(source,'cas',objects[i].sha256),values[i]);
const save=items=>fs.writeFileSync(path.join(meta,'cas-index.json'),JSON.stringify({schemaVersion:1,objects:items}));save(objects);
const results=[];async function test(name,fn){try{await fn();results.push({name,status:'PASS'});}catch(e){results.push({name,status:'FAIL',error:e.message});}}
async function rejects(fn){try{await fn();}catch{return;}throw Error('Invalid input accepted');}
(async()=>{
 await test('reject already archived content',()=>rejects(()=>pack(meta,source,{prior:new Map([[objects[0].sha256,objects[0].bytes]])})));
 await test('reject duplicate object metadata',()=>rejects(()=>objectMap([objects[0],objects[0]])));
 let manifest;await test('valid packing and exact byte restoration',async()=>{manifest=await pack(meta,source,{prior:new Map()});fs.mkdirSync(path.join(target,'packs'),{recursive:true});for(const p of manifest.packs)fs.copyFileSync(path.join(source,'packs',p.name),path.join(target,'packs',p.name));await restore(meta,target,{localOnly:true});for(const o of objects){const b=fs.readFileSync(path.join(target,'cas',o.sha256));if(b.length!==o.bytes||sha(b)!==o.sha256)throw Error('Roundtrip mismatch');}});
 await test('repeat packaging deterministic',async()=>{const again=await pack(meta,source,{prior:new Map()});if(JSON.stringify(again)!==JSON.stringify(manifest))throw Error('Nondeterministic pack');});
 await test('restoration idempotent',async()=>{if((await restore(meta,target,{localOnly:true})).restoredObjects!==0)throw Error('Redundant restore');});
 await test('wrong repository metadata rejected',()=>rejects(()=>checkedManifest({...manifest,repository:'other/repo'})));
 await test('path traversal pack rejected',()=>{const m=structuredClone(manifest);m.packs[0].name='../escape.tar.gz';return rejects(()=>checkedManifest(m));});
 await test('index disagreement rejected',async()=>{save(objects.slice(1));await rejects(()=>restore(meta,target,{localOnly:true}));save(objects);});
 await test('corrupt pack rejected',async()=>{const dest=path.join(root,'corrupt');fs.mkdirSync(path.join(dest,'packs'),{recursive:true});fs.writeFileSync(path.join(dest,'packs',manifest.packs[0].name),'corrupt');await rejects(()=>restore(meta,dest,{localOnly:true}));});
 const result={checkedAt:new Date().toISOString(),scope:'Data-only delivery helper; isolated synthetic objects, no real payload packaged or published',status:results.every(r=>r.status==='PASS')?'PASS':'FAIL',passed:results.filter(r=>r.status==='PASS').length,total:results.length,helperSha256:sha(fs.readFileSync(path.resolve(__dirname,'../../tools/deliver-decompilation-repair-20261101.cjs'))),results};fs.writeFileSync(path.join(__dirname,'DELIVERY-HELPER-RESULTS.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));if(result.status!=='PASS')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
