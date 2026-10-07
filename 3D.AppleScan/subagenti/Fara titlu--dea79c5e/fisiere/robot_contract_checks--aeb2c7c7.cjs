'use strict';
// Offline executable specification. No ROS, iOS, network or hardware execution.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8').replace(/^\uFEFF/,''));
const schema=read('03_contracte/transport.schema.json'),samples=read('03_contracte/protocol_samples.json');
const cases=[];function test(name,fn){try{fn();cases.push({name,status:'pass'});}catch(e){cases.push({name,status:'fail',detail:e.message});}}
// Deliberately limited to keywords emitted by this schema; unknown keywords fail.
// This is not an independently certified general JSON Schema 2020-12 engine.
const supported=new Set(['$schema','$id','title','$defs','$ref','type','properties','required','additionalProperties','enum','const','pattern','minimum','maximum','minItems','maxItems','items','oneOf','allOf','if','then']);
function validate(s,v){for(const k of Object.keys(s))assert(supported.has(k),'unsupported keyword '+k);if(s.$ref)return validate(schema.$defs[s.$ref.split('/').pop()],v);
 if(s.type){const ok=s.type==='null'?v===null:s.type==='array'?Array.isArray(v):s.type==='object'?v!==null&&typeof v==='object'&&!Array.isArray(v):s.type==='integer'?Number.isSafeInteger(v):s.type==='number'?typeof v==='number'&&Number.isFinite(v):typeof v===s.type;assert(ok,'type '+s.type);}
 if(s.const!==undefined)assert.deepEqual(v,s.const);if(s.enum)assert(s.enum.includes(v),'enum');if(s.pattern)assert(new RegExp(s.pattern).test(v),'pattern');
 if(s.minimum!==undefined)assert(v>=s.minimum,'minimum');if(s.maximum!==undefined)assert(v<=s.maximum,'maximum');
 if(s.minItems!==undefined)assert(v.length>=s.minItems,'minItems');if(s.maxItems!==undefined)assert(v.length<=s.maxItems,'maxItems');if(s.items)for(const x of v)validate(s.items,x);
 if(s.required)for(const k of s.required)assert(Object.hasOwn(v,k),'required '+k);
 if(s.properties&&v!==null&&typeof v==='object'){for(const[k,x]of Object.entries(v)){if(s.properties[k])validate(s.properties[k],x);else if(s.additionalProperties===false)assert.fail('extra '+k);}}
 if(s.oneOf){let n=0;for(const branch of s.oneOf)try{validate(branch,v);n++;}catch{}assert.equal(n,1,'oneOf');}
 if(s.allOf)for(const branch of s.allOf)validate(branch,v);if(s.if){let matched=true;try{validate(s.if,v);}catch{matched=false;}if(matched&&s.then)validate(s.then,v);}return true;
}
const jcs=x=>x===null||typeof x!=='object'?JSON.stringify(x):Array.isArray(x)?'['+x.map(jcs).join(',')+']':'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+jcs(x[k])).join(',')+'}';
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const uint=x=>{assert(/^(0|[1-9][0-9]*)$/.test(x));const n=BigInt(x);assert(n<=18446744073709551615n);return n;};
const sint=x=>{assert(/^(0|-?[1-9][0-9]*)$/.test(x));const n=BigInt(x);assert(n>=-9223372036854775808n&&n<=9223372036854775807n);return n;};
const norm=a=>Math.sqrt(a.reduce((s,v)=>s+v*v,0));
function semantic(m){validate(schema,m);for(const k of ['sequence','map_epoch','clock_epoch','uncertainty_ns'])uint(m[k]);sint(m.capture_time_ns);
 if(m.kind==='control'){const n=m.body.action==='clock_probe'?1:m.body.action==='clock_reply'?3:0;assert.equal(m.body.clock_samples_ns.length,n,'clock sample count');m.body.clock_samples_ns.forEach(sint);}
 if(m.kind==='clock_model'){const b=m.body;uint(b.target_clock_epoch);uint(b.uncertainty_ns);const a=sint(b.robot_origin_ns),z=sint(b.valid_until_robot_ns);sint(b.phone_origin_ns);assert(z>a&&z-a<=2000000000n,'model TTL');}
 const b=m.body,p=b.observation?.pose||b.delta?.chunk_pose||b.camera_pose;if(p)assert(Math.abs(norm(p.quaternion_xyzw)-1)<=1e-6,'unit quaternion');
 if(b.delta){const q=b.delta;assert.equal(q.map_epoch,m.map_epoch);assert.equal(uint(q.new_revision),uint(q.base_revision)+1n);assert.equal(sha(jcs(q)),b.semantic_hash);}
 if(m.kind==='depth_frame'){assert.equal(b.payload.byte_length,b.width*b.height*4);const k=b.intrinsics_row_major;assert(k[0]>0&&k[4]>0&&k[8]===1);assert(k[1]===0&&k[3]===0&&k[6]===0&&k[7]===0);}
 return true;}
function accepted({now,stamp,u,limit,maxU,valid=true,epoch=true}){return valid&&epoch&&u>=0n&&u<=maxU&&limit>=0n&&now-stamp>=-u&&now-stamp+u<=limit;}
const mm=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((v,x,k)=>v+x*b[k][j],0)));
const mv=(a,x)=>a.map(r=>r.reduce((s,v,i)=>s+v*x[i],0));const tr=a=>a[0].map((_,i)=>a.map(r=>r[i]));
const compose=(a,b)=>({R:mm(a.R,b.R),t:mv(a.R,b.t).map((v,i)=>v+a.t[i])});const inv=a=>{const R=tr(a.R);return{R,t:mv(R,a.t).map(v=>-v)};};
const close=(a,b,eps=1e-10)=>assert(Math.max(...a.flat(Infinity).map((v,i)=>Math.abs(v-b.flat(Infinity)[i])))<eps);
const clone=x=>JSON.parse(JSON.stringify(x));
test('all metadata fixtures pass emitted schema and semantic checks',()=>samples.forEach(semantic));
test('schema rejects unknown envelope fields',()=>{const x=clone(samples[0]);x.secret=1;assert.throws(()=>semantic(x));});
test('schema rejects mismatched transport stream',()=>{const x=clone(samples[0]);x.stream_id='map';assert.throws(()=>semantic(x));});
test('schema rejects delete with geometry',()=>{const x=clone(samples[1]);x.body.delta.operation='delete';assert.throws(()=>semantic(x));});
test('uint64 boundaries and JSON number rejection',()=>{uint('18446744073709551615');assert.throws(()=>uint('18446744073709551616'));const x=clone(samples[0]);x.sequence=1;assert.throws(()=>semantic(x));});
test('int64 boundaries including negative minimum',()=>{sint('-9223372036854775808');sint('9223372036854775807');assert.throws(()=>sint('9223372036854775808'));});
test('pose quaternion rejection',()=>{const x=clone(samples[0]);x.body.observation.pose.quaternion_xyzw=[0,0,0,2];assert.throws(()=>semantic(x));});
test('ROS optical conversion and inverse',()=>{const R=[[0,0,1],[-1,0,0],[0,-1,0]];close(mv(R,[0,0,1]),[1,0,0]);close(mm(R,tr(R)),[[1,0,0],[0,1,0],[0,0,1]]);});
test('SE3 composition and inverse 1000 deterministic poses',()=>{for(let i=0;i<1000;i++){const t=i/73,R=[[Math.cos(t),-Math.sin(t),0],[Math.sin(t),Math.cos(t),0],[0,0,1]],a={R,t:[i/100,-i/77,0.5]},b={R:[[1,0,0],[0,1,0],[0,0,1]],t:[0.2,0,0.1]};const c=compose(inv(a),compose(a,b));close(c.R,b.R);close(c.t,b.t);}});
test('ROS covariance block rotation swaps diagonal x y variances',()=>{const R=[[0,-1,0],[1,0,0],[0,0,1]];close(mm(mm(R,[[1,0,0],[0,4,0],[0,0,9]]),tr(R)),[[4,0,0],[0,1,0],[0,0,9]]);});
const time={now:1000000000n,stamp:900000000n,u:1000000n,limit:150000000n,maxU:5000000n};
test('timestamp valid case',()=>assert(accepted(time)));
test('timestamp future outside uncertainty rejected',()=>assert(!accepted({...time,stamp:1002000000n})));
test('timestamp future uncertainty boundary accepted',()=>assert(accepted({...time,stamp:1001000000n})));
test('timestamp stale after uncertainty rejected',()=>assert(!accepted({...time,stamp:850000000n})));
test('timestamp expired model and wrong epoch rejected',()=>{assert(!accepted({...time,valid:false}));assert(!accepted({...time,epoch:false}));});
test('dedup across stream and session never collides',()=>{const key=m=>[m.device_id,m.session_id,m.stream_id,m.sequence].join('|');assert.notEqual(key(samples[0]),key(samples[1]));assert.notEqual(key(samples[0]),key({...samples[0],session_id:'new'}));assert.equal(key(samples[0]),key(clone(samples[0])));});
test('canonical hash ignores key insertion order',()=>{const a=samples[1].body.delta,b=Object.fromEntries(Object.entries(a).reverse());assert.equal(sha(jcs(a)),sha(jcs(b)));});
test('semantic hash binds pose, operation and epochs',()=>{const a=samples[1].body.delta;for(const b of [{...a,map_epoch:'2'},{...a,operation:'delete',geometry:null},{...a,chunk_pose:{...a.chunk_pose,translation_m:[9,2,0.5]}}])assert.notEqual(sha(jcs(a)),sha(jcs(b)));});
test('payload fixture digest and mesh lengths',()=>{const b=fs.readFileSync(path.join(root,'03_contracte/fixture_mesh.bin')),g=samples[1].body.delta.geometry;assert.equal(sha(b),g.sha256);assert.equal(b.length,g.byte_length);assert.equal(b.length,12+12*b.readUInt32LE(0)+12*b.readUInt32LE(4));});
test('delta upsert duplicate delete stale reappearance',()=>{const state=new Map(),seen=new Map();function apply(m){semantic(m);const d=m.body.delta,k=d.map_epoch+'/'+d.chunk_id+'/'+d.new_revision;if(seen.has(k)){assert.equal(seen.get(k),m.body.semantic_hash);return 'duplicate';}const old=state.get(d.chunk_id);assert.equal(d.base_revision,old?.revision||'0');state.set(d.chunk_id,{revision:d.new_revision,deleted:d.operation==='delete'});seen.set(k,m.body.semantic_hash);return 'applied';}assert.equal(apply(samples[1]),'applied');assert.equal(apply(samples[1]),'duplicate');assert.equal(apply(samples[4]),'applied');assert(state.get('chunk-001').deleted);assert.equal(apply(samples[1]),'duplicate');assert(state.get('chunk-001').deleted);});
test('depth binary frame size check',()=>{const d={...clone(samples[0]),kind:'depth_frame',body:{observation_id:'depth-001',camera_frame_id:'iphone_depth_optical',width:256,height:192,intrinsics_row_major:[200,0,128,0,200,96,0,0,1],camera_pose:samples[0].body.observation.pose,payload:{sha256:'0'.repeat(64),byte_length:256*192*4,encoding:'depth_f32_le'}}};semantic(d);d.body.payload.byte_length--;assert.throws(()=>semantic(d));});
test('bootstrap hello before clock model is accepted only as control',()=>{semantic(samples[5]);const bad=clone(samples[0]);bad.clock_model_id=null;assert.throws(()=>semantic(bad));});
test('clock probe bootstrap carries source-domain sample separately',()=>{const m=clone(samples[5]);m.body.action='clock_probe';m.body.clock_samples_ns=['1000000000'];semantic(m);m.body.clock_samples_ns=[];assert.throws(()=>semantic(m));});
test('depth camera pose maps optical point into parent frame',()=>{const camera={R:[[0,0,1],[-1,0,0],[0,-1,0]],t:[1,2,0.5]};close(mv(camera.R,[0,0,1]).map((v,i)=>v+camera.t[i]),[2,2,0.5]);});
test('clock model is publishable before synchronized envelope',()=>{semantic(samples[6]);const x=clone(samples[6]);x.body.valid_until_robot_ns='4000000000';assert.throws(()=>semantic(x));});
test('anchored affine time maps large integer timestamps exactly',()=>{const convert=(phone,po,ro,ppb)=>{const dt=phone-po;assert(dt>=-60000000000n&&dt<=60000000000n);const num=dt*(1000000000n+ppb),half=num<0n?-500000000n:500000000n;return ro+(num+half)/1000000000n;};assert.equal(convert(9000000000000000001n,9000000000000000000n,8000000000000000000n,0n),8000000000000000001n);assert.equal(convert(1000000000n,0n,0n,1000n),1000001000n);assert.equal(convert(-1n,0n,0n,0n),-1n);});
test('mesh delta rejects RGB and depth even with recomputed hash',()=>{for(const encoding of ['rgb_hevc_annex_b','depth_f32_le']){const x=clone(samples[1]);x.body.delta.geometry.encoding=encoding;x.body.semantic_hash=sha(jcs(x.body.delta));assert.throws(()=>semantic(x));}});
test('all sample dedup keys are distinct',()=>{const keys=samples.map(m=>[m.device_id,m.session_id,m.stream_id,m.sequence].join('|'));assert.equal(new Set(keys).size,keys.length);});
test('v1 retained hypothesis expires using original observation timestamp',()=>{const x=clone(samples[0]);x.body.observation.state='predicted';semantic(x);assert(!accepted({...time,now:1200000000n,stamp:BigInt(x.capture_time_ns)}));});
const report={timestamp_utc:new Date().toISOString(),scope:'Offline executable specification: emitted schema subset and deterministic numeric/protocol tests; no hardware, ROS, iOS, TLS or generic JSON Schema certification',passed:cases.filter(x=>x.status==='pass').length,total:cases.length,cases};
fs.writeFileSync(path.join(root,'04_validare/robot_contract_results.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));process.exitCode=report.passed===report.total?0:1;
