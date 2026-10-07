const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'../outputs/dracula-design-office/dist');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
let count=0;
for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g)){
 const url=match[1];
 if(url.startsWith('data:'))continue;
 if(url.startsWith('#')){if(!html.includes('id="'+url.slice(1)+'"'))throw Error('Missing anchor: '+url);}
 else if(!fs.existsSync(path.join(root,url)))throw Error('Missing asset: '+url);
 count++;
}
console.log('PASS: '+count+' local links and asset references.');
