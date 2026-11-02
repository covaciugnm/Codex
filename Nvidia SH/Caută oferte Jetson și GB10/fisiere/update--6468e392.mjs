import fs from 'node:fs/promises';
import {SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const root='//192.168.100.169/Comun/00.Roboti/Nvidia/SH', day='2026-10-31';
const data=JSON.parse(await fs.readFile(root+'/monitorizare/oferte.json','utf8'));
const old=structuredClone(data), checked=new Set();
function update(part, fields={}) {const r=data.offers.find(r=>r[12].includes(part)); if(!r)throw Error(part); for(const [k,v]of Object.entries(fields))r[+k]=v;checked.add(r[12]);}
update('BTO100_FCM1253_EMEA',{6:33578.83,8:'Inclus; net 27751.10',9:33.92,10:'11-20 buc afisate*'});
update('90MS0371-M00030',{6:36822.95,8:'Inclus; net 30432.19',9:33.90,13:'Livrare afisata 05.11.2026. *Mesaj generic contradictoriu de lipsa stoc.'});
for(const p of ['ATAGB10-9001','EDGEXPERT-32SEU','940-54242-0005-000','0606863','2539662','907864','bp885202','NVIDIA-Jetson-AGX-Orin-Dev-Kit-64GB'])update(p);
update('cz9k4et-abd',{1:'Excluse',10:'Stoc epuizat: NICHT LAGERND',11:'Nu este livrabil acum',13:'Pret neschimbat 6849 EUR; pagina directa indica lipsa stoc la 31.10.2026.'});
update('398028165227',{13:'31.10.2026: pagina eBay inaccesibila dupa doua incercari. Pretul si starea sunt istorice din 30.10; nu este dovada de retragere. Livrarea RO neconfirmata.'});checked.delete(data.offers.find(r=>r[12].includes('398028165227'))[12]);
const additions=[
['SH','De verificat','Jetson AGX Thor','Dev Kit, 1TB; 128GB de reconfirmat','OLX Polonia / Martyna','Polonia, Warszawa',16999,'PLN','Privat; TVA nedetaliat',null,'Desigilat si testat; anunt accesibil','Neconfirmata','https://www.olx.pl/d/oferta/nvidia-jetson-agx-thor-developer-kit-CID99-ID1adjjT.html','Nou identificat, publicat 11.10.2026. Etichetat nou, dar descrierea spune deschis si conectat. Fara garantie/retur declarat. Camp RAM generic 64GB sau mai mult; confirmati SKU T5000/128GB.'],
['SH','De verificat','NVIDIA DGX Spark','128GB, 4TB','Kleinanzeigen / NProxima GmbH','Germania, München',7735,'EUR','Brut calculat: 6500 net +19%',null,'SH; B2B exclusiv','Transport mentionat; RO neconfirmata','https://www.kleinanzeigen.de/s-anzeige/nvidia-dgx-spark-ai-supercomputer/3556695883-228-16341','Publicat 30.10.2026. Titlu 6900 EUR negociabil, dar descriere 6500 EUR net (7735 brut): pret contradictoriu, de clarificat.'],
['SH','De verificat','ASUS Ascent GX10','Lot 4 buc: 2x2TB + 2x1TB','Kleinanzeigen / Manni','Germania, Köln',22000,'EUR','Privat; TVA nedetaliat',null,'SH, lot indivizibil nespecificat','Antet transport; descriere ridicare','https://www.kleinanzeigen.de/s-anzeige/4x-asus-gx10-dgx-spark-/3555162976-228-955','5500 EUR/buc este numai media lotului, nu pret unitar oferit. RAM de confirmat. 4 cabluri ConnectX7 incluse; facturi declarate. Nu recomandat ca livrabil RO.'],
['SH','De verificat','NVIDIA DGX Spark','Titlu 1TB; RAM neprecizat','Subito','Italia, Milano',7950,'EUR','Factura posibila; TVA nedetaliat',null,'Ca nou','Transport Subito afisat; RO neconfirmata','https://www.subito.it/informatica/dgx-spark-nvidia-1t-di-memoria-milano-666269927.htm','Configuratie insuficient documentata; nu presupune 128GB/4TB. Costurile domestice afisate nu sunt tarife RO.']
];
for(const r of additions)if(!data.offers.some(x=>x[12]===r[12])){data.offers.push(r);checked.add(r[12]);}
data.checked_at=day;data.verified_at_by_url={...(data.verified_at_by_url||{})};
for(const r of old.offers)data.verified_at_by_url[r[12]]??=old.checked_at;
for(const url of checked)data.verified_at_by_url[url]=day;
data.verification_errors=[{url:'https://www.ebay.de/itm/398028165227',date:day,attempts:2,error:'Pagina inaccesibila prin instrumentul web; pret anterior pastrat.'}];
data.run_notes=['Verificare partiala: pagini directe Senetic RO (5), RS DE (2), NBB ASUS, HP, ForIT, Welectron, OLX PL Thor, Kleinanzeigen si Subito. Cautari suplimentare OLX RO/PL, eBay, Marktplaats, Leboncoin, Willhaben, Cyberport, Alza si retail european. Nu toate magazinele au putut fi reverificate individual.','Indexurile Aetherix aveau preturi vechi: pagina directa Spark 8639.40 EUR, Orin 4585.90 EUR. ASUS 64GB exclus din comparatia GB10 128GB.'];
data.changes=[{type:'reducere',model:'Dell Pro Max GB10',old:33773.51,new:33578.83,currency:'RON'},{type:'reducere',model:'ASUS GX10 Senetic',old:36917.43,new:36822.95,currency:'RON'},{type:'candidat_nou',model:'Jetson AGX Thor OLX PL',price:16999,currency:'PLN',shipping:'RO neconfirmata'},{type:'stoc_epuizat',model:'HP ZGX Nano HP DE'}];
for(const cat of ['Noi','SH']){
 const path=root+(cat==='Noi'?'/Noi/Oferte_NVIDIA_Noi.xlsx':'/Second_Hand/Oferte_NVIDIA_SH.xlsx');
 await fs.copyFile(path,root+'/monitorizare/istoric/'+day+'_'+cat+'_inainte.xlsx');
 const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));const notes=new Map();
 for(const s of wb.worksheets.items)for(const row of s.getRange('A8:O100').values)if(row[14])notes.set(row[14],row[13]);
 for(const section of ['Oferte','De verificat','Excluse']){
  const s=wb.worksheets.getItem(section), rows=data.offers.filter(r=>r[0]===cat&&r[1]===section).sort((a,b)=>a[2].localeCompare(b[2])||a[7].localeCompare(b[7])||a[6]-b[6]);
  const prev=old.offers.filter(r=>r[0]===cat&&r[1]===section).length,last=7+rows.length;
  for(let i=prev+8;i<=last;i++)s.getRange(`A${i}:O${i}`).copyFrom(s.getRange('A8:O8'),'all');
  for(const t of [...s.tables.items])t.delete();
  s.getRange(`A8:O${Math.max(last,prev+7)}`).values=Array.from({length:Math.max(rows.length,prev)},()=>Array(15).fill(null));
  s.getRange(`A8:O${last}`).values=rows.map(r=>[r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],null,r[10],r[11],(Date.parse(data.verified_at_by_url[r[12]])-Date.UTC(1899,11,30))/86400000,r[13],notes.get(r[12])||'',r[12]]);
  s.getRange(`I8:I${last}`).formulas=rows.map((_,i)=>[`=IF(ISNUMBER(H${i+8}),E${i+8}+H${i+8},"Necunoscut")`]);
  s.getRange(`L8:L${last}`).setNumberFormat('yyyy-mm-dd');
  s.getRange('A3').values=[['Monitorizare 31.10.2026. Data verificarii fiecarui rand apare in coloana L. Livrarea RO necesita confirmare unde este indicat.']];
  if(cat==='SH')s.getRange('A4').values=[['Thor: candidat desigilat OLX PL in De verificat; memoria exacta si livrarea RO neconfirmate.']];
  s.tables.add(`A7:O${last}`,true,`${cat}_${section.replaceAll(' ','')}`);
 }
 wb.recalculate();
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
 const preview=await wb.render({sheetName:cat==='SH'?'De verificat':'Oferte',range:cat==='SH'?'A7:G11':'D7:L11',scale:1,format:'png'});
 await fs.writeFile(root+'/monitorizare/'+cat+'_2026-10-31.png',new Uint8Array(await preview.arrayBuffer()));
 await(await SpreadsheetFile.exportXlsx(wb)).save(path);
 console.log('Saved',cat,'manual notes preserved',notes.size);
}
await fs.writeFile(root+'/monitorizare/istoric/'+day+'.json',JSON.stringify(data,null,2));
await fs.writeFile(root+'/monitorizare/oferte.json',JSON.stringify(data,null,2));
