import {createRequire} from 'node:module';
import {readFile,writeFile,stat,mkdir} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..');const browser=await chromium.launch({headless:true});const page=await browser.newPage();const result=[];
try{
 for(const name of ['01-capture','02-face','03-objects','04-measure','05-spaces']){
  const source=await readFile(path.join(root,'public/assets/campaign',name+'.png'));
  const encoded=await page.evaluate(async data=>{const image=new Image();image.src='data:image/png;base64,'+data;await image.decode();const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;canvas.getContext('2d').drawImage(image,0,0);return canvas.toDataURL('image/webp',.84).split(',')[1];},source.toString('base64'));
  const output=Buffer.from(encoded,'base64');await writeFile(path.join(root,'public/assets/campaign',name+'.webp'),output);result.push({name,original_bytes:source.length,webp_bytes:output.length});
 }
 const svg=await readFile(path.join(root,'public/assets/eva-app-icon.svg'),'utf8');
 for(const size of [1024,180,32]){
  const encoded=await page.evaluate(async({svg,size})=>{const i=new Image();i.src='data:image/svg+xml;base64,'+svg;await i.decode();const c=document.createElement('canvas');c.width=c.height=size;c.getContext('2d').drawImage(i,0,0,size,size);return c.toDataURL('image/png').split(',')[1];},{svg:Buffer.from(svg).toString('base64'),size});
  await writeFile(path.join(root,`public/assets/eva-app-icon-${size}.png`),Buffer.from(encoded,'base64'));
 }
 await writeFile(path.join(root,'docs/campaign-optimization.json'),JSON.stringify({created:new Date().toISOString(),files:result,operation:'WebP encoding only; original generated PNGs retained'},null,2));console.log(JSON.stringify(result));
}finally{await browser.close();}
