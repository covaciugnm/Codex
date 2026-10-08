import fs from 'node:fs/promises';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const dir='D:/MP3.Varvi/outputs/party_20261008';
const wb=Workbook.create();
const summary=wb.worksheets.add('Sinteză');
const categories=[
 ['Jazz & lounge','Masă și conversație'],
 ['Soul & Motown','Masă, apoi dans lejer'],
 ['Disco & funk','Dans și energie'],
 ['Pop de petrecere','Dans și refrene cunoscute'],
 ['Balade rock','Dans lent și pauze între seturi'],
 ['Blues','Atmosferă și dans lent'],
 ['Rock clasic','Petrecere, după masă'],
 ["Rock'n'roll & oldies",'Dans în perechi'],
 ['Latino & internațional','Dans și varietate'],
 ['Românești','Refrene cunoscute și dans']
];
const navy='#20364B', muted='#637587', light='#EDF2F7';
function styleBase(sh,lastCol,lastRow){
 sh.showGridLines=false;
 const area=sh.getRange(`A1:${lastCol}${lastRow}`);
 area.format.font={name:'Arial',size:11,color:'#253547'};
 area.format.verticalAlignment='center';
 area.format.rowHeight=24;
 sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
 sh.getRange(`A2:${lastCol}2`).format.rowHeight=32;
 sh.getRange(`A2:${lastCol}2`).format.borders={bottom:{style:'thin',color:'#C4CED8'}};
}
for(let i=0;i<categories.length;i++){
 const [name,moment]=categories[i];
 const sh=wb.worksheets.add(name);
 styleBase(sh,'G',57);
 for(const [col,width] of Object.entries({A:29,B:44,C:40,D:26,E:17,F:13,G:48}))sh.getRange(`${col}1:${col}57`).format.columnWidth=width;
 sh.getRange('A2').values=[[name]];
 sh.getRange('A4').values=[['Melodii completate']];
 sh.getRange('B4').formulas=[['=COUNTA(B8:B57)']];
 sh.getRange('E4').values=[['Durată totală']];
 sh.getRange('F4').formulas=[['=SUM(F8:F57)']];
 sh.getRange('F4').setNumberFormat('[h]:mm:ss');
 sh.getRange('A5').values=[['Durată: introdu 0:03:45 pentru o piesă de 3 min 45 sec. În coloana YouTube, lipește linkul videoclipului.']];
 sh.getRange('A5').format.font={name:'Arial',size:11,italic:true,color:muted};
 sh.getRange('A7:G7').values=[['Nume artist','Nume melodie','Nume album','Stil','Anul publicării','Durată','Link YouTube']];
 const table=sh.tables.add('A7:G57',true,`Playlist_${i+1}`);
 table.style='TableStyleMedium2';
 table.showFilterButton=true;
 sh.getRange('A7:G7').format={fill:navy,font:{name:'Arial',size:11,color:'#FFFFFF',bold:true},horizontalAlignment:'center',verticalAlignment:'center',rowHeight:30};
 sh.getRange('A8:D57').format.horizontalAlignment='left';
 sh.getRange('E8:F57').format.horizontalAlignment='right';
 sh.getRange('E8:E57').setNumberFormat('0');
 sh.getRange('F8:F57').setNumberFormat('mm:ss');
 sh.getRange('G8:G57').format.font={name:'Arial',size:11,color:'#1763AA'};
 sh.getRange('E8:E57').dataValidation={rule:{type:'whole',operator:'between',formula1:1900,formula2:2100}};
 sh.freezePanes.freezeRows(7);
}
styleBase(summary,'E',27);
summary.tabColor=navy;
for(const [c,w] of Object.entries({A:31,B:19,C:18,D:40,E:3}))summary.getRange(`${c}1:${c}27`).format.columnWidth=w;
summary.getRange('A2').values=[['Playlist pentru masă și petrecere']];
summary.getRange('A4').values=[['Țintă după completare: 20–24 de ore de muzică, echilibrate pe stiluri.']];
summary.getRange('A5').values=[['Model nepopulat. Cele 10 foi de stiluri au câte 50 de rânduri libere.']];
summary.getRange('A4:A5').format.font={name:'Arial',size:11,color:muted};
summary.getRange('A7:D7').values=[['Stil / tab','Nr. melodii','Durată totală','Moment potrivit']];
summary.getRange('A7:D7').format={fill:navy,font:{name:'Arial',size:11,color:'#FFFFFF',bold:true},horizontalAlignment:'center',rowHeight:30};
for(let i=0;i<categories.length;i++){
 const [name,moment]=categories[i],r=i+8;
 const escaped=name.replaceAll("'","''");
 summary.getRange(`A${r}:D${r}`).values=[[name,null,null,moment]];
 summary.getRange(`B${r}:C${r}`).formulas=[[`='${escaped}'!B4`,`='${escaped}'!F4`]];
 if(i%2===0)summary.getRange(`A${r}:D${r}`).format.fill=light;
}
summary.getRange('A19').values=[['TOTAL']];
summary.getRange('B19:C19').formulas=[['=SUM(B8:B17)','=SUM(C8:C17)']];
summary.getRange('A19:D19').format={fill:'#DEE7EF',font:{name:'Arial',size:11,bold:true,color:navy},rowHeight:30};
summary.getRange('B8:B19').setNumberFormat('0');
summary.getRange('C8:C19').setNumberFormat('[h]:mm:ss');
summary.getRange('B8:C19').format.horizontalAlignment='right';
summary.getRange('A22').values=[['Cum completezi']];
summary.getRange('A22').format.font={name:'Arial',size:11,bold:true,color:navy};
summary.getRange('A23').values=[['O melodie pe rând, în foaia stilului potrivit. Toate cele 7 coloane sunt libere.']];
summary.getRange('A24').values=[['Anul se referă la publicarea melodiei în versiunea aleasă. Durata se introduce ca h:mm:ss.']];
summary.getRange('A25').values=[['Totalurile se actualizează automat pentru cele 50 de rânduri din fiecare foaie.']];
summary.getRange('A26').values=[['Folosește filtrele din antet pentru a alege artistul, stilul sau anul.']];
summary.getRange('A23:A26').format.font={name:'Arial',size:11,color:muted};
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Sinteză'!A7:D19",include:'values,formulas',tableMaxRows:13,tableMaxCols:4,maxChars:3500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'Formula errors'})).ndjson);
// A temporary input verifies that summary links really recalculate.
const first=wb.worksheets.getItem(categories[0][0]);
first.getRange('B8').values=[['TEST TEMPORAR']];first.getRange('F8').values=[[225/86400]];
wb.recalculate();
const probe=summary.getRange('B19:C19').values[0];
if(probe[0]!==1 || Math.abs(probe[1]-225/86400)>1e-9)throw Error('Summary recalculation failed '+JSON.stringify(probe));
first.getRange('B8').clear({applyTo:'contents'});first.getRange('F8').clear({applyTo:'contents'});
wb.recalculate();
if(summary.getRange('B19:C19').values[0].some(v=>v!==0))throw Error('Template was not reset');
for(let i=0;i<categories.length;i++){
 const sh=wb.worksheets.getItem(categories[i][0]);
 if(sh.getRange('A8:G57').values.some(row=>row.some(v=>v!==null && v!=='' && v!==undefined)))throw Error('Nonempty music row');
}
await fs.mkdir(dir+'/previews',{recursive:true});
for(const [idx,name] of ['Sinteză',...categories.map(x=>x[0])].entries()){
 const preview=await wb.render({sheetName:name,range:idx===0?'A1:D27':'A1:G11',scale:1,format:'png'});
 await fs.writeFile(`${dir}/previews/template_${idx}.png`,new Uint8Array(await preview.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(dir+'/Model_playlist_masa_si_petrecere.xlsx');
console.log('Exported empty template: 11 tabs, 500 blank music rows, totals verified.');
