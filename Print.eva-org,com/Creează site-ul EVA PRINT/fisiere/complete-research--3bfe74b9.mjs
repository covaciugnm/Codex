import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('EVA_PRINT_WEBSITE_BRIEF_2026-10-02');
const load=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const save=async(p,x)=>fs.writeFile(path.join(root,p),JSON.stringify(x,null,2));
const manifest=await load('09_SOURCES/download-manifest.json');
const cases=await load('03_INDUSTRIES/documented-external-cases.json');
const xml=await fs.readFile(path.join(root,'09_SOURCES/modix-cases.xml'),'utf8');
const dec=s=>s.replaceAll('&amp;','&').replaceAll('&quot;','"').replaceAll('&lt;','<').replaceAll('&gt;','>').replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,'$1').trim();
async function download(url,rel,source,kind){
 const previous=manifest.find(d=>d.url===url&&d.status==='downloaded');
 if(previous)return previous;
 const item={url,path:rel,source_page:source,kind,checked_at:'2026-10-02',rights_status:'reference_only_permission_required'};
 try{const r=await fetch(url,{signal:AbortSignal.timeout(35000)});if(!r.ok)throw Error('HTTP '+r.status);const b=Buffer.from(await r.arrayBuffer());if(kind==='image'&&!/image/.test(r.headers.get('content-type')||''))throw Error('Not an image');if(kind==='pdf'&&b.subarray(0,5).toString()!=='%PDF-')throw Error('Not a PDF');await fs.mkdir(path.dirname(path.join(root,rel)),{recursive:true});await fs.writeFile(path.join(root,rel),b);Object.assign(item,{status:'downloaded',bytes:b.length});}catch(e){item.status='failed';item.error=e.message;}manifest.push(item);return item;
}
const pending=[...xml.matchAll(/<case id="([^"]+)">([\s\S]*?)<\/case>/g)];
for(let n=0;n<pending.length;n+=4){await Promise.all(pending.slice(n,n+4).map(async([,id,body])=>{
 if(cases.some(c=>c.id==='modix-'+id))return;
 const get=tag=>dec(body.match(new RegExp('<'+tag+'(?: [^>]*)?>([\\s\\S]*?)</'+tag+'>'))?.[1]||'');
 const title=get('title'),company=get('company'),printer=get('printer');
 const source=new URL(get('url'),'https://www.modix3d.com').href;
 const refs=[get('image'),...[...body.matchAll(/<image src="([^"]+)"/g)].map(m=>dec(m[1]))].filter(Boolean).slice(0,2);
 const photos=[];for(const [i,ref] of refs.entries()){const url=new URL(ref,'https://www.modix3d.com/lp/cases/').href;const ext=path.extname(new URL(url).pathname)||'.jpg';const d=await download(url,'04_REFERENCE_PHOTOS/modix-cases/'+id+'-'+i+ext,source,'image');if(d.status==='downloaded')photos.push({path:d.path,url,rights:'reference_only_permission_required'});}
 cases.push({id:'modix-'+id,title,source,source_dataset:'https://www.modix3d.com/lp/cases/cases.xml',kind:'documented_external_reference',eva_print_portfolio:false,description:'Modix lists '+title+' as a large-format printing application'+(company?' associated with '+company:'')+'. Consult the linked manufacturer case for the original project context. This is external industry inspiration; EVA PRINT project feasibility is reviewed separately.',material:'Exact filament grade not established from the manufacturer case dataset.',named_user:company||null,external_printer_reference:printer||null,tags:[...body.matchAll(/<tag>(.*?)<\/tag>/g)].map(m=>dec(m[1])),photos,checked_at:'2026-10-02'});
}));}
await save('03_INDUSTRIES/documented-external-cases.json',cases);
await save('09_SOURCES/download-manifest.json',manifest);
console.log(JSON.stringify({modixCases:pending.length,totalCases:cases.length,downloadedCasePhotos:cases.filter(c=>c.id.startsWith('modix-')).reduce((a,c)=>a+c.photos.length,0)}));
