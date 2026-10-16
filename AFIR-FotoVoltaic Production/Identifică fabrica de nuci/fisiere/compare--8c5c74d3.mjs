import fs from 'node:fs/promises';
import {Workbook,FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='C:/Users/User/.codex/visualizations/2026/10/16/01a144d6-5235-7b32-a0ad-d075f50f44b4/nuci';
const d=JSON.parse(await fs.readFile(dir+'/data.json','utf8'));
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(dir+'/before_edit.xlsx'));
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const ref=(sheet,cell)=>"'"+sheet+"'!"+cell;
const models=d.catalog.map(r=>({id:r[0],name:r[2],unit:r[2].startsWith('Uscător')?'kg/24 h':'kg/h',note:r[11]||''}));
models.push(
{id:49,name:'Curățare nuci verzi / ofertă 500 kg/h (descriere 500–600)',unit:'kg/h'},
{id:50,name:'Linie completă combinată / 200 kg/h / nuci, alune, migdale',unit:'kg/h'},
{id:51,name:'Calibrator 4 fracții / 300 kg/h / ofertă 1,1 kW',unit:'kg/h'},
{id:52,name:'Separator cromatic 3S / ofertă 4 t/h',unit:'kg/h'});
const model=id=>models.find(m=>m.id===id);
const offers=[
{name:'82 16.04.2026 - 200',title:'Nr. 82 / 16.04.2026 / varianta 200 kg/h',declared:85100,source:d.old[0][7],
rows:[
[49,1,500,8000,8000,2.2,'p. 1; 500 kg/h tabel, 500–600 detalii, 700 descriere.'],
[9,1,2000,16000,16000,14,'p. 3; uscător 2 t/24 h.'],
[13,1,2000,6700,6700,null,'Puterea nu este precizată.'],
[51,2,300,8600,17200,1.1,'p. 6; 17.200 EUR pentru 2 buc.; preț unitar derivat.'],
[6,1,300,4300,4300,2.2,'p. 6; utilaj pentru alune.'],
[50,1,200,32900,32900,null,'Puterea întregii linii lipsește; puterile componentelor nu sunt un total complet.']
],line:[50],dryer:[9]},
{name:'82 16.04.2026 - 400',title:'Nr. 82 / 16.04.2026 / fișier 400 kg/h; linie descrisă 200 kg/h',declared:null,source:d.old[6][7],
rows:[
[5,1,1000,29000,29000,3.7,'p. 1.'],
[10,1,4000,19200,19200,14,'p. 4–5; uscător 4 t/24 h.'],
[14,1,4000,8600,8600,null,'4 t/h în tabel; puterea lipsește.'],
[51,2,300,8600,17200,1.1,'p. 6; 17.200 EUR pentru 2 buc.; preț unitar derivat.'],
[6,1,300,4300,4300,2.2,'p. 7; utilaj pentru alune.'],
[42,1,200,28600,28600,null,'Alternativa 1: linie numai nuci, 200 kg/h.'],
[50,1,200,32900,32900,null,'Alternativa 2: linie combinată, 200 kg/h.']
],line:[42,50],dryer:[10]},
{name:'179 11.10.2026 - 400',title:'Nr. 179 / 11.10.2026 / două linii × 200 kg/h',declared:320400,source:d.latest[0][10],
rows:[
[5,1,1000,34000,34000,3.7,'p. 1; NERI/MOTOVARIO conform emailului.'],
[10,2,4000,22400,44800,14,'p. 4; necesită bilanț termic și putere totală confirmată.'],
[14,1,4000,9800,9800,null,'p. 3: descriere 2 t/h, tabel 4 t/h.'],
[18,2,300,8500,17000,4.5,'p. 5: denumire/SKU neconcordante.'],
[17,2,500,21200,42400,2.95,'p. 6; 2 buc. în ofertă.'],
[6,1,300,4800,4800,2.2,'p. 7; utilaj pentru alune.'],
[50,2,200,44900,95800,null,'p. 1: 44.900 × 2 = 89.800, dar total declarat 95.800 EUR.'],
[52,1,4000,56000,56000,2,'p. 15–16: 4 t/h; catalogul indică 400 kg/h, de confirmat.'],
[35,2,null,7900,15800,0.55,'p. 16; capacitate kg/h nedeclarată; bandă 4 m.']
],line:[50],dryer:[10]}
];
function base(name,title,last,widths){
 const s=w.worksheets.add(name);s.showGridLines=false;s.tabColor='#344E41';
 s.getRange('A1:'+last+'90').format.font={name:'Arial',size:10,color:'#222222'};
 s.getRange('A2:'+(last==='G'?'G':'J')+'2').merge();s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:'#344E41'};s.getRange('A2').format.rowHeight=28;
 widths.forEach((v,i)=>s.getRange(col(i)+':'+col(i)).format.columnWidth=v);
 return s;
}
function note(s,row,text,last){const end=last==='G'?'G':'J';s.getRange('A'+row+':'+end+row).merge();s.getRange('A'+row).values=[[text]];s.getRange('A'+row).format={wrapText:true,rowHeight:30,font:{name:'Arial',size:10,color:'#555555'}};}
function header(s,address){s.getRange(address).format={fill:'#344E41',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:44,horizontalAlignment:'center',verticalAlignment:'center'};}
function body(s,address){s.getRange(address).format={wrapText:true,verticalAlignment:'center',rowHeight:44};}
for(const o of offers){
 const s=base(o.name,o.title,'N',[65,14,12,12,18,20,20,22,22,20,19,20,76,70]);o.sheet=s;
 note(s,3,'Prețuri în EUR fără TVA. Cantitățile de 1 buc. din ofertele 82 sunt presupuse unde tabelul nu indică numărul.','N');
 note(s,4,'kW = putere declarată, nu consum kWh. Capacitățile se însumează numai pentru utilaje identice în paralel.','N');
 if(o===offers[1]){
 s.getRange('A5').values=[['Linie inclusă în total: 1 = numai nuci, 2 = combinată']];s.getRange('C5').values=[[2]];
 s.getRange('C5').dataValidation={rule:{type:'list',values:['1','2']}};s.getRange('C5').format.fill='#FFF2CC';
 note(s,6,'O singură alternativă este inclusă. Selecția se propagă în matrice și în totaluri; prețurile ambelor variante rămân vizibile.','N');
 }else note(s,6,o===offers[2]?'Panourile de comandă sunt excluse. Totalul declarat diferă cu 6.000 EUR de calculul cantitate × preț.':'Oferta istorică necesită reconfirmare. Nu se presupune că include automatizarea cerută ulterior.','N');
 const headers=['Echipament / versiune','Unitate capacitate','Buc. ofertate','Inclus în total (1/0)','Capacitate / utilaj','Capacitate × buc. incluse','Preț unitar EUR','Preț calculat EUR','Preț declarat rând EUR','Diferență EUR','Putere / utilaj kW','Putere × buc. kW','Precizări tehnice / pagină','Document sursă'];
 s.getRange('A7:N7').values=[headers];header(s,'A7:N7');
 o.rowMap={};
 o.rows.forEach((r,i)=>{
 const n=8+i;const m=model(r[0]);o.rowMap[r[0]]=n;
 s.getRange('A'+n+':N'+n).values=[[m.name,m.unit,r[1],1,r[2]??'ND',null,r[3],null,r[4],null,r[5]??'ND',null,r[6],o.source]];
 if(o===offers[1]&&[42,50].includes(r[0]))s.getRange('D'+n).formulas=[['=IF($C$5='+(r[0]===42?1:2)+',1,0)']];
 s.getRange('F'+n).formulas=[['=IF(D'+n+'=0,0,IF(ISNUMBER(E'+n+'),C'+n+'*D'+n+'*E'+n+',"ND"))']];
 s.getRange('H'+n).formulas=[['=C'+n+'*D'+n+'*G'+n]];
 s.getRange('J'+n).formulas=[['=IF(D'+n+'=0,0,I'+n+'-H'+n+')']];
 s.getRange('L'+n).formulas=[['=IF(D'+n+'=0,0,IF(ISNUMBER(K'+n+'),C'+n+'*D'+n+'*K'+n+',"ND"))']];
 });
 const end=7+o.rows.length;
 body(s,'A8:N'+end);s.getRange('G8:J'+end).setNumberFormat('#,##0.00');s.getRange('K8:L'+end).setNumberFormat('0.00');
 s.getRange('J8:J'+end).conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4D6',font:{color:'#9C0006',bold:true}}});
 s.getRange('A22:A29').values=[['Capacitate de spargere propusă (kg/h), teoretică'],['Capacitate uscare (kg/24 h), declarată'],['Preț calculat configurație selectată (EUR fără TVA)'],['Total general declarat în ofertă (EUR fără TVA)'],['Diferență total declarat minus calculat (EUR)'],['Subtotal puteri cunoscute (kW), incomplet'],['Poziții incluse fără putere totală declarată'],['Putere totală completă configurație (kW)']];
 s.getRange('B22').formulas=[['='+o.line.map(id=>'F'+o.rowMap[id]).join('+')]];
 s.getRange('B23').formulas=[['='+o.dryer.map(id=>'F'+o.rowMap[id]).join('+')]];
 s.getRange('B24').formulas=[['=SUM(H8:H'+end+')']];
 s.getRange('B25').values=[[o.declared??'Nedeclarat']];
 s.getRange('B26').formulas=[['=IF(ISNUMBER(B25),B25-B24,"ND")']];
 s.getRange('B27').formulas=[['=SUM(L8:L'+end+')']];
 s.getRange('B28').formulas=[['=COUNTIF(L8:L'+end+',"ND")']];
 s.getRange('B29').formulas=[['=IF(B28>0,"ND",B27)']];
 s.getRange('A22:B29').format.rowHeight=25;s.getRange('A22:B29').format.font.bold=true;s.getRange('B22:B29').setNumberFormat('#,##0.00');
 note(s,31,'ND = informație nedeclarată / incompletă. Subtotalul cunoscut nu include consumatorii fără putere specificată.','N');
 note(s,32,'Capacitatea liniei întregi nu este garantată: depinde de alimentare, sortare, umiditate și funcționarea în paralel.','N');
 s.freezePanes.freezeRows(7);s.freezePanes.freezeColumns(1);
}
const matrix=base('Matrice echipamente','Toate echipamentele și versiunile - cantități, capacități, prețuri și puteri','Z',[65,14,...Array(24).fill(17)]);
note(matrix,3,'Celule goale = articol neofertat. ND = parametru nedeclarat. Cantitatea este cea inclusă în configurația selectată.','Z');
note(matrix,4,'Ofertele se compară pe versiuni distincte. Nu se însumează debitele etapelor succesive. Unitățile sunt în coloana B.','Z');
matrix.getRange('A6:A7').merge();matrix.getRange('A6').values=[['Echipament / versiune']];
matrix.getRange('B6:B7').merge();matrix.getRange('B6').values=[['Unitate capacitate']];
header(matrix,'A6:Z7');
const sub=['Buc. incluse','Capacitate / utilaj','Capacitate × buc.','Preț unitar EUR','Preț total EUR','Putere / utilaj kW','Putere totală kW','Total declarat EUR'];
// 8 requested measures: retain price discrepancy as 9th? Core has 7? quantity + capacity + total + unit price + total + power + total =7.
// Use final slot to expose the supplier's declared amount alongside calculated price.
offers.forEach((o,i)=>{
 let c=2+i*8;matrix.getRange(col(c)+'6:'+col(c+7)+'6').merge();matrix.getRange(col(c)+'6').values=[[o.title]];
 matrix.getRange(col(c)+'7:'+col(c+7)+'7').values=[sub];
});
const ordered=[...models].sort((a,b)=>{
 const rank=id=>({49:3.9,50:43.1,51:16.1,52:38.1}[id]??id);
 return rank(a.id)-rank(b.id);
});
ordered.forEach((m,i)=>{
 const n=8+i;matrix.getRange('A'+n+':B'+n).values=[[m.name,m.unit]];
 offers.forEach((o,j)=>{
  const sr=o.rowMap[m.id];if(!sr)return;
  const c=2+j*8;const q=x=>ref(o.name,x+sr);
  matrix.getRange(col(c)+n+':'+col(c+7)+n).formulas=[['='+q('C')+'*'+q('D'),'='+q('E'),'='+q('F'),'='+q('G'),'='+q('H'),'='+q('K'),'='+q('L'),'=IF('+q('D')+'=0,0,'+q('I')+')']];
 });
});
const mend=7+ordered.length;
body(matrix,'A8:Z'+mend);matrix.getRange('C8:Z'+mend).setNumberFormat('#,##0.00');matrix.getRange('C6:Z6').format.rowHeight=46;
offers.forEach((o,j)=>{
 const c=2+j*8;
 matrix.getRange(col(c)+'8:'+col(c)+mend).setNumberFormat('0');
 matrix.getRange(col(c)+'8:'+col(c+7)+mend).conditionalFormats.add('containsText',{text:'ND',format:{fill:'#FFF2CC',font:{color:'#805600'}}});
});
const foot=mend+3;const labels=['Capacitate spargere propusă (kg/h), teoretică','Capacitate uscare declarată (kg/24 h)','Preț calculat configurație (EUR fără TVA)','Total general declarat (EUR fără TVA)','Diferență declarat minus calculat (EUR)','Subtotal puteri cunoscute (kW), incomplet','Poziții incluse fără putere declarată','Putere totală completă configurație (kW)'];
labels.forEach((label,k)=>{
 matrix.getRange('A'+(foot+k)+':B'+(foot+k)).merge();matrix.getRange('A'+(foot+k)).values=[[label]];
 offers.forEach((o,j)=>{
  const c=2+j*8;matrix.getRange(col(c)+(foot+k)+':'+col(c+7)+(foot+k)).merge();
  matrix.getRange(col(c)+(foot+k)).formulas=[['='+ref(o.name,'B'+(22+k))]];
 });
});
matrix.getRange('A'+foot+':Z'+(foot+7)).format={rowHeight:25,font:{name:'Arial',size:10,bold:true},fill:'#EEF3EF'};
matrix.getRange('C'+foot+':Z'+(foot+7)).setNumberFormat('#,##0.00');
matrix.freezePanes.freezeRows(7);matrix.freezePanes.freezeColumns(2);
const prices=base('Comparativ preturi','Comparație prețuri unitare - aceleași echipamente și versiuni','G',[65,24,24,24,24,21,64]);
note(prices,3,'EUR fără TVA. Prețurile sunt istorice, nu ajustate cu inflația. O celulă goală înseamnă că modelul nu a fost ofertat.','G');
note(prices,4,'Diferența compară oferta 179 cu ultima ofertă 82 disponibilă pentru exact aceeași versiune. Configurațiile totale diferă.','G');
prices.getRange('A6:G6').values=[['Echipament / versiune','82 / 16.04.2026 / 200','82 / 16.04.2026 / 400','179 / 11.10.2026 / 400','Diferență unitară EUR','Modificare %','Observații']];
header(prices,'A6:G6');
const offered=ordered.filter(m=>offers.some(o=>o.rowMap[m.id]));
offered.forEach((m,i)=>{
 const n=7+i;prices.getRange('A'+n).values=[[m.name]];
 offers.forEach((o,j)=>{if(o.rowMap[m.id])prices.getRange(col(j+1)+n).formulas=[['='+ref(o.name,'G'+o.rowMap[m.id])]];});
 prices.getRange('E'+n).formulas=[['=IF(ISNUMBER(D'+n+'),IF(ISNUMBER(C'+n+'),D'+n+'-C'+n+',IF(ISNUMBER(B'+n+'),D'+n+'-B'+n+',"")),"")']];
 prices.getRange('F'+n).formulas=[['=IF(ISNUMBER(E'+n+'),IF(ISNUMBER(C'+n+'),IF(C'+n+'=0,"ND",E'+n+'/C'+n+'),IF(B'+n+'=0,"ND",E'+n+'/B'+n+')),"")']];
 let note='';
 if(m.id===50)note='179: preț unitar 44.900 EUR, total rând neconcordant. Variantele mai vechi nu au aceleași condiții de echipare.';
 if(m.id===52)note='4 t/h în oferta 179, 400 kg/h în catalog: nu echivalăm automat variantele.';
 if(m.id===51)note='Preț unitar 8.600 EUR derivat din lot de 2 buc. la 17.200 EUR.';
 if(m.id===14)note='Capacitate Noria neconcordantă în descriere; de confirmat.';
 prices.getRange('G'+n).values=[[note]];
});
body(prices,'A7:G'+(6+offered.length));prices.getRange('B7:E'+(6+offered.length)).setNumberFormat('#,##0.00');prices.getRange('F7:F'+(6+offered.length)).setNumberFormat('0.0%');
prices.getRange('A24:D24').values=[['Rezumat configurații',...offers.map(o=>o.name)]];header(prices,'A24:D24');
labels.forEach((label,k)=>{
 const r=25+k;prices.getRange('A'+r).values=[[label]];offers.forEach((o,j)=>prices.getRange(col(j+1)+r).formulas=[['='+ref(o.name,'B'+(22+k))]]);
});
prices.getRange('A25:D32').format.rowHeight=26;prices.getRange('B25:D32').setNumberFormat('#,##0.00');
note(prices,34,'În oferta 82 / varianta 400: alegerea liniei se face în C5 din tabul ofertei. Totalul nu include ambele alternative.','G');
prices.freezePanes.freezeRows(6);prices.freezePanes.freezeColumns(1);
w.recalculate();
// Behavioral check: selecting the basic line must reduce the old-400 total by 4,300 EUR.
const alt=offers[1].sheet;
const before=alt.getRange('B24').values[0][0];alt.getRange('C5').values=[[1]];w.recalculate();
const after=alt.getRange('B24').values[0][0];
if(prices.getRange('C27').values[0][0]!==106900||matrix.getRange('K'+(foot+2)).values[0][0]!==106900)throw new Error('Comparisons did not update');
if(before!==111200||after!==106900)throw new Error('Alternative totals '+before+' / '+after);
alt.getRange('C5').values=[[2]];w.recalculate();
const latest=offers[2].sheet;
latest.getRange('C8').values=[[2]];w.recalculate();
if(latest.getRange('B24').values[0][0]!==348400||prices.getRange('D27').values[0][0]!==348400)throw new Error('Quantity recalculation failed');
latest.getRange('C8').values=[[1]];latest.getRange('K10').values=[[1]];w.recalculate();
if(latest.getRange('B29').values[0][0]!=='ND')throw new Error('Incomplete power incorrectly totalled');
latest.getRange('K10').values=[['ND']];w.recalculate();
const totals=offers.map(o=>({name:o.name,values:o.sheet.getRange('B22:B29').values}));
console.log(JSON.stringify(totals));
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:2000})).ndjson);
for(const [name,range] of [
[offers[0].name,'A1:L14'],[offers[1].name,'A1:L15'],[offers[2].name,'A1:L17'],
['Comparativ preturi','A1:G21'],['Comparativ preturi','A24:D34'],
['Matrice echipamente','A1:J20'],['Matrice echipamente','K6:Z20'],['Matrice echipamente','A'+foot+':Z'+(foot+7)]]){
 const p=await w.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(dir+'/edit_'+name+'_'+range.replaceAll(':','-')+'.png',new Uint8Array(await p.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(w)).save(dir+'/comparison_export.xlsx');
await fs.writeFile(dir+'/comparison_meta.json',JSON.stringify({offers:offers.map(({sheet,...o})=>o),models:ordered,foot,totals,order:['Comparativ preturi','Matrice echipamente',...offers.map(o=>o.name),'Catalog echipamente','Index fise','Conditii si diferente']}));

