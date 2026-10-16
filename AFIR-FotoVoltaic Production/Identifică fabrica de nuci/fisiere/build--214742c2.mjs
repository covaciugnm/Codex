import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const work=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/,'$1'));
const root='Z:/00. Proiecte 2025/AFIR FotoVoltaic 1/50. Fabrica Nuci/nuttechnology.com';
const d=JSON.parse(await fs.readFile(path.join(work,'data.json'),'utf8'));
const out=root+'/07_Centralizatoare';
let tableNum=0;const nativeLinks=[];
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
function sheet(w,name,title,headers,rows,widths,note='',start=5){
 const s=w.worksheets.add(name);s.showGridLines=false;
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:'#273C32'};
 if(note){s.getRange('A3').values=[[note]];s.getRange('A3').format.font={name:'Arial',size:10,color:'#5F6368'};}
 const end=start+rows.length;
 s.getRange('A'+start+':'+col(headers.length-1)+end).values=[headers,...rows.map(r=>r.map(v=>v??null))];
 const all=s.getRange('A'+start+':'+col(headers.length-1)+end);all.format.font={name:'Arial',size:10};all.format.verticalAlignment='top';all.format.wrapText=true;
 s.getRange('A'+start+':'+col(headers.length-1)+start).format={fill:'#344E41',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:34,wrapText:true,verticalAlignment:'center'};
 s.getRange('A'+(start+1)+':'+col(headers.length-1)+end).format.rowHeight=48;
 widths.forEach((width,i)=>s.getRange(col(i)+':'+col(i)).format.columnWidth=width);
 s.freezePanes.freezeRows(start);s.freezePanes.freezeColumns(2);
 const table=s.tables.add('A'+start+':'+col(headers.length-1)+end,true,'Data'+(++tableNum));table.style='TableStyleMedium4';
 s.getRange('A'+start+':'+col(headers.length-1)+start).format.horizontalAlignment='center';
 return s;
}
function links(s,rows,column,start=6){rows.forEach((r,i)=>{
 const v=r[column];if(!v||typeof v!=='string')return;
 const dest=v.startsWith('http')?v:path.resolve(root,v).replaceAll('\\','/');
 const label=v.startsWith('http')?'Pagina produs':path.basename(v.replaceAll('\\','/'));
 s.getRange(col(column)+(start+i)).values=[[label]];
 nativeLinks.push({sheet:s.name,cell:col(column)+(start+i),target:dest});
 s.getRange(col(column)+(start+i)).format.font.color='#2167A6';
});}
const comm=Workbook.create();
const serial=s=>(Date.parse(s)-Date.UTC(1899,11,30))/86400000;
const cr=d.comm.map(r=>[serial(r[0]+'Z'),...r.slice(1)]);
let s=sheet(comm,'Comunicatii','Comunicări cu Tudor și Nut Technology',['Data / ora RO','Canal','Sens','Expeditor','Destinatar / chat','Subiect / tip','Rezumat / mesaj','Atașamente','Export local','ID mesaj','Cont accesat','CC'],cr,[21,13,12,30,32,52,78,13,40,38,30,30],'7 emailuri și 5 mesaje WhatsApp recuperate. Ora României; istoricul este limitat la datele disponibile în EVA.');
s.getRange('A6:A17').setNumberFormat('yyyy-mm-dd hh:mm');links(s,cr,8);s.getRange('A6:L17').format.rowHeight=74;s.getRange('A6:L6').format.rowHeight=150;
s=sheet(comm,'Atasamente','Atașamente și documente transmise',['Data','Fișier','ID mesaj','ID atașament','Octeți','Fișier local','SHA-256 / proveniență'],d.attachments,[14,68,39,39,14,68,70],'Fiecare apariție este păstrată, inclusiv retransmiterile aceluiași document.');
links(s,d.attachments,5);s.getRange('E6:E'+(d.attachments.length+5)).setNumberFormat('#,##0');
s=sheet(comm,'De clarificat','Puncte rămase de clarificat',['Temă','Constatare','Acțiune necesară','Sursă'],d.actions,[23,80,74,72]);
s=sheet(comm,'Media locale','Filmări existente în folderul TechnoMS',['Fișier','Octeți','Copie locală','Proveniență'],d.media,[62,17,62,76],'Data din numele fișierului nu dovedește data transmiterii. Filmările nu au fost transcrise.');
links(s,d.media,2);
const eq=Workbook.create();
s=sheet(eq,'Oferta 179','Oferta 179 / 11.10.2026 - EUR fără TVA',['Poz.','Echipament','Buc.','Preț unitar EUR','Total declarat EUR','Total calculat EUR','Diferență EUR','Capacitate declarată','Putere declarată kW','Observații','Ofertă sursă','Pagina PDF'],d.latest,[8,58,9,17,19,19,17,40,18,76,65,12],'Panourile de comandă sunt excluse. Valabilitate: 60 de zile de la primire. Totalul necesită clarificare.',8);
for(let i=0;i<9;i++){let row=i+9;s.getRange('F'+row+':G'+row).formulas=[['=C'+row+'*D'+row,'=E'+row+'-F'+row]];}
s.getRange('A5').values=[['Total declarat EUR']];s.getRange('D5').values=[[320400]];
s.getRange('E5').values=[['Recalculat EUR']];s.getRange('F5').formulas=[['=SUM(F9:F17)']];
s.getRange('G5').formulas=[['=D5-F5']];s.getRange('H5').values=[['Diferență de clarificat']];
s.getRange('D5:G5').setNumberFormat('#,##0.00');s.getRange('D9:G17').setNumberFormat('#,##0.00');s.getRange('I9:I17').setNumberFormat('0.00');
s.getRange('G9:G17').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4D6',font:{bold:true,color:'#9C0006'}}});
s.getRange('G5').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4D6',font:{bold:true,color:'#9C0006'}}});
links(s,d.latest,10,9);
s=sheet(eq,'Preturi istorice','Oferte 82 / 16.04.2026 - EUR fără TVA',['Ofertă / variantă','Data ofertei','Echipament','Buc. în lot','Preț declarat lot EUR','Preț unitar derivat EUR','Interpretare','Document sursă','Pagina'],d.old.map(r=>[r[0],serial(r[1]),...r.slice(2)]),[32,17,63,13,23,24,48,68,11],'Prețuri istorice de reconfirmat. Variantele de linie sunt alternative, nu se însumează.');
for(let i=0;i<d.old.length;i++)s.getRange('F'+(i+6)).formulas=[['=E'+(i+6)+'/D'+(i+6)]];
s.getRange('B6:B'+(d.old.length+5)).setNumberFormat('yyyy-mm-dd');s.getRange('E6:F'+(d.old.length+5)).setNumberFormat('#,##0.00');links(s,d.old,7);
s=sheet(eq,'Catalog echipamente','Catalog echipamente și fișe disponibile',['Nr.','Etapă','Echipament','Capacitate','Putere din catalog','Tensiune','Material','Utilizare','Fișier local','Pagina în dosar','Document disponibil','Observații existente','Pagina produs'],d.catalog,[8,32,62,38,25,17,30,36,68,15,33,65,58],'Caracteristici din centralizatorul existent la 28.09.2026. Nu reprezintă confirmarea configurației ofertate.');
links(s,d.catalog,8);links(s,d.catalog,12);
s=sheet(eq,'Index fise','Index documente din dosarul tehnic',['Fișier original','Pagini document','Început în dosar','SHA-256','Tip document'],d.index,[85,18,19,70,55],d.uniquePdf+' PDF-uri unice, '+d.totalPages+' pagini în dosar. Copiile identice trimit la aceleași pagini.');
links(s,d.index,0);
s=sheet(eq,'Conditii si diferente','Condiții și diferențe de confirmat',['Temă','Constatare','Acțiune necesară','Sursă'],d.actions,[23,80,74,72]);
for(const [w,name] of [[comm,'Comunicatii_Tudor_NutTechnology_2026-10-16'],[eq,'Echipamente_si_preturi_NutTechnology_2026-10-16']]){
 w.recalculate();
 console.log(name,(await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1500})).ndjson);
 for(const sh of w.worksheets.items){
  const end=sh.name==='Oferta 179'?17:Math.min(sh.getUsedRange().values.length,9);
  const preview=await w.render({sheetName:sh.name,range:'A1:'+(sh.name==='Oferta 179'?'I':'D')+end,scale:1,format:'png'});
  await fs.writeFile(path.join(work,name+'_'+sh.name+'.png'),new Uint8Array(await preview.arrayBuffer()));
 }
 const x=await SpreadsheetFile.exportXlsx(w);await x.save(out+'/'+name+'.xlsx');
}
await fs.writeFile(path.join(work,'links.json'),JSON.stringify(nativeLinks));
console.log((await eq.inspect({kind:'table',range:"'Oferta 179'!D5:G5",include:'values,formulas',maxChars:1500})).ndjson);

