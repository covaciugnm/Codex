'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {pack,restore,objectMap,checkedManifest}=require('./deliver-decompilation-repair-20261101.cjs');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
async function main(){
 const base=fs.mkdtempSync('D:/iflytek-repair-delivery-fixture-'),meta=path.join(base,'metadata'),source=path.join(base,'source'),target=path.join(base,'restored');fs.mkdirSync(meta);fs.mkdirSync(path.join(source,'cas'),{recursive:true});
 const values=[Buffer.from('verified fixture\n'),Buffer.alloc(0)],objects=values.map(b=>({sha256:hash(b),bytes:b.length}));for(let i=0;i<values.length;i++)fs.writeFileSync(path.join(source,'cas',objects[i].sha256),values[i]);
 const index={schemaVersion:1,objects},saveIndex=()=>fs.writeFileSync(path.join(meta,'cas-index.json'),JSON.stringify(index));saveIndex();
 const checks=[];const pass=n=>checks.push({name:n,status:'PASS'});
 assert.throws(()=>objectMap([objects[0],objects[0]]),/duplicate/);pass('duplicate objects rejected');
 assert.throws(()=>objectMap([{sha256:'../outside',bytes:1}]),/Invalid/);pass('nonhash object paths rejected');
 await assert.rejects(pack(meta,source,{prior:new Map([[objects[0].sha256,objects[0].bytes]])}),/Previously archived/);pass('previous archive objects rejected');
 fs.writeFileSync(path.join(source,'cas',objects[0].sha256),'corrupt');await assert.rejects(pack(meta,source,{prior:new Map()}),/integrity/);fs.writeFileSync(path.join(source,'cas',objects[0].sha256),values[0]);pass('corrupt CAS rejected before packaging');
 const m=await pack(meta,source,{prior:new Map()});assert.equal(m.objects,2);pass('pack includes empty and nonempty objects');
 const evil=structuredClone(m);evil.packs[0].name='../escape.tar.gz';assert.throws(()=>checkedManifest(evil),/Invalid pack/);pass('pack path traversal rejected');
 const repeated=structuredClone(m);repeated.packs.push(repeated.packs[0]);assert.throws(()=>checkedManifest(repeated),/Invalid pack/);pass('repeated pack rejected');
 const totals=structuredClone(m);totals.objectBytes++;assert.throws(()=>checkedManifest(totals),/totals/);pass('inconsistent totals rejected');
 await assert.rejects(restore(meta,target,{localOnly:true}),/Missing local pack/);pass('local-only does not download absent pack');
 fs.mkdirSync(path.join(target,'packs'),{recursive:true});for(const p of m.packs)fs.copyFileSync(path.join(source,'packs',p.name),path.join(target,'packs',p.name));
 const result=await restore(meta,target,{localOnly:true});assert.equal(result.verifiedObjects,2);for(let i=0;i<values.length;i++)assert.deepEqual(fs.readFileSync(path.join(target,'cas',objects[i].sha256)),values[i]);pass('local round trip verifies exact bytes');
 assert.equal((await restore(meta,target,{localOnly:true})).restoredObjects,0);pass('verified restoration is idempotent');
 const badTarget=path.join(base,'corrupt-pack');fs.mkdirSync(path.join(badTarget,'packs'),{recursive:true});fs.writeFileSync(path.join(badTarget,'packs',m.packs[0].name),'broken');await assert.rejects(restore(meta,badTarget,{localOnly:true}),/checksum/);pass('corrupt pack rejected before extraction');
 index.objects=[objects[0]];saveIndex();await assert.rejects(restore(meta,target,{localOnly:true}),/differs/);pass('pack and CAS indexes must agree');
 console.log(JSON.stringify({fixture:base,checks,passed:checks.length},null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
