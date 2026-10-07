import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('EVA_PRINT_WEBSITE_BRIEF_2026-10-02');
const dirs=['00_README','01_PROMPT','02_MATERIALS','03_INDUSTRIES','04_REFERENCE_PHOTOS','05_TECHNICAL_DRAWINGS','06_DATASHEETS','07_DATABASE','08_LOCALIZATION','09_SOURCES/private_html','10_AUTH_AND_ORDER','11_PREVIEW','12_VALIDATION'];
for(const d of dirs) await fs.mkdir(path.join(root,d),{recursive:true});
const manifest=[];const pages=[];
const decode=s=>s.replace(/&amp;/g,'&').replace(/&#0*39;|&apos;/g,"'").replace(/&quot;/g,'"').replace(/&nbsp;/g,' ').replace(/&#(\d+);/g,(_,n)=>String.fromCharCode(+n));
const plain=s=>decode(s.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')).trim();
const slug=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
async function get(url,rel,kind,source=url){
 try{const r=await fetch(url,{signal:AbortSignal.timeout(40000),headers:{'User-Agent':'EVA PRINT research archive contact print@eva-org.com'}});if(!r.ok)throw Error('HTTP '+r.status);const b=Buffer.from(await r.arrayBuffer());if(kind==='pdf'&&b.subarray(0,5).toString()!=='%PDF-')throw Error('Not a PDF');if(kind==='image'&&!/image\//.test(r.headers.get('content-type')||''))throw Error('Not an image');await fs.mkdir(path.dirname(path.join(root,rel)),{recursive:true});await fs.writeFile(path.join(root,rel),b);manifest.push({url,final_url:r.url,path:rel,kind,status:'downloaded',bytes:b.length,content_type:r.headers.get('content-type'),source_page:source,publication_rights:kind==='image'?'reference_only_permission_required':'manufacturer_document_reference',checked_at:'2026-10-02'});return b.toString();}catch(e){manifest.push({url,path:rel,kind,status:'failed',error:e.message,source_page:source});return null;}
}
async function pool(items,fn,n=5){let i=0;await Promise.all(Array.from({length:n},async()=>{while(i<items.length){const item=items[i++];await fn(item);}}));}
const hubs=[
 ['prusament-materials','https://prusament.com/materials/'],
 ['prusa-material-guide','https://help.prusa3d.com/filament-material-guide'],
 ['prusa-xl','https://www.prusa3d.com/product/original-prusa-xl-5-toolhead-3d-printer/'],
 ['rat-rig-v-core-4-1','https://ratrig.com/products/rat-rig-v-core-4-1'],
 ['modix-big-meter','https://www.modix3d.com/big-meter/'],
 ['modix-tech-specs','https://www.modix3d.com/tech-specs/'],
 ['fiberlogy-materials','https://fiberlogy.com/en/fiberlogy-filaments/'],
 ['fillamentum-datasheets','https://fillamentum.com/technical-datasheets/'],
 ['polymaker-downloads','https://polymaker.com/downloads/'],
 ['3dxtech-materials','https://www.3dxtech.com/'],
 ['eu-login','https://trusted-digital-identity.europa.eu/eu-login-help/external-user-portal_en'],
 ['google-login','https://developers.google.com/identity/openid-connect']
];
await pool(hubs,async([id,url])=>{let html=await get(url,'09_SOURCES/private_html/'+id+'.html','html');if(html)pages.push({id,url,title:plain(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||id),html});});
let ph=pages.find(p=>p.id==='prusament-materials');
const urls=[...new Set([...ph.html.matchAll(/href=["']([^"']+)["']/g)].map(m=>decode(m[1])).filter(u=>/^https:\/\/prusament.com\/materials\/[^/]+\//.test(u)))];
await pool(urls,async url=>{let id='prusament-'+url.split('/').filter(Boolean).at(-1);let html=await get(url,'09_SOURCES/private_html/'+id+'.html','html');if(html)pages.push({id,url,title:plain(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||id),html});});
await fs.writeFile(path.join(root,'09_SOURCES/pages.json'),JSON.stringify(pages.map(({html,...p})=>({...p,text:plain(html)})),null,2));
await fs.writeFile(path.join(root,'09_SOURCES/download-manifest.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify({root,pages:pages.map(p=>({id:p.id,url:p.url,pdfs:[...new Set([...p.html.matchAll(/(?:href|src)=["']([^"']+\.pdf(?:\?[^"']*)?)["']/gi)].map(m=>decode(m[1])))].slice(0,30),images:[...new Set([...p.html.matchAll(/(?:src|data-src)=["']([^"']+\.(?:jpg|jpeg|png|webp)(?:\?[^"']*)?)["']/gi)].map(m=>decode(m[1])))].filter(x=>!/(logo|icon|avatar|flag)/i.test(x)).slice(0,5)})),failed:manifest.filter(x=>x.status==='failed')},null,2));
