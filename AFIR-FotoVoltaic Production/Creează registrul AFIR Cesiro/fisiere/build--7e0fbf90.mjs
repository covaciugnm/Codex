import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const d=JSON.parse(await fs.readFile(new URL('./data.json',import.meta.url),'utf8'));
const wb=Workbook.create();
const specs=[
['Registru AFIR',d.main,['ID','Document / eveniment','Emitent','Nr. Cesiro','Data Cesiro','Nr. AFIR','Data AFIR','Cod contract / alt emitent','Data comunicării / depunerii','Stare / dovadă','Sursă','Observații'],[75,360,140,130,110,180,110,230,120,350,430,470],[4,6,8]],
['Documente',d.documents,['ID fișier','Document / versiune','Etapă','Nr. Cesiro','Data Cesiro','Nr. AFIR','Data AFIR','Alt nr. din antet; emitent de verificat','Starea transmiterii','Numere și referințe din text, de verificat în context','Citire / limite','Sursă locală'],[75,380,180,130,110,160,110,220,320,720,330,500],[4,6]],
['Emailuri',d.emails,['ID','Data email UTC','Sens','Relație','Subiect','Expeditor','Destinatari','CC','Atașamente','Extras corp email','Cont','ID EVA','Sursă text email','Observații'],[75,160,100,160,420,250,320,300,100,800,250,300,420,350],[1]],
['Atasamente email',d.attachments,['ID atașament','ID email','Nume atașament','Dimensiune octeți','ID EVA atașament','Disponibilitate','Sursă text extras','Amprentă text (nu fișier original)'],[120,90,480,140,300,270,450,450],[]],
['Inventar local',d.inventory,['ID','Nume fișier','Dosar','Încadrare','Format','Dimensiune octeți','Citire','Stare','Copie identică a ID','Sursă locală'],[80,420,320,330,90,150,320,420,130,650],[]],
['Continut arhive',d.archives,['Arhiva ZIP','Document în arhivă','Dimensiune octeți'],[600,800,160],[]]
];
const guide=wb.worksheets.add('Sinteza');guide.showGridLines=false;
guide.getRange('A2').values=[['CESIRO PRODUCTION · Registru documente și corespondență AFIR']];
guide.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:'#17365D'};
guide.getRange('A4:B8').values=[['Actualizat la','16.10.2026'],['Proiect','FMSES011011372801030'],['Contract','CFMSES011011372801030 / 30.12.2024'],['Dosar rambursare','RFMSES011011372801030.1'],['Investiție','Sistem fotovoltaic 1 MW pentru autoconsum – fabrica de prelucrare nuci, alune, pistacio și migdale']];
guide.getRange('A10:B16').values=[['Conținut','Înregistrări'],['Evenimente / documente AFIR',d.main.length],['Documente locale și versiuni fără copii identice',d.documents.length],['Emailuri păstrate',d.emails.length],['Atașamente asociate emailurilor',d.attachments.length],['Fișiere inventariate',d.inventory.length],['Fișiere în arhive ZIP',d.archives.length]];
guide.getRange('A18:B25').values=[['Citirea registrului','Regulă'],['Numere proprii și AFIR','Coloane separate. FN = fără număr. Câmp gol = număr/data neidentificate sau neaplicabile; nu înseamnă că nu există.'],['Data comunicării','Separată de data documentului și de înregistrare. Emailurile păstrează UTC, exact cum sunt returnate de EVA.'],['Depunere confirmată','Numai când există confirmare în email sau document AFIR. Denumirile dosarelor sunt păstrate ca indicii distincte.'],['Copii și versiuni','Inventarul păstrează toate fișierele. Copiile PDF/DOCX/TXT identice sunt asociate prin SHA-256; versiunile diferite rămân distincte.'],['Numere din text','În Documente, coloana de referințe include și numere citate; nu toate sunt numărul documentului curent. Registru AFIR conține perechile verificate.'],['Emailuri și atașamente','Sursele text sunt copii pentru consultare, nu fișiere EML/MIME și nu înlocuiesc originalele semnate. Atașamentele cu text identic pot avea ID-uri distincte.'],['Acoperire','Dosarul local și emailurile accesibile prin EVA. Nu a fost consultată direct platforma AFIR. Mesajele nesincronizate și documentele care lipsesc din surse pot lipsi din registru.']];
guide.getRange('A27:B32').values=[['De completat / verificat','Detaliu'],['Răspuns la 961/15.10.2026','Documentele locale indică proiect netransmis; număr intern de completat.'],['AA2 primit 09.10.2026','Nr. AFIR 1379871; data din antet este necompletată. Dovada semnării bilaterale și retransmiterii rămâne de verificat.'],['Dovezi platformă','Recipise, numere de încărcare și date pentru depunerile care sunt documentate doar prin numele dosarului.'],['Scanuri / formulare XFA','Documentele cu text insuficient sunt marcate. Numerele nu au fost inventate din numele fișierelor.'],['Alte proiecte','Mesajele AFIR despre Marius Code WNK și proiectul Parchetului Alba au fost excluse. Inventarul local marchează separat dosarele conexe.']];
guide.getRange('A34:B34').values=[['Sincronizare email','production@cesiro.ro: ultima sincronizare raportată 16.09.2026. Conturile cosmin.covaciu@cesiro.com / .ro: 16.10.2026. Corespondența recentă din contul production poate lipsi.']];
guide.getRange('A34:B34').format={font:{name:'Arial',size:11,color:'#8A4B08'},wrapText:true,rowHeight:44};
guide.getRange('A4:A32').format.columnWidthPx=300;guide.getRange('B4:B32').format.columnWidthPx=870;
guide.getRange('A4:B32').format.font={name:'Arial',size:11,color:'#243746'};guide.getRange('A4:B32').format.wrapText=true;guide.getRange('A4:B32').format.rowHeight=38;
for(const r of [10,18,27])guide.getRange(`A${r}:B${r}`).format={fill:'#17365D',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'}};
const safe=v=>typeof v==='string'&&/^[=+@]/.test(v)?"'"+v:v;
const dateValue=v=>{let m=String(v).match(/^(\d{1,2})\s*\.\s*(\d{1,2})\s*\.\s*(\d{4})$/);return m?new Date(Date.UTC(+m[3],+m[2]-1,+m[1])):new Date(v)};
for(const [name,rows,headers,widths,dates] of specs){
 const s=wb.worksheets.add(name);s.showGridLines=false;s.tabColor='#426A8D';
 s.getRange('A2').values=[[name+' · Cesiro Production']];s.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:'#17365D'};
 const vals=rows.map(r=>r.map((v,j)=>{if(dates.includes(j)&&v){let dt=dateValue(v);if(!isNaN(dt))return dt.getTime()/86400000+25569;}return safe(v??'')}));
 s.getRangeByIndexes(3,0,1,headers.length).values=[headers];
 if(vals.length)s.getRangeByIndexes(4,0,vals.length,headers.length).values=vals;
 const all=s.getRangeByIndexes(3,0,rows.length+1,headers.length);all.format.font={name:'Arial',size:11,color:'#243746'};all.format.wrapText=true;all.format.verticalAlignment='top';
 widths.forEach((w,j)=>s.getRangeByIndexes(3,j,rows.length+1,1).format.columnWidthPx=w);
 s.getRangeByIndexes(3,0,1,headers.length).format={fill:'#17365D',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:45,wrapText:true};
 if(rows.length){const table=s.tables.add(`A4:${String.fromCharCode(64+headers.length)}${rows.length+4}`,true,'T'+name.replace(/\W/g,''));table.style='TableStyleMedium2';}
 for(let i=0;i<rows.length;i++){
  let lines=Math.max(...rows[i].map((v,j)=>String(v??'').split('\n').reduce((sum,l)=>sum+Math.max(1,Math.ceil(l.length/(widths[j]/6.3))),0)));
  s.getRangeByIndexes(i+4,0,1,headers.length).format.rowHeight=Math.min(400,Math.max(32,lines*14+8));
 }
 dates.forEach(j=>s.getRangeByIndexes(4,j,Math.max(1,rows.length),1).setNumberFormat(name==='Emailuri'?'dd.mm.yyyy hh:mm':'dd.mm.yyyy'));
 if(name==='Registru AFIR'||name==='Documente')for(const j of [3,5])s.getRangeByIndexes(4,j,Math.max(1,rows.length),1).setNumberFormat('@');
 const sourceCol=headers.findIndex(h=>h==='Sursă'||h==='Sursă locală'||h==='Sursă text email'||h==='Sursă text extras');
 if(sourceCol>=0)rows.forEach((r,i)=>{let p=r[sourceCol];if(p&&/^[A-Z]:/i.test(p))s.getCell(i+4,sourceCol).formulas=[[`=HYPERLINK("file:///${p.replace(/\\/g,'/').replace(/"/g,'""')}","Deschide sursa")`]]});
 s.freezePanes.freezeRows(4);s.freezePanes.freezeColumns(2);
}
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Registru AFIR'!A5:J10",include:'values',tableMaxRows:6,tableMaxCols:10})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10}})).ndjson);
for(const name of ['Sinteza',...specs.map(s=>s[0])]){try{const blob=await wb.render({sheetName:name,range:name==='Sinteza'?'A2:B16':(name==='Continut arhive'?'A4:C7':'A4:F7'),scale:1,format:'png'});await fs.writeFile(new URL('./preview-'+name.replace(/ /g,'_')+'.png',import.meta.url),new Uint8Array(await blob.arrayBuffer()));}catch(e){console.log('RENDER '+name+': '+e.message);}}
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(d.out+'/Registru_AFIR_Cesiro_Production_16.10.2026.xlsx');
console.log('SAVED '+d.out+'/Registru_AFIR_Cesiro_Production_16.10.2026.xlsx');
