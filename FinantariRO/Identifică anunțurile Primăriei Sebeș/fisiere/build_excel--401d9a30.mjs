import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const base=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(.:)/,'$1'));
const rows=JSON.parse(await fs.readFile(path.join(base,'records.json'),'utf8'));
const projects=JSON.parse(await fs.readFile(path.join(base,'projects.json'),'utf8'));
const exists=async p=>p?fs.access(p).then(()=>true).catch(()=>false):false;
const q=s=>String(s).replaceAll('"','""');
// Excel stores local wall-clock dates as serial numbers, without timezone conversion.
const serial=s=>Date.parse(s+'Z')/86400000+25569;
for(const pr of projects){
 const rr=rows.filter(r=>r.project===pr.id).sort((a,b)=>a.folder-b.folder||a.id.localeCompare(b.id));
 const wb=Workbook.create();const sh=wb.worksheets.add('Documente');const cal=wb.worksheets.add('Termene');
 for(const s of [sh,cal]){s.showGridLines=false;s.tabColor='#243C58';}
 sh.getRange('A2').values=[[`Registru documente ROSE anunt ${pr.num}`]];
 sh.getRange('A2').format.font={name:'Arial',size:14,bold:true};
 sh.getRange('A3').values=[[pr.title]];
 sh.getRange('A4').values=[['Situație verificată la 01.11.2026. Documentele nesemnate și câmpurile lipsă împiedică depunerea completă.']];
 sh.getRange('A5:B5').values=[['Documente lipsă','']];sh.getRange('B5').formulas=[[`=COUNTIF(E9:E${rr.length+8},"Lipsa")`]];
 sh.getRange('D5:E5').values=[['Semnături lipsă','']];sh.getRange('E5').formulas=[[`=COUNTIF(E9:E${rr.length+8},"Lipsa semnatura")`]];
 const headers=['ID','Categorie','Document','Cerință','Stare la verificare','Acțiune necesară','Responsabil','Semnatar','Termen fizic','Termen e-mail','Observații','Word sau copie','PDF','Sursă și pagini'];
 headers.push('Cale copie','Cale PDF');sh.getRange('A8:P8').values=[headers];
 const data=[];
 for(const r of rr){
  const file=await exists(r.dest);const pdf=r.dest.endsWith('.docx')?r.dest.replace('Word pentru semnare','PDF pentru semnare').replace(/\.docx$/,'.pdf'):r.dest.endsWith('.pdf')?r.dest:'';
  const pdfok=await exists(pdf);
  data.push([r.id,r.folder,r.title,r.required,r.status,r.action||'Verificare finală',r.owner,r.signer,serial(r.due),serial(r.email_due),r.obs,'','',''+r.source,file?r.dest:'',pdfok?pdf:'']);
 }
 sh.getRange(`A9:P${data.length+8}`).values=data;
 for(let i=0;i<data.length;i++)for(const [c,pi,label] of [['L',14,'Deschide copia'],['M',15,'Deschide PDF']]){
  if(data[i][pi]){const rel=path.relative(pr.out,data[i][pi]);sh.getRange(`${c}${i+9}`).formulas=[[`=HYPERLINK("${q(rel)}","${label}")`]];}
 }
 const body=sh.getRange(`A8:P${data.length+8}`);body.format.font={name:'Arial',size:10};body.format.verticalAlignment='top';body.format.wrapText=true;
 sh.getRange('A8:P8').format={fill:'#243C58',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:34,wrapText:true};
 const widths=[12,10,44,23,25,51,28,31,22,22,80,22,22,90,68,68];
 widths.forEach((v,i)=>sh.getRangeByIndexes(0,i,data.length+8,1).format.columnWidth=v);
 data.forEach((row,i)=>{const lines=Math.max(...row.map((v,c)=>Math.ceil(String(v??'').length/(widths[c]*0.9))));sh.getRange(`A${i+9}:P${i+9}`).format.rowHeight=Math.max(34,lines*13+8);});
 sh.getRange(`B9:B${data.length+8}`).setNumberFormat('00');
 sh.getRange(`I9:J${data.length+8}`).setNumberFormat('dd.mm.yyyy hh:mm');
 sh.freezePanes.freezeRows(8);sh.freezePanes.freezeColumns(3);
 const table=sh.tables.add(`A8:P${data.length+8}`,true,'DocumenteP'+pr.id);table.style='TableStyleLight9';table.showFilterButton=true;
 for(const status of ['Lipsa','Lipsa semnatura','Necesita forma lizibila','Neconcordante'])sh.getRange(`E9:E${data.length+8}`).conditionalFormats.add('containsText',{text:status,format:{fill:'#FCE4D6',font:{color:'#9C0006',bold:true}}});
 sh.getRange(`E9:E${data.length+8}`).conditionalFormats.add('containsText',{text:'De confirmat',format:{fill:'#FFF2CC'}});
 cal.getRange('A2').values=[['Calendar si reguli de predare']];cal.getRange('A2').format.font={name:'Arial',size:14,bold:true};
 cal.getRange('A4:E4').values=[['Etapă','Termen','Responsabil propus','Canal / destinație','Observații']];
 const cr=[
 ['Finalizare documente și verificări',new Date('2026-11-02T12:00:00'),'ROSE și experții','Intern','Termen intern recomandat, nu termen oficial. Nu se declară complet până la închiderea lipsurilor.'],
 ['Depunere fizică',new Date('2026-11-02T16:00:00'),'ROSE','Registratura Primăriei Sebeș, Piața Primăriei nr.1','Plic sigilat cu titlul proiectului și numărul anunțului.'],
 ['Depunere e-mail / poștă / curier',new Date('2026-11-03T00:00:00'),'ROSE','proiecte@primariasebes.ro','02.11.2026 ora24:00, adică03.11.2026 ora00:00. PDF scanat, numerotat și opisat. Documentele trebuie primite în termen.'],
 ['Solicitări clarificări către participanți',new Date('2026-11-05T00:00:00'),'Primăria Sebeș','Conform anunțului','Data fără oră precizată.'],
 ['Răspuns la clarificări',new Date('2026-11-09T16:00:00'),'ROSE','Registratură sau proiecte@primariasebes.ro','Persoană contact: Armian Steliana.'],
 ['Evaluare dosare',new Date('2026-11-10T00:00:00'),'Comisia de evaluare','Calendar Anexa5','Data fără oră precizată.'],
 ['Publicare rezultate',new Date('2026-11-11T00:00:00'),'Primăria Sebeș','Site Primăria Sebeș','Calendarul și clauza generală de publicare din anunț nu sunt perfect corelate; urmăriți comunicările oficiale.'],
 ['Depunere contestații',new Date('2026-11-12T00:00:00'),'ROSE dacă este cazul','Registratură / e-mail','Anunțul menționează și maximum1 zi lucrătoare de la comunicarea rezultatelor. Ora nu este precizată.'],
 ['Soluționare contestații',new Date('2026-11-16T00:00:00'),'Comisia de evaluare','Calendar Anexa5','Data fără oră precizată.'],
 ['Rezultate finale',new Date('2026-11-17T00:00:00'),'Primăria Sebeș','Site Primăria Sebeș','Data fără oră precizată.']];
 for(const row of cr){const s=row[1];const local=[s.getFullYear(),String(s.getMonth()+1).padStart(2,'0'),String(s.getDate()).padStart(2,'0')].join('-')+'T'+[String(s.getHours()).padStart(2,'0'),String(s.getMinutes()).padStart(2,'0'),'00'].join(':');row[1]=serial(local);row[4]=row[4].replaceAll('ora24','ora 24').replaceAll('adică03','adică 03').replaceAll('ora00','ora 00').replaceAll('maximum1','maximum 1').replaceAll('Anexa5','Anexa 5');}
 cal.getRange('A5:E14').values=cr;cal.getRange('A4:E14').format.font={name:'Arial',size:10};cal.getRange('A4:E14').format.wrapText=true;cal.getRange('A4:E14').format.verticalAlignment='top';
 cal.getRange('A4:E4').format={fill:'#243C58',font:{color:'#FFFFFF',bold:true},rowHeight:30};
 [39,25,28,58,85].forEach((w,i)=>cal.getRangeByIndexes(0,i,18,1).format.columnWidth=w);cal.getRange('A5:E14').format.rowHeight=60;cal.getRange('B5:B14').setNumberFormat('dd.mm.yyyy hh:mm');
 cal.getRange('A16').values=[['Sursa: anunțul din folderul 00 Procedura si modele oficiale, secțiunile1–3 și calendarul Anexa5. Orele00:00 la datele fără oră sunt convenții de stocare, nu termene orare oficiale.']];
 cal.getRange('A16:E17').format.wrapText=true;cal.getRange('A16').format.font={name:'Arial',size:10,italic:true};
 let auditSheet=null;
 const auditData=await fs.readFile(path.join(base,'audit_checklist.json'),'utf8').then(JSON.parse).catch(()=>null);
 if(auditData?.length){
  auditSheet=wb.worksheets.add('Corecturi audit');auditSheet.showGridLines=false;
  auditSheet.getRange('A2').values=[['Checklist audit si lipsuri externe']];auditSheet.getRange('A2').format.font={name:'Arial',size:14,bold:true};
  const keys=Object.keys(auditData[0]);auditSheet.getRange('A4:F4').values=[keys];
  auditSheet.getRange(`A5:F${auditData.length+4}`).values=auditData.map(r=>keys.map(k=>r[k]||''));
  const range=auditSheet.getRange(`A4:F${auditData.length+4}`);range.format.font={name:'Arial',size:10};range.format.wrapText=true;range.format.verticalAlignment='top';
  auditSheet.getRange('A4:F4').format={fill:'#243C58',font:{color:'#FFFFFF',bold:true},rowHeight:34};
  [10,29,37,85,90,38].forEach((v,i)=>auditSheet.getRangeByIndexes(0,i,auditData.length+4,1).format.columnWidth=v);
  auditSheet.getRange(`A5:F${auditData.length+4}`).format.rowHeight=65;
  const at=auditSheet.tables.add(`A4:F${auditData.length+4}`,true,'AuditP'+pr.id);at.style='TableStyleLight9';at.showFilterButton=true;auditSheet.freezePanes.freezeRows(4);
  auditSheet.getRange(`B5:B${auditData.length+4}`).conditionalFormats.add('containsText',{text:'DESCHIS',format:{fill:'#FFF2CC',font:{color:'#9C0006'}}});
 }
 wb.recalculate();
 const inspect=await wb.inspect({kind:'table',range:'Documente!A8:F13',include:'values,formulas',tableMaxRows:6,tableMaxCols:6,maxChars:3000});
 await fs.writeFile(path.join(base,`excel_inspect_${pr.id}.json`),inspect.ndjson);
 const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:30},maxChars:2000});
 await fs.writeFile(path.join(base,`excel_errors_${pr.id}.json`),errors.ndjson);
 for(const [sheet,range] of [['Documente','A8:F14'],['Termene','A4:E10'],...(auditSheet?[['Corecturi audit','A4:F10']]:[])]){
  const preview=await wb.render({sheetName:sheet,range,scale:1.4,format:'png'});await fs.writeFile(path.join(base,`excel_${pr.id}_${sheet}.png`),new Uint8Array(await preview.arrayBuffer()));
 }
 const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path.join(pr.out,'00 Registru documente si termene ROSE.xlsx'));
 console.log('Exported project',pr.id,'rows',rr.length);
}
