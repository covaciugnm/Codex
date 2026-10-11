import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/MP3.Varvi/outputs/free_mp3_20261008';
const tracks=JSON.parse(await fs.readFile(dir+'/free_tracks.json','utf8'));
const cats=[...new Set(tracks.map(t=>t.category))];
const moments=['Masă și conversație','Soul și dans lejer','Dans și ritm funk','Petrecere pop','Pauze și dans lent','Blues de ascultat','Rock melodic și pop-rock','Dans retro și surf','Salsa, latino și world','Art rock românesc'];
const wb=Workbook.create(),summary=wb.worksheets.add('Sinteză');
const navy='#20364B',light='#EDF2F7',muted='#627487';
function base(sh,end,rows){
 sh.showGridLines=false;
 sh.getRange(`A1:${end}${rows}`).format={font:{name:'Arial',size:11,color:'#253547'},verticalAlignment:'center',rowHeight:24};
 sh.getRange(`A2:${end}2`).format.rowHeight=32;
 sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
 sh.getRange(`A2:${end}2`).format.borders={bottom:{style:'thin',color:'#C4CED8'}};
}
const linkMap=[];
for(const [i,cat] of cats.entries()){
 const data=tracks.filter(t=>t.category===cat),last=data.length+7;
 const sh=wb.worksheets.add(cat);base(sh,'I',last);
 for(const [c,w] of Object.entries({A:29,B:45,C:40,D:25,E:18,F:12,G:25,H:38,I:28}))sh.getRange(`${c}1:${c}${last}`).format.columnWidth=w;
 sh.getRange('A2').values=[[cat]];
 sh.getRange('A4').values=[['Număr melodii']];sh.getRange('B4').formulas=[[`=COUNTA(B8:B${last})`]];
 sh.getRange('E4').values=[['Durată totală']];sh.getRange('F4').formulas=[[`=SUM(F8:F${last})`]];sh.getRange('F4').setNumberFormat('[h]:mm:ss');
 sh.getRange('A5').values=[['Click pe linkul din G. Coloana H arată condiția de acces; sursele și licența sunt în nota albumului.']];
 sh.getRange('A5').format.font={name:'Arial',size:11,italic:true,color:muted};
 sh.getRange('A7:I7').values=[['Nume artist','Nume melodie','Nume album','Stil','Anul publicării','Durată','Link descărcare','Acces gratuit','Platformă']];
 const values=data.map(r=>[r.artist,r.title,r.album==='Unnamed album'?'Single / album neprecizat':r.album,r.category,r.year,r.seconds/86400,r.source.startsWith('Jamendo')?'Descarcă MP3':r.source.startsWith('Bandcamp')?'Deschide albumul':'Descarcă de pe FMA',r.access,r.source]);
 sh.getRange(`A8:I${last}`).values=values;
 const table=sh.tables.add(`A7:I${last}`,true,`FreeMusic_${i+1}`);table.style='TableStyleMedium2';table.showFilterButton=true;
 sh.getRange('A7:I7').format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',rowHeight:30};
 sh.getRange(`A8:I${last}`).format.wrapText=true;
 sh.getRange(`A8:I${last}`).format.rowHeight=48;
 sh.getRange(`G8:G${last}`).format.font={name:'Arial',size:11,color:'#1763AA'};
 sh.getRange(`E8:F${last}`).format.horizontalAlignment='right';
 sh.getRange(`E8:E${last}`).setNumberFormat('0');sh.getRange(`F8:F${last}`).setNumberFormat('mm:ss');
 for(const [j,r] of data.entries()){
  let lines=Math.max(Math.ceil(r.artist.length/25),Math.ceil(r.title.length/39),Math.ceil(r.album.length/34),Math.ceil(r.access.length/32));
  if(lines>=3)sh.getRange(`A${j+8}:I${j+8}`).format.rowHeight=lines*17+9;
  let note=`Pagina piesei / albumului: ${r.page}\n${r.origin?'Origine: '+r.origin+'\n':''}Licență: ${r.license}\n${r.license_url}\nEtichete ale sursei: ${r.genres}\n${r.checked||'Oferta albumului la preț minim zero verificată'}\nVerificat: 8 octombrie 2026. Selecție pe baza metadatelor, fără audiție integrală.`;
  wb.notes.add({id:`source_${i}_${j}`,target:{cell:{sheetName:cat,sheetId:sh.sheetId,address:`C${j+8}`}},authorId:'',createdAt:'',body:{plainText:note}});
  linkMap.push({sheet:i+2,cell:`G${j+8}`,url:r.download});
 }
 sh.freezePanes.freezeRows(7);
}
base(summary,'H',32);summary.tabColor=navy;
for(const [c,w] of Object.entries({A:30,B:14,C:18,D:36,E:3,F:36,G:14,H:19}))summary.getRange(`${c}1:${c}32`).format.columnWidth=w;
summary.getRange('A2').values=[['Muzică gratuită pentru masă și petrecere']];
summary.getRange('A4').values=[['Selecție nouă de 24 de ore, cu MP3 directe și descărcări oferite gratuit de platforme.']];
summary.getRange('A5').values=[['Artiști independenți și înregistrări live. Duratele nu includ pauze. Verificat la 8 octombrie 2026.']];
summary.getRange('A4:A5').format.font={name:'Arial',size:11,color:muted};
summary.getRange('A7:D7').values=[['Stil / tab','Melodii','Durată totală','Moment potrivit']];
summary.getRange('F7:H7').values=[['Tip de acces','Melodii','Durată totală']];
for(const a of ['A7:D7','F7:H7'])summary.getRange(a).format={fill:navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',rowHeight:30};
for(const [i,c] of cats.entries()){
 const r=i+8,q=c.replaceAll("'","''");summary.getRange(`A${r}:D${r}`).values=[[c,null,null,moments[i]]];
 summary.getRange(`B${r}:C${r}`).formulas=[[`='${q}'!B4`,`='${q}'!F4`]];
 if(i%2===0)summary.getRange(`A${r}:D${r}`).format.fill=light;
}
const sources=['Jamendo / Internet Archive','Free Music Archive','Bandcamp — pagina artistului'];
for(let i=0;i<3;i++){
 const row=i+8;summary.getRange(`F${row}`).values=[[["MP3 direct, fără cont","FMA, cont gratuit","Bandcamp, preț zero + e-mail"][i]]];
 const parts=cats.map(c=>{const q=c.replaceAll("'","''"),last=tracks.filter(r=>r.category===c).length+7;return {range:`'${q}'!I8:I${last}`,dur:`'${q}'!F8:F${last}`}});
 summary.getRange(`G${row}`).formulas=[['='+parts.map(p=>`COUNTIFS(${p.range},"${sources[i]}")`).join('+')]];
 summary.getRange(`H${row}`).formulas=[['='+parts.map(p=>`SUMIFS(${p.dur},${p.range},"${sources[i]}")`).join('+')]];
}
summary.getRange('A19').values=[['TOTAL']];summary.getRange('B19:C19').formulas=[['=SUM(B8:B17)','=SUM(C8:C17)']];
summary.getRange('A19:D19').format={fill:'#DEE7EF',font:{name:'Arial',size:11,bold:true,color:navy},rowHeight:30};
summary.getRange('B8:B19').setNumberFormat('0');summary.getRange('C8:C19').setNumberFormat('[h]:mm:ss');
summary.getRange('G8:G10').setNumberFormat('0');summary.getRange('H8:H10').setNumberFormat('[h]:mm:ss');
summary.getRange('A22').values=[['Cum folosești lista']];summary.getRange('A22').format.font={name:'Arial',size:11,bold:true,color:navy};
const notes=[
 'Descărcările directe se deschid din coloana G. FMA cere autentificare într-un cont gratuit.',
 'Pe Bandcamp, alege Buy Digital Album, introdu 0 și urmează pașii. Este cerută o adresă de e-mail.',
 'Tabul Românești conține byron, artist român cu versuri în engleză, din două albume oferite gratuit.',
 'Stilurile sunt apropiate de cererea inițială; repertoriul include pop-rock, acustic și retro independent.',
 'Anul este cel publicat de sursă pentru această ediție. Duratele sunt rotunjite la secunde.',
 'Licențele diferă de la piesă la piesă și sunt păstrate în notele albumelor.',
 'MP3 Varvi acceptă momentan numai YouTube. Acest fișier se folosește pentru descărcare de pe site-urile indicate.'
];
notes.forEach((n,i)=>{summary.getRange(`A${23+i}`).values=[[n]];summary.getRange(`A${23+i}`).format.font={name:'Arial',size:11,color:muted};});
wb.recalculate();
const expected=tracks.reduce((s,r)=>s+r.seconds,0),total=summary.getRange('B19:C19').values[0];
if(total[0]!==tracks.length||Math.abs(total[1]*86400-expected)>.1||expected!==86400)throw Error('Total mismatch');
if(new Set(tracks.map(t=>t.id)).size!==tracks.length)throw Error('Duplicate record');
if(tracks.some(t=>!t.artist||!t.title||!t.album||!t.year||!t.download))throw Error('Incomplete record');
if(tracks.some(t=>t.source.startsWith('Jamendo')&&![200,206].includes(t.http_status)))throw Error('Unverified MP3');
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Formula errors'})).ndjson);
console.log((await wb.inspect({kind:'table',range:"'Sinteză'!F7:H10",include:'values,formulas',tableMaxRows:4,maxChars:1700})).ndjson);
await fs.mkdir(dir+'/previews',{recursive:true});
for(const [i,c] of ['Sinteză',...cats].entries()){
 const b=await wb.render({sheetName:c,range:i===0?'A1:H30':'A1:I12',scale:1,format:'png'});
 await fs.writeFile(`${dir}/previews/free_${i}.png`,new Uint8Array(await b.arrayBuffer()));
}
await fs.writeFile(dir+'/hyperlinks.json',JSON.stringify(linkMap));
await (await SpreadsheetFile.exportXlsx(wb)).save(dir+'/Playlist_MP3_gratuite_24_ore.xlsx');
console.log(JSON.stringify({tracks:tracks.length,seconds:expected,artists:new Set(tracks.map(r=>r.artist)).size}));
