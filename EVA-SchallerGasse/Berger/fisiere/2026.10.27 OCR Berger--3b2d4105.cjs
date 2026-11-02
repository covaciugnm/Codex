const fs=require('fs');const path=require('path');
const {createWorker}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/tesseract.js');
const qa=path.resolve('folder map/2026.10.27 QA Berger adnotari');
(async()=>{
 const workers=await Promise.all([0,1].map(()=>createWorker('deu',1,{langPath:'C:/Program Files/PDFgear/tessdata',gzip:false,cachePath:qa,cacheMethod:'none'})));
 let next=1;
 await Promise.all(workers.map(async w=>{for(;;){let i=next++;if(i>18)break;const {data}=await w.recognize(path.join(qa,`ocr-${i}.png`),{},{text:true,hocr:true,tsv:true});fs.writeFileSync(path.join(qa,`ocr-${i}.json`),JSON.stringify({text:data.text,hocr:data.hocr,tsv:data.tsv,confidence:data.confidence}));console.log(`page ${i}: confidence ${data.confidence}`);}}));
 await Promise.all(workers.map(w=>w.terminate()));
 console.log('OCR COMPLETE');
})().catch(e=>{console.error(e);process.exit(1)});
