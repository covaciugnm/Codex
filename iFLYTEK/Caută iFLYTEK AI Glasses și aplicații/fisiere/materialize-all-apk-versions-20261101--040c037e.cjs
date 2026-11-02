'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const repo=path.resolve(__dirname,'..'),root=path.join(repo,'apk-analysis-2026-11-01');
const option=(name,fallback)=>{const i=process.argv.indexOf(name);return i<0?fallback:process.argv[i+1];};
const store=path.resolve(option('--store-dir',root)),output=path.resolve(option('--output',path.join(store,'materialized'))),cache=path.resolve(option('--cache-dir',path.join(store,'existing-cache')));
async function main(){
 const c=JSON.parse(fs.readFileSync(path.join(root,'catalog.json'),'utf8')),runs=[];let cursor=0;
 if(!fs.existsSync(path.join(root,'cas-index.json')))throw Error('Finalize the analysis before materializing all versions.');
 for(const v of c.versions){const m=JSON.parse(fs.readFileSync(path.join(root,v.manifest),'utf8'));if(m.decompilation?.status!=='complete-with-documented-limitations')throw Error('Pending decompilation '+v.variant);for(const x of m.components.filter(x=>x.dex?.length))if(!m.decompilation.components.some(d=>d.component===x.name))throw Error('Missing DEX report '+v.variant+' '+x.name);}
 async function worker(){while(cursor<c.versions.length){const v=c.versions[cursor++],dest=path.join(output,v.package,v.version,v.variant),args=[path.join(__dirname,'materialize-apk-version-20261101.cjs'),'--manifest',v.manifest,'--output',dest,'--store-dir',store,'--cache-dir',cache,'--preload-git'];if(process.argv.includes('--local-only'))args.push('--local-only');
  console.log('Materializing',v.package,v.version,v.variant);
  const r=await new Promise((resolve,reject)=>{const child=cp.spawn(process.execPath,args,{cwd:repo,windowsHide:true,stdio:['ignore','pipe','pipe']});let stdout='',stderr='';child.stdout.on('data',b=>stdout+=b);child.stderr.on('data',b=>stderr+=b);child.on('error',reject);child.on('close',exitCode=>resolve({exitCode,stdout,stderr}));});
  if(r.exitCode!==0){runs.push({manifest:v.manifest,status:'failed',...r});throw Error('Materialization failed '+v.variant+' '+r.stderr);}
  const start=r.stdout.indexOf('{');if(start<0)throw Error('Missing materialization result '+v.variant);const result=JSON.parse(r.stdout.slice(start));runs.push({manifest:v.manifest,status:'verified',...result});console.log('Verified',v.variant,result.raw,result.decompiled);
 }}
 const outcomes=await Promise.allSettled([worker(),worker()]);fs.writeFileSync(path.join(root,'materialization-runs.json'),JSON.stringify({date:new Date().toISOString(),outputRoot:output,storeRoot:store,versions:runs},null,2)+'\n');for(const o of outcomes)if(o.status==='rejected')throw o.reason;
 if(runs.length!==c.versions.length||runs.some(r=>r.status!=='verified'))throw Error('Incomplete materialization');
 const escape=s=>String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 const rows=c.versions.map(v=>{const r=runs.find(r=>r.manifest===v.manifest),prefix=[v.package,v.version,v.variant].map(encodeURIComponent).join('/');return '<tr><td>'+escape(v.package)+'</td><td>'+escape(v.version)+'</td><td>'+escape(v.variant)+'</td><td><a href="'+prefix+'/raw/">Fișiere extrase</a></td><td><a href="'+prefix+'/decompiled/">Cod decompilat</a></td><td><a href="'+prefix+'/SOURCE-MANIFEST.json">Manifest</a></td><td>'+r.raw+' / '+r.decompiled+'</td></tr>';}).join('\n');
 fs.writeFileSync(path.join(output,'INDEX.html'),'<!doctype html><html lang="ro"><meta charset="utf-8"><title>APK/XAPK — versiuni separate</title><style>body{font:16px system-ui;margin:2em}td,th{padding:.6em;text-align:left;border-bottom:1px solid #ccc}table{border-collapse:collapse}</style><h1>APK/XAPK — versiuni separate</h1><p>Extracție statică și cod decompilat, cu limitele JADX păstrate în jurnale. Aceste fișiere nu reprezintă proiectele sursă originale. Variantele full-rebuilt și romania40 sunt reconstrucții locale.</p><table><thead><tr><th>Aplicație</th><th>Versiune</th><th>Variantă</th><th>Raw</th><th>Cod</th><th>Proveniență</th><th>Fișiere raw / cod+log</th></tr></thead><tbody>'+rows+'</tbody></table></html>\n');
 console.log('All',runs.length,'version directories materialized.');
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
