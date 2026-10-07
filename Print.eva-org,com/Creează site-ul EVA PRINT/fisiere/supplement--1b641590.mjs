import fs from 'node:fs/promises';import path from 'node:path';import {spawn} from 'node:child_process';
const root=path.resolve('EVA_PRINT_WEBSITE_BRIEF_2026-10-02');const manifest=JSON.parse(await fs.readFile(path.join(root,'09_SOURCES/download-manifest.json')));const pages=JSON.parse(await fs.readFile(path.join(root,'09_SOURCES/pages.json')));
const dec=s=>s.replace(/&amp;|&#038;/g,'&').replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(+n)).replace(/&quot;/g,'"').replace(/&nbsp;/g,' ');const plain=s=>dec(s.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ')).trim();
async function get(u,rel,kind,source=u){try{const r=await fetch(u,{signal:AbortSignal.timeout(30000)});if(!r.ok)throw Error('HTTP '+r.status);const b=Buffer.from(await r.arrayBuffer());if(kind==='pdf'&&b.subarray(0,5).toString()!=='%PDF-')throw Error('Not PDF');await fs.mkdir(path.dirname(path.join(root,rel)),{recursive:true});await fs.writeFile(path.join(root,rel),b);manifest.push({url:u,final_url:r.url,path:rel,kind,status:'downloaded',bytes:b.length,source_page:source,publication_rights:kind==='image'?'reference_only_permission_required':'manufacturer_reference',checked_at:'2026-10-02'});return b.toString();}catch(e){manifest.push({url:u,path:rel,kind,status:'failed',error:e.message,source_page:source});return '';}}
async function pool(a,fn,n=6){let i=0;await Promise.all(Array.from({length:n},async()=>{while(i<a.length)await fn(a[i++]);}));}
const cases=[
 ['skoda-auto','https://blog.prusa3d.com/3d-printing-in-skoda-auto_73147/'],
 ['jku-linz','https://blog.prusa3d.com/teaching-mathematics-redefined-with-3d-printing-at-jku-linz_123196/'],
 ['victoria-hand','https://blog.prusa3d.com/victoria-hand-project-changing-prosthetic-care-with-3d-printing_119667/'],
 ['architecture','https://www.prusa3d.com/applications/3d-printing-for-architects-and-designers_231948/'],
 ['film','https://www.prusa3d.com/applications/3d-printing-for-the-film-industry-special-effects_231989/'],
 ['manufacturing','https://www.prusa3d.com/applications/3d-printing-for-manufacturing-and-rd_232937/'],
 ['modix-gallery','https://www.modix3d.com/modix-case-study-gallery/'],
 ['modix-gallery-no','https://www.modix3d.com/no/modix-case-study-gallery/'],
 ['fiberlogy-faq','https://fiberlogy.com/faq/'],
 ['eu-login-portal','https://trusted-digital-identity.europa.eu/index_en'],
 ['google-openid','https://developers.google.com/identity/openid-connect?hl=en'],
 ['prusa-logo-and-photos','https://www.prusa3d.com/page/logo-and-photos_236913/']
];
await pool(cases,async([id,u])=>{const html=await get(u,'09_SOURCES/private_html/'+id+'.html','html');if(!html)return;pages.push({id,url:u,title:plain(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||id),text:plain(html)});
 const imgs=[...new Set([...html.matchAll(/(?:src|data-src|href)=["']([^"']+\.(?:jpg|jpeg|png|webp)(?:\?[^"'\s]*)?)["']/gi)].map(m=>new URL(dec(m[1]),u).href))].filter(x=>!/(logo|icon|avatar|flag|country|badge|150x150)/i.test(x));
 if(id!=='fiberlogy-faq')await pool(imgs.filter(x=>/uploads|case|skoda|linz|hand|architect|modix|masslab/i.test(x)).slice(0,id.includes('gallery')?30:5),async(im,i)=>{let ext=new URL(im).pathname.split('.').at(-1);await get(im,'04_REFERENCE_PHOTOS/'+id+'/'+new URL(im).pathname.split('/').at(-1),'image',u);});
 if(id==='fiberlogy-faq'){const ds=[...new Set([...html.matchAll(/href=["']([^"']+\.pdf(?:\?[^"']*)?)["']/gi)].map(m=>new URL(dec(m[1]),u).href))].filter(x=>/tds|technical/i.test(x)&&!manifest.some(m=>m.url===x&&m.status==='downloaded'));await pool(ds,async d=>get(d,'06_DATASHEETS/fiberlogy-faq/'+decodeURIComponent(new URL(d).pathname.split('/').at(-1)).replace(/[^a-zA-Z0-9_.-]/g,'_'),'pdf',u));}
});
async function files(d){let a=[];for(const e of await fs.readdir(d,{withFileTypes:true})){let p=path.join(d,e.name);if(e.isDirectory())a.push(...await files(p));else a.push(p);}return a;}
const pdfs=(await files(path.join(root,'06_DATASHEETS'))).filter(f=>/\.pdf$/i.test(f)&&/tds|technical|data.?sheet|ENG\.pdf|PA11CFB|V5\./i.test(f)&&!/(sds|msds|safety)/i.test(f));
await fs.mkdir(path.join(root,'09_SOURCES/datasheet_text'),{recursive:true});
await pool(pdfs,async f=>{let rel=path.relative(root,f).replaceAll('\\','/');let out=path.join(root,'09_SOURCES/datasheet_text',rel.replace(/[\\/]/g,'__')+'.txt');await new Promise(resolve=>{const proc=spawn('C:\\Program Files\\gs\\gs9.02\\bin\\gswin64c.exe',['-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=txtwrite','-sOutputFile='+out,f],{windowsHide:true,stdio:'ignore'});proc.on('error',resolve);proc.on('exit',resolve);});});
await fs.writeFile(path.join(root,'09_SOURCES/pages.json'),JSON.stringify(pages,null,2));await fs.writeFile(path.join(root,'09_SOURCES/download-manifest.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify({pages:pages.length,files:manifest.filter(x=>x.status==='downloaded').reduce((a,x)=>(a[x.kind]=(a[x.kind]||0)+1,a),{}),extractedText:pdfs.length,newSources:pages.slice(-12).map(x=>x.id)},null,2));
