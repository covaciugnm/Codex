import {createRequire} from 'node:module';
import {writeFile,stat} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||'/home/saga-server/site-uri/cesiro1-site/e2e/package.json');
const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true});const page=await browser.newPage();
const root=path.resolve(import.meta.dirname,'..');const report=[];
try{
 await page.goto('http://127.0.0.1:4160/healthz');
 for(const file of ['hero-scan','room-scan']){
  const encoded=await page.evaluate(async name=>{const image=new Image();image.src='/assets/'+name+'.png';await image.decode();const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;canvas.getContext('2d').drawImage(image,0,0);return canvas.toDataURL('image/webp',.85).split(',')[1];},file);
  const output=Buffer.from(encoded,'base64');await writeFile(path.join(root,'public/assets',file+'.webp'),output);report.push({asset:file,operation:'Lossy WebP encoding at original dimensions; original PNG retained',original_bytes:(await stat(path.join(root,'public/assets',file+'.png'))).size,webp_bytes:output.length});
 }
 await writeFile(path.join(root,'docs/asset-optimization.json'),JSON.stringify({created:new Date().toISOString(),files:report},null,2));console.log(JSON.stringify(report));
}finally{await browser.close();}
