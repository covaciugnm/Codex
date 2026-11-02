'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {zipEntries}=require('./inspect-android-archive.cjs');
const repo=path.resolve(__dirname,'..'),out=path.join(repo,'loomy-translate-skill-2026-11-01');fs.mkdirSync(out,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const known=new Map();
function remember(file,select){if(!fs.existsSync(path.join(repo,file)))return;const data=JSON.parse(fs.readFileSync(path.join(repo,file),'utf8'));for(const r of select(data))if(r.sha256&&!known.has(r.sha256)){const pointer=r.existing||{path:r.path||(r.file?path.posix.dirname(file)+'/'+r.file:undefined),storage:r.storage||(file.includes('cas-index')?'cas':undefined),gitBlobSha1:r.gitBlobSha1,asset:r.asset||r.assetName,entry:r.entry,archiveSha256:r.archiveSha256,release:r.release||r.releaseTag||data.releaseTag,downloadUrl:r.downloadUrl};known.set(r.sha256,{inventory:file,...pointer,...(file.includes('cas-index')?{objectSha256:r.sha256}: {})});}}
remember('iflytek-manifest-sha256.json',x=>x.files);remember('collection-2026-11-01/manifest.json',x=>x.records);remember('retailer-audit-2026-11-01/file-inventory.json',x=>x);remember('apk-analysis-2026-11-01/cas-index.json',x=>x.objects);
remember('apk-analysis-2026-11-01/baseline-release-index.json',x=>Object.entries(x).map(([sha256,r])=>({sha256,...r})));
const mp=path.join(out,'manifest.json'),records=fs.existsSync(mp)?JSON.parse(fs.readFileSync(mp,'utf8')).records:[];
for(const r of records)if(r.sha256&&r.file&&r.status==='downloaded'&&!known.has(r.sha256))known.set(r.sha256,{path:'loomy-translate-skill-2026-11-01/'+r.file,storage:r.storage,asset:r.asset,release:r.release,downloadUrl:r.downloadUrl});
for(const r of records)if(r.status==='already-in-github'&&known.has(r.sha256))r.existing=known.get(r.sha256);
function save(){fs.writeFileSync(mp,JSON.stringify({date:'2026-11-01',scope:'Public Loomy translation skill, its CLI and separately labelled other-hardware software. No account access, installation or collected code execution.',records},null,2)+'\n');}
function store(data,file,source,category){const h=sha(data),old=known.get(h),r={url:source,category,bytes:data.length,sha256:h};if(old){r.status=old.path?.startsWith('loomy-translate-skill-2026-11-01/')?'reused-in-collection':'already-in-github';r.existing=old;}else{r.status='downloaded';r.file=file;fs.mkdirSync(path.dirname(path.join(out,file)),{recursive:true});fs.writeFileSync(path.join(out,file),data);known.set(h,{path:'loomy-translate-skill-2026-11-01/'+file});}return r;}
async function resource(url,file,category){const prev=records.find(r=>r.url===url&&r.status!=='unavailable');if(prev)return prev;let r={url,category,checkedAt:new Date().toISOString()};try{const res=await fetch(url,{signal:AbortSignal.timeout(180000),headers:{'User-Agent':'Mozilla/5.0'}});r.statusCode=res.status;r.finalUrl=res.url;r.contentType=res.headers.get('content-type');if(!res.ok)throw Error('HTTP '+res.status);const b=Buffer.from(await res.arrayBuffer());if(/\.(?:zip|apk|xapk|tgz)$/.test(file)&&b.subarray(0,2).toString()!=='PK'&&!(b[0]===31&&b[1]===139))throw Error('Not a software archive');Object.assign(r,store(b,file,url,category));}catch(e){r.status='unavailable';r.error=e.message;}const i=records.findIndex(x=>x.url===url);if(i>=0)records[i]=r;else records.push(r);save();console.log(r.status,file,r.bytes||'',r.error||'');return r;}
function packagedPublicBase(){
 const input=path.join(repo,'collection-2026-11-01/applications/Loomy-0.9.39-win.zip'),es=zipEntries(fs.readFileSync(input));
 const source=es.find(e=>e.name==='resources/app.asar.unpacked/electron/utils/env-file-crypto.js').read().toString('utf8');
 const literal=name=>{const re=new RegExp(name+"\\s*=\\s*(['\"])(.*?)\\1");const m=re.exec(source);if(!m)throw Error('Unsupported client config format');return m[2];};
 const magic=literal('ENV_CRYPT_MAGIC'),phrase=literal('ENV_CRYPT_PASSPHRASE'),encrypted=es.find(e=>e.name==='resources/.env.prod').read();
 const raw=encrypted.toString('utf8').trim();if(!raw.startsWith(magic+':'))throw Error('Unexpected env header');
 const payload=Buffer.from(raw.slice(magic.length+1).trim(),'base64'),salt=payload.subarray(0,16),iv=payload.subarray(16,28),tag=payload.subarray(28,44),ciphertext=payload.subarray(44);
 const decipher=crypto.createDecipheriv('aes-256-gcm',crypto.scryptSync(phrase,salt,32),iv);decipher.setAuthTag(tag);const plain=Buffer.concat([decipher.update(ciphertext),decipher.final()]).toString('utf8');
 // Inspect only the public catalog base address. Never persist/use authentication values.
 const m=/^(?:VITE_)?LOOMY_POINTS_BASE_URL\s*=\s*(.+)$/m.exec(plain);if(!m)throw Error('Public base missing');const url=new URL(m[1].trim().replace(/^['"]|['"]$/g,''));
 const base=url.origin+url.pathname;fs.writeFileSync(path.join(out,'configuration-provenance.json'),JSON.stringify({sourceArchive:'collection-2026-11-01/applications/Loomy-0.9.39-win.zip',sourceEntry:'resources/.env.prod',sourceEntrySha256:sha(encrypted),publicCatalogBase:base,note:'Only a public base URL was retained from shipped configuration; no authentication values were stored or used, and no distributed code was executed.'},null,2)+'\n');return base;
}
module.exports={resource,store,save,records,out,packagedPublicBase,known};
if(require.main===module)(async()=>{const base=packagedPublicBase().replace(/\/+$/,'');console.log('Public catalog base',base);await resource(base+'/api/v1/skills/store/list','sources/loomy-skill-catalog.json','official-public-catalog');})().catch(e=>{console.error(e.message);process.exitCode=1});
