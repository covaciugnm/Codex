import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='Z:/00.Roboti/Nvidia/SH';
const data=JSON.parse(await fs.readFile(`${root}/monitorizare/oferte.json`,'utf8'));
const dateSerial=(Date.UTC(2026,9,30)-Date.UTC(1899,11,30))/86400000;
const headers=['Model','Configuratie','Vanzator','Tara expediere','Pret afisat','Moneda','TVA / baza pretului','Transport RO','Total cunoscut','Stoc / stare','Livrare in Romania','Verificat la','Observatii','Note personale','Sursa'];
for(const cat of ['Noi','SH']){
 const wb=Workbook.create();
 for(const section of ['Oferte','De verificat','Excluse']){
  const rows=data.offers.filter(r=>r[0]===cat&&r[1]===section).sort((a,b)=>a[2].localeCompare(b[2])||a[7].localeCompare(b[7])||a[6]-b[6]);
  const s=wb.worksheets.add(section); s.showGridLines=false;
  s.getRange('A2').values=[[`NVIDIA Europa — ${cat==='Noi'?'echipamente noi':'second-hand'}`]];
  s.getRange('A3').values=[[section==='Oferte'?'30.10.2026. Livrarea RO este confirmata numai unde apare explicit.':'30.10.2026. Aceste rezultate nu sunt oferte confirmate pentru livrare in Romania.']];
  s.getRange('A4').values=[[cat==='SH'?'Thor 128GB SH: nicio oferta europeana eligibila verificata in aceasta cautare.':'Preturile sunt in moneda sursei. TVA local poate fi ajustat pentru Romania la checkout.']];
  s.getRange('A5').values=[['Totalul ramane necunoscut daca transportul RO lipseste. Minimele sunt dintre ofertele gasite, nu din intreaga piata.']];
  s.getRange('A7:O7').values=[headers];
  const matrix=rows.map(r=>[r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],null,r[10],r[11],dateSerial,r[13],'',r[12]]);
  const last=7+matrix.length;
  s.getRange(`A8:O${last}`).values=matrix;
  s.getRange(`I8:I${last}`).formulas=rows.map((r,i)=>[`=IF(ISNUMBER(H${i+8}),E${i+8}+H${i+8},"Necunoscut")`]);
  s.getRange(`A7:N${last}`).format.font={name:'Arial',size:10,color:'#17253A'};
  s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#17253A'};
  s.getRange('A3:A5').format.font={name:'Arial',size:10,color:'#4B5563'};
  s.getRange('A7:N7').format={fill:'#263C5A',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeight:32};
  s.getRange(`A8:N${last}`).format.wrapText=true;
  s.getRange(`A8:N${last}`).format.verticalAlignment='center';
  s.getRange(`A8:N${last}`).format.rowHeight=62;
  const widths={A:25,B:27,C:27,D:25,E:16,F:10,G:29,H:16,I:17,J:27,K:31,L:15,M:65,N:30,O:115};
  for(const [col,width]of Object.entries(widths))s.getRange(`${col}7:${col}${last}`).format.columnWidth=width;
  s.getRange(`E8:I${last}`).setNumberFormat('#,##0.00');
  s.getRange(`L8:L${last}`).setNumberFormat('yyyy-mm-dd');
  s.getRange(`O8:O${last}`).format.font={name:'Arial',size:10,color:'#1D4ED8'};
  s.getRange(`O8:O${last}`).format.wrapText=true;
  s.getRange(`O8:O${last}`).format.verticalAlignment='center';
  s.getRange('O7').format={fill:'#263C5A',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center'};
  s.getRange(`N8:N${last}`).format.fill='#FFF6D6';
  for(let i=0;i<rows.length;i++)if(i%2===1)s.getRange(`A${i+8}:M${i+8}`).format.fill='#F1F5F9';
  s.tables.add(`A7:O${last}`,true,`${cat}_${section.replaceAll(' ','')}`);
  s.freezePanes.freezeRows(7);s.freezePanes.freezeColumns(1);
  s.tabColor=section==='Oferte'?'#263C5A':section==='De verificat'?'#B7791F':'#9CA3AF';
 }
 wb.recalculate();
 console.log(cat,(await wb.inspect({kind:'region',sheetId:'Oferte',range:'E8:L10',maxChars:1600,tableMaxCols:8})).ndjson);
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:15},maxChars:1200})).ndjson);
 for(const section of ['Oferte','De verificat','Excluse']){
  const preview=await wb.render({sheetName:section,range:'L7:O11',scale:1,format:'png'});
  await fs.writeFile(`${root}/monitorizare/${cat}_${section.replaceAll(' ','_')}.png`,new Uint8Array(await preview.arrayBuffer()));
 }
 const out=cat==='Noi'?`${root}/Noi/Oferte_NVIDIA_Noi.xlsx`:`${root}/Second_Hand/Oferte_NVIDIA_SH.xlsx`;
 await (await SpreadsheetFile.exportXlsx(wb)).save(out);
 console.log('SAVED',out);
}
await fs.mkdir(`${root}/monitorizare/istoric`,{recursive:true});
await fs.copyFile(`${root}/monitorizare/oferte.json`,`${root}/monitorizare/istoric/2026-10-30.json`);
