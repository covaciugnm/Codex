import fs from 'node:fs';
const listings=JSON.parse(fs.readFileSync('sources/listings.json'));
const clean=s=>s.replace(/<[^>]+>/g,' ').replace(/&nbsp;|&#160;/g,' ').replace(/&amp;/g,'&').replace(/&ndash;/g,'–').replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/\s+/g,' ').trim();
const candidates=listings.filter(x=>/Autovehicule/.test(x.category)||/autoturism|porsche|porche|bmw|mercedes|audi|volkswagen|skoda|dacia|renault|ford|toyota|land rover|range rover|bentley|ferrari|lamborghini|maserati|opel|peugeot|citroen|volvo|honda|hyundai|kia|lexus|nissan|fiat|seat|suzuki|chevrolet/i.test(x.title));
let result=[];
for(const x of candidates){
 try{const path=`sources/auction-${x.id}.html`;const html=fs.existsSync(path)?fs.readFileSync(path,'utf8'):await (await fetch(x.url)).text();fs.writeFileSync(path,html);
 const start=html.indexOf('În temeiul'); const end=html.indexOf('Istoricul ofertelor');
 x.text=clean(html.slice(start>=0?start:html.indexOf('<h1'),end));
 x.tables=[...html.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi)].map(m=>[...m[1].matchAll(/<t[dh]\b[^>]*>([\s\S]*?)<\/t[dh]>/gi)].map(c=>clean(c[1])));
 x.docs=[...html.matchAll(/href="([^"]+\.pdf[^"]*)"/gi)].map(m=>m[1]);
 x.vins=[...new Set(x.text.match(/\b[A-HJ-NPR-Z0-9]{17}\b/g)||[])];
 const dates=[...x.text.matchAll(/(?:data de|ziua de|data)\s*(\d{2})[.\/](\d{2})[.\/](20\d{2})/gi)];x.auctionDate=dates.length?`${dates[0][3]}-${dates[0][2]}-${dates[0][1]}`:null;
 result.push(x);if(result.length%40===0)console.log(result.length,'/',candidates.length);
 }catch(e){console.log('ERROR',x.id,e.message);}
}
fs.writeFileSync('sources/details.json',JSON.stringify(result,null,2));
console.log('RECENT',JSON.stringify(result.filter(x=>x.auctionDate>='2026-10-12').map(({text,tables,...x})=>x),null,2));
