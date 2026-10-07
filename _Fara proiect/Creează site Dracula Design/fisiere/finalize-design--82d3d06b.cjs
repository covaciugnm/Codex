const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'../outputs/dracula-design-office');
let p=path.join(root,'backend/public/shop.js'),s=fs.readFileSync(p,'utf8');
s=s.replace("['all','business','everyday','women'].map(f=>", "['all',...state.data.categories.map(c=>c.code)].map(f=>");
s=s.replace("${t('collection.'+f)}</button>","${f==='all'?t('collection.all'):esc(state.data.categories.find(c=>c.code===f)?.name)}</button>");
s=s.replace("+' — Dracula Design Office'","+' — '+state.data.brand.name");fs.writeFileSync(p,s);
p=path.join(root,'backend/dracula-content.json');const c=JSON.parse(fs.readFileSync(p));
const keys={'nav.inquiries':['Solicitări','Inquiries','Anfragen'],'inquiries.error':['Solicitarea nu a putut fi încărcată sau salvată.','Could not load or save the request.','Anfrage konnte nicht geladen oder gespeichert werden.'],'inquiries.empty':['Nu există solicitări.','No inquiries yet.','Noch keine Anfragen.'],'inquiries.status':['Stare','Status','Status'],'inquiries.new':['Nouă','New','Neu'],'inquiries.in_progress':['În lucru','In progress','In Bearbeitung'],'inquiries.closed':['Închisă','Closed','Geschlossen'],'inquiries.contact':['Contact','Contact','Kontakt'],'inquiries.complaint':['Reclamație','Complaint','Beschwerde'],'inquiries.withdrawal':['Retragere','Withdrawal','Widerruf'],'inquiries.privacy':['Date personale','Personal data','Personenbezogene Daten']};
for(const [key,values] of Object.entries(keys))c.ui['admin.'+key]={ro:values[0],en:values[1],de:values[2]};fs.writeFileSync(p,JSON.stringify(c,null,2));
