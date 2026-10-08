import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='C:/Users/User/.codex/visualizations/2026/10/08/01a11add-716d-7ea3-88e3-6c44068f5a42';
const data=JSON.parse(await fs.readFile(root+'/work/excel-data.json','utf8'));
data.releases['frappe/erpnext']={version:'v16.50.0 și v15.122.0',url:'https://github.com/frappe/erpnext/releases/tag/v16.50.0'};
data.releases['frappe/hrms']={version:'v16.50.0 și v15.64.3',url:'https://github.com/frappe/hrms/releases'};
data.sources.push(...[
 ['E15','ERPNext release v16.50.0','https://github.com/frappe/erpnext/releases/tag/v16.50.0'],
 ['E16','ERPNext releases inclusiv v15.122.0','https://github.com/frappe/erpnext/releases'],
 ['E17','Frappe HR releases v16.50.0 și v15.64.3','https://github.com/frappe/hrms/releases'],
 ['B11','BookStack release v26.09.1','https://api.github.com/repos/BookStackApp/BookStack/releases/latest']
].map(([id,titlu,url])=>({id,titlu,url,grup:'Versiuni verificate',utilizare:'Versiuni identificate la 08.10.2026; fără test de instalare',status:'Consultat web'})));
data.rows[0][1]='HR și competențe';
const order=['Manualul și controlul documentelor','Audituri și îmbunătățire','HR și competențe','Rezultate și Six Sigma','Integrare și exploatare'];
data.rows.sort((a,b)=>order.indexOf(a[1])-order.indexOf(b[1]));
for(const row of data.rows)if(row[2]==='Componentă HR în ecosistem')row[10]='N';
const wb=Workbook.create();
const main=wb.worksheets.add('Comparatie');
const modules=wb.worksheets.add('Module OCA');
const versions=wb.worksheets.add('Versiuni si surse');
const labels={N:'✓ Da',C:'◐ Parțial',A:'◐ Parțial',D:'✕ Nu',U:'? Neverificat','—':'— N/A'};
function status(x){if(x.includes('U'))return labels.U;if(x==='D')return labels.D;if(x.includes('/')||x==='A'||x==='C')return labels.C;return labels[x]||labels.U;}
const color={'✓ Da':['#E8F3EA','#235B34'],'◐ Parțial':['#FFF1CC','#785414'],'✕ Nu':['#F9E4E3','#912D2D'],'? Neverificat':['#E9EDF2','#4F5D70'],'— N/A':['#F4F5F7','#707780']};
function base(sh,range){sh.showGridLines=false;sh.getRange(range).format.font={name:'Arial',size:10,color:'#182737'};sh.getRange(range).format.verticalAlignment='center';sh.getRange(range).format.rowHeight=28;sh.getRange(range).format.wrapText=true;sh.tabColor='#264763';}
function head(sh,range){sh.getRange(range).format={fill:'#264763',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true};}
function title(sh,text,last){sh.getRange('A2').values=[[text]];sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#182737'};sh.getRange('A2').format.wrapText=false;sh.getRange('A2:'+last+'2').format.rowHeight=30;sh.getRange('A2:'+last+'2').format.borders={bottom:{style:'thin',color:'#9DACBA'}};}
function colors(sh,range){const rg=sh.getRange(range);rg.format.horizontalAlignment='center';for(const [text,[fill,fg]] of Object.entries(color))rg.conditionalFormats.add('containsText',{text,format:{fill,font:{color:fg,bold:true}}});}
const vErp=data.releases['frappe/erpnext'].version,vHr=data.releases['frappe/hrms'].version;
const shortv=x=>x.startsWith('Versiune')?'Neconfirmată':x.replace(' și ','\nși ');
base(main,'A1:N'+(data.rows.length+10));title(main,'Comparație funcțională QMS pentru EVA și iDempiere','K');
main.getRange('A3').values=[['Analiză documentară la 08.10.2026. Bifele nu reprezintă teste în mediul EVA.']];main.getRange('A3').format.wrapText=false;
main.getRange('C4:G4').values=[['✓ Da','◐ Parțial','✕ Nu','? Neverificat','— N/A']];colors(main,'C4:G4');
main.getRange('A5').values=[['Da = funcție documentată. Parțial = configurare / modul suplimentar. Nu = necesită dezvoltare. N/A = în afara rolului.']];main.getRange('A5').format.wrapText=false;
main.getRange('A6').values=[['Modulele OCA sunt detaliate separat. EVA existentă nu include QMS-ul nativ propus în raport.']];main.getRange('A6').format.wrapText=false;
main.getRange('C8:K8').values=[['Versiune / ramură','18.0\nQMS 18.0.1.0.1',shortv(vErp),shortv(vHr),'v26.09.1','Catalog 11\n13 nevalidat','2.7','0.11.1','iDempiere 13\ncommit 1c03919']];main.getRange('C8:K8').format.rowHeight=45;main.getRange('C8:K8').format.fill='#EFF3F7';
const header=['ID','Capitol','Funcție efectivă','OCA QMS și module','ERPNext','Frappe HR','BookStack','Logilite DMS','R qcc','R SixSigma','EVA existentă'];
main.getRange('A10:K10').values=[header];head(main,'A10:K10');main.getRange('A10:K10').format.rowHeight=38;
main.getRange('M10:N10').values=[['Condiție sau limită','Surse din registru']];head(main,'M10:N10');
const rows=data.rows.map(r=>[...r.slice(0,3),...r.slice(3,11).map(status)]);
main.getRange(`A11:K${10+rows.length}`).values=rows;
main.getRange(`M11:N${10+rows.length}`).values=data.rows.map(r=>[r[11],r[12]]);
main.getRange(`A11:K${10+rows.length}`).format.rowHeight=42;
main.getRange(`B11:C${10+rows.length}`).format.horizontalAlignment='left';
colors(main,`D11:K${10+rows.length}`);
main.tables.add(`A10:K${10+rows.length}`,true,'ComparatieQMS');
main.freezePanes.freezeRows(10);main.freezePanes.freezeColumns(3);
for(const [col,width] of Object.entries({A:7,B:25,C:43,D:18,E:18,F:18,G:18,H:18,I:18,J:18,K:18,L:3,M:82,N:38}))main.getRange(`${col}1:${col}${10+rows.length}`).format.columnWidth=width;
let prev='';for(let i=0;i<data.rows.length;i++){if(prev!==data.rows[i][1]){main.getRange(`A${11+i}:K${11+i}`).format.borders={top:{style:'medium',color:'#A7B6C5'}};main.getRange(`B${11+i}`).format.font.bold=true;}prev=data.rows[i][1];}

base(modules,'A1:N28');title(modules,'Module OCA și funcțiile pe care le adaugă','K');
modules.getRange('A3').values=[['Ramura 18.0. Coloanele reprezintă module distincte; denumirile tehnice și versiunile sunt în foaia de referință.']];modules.getRange('A3').format.wrapText=false;
modules.getRange('A4').values=[['✓ Da = funcție principală documentată; ◐ Parțial = inclusă prin dependențe; ? = nu este demonstrată în sursa modulului.']];modules.getRange('A4').format.wrapText=false;
const names=['QMS','Manual','Neconformități','Audit','HR / departament','Aprobări pagini','Eficacitate','Review','Produs'];
modules.getRange('A7:K7').values=[['Capitol','Funcție',...names]];head(modules,'A7:K7');modules.getRange('A7:K7').format.rowHeight=45;
modules.getRange('C6:K6').values=[data.modules.map(m=>m.version)];modules.getRange('C6:K6').format.rowHeight=40;
const moduleRows=data.modules.map((m,i)=>{let state=Array(9).fill('? Neverificat');state[i]='✓ Da';if([1,3,7].includes(i))state[0]='◐ Parțial';return [i===4?'HR':i===5||i===1?'Documente':'QMS',m.role,...state];});
moduleRows.push(['Integrare','Conector gata făcut pentru AMN_Employee',...Array(9).fill('? Neverificat')]);
moduleRows.push(['Platformă','Rulează direct în iDempiere',...Array(9).fill('✕ Nu')]);
modules.getRange('A8:K18').values=moduleRows;modules.getRange('A8:K18').format.rowHeight=42;colors(modules,'C8:K18');
modules.getRange('M7:N7').values=[['Identificator modul','Sursă']];head(modules,'M7:N7');modules.getRange('M8:N16').values=data.modules.map(m=>[m.name,m.id]);
modules.getRange('A21').values=[['Notă: un modul OCA poate avea dependențe. Matricea identifică responsabilitatea sa principală, fără a atribui funcții nedocumentate.']];modules.getRange('A21').format.wrapText=false;
for(const [c,w] of Object.entries({A:16,B:44,C:20,D:20,E:20,F:20,G:20,H:20,I:20,J:20,K:20,L:3,M:48,N:14}))modules.getRange(`${c}1:${c}28`).format.columnWidth=w;
modules.tables.add('A7:K18',true,'ModuleOCA');modules.freezePanes.freezeRows(7);modules.freezePanes.freezeColumns(2);

const catalog=[
 ['OCA Management System','18.0; QMS 18.0.1.0.1','Ramură și manifest','AGPL-3 pentru QMS','QMS extern; integrare EVA de dezvoltat','O01 O11','https://github.com/OCA/management-system/tree/18.0'],
 ['Odoo Community','Ramura 18.0','Ramură analizată','LGPL-3; modulele pot diferi','Platformă necesară pentru OCA','O12','https://github.com/odoo/odoo/tree/18.0'],
 ['ERPNext',vErp,'Release găsit; documentație generală','GPL-3','Nu este o instalare testată în EVA','E01',data.releases['frappe/erpnext'].url],
 ['Frappe HR',vHr,'Release găsit; documentație generală','GPL-3','Modul separat de ERPNext; sincronizare HR necesară','E07',data.releases['frappe/hrms'].url],
 ['BookStack','v26.09.1','Release găsit','MIT','Manual și proceduri; aprobări QMS externe','B09','https://github.com/BookStackApp/BookStack/releases/tag/v26.09.1'],
 ['Logilite DMS','Catalog 11; README DMS-UUID-7.1','Catalog și ramură','GPL v2 declarat în catalog','Compatibilitatea cu iDempiere 13 este neconfirmată','D01 D02 D03 D04','https://github.com/logilite/logilite-DMS'],
 ['R qcc','2.7','Versiune CRAN consultată','GPL >= 2','Motor statistic, fără fluxuri QMS','R01','https://cran.r-project.org/web/packages/qcc/index.html'],
 ['R SixSigma','0.11.1','Versiune CRAN consultată','GPL >= 2','Gage R&R, capabilitate, grafice; fără HR','R02','https://cran.r-project.org/web/packages/SixSigma/index.html'],
 ['EVA și iDempiere','13; commit 1c039193e0c1626cb03fb8ca37f9980a1703fd0c','Cod privat consultat','Licența ansamblului privat neauditată','AMN HR, ZK și EVA_DocEmis existente; QMS propus nu există','P01 P02 P03 P07','https://github.com/cesiroproduction/Eva-Accounting/tree/1c039193e0c1626cb03fb8ca37f9980a1703fd0c'],
 ['iDempiere REST','README pentru 12; EVA 13 de validat','Documentație consultată','De verificat pe versiunea fixată','Transport API; fără conector QMS complet','I01 I02','https://github.com/bxservice/idempiere-rest'],
 ['plumber','Versiune exactă neconfirmată','Documentație generală','De verificat pe pachetul fixat','Serviciu HTTP R de construit','R05','https://www.rplumber.io/'],
 ['FlinkISO','Versiune exactă neconfirmată','Alternativă exclusă din selecția strictă','Licența pachetului neconfirmată','API de creare formulare personalizate plătit; nu API generic de date','F01 F02 F03','https://www.flinkiso.com/pricing/free-vs-paid.html'],
 ['FR Forge pe Hugging Face','FR-Forge-1.7B; acces nereușit','Model AI; exclus din matricea QMS','Neconfirmată','Nu este aplicație de management al calității','H01','https://huggingface.co/FahrenheitResearch/FR-Forge-1.7B'],
 ...data.modules.map(m=>[m.name,m.version,'Manifest ramura 18.0',m.license,m.role,m.id,m.url])
];
const start=9+catalog.length;
base(versions,`A1:H${start+data.sources.length+2}`);title(versions,'Versiuni identificate și surse','G');
versions.getRange('A3').values=[['Consultare 08.10.2026. Release găsit ≠ versiune instalată sau compatibilitate validată.']];versions.getRange('A3').format.wrapText=false;
versions.getRange('A5:G5').values=[['Aplicație / modul','Versiune identificată','Tipul dovezii','Licență','Rol / condiție','Referință','Cod, descărcare sau documentație']];head(versions,'A5:G5');versions.getRange('A5:G5').format.rowHeight=36;
versions.getRange(`A6:G${5+catalog.length}`).values=catalog;versions.getRange(`A6:G${5+catalog.length}`).format.rowHeight=60;versions.tables.add(`A5:G${5+catalog.length}`,true,'VersiuniQMS');
versions.getRange(`A${start-1}`).values=[['Registrul surselor raportului']];versions.getRange(`A${start-1}`).format.font.bold=true;
versions.getRange(`A${start}:G${start}`).values=[['ID','Grup','Document','Utilizare','Starea accesului','Data verificării','URL complet']];head(versions,`A${start}:G${start}`);
versions.getRange(`A${start+1}:G${start+data.sources.length}`).values=data.sources.map(s=>[s.id,s.grup,s.titlu,s.utilizare,s.status,new Date('2026-10-08T00:00:00Z'),s.url]);
versions.getRange(`F${start+1}:F${start+data.sources.length}`).setNumberFormat('dd.mm.yyyy');versions.getRange(`A${start+1}:G${start+data.sources.length}`).format.rowHeight=60;
versions.tables.add(`A${start}:G${start+data.sources.length}`,true,'SurseQMS');
for(const [c,w] of Object.entries({A:42,B:34,C:40,D:35,E:64,F:23,G:100}))versions.getRange(`${c}1:${c}${start+data.sources.length}`).format.columnWidth=w;
versions.freezePanes.freezeRows(5);versions.freezePanes.freezeColumns(1);
// Reapply explicit headers after table defaults.
head(main,'A10:K10');head(modules,'A7:K7');head(versions,'A5:G5');head(versions,`A${start}:G${start}`);
for(const sh of [main,modules,versions])for(const table of sh.tables.items)table.showFilterButton=true;
versions.getRange(`F${start+1}:F${start+data.sources.length}`).setNumberFormat('yyyy-mm-dd');
versions.getRange(`F${start+1}:F${start+data.sources.length}`).format.horizontalAlignment='center';
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Comparatie!A10:K14',include:'values',tableMaxRows:5,tableMaxCols:11,maxChars:2200})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},summary:'Verificare erori'})).ndjson);
const output=root+'/outputs/01a11add-716d-7ea3-88e3-6c44068f5a42';await fs.mkdir(output,{recursive:true});
await (await SpreadsheetFile.exportXlsx(wb)).save(output+'/Comparatie_QMS_ISO_SixSigma_EVA.xlsx');
for(const [sheetName,range,file] of [['Comparatie','A1:K15','comparatie'],['Comparatie','A30:K52','final'],['Module OCA','A6:K18','module'],['Versiuni si surse','A5:F15','versiuni'],['Versiuni si surse',`A${start}:G${start+5}`,'surse']]){try{const blob=await wb.render({sheetName,range,scale:1.3,format:'png'});await fs.writeFile(root+'/work/excel-'+file+'.png',new Uint8Array(await blob.arrayBuffer()));}catch(e){console.log('Render error',sheetName,String(e));}}
console.log(JSON.stringify({functions:rows.length,modules:data.modules.length,catalog:catalog.length,output}));
