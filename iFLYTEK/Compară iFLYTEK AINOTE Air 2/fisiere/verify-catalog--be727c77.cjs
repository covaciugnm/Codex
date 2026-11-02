const fs=require('fs'),p=require('path'),vm=require('vm');const root=p.resolve(__dirname,'..');
const elements={};for(const name of ['query','group','count','results'])elements[name]={value:'',textContent:'',innerHTML:'',addEventListener(){}};
const ctx={window:{},document:{getElementById:n=>elements[n]}};vm.createContext(ctx);for(const f of ['inventar/classes.js','catalog.js'])vm.runInContext(fs.readFileSync(p.join(root,f),'utf8'),ctx);
if(elements.count.textContent!=='47219 clase')throw Error('Initial count');
elements.query.value='BtGlassRecorder';vm.runInContext('render()',ctx);if(!elements.results.innerHTML.includes('BtGlassRecorder'))throw Error('Search');
elements.query.value='no_class_can_match_this_987654';vm.runInContext('render()',ctx);if(elements.count.textContent!=='0 clase')throw Error('No matches');
elements.query.value='';elements.group.value='Bluetooth-ochelari-casti';vm.runInContext('render()',ctx);if(elements.count.textContent!=='171 clase')throw Error('Module filter');
const results={search:true,noMatches:true,moduleFilter:true,initialCount:47219,browserVisualCheck:false};fs.writeFileSync(p.join(root,'inventar/catalog-tests.json'),JSON.stringify(results,null,2));console.log(results);
const sw=p.resolve(root,'..');for(const rel of ['Biblioteca_Glasses/INDEX.html','INDEX.html']){const target=p.join(sw,rel);let html=fs.readFileSync(target,'utf8');if(!html.includes('id="apk-reconstituit"')){const href=rel.startsWith('Biblioteca')?'../APK_Reconstituit_2026-10-30/INDEX.html':'APK_Reconstituit_2026-10-30/INDEX.html';html=html.replace(/<body[^>]*>/i,m=>m+'<p id="apk-reconstituit"><a href="'+href+'"><strong>APK reconstituit integral — clase, Smali, API, JNI și documentații</strong></a></p>');fs.writeFileSync(target,html);}}
