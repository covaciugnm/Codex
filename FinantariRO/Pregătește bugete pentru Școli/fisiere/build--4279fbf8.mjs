import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const local=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/,'$1'));
const project='Z:/00. Proiecte 2026/2026.11.27 - SCOLI ISJ CJRAE ONG PARTENER - PEO P7 7.e.3 Scoli pentru viitor';
const out=path.join(local,'output'); await fs.mkdir(out,{recursive:true});
const fmt='#,##0.00;(#,##0.00);"-"';
const blue='#1643A0',green='#14714C',navy='#19364F';
const scenarios=[{key:'minim',eur:700000,months:24,pupils:480,teachers:32,groups:32,staff:8,hTeach:3766,hPed:480,hCounsel:576,hFac:120,impact:200}, {key:'maxim',eur:1000000,months:30,pupils:720,teachers:48,groups:48,staff:12,hTeach:5649,hPed:600,hCounsel:864,hFac:180,impact:280}];
for(const s of scenarios){
 const w=Workbook.create();
 const sheets={}; for(const name of ['Sinteza','Parametri','Buget','Personal','Salarizare','Achizitii','Activitati','Verificari']){const sh=w.worksheets.add(name);sheets[name]=sh;sh.showGridLines=false;sh.getRange('A1:P100').format.font={name:'Arial',size:10};sh.getRange('A1:P100').format.verticalAlignment='center';}
 const put=(sh,cell,v)=>sh.getRange(cell).values=[[v]];
 const formula=(sh,cell,v)=>{sh.getRange(cell).formulas=[[v]];sh.getRange(cell).format.font.color=v.includes('!')?green:'#111111';};
 const title=(sh,t)=>{put(sh,'A2',t);sh.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:navy};};
 const header=(sh,range)=>sh.getRange(range).format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32};
 const p=sheets.Parametri;title(p,'Ipoteze și reguli de calcul');
 p.getRange('A5:D5').values=[['Parametru','Valoare','Statut','Sursă / regulă']];header(p,'A5:D5');
 const params=[
 ['Buget eligibil țintă (EUR)',s.eur,'Limită ghid','GSCS §5.4 p.46'],
 ['Curs lei/EUR',5.2584,'Fix în apel','GSCS §5.4 p.46; InforEuro septembrie 2026'],
 ['Buget țintă (lei)',null,'Calcul','Include toate contribuțiile, nu doar grantul'],
 ['Durată (luni)',s.months,'Ipoteză','Maximum30 luni, finalizare până la31.12.2029'],
 ['Elevi unici',s.pupils,'Ipoteză','Minimum400; >456 pentru3 puncte; fără dublă numărare'],
 ['Profesori în formare',s.teachers,'Ipoteză','EECO05; certificat valid, fără dublă finanțare'],
 ['Rata indirectelor',0.15,'Regulă','GSCS §5.3.2: personal direct per membru'],
 ['Plafon FEDR / directe',0.15,'Regulă','GSCS §5.3.2 p.43'],
 ['Minim A1+A2 / total',0.50,'Regulă','GSCS §5.2.3 p.36–37'],
 ['Contribuție ONG',0,'Regulă','GSCG §2.2 tabel11 P7: ONG fără scop patrimonial'],
 ['Contribuție lider',0.02,'DE CONFIRMAT','Ipoteză2%: instituție din categoria publică locală/finanțare parțială. Categoria integral buget stat:15% în regiuni mai puțin dezvoltate.'],
 ['CAS salariat',0.25,'Ipoteză fiscală standard','Cod fiscal art.138; recalculare la angajare, fără deduceri/scutiri în model'],
 ['CASS salariat',0.10,'Ipoteză fiscală standard','Cod fiscal art.156; verificare situație individuală'],
 ['Impozit pe salariu',0.10,'Ipoteză fiscală standard','Cod fiscal art.78; baza după CAS/CASS'],
 ['CAM angajator',0.0225,'Ipoteză fiscală standard','Cod fiscal art.220^3; condiții normale'],
 ['Capacitate AFN ONG (lei)',2013707,'Calcul ANAF2022–2025','316590+674835+127710+894572; confirmare bilanțuri integrale'],
 ['Scenariu contribuție',1,'Selectabil1 sau2','1=Minim acceptat;2=Optimizare punctaj. Aceleași cote: grila nu punctează contribuția suplimentară.'],
 ['Elevi/grupă',15,'Ipoteză','Dimensionare specialist educație; nu prag din ghid'],
 ['Număr grupe',s.groups,'Ipoteză','Grupe de15 pentru A1.1'],
 ['Porții catering/elev',60,'Ipoteză','60 întâlniri eligibile, maximum o porție/elev/întâlnire; fără suprapunere cu alt program'],
 ['Elevi cu transport',s.pupils/2,'Ipoteză','50% cu nevoie; de verificat domiciliu/rute'],
 ['Deplasări dus-întors/elev',60,'Ipoteză','Numai întâlniri efective; liste și rute'],
 ['Elevi STEAM',s.pupils/4,'Ipoteză','Subgrup inclus în elevii unici'],
 ['Plafon net/oră utilizat',70,'Regulă prudentă','GSCG tabel15: <5 ani70,5–10ani80,>10ani90; pentru personal eligibil'],
 ['Luni de activitate didactică',s.months===24?18:24,'Ipoteză','Orele se planifică pe săptămâni și discipline'],
 ['Ore/lună pentru echivalent normă',168,'Referință GSCG','8ore×21zile; nu aprobă depășiri Codul muncii'],
 ['Tema verde / directe – minim',0.04,'Regulă','Anexa3 criteriul1.6: minimum4% directe; urmărit și la total prudent'],
 ];
 p.getRange(`A6:D${5+params.length}`).values=params; formula(p,'B8','=B6*B7');
 formula(p,'B24','=ROUNDUP(B10/B23,0)');formula(p,'B26','=ROUNDUP(B10/2,0)');formula(p,'B28','=ROUNDUP(B10/4,0)');
 p.getRange('B6:B32').format.font.color=blue;p.getRange('B8').format.font.color='#111111';p.getRange('B12:B20').setNumberFormat('0.00%');p.getRange('B32').setNumberFormat('0.0%');p.getRange('B6:B8').setNumberFormat(fmt);p.getRange('B7').setNumberFormat('0.0000');p.getRange('B21').setNumberFormat(fmt);p.getRange('B22').dataValidation={rule:{type:'list',values:['1','2']}};
 p.getRange('A1:A36').format.columnWidth=41;p.getRange('B1:B36').format.columnWidth=19;p.getRange('C1:C36').format.columnWidth=24;p.getRange('D1:D36').format.columnWidth=85;p.getRange('A6:D32').format.wrapText=true;p.getRange('A6:D32').format.rowHeight=43;p.freezePanes.freezeRows(5);
 put(p,'A35','Surse principale');put(p,'D35','Ghid final OMIPE1517/2026 și GSCG consolidat Corr4, arhivate în 1. DOCUMENTE OFICIALE.');
 put(p,'D36','https://mfe.gov.ro/wp-content/uploads/2026/03/a6d051aa4c909ac6bdd802d6a9f94890.7z');
 const staff=sheets.Personal;title(staff,'Personal minim propus – cost total și ore');
 put(staff,'A3','Tarife brute ipotetice. Pentru personalul public din organigramă se aplică Legea153/2017, nu automat aceste tarife.');
 staff.getRange('A5:M5').values=[['Rol','Entitate','Activitate','Persoane','Ore totale','Brut lei/oră','CAM','Cost total lei','Net lei/oră estimat','Plafon net','Ore medii/pers/lună','Justificare ore','Probă necesară']];header(staff,'A5:M5');
 const roles=[
 ['Manager proiect','Lider','M',1,s.months*40,110,'Plan, contracte, raportare;40h/lună','CV, experiență management, contract'],
 ['Responsabil financiar lider','Lider','M',1,s.months*24,100,'Verificare cheltuieli și cereri;24h/lună','Studii economice, experiență financiară'],
 ['Coordonator ONG','ONG','M',1,s.months*24,100,'Coordonare A2/A4;24h/lună; fără dublarea facilitării','CV, experiență relevantă'],
 ['Responsabil financiar ONG','ONG','M',1,s.months*12,90,'Evidență proiect și deconturi ONG;12h/lună','Studii economice și evidență separată'],
 ['Coordonator pedagogic','Lider','A1',1,s.hPed,110,'Planuri diferențiate, instrumente, progres; exclude predarea','Cadru didactic cu experiență și competențe'],
 ['Profesori și mentori','Lider','A1/A3/A4',s.staff,s.hTeach,100,'Contact+p pregătire+evaluare+CDEOȘ; raport educație','Calificări pe discipline; orar și pontaj fără suprapuneri'],
 ['Consilier educațional','ONG','A2',1,s.hCounsel,100,'Contact individual/grup +20% pregătire/documentare','Competență/atestare și statut ONG relevante'],
 ['Facilitator comunitar','ONG','A4',1,s.hFac,90,'Consultări, acces și activități comunitare; livrabile distincte','Foaie post distinctă; poate fi persoană existentă cu ore separate']
 ];
 const staffRows=roles.map(r=>[...r.slice(0,6),null,null,null,null,null,r[6],r[7]]);staff.getRange('A6:M13').values=staffRows;
 const sal=sheets.Salarizare;title(sal,'Regim de salarizare și calculul tarifului');
 put(sal,'A3','1 = ONG / post public în afara organigramei; 2 = personal public din organigramă. Alegerea necesită documente.');
 sal.getRange('A5:K5').values=[['Rol','Regim1/2','Brut orar propus','Salariu brut lunar de bază','Majorare proiect %','Ore referință/lună','Decontare1/2','Brut orar activ','Statut bază','Document justificativ','Regulă']];header(sal,'A5:K5');
 for(let i=0;i<roles.length;i++){const r=i+6;sal.getRange(`A${r}:K${r}`).values=[[roles[i][0],1,roles[i][5],null,null,168,1,null,null,'De completat după selecția instituției și postului','Regim2: mod1 salariu+majorare; mod2 numai majorare pentru categoriile publice prevăzute de Manual.']];
  formula(sal,`H${r}`,`=IF(B${r}=1,C${r},IF(OR(D${r}="",E${r}=""),"LIPSA_DATE",D${r}/F${r}*IF(G${r}=2,E${r},1+E${r})))`);
  formula(sal,`I${r}`,`=IF(B${r}=1,"IPOTEZA TARIF",IF(OR(D${r}="",E${r}=""),"NECESAR BAZA LEGALA","CALCUL CONDITIONAT"))`);
  formula(staff,`F${r}`,`=Salarizare!H${r}`);
 }
 put(sal,'A16','Surse: GSCG §3.6 / tabel15; Legea153/2017 art.16; HG234/2023 și HG1009/2025; Manual beneficiar PEO v5.');
 put(sal,'A17','Majorarea până la40% nu este automată: se stabilește după ore, valoare, progres și actele de nominalizare.');
 put(sal,'A18','Nu se cumulează în model plata aceleiași ore prin salariul obișnuit, majorare și contract distinct.');
 put(sal,'A19','Regimul1 pentru posturi publice în afara organigramei presupune procedura legală de creare/recrutare a postului.');
 sal.getRange('A1:A19').format.columnWidth=31;sal.getRange('B1:H19').format.columnWidth=19;sal.getRange('I1:I19').format.columnWidth=24;sal.getRange('J1:K19').format.columnWidth=55;sal.getRange('A6:K13').format.wrapText=true;sal.getRange('A6:K13').format.rowHeight=68;sal.getRange('C6:F13').setNumberFormat(fmt);sal.getRange('E6:E13').setNumberFormat('0.0%');sal.getRange('H6:H13').setNumberFormat(fmt);sal.getRange('B6:G13').format.font.color=blue;sal.getRange('D6:E13').format.fill='#FFF2CC';
 sal.getRange('B6:B13').dataValidation={rule:{type:'list',values:['1','2']}};sal.getRange('G6:G13').dataValidation={rule:{type:'list',values:['1','2']}};
 for(const [row,h] of [[6,40],[7,24],[8,24],[9,12],[10,20]])formula(staff,`E${row}`,`=Parametri!B9*${h}`);
 formula(staff,'D11','=ROUNDUP(Parametri!B24/4,0)');formula(staff,'E11','=SUM(B21:B25)');formula(staff,'E12','=(Parametri!B24*12+Parametri!B10*0.2)*1.2');formula(staff,'E13','=Parametri!B10*0.25');
 for(let row=6;row<=13;row++){
 formula(staff,`G${row}`,`=F${row}*Parametri!$B$20`);formula(staff,`H${row}`,`=ROUND(E${row}*(F${row}+G${row}),2)`);
 formula(staff,`I${row}`,`=F${row}*(1-Parametri!$B$17-Parametri!$B$18)*(1-Parametri!$B$19)`);formula(staff,`J${row}`,'=Parametri!$B$29');formula(staff,`K${row}`,`=E${row}/D${row}/Parametri!$B$9`);
 }
 put(staff,'A15','TOTAL personal direct');formula(staff,'H15','=SUM(H6:H13)');put(staff,'A16','Lider');formula(staff,'H16','=SUMIFS(H6:H13,B6:B13,"Lider")');put(staff,'A17','ONG');formula(staff,'H17','=SUMIFS(H6:H13,B6:B13,"ONG")');
 put(staff,'A19','Orele profesorilor – repartizare fără dublare');
 staff.getRange('A20:D25').values=[['Componentă','Minim / maxim selectat','Activitate','Observație'],['Contact alfabetizare',s.groups*60,'A1','60h/grup'],['Contact STEAM',(s.groups/4)*48,'A1','48h/grup subgrup STEAM'],['Pregătire și evaluare',s.key==='minim'?1110:1665,'A1','750/1125 pregătire+360/540 evaluare'],['CDEOȘ/resurse',s.key==='minim'?160:240,'A3','Fără dublare serviciu multimedia'],['Contact comunitate',s.groups*6,'A4','Profesor însoțitor și aplicații']];header(staff,'A20:D20');
 formula(staff,'B21','=Parametri!B24*60');formula(staff,'B22','=ROUNDUP(Parametri!B28/Parametri!B23,0)*48');formula(staff,'B25','=Parametri!B24*6');formula(staff,'B23','=ROUNDUP((B21+B22+B25)*30%/5,0)*5+Parametri!B10*0.75');formula(staff,'B24','=Parametri!B24*5');
 put(staff,'D23','30% contact, rotunjit la5h, plus0,75h/elev evaluare');put(staff,'D24','5h/grupă pentru CDEOȘ; fără dublare multimedia');
 put(staff,'A27','Management obligatoriu:4 funcții pentru2 entități. Nu sunt bugetate funcții distincte de asistent manager/achiziții.');
 put(staff,'A28','Juridic, suport IT, RU, publicitate obligatorie și administrație: în forfetar, fără linii directe duplicate.');
 staff.getRange('A1:A28').format.columnWidth=30;staff.getRange('B1:C28').format.columnWidth=13;staff.getRange('D1:K28').format.columnWidth=16;staff.getRange('L1:M28').format.columnWidth=55;staff.getRange('A6:M13').format.wrapText=true;staff.getRange('A6:M13').format.rowHeight=62;staff.getRange('F6:K17').setNumberFormat(fmt);staff.getRange('D6:F13').format.font.color=blue;staff.freezePanes.freezeRows(5);
 const b=sheets.Buget;title(b,`Buget ${s.key} – alocări de proiectare (lei)`);
 put(b,'A3','Costurile de achiziție sunt PLAFOANE DE PLANIFICARE, repartizate transparent; nu sunt prețuri de piață validate.');
 b.getRange('A5:D9').values=[['Calcul de alocare',null,'Statut','Sens'],['Personal direct',null,'Din ore și tarife','Detalii în Personal'],['Indirecte',null,'15% personal direct','Rotunjire la bani separat per membru'],['Premii și subvenții',null,'Plafoane ghid','3/4 competiții × distincții/elev, profesori diferiți conform metodologiei'],['Disponibil bunuri/servicii',null,'Buget țintă minus categoriile de mai sus','Ponderile următoare distribuie integral acest plafon']];header(b,'A5:D5');formula(b,'B6','=Personal!H15');formula(b,'B7','=ROUND(Personal!H16*Parametri!B12,2)+ROUND(Personal!H17*Parametri!B12,2)');formula(b,'B8',`=${s.key==='minim'?3:4}*2*(1000+700+500+2*300)`);formula(b,'B9','=Parametri!B8-SUM(B6:B8)');
 b.getRange('A12:L12').values=[['Cheltuială / livrabil','Entitate','Activitate','Pondere disponibil','Cantitate','UM','Plafon unitar lei','Buget lei','FEDR','Pondere verde','Verde lei','Fundamentare de completat']];header(b,'A12:L12');
 const items=[
 ['Catering pentru întâlniri eligibile','Lider','A2',.31,s.pupils*60,'porții',0,0,'Prezență, orar complementar; ofertă pe porție cu TVA și alergeni; liderul contractează suportul școlar'],
 ['Transport la activități','Lider','A2',.20,s.pupils/2*60,'curse/elev',0,0,'Rute, distanțe, locuri; ofertă; nu buget per kilometru presupus'],
 ['Kituri robotică / laborator STEAM','Lider','A1',.09,s.groups/4,'kituri',1,.5,'Inventar existent, specificații și oferte; bunuri rămân școlii'],
 ['Dispozitive digitale și accesibilitate','Lider','A1',.05,s.groups,'dispozitive',1,0,'Maximum pe echipament din GSCG; configurație și inventar de verificat'],
 ['Materiale didactice și eco-STEAM','Lider','A1',.06,s.pupils,'pachete',0,1,'Conținut și consum justificat pe sesiuni; diferențiați FEDR de consumabile'],
 ['Instrumente evaluare și licențe','Lider','A1',.055,s.pupils,'utilizatori',0,0,'Durată licență, testare T0/T1/T2; fără platformă nouă dacă există'],
 ['Logistică participare competiții','Lider','A1',.035,s.pupils/4,'elevi',0,0,'Calendar eligibil, deplasări distincte de transport A2, fără premii duplicate'],
 ['Formare profesori40h, certificare','Lider','A3',.05,s.teachers,'persoane',0,.5,'Furnizor competent;40h/pers; tematici complementare; cost personal extern separat dacă identificabil'],
 ['Digitizare și accesibilizare resurse','Lider','A3',.04,s.key==='minim'?4:6,'module',0,0,'Producție multimedia; conținut realizat de profesori nu se plătește dublu'],
 ['Vizite și ateliere comunitare','Lider','A4',.04,s.groups,'ateliere',0,.5,'6h/grup; acces instituții și materiale; fără ore profesori duplicate'],
 ['Evaluare impact independentă','Lider','A5',.025,s.impact,'ore-serviciu',0,0,'T0/T1/T2, analiză date, raport scalare; a se separa personal extern dacă identificabil'],
 ['Resurse incluzive adaptate','Lider','A2',.025,s.pupils,'pachete',0,0,'Accesibilitate, egalitate gen; probă nevoi și ofertă'],
 ['Ateliere practică și consumabile','Lider','A1',.02,s.groups,'grupe',0,1,'Consum pe experimente, fără echipamente ascunse'],
 ];
 // Exact allocation weights are a visible planning choice, not evidence of price reasonableness.
 const itemRows=items.map(r=>[...r.slice(0,6),null,null,r[6],r[7],null,r[8]]);b.getRange('A13:L25').values=itemRows;
 const quantities={13:'=Parametri!B10*Parametri!B25',14:'=Parametri!B26*Parametri!B27',15:'=ROUNDUP(Parametri!B28/Parametri!B23,0)',16:'=Parametri!B24',17:'=Parametri!B10',18:'=Parametri!B10',19:'=Parametri!B28',20:'=Parametri!B11',21:'=ROUNDUP(Parametri!B10/120,0)',22:'=Parametri!B24',23:'=40+Parametri!B10/3',24:'=Parametri!B10',25:'=Parametri!B24'};
 for(const [row,f] of Object.entries(quantities))formula(b,`E${row}`,f);
 for(let row=13;row<=25;row++){formula(b,`H${row}`,`=ROUND($B$9*D${row},2)`);formula(b,`G${row}`,`=H${row}/E${row}`);formula(b,`K${row}`,`=H${row}*J${row}`);}
 b.getRange('M12:O12').values=[['Ofertă unitară lei (editabil)','Sursă ofertă / dată','Alocare inițială lei']];header(b,'M12:O12');
 for(let row=13;row<=25;row++){
  formula(b,`O${row}`,`=ROUND($B$9*D${row},2)`);
  formula(b,`G${row}`,`=O${row}/E${row}`);
  formula(b,`H${row}`,`=IF(ISNUMBER(M${row}),ROUND(E${row}*M${row},2),O${row})`);
  put(b,`N${row}`,'Lipsă ofertă');
 }
 formula(b,'O25','=ROUND($B$9-SUM(O13:O24),2)');
 put(b,'P12','Personal extern eligibil din bugetul liniei');header(b,'P12');b.getRange('P1:P39').format.columnWidth=25;b.getRange('P13:P25').format={fill:'#FFF2CC',font:{name:'Arial',size:10,color:blue},numberFormat:fmt};
 put(b,'A10','Bază personal extern din oferte');formula(b,'B10','=SUM(P13:P25)');
 formula(b,'B7','=ROUND((Personal!H16+SUMIFS(P13:P25,B13:B25,"Lider"))*Parametri!B12,2)+ROUND((Personal!H17+SUMIFS(P13:P25,B13:B25,"ONG"))*Parametri!B12,2)');
 put(b,'L25','Consum pe experimente. Pondere2%; ultima linie preia exclusiv diferența de rotunjire la bani a alocărilor.');
 put(b,'A27','Total bunuri/servicii');formula(b,'D27','=SUM(D13:D25)');formula(b,'H27','=SUM(H13:H25)');
 b.getRange('A30:F30').values=[['Entitate','Personal direct','Bunuri/servicii + premii','Total directe','Indirecte15%','Total eligibil']];header(b,'A30:F30');
 for(const [r,entity] of [[31,'Lider'],[32,'ONG']]){put(b,`A${r}`,entity);formula(b,`B${r}`,`=SUMIFS(Personal!H6:H13,Personal!B6:B13,A${r})`);formula(b,`C${r}`,`=SUMIFS(H13:H25,B13:B25,A${r})${entity==='Lider'?'+B8':''}`);formula(b,`D${r}`,`=SUM(B${r}:C${r})`);formula(b,`E${r}`,`=ROUND(B${r}*Parametri!B12,2)`);formula(b,`F${r}`,`=SUM(D${r}:E${r})`);}
 for(const r of [31,32])formula(b,`E${r}`,`=ROUND((B${r}+SUMIFS(P13:P25,B13:B25,A${r}))*Parametri!B12,2)`);
 put(b,'A33','TOTAL');for(const c of ['B','C','D','E','F'])formula(b,`${c}33`,`=SUM(${c}31:${c}32)`);
 put(b,'A35','Premii/subvenții: per concurs1.000/700/500/300lei;5 distincții planificate, minimum17 participanți pentru limita30%.');
 put(b,'A36','Subvențiile profesorilor sunt condiționate de premii reale și documente; nu drept automat pentru întreaga echipă.');
 put(b,'A37','TVA: plafoane de planificare inclusiv TVA nerecuperabilă, dacă eligibilă. În bugetul de depunere se separă baza/TVA.');
 put(b,'A38','Completați oferta unitară în M și sursa în N. Bugetul devine cantitate×ofertă; totalul NU mai este forțat la limită.');
 put(b,'A39','P: introduceți numai componenta de personal extern eligibil confirmată din H, nu toată factura. Se actualizează indirectele.');
 put(b,'A40','Catering/transport la lider este recomandare de organizare; ONG execută direct consilierea și facilitarea comunitară.');
 const ac=sheets.Achizitii;title(ac,'Fișe de achiziție și comparația ofertelor');
 put(ac,'A3','Specificații funcționale propuse de echipă, nu condiții suplimentare din ghid. Se adaptează diagnosticului și inventarului.');
 ac.getRange('A5:F5').values=[['Linie buget','Obiect','Specificație minimă propusă','Unitate comparabilă','Probe necesare','Condiție critică']];header(ac,'A5:F5');
 const specs=[
 ['Meniu adaptat vârstei, alergeni, livrare la orar și locații, trasabilitate și condiții alimentare legale','Lei/porție livrată, același conținut și aceeași TVA','Liste prezență, program masă existent, minimum surse comparabile motivate','Fără dublă finanțare pentru aceeași persoană și interval'],
 ['Rute și kilometri reali, capacitate locuri, accesibilitate după nevoie, autorizări și asigurări','Lei/cursă completă și lei/elev transportat','Hartă rute, elevi, orar, ofertă cu costuri incluse','Fără kilometri inventați; transport sigur al minorilor'],
 ['Kit educațional complet, număr posturi utilizabile, senzori/controler, software, garanție, manuale','Lei/kit cu aceeași listă componente și servicii','Inventar existent;3 surse comparabile recomandate, fără impunere de marcă','Descompunere FEDR/consumabile; proprietate școală și utilizare gratuită'],
 ['Dispozitiv compatibil cu aplicațiile alese, accesibilitate, garanție, licență și suport','Lei/dispozitiv, configurație echivalentă, TVA separat','Fișă tehnică; verificare plafon specific GSCG pentru tipul ales','Nu înlocuiește dotări finanțate fără motiv; criterii ecologice verificabile'],
 ['Materiale pe elev și consum pe activitate, reutilizare și componentă eco-STEAM descrisă','Lei/pachet cu aceeași compoziție','Listă consum pe sesiuni; cost atribuit temei verzi','Denumirea eco nu justifică singură100% cost verde'],
 ['Evaluare inițială/intermediară/finală, raportare pe competențe, accesibilitate și protecția datelor','Lei/utilizator pe durata proiectului, toate funcțiile incluse','Licențe existente; contract prelucrare date; cost suport separat','Fără construcția unei platforme noi când resursele existente sunt suficiente'],
 ['Calendar concurs, număr elevi, taxe, transport/cazare/masă eligibile distinct','Lei/elev/deplasare cu aceleași servicii','Calendar avizat și costuri detaliate, reguli concurs și jurizare','Nu dublează A2; premiile/subvențiile au evidență separată'],
 ['40h/persoană, grupe16, curriculum complementar, evaluare și certificare recunoscută','Lei/persoană și lei/grupă; defalcare personal extern','Furnizor competent; rezultate învățare; declarații anti-dublă finanțare','EECR03 minim80%; un certificat de simplă prezență poate fi insuficient'],
 ['Module accesibile și reutilizabile, format editabil, drepturi de utilizare, testare','Lei/modul cu aceeași listă livrabile','Caiet sarcini, surse resurse, livrabile profesor vs furnizor','Nu se plătește de două ori conținutul creat de profesor'],
 ['Ateliere6h/grup, locație sigură, acord partener asociat, materiale și acces','Lei/atelier pentru15elevi și6h; servicii delimitate','Acord colaborare, plan pedagogic, acorduri necesare pentru minori','Orele profesorilor sunt deja în Personal'],
 ['T0/T1/T2, metodologie, analiză A1–A4, date pseudonimizate, raport de scalare','Lei/oră expert și lei/livrabil; personal extern separat','Plan evaluare independentă, rezultate verificabile','A5 nu este audit financiar; nu dublează evaluările de rutină'],
 ['Resurse accesibile adaptate nevoilor identificate, egalitate și incluziune','Lei/pachet pe nevoie concretă, fără materiale decorative','Diagnostic nevoi și adaptări, ofertă detaliată','Nu se presupune automat existența unei dizabilități'],
 ['Consumabile pentru experimente și activități practice, cantitate per grupă/sesiune','Lei/set pe aceeași listă materiale','Fișă consum și justificare experimentală','Activele reutilizabile se reclasifică după natura lor']
 ];
 for(let i=0;i<items.length;i++)ac.getRange(`A${i+6}:F${i+6}`).values=[[`Buget rând${i+13}`,items[i][0],...specs[i]]];
 ac.getRange('A1:A22').format.columnWidth=18;ac.getRange('B1:B22').format.columnWidth=38;ac.getRange('C1:F22').format.columnWidth=57;ac.getRange('A6:F18').format.wrapText=true;ac.getRange('A6:F18').format.rowHeight=83;
 put(ac,'A21','Comparație recomandată: descriere identică, UM, cantitate, preț fără TVA, TVA, total, valabilitate, termen, garanție, sursă/date.');
 put(ac,'A22','3 surse comparabile este recomandare de robustețe a echipei; numărul nu este prezentat drept obligație universală a acestui ghid.');
 b.getRange('M1:M39').format.columnWidth=23;b.getRange('N1:N39').format.columnWidth=55;b.getRange('O1:O39').format.columnWidth=22;b.getRange('M13:M25').format={fill:'#FFF2CC',font:{name:'Arial',size:10,color:blue},numberFormat:fmt};b.getRange('N13:N25').format.wrapText=true;b.getRange('O13:O25').setNumberFormat(fmt);
 b.getRange('A1:A38').format.columnWidth=42;b.getRange('B1:C38').format.columnWidth=17;b.getRange('D1:K38').format.columnWidth=17;b.getRange('L1:L38').format.columnWidth=66;b.getRange('A13:L25').format.wrapText=true;b.getRange('A13:L25').format.rowHeight=66;b.getRange('D13:D27').setNumberFormat('0.0%');b.getRange('J13:J25').setNumberFormat('0.0%');b.getRange('G13:H27').setNumberFormat(fmt);b.getRange('K13:K25').setNumberFormat(fmt);b.getRange('B31:F33').setNumberFormat(fmt);b.getRange('B6:B9').setNumberFormat(fmt);b.freezePanes.freezeRows(12);
 const a=sheets.Activitati;title(a,'Activități, rezultate și alocări');a.getRange('A5:F5').values=[['Activitate','Conținut','Cantitate / țintă','Buget direct lei','Calendar relativ','Dovezi / condiții']];header(a,'A5:F5');
 const aa=[['A1','Alfabetizare60h/grup + STEAM48h/grup',s.pupils,null,'L2–L'+(s.months-2),'Diagnostic, planuri, programe, evaluări, concursuri'],['A2','Masă, transport, consiliere, abilități sociale',s.pupils,null,'L2–L'+(s.months-2),'Nevoi individuale; fără dublă finanțare'],['A3','CDEOȘ, resurse digitale, formare40h',s.teachers,null,'L3–L'+(s.months-3),'Avizare, certificate, declarații complementaritate'],['A4','Programe comunitare6h/grup',s.groups,null,'L4–L'+(s.months-2),'Acorduri școală-muzee/antreprenori; protecție minori'],['A5','Evaluare impact T0/intermediar/final și scalare',3,null,'L1–L'+s.months,'Standarde naționale; raport și resurse deschise'],['M','Management obligatoriu în2 entități',4,null,'L1–L'+s.months,'Fișe post, CV, pontaje; personal suport din indirecte']];a.getRange('A6:F11').values=aa;
 formula(a,'C6','=Parametri!B10');formula(a,'C7','=Parametri!B10');formula(a,'C8','=Parametri!B11');formula(a,'C9','=Parametri!B24');
 for(const [row,start,end] of [[6,2,2],[7,2,2],[8,3,3],[9,4,2],[10,1,0],[11,1,0]])formula(a,`E${row}`,`="L${start} - L"&(Parametri!B9-${end})`);
 formula(a,'D6','=SUMIFS(Buget!H13:H25,Buget!C13:C25,"A1")+Personal!H10+Personal!H11*(Personal!B21+Personal!B22+Personal!B23)/Personal!E11+Buget!B8');
 formula(a,'D7','=SUMIFS(Buget!H13:H25,Buget!C13:C25,"A2")+Personal!H12');
 formula(a,'D8','=SUMIFS(Buget!H13:H25,Buget!C13:C25,"A3")+Personal!H11*Personal!B24/Personal!E11');
 formula(a,'D9','=SUMIFS(Buget!H13:H25,Buget!C13:C25,"A4")+Personal!H13+Personal!H11*Personal!B25/Personal!E11');
 formula(a,'D10','=SUMIFS(Buget!H13:H25,Buget!C13:C25,"A5")');formula(a,'D11','=SUM(Personal!H6:H9)');
 put(a,'A14','Indicator');put(a,'B14','Țintă planificată');header(a,'A14:B14');put(a,'A15','EECO06+07');formula(a,'B15','=Parametri!B10');put(a,'A16','5SR09 minimum80%');formula(a,'B16','=ROUNDUP(B15*80%,0)');put(a,'A17','EECO05');formula(a,'B17','=Parametri!B11');put(a,'A18','EECR03 minimum80%');formula(a,'B18','=ROUNDUP(B17*80%,0)');
 a.getRange('A1:A18').format.columnWidth=26;a.getRange('B1:B18').format.columnWidth=53;a.getRange('C1:E18').format.columnWidth=21;a.getRange('F1:F18').format.columnWidth=65;a.getRange('A6:F11').format.wrapText=true;a.getRange('A6:F11').format.rowHeight=55;a.getRange('D6:D11').setNumberFormat(fmt);
 const sum=sheets.Sinteza;title(sum,`Școli pentru viitor – buget ${s.key}`);
 put(sum,'A3','PROIECTARE IDEALĂ CONDIȚIONATĂ. ONG partener; școlile și probele se selectează conform fișelor de condiții.');
 sum.getRange('A5:D5').values=[['Indicator','Valoare','Unitate','Interpretare']];header(sum,'A5:D5');
 const summaries=[['Total eligibil', '=Buget!F33','lei','Buget de proiectare la limita apelului'],['Echivalent EUR','=B6/Parametri!B7','EUR','Grant + contribuții'],['Buget lider','=Buget!F31','lei','Lider eligibil de confirmat'],['Buget ONG','=Buget!F32','lei','ROSE ca serviciu; entitatea fiscală este asociațiaCUI29433614'],['Personal direct','=Personal!H15','lei','Ore și tarife ipotetice'],['Personal / total','=B10/B6','%','Fără personal externalizat neidentificat în oferte'],['Elevi unici','=Parametri!B10','persoane','Ipoteză, nu beneficiari confirmați'],['Cost total/elev','=B6/B12','lei/elev','Nu este plafon ghid sau preț de piață'],['Scenariu selectat','=CHOOSE(Parametri!B22,"Minim acceptat","Optimizare punctaj")','','Scenariile au aceleași cote; contribuția suplimentară nu aduce puncte']];
 for(let i=0;i<summaries.length;i++){let row=6+i;put(sum,`A${row}`,summaries[i][0]);formula(sum,`B${row}`,summaries[i][1]);put(sum,`C${row}`,summaries[i][2]);put(sum,`D${row}`,summaries[i][3]);}
 formula(sum,'B10','=SUM(Personal!H15,Buget!B10)');put(sum,'D10','Include componenta externă numai după introducerea și validarea ei în Buget!P.');
 sum.getRange('A17:D17').values=[['Contribuție / finanțare','V1 minim acceptat','V2 optimizare punctaj','Regula']];header(sum,'A17:D17');
 const finance=[['Cotă ONG','=Parametri!B15','=Parametri!B15','0%; nu există prag superior pentru punctaj'],['Cotă lider','=Parametri!B16','=Parametri!B16','2% ipoteză; categoria juridică poate impune 15%'],['Contribuție ONG','=ROUND(B9*B18,2)','=ROUND(B9*C18,2)','Din bugetul propriu ONG'],['Contribuție lider','=ROUND(B8*B19,2)','=ROUND(B8*C19,2)','Liderul suportă propria cotă'],['Contribuție totală','=SUM(B20:B21)','=SUM(C20:C21)','Suma contribuțiilor membrilor'],['AFN totală','=B6-B22','=B6-C22','Finanțare nerambursabilă estimată'],['AFN ONG','=B9-B20','=B9-C20','Comparată cu capacitatea ANAF'],['Bonus punctaj contribuție',0,0,'Anexa3 nu acordă acest bonus']];
 for(let i=0;i<finance.length;i++){const r=18+i;put(sum,`A${r}`,finance[i][0]);for(let c=1;c<=2;c++){const col=c===1?'B':'C';typeof finance[i][c]==='string'?formula(sum,`${col}${r}`,finance[i][c]):put(sum,`${col}${r}`,finance[i][c]);}put(sum,`D${r}`,finance[i][3]);}
 put(sum,'A28','Decizia de proiectare');put(sum,'D28','Preferință preliminară: varianta minimă dacă acoperă nevoile reale. Bugetul maxim nu aduce automat punctaj.');
 put(sum,'A29','Țintă ideală punctaj ITI');put(sum,'B29',100);put(sum,'D29','100 condiționat de criteriul ITI și toate probele; plafon99 fără ITI. Nu este punctaj acordat.');
 put(sum,'A30','Disponibil ANAF31.12.2025');put(sum,'B30',35819);put(sum,'D30','Istoric. Utilizatorul declară fonduri actuale suficiente și niciun alt proiect PEO aprobat.');
 put(sum,'A31','Rezervă numerar ONG – 3luni');formula(sum,'B31','=B9/Parametri!B9*3');put(sum,'D31','Test simplificat de lichiditate, nu flux de numerar și nu condiție legală.');
 put(sum,'A33','Persoane dacă roluri distincte');formula(sum,'B33','=SUM(Personal!D6:D13)');put(sum,'D33','15 /19 persoane, majoritatea cu timp parțial; personalul furnizorilor nu este inclus.');
 put(sum,'A34','Ore totale personal');formula(sum,'B34','=SUM(Personal!E6:E13)');
 put(sum,'A35','Norme echivalente medii');formula(sum,'B35','=B34/Parametri!B9/Parametri!B31');put(sum,'D35','Media pe proiect nu înlocuiește controlul orelor zilnice și al lunilor de vârf.');
 sum.getRange('A1:A32').format.columnWidth=36;sum.getRange('B1:C32').format.columnWidth=23;sum.getRange('D1:D32').format.columnWidth=85;sum.getRange('A6:D14').format.rowHeight=34;sum.getRange('D6:D32').format.wrapText=true;sum.getRange('A18:D31').format.rowHeight=36;sum.getRange('B6:C31').setNumberFormat(fmt);sum.getRange('B11').setNumberFormat('0.0%');sum.getRange('B18:C19').setNumberFormat('0.0%');sum.getRange('B12').setNumberFormat('0');sum.getRange('B29').setNumberFormat('0');sum.getRange('B6:C31').format.font.color='#172B3A';sum.getRange('B14').format.font.color=green;
 header(sum,'A17:D17');put(sum,'C11','');
 sum.getRange('B33:B34').setNumberFormat('#,##0');sum.getRange('B35').setNumberFormat('0.00');sum.getRange('A33:D35').format.rowHeight=34;sum.getRange('D33:D35').format.wrapText=true;sum.getRange('B33:B35').format.font.color='#172B3A';
 const v=sheets.Verificari;title(v,'Controale matematice și condiții de validare');v.getRange('A5:D5').values=[['Control','Valoare','Prag / rezultat așteptat','Interpretare']];header(v,'A5:D5');
 const checks=[['Diferență total față de țintă','=Buget!F33-Parametri!B8','0 lei','Rotunjirea poate genera diferențe de câțiva bani'],['Suma ponderilor achizițiilor','=SUM(Buget!D13:D25)','100%','Nu constituie verificare prețuri de piață'],['A1+A2 / total','=(Activitati!D6+Activitati!D7)/Buget!F33','>=50%','GSCS §5.2.3'],['FEDR / directe','=SUMIFS(Buget!H13:H25,Buget!I13:I25,1)/Buget!D33','<=15%','Verificare echipamente; reclasificare după specificații'],['Verde / directe','=SUM(Buget!K13:K25)/Buget!D33','>=4%','Doar dacă justificarea tematică și partea de cost sunt probate'],['Verde / total','=SUM(Buget!K13:K25)/Buget!F33','>=4% prudent','Acoperă și lectura mai conservatoare a ponderii'],['Diferență lider minus ONG','=Buget!F31-Buget!F32','>0 lei','GSCS §5.1.4'],['Marjă capacitate AFN ONG','=Parametri!B21-Sinteza!B24','>=0 lei','Metoda venituri2022–2025; nu certifică întreaga eligibilitate'],['Reconciliere activități cu directe','=SUM(Activitati!D6:D11)-Buget!D33','0 lei','Fără dublare personal profesori'],['Reconciliere ore profesori','=SUM(Personal!B21:B25)-Personal!E11','0 ore','Ore globale distribuite pe activități'],['Net orar maxim estimat','=MAX(Personal!I6:I13)','<=70 lei în ipoteza curentă','Regimul public din organigramă necesită calcul separat'],['Grup țintă','=Parametri!B10','>=400;>456 pentru3p','Evidență unică pe elev'],['Documente ONG','NECONFIRMAT','Proiect relevant în ultimii3ani','Serviciile de vârstnici nu sunt dovadă suficientă'],['Lider și contribuție','NECONFIRMAT','Tip exact și sursă finanțare','2% este ipoteză; nu rată universală pentru instituții publice'],['Analiză de piață','NECONFIRMAT','Oferte/surse pentru fiecare achiziție','Alocările nu pot fi prezentate ca prețuri validate'],['Flux de numerar','NECONFIRMAT','Sold actual și calendar rambursări','Capitaluri negative2025; evaluare contabilă necesară'],['Buget de depunere','NEFINALIZAT','Toate clarificările și probele','Acest fișier este model de lucru, nu confirmare eligibilitate']];
 for(let i=0;i<checks.length;i++){const r=6+i;put(v,`A${r}`,checks[i][0]);checks[i][1].startsWith('=')?formula(v,`B${r}`,checks[i][1]):put(v,`B${r}`,checks[i][1]);put(v,`C${r}`,checks[i][2]);put(v,`D${r}`,checks[i][3]);}
 v.getRange('A1:A24').format.columnWidth=43;v.getRange('B1:B24').format.columnWidth=24;v.getRange('C1:C24').format.columnWidth=38;v.getRange('D1:D24').format.columnWidth=70;v.getRange('A6:D22').format.wrapText=true;v.getRange('A6:D22').format.rowHeight=43;v.getRange('B6:B17').setNumberFormat(fmt);v.getRange('B7:B11').setNumberFormat('0.00%');
 v.getRange('B6').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FDE9E7',font:{color:'#A4262C',bold:true}}});v.getRange('B13').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FDE9E7',font:{color:'#A4262C',bold:true}}});v.getRange('B18:B22').format={fill:'#FFF2CC',font:{name:'Arial',size:10,bold:true,color:'#7F4700'}};
 put(v,'A24','Peste pragul minim (lei)');formula(v,'B24','=Buget!F33-700000*Parametri!B7');put(v,'C24','>=0');put(v,'D24','Eligibilitatea intervalului se verifică distinct de ținta variantei.');
 put(v,'A25','Sub plafonul maxim (lei)');formula(v,'B25','=1000000*Parametri!B7-Buget!F33');put(v,'C25','>=0');
 put(v,'A26','Oferte unitare introduse');formula(v,'B26','=COUNT(Buget!M13:M25)');put(v,'C26','13 pentru acoperire completă');put(v,'D26','Introducerea unui preț nu validează singură oferta sau eligibilitatea.');
 v.getRange('B24:B25').setNumberFormat(fmt);v.getRange('B24:B25').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FDE9E7',font:{color:'#A4262C',bold:true}}});v.getRange('A24:D26').format.rowHeight=42;v.getRange('A24:D26').format.wrapText=true;
 put(v,'A27','Personal extern peste linia aferentă');formula(v,'B27','=SUMPRODUCT(--(Buget!P13:P25>Buget!H13:H25))');put(v,'C27','0 linii');put(v,'D27','P este inclus în H, nu se adaugă a doua oară. Validați natura și documentele costului.');
 put(v,'A28','Ipoteză de proiectare acceptată');put(v,'B28','CONDIȚIONAT');put(v,'C28','Condiții ideale, la cererea beneficiarului');put(v,'D28','Lipsa actuală a probelor devine cerință de selecție, nu probă de neeligibilitate.');
 formula(v,'B6','=ROUND(Buget!F33-Parametri!B8,2)');formula(v,'B14','=ROUND(SUM(Activitati!D6:D11)-Buget!D33,2)');formula(v,'B24','=ROUND(Buget!F33-700000*Parametri!B7,2)');formula(v,'B25','=ROUND(1000000*Parametri!B7-Buget!F33,2)');
 put(v,'A29','Valori negative cantități/preț/personal');formula(v,'B29','=COUNTIFS(Buget!E13:E25,"<0")+COUNTIFS(Buget!M13:M25,"<0")+COUNTIFS(Buget!P13:P25,"<0")+COUNTIFS(Salarizare!C6:D13,"<0")+COUNTIFS(Salarizare!F6:F13,"<=0")+COUNTIFS(Personal!D6:D13,"<=0")+IF(Parametri!B9<=0,1,0)+IF(Parametri!B23<=0,1,0)+IF(Parametri!B31<=0,1,0)');put(v,'C29','0');
 put(b,"Q12","Ofertă fără sursă");for(let qr=13;qr<=25;qr++)formula(b,"Q"+qr,'=IF(ISNUMBER(M'+qr+'),IF(OR(N'+qr+'="",N'+qr+'="Lipsă ofertă"),1,0),0)'); put(v,'A30','Oferte fără sursă completată');formula(v,'B30','=SUM(Buget!Q13:Q25)');put(v,'C30','0 la validare');put(v,'D30','Prețul numeric nu este suficient. Păstrați oferta, data și specificația comparabilă.');
 put(v,'A31','Regim public fără bază de calcul');formula(v,'B31','=COUNTIFS(Salarizare!I6:I13,"NECESAR BAZA LEGALA")');put(v,'C31','0');put(v,'D31','Dacă regimul2 este ales fără salariu/majorare, erorile de calcul rămân vizibile până la completare.');
 put(v,'A32','Majorări publice în afara0–40%');formula(v,'B32','=COUNTIFS(Salarizare!E6:E13,">0.4")+COUNTIFS(Salarizare!E6:E13,"<0")');put(v,'C32','0');put(v,'D32','Plafonul nu validează procentul concret; se aplică grila și progresul proiectului.');
 v.getRange('A27:D28').format.wrapText=true;v.getRange('A27:D28').format.rowHeight=46;
 v.getRange('A29:D32').format.wrapText=true;v.getRange('A29:D32').format.rowHeight=46;v.getRange('B27:B32').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:0,format:{fill:'#FDE9E7',font:{color:'#A4262C',bold:true}}});
 w.recalculate();
 const originalTotal=b.getRange('F33').values[0][0];const originalCatering=b.getRange('H13').values[0][0];
 b.getRange('M13').values=[[10]];w.recalculate();
 if(Math.abs(b.getRange('F33').values[0][0]-(originalTotal-originalCatering+s.pupils*60*10))>0.02)throw new Error('Quote input did not flow to budget');
 b.getRange('M13').values=[[null]];w.recalculate();
 const oldTeachersHours=staff.getRange('E11').values[0][0];p.getRange('B10').values=[[s.pupils+120]];w.recalculate();
 if(b.getRange('E13').values[0][0]!==((s.pupils+120)*60)||staff.getRange('E11').values[0][0]<=oldTeachersHours)throw new Error('Pupil driver did not update quantities and staffing');
 p.getRange('B10').values=[[s.pupils]];w.recalculate();
 const beforeExt=b.getRange('E33').values[0][0];b.getRange('P20').values=[[1000]];w.recalculate();if(Math.abs(b.getRange('E33').values[0][0]-beforeExt-150)>0.02)throw new Error('External personnel base calculation failed');b.getRange('P20').values=[[null]];w.recalculate();
 sal.getRange('B6').values=[[2]];sal.getRange('D6:E6').values=[[8000,0.1]];w.recalculate();if(Math.abs(staff.getRange('F6').values[0][0]-8000/168*1.1)>0.001)throw new Error('Public salary regime1 failed');sal.getRange('G6').values=[[2]];w.recalculate();if(Math.abs(staff.getRange('F6').values[0][0]-8000/168*0.1)>0.001)throw new Error('Public salary majoration-only failed');sal.getRange('B6').values=[[1]];sal.getRange('D6:E6').values=[[null,null]];sal.getRange('G6').values=[[1]];w.recalculate();
 if(v.getRange("B30").values[0][0]!==0)throw new Error("Blank quotes counted");b.getRange("M13:N13").values=[[10,null]];w.recalculate();if(v.getRange("B30").values[0][0]!==1)throw new Error("Missing quote source not caught");b.getRange("M13:N13").values=[[null,"Lipsă ofertă"]];w.recalculate();sal.getRange("C6").values=[[-1]];w.recalculate();if(v.getRange("B29").values[0][0]<1)throw new Error("Negative salary not caught");sal.getRange("C6").values=[[110]];w.recalculate(); const totals={variant:s.key,total:b.getRange('F33').values,split:b.getRange('A31:F33').values,checks:v.getRange('A6:B32').values};
 await fs.writeFile(path.join(out,`verification_${s.key}.json`),JSON.stringify(totals,null,2));
 console.log(JSON.stringify(totals));
 const scan=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:20},summary:'Formula errors'});await fs.writeFile(path.join(out,`errors_${s.key}.txt`),scan.ndjson);
 // Test the requested contribution selector and restore it.
 p.getRange('B22').values=[[2]];w.recalculate();if(sum.getRange('B14').values[0][0]!=='Optimizare punctaj')throw new Error('Selector contribution failed');p.getRange('B22').values=[[1]];w.recalculate();
 const xlsx=await SpreadsheetFile.exportXlsx(w);await xlsx.save(path.join(out,`Buget_${s.key}_doua_scenarii_contributie.xlsx`));
 const renders=[['Sinteza','A1:D35'],['Parametri','A1:D32'],['Personal','A1:M25'],['Salarizare','A1:K19'],['Achizitii','A1:F22'],['Buget','A12:P27'],['Activitati','A1:F18'],['Verificari','A1:D32']];
 for(const [name,range] of renders){const img=await w.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(out,`${s.key}_${name}.png`),new Uint8Array(await img.arrayBuffer()));}
}
