'use strict';
const fs=require('node:fs'),path=require('node:path'),zlib=require('node:zlib'),crypto=require('node:crypto');
const {header}=require('../../tools/package-apk-analysis-20261101.cjs');
const {unpack}=require('../../tools/restore-apk-analysis-20261101.cjs');
const root=path.resolve(__dirname,'../.work/audit-fixture');fs.mkdirSync(root,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const inputs=[Buffer.alloc(0),Buffer.from('a'),Buffer.alloc(513,37),Buffer.alloc(1000000,83)];
function tar(data,end=true){return Buffer.concat([...data.flatMap(b=>[header('cas/'+sha(b),b.length),b,Buffer.alloc((512-b.length%512)%512)]),...(end?[Buffer.alloc(1024)]:[])]);}
const objects=inputs.map(b=>({sha256:sha(b),bytes:b.length}));
const valid=tar(inputs),one=tar([inputs[1]]),cases=[
 {name:'valid-multiple-boundaries',tar:valid,objects,reject:false},
 {name:'valid-existing-identical',tar:valid,objects,reject:false,target:'valid-multiple-boundaries'},
 {name:'truncated-body',tar:one.subarray(0,512),objects:[objects[1]],reject:true},
 {name:'missing-padding',tar:one.subarray(0,513),objects:[objects[1]],reject:true},
 {name:'missing-eof',tar:tar([inputs[1]],false),objects:[objects[1]],reject:true},
 {name:'partial-next-header',tar:Buffer.concat([tar([inputs[1]],false),Buffer.alloc(13,5)]),objects:[objects[1]],reject:true},
 {name:'unlisted-object',tar:one,objects:[],reject:true},
 {name:'duplicate-object',tar:tar([inputs[1],inputs[1]]),objects:[objects[1]],reject:true},
 {name:'invalid-checksum',tar:Buffer.from(one),objects:[objects[1]],reject:true},
 {name:'corrupt-body',tar:Buffer.from(one),objects:[objects[1]],reject:true},
 {name:'path-traversal',tar:Buffer.concat([header('../escape',1),inputs[1],Buffer.alloc(511),Buffer.alloc(1024)]),objects:[objects[1]],reject:true},
 {name:'truncated-gzip',tar:valid,objects,reject:true,truncatedGzip:true}
];
cases.find(x=>x.name==='invalid-checksum').tar[100]^=1;
cases.find(x=>x.name==='corrupt-body').tar[512]^=1;
(async()=>{const results=[];for(const c of cases){
 const dest=path.join(root,c.target||c.name),p=path.join(root,c.name+'.tar.gz');let gz=zlib.gzipSync(c.tar);if(c.truncatedGzip)gz=gz.subarray(0,gz.length-10);fs.writeFileSync(p,gz);let error=null,count=null;
 try{count=await unpack(p,{name:c.name,objects:c.objects},dest);}catch(e){error=e.message;}
 let validOutputs=true;if(!c.reject&&!error)for(const o of c.objects){const b=fs.readFileSync(path.join(dest,'cas',o.sha256));if(b.length!==o.bytes||sha(b)!==o.sha256)validOutputs=false;}
 const pass=Boolean(error)===c.reject&&validOutputs;results.push({name:c.name,expectedRejection:c.reject,error,count,pass});
 }fs.writeFileSync(path.join(__dirname,'restore-fixture-results.json'),JSON.stringify({checkedAt:new Date().toISOString(),cases:results,passed:results.filter(x=>x.pass).length,total:results.length},null,2)+'\n');console.log(JSON.stringify(results,null,2));if(results.some(x=>!x.pass))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
