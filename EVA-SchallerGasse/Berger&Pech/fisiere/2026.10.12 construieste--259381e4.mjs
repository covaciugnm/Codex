import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const root = process.cwd();
const rel = '04. Firme + Executie/2026.10.12 Comparatie servicii structura';
const dest = path.join(root, rel);
const work = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(await fs.readFile(path.join(dest, '2026.10.12 Matrice comparatie.json'),'utf8'));
const tomsBase = '04. Firme + Executie/01. Verificator (Pruefingenieur)/TOMS/2026.10.02 Contract v4.1 - data actualizata';
const sources = [
 ['T1','TOMS v4.1, propunere AG transmisă','2026.10.02',tomsBase+'/2026.10.02 Werkvertrag TOMS - Entwurf AG v4.1.pdf','64c91100-89c3-4206-8e7e-988e575385b8'],
 ['T2','TOMS ANG 855, structură și asistență','2026.09.03',tomsBase+'/Beilagen/2026.10.02 ANG 855_Schallergasse 35, 1120 Wien_TWP.PDF',''],
 ['T3','TOMS ANG 839, Prüfingenieur','2026.08.20',tomsBase+'/Beilagen/2026.10.02 ANG 839_Schallergasse 35, 1120 Wien_PI.PDF',''],
 ['T4','TOMS ANG 891, Bauwerksbuch','2026.09.23',tomsBase+'/Beilagen/2026.10.02 2026-09-23 ANG 891 Bauwerksbuch (3.400 EUR netto).PDF',''],
 ['T5','TOMS Q2, chestionar semnat','2026.09.28',tomsBase+'/Beilagen/2026.10.02 2026-09-28 Fragekatalog 2 - unterzeichnet von TOMS.pdf',''],
 ['T6','TOMS, răspuns privind delimitarea serviciilor','2026.10.01',tomsBase+'/Beilagen/2026.10.01 PRIMIT TOMS 838c8bcd.txt','838c8bcd-4e2d-4e90-bc25-25355ea6da60'],
 ['T7','TOMS, refuz de preluare din lipsă de resurse','2026.10.08','08. Corespondenta/2026.10.11 Verificare zilnica/2026.10.11 PRIMIT TOMS cdd301b0.txt','cdd301b0-457e-4452-a394-6eea21256e61'],
 ['T8','Dovada trimiterii v4.1 în Eva-Mail','2026.10.05',tomsBase+'/2026.10.05 Status trimitere verificat.txt','64c91100-89c3-4206-8e7e-988e575385b8'],
 ['T9','TOMS ANG 840, BauKG istoric separat','2026.08.20','04. Firme + Executie/02. Protectia Muncii (BauKG-Koordinator)/TOMS/ANG 840_Schallergasse 35, 1120 Wien_BauKG.PDF',''],
 ['T10','TOMS Q1, versiune corectată și semnată','2026.09.23',tomsBase+'/Beilagen/2026.10.02 2026-09-23 Anlage 5 - Fragenkatalog (digitale Reinschrift) korrigiert + signiert von TOMS.pdf',''],
 ['B1','Markus BERGER, ofertă detaliată, 4 pagini','2026.08.17','00.Proiect/09. Vertraege/bmberger.at/2026.08.17/2026_08_17_Anbot_Statik_Detail.pdf','ce6905cb-0c93-4e6b-8cde-7e300dfc874c'],
 ['P1','Dr. PECH, ofertă 2026-470/AN01, 4 pagini','2026.09.17','03. Proiectare/Statik/Angebot 2026-470-AN01 2026-09-17.pdf','63cd2bcb-2160-4027-b6c8-25bb42d9ae50'],
 ['R1','REALIG, ofertă generală cu sumă presupusă','2026.03.26','00.Proiect/07. Kosten + Ausschreibung/03. Angebote (Oferte)/Angebot REALIG Gschirtz.pdf','']
];
// Validate source targets before linking the originals.
for(const s of sources) { await fs.access(path.join(root,s[3])); }
const wb = Workbook.create();
const coverage = wb.worksheets.add('1 Servicii');
const prices = wb.worksheets.add('2 Preturi');
const colors = {navy:'#24344B', light:'#EEF2F7', amber:'#FFF2CC', red:'#FDE9E7', gray:'#5F6B79', blue:'#1767A6'};
const money = '#,##0.00;[Red](#,##0.00);0.00';
const dateSerial = text => Date.parse(text.replaceAll('.','-')+'T00:00:00Z')/86400000+25569;
const widths = [120,215,340,340,290,335,175];
function lineCount(txt,w) {
  const charWidth=6.9, limit=Math.floor((w-16)/charWidth);
  return String(txt??'').split('\n').reduce((acc,p)=>{
    let lines=1,n=0;
    for(const word of p.split(' ')) {if(n+word.length+1>limit) {lines++;n=word.length;} else n+=word.length+1;}
    return acc+lines;
  },0);
}
function styleSheet(sh, rows, title, header) {
  sh.showGridLines=false; sh.tabColor=colors.navy;
  const end=7+rows.length;
  sh.getRange(`A1:G${end}`).format.font={name:'Arial',size:11,color:'#172333'};
  sh.getRange(`A1:G${end}`).format.verticalAlignment='center';
  for(let c=0;c<7;c++) sh.getRangeByIndexes(0,c,end,1).format.columnWidthPx=widths[c];
  sh.getRange('A1:G1').format.rowHeightPx=12;
  sh.getRange('A2').values=[[title]];
  sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:colors.navy};
  sh.getRange('A2:G2').format.rowHeightPx=31;
  sh.getRange('A3:G3').format.borders={bottom:{style:'thin',color:colors.navy}};
  sh.getRange('A3:G3').format.rowHeightPx=6;
  sh.getRange('A7:G7').values=[header];
  sh.getRange(`A8:G${end}`).values=rows;
  const table=sh.tables.add(`A7:G${end}`,true,sh.name==='1 Servicii'?'ComparatieServicii':'ComparatiePreturi');
  table.showBandedColumns=false; table.showFilterButton=true;
  const h=sh.getRange('A7:G7');
  h.format={fill:colors.navy,font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeightPx:48,borders:{insideVertical:{style:'thin',color:'#FFFFFF'}}};
  const body=sh.getRange(`A8:G${end}`);body.format.wrapText=true;body.format.verticalAlignment='top';
  rows.forEach((row,i)=>{
    const r=i+8,lines=Math.max(...row.map((x,c)=>lineCount(x,widths[c])));
    sh.getRange(`A${r}:G${r}`).format.rowHeightPx=Math.max(48,lines*17+16);
    sh.getRange(`A${r}:G${r}`).format.fill=i%2?'#F5F7FA':'#FFFFFF';
    sh.getRange(`A${r}`).format.font={name:'Arial',size:11,bold:true,color:colors.gray};
    if(i===0 || rows[i-1][0]!==row[0]) sh.getRange(`A${r}:G${r}`).format.borders={top:{style:'thin',color:'#CBD2DC'}};
  });
  sh.freezePanes.freezeRows(7);sh.freezePanes.freezeColumns(2);
  return end;
}
const coverageEnd=styleSheet(coverage,data.coverage,'Schallergasse 35 — servicii și discuții, 2026.10.12',data.coverageHeaders);
coverage.getRange('A4').values=[['Reper: propunerea TOMS v4.1 trimisă la 2026.10.02. Cererile AG se disting de confirmările ofertantului.']];
coverage.getRange('A5').values=[['TOMS a refuzat preluarea în prezent la 2026.10.08. Întinderea față de v4.1 este de clarificat. Nu există acceptare confirmată.']];
coverage.getRange('A4:G5').format.rowHeightPx=25;
coverage.getRange('A6').values=[['AG = beneficiar. PI = Prüfingenieur. LB = descrierea serviciilor. Confirmarea unui punct nu dovedește acceptarea întregului contract.']];
coverage.getRange('A6').format.font={name:'Arial',size:11,color:colors.gray};
coverage.getRange('A5').format.font={name:'Arial',size:11,bold:true,color:'#9C2C26'};
coverage.getRange(`C8:F${coverageEnd}`).conditionalFormats.add('containsText',{text:'EXCLUS',format:{font:{color:'#9C2C26'}}});
coverage.getRange(`C8:F${coverageEnd}`).conditionalFormats.add('containsText',{text:'Nespecificat',format:{fill:colors.amber}});

const pricesEnd=styleSheet(prices,data.prices,'Schallergasse 35 — prețuri pe servicii, 2026.10.12',data.priceHeaders);
prices.getRange('A4').values=[['TVA']];prices.getRange('C4').values=[[0.2]];prices.getRange('C4').setNumberFormat('0%');
prices.getRange('C4').format.font={name:'Arial',size:11,color:colors.blue};
prices.getRange('D4').values=[['Toate prețurile sunt în EUR. Totalurile au domenii diferite.']];
prices.getRange('A5').values=[['„Nespecificat”, „Exclus” și „Inclus în pachet” nu reprezintă zero. Suplimentele și pozițiile istorice nu intră în total.']];
prices.getRange('A4:G5').format.rowHeightPx=25;
prices.getRange(`C8:E${pricesEnd}`).setNumberFormat(money);
prices.getRange(`C8:E${pricesEnd}`).format.horizontalAlignment='right';
prices.getRange(`C8:E${pricesEnd}`).format.font={name:'Arial',size:11,color:colors.blue};
for(const col of ['C','D','E']) {
  prices.getRange(`${col}17`).formulas=[[`=SUM(${col}8:${col}16)`]];
  prices.getRange(`${col}18`).formulas=[[`=${col}17*$C$4`]];
  prices.getRange(`${col}19`).formulas=[[`=SUM(${col}17:${col}18)`]];
}
prices.getRange('C20').formulas=[['=SUM(C8:C9,C13)']];
prices.getRange('D20').formulas=[['=SUM(D8:D9,D13)']];
prices.getRange('C17:E20').format.font={name:'Arial',size:11,bold:true,color:'#172333'};
prices.getRange('A17:G19').format.fill=colors.light;
prices.getRange('A17:G17').format.borders={top:{style:'medium',color:colors.navy}};
prices.getRange('A19:G19').format.font={name:'Arial',size:11,bold:true,color:colors.navy};
prices.getRange(`C8:E${pricesEnd}`).conditionalFormats.add('containsText',{text:'Nespecificat',format:{fill:colors.amber}});
prices.getRange(`C8:E${pricesEnd}`).conditionalFormats.add('containsText',{text:'Neconfirmat',format:{fill:colors.amber}});
prices.getRange(`C8:E${pricesEnd}`).conditionalFormats.add('containsText',{text:'Fără sumă',format:{fill:colors.amber}});
const dateRow=8+data.prices.findIndex(r=>r[1].startsWith('Valabilitate'));
for(let c=2;c<=4;c++) {
  const cell=prices.getRangeByIndexes(dateRow-1,c,1,1);
  cell.values=[[dateSerial(data.prices[dateRow-8][c])]];
  cell.setNumberFormat('yyyy.mm.dd');
}

function addSources(sh,start) {
  sh.getRange(`A${start}`).values=[['Surse și originale']];
  sh.getRange(`A${start}`).format.font={name:'Arial',size:14,bold:true,color:colors.navy};
  sh.getRange(`A${start}:G${start}`).format.rowHeightPx=30;
  sources.forEach((s,i)=>{
    const r=start+1+i;
    sh.getRange(`A${r}:G${r}`).values=[[s[0],s[1],dateSerial(s[2]),'Original în arhivă',s[4]?'ID Eva-Mail':'Document anexat',s[4],'Calea în nota celulei']];
    const rg=sh.getRange(`A${r}:G${r}`);
    rg.format={font:{name:'Arial',size:11,color:colors.gray},wrapText:true,verticalAlignment:'center',rowHeightPx:58};
    sh.getRange(`C${r}`).setNumberFormat('yyyy.mm.dd');
    const abs=path.join(root,s[3]);
    sh.getRange(`G${r}`).format.font={name:'Arial',size:11,color:colors.blue};
    wb.notes.add({id:`${sh.name}:${r}`,target:{cell:{sheetName:sh.name,sheetId:sh.sheetId,address:`G${r}`}},authorId:'',createdAt:'',body:{plainText:'Sursa originală: '+abs+'\nData lizibilă: '+s[2]+(s[4]?'\nID Eva-Mail: '+s[4]:'')}});
  });
  return start+sources.length;
}
const cLast=addSources(coverage,coverageEnd+3);
const pLast=addSources(prices,pricesEnd+3);
const realigRow=pLast+2;
prices.getRange(`A${realigRow}`).values=[['REALIG: 24.000 EUR net pentru statică și verificări armare, sumă presupusă în oferta generală 2026.03.26 (R1 p2).']];
prices.getRange(`A${realigRow+1}`).values=[['Nu este ofertă fermă separată pentru același pachet. Neid/Avunduk: refuzuri de capacitate în arhivă, fără preț comparabil confirmat.']];
prices.getRange(`A${realigRow}:G${realigRow+1}`).format={font:{name:'Arial',size:11,color:colors.gray},rowHeightPx:28};
wb.recalculate();
const inspections=[];
inspections.push(await wb.inspect({kind:'table',sheetId:'2 Preturi',range:'A8:G20',include:'values,formulas',tableMaxRows:15,tableMaxCols:7,maxChars:12000}));
inspections.push(await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!|not implemented',options:{useRegex:true,maxResults:100},summary:'Formula errors'}));
await fs.writeFile(path.join(work,'2026.10.12 Inspectii.json'),JSON.stringify(inspections.map(x=>x.ndjson),null,2));
console.log(inspections.map(x=>x.ndjson).join('\n').slice(0,3000));
const totals=prices.getRange('C17:E19').values;
const expected=[[37900,45000,69300],[7580,9000,13860],[45480,54000,83160]];
if(JSON.stringify(totals)!==JSON.stringify(expected)) throw new Error('Totals mismatch: '+JSON.stringify(totals));
const output=await SpreadsheetFile.exportXlsx(wb);
await output.save(path.join(dest,'2026.10.12 Comparatie servicii si preturi structura.xlsx'));
const renderRanges=[];
for(let start=1;start<=cLast;start+=11) renderRanges.push(['1 Servicii',`A${start}:G${Math.min(cLast,start+10)}`]);
for(let start=1;start<=pLast+4;start+=11) renderRanges.push(['2 Preturi',`A${start}:G${Math.min(pLast+4,start+10)}`]);
for(let i=0;i<renderRanges.length;i++) {
  const [name,range]=renderRanges[i];
  const blob=await wb.render({sheetName:name,range,scale:1,format:'png'});
  const file=path.join(work,`2026.10.12 QA ${String(i+1).padStart(2,'0')} ${name.replace(' ','_')}.png`);
  await fs.writeFile(file,new Uint8Array(await blob.arrayBuffer()));
  console.log('RENDER '+range+' '+file);
}
await fs.writeFile(path.join(dest,'2026.10.12 Surse comparatie.json'),JSON.stringify({data:'2026.10.12',surse:sources.map(s=>({id:s[0],descriere:s[1],data:s[2],cale:s[3],email_id:s[4]})),formule:{net:'SUM(C8:C16), SUM(D8:D16), SUM(E8:E16)',TVA:'net * C4',brut:'net + TVA',subtotal:'TOMS25000+1500; BERGER13000+20000+2000'},totaluri:expected},null,2));
console.log('DONE '+data.coverage.length+' services, '+data.prices.length+' price rows.');
