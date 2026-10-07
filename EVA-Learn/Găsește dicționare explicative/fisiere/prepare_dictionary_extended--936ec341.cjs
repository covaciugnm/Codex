const fs=require('fs'),os=require('os'),path=require('path');
const base=os.tmpdir();
const data=JSON.parse(fs.readFileSync(path.join(base,'dictionary_data_extended.json'),'utf8'));
const versions=JSON.parse(fs.readFileSync(path.join(base,'dictionary_freedict_versions.json'),'utf8'));
const checks=JSON.parse(fs.readFileSync(path.join(base,'dictionary_archive_checks.json'),'utf8'));
const latest={'eng-deu':'1.9-fd1','deu-eng':'1.9-fd1','eng-fra':'0.1.6','fra-eng':'0.4.1','eng-spa':'2025.11.23','spa-eng':'0.3.1','deu-fra':'2025.11.23','fra-deu':'2025.11.23','deu-spa':'2025.11.23','spa-deu':'0.1','fra-spa':'2025.11.23','spa-fra':'2025.11.23'};
const languages={eng:['Engleză','EN'],deu:['Germană','DE'],fra:['Franceză','FR'],spa:['Spaniolă','ES']};
const valid=versions.filter(v=>v.status===200&&v.links.length);
const format=url=>url.includes('.stardict.')?'StarDict — arhivă '+url.split('.').slice(-2).join('.'):url.includes('.dictd.')?'Dictd — arhivă '+url.split('.').slice(-2).join('.'):url.includes('.src.')?'Surse XML/TEI — arhivă '+url.split('.').slice(-2).join('.'):url.endsWith('.zip')?'ZIP; structură internă de verificat':url.endsWith('.tar.gz')?'TAR.GZ; structură internă de verificat':'Arhivă; structură internă de verificat';
let currentUpdated=0,olderAdded=0;
for(const v of valid){
 const [from,to]=v.pair.split('-'),a=languages[from],b=languages[to];
 if(v.version===latest[v.pair]){
  const row=data.all.find(r=>r[7]==='FreeDict'&&r[3]===a[1]&&r[5]===b[1]);
  if(!row)throw Error('Lipsește rândul curent '+v.pair);
  row[10]=v.url;row[8]=format(v.url);row[20]=v.version;row[21]=v.page;
  row[17]+=' Alte formate ale aceleiași versiuni sunt în foaia Formate FreeDict.';
  row[18]='Directorul versiunii HTTP 200; fișierul este listat în catalogul oficial.';
  row[22]='Director verificat HTTP 200; fără test individual al fișierului.';
  currentUpdated++;
 }else{
  data.all.push([0,'Versiuni FreeDict',a[0],a[1],b[0],b[1],'Traducere','FreeDict — '+v.version+' ('+v.pair+')',format(v.url),'Gratuit',v.url,'Descarcă arhiva; deschide cu un cititor compatibil StarDict / Dictd sau prelucrează sursele. Formatele alternative sunt în foaia Formate FreeDict.','Fără rating independent verificat pentru această ediție.','F','https://freedict.org/','Dicționar liber; licența exactă diferă între perechi și versiuni. Consultă COPYING / README / antetul TEI din arhivă.','','Ediție arhivată. Poate avea vocabular mai redus și erori corectate în edițiile ulterioare. Formatul intern al pachetelor vechi fără marcaj StarDict / Dictd / src nu a fost inspectat.','Director verificat HTTP 200; fișierele sunt listate în depozitul oficial.','2026-10-01',v.version,v.page,'Director verificat HTTP 200; fără test individual al fișierului.','Da']);
  olderAdded++;
 }
}
const norm=u=>String(u||'').split('?')[0];
const checkMap=new Map(checks.map(c=>[norm(c.url),c]));
const checkedText=c=>{
 if((c.status===200||c.status===206)&&c.first&&!String(c.type).includes('text/html'))return 'Început de fișier transmis; HTTP '+c.status+'. Tip / semnătură verificate; fără verificare integrală.';
 if(c.status===429)return 'Catalog verificat; acces automat limitat HTTP 429. Încearcă manual pagina sursei → Original file.';
 if(c.status===403)return 'Acces refuzat HTTP 403; descărcare neconfirmată.';
 return 'Descărcare automată neconfirmată: '+(c.error||c.status||'timeout')+'. Folosește pagina sursei.';
};
data.all.forEach((r,i)=>{r[0]=i+1;const c=checkMap.get(norm(r[10]));if(c){r[22]=checkedText(c);if(c.status===200||c.status===206)r[18]='Începutul fișierului și tipul de conținut verificate; fără descărcare integrală / instalare.';}});
data.formatRows=valid.flatMap(v=>{const [from,to]=v.pair.split('-');return v.links.map(url=>[languages[from][0],languages[to][0],languages[from][1]+'→'+languages[to][1],v.version,format(url),url,v.page,checkMap.has(norm(url))?checkedText(checkMap.get(norm(url))):'Fișier listat; director HTTP 200; fără test individual.']);});
data.checkRows=checks.map(c=>[c.url,c.status||'Timeout / eroare',c.type||'',checkedText(c),'2026-10-01']);
data.freeCount=data.all.filter(r=>r[9].startsWith('Gratuit')).length;
data.newCount=data.all.filter(r=>r[23]==='Da').length;
data.expectedTotal=data.all.length;
const successes=checks.filter(c=>(c.status===200||c.status===206)&&c.first&&!String(c.type).includes('text/html')).length;
data.guide=data.guide.map(r=>r[0]==='Verificare efectuată'?[r[0],'Pagini, cataloage și directoare de descărcare verificate. Pentru '+successes+' linkuri a fost confirmat începutul fișierului; nu au fost toate descărcate integral sau instalate. Nu s-au efectuat cumpărări.']:r);
data.guide.push(['Total actual',data.all.length+' înregistrări în Catalog complet, dintre care '+data.freeCount+' gratuite și '+(data.all.length-data.freeCount)+' cu taxă din cercetarea inițială. '+data.newCount+' înregistrări noi gratuite; '+olderAdded+' sunt versiuni oficiale FreeDict mai vechi.']);
data.guide.push(['Toate formatele FreeDict',data.formatRows.length+' fișiere concrete listate în foaia Formate FreeDict pentru 102 versiuni oficiale. Sunt alternative de format ale acelorași dicționare, fără a fi numărate încă o dată în totalul catalogului.']);
data.guide.push(['Structura Excel','15 foi: Gratuite, Noutati gratuite, Ghid si note, Catalog complet, Traduceri, Versiuni FreeDict, Formate FreeDict, Explicative, Definitii multilingve, Carti PDF si EPUB, Date lexicale, Recenzii, Licente, Verificari linkuri și Neconfirmate.']);
data.guide.push(['Drepturi pentru colecția gratuită','Foaia Gratuite include surse gratuite pentru uz personal și resurse cu licențe libere. Pentru redistribuire, editare sau integrare într-un produs se aplică condițiile din fiecare rând; nu toate pachetele au aceeași licență.']);
if(currentUpdated!==12||olderAdded!==90||data.all.length!==257||data.all.some(r=>r.length!==24))throw Error('Numărul de înregistrări / coloane nu corespunde.');
fs.writeFileSync(path.join(base,'dictionary_data_extended.json'),JSON.stringify(data,null,2),'utf8');
console.log(JSON.stringify({entries:data.all.length,free:data.freeCount,newFree:data.newCount,olderFreeDict:olderAdded,currentUpdated,formatLinks:data.formatRows.length,testedLinks:checks.length,confirmedFiles:successes},null,2));
require('child_process').execFileSync(process.execPath,[path.join(base,'build_dictionary_extended.cjs')],{stdio:'inherit'});
