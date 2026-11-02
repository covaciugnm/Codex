'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {planPaths,safe}=require('./materialize-apk-version-20261101.cjs');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const names=['raw/base.apk/res/2F.xml','raw/base.apk/res/2f.xml','raw/base.apk/Dir/a.txt','raw/base.apk/dir/b.txt','raw/base.apk/node','raw/base.apk/node/child.txt','raw/base.apk/CON.xml','raw/base.apk/con .xml','raw/base.apk/PRN','raw/base.apk/AUX.txt','raw/base.apk/NUL','raw/base.apk/COM1.xml','raw/base.apk/LPT9.xml','raw/base.apk/end.','raw/base.apk/end ','raw/base.apk/a:b.xml','raw/base.apk/a?b.xml','raw/base.apk/normal.txt','raw/base.apk/é.txt','raw/base.apk/é.txt'];
const initial=planPaths(names.map(logical=>({logical}))),forged=initial.find(x=>x.logical.endsWith('2F.xml')).physical;
names.push(forged);
const rows=names.map((logical,i)=>{const data=Buffer.from('fixture-'+i+'-'+logical);return{logical,data,sha256:hash(data),bytes:data.length};});
const planned=planPaths(rows),again=planPaths([...rows].reverse());assert.deepEqual(planned.map(x=>[x.logical,x.physical]),again.map(x=>[x.logical,x.physical]));
assert.equal(planned.find(x=>x.logical.endsWith('/normal.txt')).physical,'raw/base.apk/normal.txt');
assert.equal(new Set(planned.map(x=>x.physical.toUpperCase())).size,planned.length);
assert.throws(()=>planPaths([{logical:'raw/../outside'}]),/Unsafe/);assert.throws(()=>planPaths([{logical:'raw/a'},{logical:'raw/a'}]),/Duplicate/);
const destination=path.resolve(process.env.IFLYTEK_APK_PATH_TEST_DIR||'D:/Codex-iflytek-apk-analysis-20261101/path-fixture-'+Date.now());fs.mkdirSync(destination,{recursive:true});
for(const row of planned){const p=safe(destination,row.physical);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,row.data);}
for(const row of planned){const b=fs.readFileSync(safe(destination,row.physical));assert.equal(b.length,row.bytes);assert.equal(hash(b),row.sha256);}
const report={passed:true,files:planned.length,mapped:planned.filter(x=>x.logical!==x.physical).length,destination,checks:['case-distinct files','case-distinct directories','file-versus-directory prefix','reserved Windows names including extensions','trailing dot/space','invalid colon/question mark','Unicode canonical-equivalent names','forged encoded-name namespace','ordinary filename unchanged','deterministic independent of input order','all bytes verified after actual Windows writes','traversal and duplicate logical paths rejected'],paths:planned.map(({logical,physical,sha256,bytes})=>({logical,physical,sha256,bytes}))};
const target=path.resolve(__dirname,'../apk-analysis-2026-11-01/audit/path-mapping-test-results.json');fs.writeFileSync(target,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:true,files:report.files,mapped:report.mapped,destination}));
