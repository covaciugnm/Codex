const fs=require('fs');
for(const f of ['kaikki-home.html','kaikki-raw.html','kaikki-bengali.html','wikdict-sqlite.html','wikdict-tei.html','wikdict-kobo.html','dictcc-source.html']){
 const t=fs.readFileSync(f,'utf8');
 const a=[...t.matchAll(/href="([^"]+)"/g)].map(x=>x[1]);
 console.log(JSON.stringify({f,links:a.filter(x=>/jsonl|gz|bz2|zip|sqlite|\.tei|\.xml|\.tar/.test(x)).slice(0,f.startsWith('kaikki')?100:12),options:f.startsWith('dictcc')?[...t.matchAll(/<option[^>]*>([^<]+)/g)].map(x=>x[1]):[]}));
}
const d=JSON.parse(fs.readFileSync('freedict-catalog-source.json','utf8').replace(/^\uFEFF/,''));
console.log(JSON.stringify({freecount:d.length,selected:d.filter(x=>/^(eng|deu|fra|spa|ron)-(eng|deu|fra|spa|ron)$/.test(x.name)).map(x=>[x.name,x.headwords,x.status]),last:d.slice(-1)}));
