'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib');
const {zipEntries}=require('./inspect-android-archive.cjs');
const dir='retailer-audit-2026-11-01',release='iflytek-retailer-software-2026-11-01';
const read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const write=(f,v)=>fs.writeFileSync(path.join(dir,f),JSON.stringify(v,null,2)+'\n');
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const assets=read('assets.json'),versions=read('xfyun-cli-versions.json');
const sources={
 'iflytek-translate-chrome.crx':'https://clients2.google.com/service/update2/crx?response=redirect&prodversion=156.0.8078.76&acceptformat=crx2,crx3&x=id%3Dcmjdeaeonbhajidgpmbappcleimpcmlg%26uc',
 'iflytek-translate-edge.crx':'https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&x=id%3Dlhnkmmijpiijmedbojlefopjgagogmjl%26installsource%3Dondemand%26uc',
 'iFly-Skills-b8f5d7d.zip':'https://codeload.github.com/iflytek/iFly-Skills/zip/b8f5d7d0bad672c7b12d161ab11cf1de53461e08'
};
for(const v of versions)sources['xfyun-cli-'+v.version+'.tgz']=v.dist.tarball;
for(const [name,remote] of [['windows','win-gw-x64.exe'],['mac-arm64','mac-arm64.dmg'],['mac-x64','mac-x64.dmg']])sources['iflytek-translate-'+name+(name==='windows'?'.exe':'.dmg')]='https://saas-public-cdn-ioss.iflytranslate.com/desktop/iflytek-translate-saas-1.0.9-'+remote;
for(const name of fs.readdirSync(path.join(dir,'software'))){
 const file='software/'+name,b=fs.readFileSync(path.join(dir,file)),url=sources[name];if(!url)throw Error('Missing source: '+name);
 let r=assets.find(x=>x.file===file||x.url===url);if(!r){r={url};assets.push(r);}
 Object.assign(r,{file,bytes:b.length,sha256:digest(b),status:'downloaded',storage:b.length>25000000?'release':'git'});
 if(name.endsWith('.dmg')&&b.subarray(-512,-508).toString()!=='koly')throw Error('Invalid DMG '+name);
 if(name.endsWith('.exe')&&b.subarray(0,2).toString()!=='MZ')throw Error('Invalid EXE');
 if(name.endsWith('.crx')){
  if(b.subarray(0,4).toString()!=='Cr24')throw Error('Invalid CRX');const v=b.readUInt32LE(4),off=v===3?12+b.readUInt32LE(8):16+b.readUInt32LE(8)+b.readUInt32LE(12);
  const m=JSON.parse(zipEntries(b.subarray(off)).find(x=>x.name==='manifest.json').read().toString());r.extensionManifest={name:m.name,version:m.version,manifest_version:m.manifest_version,description:m.description};
 }
 if(name.endsWith('.tgz')){const v=versions.find(x=>name==='xfyun-cli-'+x.version+'.tgz'),[algo,hash]=v.dist.integrity.split('-');if(crypto.createHash(algo).update(b).digest('base64')!==hash)throw Error('Integrity mismatch '+name);r.registryIntegrityVerified=true;r.version=v.version;r.scope='Generic cloud AI CLI; not a glasses driver or transaas CLI';}
 if(r.storage==='release'){r.release=release;r.asset=name;r.downloadUrl='https://github.com/covaciugnm/iFLYTEK/releases/download/'+release+'/'+name;r.version='1.0.9';}
}
write('assets.json',assets);
const audit=read('manifest.json'),excluded=[],seen=new Set();
audit.records=audit.records.filter(r=>{
 const u=new URL(r.url);u.hash='';const key=u.href;
 const irrelevant=/xiaomi-mijia|livetalk-ai|hearview.ai|vuzix.com|ajnalens.com|item.lenovo|quick_shop/.test(r.url)||(/xunfei.cn\/goods\?goodsId=/.test(r.url)&&!r.url.includes('goodsId=2448'));
 if(irrelevant||seen.has(key)){excluded.push({url:r.url,reason:irrelevant?'Unrelated cross-sell or different product; excluded from findings':'Duplicate page fragment'});return false;}seen.add(key);return true;
});write('manifest.json',audit);write('excluded-leads.json',excluded);
const prior=new Map(JSON.parse(fs.readFileSync('iflytek-manifest-sha256.json','utf8')).files.map(r=>[r.sha256,{path:r.path,storage:r.storage,asset:r.asset}]));
for(const r of JSON.parse(fs.readFileSync('collection-2026-11-01/manifest.json','utf8')).records)if(r.sha256)prior.set(r.sha256,r.existing||{path:'collection-2026-11-01/'+r.file,storage:r.storage});
const qr=read('qr-image-audit.json');
for(const r of [...assets,...qr.images])if(r.sha256&&prior.has(r.sha256)){r.existing=prior.get(r.sha256);r.status='already-in-github';delete r.file;}
write('assets.json',assets);write('qr-image-audit.json',qr);
const inventory=[];
for(const r of [...audit.records,...assets,...qr.images])if(r.file&&r.status==='downloaded'){
 const p=path.join(dir,r.file);if(!fs.existsSync(p))throw Error('Missing '+p);const b=fs.readFileSync(p);if(r.sha256&&digest(b)!==r.sha256)throw Error('Hash mismatch '+p);if(!inventory.some(x=>x.file===r.file))inventory.push({file:r.file,bytes:b.length,sha256:digest(b),source:r.url,storage:r.storage||'git',...(r.downloadUrl?{downloadUrl:r.downloadUrl}:{})});
}
write('file-inventory.json',inventory);
const tracked=new Set(inventory.filter(r=>r.storage==='git').map(r=>r.file));
let ignored='software/*.exe\nsoftware/*.dmg\nloomy-references/\nloomy-asar-reference-index.json\n';
for(const sub of ['pages','images','resources','software'])for(const name of fs.readdirSync(path.join(dir,sub)))if(!tracked.has(sub+'/'+name))ignored+=sub+'/'+name+'\n';
fs.writeFileSync(path.join(dir,'.gitignore'),ignored);
console.log(JSON.stringify({pages:audit.records.length,hosts:new Set(audit.records.map(r=>new URL(r.url).host)).size,software:assets.filter(r=>r.file?.startsWith('software/')).map(r=>({file:r.file,version:r.extensionManifest?.version||r.version,bytes:r.bytes})),files:inventory.length},null,2));
