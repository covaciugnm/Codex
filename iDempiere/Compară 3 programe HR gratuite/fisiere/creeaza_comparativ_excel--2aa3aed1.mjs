import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const base=process.cwd();
const data=JSON.parse(await fs.readFile(path.join(base,'date_comparativ_excel.json'),'utf8'));
const out=path.join(base,'outputs','01a11ac9-7ce0-7481-87a6-870f72ae1107');
await fs.mkdir(out,{recursive:true});
const wb=Workbook.create();
const main=wb.worksheets.add('Comparativ');
const products=wb.worksheets.add('Produse și versiuni');
const ev=wb.worksheets.add('Dovezi și explicații');
const guide=wb.worksheets.add('Legendă și utilizare');
const P=data.products,R=data.rows;
const color={ink:'#23394D',blue:'#DDEAF6',green:'#DCEFD9',amber:'#FFF0CA',red:'#F8DFDD',gray:'#E9ECF0',muted:'#5D6772',white:'#FFFFFF'};
function col(i){let s='';for(i++;i>0;i=Math.floor((i-1)/26))s=String.fromCharCode(65+(i-1)%26)+s;return s;}
function init(s,end,rows){
 s.showGridLines=false;
 s.getRange(`A1:${end}${rows}`).format.font={name:'Arial',size:10,color:color.ink};
 s.getRange(`A1:${end}${rows}`).format.verticalAlignment='center';
 s.getRange(`A1:${end}${rows}`).format.rowHeight=24;
 s.getRange(`A1:${end}1`).format.rowHeight=10;
}
function title(s,t,end){s.getRange('A2').values=[[t]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:color.ink};s.getRange(`A2:${end}2`).format.rowHeight=30;}
function header(s,address){s.getRange(address).format={fill:color.ink,font:{name:'Arial',size:10,bold:true,color:color.white},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',borders:{insideVertical:{style:'thin',color:color.white}}};}
function table(s,range,name){const t=s.tables.add(range,true,name);t.style='TableStyleLight1';t.showBandedColumns=false;t.showFilterButton=true;return t;}
function statusStyle(range,anchor='D7'){
 const spec=[['✓ Da',color.green,'#255E28'],['◐ Parțial',color.amber,'#815400'],['✕ Nu',color.red,'#922C25'],['? Neconfirmat',color.gray,'#56616D'],['— N/A','#FFFFFF','#9299A0']];
 for(const [v,fill,font]of spec)range.conditionalFormats.addCustom(anchor+'="'+v+'"',{fill,font:{color:font}});
}
function fitRows(s,start,rows,widths,min=38){for(let i=0;i<rows.length;i++){const lines=Math.max(...rows[i].map((v,j)=>Math.max(1,String(v??'').split('\n').reduce((n,t)=>n+Math.ceil(t.length/(widths[j]*1.12)),0))));s.getRange(`A${start+i}:${col(widths.length-1)}${start+i}`).format.rowHeight=Math.max(min,12*lines+14);}}

const last=col(P.length+2),lastRow=R.length+6;
init(main,last,lastRow);
main.tabColor=color.ink;
title(main,'Comparație iDempiere, HR și SSM/SU',last);
main.getRange('A3').values=[['✓ Da     ◐ Parțial     ✕ Nu     ? Neconfirmat     — N/A: în afara scopului modulului']];
main.getRange('A4').values=[['08.10.2026. Filtrați după capitol sau funcție. Versiunile sunt în antete; justificările sunt în foaia Dovezi și explicații.']];
main.getRange('A3:C4').format.font={name:'Arial',size:10,color:color.muted};
main.getRange('A5').values=[['ID']];
main.getRange('B5').values=[['Capitole și funcții']];
for(let j=0;j<P.length;j++)main.getCell(4,j+3).values=[[P[j].kind]];
main.getRange(`D5:${last}5`).format.wrapText=true;
main.getRange(`A5:${last}5`).format.rowHeight=33;
main.getRange(`D5:${last}5`).format.fill='#EEF2F5';
const heads=['ID funcție','Capitol','Funcție / criteriu',...P.map(p=>p.short)];
main.getRange(`A6:${last}${lastRow}`).values=[heads,...R.map(r=>[r.id,r.chapter,r.feature,...P.map(p=>data.labels[r.cells[p.id].status])])];
table(main,`A6:${last}${lastRow}`,'ComparativFunctii');
header(main,`A6:${last}6`);
main.getRange(`A6:${last}6`).format.rowHeight=84;
main.getRange(`A7:C${lastRow}`).format.wrapText=true;
main.getRange(`A7:${last}${lastRow}`).format.rowHeight=36;
main.getRange(`D7:${last}${lastRow}`).format.horizontalAlignment='center';
main.getRange(`A1:A${lastRow}`).format.columnWidth=10;
main.getRange(`B1:B${lastRow}`).format.columnWidth=27;
main.getRange(`C1:C${lastRow}`).format.columnWidth=52;
main.getRange(`D1:${last}${lastRow}`).format.columnWidth=20;
statusStyle(main.getRange(`D7:${last}${lastRow}`));
main.getRange(`D7:${last}${lastRow}`).dataValidation={rule:{type:'list',values:Object.values(data.labels)}};
let chapter='';
for(let i=0;i<R.length;i++){
 if(R[i].chapter!==chapter){
  chapter=R[i].chapter;
  main.getRange(`A${i+7}:${last}${i+7}`).format.borders={top:{style:'medium',color:'#BAC8D4'}};
  main.getRange(`A${i+7}:C${i+7}`).format.fill=color.blue;
  main.getRange(`B${i+7}`).format.font.bold=true;
 }
}
main.freezePanes.freezeRows(6);main.freezePanes.freezeColumns(3);

init(products,'J',P.length+6);
title(products,'Produse, versiuni și limite','J');
products.getRange('A3').values=[['Versiunea produsului, versiunea manualului și versiunea iDempiere testată sunt informații distincte.']];
products.getRange('A4').values=[['N/A în matrice nu înseamnă că platforma gazdă nu are funcția. Modulul este evaluat pentru aportul său propriu.']];
const productRows=P.map(p=>[p.id,p.name,p.kind,p.version,p.tech,p.licence,p.note,p.refs.join(', '),'','']);
products.getRange(`A6:J${P.length+6}`).values=[['ID','Produs / modul','Categorie','Versiune / compatibilitate identificată','Tehnologie','Licență / cost','Limită sau dependență','Surse','Documentație / versiune','Sursă suplimentară'],...productRows];
table(products,`A6:J${P.length+6}`,'ProduseVersiuni');
header(products,'A6:J6');
products.getRange('A6:J6').format.rowHeight=44;
products.getRange(`A7:H${P.length+6}`).format.wrapText=true;
const widths=[8,29,23,49,25,36,64,27,26,26];
widths.forEach((w,i)=>products.getRange(`${col(i)}1:${col(i)}${P.length+6}`).format.columnWidth=w);
fitRows(products,7,productRows,widths,46);
for(let i=0;i<P.length;i++){
 const refs=P[i].refs;
 products.getCell(i+6,8).values=[[refs[0]+' — Deschide sursa']];
 products.getCell(i+6,9).values=[[refs[Math.min(1,refs.length-1)]+' — Deschide sursa']];
}
products.getRange(`I7:J${P.length+6}`).format.font.color='#176AB1';
products.freezePanes.freezeRows(6);products.freezePanes.freezeColumns(2);

const evidence=data.evidence;
init(ev,'I',evidence.length+6);
title(ev,'Dovezi și explicații pentru marcaje','I');
ev.getRange('A3').values=[['Filtrați după ID-ul funcției și produs. „Da” documentat sau declarat nu înseamnă test executat în instalarea firmei.']];
ev.getRange('A4').values=[['Sursele sunt cele consultate pentru raportul din 08.10.2026. Marcajele N/A sunt explicate prin categoria și scopul produsului.']];
ev.getRange(`A6:I${evidence.length+6}`).values=[['ID funcție','Funcție / criteriu','Produs / modul','Statut','Explicație și limită','Tipul dovezii','ID surse','URL-uri oficiale','Precizare asupra criteriului'],...evidence];
table(ev,`A6:I${evidence.length+6}`,'DoveziFunctii');
header(ev,'A6:I6');
ev.getRange('A6:I6').format.rowHeight=40;
ev.getRange(`A7:I${evidence.length+6}`).format.wrapText=true;
const ew=[10,47,31,20,75,25,29,94,63];
ew.forEach((w,i)=>ev.getRange(`${col(i)}1:${col(i)}${evidence.length+6}`).format.columnWidth=w);
fitRows(ev,7,evidence,ew,40);
statusStyle(ev.getRange(`D7:D${evidence.length+6}`));
ev.freezePanes.freezeRows(6);ev.freezePanes.freezeColumns(1);

init(guide,'C',24);
title(guide,'Cum se citește comparația','C');
guide.getRange('A4:C15').values=[
 ['Marcaj / regulă','Semnificație','Consecință pentru evaluare'],
 ['✓ Da','Funcția este documentată sau declarată pentru produsul / modulul indicat.','Tipul dovezii este indicat separat. Nu reprezintă testare în producție.'],
 ['◐ Parțial','Acoperire limitată, componentă de flux sau dependență explicită.','Consultați explicația: pregătirea payroll nu este motor salarial complet.'],
 ['✕ Nu','Criteriul este explicit neîndeplinit sau funcția este atribuită unei extensii, nu nucleului standard.','Lipsa unei pagini ori a unui răspuns nu este folosită singură pentru „Nu”.'],
 ['? Neconfirmat','Dovezile consultate nu stabilesc acoperirea.','Cereți demonstrație, documentație sau test. Nu înseamnă lipsă.'],
 ['— N/A','În afara scopului individual al modulului pentru această comparație.','Un raport payroll nu moștenește automat toate funcțiile ERP-ului gazdă.'],
 ['Versiuni','Numere identificate în sursele cercetării la 08.10.2026.','Manualele pot fi pentru alte ramuri. Antetul nu garantează fiecare funcție în fiecare build.'],
 ['SSM și România','Instruirea generică, șabloanele și semnarea nu certifică singure conformitatea integrală.','Se verifică documentele și circuitul aplicabil firmei.'],
 ['Surse','Foaia Dovezi și explicații păstrează raționamentul, tipul dovezii și URL-urile.','Copiile locale și stările descărcărilor se află în biblioteca raportului.'],
 ['Filtrare','Folosiți săgețile din antet pentru capitol, funcție sau statutul unui produs.','Primele trei coloane și antetul rămân fixe când derulați matricea.'],
 ['Actualizare','Lista de statut permite schimbarea marcajelor după o nouă verificare.','Actualizați și explicația, sursa și versiunea. Excelul este un instantaneu, fără actualizare web automată.'],
 ['Acoperire',''+R.length+' criterii în '+data.chapters.length+' capitole și '+P.length+' produse / module.','Nu sunt atribuite procese operaționale doar pentru că există tabele sau clase generate.']
 ];
guide.getRange('A1:A24').format.columnWidth=25;
guide.getRange('B1:B24').format.columnWidth=81;
guide.getRange('C1:C24').format.columnWidth=84;
header(guide,'A4:C4');
guide.getRange('A4:C4').format.rowHeight=34;
guide.getRange('A5:C15').format.wrapText=true;
guide.getRange('A5:C15').format.rowHeight=44;
statusStyle(guide.getRange('A5:A9'),'A5');
guide.tabColor='#A0A8AF';

wb.recalculate();
const inspect=await wb.inspect({kind:'table',range:'Comparativ!A6:H12',include:'values,formulas',tableMaxRows:7,tableMaxCols:8,maxChars:2000});
await fs.writeFile(path.join(out,'inspectie.jsonl'),inspect.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1500});
await fs.writeFile(path.join(out,'verificare_formule.jsonl'),errors.ndjson);
const file=await SpreadsheetFile.exportXlsx(wb);
const target=path.join(out,'Comparativ_iDempiere_HR_SSM_SU_2026-10-08.xlsx');
await file.save(target);
for(const [sheet,range,filename] of [['Comparativ','A1:H15','matrice.png'],['Comparativ','H5:Q15','module.png'],['Produse și versiuni','A1:G10','produse.png'],['Produse și versiuni','H6:J12','linkuri.png'],['Dovezi și explicații','A1:F11','dovezi.png'],['Legendă și utilizare','A1:C15','legenda.png']]){
 try{
  const im=await wb.render({sheetName:sheet,range,scale:1.2,format:'png'});
  await fs.writeFile(path.join(out,filename),new Uint8Array(await im.arrayBuffer()));
 }catch(err){console.log('Randare '+sheet+': '+err.message);throw err;}
}
console.log(JSON.stringify({file:target,products:P.length,functions:R.length,chapters:data.chapters.length,evidence:evidence.length,formulaCheck:errors.ndjson}));
