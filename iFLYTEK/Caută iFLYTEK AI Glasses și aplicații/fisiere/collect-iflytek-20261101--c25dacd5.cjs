'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..'),out=path.join(root,'collection-2026-11-01');
fs.mkdirSync(out,{recursive:true});
const manifestPath=path.join(out,'manifest.json');
const records=fs.existsSync(manifestPath)?JSON.parse(fs.readFileSync(manifestPath,'utf8')).records:[];
const previous=JSON.parse(fs.readFileSync(path.join(root,'iflytek-manifest-sha256.json'),'utf8'));
const hashes=new Map(previous.files.map(f=>[f.sha256,{path:f.path,asset:f.asset,storage:f.storage}]));
for(const r of records)if(r.sha256&&r.file)hashes.set(r.sha256,{path:'collection-2026-11-01/'+r.file});
function save(){fs.writeFileSync(manifestPath,JSON.stringify({date:'2026-11-01',repository:'covaciugnm/iFLYTEK',scope:'iFLYTEK Translate, Bavvo, Loomy, glasses documentation and related developer references. All publicly discovered versions; unavailable files are explicitly recorded.',records},null,2)+'\n');}
async function get(url,name,kind='documentation',extra={}){
 const old=records.find(r=>r.url===url&&['downloaded','already-in-github'].includes(r.status));if(old)return old;
 const r={url,kind,...extra,checkedAt:new Date().toISOString()};
 try{
  const res=await fetch(url,{signal:AbortSignal.timeout(['application','installer'].includes(kind)?180000:30000),headers:{'User-Agent':'Mozilla/5.0'}});
  r.httpStatus=res.status;r.finalUrl=res.url;r.contentType=res.headers.get('content-type');
  if(!res.ok)throw Error('HTTP '+res.status);
  if(/\.js$/.test(new URL(url).pathname)&&r.contentType?.includes('text/html'))throw Error('Server returned HTML for a JavaScript URL');
  const data=Buffer.from(await res.arrayBuffer());
  if(kind==='application'&&(data[0]!==0x50||data[1]!==0x4b))throw Error('Not an APK/XAPK/ZIP; rejected '+data.subarray(0,40).toString());
  if(kind==='installer'&&!(data.subarray(0,2).equals(Buffer.from('MZ'))||data.subarray(0,2).equals(Buffer.from('PK'))||data.subarray(-512,-508).toString()==='koly'))throw Error('Invalid installer magic');
  if(kind!=='application'&&/EO_Bot_Ssid|Just a moment|cf-chl-/.test(data.toString().slice(0,10000)))throw Error('Anti-bot challenge; not archived as documentation');
  r.bytes=data.length;r.sha256=crypto.createHash('sha256').update(data).digest('hex');
  if(extra.expectedSha256&&r.sha256!==extra.expectedSha256)throw Error('SHA-256 differs from source metadata');
  const dup=hashes.get(r.sha256);
  if(dup){r.status='already-in-github';r.existing=dup;}
  else{const file=path.join(out,name);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,data);r.file=name;r.status='downloaded';hashes.set(r.sha256,{path:'collection-2026-11-01/'+name});}
 }catch(e){r.status='unavailable';r.error=e.message;}
 const idx=records.findIndex(x=>x.url===url);if(idx>=0)records[idx]=r;else records.push(r);save();
 console.log(r.status,kind,name,r.bytes||'',r.error||'');return r;
}
async function pool(jobs,n=3){let i=0;await Promise.all(Array.from({length:n},async()=>{while(i<jobs.length)await jobs[i++]();}));}
async function main(){
 const sources=[
 ['https://m.iflytranslate.com/','official-translate.html'],
 ['https://transsaas-h5-ap1.iflyoversea.com/download?lang=EN','bavvo-download.html'],
 ['https://transsaas-h5-ap1.iflyoversea.com/guide?lang=EN','bavvo-guide.html'],
 ['https://transsaas-h5-ap1.iflyoversea.com/help?lang=EN','bavvo-help.html'],
 ['https://www.iflytek.com/en/products/translator/bavvo.html','bavvo-product.html'],
 ['https://saas-public.ioss.xfinfr.com/private/config/privacy-policy.html','translate-privacy.html'],
 ['https://saas-public-cdn-ap1.iflyoversea.com/private/config/en/privacy-policy.html','bavvo-privacy.html'],
 ['https://www.iflytek.com/en/news-events/news/311.html','glasses-mwc.html'],
 ['https://www.iflytek.com/en/news-events/news/343.html','glasses-ifa.html'],
 ['https://app.meizu.com/apps/public/detail?package_name=com.iflytek.translateapp','meizu.html'],
 ['https://app.mi.com/details?id=com.iflytek.translateapp','xiaomi.html'],
 ['https://www.xlhs.com/app/106712.html','xlhs.html'],
 ['https://www.itmop.com/downinfo/638208.html','itmop.html'],
 ['https://www.hackhome.com/soft/1316691.html','hackhome.html'],
 ['https://www.lcks.com.cn/soft/3125.html','lcks.html'],
 ['https://www.6ll.com/soft/45104.html','6ll.html'],
 ['https://www.chushou.tv/room/702.html','chushou.html'],
 ['https://www.51wan.com/azsoft/xffy2020bb/','51wan.html'],
 ['https://www.trans.org.cn/soft/13582.html','trans-org.html'],
 ['https://apps.apple.com/cn/app/id6739250870','ios-translate-cn.html'],
 ['https://apps.apple.com/us/app/bavvo-ai-translator/id6757071464','ios-bavvo-us.html'],
 ['https://play.google.com/store/apps/details?id=com.iflytek.bavvo','android-bavvo-play.html'],
 ['https://apkpure.net/fr/bavvo-ai-translator/com.iflytek.bavvo/versions','bavvo-versions.html'],
 ['https://lo omy.xunfei.cn/'.replace('lo omy','loomy'),'loomy.html']
 ];
 await pool(sources.map(([u,n])=>()=>get(u,'sources/'+n)));
 // Preserve the public JavaScript that implements official downloads and help pages.
 const queue=[];const seen=new Set();
 for(const r of records.filter(r=>r.file&&r.kind==='documentation'&&/iflytranslate|iflyoversea/.test(r.url))){
  const txt=fs.readFileSync(path.join(out,r.file),'utf8');
  for(const m of txt.matchAll(/(?:src|href)=["']([^"']+\.(?:js|css))["']/g)){const u=new URL(m[1],r.url).href;if(!seen.has(u)){seen.add(u);queue.push(u);}}
 }
 for(let depth=0;depth<3&&queue.length;depth++){
  const batch=queue.splice(0);await pool(batch.map(u=>async()=>{
   const r=await get(u,'web-assets/'+new URL(u).hostname+'-'+path.basename(new URL(u).pathname));
   if(!r.file||!u.endsWith('.js'))return;
   const txt=fs.readFileSync(path.join(out,r.file),'utf8');
   for(const m of txt.matchAll(/["']((?:\.\/|assets\/)[A-Za-z0-9_./-]+\.js)["']/g)){const link=new URL(m[1],m[1].startsWith('assets/')?new URL(u).origin:u).href;if(!seen.has(link)){seen.add(link);queue.push(link);}}
  }));
 }
 const binaries=[
 ['https://m.iflytranslate.com/download/android/FY10010010','translate-official-current.apk',{package:'com.iflytek.translateapp',region:'China distribution; EU not verified'}],
 ['https://z85.198274.com/9/com.iflytek.translateapp.apk','translate-xlhs-current.apk',{package:'com.iflytek.translateapp',claimedVersion:'1.0.3949',sourcePage:'https://www.xlhs.com/app/106712.html',region:'China mirror; EU not verified'}],
 ['https://loomy.xunfei.cn/api/download?platform=android','loomy-current.apk',{region:'China; companion workflow, not a glasses SDK'}],
 ...[1222,1211,1205,1197,1179,1112].map(v=>['https://d.apkpure.net/b/XAPK/com.iflytek.bavvo?versionCode='+v,'bavvo-1.0.'+v+'.xapk',{package:'com.iflytek.bavvo',claimedVersion:'1.0.'+v,region:'International; EU-specific build and glasses compatibility unverified'}])
 ];
 await pool(binaries.map(([u,n,e])=>()=>get(u,'applications/'+n,'application',e)),2);
 save();console.log(JSON.stringify(records.reduce((a,r)=>(a[r.status]=(a[r.status]||0)+1,a),{})));
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1});
module.exports={get,pool,out,records,save};
