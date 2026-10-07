const fs=require('fs'),path=require('path'),cp=require('child_process');const {pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..');const browser=process.argv[2];if(!browser)throw Error('Pass installed Chromium/Edge executable');
const profile=process.argv[3];if(!profile)throw Error('Pass separate browser profile directory outside dossier');
const source=path.join(root,'08_livrabile/DOSAR_COMPLET.html');const pdf=path.join(root,'08_livrabile/DOSAR_COMPLET.pdf');
const args=['--headless','--disable-gpu','--no-first-run','--no-pdf-header-footer','--user-data-dir='+profile,'--print-to-pdf='+pdf,pathToFileURL(source).href];
const result=cp.spawnSync(browser,args,{encoding:'utf8',timeout:90000,windowsHide:true});
if(!fs.existsSync(pdf)||fs.statSync(pdf).mtimeMs<fs.statSync(source).mtimeMs){console.error(result.stderr||result.error||'No fresh PDF');process.exit(1);}
const data=fs.readFileSync(pdf);const pages=(data.toString('latin1').match(/\/Type\s*\/Page\b/g)||[]).length;
console.log(JSON.stringify({pdf,bytes:data.length,pages,exit_code:result.status}));
