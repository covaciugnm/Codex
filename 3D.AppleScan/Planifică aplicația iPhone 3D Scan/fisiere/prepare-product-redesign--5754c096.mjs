import {readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const read=p=>readFile(path.join(root,p),'utf8');
const write=(p,v)=>writeFile(path.join(root,p),v);
let source=JSON.parse(await read('content/redesign-v2-source.json'));
Object.assign(source.en,{
 'v2.architectSteps':'Capture the rooms|Check dimensions and scale|Review the connected layout',
 'v2.architectDeliverable':'A dimensioned reference of the existing space, to verify and complete during design. CAD exports are planned; editable construction drawings need further work.',
 'v2.designerSteps':'Capture the existing room|Check furniture dimensions|Compare placement in your design',
 'v2.designerDeliverable':'The existing room and relevant dimensions, as a reference for furniture placement and client conversations. Continue the interior design in your chosen design tool.',
 'v2.measureResult':'A temporary distance over the camera view, without automatic saving',
 'v2.sampleDownload':'Open the sample floor plan (DXF)',
 'v2.builderNeed':'Prepare renovation with room dimensions and manually entered observations about areas that need repair.',
 'v2.builderSteps':'Measure the wall or opening|Record your observations manually|Verify installation dimensions on site'
});
Object.assign(source.ro,{
 'v2.architectSteps':'Scanezi camerele|Verifici cotele și scara|Analizezi planul camerelor conectate',
 'v2.architectDeliverable':'O referință cotată a spațiului existent, de verificat și completat în proiectare. Exporturile CAD sunt planificate; planșele de execuție editabile cer prelucrare suplimentară.',
 'v2.designerSteps':'Scanezi camera existentă|Verifici dimensiunile mobilierului|Compari amplasarea în proiect',
 'v2.designerDeliverable':'Camera existentă și dimensiunile relevante, ca referință pentru amplasarea mobilierului și discuția cu clientul. Amenajarea se dezvoltă apoi în instrumentul de proiectare ales.',
 'v2.measureResult':'O distanță temporară peste imaginea camerei, fără salvare automată',
 'v2.sampleDownload':'Deschide planul exemplu (DXF)',
 'v2.builderNeed':'Pregătește renovarea cu dimensiunile camerei și observații introduse manual despre zonele de reparat.',
 'v2.builderSteps':'Măsori peretele sau golul|Notezi manual observațiile|Verifici la fața locului cotele de montaj'
});
await write('content/redesign-v2-source.json',JSON.stringify(source,null,2)+'\n');
if(process.argv.includes('--locales')){
 const translations=JSON.parse(await read('content/redesign-v2-translations.json'));
 const dictionaries={...source,...translations};const reference=Object.keys(source.en).sort();
 for(const lang of ['en','ro','de','fr','es','hu','bg']){
  if(JSON.stringify(Object.keys(dictionaries[lang]).sort())!==JSON.stringify(reference))throw Error('Key mismatch '+lang);
  for(const [key,value] of Object.entries(dictionaries[lang]))if(typeof value!=='string'||!value.trim()||(key.endsWith('Steps')&&value.split('|').length!==3))throw Error('Invalid '+lang+' '+key);
  const existing=JSON.parse(await read('content/locales/'+lang+'.json'));Object.assign(existing,dictionaries[lang]);
  await write('content/locales/'+lang+'.json',JSON.stringify(existing,null,2)+'\n');
 }
 console.log(JSON.stringify({locales:7,updatedKeys:reference.length,totalKeys:Object.keys(JSON.parse(await read('content/locales/en.json'))).length}));
}
if(process.argv.includes('--wire')){
 let app=await read('public/app.js');
 if(!app.includes("import {createProductStory}"))app="import {createProductStory} from './product-story.js';\n"+app;
 const start=app.indexOf('function home(){');const end=app.indexOf('const campaignFiles=',start);
 if(start<0||end<start)throw Error('Home boundaries missing');
 app=app.slice(0,start)+'function home(){return productStory.home();}\n'+app.slice(end);
 if(!app.includes('const productStory='))app=app.replace('loadLanguage(locale);',"const productStory=createProductStory({s,t,h,icon,url,link,badge,campaignFrame,getSlide:()=>campaignSlide,isPaused:()=>carouselPaused});\nloadLanguage(locale);");
 app=app.replace("const focusSelector=useFocused?'#use-search':focused?", "const storyFocus=active?.hasAttribute('data-demo')?'[data-demo=\"'+active.dataset.demo+'\"]':active?.hasAttribute('data-profession')?'[data-profession=\"'+active.dataset.profession+'\"]':null;const focusSelector=storyFocus|| (useFocused?'#use-search':focused?");
 app=app.replace("null):null;if(region&&", "null):null);if(region&&");
 await write('public/app.js',app);
 let html=await read('public/index.html');if(!html.includes('/product-story.css'))html=html.replace('<script src="/app.js"','<link rel="stylesheet" href="/product-story.css">\n  <script src="/app.js"');await write('public/index.html',html);
}
