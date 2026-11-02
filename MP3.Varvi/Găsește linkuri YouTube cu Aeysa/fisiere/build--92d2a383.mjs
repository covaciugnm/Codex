import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out='D:/MP3.Varvi/outputs/aeysa_20261023';
const rows=JSON.parse(await fs.readFile(out+'/records.json','utf8'));
const wb=Workbook.create();
for(const [name,kind] of [['Piese integrale','Piesă integrală'],['Clipuri scurte','Clip scurt'],['Live radio','Live / radio']]){
 const data=rows.filter(r=>r.kind===kind);
 const sh=wb.worksheets.add(name); sh.showGridLines=false;
 sh.getRange('A2').values=[['AEYSA — '+name]];
 sh.getRange('A3').values=[[`${data.length} linkuri • Catalog oficial consultat la 23.10.2026`]];
 sh.getRange('A4').values=[['Sursa: https://aeysa.com/videos/all/']];
 sh.getRange('A5').values=[[kind==='Live / radio'?'Transmisie continuă; verificați starea înainte de descărcare.':'Linkuri din catalog; redarea pe YouTube nu a fost verificată individual.']];
 sh.getRange('A7:F7').values=[['Nr.','Titlu','Durată','Link YouTube','Publicat','Pagina sursă']];
 sh.getRange(`A8:F${7+data.length}`).values=data.map((r,i)=>[i+1,r.title,r.duration,r.url,r.date?(Date.parse(r.date+'T00:00:00Z')/86400000+25569):null,r.source]);
 sh.getRange(`A1:F${7+data.length}`).format.font={name:'Arial',size:11,color:'#1E293B'};
 sh.getRange('A2').format.font={size:16,bold:true};
 sh.getRange('A3:A5').format.font={size:10,color:'#64748B'};
 sh.getRange('A7:F7').format={fill:'#203C50',font:{bold:true,color:'#FFFFFF'},rowHeight:26};
 for(const [col,width] of [['A',7],['B',90],['C',10],['D',54],['E',14],['F',65]]) sh.getRange(`${col}7:${col}${7+data.length}`).format.columnWidth=width;
 sh.getRange(`A8:F${7+data.length}`).format.rowHeight=24;
 sh.getRange(`E8:E${7+data.length}`).setNumberFormat('yyyy-mm-dd');
 sh.getRange(`D8:D${7+data.length}`).format.font={color:'#2563EB'};
 sh.freezePanes.freezeRows(7);
}
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Piese integrale'!A7:F10",maxChars:1800,tableMaxRows:4})).ndjson);
for(const name of ['Piese integrale','Clipuri scurte','Live radio']){
 const p=await wb.render({sheetName:name,range:'A1:E12',scale:1,format:'png'});
 await fs.writeFile(`${out}/${name}.png`,new Uint8Array(await p.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(out+'/AEYSA_linkuri_YouTube.xlsx');
console.log('Exported 76 links; unique IDs: '+new Set(rows.map(r=>r.id)).size);


