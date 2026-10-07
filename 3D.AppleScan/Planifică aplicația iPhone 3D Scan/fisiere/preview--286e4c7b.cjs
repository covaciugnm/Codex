const path=require('path'),cp=require('child_process'),fs=require('fs');const{pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..'),browser=process.argv[2],profile=process.argv[3];
const url=pathToFileURL(path.join(root,'08_livrabile/DOSAR_COMPLET.html')).href;
const out=path.join(root,'07_audit/document-preview.png');
const r=cp.spawnSync(browser,['--headless','--disable-gpu','--no-first-run','--user-data-dir='+profile,'--window-size=1440,1100','--screenshot='+out,url],{encoding:'utf8',timeout:45000,windowsHide:true});
if(!fs.existsSync(out)){console.error(r.stderr);process.exit(1);}console.log(out);
