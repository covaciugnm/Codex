import fs from 'node:fs';
export function extract(file){let html=fs.readFileSync(file,'utf8');let texts=[];for(let m of html.matchAll(/self\.__next_f\.push\((\[[\s\S]*?\])\)<\/script>/g)){try{let a=JSON.parse(m[1]);if(typeof a[1]==='string')texts.push(a[1]);}catch{}}
let txt=texts.join('\n');fs.writeFileSync(file+'.txt',txt);let ads=[];
const walk=o=>{if(!o||typeof o!=='object')return;if(o.shortTitle&&o.id)ads.push(o);for(let v of Object.values(o))walk(v);};
for(let line of txt.split('\n')){let i=line.indexOf(':');try{walk(JSON.parse(line.slice(i+1)));}catch{}}
for(let m of txt.matchAll(/"id":"?\d+/g)){let start=txt.lastIndexOf('{',m.index);for(let j=start,depth=0,str=false,esc=false;j<txt.length;j++){let c=txt[j];if(str){if(esc)esc=false;else if(c==='\\')esc=true;else if(c==='"')str=false;}else{if(c==='"')str=true;else if(c==='{')depth++;else if(c==='}'&&--depth===0){try{let a=JSON.parse(txt.slice(start,j+1));if(a.shortTitle||a.subTitle)ads.push(a);}catch{}break;}}}}
return [...new Map(ads.map(a=>[a.id,a])).values()];}
if(process.argv[2])console.log(JSON.stringify(extract(process.argv[2]),null,2));
