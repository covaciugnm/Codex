'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('./inspect-android-archive.cjs');
const root=path.resolve(__dirname,'..','apk-analysis-2026-11-01'),release='iflytek-apk-romania40-2026-10-31';
const inputs=[
 {asset:'iflytek-1.0.3899-editable-source.zip',sha256:'e53fe743b74c2825323c9a2b62b2b01bcf1c19fb1c0a05a7af2ab6494eaa0eea',bytes:191752231},
 {asset:'iflytek-1.0.3899-aot-analysis.zip',sha256:'674b063c0a7b792c08d846868de5c800be1c06eda10d9a991f4ed116f49fc5fa',bytes:58760652}
];
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const index=Object.create(null),audit={date:new Date().toISOString(),release,inputs:[],duplicateContentEntries:0,uniqueContentBytes:0};
for(const input of inputs){
 const file=path.join(root,'.work','baseline-release',input.asset),buf=fs.readFileSync(file),archiveSha256=hash(buf);
 if(buf.length!==input.bytes||archiveSha256!==input.sha256)throw Error('Release archive integrity mismatch '+input.asset);
 const entries=zipEntries(buf),result={asset:input.asset,archiveSha256,bytes:buf.length,zipEntries:entries.length,files:0,uncompressedBytes:0};
 const names=new Set();
 for(const entry of entries){
  if(entry.name.endsWith('/'))continue;if(names.has(entry.name))throw Error('Duplicate ZIP entry '+entry.name);names.add(entry.name);
  const data=entry.read(),sha256=hash(data);if(data.length!==entry.uncompressed)throw Error('Entry size mismatch '+entry.name);
  result.files++;result.uncompressedBytes+=data.length;
  if(index[sha256]){if(index[sha256].bytes!==data.length)throw Error('Hash size conflict');audit.duplicateContentEntries++;}
  else {index[sha256]={storage:'release-zip-entry',release,asset:input.asset,archiveSha256,entry:entry.name,bytes:data.length};audit.uniqueContentBytes+=data.length;}
  if(result.files%5000===0)console.log(input.asset,result.files);
 }
 audit.inputs.push(result);console.log(JSON.stringify(result));
}
audit.uniqueObjects=Object.keys(index).length;
fs.writeFileSync(path.join(root,'baseline-release-index.json'),JSON.stringify(index,null,2)+'\n');
fs.writeFileSync(path.join(root,'baseline-release-index-audit.json'),JSON.stringify(audit,null,2)+'\n');
console.log(JSON.stringify(audit));
