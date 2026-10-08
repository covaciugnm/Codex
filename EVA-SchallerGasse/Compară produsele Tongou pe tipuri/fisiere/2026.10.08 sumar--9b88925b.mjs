import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const base=path.join(process.cwd(),'Acasa'),file=path.join(base,'2026.10.08 Acasa inventar si echivalente.xlsx');
const backup=path.join(base,'Lucru/2026.10.08 Istoric inainte de sumar.xlsx');
try{await fs.access(backup);}catch{await fs.copyFile(file,backup);}
const data=JSON.parse(await fs.readFile(path.join(base,'Surse/2026.10.08 Inventar si echivalente.json'),'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(backup));
wb.worksheets.getItem('Echivalente propuse').freezePanes.freezeRows(20);
wb.worksheets.getItem('Echivalente propuse').freezePanes.freezeColumns(2);
const sh=wb.worksheets.add('Necesar si stoc');sh.showGridLines=false;
const groups=new Map();
data.inventory.forEach((r,i)=>{
 const eligible=typeof r.Cantitate==='number'&&r.Cantitate>0&&(/^C\d+$/.test(r.Marcaj))&&['M1','M3','M4'].includes(r.Plan);
 const sku=eligible?data.equivalents[i]['SKU preferat']:r.Plan==='T'?'43074':'';
 const label=[r.Tip,r.Poli,r.Marcaj].filter(Boolean).join(' · ');
 const key=label+'|'+sku+'|'+(typeof r.Cantitate);
 if(!groups.has(key))groups.set(key,{label,sku,rows:[],qty:0,unknown:false,ids:[]});
 const g=groups.get(key);g.rows.push(i+6);g.ids.push(r.ID);if(typeof r.Cantitate==='number')g.qty+=r.Cantitate;else g.unknown=true;
});
const list=[...groups.values()],first=7,last=first+list.length-1,start=last+5;
const skus=[...new Set(list.map(g=>g.sku).filter(Boolean))];
const all=sh.getRange(`A1:G${start+skus.length+8}`);all.format.font={name:'Arial',size:11,color:'#243B53'};all.format.wrapText=true;all.format.verticalAlignment='center';all.format.rowHeight=58;
[48,14,56,14,15,65,37].forEach((w,i)=>sh.getRangeByIndexes(0,i,start+skus.length+8,1).format.columnWidth=w);
function line(r,t){sh.getRange(`A${r}:G${r}`).merge();sh.getCell(r-1,0).values=[[t]];}
function head(r,vals){sh.getRangeByIndexes(r-1,0,1,vals.length).values=[vals];const a=sh.getRangeByIndexes(r-1,0,1,vals.length);a.format.fill='#243B53';a.format.font={bold:true,color:'#FFFFFF'};a.format.rowHeight=38;}
line(1,'ACASA · Necesar și stoc Tongou');sh.getRange('A1:G1').format.fill='#243B53';sh.getCell(0,0).format.font={size:18,bold:true,color:'#FFFFFF'};
line(2,'2026.10.08 · Stoc din catalogul arhivat. Cantitățile sunt observații din fotografii, fără confirmarea eventualelor dubluri.');
line(3,'Necesarul de mai jos este un scenariu provizoriu: numai marcaje de curent citite clar + ceasul programator. Piesele ilizibile nu sunt transformate în necesar Tongou.');
line(4,'✓ albastru = candidat condiționat, NU înlocuitor validat. Stoc comun pe SKU: nu se însumează stocul repetat din primul tabel.');
sh.getRange('A5:G5').format.rowHeight=12;
head(6,['Ce am identificat','Bucăți observate','Echivalent utilizabil / candidat','Stoc SKU','SKU Tongou','Observații','Repere foto']);
list.forEach((g,i)=>{
 const row=first+i,pi=data.products.findIndex(p=>p.SKU===g.sku),p=data.products[pi];
 let note=g.sku?'✓ Utilizabil numai după verificarea nominalului, curbei, Icn și tipului RCD; vezi Echivalente propuse.':'Fără echivalent validat / identificare incompletă. Se selectează separat; nu intră în necesarul de SKU.';
 if(g.unknown)note='Cantitate de măsurat / numărat fizic. '+note;
 if(g.qty===0&&!g.unknown)note='Poziții deduse/acoperite; 0 aparate confirmate vizual. Nu înseamnă că lipsesc fizic.';
 if(g.sku==='43074')note='✓ Numai funcție de temporizare, după verificarea ieșirii și sarcinii. Stoc epuizat.';
 sh.getRange(`A${row}:G${row}`).values=[[g.label,g.unknown?'Necunoscut':g.qty,p?p.Denumire:'De identificat / fără echivalent verificat',p?p.Stoc:'—',g.sku,note,g.ids.join(', ')]];
 if(!g.unknown)sh.getRange(`B${row}`).formulas=[['=SUM('+g.rows.map(n=>`'Inventar foto'!E${n}`).join(',')+')']];
 if(p)sh.getRange(`D${row}`).formulas=[[`='Produse candidate'!G${pi+6}`]];
 sh.getRange(`C${row}`).format.fill=g.sku?'#EAF2FC':'#FFF2CC';
 if(i%2===1)sh.getRange(`A${row}:B${row}`).format.fill='#F0F4F8';
});
line(start-2,'CENTRALIZATOR MODULE TONGOU · Necesar provizoriu, după validarea tehnică');
head(start-1,['Modul Tongou','Stoc','Necesar','Diferență stoc − necesar','Din stoc*','De comandat ulterior*','Statut']);
const totals=[];
skus.forEach((sku,i)=>{
 const r=start+i,pi=data.products.findIndex(p=>p.SKU===sku),p=data.products[pi],qty=list.filter(g=>g.sku===sku).reduce((s,g)=>s+g.qty,0);
 sh.getRange(`A${r}:G${r}`).values=[[sku+'\n'+p.Denumire,p.Stoc,qty,p.Stoc-qty,Math.min(qty,p.Stoc),Math.max(0,qty-p.Stoc),'']];
 sh.getRange(`B${r}`).formulas=[[`='Produse candidate'!G${pi+6}`]];
 sh.getRange(`C${r}`).formulas=[[`=SUMIF(E${first}:E${last},"${sku}",B${first}:B${last})`]];
 sh.getRange(`D${r}`).formulas=[[`=B${r}-C${r}`]];
 sh.getRange(`E${r}`).formulas=[[`=MIN(B${r},C${r})`]];
 sh.getRange(`F${r}`).formulas=[[`=MAX(0,C${r}-B${r})`]];
 sh.getRange(`G${r}`).formulas=[[`=IF(B${r}=0,"Epuizat — după validare",IF(F${r}>0,"Parțial disponibil — după validare","Acoperit de stoc — după validare"))`]];
 sh.getRange(`A${r}:G${r}`).format.rowHeight=86;
 sh.getRange(`D${r}`).setNumberFormat('+0;-0;0');
 if(p.Stoc<qty)sh.getRange(`F${r}`).format.fill='#FDE9E7';
 totals.push({sku,stock:p.Stoc,need:qty,now:Math.min(qty,p.Stoc),later:Math.max(0,qty-p.Stoc)});
});
const end=start+skus.length;
head(end,['TOTAL SCENARIU','','','','','','']);
for(const c of ['B','C','D','E','F'])sh.getRange(`${c}${end}`).formulas=[[`=SUM(${c}${start}:${c}${end-1})`]];
line(end+2,'* „Din stoc” și „De comandat ulterior” arată disponibilitatea calculată, nu o comandă aprobată. Pentru toate SKU-urile propuse, echivalența tehnică rămâne de verificat.');
line(end+3,'Accesoriile, C80/C100, contactoarele, CT-urile, pozițiile neclare și protecțiile suplimentare SPD/AFDD nu sunt omise: sunt în primul tabel ori în fila Protecție, dar fără cantități de cumpărat inventate.');
line(end+4,'Fișe și manuale: deschide „2026.10.08 Documentatie Tongou.html” din dosarul Acasa/Documentatie Tongou.');
sh.freezePanes.freezeRows(6);sh.freezePanes.freezeColumns(1);
wb.recalculate();
await fs.writeFile(path.join(base,'Lucru/2026.10.08 Control sumar.json'),JSON.stringify({first,last,start,end,groups:list.length,totals},null,2));
console.log((await wb.inspect({kind:'table',range:`'Necesar si stoc'!A${start}:G${end}`,include:'values,formulas',tableMaxRows:15,tableMaxCols:7})).ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(file);
for(const [suffix,range] of [['sus','A1:F10'],['total',`A${start-2}:G${end+2}`]]){
 const img=await wb.render({sheetName:'Necesar si stoc',range,scale:1,format:'png'});await fs.writeFile(path.join(base,`Lucru/2026.10.08 Sumar ${suffix}.png`),new Uint8Array(await img.arrayBuffer()));
}
console.log(JSON.stringify(totals));
