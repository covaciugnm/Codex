import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=new URL('.',import.meta.url);const data=JSON.parse(await fs.readFile(new URL('workbook_data.json',root),'utf8'));
const wb=Workbook.create();const qa=new URL('qa/',root);await fs.mkdir(qa,{recursive:true});
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function base(name,title,subtitle,heads,rows,widths,start=7){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;sh.tabColor='#203E60';
 const last=col(heads.length-1),end=start+rows.length;
 sh.getRange(`A1:${last}${end}`).format.font={name:'Arial',size:10,color:'#203044'};
 sh.getRange(`A1:${last}${end}`).format.verticalAlignment='center';
 sh.getRange('A2').values=[[title]];sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#183D63'};sh.getRange('A2').format.rowHeight=28;
 sh.getRange('A3').values=[[subtitle]];sh.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#596B7F'};
 sh.getRange(`A${start}:${last}${end}`).values=[heads,...rows];
 sh.getRange(`A${start}:${last}${end}`).format.wrapText=true;
 sh.getRange(`A${start}:${last}${start}`).format={fill:'#203E60',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',rowHeight:50};
 sh.getRange(`A${start+1}:${last}${end}`).format.rowHeight=42;
 widths.forEach((w,i)=>sh.getRange(`${col(i)}1:${col(i)}${end}`).format.columnWidthPx=w);
 sh.tables.add(`A${start}:${last}${end}`,true,'T'+name.replace(/[^A-Za-z]/g,''));
 sh.freezePanes.freezeRows(start);sh.freezePanes.freezeColumns(2);
 return {sh,end,last};
}
const widths=[195,285,...data.versions.map(()=>155),230,500];
const matrix=base('Comparatie','ERP producție — funcții și module','08.10.2026 | ✓ Da / modul oficial • △ Parțial / extensie • ✕ Dezvoltare • ? Neconfirmat • — În afara scopului modulului',data.headers,data.rows,widths);
matrix.sh.getRange('A5').values=[['Versiune / reper']];
matrix.sh.getRange(`C5:${col(1+data.versions.length)}5`).values=[data.versions.map(v=>v[1])];
matrix.sh.getRange(`C5:${col(1+data.versions.length)}5`).format={wrapText:true,rowHeight:58,font:{name:'Arial',size:10,color:'#596B7F'},horizontalAlignment:'center'};
const statusRange=matrix.sh.getRange(`C8:${col(1+data.versions.length)}${matrix.end}`);statusRange.format.horizontalAlignment='center';
for(const [text,fill,color] of [['✓','#E2F0E7','#18643A'],['△','#FFF0CC','#865500'],['✕','#FCE4E2','#9C2B25'],['?','#EAF0F6','#465A70'],['—','#F6F7F9','#8894A2']])statusRange.conditionalFormats.add('containsText',{text,format:{fill,font:{color}}});
let lastCat='';for(let i=0;i<data.rows.length;i++){const cat=data.rows[i][0];if(cat!==lastCat){matrix.sh.getRange(`A${i+8}:${matrix.last}${i+8}`).format.borders={top:{style:'medium',color:'#A8BACD'}};matrix.sh.getRange(`A${i+8}:B${i+8}`).format.font={name:'Arial',size:10,bold:true,color:'#183D63'};lastCat=cat;}}
const ver=base('Versiuni si module','Versiuni, licențe și compatibilitate','Repere inspectate, nu confirmarea versiunilor instalate în producție. Licențele neconfirmate cer verificarea pachetului.', ['Aplicație / modul','Versiune găsită / reper','Licență / situație','ID sursă','Funcții și limite','URL sursă'],data.versions,[185,270,230,160,440,480]);ver.sh.getRange(`A8:F${ver.end}`).format.rowHeight=60;
const srcRows=data.sources.map(s=>[s.id,s.group,s.title,s.url,s.local?'Copie locală':s.error?'Indisponibil':'Link cod privat',s.local||s.error||s.note||'',s.sha256||'']);
const src=base('Surse','Documentații și surse descărcate','URL-ul deschide originalul; calea locală este relativă la rădăcina bibliotecii. Erorile sunt păstrate explicit.', ['ID','Categorie','Document','URL original / download','Stare','Cale locală / eroare','SHA-256 original'],srcRows,[175,160,330,570,155,540,470]);src.sh.getRange(`A8:G${src.end}`).format.rowHeight=80;
const legendRows=[['✓ Da','N','Inclus în codul/distribuția evaluată; poate necesita activare/configurare. Nu înseamnă testat în EVA.'],['✓ Modul oficial','M','Modul oficial liber separat, mai ales Tryton; nu implicit în instalarea serverului gol.'],['△ Parțial','C','Cerința se acoperă cu limitări sau prin configurarea unor funcții existente.'],['△ Extensie','A','Extensie comunitară identificată, neinclusă implicit; licența și compatibilitatea exactă trebuie verificate.'],['△ Cod cu limite','N*','Cod existent cu limită concretă descrisă în raport; fluxul contabil nu este validat aici.'],['✕ Nu (dezvoltare)','D','Nu este livrată cerința exactă în configurația evaluată; este necesară dezvoltare/integrare. Nu înseamnă imposibil.'],['? Neconfirmat','U','Dovezi insuficiente. Nu trebuie interpretat ca Nu sau zero.'],['— Fără obiect','—','Pentru extensiile înguste, funcția nu intră în scopul modulului. Nu e verdict asupra întregului iDempiere.'],['Configurații complete','Primele 7 coloane de produse','Cinci ERP externe + iDempiere nucleu + ecranele EVA inspectate. MFG2/Libero sunt extensii, nu ERP-uri separate.'],['Module iDempiere','Următoarele 21 coloane','Se evaluează contribuția modulului. Funcțiile moștenite din nucleu nu sunt bifate din nou. Nu instalați Libero și MFG2 simultan fără analiza conflictelor.'],['Dovada funcțiilor','Surse + raport','Primele 96 funcții formează comparația generală; următoarele 13 explicitează contribuțiile unor extensii. Sursele de categorie și limitările sunt la dreapta matricei.'],['Zero licență','≠ zero TCO','Pentru configurațiile libere selectate nu este necesară o taxă de licență. Implementarea, serverele, integrarea și suportul au cost. Modulele cu licență necunoscută nu sunt aprobate ca gratuite.'],['Recomandare','Pilot EVA + MFG2','Prima opțiune nativă pentru iDempiere13; ERPNext alternativă externă. Testele de cost, reversare, loturi și izolare sunt eliminatorii.'],['Limite','Audit static/documentar','Nu s-au executat instalări sau teste funcționale ERP. Corpusul public nu garantează toate pluginurile private sau toate extensiile istorice.']];
const leg=base('Legenda','Cum se citește comparația','Simbolurile sunt însoțite de text și culori, pentru filtrare și interpretare fără ambiguitate.', ['Marcaj / temă','Cod / reper','Interpretare'],legendRows,[210,260,690]);leg.sh.getRange(`A8:C${leg.end}`).format.rowHeight=52;leg.sh.tabColor='#778799';
wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1500})).ndjson);
console.log((await wb.inspect({kind:'region',sheetId:'Comparatie',range:'A7:F10',maxChars:2200,tableMaxRows:4,tableMaxCols:6})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
for(const [sheetName,range,file] of [['Comparatie','A2:I14','comparatie'],['Comparatie','J5:R14','module1'],['Comparatie','S5:AD14','module2'],['Versiuni si module','A2:F12','versiuni'],['Surse','A2:F11','surse'],['Legenda','A2:C14','legenda']]){
 const png=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(new URL(file+'.png',qa),new Uint8Array(await png.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(new URL('package/01_Raport/Comparatie_ERP_Productie.xlsx',root).pathname.replace(/^\/([A-Z]:)/,'$1'));
console.log('Excel exported',data.rows.length,'functions',data.versions.length,'products/modules');
