import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
process.on('uncaughtException',e=>{console.error(e.message);console.error(e.stack.split('\n').filter(l=>l.includes('build_5900')).join('\n'));process.exit(1);});

const base='Z:/00.Roboti/cesiro.com/work_nomexp';
const out='Z:/00.Roboti/cesiro.com/outputs/nomexp_5900_20261020';
await fs.mkdir(out,{recursive:true});
const data=JSON.parse(await fs.readFile(`${base}/build_5900_data.json`,'utf8'));
const wb=Workbook.create();
const sku=wb.worksheets.add('SKU_5900');
const exp=wb.worksheets.add('NOMEXP02_5900');
const cat=wb.worksheets.add('Cataloage');
const log=wb.worksheets.add('Corectii');
const original=wb.worksheets.add('Original_5900');
const navy='#24415A', muted='#526777', amber='#FFF3D6', pale='#EAF0F5';
const start=7,end=start+data.records.length-1;
const formEnd=6+data.forms.length,glazeEnd=6+data.glazes.length;
const formRange=`'Cataloage'!$A$7:$E$${formEnd}`,formKeys=`'Cataloage'!$A$7:$A$${formEnd}`;
const glazeRange=`'Cataloage'!$G$7:$J$${glazeEnd}`,glazeKeys=`'Cataloage'!$G$7:$G$${glazeEnd}`;
function fmt(sh,range) {
  sh.showGridLines=false;
  sh.getRange(range).format.font={name:'Arial',size:10,color:'#172C3C'};
  sh.getRange(range).format.verticalAlignment='center';
  sh.getRange(range).format.rowHeight=22;
}
function title(sh,text,sub) {
  sh.getRange('A2').values=[[text]];
  sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
  sh.getRange('A2').format.rowHeight=28;
  sh.getRange('A3').values=[[sub]];
  sh.getRange('A3').format.font={name:'Arial',size:10,color:muted};
}
function header(sh,range) {
  sh.getRange(range).format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center',horizontalAlignment:'center',rowHeight:42};
}
function table(sh,range,name) {
  const t=sh.tables.add(range,true,name);
  t.style='TableStyleMedium2';
  return t;
}
function col(sh,letters,width) {sh.getRange(`${letters}:${letters}`).format.columnWidth=width;}
function literal(v) {return typeof v==='string'&&v.startsWith('=')?"'"+v:v;}

fmt(cat,`A1:J${Math.max(formEnd,glazeEnd)}`);
title(cat,'Cataloage pentru SKU 5900','Sursa: NOMEXP_v9_ultimate.(2).xlsx. Referințele exacte sunt indicate lângă fiecare definiție.');
cat.getRange('A5').values=[['Forme de set']];
cat.getRange('G5').values=[['Glazuri și compoziții']];
cat.getRange('A6:E6').values=[['Cod formă','Denumire set','Model din SKU','Nr. piese','Sursă']];
cat.getRange('G6:J6').values=[['Cod glazură','Descriere / compoziție','Stare descriere','Sursă']];
cat.getRange(`A7:E${formEnd}`).values=data.forms;
cat.getRange(`G7:J${glazeEnd}`).values=data.glazes.map(r=>[r[0],r[1]??'De completat',r[2],r[3]]);
header(cat,'A6:E6');header(cat,'G6:J6');
table(cat,`A6:E${formEnd}`,'Forme5900');table(cat,`G6:J${glazeEnd}`,'Glazuri5900');
[['A',12],['B',34],['C',16],['D',12],['E',51],['F',3],['G',15],['H',63],['I',20],['J',62]].forEach(([c,w])=>col(cat,c,w));
cat.getRange(`A7:A${formEnd}`).setNumberFormat('0');
cat.getRange(`C7:C${formEnd}`).setNumberFormat('@');
cat.getRange(`D7:D${formEnd}`).setNumberFormat('0');
cat.getRange(`A7:A${formEnd}`).format.horizontalAlignment='center';
cat.getRange(`D7:D${formEnd}`).format.horizontalAlignment='center';
cat.getRange(`G7:G${glazeEnd}`).setNumberFormat('@');
const unknownColorIndex=data.glazes.findIndex(r=>r[0]==='324L')+7;
cat.getRange(`H${unknownColorIndex}`).format.fill=amber;
cat.freezePanes.freezeRows(6);

const headers=['SKU corect','Denumire articol','Model','Cod formă','Cod glazură','Descriere glazură','Nr. piese','Categorie','UM','Cod beneficiar','Valută','Preț unitar','Cost standard','Greutate netă','Greutate brută','Cod intern','Articol client','Denumire beneficiar','Control cod','Date de completat','Rânduri în sursă'];
fmt(sku,`A1:U${end}`);
title(sku,'Nomenclator SKU 5900','366 SKU unice • 18 forme de set • 367 înregistrări sursă • 20.10.2026');
sku.getRange('A4').values=[['Câmpurile galbene sunt de completat. Prețurile, costurile și greutățile lipsesc din sursă; zero nu a fost presupus.']];
sku.getRange('A4').format.font={name:'Arial',size:10,color:muted};
sku.getRange('A6:U6').values=[headers];
const rows=data.records.map(r=>{
  const v=r.values;
  return [null,null,String(v.U),v.I,v.F,null,null,v.H,v.AD,v.O,v.AB,v.K,v.L,v.M,v.N,v.T,v.Q,v.P,null,null,r.source_rows.join(', ')];
});
sku.getRange(`A7:U${end}`).values=rows;
const colFormulas={A:[],B:[],F:[],G:[],S:[],T:[]};
for(let r=start;r<=end;r++) {
  colFormulas.A.push([`=J${r}&"_"&C${r}&"_"&D${r}&"_"&E${r}`]);
  colFormulas.F.push([`=IF(COUNTIF(${glazeKeys},E${r})=0,"Glazură necunoscută",IF(OR(VLOOKUP(E${r},${glazeRange},2,FALSE)="De completat",VLOOKUP(E${r},${glazeRange},2,FALSE)=0),"Descriere lipsă: "&E${r},VLOOKUP(E${r},${glazeRange},2,FALSE)))`]);
  colFormulas.B.push([`=IF(COUNTIF(${formKeys},D${r})=0,"Formă necunoscută",VLOOKUP(D${r},${formRange},2,FALSE))&" - "&IF(F${r}="Descriere lipsă: "&E${r},E${r},F${r})`]);
  colFormulas.G.push([`=IF(COUNTIF(${formKeys},D${r})=0,"Formă necunoscută",VLOOKUP(D${r},${formRange},4,FALSE))`]);
  colFormulas.S.push([`=IF(OR(C${r}="",D${r}="",E${r}="",J${r}=""),"Cod incomplet",IF(COUNTIF($A$7:$A$${end},A${r})>1,"SKU duplicat",IF(COUNTIF(${formKeys},D${r})=0,"Formă necunoscută",IF(OR(LEN(C${r})<>4,LEN(D${r}&"")<>4,LEN(E${r})<>4,J${r}<>5900),"Format de verificat",IF(C${r}<>VLOOKUP(D${r},${formRange},3,FALSE),"Model neconcordant",IF(COUNTIF(${glazeKeys},E${r})=0,"Glazură necunoscută","Cod valid"))))))`]);
  colFormulas.T.push([`=IF(F${r}="Descriere lipsă: "&E${r},"Descriere glazură; ","")&IF(L${r}="","Preț; ","")&IF(M${r}="","Cost; ","")&IF(N${r}="","Greutate netă; ","")&IF(O${r}="","Greutate brută; ","")&IF(P${r}="","Cod intern; ","")&IF(OR(R${r}="",R${r}="A"),"Beneficiar; ","")`]);
}
for(const [c,forms] of Object.entries(colFormulas))sku.getRange(`${c}7:${c}${end}`).formulas=forms;
table(sku,`A6:U${end}`,'TblSku5900');
header(sku,'A6:U6');
[['A',30],['B',48],['C',10],['D',11],['E',13],['F',59],['G',10],['H',12],['I',8],['J',13],['K',10],['L',14],['M',15],['N',15],['O',15],['P',18],['Q',19],['R',24],['S',23],['T',100],['U',20]].forEach(([c,w])=>col(sku,c,w));
sku.getRange(`A7:A${end}`).setNumberFormat('@');
sku.getRange(`C7:C${end}`).setNumberFormat('@');
sku.getRange(`D7:D${end}`).setNumberFormat('0');
sku.getRange(`E7:E${end}`).setNumberFormat('@');
sku.getRange(`G7:G${end}`).setNumberFormat('0');
sku.getRange(`J7:J${end}`).setNumberFormat('0');
sku.getRange(`L7:M${end}`).setNumberFormat('0.0000');
sku.getRange(`N7:O${end}`).setNumberFormat('0.00');
sku.getRange(`P7:Q${end}`).setNumberFormat('@');
sku.getRange(`B7:B${end}`).format.wrapText=true;
sku.getRange(`F7:F${end}`).format.wrapText=true;
for(let i=0;i<data.records.length;i++) {
  const v=data.records[i].values;
  const label=data.forms.find(x=>x[0]===v.I)[1]+' - '+(v.G?.startsWith('Descriere lipsă')?v.F:v.G);
  if(label.length>47)sku.getRange(`A${i+7}:U${i+7}`).format.rowHeight=34;
}
sku.getRange(`L7:R${end}`).format.fill=amber;
sku.getRange(`S7:S${end}`).conditionalFormats.add('cellIs',{operator:'notEqual',formula:'"Cod valid"',format:{fill:'#FCE3E0',font:{color:'#A12424'}}});
sku.getRange(`F7:F${end}`).conditionalFormats.add('beginsWith',{text:'Descriere lipsă',format:{fill:amber,font:{color:'#875500'}}});
sku.getRange(`D7:D${end}`).dataValidation={rule:{type:'list',formula1:formKeys}};
sku.getRange(`E7:E${end}`).dataValidation={rule:{type:'list',formula1:glazeKeys}};
sku.freezePanes.freezeRows(6);
sku.freezePanes.freezeColumns(2);
sku.tabColor=navy;

// Full source column structure is retained for the dedicated NOMEXP output.
const originalCols=Array.from({length:26},(_,i)=>String.fromCharCode(65+i)).concat(['AA','AB','AC','AD','AE','AF']);
fmt(exp,`A1:AF${data.records.length+1}`);
exp.getRange('A1:AF1').values=[originalCols.map(c=>data.original.headers[c])];
const map=['A','P','B','B','Q','E','F','H','D','B','L','M','N','O','J','R','Q',null,'B','P','C','B',null,'E',null,null,null,'K','L','I','G','E'];
const expForms=data.records.map((rec,idx)=>{
  const r=idx+7;
  return map.map(c=>c?`=IF('SKU_5900'!${c}${r}="","",'SKU_5900'!${c}${r})`:null);
});
exp.getRange(`A2:AF${data.records.length+1}`).formulas=expForms;
table(exp,`A1:AF${data.records.length+1}`,'Nomexp5900');
header(exp,'A1:AF1');
for(const c of originalCols)col(exp,c,['C','D','G','J','S','V','AF'].includes(c)?48:17);
col(exp,'A',30);
for(const c of ['C','D','G','J','S','V'])exp.getRange(`${c}2:${c}${data.records.length+1}`).format.wrapText=true;
for(let i=0;i<data.records.length;i++){
  const v=data.records[i].values;
  const label=data.forms.find(x=>x[0]===v.I)[1]+' - '+(v.G?.startsWith('Descriere lipsă')?v.F:v.G);
  if(label.length>47)exp.getRange(`A${i+2}:AF${i+2}`).format.rowHeight=34;
}
exp.getRange(`A2:A${data.records.length+1}`).setNumberFormat('@');
exp.getRange(`F2:F${data.records.length+1}`).setNumberFormat('@');
exp.getRange(`K2:N${data.records.length+1}`).setNumberFormat('0.0000');
exp.getRange(`U2:U${data.records.length+1}`).setNumberFormat('@');
exp.freezePanes.freezeRows(1);
exp.freezePanes.freezeColumns(1);

fmt(original,`A1:AG${data.original.rows.length+6}`);
title(original,'Înregistrări originale 5900','Sursa: NOMEXP_v9_ultimate.(2).xlsx • NOMEXP02, rândurile 3216–3469 și 3503–3615. Toate cele 367 de rânduri sunt păstrate.');
original.getRange('A4').values=[['Valorile #N/A de mai jos sunt erori din fișierul original, păstrate ca text pentru comparație.']];
original.getRange('A6:AG6').values=[['Rând sursă',...originalCols.map(c=>data.original.headers[c])]];
original.getRange(`A7:AG${data.original.rows.length+6}`).values=data.original.rows.map(r=>[r.source_row,...originalCols.map(c=>literal(r.values[c]))]);
table(original,`A6:AG${data.original.rows.length+6}`,'Original5900');
header(original,'A6:AG6');
for(let i=0;i<33;i++)original.getRangeByIndexes(0,i,1,1).format.columnWidth=18;
col(original,'B',30);
for(const c of ['D','E','H','K','T','W','AG'])col(original,c,48);
for(const c of ['D','E','H','K','T','W','AG'])original.getRange(`${c}7:${c}${data.original.rows.length+6}`).format.wrapText=true;
data.original.rows.forEach((r,i)=>{if(String(r.values.C).length>47)original.getRange(`A${i+7}:AG${i+7}`).format.rowHeight=34;});
original.freezePanes.freezeRows(6);

const logStart=21,logEnd=logStart+data.changes.length-1;
fmt(log,`A1:E${logEnd}`);
title(log,'Corecții și verificări','Domeniu: exclusiv SKU cu prefixul 5900. Fișierul original a rămas neschimbat.');
log.getRange('A5:C5').values=[['Verificare','Rezultat','Explicație']];
log.getRange('A6:C17').values=[
  ['Înregistrări originale',367,'Toate sunt păstrate în Original_5900.'],
  ['SKU în catalog',null,'Un singur rând pentru fiecare SKU corectat.'],
  ['Coduri de verificat',null,'Control de format, unicitate și coerență cu modelul formei.'],
  ['SKU cu spații corectate',18,'Spațiile din codurile de glazură au fost eliminate.'],
  ['Modele corectate',3,'NOMEXP02: rândurile 3307–3309, 3070 → 2345.'],
  ['Dublură consolidată',1,'Rândurile 3284 și 3520 sunt identice după normalizare.'],
  ['Număr de piese completat',367,'Din definițiile explicite SET n din cataloage.'],
  ['Descriere glazură lipsă',null,'324L: descrierea se completează în Cataloage.'],
  ['Prețuri lipsă',null,'Lipsesc pentru toate SKU în sursa inițială.'],
  ['Costuri lipsă',null,'Lipsesc pentru toate SKU în sursa inițială.'],
  ['Greutăți nete lipsă',null,'Se păstrează unitatea sistemului sursă; nu s-au presupus conversii.'],
  ['Greutăți brute lipsă',null,'Nu se deduc fără o regulă confirmată.']
];
log.getRange('B7').formulas=[[`=COUNTA('SKU_5900'!A7:A${end})`]];
log.getRange('B8').formulas=[[`=COUNTIF('SKU_5900'!S7:S${end},"<>Cod valid")`]];
log.getRange('B13').formulas=[[`=COUNTIF('SKU_5900'!F7:F${end},"Descriere lipsă: 324L")`]];
log.getRange('B14').formulas=[[`=COUNTBLANK('SKU_5900'!L7:L${end})`]];
log.getRange('B15').formulas=[[`=COUNTBLANK('SKU_5900'!M7:M${end})`]];
log.getRange('B16').formulas=[[`=COUNTBLANK('SKU_5900'!N7:N${end})`]];
log.getRange('B17').formulas=[[`=COUNTBLANK('SKU_5900'!O7:O${end})`]];
log.getRange('A19').values=[['Denumirile se calculează din forma setului și glazură. NOMEXP02_5900 preia modificările din SKU_5900. Câmpurile fără date rămân goale.']];
log.getRange('A20:E20').values=[['Celulă originală','Valoare originală','Valoare corectată','Motiv','Sursă / dovadă']];
log.getRange(`A21:E${logEnd}`).values=data.changes.map(r=>r.map(literal));
table(log,`A20:E${logEnd}`,'JurnalCorectii5900');
header(log,'A5:C5');header(log,'A20:E20');
[['A',37],['B',35],['C',93],['D',94],['E',105]].forEach(([c,w])=>col(log,c,w));
log.getRange(`B6:B17`).setNumberFormat('0');
log.getRange('B6:B17').format.horizontalAlignment='center';
log.getRange('A6:C17').format.rowHeight=25;
log.getRange('A19').format.font={name:'Arial',size:10,color:muted};
log.freezePanes.freezeRows(20);

// Meaningful sensitivity checks, restored before the final recalculation.
const beforePrice=sku.getRange('L7').values;
sku.getRange('L7').values=[[12.34]];
if(Math.abs(exp.getRange('K2').values[0][0]-12.34)>1e-9)throw Error('Prețul nu se propagă în export');
sku.getRange('L7').values=beforePrice;
const oldDescription=cat.getRange(`H${unknownColorIndex}`).values;
cat.getRange(`H${unknownColorIndex}`).values=[['Test descriere']];
const probe=data.records.findIndex(r=>r.values.F==='324L')+7;
if(sku.getRange(`F${probe}`).values[0][0]!=='Test descriere')throw Error('Descrierea nu se propagă');
cat.getRange(`H${unknownColorIndex}`).values=oldDescription;

wb.recalculate();
const expectedSku=data.records.map(r=>r.values.A);
const actualSku=sku.getRange(`A7:A${end}`).values.flat();
if(JSON.stringify(expectedSku)!==JSON.stringify(actualSku))throw Error('Lista SKU nu coincide cu verificarea independentă');
const statuses=sku.getRange(`S7:S${end}`).values.flat();
if(statuses.some(x=>x!=='Cod valid'))throw Error('Validare SKU nereușită '+JSON.stringify([...new Set(statuses)]));
const checks=log.getRange('A6:C17').values;
if(sku.getRange(`F7:F${end}`).values.flat().filter(x=>x==='Descriere lipsă: 324L').length!==14)throw Error('Descrierile lipsă nu sunt semnalate corect');
if(log.getRange('B13').values[0][0]!==14)throw Error('Numărul descrierilor lipsă este incorect');
console.log('CHECKS',JSON.stringify(checks));
console.log((await wb.inspect({kind:'region',sheetId:'SKU_5900',range:'A7:G10',maxChars:2500,tableMaxRows:4,tableMaxCols:7})).ndjson);
await fs.writeFile(`${base}/build_checks.json`,JSON.stringify({stats:data.stats,checks,unique:new Set(actualSku).size,sensitivity_tests:'price and glaze description propagated; inputs restored'},null,2));
for(const [sheetName,range,file] of [
  ['SKU_5900','A1:G12','preview_sku.png'],
  ['SKU_5900',`A${probe-1}:G${probe+2}`,'preview_unknown.png'],
  ['NOMEXP02_5900','A1:J7','preview_export.png'],
  ['Cataloage','A1:E13','preview_catalog.png'],
  ['Corectii','A1:C17','preview_corrections.png'],
  ['Original_5900','A1:I10','preview_original.png'],
]) {
  const b=await wb.render({sheetName,range,scale:1.5,format:'png'});
  await fs.writeFile(`${base}/${file}`,new Uint8Array(await b.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);
await file.save(`${out}/NOMEXP_SKU_5900_corectat.xlsx`);
console.log('EXPORTED',`${out}/NOMEXP_SKU_5900_corectat.xlsx`);
