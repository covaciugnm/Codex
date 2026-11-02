'use strict';
const fs=require('node:fs'),path=require('node:path');
const {get,pool,records,out,save}=require('./collect-iflytek-20261101.cjs');
(async()=>{
 // HTML fallbacks returned for invalid JS URLs are not JavaScript documentation.
 for(const r of records)if(/\.js$/.test(r.url)&&r.contentType?.includes('text/html')){r.status='unavailable';r.error='Server returned HTML fallback for JavaScript URL';delete r.existing;}
 await pool([
 ()=>get('https://m.iflytranslate.com/assets/index-DtJPbGnW.js','web-assets/iflytranslate-index-DtJPbGnW.js'),
 ()=>get('https://loomy.xunfei.cn/download','sources/loomy-download.html'),
 ()=>get('https://loomy.xunfei.cn/changelog','sources/loomy-changelog.html'),
 ()=>get('https://loomy.xunfei.cn/docs/user-guide/toolbox','sources/loomy-toolbox.html'),
 ()=>get('https://www.xlhs.com/app/106712.html','sources/xlhs.html'),
 ()=>get('https://www.hackhome.com/soft/1316691.html','sources/hackhome.html'),
 ()=>get('https://www.6ll.com/soft/45104.html','sources/6ll.html'),
 ()=>get('https://api.itmop.com/down/638208b5','applications/translate-itmop.apk','application',{claimedVersion:'1.0.3899',sourcePage:'https://www.itmop.com/downinfo/638208.html'}),
 ()=>get('https://www.lcks.com.cn/down/3125/2/1/','applications/translate-lcks.apk','application',{claimedVersion:'1.0.2977'}),
 ()=>get('https://www.chushou.tv/down/337/2/1/','applications/translate-chushou.apk','application',{claimedVersion:'1.0.3835'}),
 ()=>get('https://www.trans.org.cn/api/counter/down?id=13582','applications/translate-trans-org.apk','application',{claimedVersion:'1.0.2181'})
 ]);
 const channelResults=[];
 const baseline=records.find(r=>r.url==='https://m.iflytranslate.com/download/android/FY10010010');
 // These channel identifiers are published in the download page JavaScript.
 await pool(['FY10030001','FY10030002','FY10030003','FY10030004','FY10030005','FY10030006','FY10030007','FY10030008','FY10030009'].map(c=>async()=>{
  const url='https://m.iflytranslate.com/download/android/'+c;
  try{const r=await fetch(url,{method:'HEAD',signal:AbortSignal.timeout(20000)});const md5=r.headers.get('content-md5');channelResults.push({url,status:r.status,bytes:r.headers.get('content-length'),contentMD5:md5,sameAsExistingOfficialAPK:md5==='yBgSm2kyvuRrjmtX/If0+Q==',note:'Channel is marketing distribution, not an EU region indicator'});if(r.ok&&md5&&md5!=='yBgSm2kyvuRrjmtX/If0+Q==')await get(url,'applications/translate-channel-'+c+'.apk','application',{region:'Official marketing channel; EU not verified'});}catch(e){channelResults.push({url,error:e.message});}
 }),3);
 fs.writeFileSync(path.join(out,'official-channels.json'),JSON.stringify(channelResults,null,2)+'\n');
 // Retain the dated catalog history pages for every publicly listed Bavvo version.
 await pool([1222,1211,1205,1197,1179,1112].map(v=>()=>get('https://apkpure.net/fr/bavvo-ai-translator/com.iflytek.bavvo/download/'+(v===1222?'':'1.0.'+v),'sources/bavvo-1.0.'+v+'.html')));
 // Download public Loomy JavaScript to discover the published desktop links.
 let loomyText='';const lr=records.find(r=>r.url==='https://loomy.xunfei.cn/download');
 if(lr?.file)loomyText=fs.readFileSync(path.join(out,lr.file),'utf8');
 const chunks=[...new Set([...loomyText.matchAll(/src="([^" ]+\.js[^" ]*)"/g)].map(m=>new URL(m[1].replaceAll('&amp;','&'),'https://loomy.xunfei.cn').href))];
 await pool(chunks.map(u=>()=>get(u,'web-assets/loomy-'+path.basename(new URL(u).pathname))));
 save();
})().catch(e=>{console.error(e);process.exitCode=1});
