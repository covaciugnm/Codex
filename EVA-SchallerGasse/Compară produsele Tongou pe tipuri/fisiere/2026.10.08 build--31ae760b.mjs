import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dest='D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ';
const data=JSON.parse(await fs.readFile(path.join(dest,'Date structurate/2026.10.08 produse-normalizate.json'),'utf8'));
const official=JSON.parse(await fs.readFile(path.join(dest,'Date structurate/2026.10.08 registru manuale oficiale.json'),'utf8'));
const broken=JSON.parse(await fs.readFile(path.join(dest,'Date structurate/2026.10.08 registru manuale.json'),'utf8'));
const wb=Workbook.create();
const names=['1 pol - 1P+N','2 poli','3 poli','4 poli'];
const navy='#243B53',blue='#155EAD',green='#267347',orange='#A95C00',red='#B42318',gray='#697586';
const groupOrder=['Disjunctoare MCB','Disjunctoare diferențiale RCBO','Diferențial RCCB / RCBO de clarificat','Întrerupătoare smart','Descărcătoare SPD'];
const techOrder=Object.keys(data[0].technical);
const blockIndex=[];
function styleBase(sh,lastRow,lastCol){
 sh.showGridLines=false;
 const range=sh.getRangeByIndexes(0,0,lastRow,lastCol);
 range.format.font={name:'Arial',size:10,color:'#263445'};
 range.format.verticalAlignment='center';range.format.rowHeight=30;
 range.format.wrapText=true;
}
function cell(sh,r,c,v){sh.getCell(r-1,c-1).values=[[v]];}
function header(sh,r,count){const a=sh.getRangeByIndexes(r-1,0,1,count);a.format.fill=navy;a.format.font={bold:true,color:'#FFFFFF'};a.format.horizontalAlignment='center';a.format.rowHeight=30;}
function fmtCell(sh,r,c,v){
 const a=sh.getCell(r-1,c-1);
 if(typeof v==='number'){a.format.horizontalAlignment='right';return;}
 if(String(v).startsWith('✓'))a.format.font.color=green;
 if(String(v).startsWith('?')){a.format.font.color=gray;a.format.fill='#F3F4F6';}
 if(String(v).startsWith('Nu')||String(v).startsWith('—'))a.format.font.color=gray;
}
for(let pole=1;pole<=4;pole++){
 const sh=wb.worksheets.add(names[pole-1]);sh.tabColor=navy;
 const items=data.filter(p=>p.sheet===pole);const maxCols=Math.max(5,...groupOrder.map(g=>items.filter(p=>p.group===g).length+1));
 const blocks=[];let row=6;
 for(const group of groupOrder){
  const ps=items.filter(p=>p.group===group).sort((a,b)=>Number(a.smart)-Number(b.smart)||a.technical['Preț cu TVA (RON)']-b.technical['Preț cu TVA (RON)']);
  if(!ps.length)continue;
  const fields=techOrder.filter(k=>{
   if(ps.every(p=>p.spd))return ['Model / serie','Configurație în titlu','Configurație în descriere','Tip aparat','Tensiune declarată (V)','Protecție impulsuri SPD','Curent descărcare nominal/maxim (kA)','Distanță între eclatoare (mm)','Montaj','Grad de protecție','Standarde declarate','Greutate (kg)','Preț cu TVA (RON)','Status stoc','Cantitate disponibilă (buc.)','PN Conex','EAN'].includes(k);
   if(['Model / serie','Configurație în titlu','Configurație în descriere','Tip aparat','Comunicație SKU','Greutate (kg)','Preț cu TVA (RON)','Status stoc','Cantitate disponibilă (buc.)','PN Conex','EAN'].includes(k))return true;
   return ps.some(p=>!['— Nu se aplică','? Neprecizat','? Nu este indicat SPD'].includes(p.technical[k]));
  });
  // Always expose key protection uncertainties, including RCBO/RCCB distinctions.
  for(const k of ['Capacitate de rupere (kA)','Tip diferențial A / AC / B','Protecție la supracurent','Protecție la scurtcircuit','Protecție diferențială'])if(!ps[0].spd&&!fields.includes(k))fields.splice(11,0,k);
  const start=row;row+=3+fields.length+5;
  blocks.push({group,ps,fields,start});
 }
 styleBase(sh,row+2,maxCols);
 sh.getRangeByIndexes(0,0,row+2,1).format.columnWidth=40;
 sh.getRangeByIndexes(0,1,row+2,maxCols-1).format.columnWidth=38;
 cell(sh,2,1,`TONGOU · ${pole===1?'1 pol / 1P+N':pole+' poli'}`);sh.getCell(1,0).format.font={size:15,bold:true};sh.getRangeByIndexes(1,0,1,maxCols).format.rowHeight=32;
 cell(sh,3,1,`2026.10.08 · ${items.length} produse`);
 cell(sh,3,2,'✓ Verde: funcție confirmată');sh.getCell(2,1).format.font.color=green;
 cell(sh,3,3,'✓ Albastru: funcție care diferă');sh.getCell(2,2).format.font.color=blue;
 cell(sh,3,4,'✓ Portocaliu: observație / neconcordanță');sh.getCell(2,3).format.font.color=orange;
 cell(sh,3,5,'? Neprecizat · Nu: absent / altă variantă');sh.getCell(2,4).format.font.color=gray;
 sh.getRangeByIndexes(2,0,2,maxCols).format.rowHeight=42;
 if(pole===1){cell(sh,4,1,'1P simplu: niciun produs în cele 29 de rezultate.');cell(sh,4,2,'Subdiviziune 1P+N: fază + neutru; nu este echivalată cu 1P simplu.');}
 else{cell(sh,4,1,'Grupare după titlul comercial.');cell(sh,4,2,'Polii și modelele neconcordante sunt explicate la Observații.');}
 for(const {group,ps,fields,start} of blocks){
  const n=ps.length+1;const section=sh.getRangeByIndexes(start-1,0,1,n);section.format.fill='#E5ECF3';section.format.rowHeight=44;section.format.font.bold=true;cell(sh,start,1,group);
  const skuRow=start+1,nameRow=start+2;
  sh.getRangeByIndexes(skuRow-1,0,1,n).values=[['Cod produs / SKU',...ps.map(p=>p.sku)]];header(sh,skuRow,n);
  sh.getRangeByIndexes(nameRow-1,0,1,n).values=[['Denumire produs',...ps.map(p=>p.name)]];
  sh.getRangeByIndexes(nameRow-1,0,1,n).format.fill='#F0F4F8';sh.getRangeByIndexes(nameRow-1,0,1,n).format.rowHeight=95;
  sh.getRangeByIndexes(nameRow-1,0,1,n).format.font.bold=true;
  let r=start+3;
  for(const key of fields){
   const values=ps.map(p=>p.technical[key]);
   sh.getRangeByIndexes(r-1,0,1,n).values=[[key,...values]];
   if((r-start)%2===0)sh.getRangeByIndexes(r-1,0,1,n).format.fill='#F8FAFC';
   sh.getCell(r-1,0).format.font.bold=true;
   if(['Model / serie','Tip aparat','Configurație în descriere'].includes(key))sh.getRangeByIndexes(r-1,0,1,n).format.rowHeight=60;
   if(['Asistenți vocali','Sisteme de operare','Limba aplicației'].includes(key))sh.getRangeByIndexes(r-1,0,1,n).format.rowHeight=44;
   const differs=values.some(v=>String(v).startsWith('Nu'));
   values.forEach((v,i)=>{fmtCell(sh,r,i+2,v);if(differs&&String(v).startsWith('✓')){sh.getCell(r-1,i+1).format.font.color=blue;sh.getCell(r-1,i+1).format.fill='#EAF2FF';}});
   if(key==='Preț cu TVA (RON)')sh.getRangeByIndexes(r-1,1,1,ps.length).setNumberFormat('#,##0.00');
   if(key==='Greutate (kg)')sh.getRangeByIndexes(r-1,1,1,ps.length).setNumberFormat('0.00');
   if(key==='EAN')sh.getRangeByIndexes(r-1,1,1,ps.length).setNumberFormat('0');
   if(key==='PN Conex')sh.getRangeByIndexes(r-1,1,1,ps.length).setNumberFormat('@');
   if(key==='Status stoc')sh.getRangeByIndexes(r-1,1,1,ps.length).conditionalFormats.add('containsText',{text:'EPUIZAT',format:{fill:'#FEE4E2',font:{color:red,bold:true}}});
   if(key==='Cantitate disponibilă (buc.)')sh.getRangeByIndexes(r-1,1,1,ps.length).conditionalFormats.add('cellIs',{operator:'equal',formula:0,format:{fill:'#FEE4E2',font:{color:red,bold:true}}});
   ps.forEach((p,i)=>{if(p.issues.length&&((key==='Model / serie')||(key==='Curent nominal / reglaj (A)'&&p.sku==='43073')||(key==='Configurație în descriere'&&p.sku==='43067')||(key==='Tensiune declarată (V)'&&['43077','43078'].includes(p.sku))||(key==='Tip aparat'&&['43084','43092'].includes(p.sku)))){sh.getCell(r-1,i+1).format.font.color=orange;sh.getCell(r-1,i+1).format.fill='#FFF2D6';}});
   r++;
  }
  cell(sh,r,1,'Diferențe funcționale în grupă');
  ps.forEach((p,i)=>{const diffs=fields.filter(k=>String(p.technical[k]).startsWith('✓')&&ps.some(q=>String(q.technical[k]).startsWith('Nu')));const specs=['Comunicație SKU','Curent nominal / reglaj (A)','Curent diferențial (mA)','Tensiune declarată (V)'].filter(k=>!String(p.technical[k]).startsWith('?')&&!String(p.technical[k]).startsWith('—')&&new Set(ps.map(q=>q.technical[k]).filter(v=>!String(v).startsWith('?')&&!String(v).startsWith('—'))).size>1);const summary=[...diffs,...specs.map(k=>k+': '+p.technical[k])];cell(sh,r,i+2,summary.length?'✓ '+summary.join('; '):'— Nicio diferență funcțională confirmată în această grupă');sh.getCell(r-1,i+1).format.font.color=blue;});
  sh.getRangeByIndexes(r-1,0,1,n).format.rowHeight=110;r++;
  cell(sh,r,1,'Observații și neconcordanțe');
  ps.forEach((p,i)=>{cell(sh,r,i+2,'✓ '+p.observations.join('\n'));sh.getCell(r-1,i+1).format.font.color=orange;sh.getCell(r-1,i+1).format.fill='#FFF2D6';});
  sh.getRangeByIndexes(r-1,0,1,n).format.rowHeight=210;
  sh.getRangeByIndexes(r-1,0,1,n).format.verticalAlignment='top';
  blockIndex.push({sheet:sh.name,start,end:r,skus:ps.map(p=>p.sku)});
 }
 sh.freezePanes.freezeRows(4);sh.freezePanes.freezeColumns(1);
}
const catalog=wb.worksheets.add('Catalog si stoc');
const hdr=['SKU','Denumire produs','Poli / grupare','Tip aparat','Model / serie','Preț cu TVA (RON)','Stoc (buc.)','Status stoc','Sursa cantității','Data verificării','Documentație Conex','URL sursă','Observații'];
styleBase(catalog,36,hdr.length);catalog.getRange('A2').values=[['Catalog Tongou · 29 produse']];catalog.getRange('A2').format.font={size:15,bold:true};
catalog.getRange('A3').values=[['2026.10.08']];catalog.getRange('B3').values=[['Cantități din câmpul public Stoc. Verificarea prin coș nu a fost necesară.']];catalog.getRange('B3').format.rowHeight=40;
catalog.getRange('A5:M5').values=[hdr];header(catalog,5,13);
const sorted=[...data].sort((a,b)=>a.sku.localeCompare(b.sku));
const table=sorted.map(p=>[p.sku,p.name,p.poles,p.technical['Tip aparat'],p.technical['Model / serie'],p.technical['Preț cu TVA (RON)'],p.technical['Cantitate disponibilă (buc.)'],p.technical['Status stoc'],p.stock_source,new Date('2026-10-08T12:00:00Z'),p.files.length?p.files.length+' link(uri); HTTP 404':'Nu este publicată',p.source,p.observations.join('\n')]);
catalog.getRange('A6:M34').values=table;catalog.getRange('A6:M34').format.rowHeight=105;
catalog.getRange('A5:A34').format.columnWidth=11;catalog.getRange('B5:B34').format.columnWidth=58;
catalog.getRange('C5:C34').format.columnWidth=16;catalog.getRange('D5:E34').format.columnWidth=33;
catalog.getRange('F5:H34').format.columnWidth=18;catalog.getRange('I5:K34').format.columnWidth=32;
catalog.getRange('L5:L34').format.columnWidth=60;catalog.getRange('M5:M34').format.columnWidth=85;
catalog.getRange('F6:F34').setNumberFormat('#,##0.00');catalog.getRange('G6:G34').setNumberFormat('0');catalog.getRange('J6:J34').setNumberFormat('yyyy.mm.dd');
const catalogTable=catalog.tables.add('A5:M34',true,'CatalogTongou');catalogTable.style='TableStyleLight9';catalog.freezePanes.freezeRows(5);catalog.freezePanes.freezeColumns(2);
catalog.getRange('H6:H34').conditionalFormats.add('containsText',{text:'EPUIZAT',format:{fill:'#FEE4E2',font:{color:red,bold:true}}});
const docs=wb.worksheets.add('Documentatie');const docRows=[];
for(const b of broken)docRows.push(['Link Conex indisponibil',b.title,b.skus.join(', '),'HTTP 404',null,b.url,'','Originalul nu a putut fi descărcat. Nu este marcat ca document recuperat.']);
function relevant(title){if(title.startsWith('TORD4'))return '43092';if(title.startsWith('TOSMR1'))return '43082; 43073 de confirmat';if(title.startsWith('SY1'))return '43074; 43083 de confirmat';if(title.startsWith('TOSPO'))return '43094, 43095, 43096';if(title.startsWith('TOSP'))return '43097, 43098';return data.filter(p=>p.technical['Model / serie'].includes('TOQCB2')).map(p=>p.sku).join(', ');}
for(const o of official)docRows.push(['Document oficial alternativ',o.titlu,relevant(o.titlu),o.status,o.pages??null,o.url,o.status==='DESCARCAT'?o.path:'',o.observatii]);
styleBase(docs,docRows.length+9,8);
cell(docs,2,1,'Documentație tehnică');docs.getCell(1,0).format.font={size:15,bold:true};
cell(docs,3,1,'5 linkuri Conex defecte.');cell(docs,3,2,`${official.filter(o=>o.status==='DESCARCAT').length} PDF-uri oficiale descărcate.`);cell(docs,3,3,'Manualele de familie nu confirmă automat toate funcțiile SKU.');docs.getRange('A3:H3').format.rowHeight=55;
docs.getRange('A5:H5').values=[['Categorie','Document','SKU / familie','Status','Pagini','URL sursă','Fișier local','Observații']];header(docs,5,8);
docs.getRangeByIndexes(5,0,docRows.length,8).values=docRows;docs.getRangeByIndexes(5,0,docRows.length,8).format.rowHeight=130;
docs.getRange('A5:A30').format.columnWidth=30;docs.getRange('B5:B30').format.columnWidth=42;docs.getRange('C5:C30').format.columnWidth=38;docs.getRange('D5:E30').format.columnWidth=16;docs.getRange('F5:G30').format.columnWidth=62;docs.getRange('H5:H30').format.columnWidth=75;
docs.freezePanes.freezeRows(5);docs.freezePanes.freezeColumns(2);
docs.getRangeByIndexes(5,3,docRows.length,1).conditionalFormats.add('containsText',{text:'404',format:{fill:'#FFF2D6',font:{color:orange,bold:true}}});
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'2 poli'!A7:E12",include:'values,formulas',tableMaxRows:6,tableMaxCols:5,maxChars:1800})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
const out=path.join(dest,'2026.10.08 Tongou comparativ produse.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(out);
await fs.writeFile(path.join(dest,'Lucru/2026.10.08 blocuri verificare.json'),JSON.stringify(blockIndex,null,2));
for(const name of [...names,'Catalog si stoc','Documentatie']){
 const range=name==='Catalog si stoc'?'A5:H10':name==='Documentatie'?'A5:E10':'A1:E20';
 try{const b=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(dest,'Lucru',`2026.10.08 previzualizare ${name}.png`),new Uint8Array(await b.arrayBuffer()));}catch(e){console.log('RENDER',name,String(e));}
}
for(const b of blockIndex.filter(b=>b.skus.includes('43073')||b.skus.includes('43092')||b.skus.includes('43074'))){const v=await wb.render({sheetName:b.sheet,range:`A${b.end-3}:E${b.end}`,scale:1,format:'png'});await fs.writeFile(path.join(dest,'Lucru',`2026.10.08 observatii ${b.skus[0]}.png`),new Uint8Array(await v.arrayBuffer()));}
console.log('SAVED',out);
