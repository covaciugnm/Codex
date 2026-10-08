import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const here=new URL('.',import.meta.url);const d=JSON.parse(await fs.readFile(new URL('excel_data.json',here),'utf8'));
const root='//192.168.100.169/Comun/00.Roboti/iDempiere/Documentatie/BI_iDempiere';
const wb=Workbook.create(); const previews=[];
function col(n){let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s}
function sheet(name,title,context,headers,rows,widths){
 const s=wb.worksheets.add(name);s.showGridLines=false;const end=col(headers.length),last=rows.length+5;
 s.getRange(`A1:${end}${last}`).format.font={name:'Arial',size:10,color:'#183044'};
 s.getRange(`A1:${end}${last}`).format.verticalAlignment='center';
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:15,bold:true};
 s.getRange('A3').values=[[context]];s.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#536372'};
 s.getRange(`A5:${end}${last}`).values=[headers,...rows];
 s.getRange(`A5:${end}5`).format={fill:'#203E59',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeight:62};
 s.getRange(`A6:${end}${last}`).format.rowHeight=36;
 s.getRange(`A6:${end}${last}`).format.wrapText=true;
 widths.forEach((w,i)=>s.getRange(`${col(i+1)}5:${col(i+1)}${last}`).format.columnWidth=w);
 for(let i=6;i<=last;i++)if(i%2===0)s.getRange(`A${i}:${end}${i}`).format.fill='#F1F5F8';
 s.tables.add(`A5:${end}${last}`,true,'T'+name.replace(/[^A-Za-z]/g,''));
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(name==='Aplicatii BI'?3:2);
 previews.push([name,`A1:${col(Math.min(headers.length,7))}${Math.min(last,14)}`]);return s;
}
const status={N:'✓ Da',C:'◐ Parțial · config',L:'◐ Parțial · limitat',P:'✕ Nu · comercial',D:'✕ Nu · dezvoltare',U:'? Neconfirmat',E:'✓ Da · în cod',A:'◐ Parțial · moștenit',G:'? Neconfirmat',H:'◐ Parțial · dormant'};
function colorStatus(s,range){const r=s.getRange(range);r.format.horizontalAlignment='center';
 for(const [text,fill,color] of [['✓','#E3F1E8','#195B35'],['◐','#FFF0C8','#785408'],['✕','#F8E4E2','#942D2D'],['?','#E9EDF2','#526173']])r.conditionalFormats.add('containsText',{text,format:{fill,font:{color}}});
}
const keys=['Superset','Metabase_OSS','Knowage_CE','Redash','Lightdash_OSS','iDempiere','Eva'];
const ah=['ID','Capitol','Funcție',...d.versions.map(v=>v[0]+'\n'+(v[0]==='Eva Accounting'?v[1].slice(0,12):v[1]))];
const a=sheet('Aplicatii BI','Comparație BI pentru Eva și iDempiere','Evaluare 08.10.2026. ✓ Da  ◐ Parțial  ✕ Nu în ediția gratuită  ? Neconfirmat. Detalii: Note functii.',ah,d.rows.map(r=>[r.id,r.categorie,r.functie,...keys.map(k=>status[r[k]])]),[9,25,43,...keys.map(()=>24)]);
a.tabColor='#203E59';colorStatus(a,'D6:J69');a.getRange('A5:J5').format.rowHeight=74;
for(const kind of ['Nativ','Extensie']){
 const ms=d.modules.filter(m=>m.kind===kind),heads=['Capitol','Funcție',...ms.map(m=>m.name+'\n'+m.version)];
 const rows=d.moduleFeatures.map(([cat,f])=>[cat,f,...ms.map(m=>f==='Izolare Eva 13 testată'?'? Neconfirmat':f==='Configurare AI după profil'?'✕ Nu · dezvoltare':m.yes.includes(f)?'✓ Da':m.partial.includes(f)?'◐ Parțial':'— N/A')]);
 const s=sheet(kind==='Nativ'?'Module native':'Extensii','Funcții '+(kind==='Nativ'?'native iDempiere':'ale extensiilor iDempiere'),'Capabilități documentate ale componentei. — N/A: în afara rolului. Nu confirmă instalarea în Eva. Licențe și limite: Catalog.',heads,rows,[23,32,...ms.map(()=>25)]);
 colorStatus(s,`C6:${col(heads.length)}${rows.length+5}`);s.getRange(`A5:${col(heads.length)}5`).format.rowHeight=96;
 previews.push([s.name,`J5:P14`]);
}
const n=sheet('Note functii','Explicații și trasabilitate','Categoriile de surse sunt completate de manualele locale. Golul în codul auditat nu dovedește absența în orice altă ramură.', ['ID','Funcție','Observație','Surse','Coduri originale SUP / MET / KNO / RED / LIG / ERP / EVA'],d.rows.map(r=>[r.id,r.functie,r.nota,r.surse,keys.map(k=>r[k]).join(' / ')]),[9,43,95,80,50]);n.getRange('A6:E69').format.rowHeight=46;
const catalogRows=[...d.versions.map(v=>[v[0],v[1],'Platformă',v[2],v[3],v[4],'Release identificat; documentația latest poate include funcții ulterioare. Nu este instalare testată.']),...d.modules.map(m=>[m.name,m.version,m.kind,m.license,m.source,m.role,m.note||'Capabilitate documentată. Compatibilitatea și activarea pe Eva necesită inventar.'])];
const ca=sheet('Catalog','Versiuni, licențe și limite','Versiune neconfirmată rămâne explicită. Extensiile fără licență verificată nu sunt recomandate drept 100% gratuite.', ['Produs / modul','Versiune identificată','Tip','Licență / condiții','Release / surse','Rol / referințe','Limită de verificare'],catalogRows,[30,44,16,48,80,64,85]);ca.getRange(`A6:G${catalogRows.length+5}`).format.rowHeight=56;
const so=sheet('Surse','Documentația oficială consultată','Instantanee și manuale complete sunt în 06_Surse_oficiale și 07_Manuale_complete. Un HTTP 200 nu confirmă singur conținutul.', ['ID','Document','URL oficial','Fișier local','HTTP'],d.sources.map(s=>[s.id,s.title,s.url,s.local||'Indisponibil; vezi referința online',s.status??s.http_status??'Vezi surse.json']),[9,45,100,85,12]);so.getRange(`A6:E${d.sources.length+5}`).format.rowHeight=46;
const le=sheet('Legenda','Interpretarea bifei','Comparația măsoară ediția gratuită și componenta indicată, nu configurarea efectivă în producție.', ['Marcaj','Semnificație','Ce trebuie verificat'],[
['✓ Da','Nativ gratuit / implementare Eva observată','Setarea datelor și drepturilor rămâne necesară. „În cod” nu confirmă funcționarea în instalare.'],
['◐ Parțial · config','Disponibil după configurare sau dependențe','Nu este gata configurat implicit pentru Eva.'],
['◐ Parțial · limitat','Numai o parte a funcției în ediția gratuită','Consultați observația și limita de ediție.'],
['◐ Parțial · dormant','Componentă istorică / neactivă conform README','Nu este punctată ca BI activ în Eva.'],
['✕ Nu · comercial','Funcția comparabilă cere ediția plătită','Nu este contabilizată ca gratuită.'],
['✕ Nu · dezvoltare','Nu există nativ; trebuie construit separat','Arhitectura AI propusă nu este implementată prin acest raport.'],
['? Neconfirmat','Dovadă insuficientă / instalare netestată','Nu echivalează cu Nu.'],
['— N/A','Funcția nu face parte din rolul componentei','Nu penalizați un scheduler pentru absența unui editor pivot.'],
['Domeniu','5 aplicații BI + iDempiere + Eva; 37 componente/familii','Inventar al surselor identificate, fără certificare de exhaustivitate a extensiilor private sau istorice.'],
['Recomandare','Superset + rapoarte native + configurator AI propriu','Detaliile de arhitectură și criteriile pilotului sunt în raport.'],
], [29,77,110]);le.getRange('A6:C15').format.rowHeight=55;
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Aplicatii BI!A5:J10',include:'values,formulas',tableMaxRows:6,tableMaxCols:10,maxChars:2400})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},summary:'verificare finala',maxChars:1000})).ndjson);
await fs.mkdir(new URL('excel_previews/',here),{recursive:true});
for(let i=0;i<previews.length;i++){const [sheetName,range]=previews[i];try{const blob=await wb.render({sheetName,range,scale:1.3,format:'png'});await fs.writeFile(new URL(`excel_previews/${i+1}.png`,here),new Uint8Array(await blob.arrayBuffer()));}catch(e){console.log('render',sheetName,String(e).slice(0,300));}}
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(root+'/02_Matrice/Comparatie_BI_iDempiere_Eva.xlsx');console.log('XLSX exported');
