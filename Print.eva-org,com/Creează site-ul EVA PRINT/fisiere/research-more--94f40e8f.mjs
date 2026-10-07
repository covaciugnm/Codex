import fs from 'node:fs/promises';import path from 'node:path';
const root=path.resolve('EVA_PRINT_WEBSITE_BRIEF_2026-10-02');
const manifest=JSON.parse(await fs.readFile(path.join(root,'09_SOURCES/download-manifest.json')));const pages=JSON.parse(await fs.readFile(path.join(root,'09_SOURCES/pages.json')));
const dec=s=>s.replace(/&amp;|&#038;/g,'&').replace(/&quot;/g,'"').replace(/&nbsp;/g,' ');
const txt=s=>dec(s.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')).trim();
const safe=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
async function get(url,rel,kind,source=url){try{const r=await fetch(url,{signal:AbortSignal.timeout(35000)});if(!r.ok)throw Error('HTTP '+r.status);const b=Buffer.from(await r.arrayBuffer());if(kind==='pdf'&&b.subarray(0,5).toString()!=='%PDF-')throw Error('Not PDF');if(kind==='image'&&!/image\//.test(r.headers.get('content-type')||''))throw Error('Not image');await fs.mkdir(path.dirname(path.join(root,rel)),{recursive:true});await fs.writeFile(path.join(root,rel),b);manifest.push({url,final_url:r.url,path:rel,kind,status:'downloaded',bytes:b.length,content_type:r.headers.get('content-type'),source_page:source,publication_rights:kind==='image'?'reference_only_permission_required':'manufacturer_reference',checked_at:'2026-10-02'});return b.toString();}catch(e){manifest.push({url,path:rel,kind,status:'failed',error:e.message,source_page:source});return null;}}
async function pool(a,fn,n=6){let i=0;await Promise.all(Array.from({length:n},async()=>{while(i<a.length)await fn(a[i++]);}));}
async function page(id,url){let html=await get(url,'09_SOURCES/private_html/'+id+'.html','html');if(html){pages.push({id,url,title:txt(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||id),text:txt(html)});return html;}return '';}
const fh=await fs.readFile(path.join(root,'09_SOURCES/private_html/fiberlogy-materials.html'),'utf8');
const fu=[...new Set([...fh.matchAll(/href=["']([^"']+)["']/g)].map(m=>dec(m[1])).filter(x=>/^https:\/\/fiberlogy.com\/en\/filaments\/[^/]+\/[^/]+\/$/.test(x)))];
await pool(fu,async u=>page('fiberlogy-'+u.split('/').filter(Boolean).at(-1),u));
await pool([
 ['fillamentum-data','https://fillamentum.com/pages/data-sheets-and-3d-printing-guides/'],
 ['polymaker-data','https://polymaker.com/download-material/'],
 ['polymaker-cn-data','https://polymaker.com.cn/download-material/'],
 ['prusa-automotive','https://www.prusa3d.com/page/automotive-industry_236464/'],
 ['modix-applications','https://www.modix3d.com/applications/']
],async([id,u])=>page(id,u));
const products=['thermax-pps','thermax-peek-1','thermax-pekk-a-1','thermax-pei-ultem-1010','thermax-pei-ultem-9085','fluorx-pvdf-1','thermax-ppe-ps-1','aquatek-pva-1','3dxstat-esd-pla-1','3dxstat-esd-petg-1','3dxstat-esd-abs-1','3dxlabs-emi-abs','3dxlabs-peba-90a','3dxlabs-pet-cf','carbonx-pa6-cf','carbonx-asa-cf','carbonx-petg-cf','3dxlabs%E2%84%A2-fr-pc'];
await pool(products,async p=>page('3dxtech-'+safe(p),'https://www.3dxtech.com/products/'+p));
const tasks=[];
for(const p of pages){if(/feed|materials$|guide$/.test(p.id))continue;const html=await fs.readFile(path.join(root,'09_SOURCES/private_html/'+p.id+'.html'),'utf8').catch(()=>null);if(!html)continue;
 const docs=[...new Set([...html.matchAll(/href=["']([^"']+\.(?:pdf|zip)(?:\?[^"']*)?)["']/gi)].map(m=>new URL(dec(m[1]),p.url).href))];
 for(const [i,u] of docs.entries()){if(/\b(sds|msds)\b|safety|_sds|_msds/i.test(u)&&/_(pl|de|fr|es|cs|cz)\b/i.test(u))continue;if(/ISO_9001|catalog|whitepaper/i.test(u))continue;const kind=/\.zip/i.test(u)?'zip':'pdf';let file=decodeURIComponent(new URL(u).pathname.split('/').at(-1)).replace(/[^a-zA-Z0-9_.-]/g,'_');if(!file)file='document-'+i+'.'+kind;tasks.push([u,'06_DATASHEETS/'+p.id+'/'+file,kind,p.url]);}
 const imgs=[...new Set([...html.matchAll(/(?:src|data-src|href|srcset)=["']([^"']+\.(?:jpg|jpeg|png|webp)(?:\?[^"'\s]*)?)["']/gi)].map(m=>new URL(dec(m[1]),p.url).href))].filter(x=>!/(logo|icon|avatar|flag|country|badge|360_degrees|256x236|202x202|150x150)/i.test(x));
 let select=imgs.filter(x=>/544x408|scaled|case|model|application|print|part|gear|spool|render/i.test(x));if(!select.length)select=imgs;
 for(const [i,u] of select.slice(0,4).entries()){let ext=new URL(u).pathname.match(/\.(jpg|jpeg|png|webp)$/i)?.[1]||'jpg';tasks.push([u,'04_REFERENCE_PHOTOS/'+p.id+'/reference-'+(i+1)+'.'+ext,'image',p.url]);}
}
await pool(tasks,async a=>{if(!manifest.some(m=>m.url===a[0]&&m.status==='downloaded'))await get(...a);},8);
await fs.writeFile(path.join(root,'09_SOURCES/pages.json'),JSON.stringify(pages,null,2));await fs.writeFile(path.join(root,'09_SOURCES/download-manifest.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify({pages:pages.length,downloaded:manifest.filter(x=>x.status==='downloaded').reduce((a,x)=>(a[x.kind]=(a[x.kind]||0)+1,a),{}),failed:manifest.filter(x=>x.status==='failed').map(x=>({url:x.url,error:x.error})),tdsSources:pages.filter(p=>/fiberlogy|3dxtech|polymaker|fillamentum/.test(p.id)).map(p=>({id:p.id,title:p.title,tds:manifest.filter(m=>m.source_page===p.url&&m.kind==='pdf'&&m.status==='downloaded').length}))},null,2));
