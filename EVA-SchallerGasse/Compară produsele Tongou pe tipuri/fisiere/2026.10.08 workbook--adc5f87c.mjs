import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.cwd(),base=path.join(root,'Acasa');
const data=JSON.parse(await fs.readFile(path.join(base,'Surse/2026.10.08 Inventar si echivalente.json'),'utf8'));
const wb=Workbook.create();
function table(name,title,subtitle,records,widths){
 const sh=wb.worksheets.add(name), keys=Object.keys(records[0]),n=records.length;
 sh.showGridLines=false;
 const all=sh.getRangeByIndexes(0,0,n+5,keys.length);all.format.font={name:'Arial',size:11,color:'#243B53'};all.format.wrapText=true;all.format.verticalAlignment='center';all.format.rowHeight=82;
 sh.getRangeByIndexes(0,0,1,Math.min(5,keys.length)).merge();sh.getCell(0,0).values=[[title]];sh.getCell(0,0).format.font={size:18,bold:true,color:'#FFFFFF'};sh.getRangeByIndexes(0,0,1,keys.length).format.fill='#243B53';sh.getRangeByIndexes(0,0,1,keys.length).format.rowHeight=38;
 sh.getRangeByIndexes(1,0,1,Math.min(5,keys.length)).merge();sh.getCell(1,0).values=[[subtitle]];sh.getRangeByIndexes(1,0,1,keys.length).format.rowHeight=55;
 sh.getRangeByIndexes(2,0,1,Math.min(5,keys.length)).merge();sh.getCell(2,0).values=[['✓ albastru: candidat condiționat · ✓ verde: marcaj vizibil · ? galben: incert · ✗ roșu: fără echivalent']];sh.getRangeByIndexes(2,0,1,keys.length).format.rowHeight=40;
 sh.getRangeByIndexes(4,0,n+1,keys.length).values=[keys,...records.map(r=>keys.map(k=>r[k]))];
 sh.tables.add(sh.getRangeByIndexes(4,0,n+1,keys.length),true,'T'+wb.worksheets.items.length).style='TableStyleLight9';
 sh.getRangeByIndexes(4,0,1,keys.length).format.fill='#243B53';sh.getRangeByIndexes(4,0,1,keys.length).format.font={bold:true,color:'#FFFFFF'};sh.getRangeByIndexes(4,0,1,keys.length).format.rowHeight=35;
 keys.forEach((k,i)=>sh.getRangeByIndexes(0,i,n+5,1).format.columnWidth=widths[i]||30);
 records.forEach((r,i)=>{
  keys.forEach((k,j)=>{let v=String(r[k]),c=sh.getCell(i+5,j);
   if(v.startsWith('✓')){c.format.font.color=name==='Inventar foto'?'#267347':'#155EAD';c.format.fill=name==='Inventar foto'?'#ECF8EF':'#EAF2FC';}
   if(v.startsWith('?')){c.format.fill='#FFF2CC';c.format.font.color='#8A5700';}
   if(v.startsWith('✗')||(k.includes('Stoc')&&r[k]===0)){c.format.fill='#FDE9E7';c.format.font.color='#B42318';}
   if(k.includes('Preț')||k==='RON cu TVA')c.setNumberFormat('#,##0.00');
  });
 });
 sh.getRangeByIndexes(3,0,1,keys.length).format.rowHeight=12;
 if(name==='Echivalente propuse'||name==='Produse candidate')sh.getRangeByIndexes(5,0,n,keys.length).format.rowHeight=145;
 sh.freezePanes.freezeRows(5);sh.freezePanes.freezeColumns(2);return sh;
}
table('Echivalente propuse','ACASA · Echivalente Tongou propuse','2026.10.08 · Preferință Zigbee, apoi Wi-Fi. Propuneri pentru validare tehnică; fără cantități de comandă.',data.equivalents,[12,40,35,29,15,48,14,22,52,90,12,16,18,52]);
table('Inventar foto','ACASA · Inventar vizual','7 fotografii · Cantitățile sunt observații per cadru. 0 = poziție dedusă, neconfirmată vizual; nu se însumează ca deviz.',data.inventory,[12,9,42,38,16,22,24,28,30,78,10]);
const protection=data.protection.map(r=>({'Temă':r[0],'Obiectiv':r[1],'Condiții și verificări':r[2]}));
protection.push({'Temă':'Surse tehnice / consultate 2026.10.08','Obiectiv':'Schneider Electric — Electrical Installation Guide','Condiții și verificări':'https://www.electrical-installation.org/enwiki/Practical_values_for_a_protective_scheme\nhttps://www.electrical-installation.org/enwiki/Additional_measure_of_protection_against_direct_contact\nhttps://www.electrical-installation.org/enwiki/RCDs_selection_in_presence_of_DC_earth_leakage_currents\nhttps://www.electrical-installation.org/enwiki/Power_quality_-_impact_of_solar_self-consumption'});
const ps=table('Protectie','ACASA · Protecții și criterii de alegere','Propunerea nu certifică instalația. Codurile și măsurătorile lipsă se completează de un electrician autorizat.',protection,[40,65,110]);ps.getRange('A6:C16').format.rowHeight=125;
table('Produse candidate','ACASA · Produse Tongou de verificat','Stoc și preț: captura catalogului 2026.10.08. Stocul nu este rezervat; fiecare SKU apare o singură dată aici.',data.products,[14,60,18,14,20,20,12,18,85,55]);
wb.recalculate();
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(base,'2026.10.08 Acasa inventar si echivalente.xlsx'));
const preview=await wb.render({sheetName:'Inventar foto',range:'A1:I10',scale:1,format:'png'});await fs.writeFile(path.join(base,'Lucru/2026.10.08 Verificare inventar.png'),new Uint8Array(await preview.arrayBuffer()));
console.log(JSON.stringify(await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!',options:{useRegex:true,maxResults:10}})));
console.log('Workbook saved');
