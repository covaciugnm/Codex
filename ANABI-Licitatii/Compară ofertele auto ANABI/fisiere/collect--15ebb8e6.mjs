import fs from 'node:fs';
fs.mkdirSync('sources',{recursive:true});
const clean=s=>s.replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
let listings=[];
for(let p=1;p<=54;p++){
 const url=`https://anabi.just.ro/licitatiionline/ads?page=${p}&shortBy=price_high_to_low`;
 const html=await (await fetch(url)).text();fs.writeFileSync(`sources/list-${p}.html`,html);
 const blocks=html.split('<div class="item-loop col-md-3">').slice(1);
 for(const b of blocks){const m=b.match(/class="licitatie-box-title" href="([^"]+)" title="([^"]+)"/);if(!m)continue;
 listings.push({url:m[1],title:clean(m[2]),id:+m[1].match(/auction\/(\d+)/)[1],price:clean(b.match(/Pret de pornire:<\/b>([^<]+)/)?.[1]||''),date:b.match(/data-expire-date="([^"]+)"/)?.[1],image:b.match(/<img[^>]+src="([^"]+)"/)?.[1],category:clean(b.match(/class="price text-muted"[^>]*>([\s\S]*?)<\/a>/)?.[1]||'')});}
 console.log(p,blocks.length);
}
listings=[...new Map(listings.map(x=>[x.id,x])).values()];fs.writeFileSync('sources/listings.json',JSON.stringify(listings,null,2));
console.log('TOTAL',listings.length);console.log(JSON.stringify(listings.filter(x=>x.date>='2026-10-12'),null,2));
