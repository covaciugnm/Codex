import {readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
async function patch(file,old,next){const p=path.join(root,file);let text=await readFile(p,'utf8');if(text.includes(next))return;if(!text.includes(old))throw Error('Missing target '+old.slice(0,100));await writeFile(p,text.replace(old,next));}
await patch('public/product-story.js',"02 / ${s('v2.rolesEyebrow')}","01 / ${s('v2.rolesEyebrow')}");
await patch('public/product-story.js',"01 / EVA-3dScan</span><h2>${s('v2.modulesTitle')}","02 / EVA-3dScan</span><h2>${s('v2.modulesTitle')}");
await patch('public/product-story.js',"${s('v2.'+mode+'Result')}","${s(currentCase().module==='/people'&&mode==='object'?'usecase.'+problem+'.title':'v2.'+mode+'Result')}");
await patch('public/app.js',"const storyFocus=active?.hasAttribute('data-faq')?", "const storyFocus=['customer-profile','customer-problem'].includes(active?.id)?'#'+active.id:active?.hasAttribute('data-faq')?");
await patch('public/product-story.js',"  const drawing=()=>mode==='object'?",`  const portraitDrawing=()=>'<svg viewBox="0 0 300 330" aria-hidden="true"><g fill="none" stroke="#79efdc" stroke-width="1.4"><ellipse cx="150" cy="128" rx="62" ry="84"/><path d="M91 105h118M89 140h122M102 174h96M118 52l-8 140m39-149v169m31-160 11 140M90 114l120 38M90 152l121-38M70 296v-40q14-36 58-45m44 0q44 9 58 45v40M70 256h160M90 230l120 64m0-64L90 294"/></g><text x="150" y="322" text-anchor="middle" fill="#c6d5ed" font-size="12">3D</text></svg>';
  const drawing=()=>mode==='object'&&currentCase().module==='/people'?portraitDrawing():mode==='object'?`);
await patch('public/product-story.js','${scene[mode]}.webp','${currentCase().module===\'/people\'&&mode===\'object\'?\'02-face\':scene[mode]}.webp');
await patch('public/product-story.js',"alt=\"${s(alt[mode])}\"","alt=\"${s(currentCase().module==='/people'&&mode==='object'?'campaign.slide2Alt':alt[mode])}\"");
await patch('public/product-story.js',"${s('v2.'+(mode==='object'?'dimension':mode==='measure'?'wall':'connected'))}","${currentCase().module==='/people'&&mode==='object'?'3D':s('v2.'+(mode==='object'?'dimension':mode==='measure'?'wall':'connected'))}");
await patch('public/product-story.js',"${mode==='object'?'100 × 100 × 100 mm':mode==='measure'?'4.00 m':'3D → 2D'}","${mode==='object'?(currentCase().module==='/people'?'3D':'100 × 100 × 100 mm'):mode==='measure'?'4.00 m':'3D → 2D'}");
// Extra role illustrations remain labelled synthetic, with accessible text.
await patch('public/product-story.js',"function roleProof(){return",`function roleProof(){if(role==='maker'||role==='creator')return '<div class="role-proof"><div><small>'+s('v2.demoLabel')+'</small><strong>'+s('v2.preview')+'</strong></div><svg viewBox="0 0 260 110" role="img" aria-label="'+s('v2.demoLabel')+': '+(role==='maker'?'100 × 100 × 100 mm':'3D')+'">'+(role==='maker'?'<path class="proof-wall" d="m125 10 50 23v49l-50 23-50-23V33Z M75 33l50 24 50-24M125 57v48"/><text x="210" y="62" text-anchor="middle">100 mm</text>':'<g fill="none" stroke="#2549eb"><ellipse cx="130" cy="45" rx="25" ry="33"/><path d="M105 32h50m-50 20h50m-45 13h40m-20-53v66M90 105V89l24-13m32 0 24 13v16M114 18l-5 47m37-47 5 47"/></g><text x="205" y="60">3D</text>')+'</svg></div>';return`);
await patch('public/product-story.js',`      role=profession.dataset.profession;
      const target=document.getElementById('role-panel');
      if(target){target.innerHTML=rolePanel();document.querySelectorAll('[data-profession]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.profession===role)));}`,`      role=profession.dataset.profession;customer=role;problem=defaultProblems[role];
      const profile=document.getElementById('customer-profile');if(profile)profile.value=customer;
      refreshCustomer({updateOptions:true});`);
// Object measurements do not imply body measurements in the creative-person workflow.
await patch('public/product-story.js',"function outcomes(){return [['capture','Input']", "function outcomes(){if(currentCase().module==='/people'&&mode==='object')return '<div><span class=\"outcome-index\">01</span><span><small>'+s('v2.capture')+'</small><strong>'+s('people.title')+'</strong></span></div><div><span class=\"outcome-index\">02</span><span><small>'+s('v2.result')+'</small><strong>'+s('usecase.'+problem+'.title')+'</strong></span></div><div><span class=\"outcome-index\">03</span><span><small>'+s('v2.use')+'</small><strong>'+s('usecase.'+problem+'.description')+'</strong></span></div>';return [['capture','Input']");
