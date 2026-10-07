import {readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const file=path.join(root,'public/product-story.js');let code=await readFile(file,'utf8');
function replace(old,next){if(!code.includes(old))throw Error('Missing target: '+old.slice(0,90));code=code.replace(old,next);}
if(!code.includes('function customerSelectors')){
 code="import {useCases,useCaseCategories} from './usecases-data.js';\n"+code;
 replace("let mode='object',role='architect';","let mode='space',role='architect',customer='architect',problem='apartment-plan';");
 replace("builder:['09-repair-foreman','spaces.repairAlt']","builder:['09-repair-foreman','spaces.repairAlt'],maker:['06-architect','campaign.slide1Alt'],property:['08-design-couple','spaces.designAlt'],creator:['02-face','campaign.slide2Alt']");
 const insertion=`
  const customerOrder=['architect','designer','builder','maker','property','creator'];
  const categoryProfiles={architect:['spaces_property','repair_construction','measure_diy'],designer:['interior_design','objects_print','measure_diy'],builder:['repair_construction','measure_diy'],maker:['objects_print'],property:['spaces_property','measure_diy','repair_construction'],creator:['people_creative','objects_print'],all:useCaseCategories};
  const defaultProblems={architect:'apartment-plan',designer:'room-redesign',builder:'repair-list',maker:'print-replica',property:'property-presentation',creator:'portrait-keepsake',all:'furniture-fit'};
  const caseMode=item=>item.module==='/measure'?'measure':item.module==='/spaces'?'space':'object';
  const currentCase=()=>useCases.find(item=>item.id===problem);
  const rolePath=()=>role==='maker'?'/objects':role==='creator'?'/people':'/spaces';
  const sample=()=>role==='maker'?['cube-100mm.stl','docs.sampleCube','docs.sampleText']:role==='creator'?['reference-cloud.ply','docs.sampleCloud','docs.sampleText']:['room-4x3m.dxf','v2.sampleDownload','v2.sampleNote'];
  function problemOptions(){return categoryProfiles[customer].map(category=>'<optgroup label="'+s('uses.category.'+category)+'">'+useCases.filter(item=>item.category===category).map(item=>'<option value="'+item.id+'" '+(problem===item.id?'selected':'')+'>'+s('usecase.'+item.id+'.title')+'</option>').join('')+'</optgroup>').join('');}
  function customerSelectors(){return '<div class="customer-finder"><label for="customer-profile"><span>01</span>'+s('v2.customerLabel')+'</label><select id="customer-profile">'+[...customerOrder,'all'].map(id=>'<option value="'+id+'" '+(customer===id?'selected':'')+'>'+s(id==='all'?'v2.anyProfile':'v2.'+id)+'</option>').join('')+'</select><label for="customer-problem"><span>02</span>'+s('v2.problemLabel')+'</label><select id="customer-problem">'+problemOptions()+'</select></div>';}
  function customerAnswer(){const item=currentCase();return '<span class="eyebrow">'+s('v2.result')+'</span><h2>'+s('usecase.'+item.id+'.title')+'</h2><p>'+s('usecase.'+item.id+'.description')+'</p>'+link(item.module,'v2.detail','text-link');}
  function modeControls(){return '<div class="mode-selector" role="group" aria-label="'+s('v2.choose')+'">'+modes.map(m=>'<button data-demo="'+m+'" aria-pressed="'+(mode===m)+'">'+icon(icons[m])+s('v2.'+m)+'</button>').join('')+'</div>';}
  function refreshCustomer({updateOptions=false}={}){
    const item=currentCase();mode=caseMode(item);
    const stageElement=document.getElementById('product-demo');
    if(!stageElement)return;
    if(updateOptions)document.getElementById('customer-problem').innerHTML=problemOptions();
    stageElement.dataset.mode=mode;stageElement.innerHTML=stage();
    document.getElementById('customer-answer').innerHTML=customerAnswer();
    document.getElementById('demo-outcomes').innerHTML=outcomes();
    document.getElementById('role-panel').innerHTML=rolePanel();
    document.querySelectorAll('[data-demo]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.demo===mode)));
    document.querySelectorAll('[data-profession]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.profession===role)));
  }
  document.addEventListener('change',event=>{
    if(event.target.id==='customer-profile'&&Object.hasOwn(categoryProfiles,event.target.value)){
      customer=event.target.value;role=customer==='all'?'designer':customer;problem=defaultProblems[customer];refreshCustomer({updateOptions:true});
    }
    if(event.target.id==='customer-problem'&&useCases.some(item=>item.id===event.target.value&&categoryProfiles[customer].includes(item.category))){
      problem=event.target.value;
      if(customer==='all')role=({objects_print:'maker',measure_diy:'builder',interior_design:'designer',repair_construction:'builder',spaces_property:'property',people_creative:'creator'})[currentCase().category];
      refreshCustomer();
    }
  });
`;
 replace('  const drawing=()',insertion+'  const drawing=()');
 replace("${s('v2.kicker')}","${s('v2.customerKicker')}");
 const oldControls=code.slice(code.indexOf('<div class="mode-selector" role="group" aria-label="${s('),code.indexOf('<div class="button-row"><a class="button primary" href="#product-demo">'));
 replace(oldControls,'${customerSelectors()}');
 replace('<a class="button primary" href="#product-demo">${s(\'v2.demoCta\')} <span aria-hidden="true">↗</span></a><a class="button story-secondary" href="#your-work">${s(\'v2.rolesCta\')} <span aria-hidden="true">↓</span></a>', '<a class="button primary" href="#customer-answer">${s(\'v2.detail\')} <span aria-hidden="true">↗</span></a>'+"${link('/uses','v2.nextCta','button story-secondary')}");
 replace('<section class="container result-section"><div class="demo-outcomes"', '<section class="container customer-result"><div id="customer-answer" aria-live="polite">${customerAnswer()}</div><div class="customer-demo-choice"><span class="eyebrow">${s(\'v2.choose\')}</span>${modeControls()}<p>${s(\'v2.sampleOnly\')}</p></div></section><section class="container result-section"><div class="demo-outcomes"');
 replace("${['architect','designer','builder'].map(r=>",'${customerOrder.map(r=>');
 replace("${s('v2.'+r)} <span aria-hidden=\"true\">↗</span>","<small>${s('v2.'+r)}</small><strong>${s('v2.activity.'+r)}</strong><span aria-hidden=\"true\">↗</span>");
 replace("${s('v2.rolesTitle')}</h2>","${s('v2.clientsTitle')}</h2>");
 replace("${s('v2.rolesIntro')}</p>","${s('v2.clientsIntro')}</p>");
 replace("aria-label=\"${s('v2.rolesTitle')}\"","aria-label=\"${s('v2.clientsTitle')}\"");
 replace('href="/downloads/room-4x3m.dxf" download>${s(\'v2.sampleDownload\')}', 'href="/downloads/${sample()[0]}" download>${s(sample()[1])}');
 replace("${s('v2.sampleNote')}</small>","${s(sample()[2])}</small>");
 replace("${link('/spaces','v2.detail','text-link')}","${link(rolePath(),'v2.detail','text-link')}");
 // Activity examples precede the technical modules.
 const moduleStart=code.indexOf('<section class="product-modules container"');
 const roleStart=code.indexOf('<section class="professional-section"',moduleStart);
 const roleEnd=code.indexOf('<section class="inspiration-section',roleStart);
 const module=code.slice(moduleStart,roleStart),professional=code.slice(roleStart,roleEnd);
 code=code.slice(0,moduleStart)+professional+module+code.slice(roleEnd);
 await writeFile(file,code);
}
if(process.argv.includes('--locales')){
 const addition=JSON.parse(await readFile(path.join(root,'content/customer-segments.json'),'utf8'));
 const keys=Object.keys(addition.en).sort();
 for(const lang of ['en','ro','de','fr','es','hu','bg']){
  if(JSON.stringify(Object.keys(addition[lang]).sort())!==JSON.stringify(keys))throw Error('Customer translation keys '+lang);
  if(Object.values(addition[lang]).some(value=>typeof value!=='string'||!value.trim()))throw Error('Empty translation '+lang);
  const p=path.join(root,'content/locales',lang+'.json');const dictionary=JSON.parse(await readFile(p,'utf8'));Object.assign(dictionary,addition[lang]);await writeFile(p,JSON.stringify(dictionary,null,2)+'\n');
 }
 console.log(JSON.stringify({customerKeys:keys.length,locales:7}));
}
