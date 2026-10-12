export function addBalanceCatalog(chapters,kpis) {
 function add(code,title,owner,data,freq,dimensions,text){
  const rows=text.trim().split('\n').map(s=>s.split('|'));
  chapters.push({code,title,owner,data,freq,dimensions,count:rows.length});
  rows.forEach(([name,definition,unit,priority='P1'],i)=>kpis.push({id:code+'-'+String(i+1).padStart(2,'0'),chapter:title,name,definition,unit,owner,data,freq,dimensions,priority}));
 }
 add('CAP','23 Bilanț, capital și îndatorare','CFO / trezorerie','Bilanț + carte mare + credite + contracte','Lunar','Firmă, grup, valută, finanțator',`
Active și capitaluri proprii|Solduri de active, datorii și capitaluri proprii; control active = datorii + capitaluri proprii|lei|P0
Capital de lucru operațional net|Stocuri + creanțe operaționale − datorii operaționale, cu perimetru aprobat|lei|P0
Ciclul de conversie a numerarului|DIO + DSO − DPO; baze și perioade comparabile|zile|P0
Datorie financiară brută|Împrumuturi și alte datorii financiare incluse în politica aprobată; leasing separat|lei|P0
Datorie financiară netă|Datorie financiară brută − numerar și echivalente eligibile|lei|P0
Datorie netă / EBITDA|Datorie financiară netă / EBITDA comparabil pe 12 luni; neaplicabil dacă EBITDA ≤ 0|x
Acoperire dobânzi|EBIT / cheltuială cu dobânzile, pe aceeași perioadă și perimetru|x
DSCR|Numerar disponibil serviciului datoriei / principal și dobândă scadente; metodologie din contract|x|P0
ROIC|NOPAT / capital investit mediu; NOPAT și capitalul se definesc consecvent|%
ROE|Profit net atribuibil / capitaluri proprii medii atribuibile; interpretare separată la capital negativ|%
`);
 add('DEV','24 Investiții, dezvoltare și portofoliu','CEO / CFO / director investiții','Proiecte + bugete + contracte + active + vânzări','Lunar / pe etapă','Proiect, activ, produs, scenariu',`
CAPEX realizat|Investiții recunoscute în perioada analizată; plățile se urmăresc separat|lei|P0
CAPEX față de buget|CAPEX realizat plus angajamente rămase versus buget aprobat, fără dublare|lei și %|P0
Valoare actualizată netă a investiției|Suma fluxurilor incrementale actualizate, inclusiv investiția inițială; rată și scenariu explicite|lei
Rata internă de rentabilitate|Rata care anulează VAN; poate lipsi ori avea soluții multiple la fluxuri neconvenționale|%
Perioadă de recuperare|Timp până când fluxurile cumulative acoperă investiția; indicați dacă sunt actualizate|luni / ani
Beneficii realizate post-investiție|Beneficii validate după punerea în funcțiune / beneficii aprobate pentru aceeași perioadă|%
Întârziere punere în funcțiune|Data efectivă sau estimată minus termenul aprobat, pe etapă|zile|P0
Venit din produse noi|Venit produse lansate în fereastra definită / venit total comparabil|%
Durată până la lansare|Zile între aprobarea dezvoltării și lansarea comercială, aceeași cohortă|zile
Conversie portofoliu de inovare|Inițiative ajunse la obiectiv / inițiative eligibile din aceeași cohortă|%
`);
}
