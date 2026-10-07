import {readFile,writeFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
async function patch(file,old,next){const p=path.join(root,file);let text=await readFile(p,'utf8');if(text.includes(next))return;if(!text.includes(old))throw Error('Missing patch target '+file+' '+old.slice(0,60));await writeFile(p,text.replace(old,next));}
await patch('public/product-story.js','<svg viewBox="0 0 260 110" aria-hidden="true">','<svg viewBox="0 0 260 110" role="img" aria-label="${s(\'v2.demoLabel\')}: ${s(\'v2.dimension\')} ${role===\'builder\'?\'4.00 m\':role===\'designer\'?\'2.00 m / 0.85 m\':\'4.00 m / 3.00 m\'}">');
await patch('public/product-story.js','<small class="sample-disclosure">${s(\'v2.sampleNote\')}</small></div>`;}', '<small class="sample-disclosure">${s(\'v2.sampleNote\')}</small><div class="role-module-link">${link(\'/spaces\',\'v2.detail\',\'text-link\')}</div></div>`;}');
await patch('public/product-story.js','`<details><summary>${s(\'v2.faq\'+i+\'Title\')}','`<details data-question="${i}" ${openQuestions.has(i)?\'open\':\'\'}><summary data-faq="${i}">${s(\'v2.faq\'+i+\'Title\')}');
await patch('public/app.js',"const storyFocus=active?.hasAttribute('data-demo')?", "const storyFocus=active?.hasAttribute('data-faq')?'[data-faq=\"'+active.dataset.faq+'\"]':active?.hasAttribute('data-demo')?");
