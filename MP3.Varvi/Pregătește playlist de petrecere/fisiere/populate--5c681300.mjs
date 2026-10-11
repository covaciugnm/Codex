import fs from 'node:fs/promises';
import {Workbook, SpreadsheetFile, FileBlob} from '@oai/artifact-tool';
const dir='D:/MP3.Varvi/outputs/party_20261008';
const rows=JSON.parse(await fs.readFile(dir+'/final_tracks.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(dir+'/Model_playlist_masa_si_petrecere.xlsx'));
const sum=wb.worksheets.getItem('Sinteză');
sum.getRange('A4').values=[['Selecție pentru masă și petrecere. Țintă: 20–24 de ore, împărțite pe stiluri.']];
sum.getRange('A5').values=[['Linkurile YouTube trimit direct la videoclipuri. Folosește filtrele pentru a alege piesele.']];
sum.getRange('A22').values=[['Versiuni și utilizare']];
sum.getRange('A23').values=[['Albumul și anul indică ediția din catalog; reeditările pot avea un an mai recent decât melodia.']];
sum.getRange('A24').values=[['Durata este cea a înregistrării din catalog. Videoclipul poate include intro sau o versiune mai scurtă.']];
sum.getRange('A25').values=[['Sursele și precizările fiecărei piese se află în notele celulelor cu albumul.']];
sum.getRange('A26').values=[['La masă: jazz, soul și blues. Pentru dans: disco, pop, oldies, latino, apoi rock.']];
sum.getRange('A27').values=[['Duratele sunt fără reclame și pauze. Totalurile se recalculează pentru rândurile 8–57.']];
sum.getRange('A27').format.font={name:'Arial',size:11,color:'#637587'};
sum.getRange('D1:D27').format.columnWidth=50;
const cats=[...new Set(rows.map(r=>r.category))];
for(const name of cats){
 const sh=wb.worksheets.getItem(name),data=rows.filter(r=>r.category===name);
 sh.getRange('A5').values=[['Durata: mm:ss. Albumul și anul: ediția de referință. Click pe link pentru YouTube.']];
 const values=data.map(r=>[r.display_artist||r.artist,r.title,r.album,r.category,r.year,r.seconds/86400,r.youtube]);
 sh.getRange(`A8:G${7+data.length}`).values=values;
 sh.getRange(`A8:G${7+data.length}`).format.wrapText=true;
 sh.getRange(`A8:G${7+data.length}`).format.rowHeight=45;
 sh.getRange('G1:G57').format.columnWidth=57;
 sh.getRange(`G8:G${7+data.length}`).format.wrapText=false;
 sh.getRange(`F8:F${7+data.length}`).setNumberFormat('mm:ss');
 for(let i=0;i<data.length;i++){
  const r=data[i],addr=`C${i+8}`;
  sh.getRange(`G${i+8}`).values=[[r.youtube]];
  wb.notes.add({id:`${name}:${addr}`,target:{cell:{sheetName:name,sheetId:sh.sheetId,address:addr}},authorId:'',createdAt:'',body:{plainText:`Sursă album, an și durată: ${r.source}\n${r.note||''}\nYouTube: ${r.video_title||r.title}\nCanal: ${r.video_channel||''}\nLink identificat în rezultatele YouTube; redarea integrală nu a fost testată.`}});
  const maxLines=Math.max(Math.ceil(r.title.length/38),Math.ceil(r.album.length/35),Math.ceil((r.display_artist||r.artist).length/25));
  if(maxLines>2)sh.getRange(`A${i+8}:G${i+8}`).format.rowHeight=maxLines*17+8;
 }
}
wb.recalculate();
const totalSeconds=rows.reduce((s,r)=>s+r.seconds,0);
const calculated=sum.getRange('B19:C19').values[0];
if(calculated[0]!==rows.length || Math.abs(calculated[1]*86400-totalSeconds)>0.1)throw Error('Totals mismatch '+JSON.stringify(calculated));
if(totalSeconds<72000 || totalSeconds>86400)throw Error('Outside requested duration');
if(new Set(rows.map(r=>r.artist+'|'+r.title)).size!==rows.length)throw Error('Duplicate songs');
if(rows.some(r=>!r.album||!r.year||!r.seconds||!/^https:\/\/www.youtube.com\/watch\?v=/.test(r.youtube)))throw Error('Missing fields');
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Final formula check'})).ndjson);
console.log((await wb.inspect({kind:'table',range:"'Sinteză'!A7:D19",include:'values,formulas',tableMaxRows:13,tableMaxCols:4,maxChars:4000})).ndjson);
await fs.mkdir(dir+'/final_previews',{recursive:true});
for(const [i,name] of ['Sinteză',...cats].entries()){
 const im=await wb.render({sheetName:name,range:i===0?'A1:D28':'A1:G13',scale:1,format:'png'});
 await fs.writeFile(`${dir}/final_previews/sheet_${i}.png`,new Uint8Array(await im.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(dir+'/Playlist_masa_si_petrecere_COMPLET.xlsx');
console.log(JSON.stringify({songs:rows.length,seconds:totalSeconds,duration:`${Math.floor(totalSeconds/3600)}:${String(Math.floor(totalSeconds%3600/60)).padStart(2,'0')}:${String(totalSeconds%60).padStart(2,'0')}`}));
