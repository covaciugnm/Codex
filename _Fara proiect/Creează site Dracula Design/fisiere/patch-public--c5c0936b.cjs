const fs=require('fs');const root='outputs/dracula-design-office/';let p=root+'backend/public/shop.js',s=fs.readFileSync(p,'utf8');
const helper=`
function rich(value){
 if(!/<\\/?[a-z][^>]*>/i.test(value||''))return esc(value).split(/\\n\\n/).map(v=>'<p>'+v.replace(/\\n/g,'<br>')+'</p>').join('');
 const doc=new DOMParser().parseFromString(value,'text/html');
 const tags=new Set(['P','BR','STRONG','EM','B','I','UL','OL','LI','H2','H3','H4','BLOCKQUOTE','A']);
 function clean(node){if(node.nodeType===3)return esc(node.textContent);if(node.nodeType!==1)return '';if(['SCRIPT','STYLE','IFRAME','OBJECT'].includes(node.tagName))return '';const body=[...node.childNodes].map(clean).join('');if(!tags.has(node.tagName))return body;const tag=node.tagName.toLowerCase();let attr='';if(tag==='a'){const target=node.getAttribute('href')||'';if(/^(https?:\\/\\/|mailto:|\\/(?!\\/))/.test(target))attr=' href="'+esc(target)+'" rel="noopener noreferrer"';}return '<'+tag+attr+'>'+body+(tag==='br'?'':'</'+tag+'>');}
 return [...doc.body.childNodes].map(clean).join('');
}
`;
s=s.replace('function legal(slug)',helper+'\nfunction legal(slug)');s=s.replace("${esc(p.body).split(/\\n\\n/).map(v=>'<p>'+v.replace(/\\n/g,'<br>')+'</p>').join('')}","${rich(p.body)}");
s=s.replace('<p>${esc(p.details)}</p>','<div>${rich(p.details)}</div>');
fs.writeFileSync(p,s);
p=root+'frontend/src/features/settings/SettingsPage.tsx';s=fs.readFileSync(p,'utf8').replace('label="Cod limbă nouă (fr, it, es, pt-BR)"',"label={t('settings.new_language')}").replace('>Adaugă limba</button>',">{t('settings.add_language')}</button>");fs.writeFileSync(p,s);
p=root+'backend/dracula-content.json';const c=JSON.parse(fs.readFileSync(p));c.ui['admin.settings.new_language']={ro:'Cod limbă nouă (fr, it, es, pt-BR)',en:'New language code (fr, it, es, pt-BR)',de:'Neuer Sprachcode (fr, it, es, pt-BR)'};c.ui['admin.settings.add_language']={ro:'Adaugă limba',en:'Add language',de:'Sprache hinzufügen'};fs.writeFileSync(p,JSON.stringify(c,null,2));
