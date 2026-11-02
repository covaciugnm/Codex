'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const repo=path.resolve(__dirname,'../..'),old='D:/Codex-iflytek-apk-analysis-20261101',file='D:/Codex-iflytek-decompilation-repair-20261101/full-diagnostics/DIAGNOSTICS.json';
const read=p=>JSON.parse(fs.readFileSync(p)),sha=b=>crypto.createHash('sha256').update(b).digest('hex'),summary=read(file),results=[];
for(const group of summary.groups){
 const d=read(group.index),report=read(path.join(repo,'apk-analysis-2026-11-01',d.baselineReport)),v=d.variants[0],base=path.join(old,'versions',v.package,v.version,v.variant),map=new Map(read(path.join(base,'PATH-MAP.json')).paths.filter(x=>x.kind==='decompiled').map(x=>[x.path,x.physical])),failed=new Map(d.failures.map(x=>[x.path,x]));
 const counts={scannedJavaFiles:0,filesWithMarkers:0,jadxError:0,jadxWarning:0,generatedUnsupportedStub:0,methodNotDecompiledText:0,inconsistentCode:0,dumpSkipped:0};
 for(const r of report.entries.filter(x=>x.path.endsWith('.java'))){
  const physical=map.get(r.path);if(!physical)throw Error('Missing materialized source');const b=fs.readFileSync(path.join(base,physical));if(b.length!==r.bytes||sha(b)!==r.sha256)throw Error('Source SHA/size mismatch');const s=b.toString(),n=t=>s.split(t).length-1;
  const m={jadxError:n('JADX ERROR:'),jadxWarning:n('JADX WARNING:')+n('JADX WARN:'),generatedUnsupportedStub:n('throw new UnsupportedOperationException("Method not decompiled:')+n('throw new java.lang.UnsupportedOperationException("Method not decompiled:'),methodNotDecompiledText:n('Method not decompiled:'),inconsistentCode:n('Code decompiled incorrectly'),dumpSkipped:n('Method dump skipped')};
  counts.scannedJavaFiles++;if(Object.values(m).some(Boolean)){counts.filesWithMarkers++;const f=failed.get(r.path);if(!f||f.sha256!==r.sha256||f.bytes!==r.bytes)throw Error('Diagnostic file provenance');for(const [k,a]of Object.entries(m))if(a!==f.counts[k])throw Error('File count mismatch');}else if(failed.has(r.path))throw Error('Spurious failure');for(const[k,a]of Object.entries(m))counts[k]+=a;
 }
 for(const[k,a]of Object.entries(counts))if(a!==d.javaMetrics[k]||a!==group.javaMetrics[k])throw Error('Aggregate mismatch');
 results.push({dexSetSha256:group.dexSetSha256,counts,indexSha256:sha(fs.readFileSync(group.index))});console.log('PASS',group.dexSetSha256,counts.scannedJavaFiles);
}
const totals={};for(const r of results)for(const[k,v]of Object.entries(r.counts))totals[k]=(totals[k]||0)+v;
const out={status:'PASS',score:10,scope:'Independent reread/hash and marker recount of all historical Java diagnostics; not semantic recovery or HeyCyan coverage',groups:results,totals,diagnosticsSha256:sha(fs.readFileSync(file)),commitApproved:false};fs.writeFileSync(path.join(__dirname,'GLOBAL-G0-RESULTS.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(totals));
