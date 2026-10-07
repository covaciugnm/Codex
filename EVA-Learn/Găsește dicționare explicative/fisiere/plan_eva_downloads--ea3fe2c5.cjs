const fs=require('fs'),p=require('path'),crypto=require('crypto'),{Readable}=require('stream'),{pipeline}=require('stream/promises');
const visual=__dirname,root='\\\\192.168.100.169\\Comun\\00.Roboti\\EVA.Pro\\Learn',out=p.join(root,'EVA_LEARN_DB_35');
fs.mkdirSync(out,{recursive:true});
const groups=[
['ro','Romana',['ro']],['en','Engleza',['en']],['de','Germana',['de']],['fr','Franceza',['fr']],['es','Spaniola',['es']],
['bn','Bengali',['bn']],['ur','Urdu',['ur']],['yue','Cantoneza',['yue']],['ha','Hausa',['ha']],['mr','Marathi',['mr']],['te','Telugu',['te']],['wuu','Wu_Shanghai',['wuu']],['ta','Tamil',['ta']],['fa','Persana',['fa']],['arab_dialect','Araba_dialectala',['arz','ary']],['vi','Vietnameza',['vi']],['kn','Kannada',['kn']],['gu','Gujarati',['gu']],['am','Amharica',['am']],['my','Birmana',['my']],['berber','Berbera_Tamazight',['tzm','rif','shi','kab']],['ml','Malayalam',['ml']],['or','Odia',['or']],['apd','Araba_sudaneza',['apd']],['pnb','Punjabi_Shahmukhi',['pnb']],['uz','Uzbeka',['uz']],['ig','Igbo',['ig']],['yo','Yoruba',['yo']],['th','Thailandeza',['th']],['ne','Nepaleza',['ne']],['nan','Taiwaneza_Hokkien',['nan']],['kk','Kazaha',['kk']],['si','Sinhaleza',['si']],['km','Khmera',['km']],['az','Azera',['az','azb','azj']]
].map((a,i)=>({code:a[0],name:a[1],codes:a[2],folder:String(i+1).padStart(2,'0')+'_'+a[1]}));
const map=new Map(groups.flatMap(g=>g.codes.map(c=>[c,g])));
for(const g of groups)for(const sub of ['01_Originale','02_Excel_DB','03_TTS','04_STT','05_Licente'])fs.mkdirSync(p.join(out,g.folder,sub),{recursive:true});
fs.mkdirSync(p.join(out,'00_Administrare'),{recursive:true});fs.mkdirSync(p.join(out,'00_Modele_comune'),{recursive:true});
fs.writeFileSync(p.join(out,'00_Administrare','limbi.json'),JSON.stringify(groups,null,2),'utf8');
const cat=JSON.parse(fs.readFileSync(p.join(visual,'catalogue_source.json'),'utf8'));
const rows=cat.find(s=>s.name==='Dictionare').rows.filter(r=>map.has(r[2])&&map.has(r[4]));
const jobs=new Map(),notDirect=[];
const filePattern=/\.(zip|gz|bz2|xz|pdf|txt|tsv|csv|json|jsonl|xml|tei|xlsx|djvu|7z|slob|tar|dict|idx|ifo)(\?|$)/i;
for(const r of rows){
 const g=map.get(r[2]),url=r[8];if(!filePattern.test(url)||!/^https?:/.test(url)){notDirect.push({id:r[0],group:g.folder,reason:'Pagina / formular / export manual; nu este un fișier direct',row:r});continue;}
 let job=jobs.get(url);
 if(!job){let file;try{file=decodeURIComponent(new URL(url).pathname.split('/').pop());}catch{file='download';}file=file.replace(/[<>:"/\\|?*\x00-\x1f]/g,'_').slice(-150);
 const hash=crypto.createHash('sha256').update(url).digest('hex').slice(0,12);
 job={id:hash,url,kind:'dictionary',path:p.join(g.folder,'01_Originale',hash+'_'+file),groups:[],rows:[],status:'pending'};jobs.set(url,job);}
 job.rows.push(r);if(!job.groups.includes(g.folder))job.groups.push(g.folder);
}
const extra=JSON.parse(fs.readFileSync('C:/Users/User/AppData/Local/Temp/dictionary_data_extended.json','utf8')).all;
for(const r of extra.filter(r=>r[9].startsWith('Gratuit')&&filePattern.test(r[10])&&map.has(r[3].toLowerCase())&&map.has(r[5].toLowerCase()))){
 if(jobs.has(r[10]))continue;
 const g=map.get(r[3].toLowerCase()),url=r[10],hash=crypto.createHash('sha256').update(url).digest('hex').slice(0,12),file=decodeURIComponent(new URL(url).pathname.split('/').pop()).replace(/[<>:"/\\|?*\x00-\x1f]/g,'_');
 jobs.set(url,{id:hash,url,kind:'dictionary',path:p.join(g.folder,'01_Originale',hash+'_'+file),groups:[g.folder],rows:[[r[0],r[2],r[3].toLowerCase(),r[4],r[5].toLowerCase(),r[7],r[6],r[8],url,r[21],r[9],r[15],r[16],r[20],r[12],r[14],'',r[17],r[18],'',r[15],'','']],status:'pending'});
}
const planFile=p.join(out,'00_Administrare','downloads_dictionary.json');
fs.writeFileSync(planFile,JSON.stringify([...jobs.values()],null,2),'utf8');
fs.writeFileSync(p.join(out,'00_Administrare','export_manual.json'),JSON.stringify(notDirect,null,2),'utf8');
console.log(JSON.stringify({groups:groups.length,rows:rows.length,downloadJobs:jobs.size,manual:notDirect.length}));
