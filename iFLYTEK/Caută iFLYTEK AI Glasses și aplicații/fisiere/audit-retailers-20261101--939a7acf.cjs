'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {createRequire}=require('node:module');
const req=createRequire(process.env.IFLYTEK_AUDIT_DEPENDENCIES||path.join(__dirname,'retailer-deps/package.json'));
const cheerio=req('cheerio');
const root=path.resolve(__dirname,'..'),out=path.join(root,'retailer-audit-2026-11-01');fs.mkdirSync(out,{recursive:true});
const previous=JSON.parse(fs.readFileSync(path.join(root,'iflytek-manifest-sha256.json'),'utf8'));
const recent=JSON.parse(fs.readFileSync(path.join(root,'collection-2026-11-01/manifest.json'),'utf8'));
const hashes=new Map(previous.files.map(f=>[f.sha256,{path:f.path,storage:f.storage,asset:f.asset}]));
for(const r of recent.records)if(r.sha256)hashes.set(r.sha256,r.existing||{path:'collection-2026-11-01/'+r.file,storage:r.storage,asset:r.assetName});
const manifestFile=path.join(out,'manifest.json');const records=fs.existsSync(manifestFile)?JSON.parse(fs.readFileSync(manifestFile,'utf8')).records:[];
for(const r of records)if(r.file&&r.sha256)hashes.set(r.sha256,{path:'retailer-audit-2026-11-01/'+r.file});
const hints=/download|\bapp\b|apk|sdk|manual|firmware|support|\bhelp\b|qr.?code|bavvo|loomy|glassclaw|hey.?cyan|lumi|下载|软件|应用|说明书|帮助|扫码|二维码|固件|tải|phần mềm|ứng dụng|hướng dẫn|تحميل|скачать|приложен/ig;
function save(){fs.writeFileSync(manifestFile,JSON.stringify({date:'2026-11-01',repository:'covaciugnm/iFLYTEK',scope:'Retailer product descriptions, download/help pages and software leads. Exact-model evidence is separated from unrelated generic glasses.',records},null,2)+'\n');}
function clean(t){return t.replace(/\s+/g,' ').trim();}
async function page(url,scope='exact-model',parent=null){
 const already=records.find(r=>r.url===url&&r.status!=='unavailable');if(already)return already;
 const r={url,scope,parent,checkedAt:new Date().toISOString()};
 try{const res=await fetch(url,{signal:AbortSignal.timeout(30000),headers:{'User-Agent':'Mozilla/5.0'}});r.statusCode=res.status;r.finalUrl=res.url;r.contentType=res.headers.get('content-type');if(!res.ok)throw Error('HTTP '+res.status);const b=Buffer.from(await res.arrayBuffer());if(!r.contentType?.includes('html'))throw Error('Expected HTML');
  const html=b.toString('utf8');if(/Just a moment|EO_Bot_Ssid|cf-chl-/.test(html.slice(0,10000)))throw Error('Anti-bot challenge');const $=cheerio.load(html);r.title=clean($('title').text());
  r.links=[];$('a[href]').each((_,el)=>{const a=$(el);try{const u=new URL(a.attr('href'),res.url);if(!/^https?:$/.test(u.protocol))return;r.links.push({url:u.href,text:clean(a.text()).slice(0,250)});}catch{}});
  r.links=[...new Map(r.links.map(l=>[l.url,l])).values()];
  r.images=[];$('img').each((_,el)=>{const i=$(el);let src=i.attr('data-src')||i.attr('data-lazy-src')||i.attr('src');if(src&&!src.startsWith('data:'))try{r.images.push({url:new URL(src,res.url).href,alt:i.attr('alt')||''});}catch{}});
  r.images=[...new Map(r.images.map(i=>[i.url,i])).values()];
  $('script,style,noscript,svg').remove();const txt=clean($('body').text());r.excerpts=[];for(const m of txt.matchAll(hints)){r.excerpts.push(txt.slice(Math.max(0,m.index-160),m.index+260));if(r.excerpts.length>=70)break;}
  r.interestingLinks=r.links.filter(l=>new RegExp(hints.source,'i').test(l.url+' '+l.text));
  r.sha256=crypto.createHash('sha256').update(b).digest('hex');r.bytes=b.length;const dup=hashes.get(r.sha256);
  if(dup){r.status='already-in-github';r.existing=dup;}else{r.status='downloaded';r.file='pages/'+new URL(url).hostname+'-'+crypto.createHash('sha256').update(url).digest('hex').slice(0,12)+'.html';fs.mkdirSync(path.join(out,'pages'),{recursive:true});fs.writeFileSync(path.join(out,r.file),b);hashes.set(r.sha256,{path:'retailer-audit-2026-11-01/'+r.file});}
 }catch(e){r.status='unavailable';r.error=e.message;}
 const n=records.findIndex(x=>x.url===url);if(n>=0)records[n]=r;else records.push(r);save();console.log(r.status,new URL(url).hostname,r.title?.slice(0,65)||r.error);return r;
}
async function pool(jobs,n=4){let i=0;await Promise.all(Array.from({length:n},async()=>{while(i<jobs.length)await jobs[i++]();}));}
const seeds=[
 ['https://a1smartshop.com/product/iflytek-ai-glasses/','exact-model'],
 ['https://uzummarket.joom.com/en/products/6a30e2450c735c016f6b2759','exact-model'],
 ['https://sahaha.vn/en/san-pham/iflytek-ai-glasses/','exact-model'],
 ['https://tainghephiendich.com/iflytek-ai-glasses/','exact-model'],
 ['https://mayphiendich.net/en/8972','exact-model'],
 ['https://www.openchinacart.com/products/2010225999563791','accessory-listing'],
 ['https://jikemijing.com/product/57','exact-model-directory'],
 ['https://www.xunfei.cn/categories','official-store'],
 ['https://www.xunfei.cn/?goodsId=2','official-store'],
 ['https://www.xunfei.cn/help/','official-help'],
 ['https://fr.iflytek.com/','regional-store'],
 ['https://uk.iflytek.com/','regional-store'],
 ['https://store.iflytek.com/','regional-store'],
 ['https://global.iflytek.com/en/','regional-store'],
 ['https://www.itenspace.com/iflytek-ai-glasses-release-supports-122-language-translations-priced-at-4299-yuan/','supplier-news'],
 ['https://www.stark-mit-technik.de/smart-glasses/info-brillen/','directory'],
 ['https://gold-optical.com/ai-glasses/','different-hardware-G100'],
 ['https://auroraaiglass.com/','different-hardware-HeyCyan'],
 ['https://www.alibaba.com/product-detail/AI-Camera-Smart-Photo-taking-Glasses_1601689773331.html','different-hardware-HeyCyan'],
 ['https://www.tvcmall.com/details/e02-smart-ai-glasses-for-photography-8mp-camera-anti-shake-image-recognition-ai-translation-with-dual-lens-e02l-137mm-sku6804000830b.html','different-hardware-E02']
];
async function main(){await pool(seeds.map(([u,s])=>()=>page(u,s)));const follow=[];
 for(const r of records.filter(r=>r.links)){
  let used=0;for(const l of r.links){if(used>=5)break;let u=new URL(l.url);const text=l.text+' '+l.url;
   if(/login|register|cart|checkout|polic|terms|shipping|return|wp-login|facebook|instagram|twitter|youtube|linkedin|pinterest|tiktok|mailto|whatsapp/i.test(text))continue;
   if((/download|apk|sdk|manual|firmware|support|help|下载|说明书|帮助|ứng dụng|hướng dẫn/i.test(text)&&u.hostname===new URL(r.url).hostname)||(/iflytek.*glasses|讯飞.*眼镜/i.test(l.text)&&/product|goods|item/i.test(u.pathname))){if(!records.some(x=>x.url===l.url)&&!follow.some(x=>x.url===l.url)){follow.push({url:l.url,scope:r.scope,parent:r.url});used++;}}
  }
 }
 await pool(follow.map(r=>()=>page(r.url,r.scope,r.parent)));console.log(JSON.stringify({pages:records.length,followed:follow.length,new:records.filter(r=>r.file).length}));
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1});
module.exports={page,pool,out,records,save,hashes};
