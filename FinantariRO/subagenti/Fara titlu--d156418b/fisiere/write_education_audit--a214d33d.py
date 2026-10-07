from pathlib import Path
import html,json,hashlib,math
from pypdf import PdfReader
BASE=Path(r'\\192.168.100.169\Comun\00. Proiecte 2026\2026.11.27 - UAT CJ ISJ ONG PARTENER - PEO P5 5.f.2 Educatie timpurie - Relansare 2026')
D=BASE/'7.3 Fezabilitate si SWOT'
D.mkdir(exist_ok=True)
text='''AUDIT EDUCAȚIONAL, FEZABILITATE ȘI SWOT – RUNDA 2
Data verificării: 07.10.2026. Lider: Municipiul Sebeș. Partener propus: Asociația ROMANIAN SOUL ENTITY, CUI 29433614.
Scop: verificarea designului educațional, a capacității și justificării resurselor. Audit intern de pregătire; nu este certificat de legalitate, raport de audit financiar sau punctaj oficial AM.

VERDICT
Varianta minimă este dimensionabilă, dar încă dependentă de operator, grupe, spațiu și situația copiilor. Varianta maximă de 1.650 copii nu are încă demonstrația capacității locale, a grupului vulnerabil și a resurselor. Nu poate primi onest verdict final 10/10. Disponibilitatea fondurilor asigurată de beneficiar rezolvă o ipoteză de finanțare; nu înlocuiește aprobările, resursa umană sau dovada nevoii. Valoarea maximă de lucru comunicată: 26.272.446 lei, plafon legal 26.292.000 lei. Apropierea de plafon nu justifică singură cheltuielile.

1. CE AM VERIFICAT EFECTIV
GSCS: activități, grup țintă, indicatori, bareme, primă dotare și formare; grila de evaluare. HG1563/2024 anexa: articolele privind constituirea, programul, evidența, anul școlar, spațiul, evaluarea și personalul. Art23/207 Legea198 în forma verificată de jurist la18.01.2026; certificarea ultimei consolidări28.09.2026 rămâne juridic deschisă. Nu folosim forma de bază drept text actual. HCL392/2025 toate3pagini și HCL235/2026 toate4pagini citite vizual din PDF scanat. SIDU2021–2030 capitol educație și tabelele23–26, nu integral219pagini. Pagina oficială LiceulGerman2026–2027 citită integral. HCL50/78/242: titlu, dispozitiv relevant și paginile inspectate; anexele de inventar nu sunt încă confruntate articol cu articol. PDF-uri arhivate integral nu înseamnă documente integral auditate.

2. REȚEA ȘCOLARĂ ACTUALIZATĂ – NU CONFUNDĂM OPERATOR, STRUCTURĂ, LOCAȚIE, GRUPĂ
HCL235/09.09.2026 completează situația față de HCL392/22.12.2025 și se bazează pe OM5594/31.08.2026. Anexa actuală include:
• LPS Florin Fleșeriu: GPP nr4, GPN nr6;
• Școala Gimnazială Petrești: GPN și GPP Petrești;
• Liceul German: GPP Germană Petrești (pagina școlii prezintă și niveluri în alte locații);
• Școala Gimnazială Mihail Kogălniceanu: Școala Silviu Cărpinișian, GPN Lancrăm, GPN nr8, GPP nr7;
• Școala Gimnazială nr2: GPN Răhău și Școala Răhău;
• Grădinița Copiilor Voioși, cu personalitate juridică: Creșa Copiilor Voioși, GPP nr2 și GPP nr3;
• particular: grădinițele Heidi, Sfântul Nicolae, Mirela;
• alte PJ în anexă: Colegiul Lucian Blaga, Liceul Tehnologic și Școala Postliceală Henri Coandă. Prezența în rețea nu dovedește nivel eligibil de educație timpurie.
Această listă identifică entități reale, nu le desemnează parteneri sau locații de proiect. Reorganizarea face vechile pagini ale Școlii nr2 și Liceului Tehnologic insuficiente pentru stabilirea operatorului actual al grădinițelor/creșelor. Se cere extras SIIIR actual și OM5594 cu anexe.
Ținta EECO18=20 poate reprezenta, dacă definiția ghidului este îndeplinită, 10 unități sprijinite în doi ani școlari succesivi. Nu înseamnă automat 20 operatori sau20spații. Nu avem încă10unități eligibile distincte confirmate prin acorduri. Nu multiplicăm operatorii cu numărul grupelor, serviciilor ori dotărilor.

3. CAPACITATE ȘI GRUP ȚINTĂ
Pagina oficială Liceul German2026–2027 publică 28locuri antepreșcolare și124preșcolare, în total152locuri aprobate. Sunt locuri de școlarizare, nu locuri libere și nici copii vulnerabili eligibili PEO. Datele preced reorganizarea dinseptembrie și se confirmă cu operatorul.
SIDU publică1.161copii înscriși în grădinițe în2020, după760în2019. Saltul seriei și vechimea o fac improprie pentru calculul GT2026. Propunerea1.380preșcolari (1.260standard+120complementar) este cu219peste reperul2020, deci reclamă validare demografică și a cohortelor, nu dovedește imposibilitate. Înscrierea pe doi ani poate produce copii unici diferiți, însă fiecare trebuie să aibă durata de sprijin bugetată și vârsta eligibilă la intrare. Aceeași persoană nu devine copilnou în anul2.
Nu există încă dovadă pentru826copii romi (>50%din1650),224CES ori1.452rezultate. Etniile se documentează legal și voluntar, CES prin documentele aplicabile; nu se deduc din adresă, venit, nume sau profilul școlii. Recrutarea nu trebuie să producă segregare. Pentru varianta65, pragul>50%=33romi; rezultatul>85%=56copii. 58/65 și1452/1650 sunt ținte propuse, nu rezultate verificate.

4. EFECTIVE, COHORTE ȘI NORMARE
Referința verificată art23: ante grupa mică medie9/min7/max11; mijlocie14/10/17; mare16/10/22; preșcolar17/12/22. Plafonul26 nu este general: ar rezulta numai din derogare individuală+4 aprobată. Art23(9) reduce maximul cu3pentru fiecare copil CES integrat. Alte reguli de medie/constituire și eventuale derogări se aplică distinct; calculul agregat nu certifică gruparea.
MIN:7ante pot reprezenta o grupă mică dacă vârstele și aprobarea permit; nu o grupă mijlocie/mare de7fără derogare. 34pre standard pot fi distribuiți în2grupe17, dar există regulă actuală de constituire peste medie și cel mult o grupă sub medie/nivel/PJ; soluția depinde de grupe existente vsnouconstituite și de aprobarea ISJ. Nu numim automat2×17 legal. Dacă34sunt doar copiii proiectului din grupe existente, se verifică efectivul TOTAL al grupelor cu toți copiii, inclusiv cei nefinanțați prin proiect.
MAX:60grupe×21preșcolari=1260 nu absoarbe224CES simultan. Dacă toți224CES sunt în acestegrupe, condiția necesară este G≥ceil((1260+3×224)/22)=88grupe. FărăCES:ceil1260/22=58. Formula se aplică fiecărei cohorte simultane și fiecărei locații, nu întregului GTmultianual fără calendar. Pentru2cohorte reale de630+112CES, fiecare12luni:minimum44grupe simultane/cohortă; acest scenariu cere24luni efective consecutive de serviciu după autorizare și nu încape automat într-un proiect24luni cu pregătire. Nu reduceți numărul de grupe doar printr-o etichetă de cohortă.
Pentru270ante simultan fărăCES, limite aritmetice:25grupe dacă toți mici(max11),16dacă toți mijlocii(max17),13dacă toți mari(max22). Mixul vârstelor, spațiile și CES pot crește necesarul. Personalul standard: art207(4) indică1post/grupă normală,2posturi/grupă prelungită; se confirmă norma orară actuală și încadrarea. Nu ajunge un simplu număr de experți ai proiectului. Baremul include salariile standard, dar bugetul trebuie însoțit de statul de funcții al operatorului și costul complet pe luni pentru a demonstra sustenabilitatea.

5. COMPLEMENTARE: 1SERVICIU×24COPII MIN /5SERVICII×24 MAX
Fiecare serviciu are minimum2grupe, deci2×12preșcolari respectă atât pragul conservator dinGSCS, cât și HG1563(min10,max20). Tipul grădiniță comunitară vizează4–6ani; sub4ani necesită alegerea tipului legal adecvat și verificarea încadrării. Fiecare dintre cele5servicii trebuie legat de o unitate școlară acreditată și să aibă aprobări/înregistrare corespunzătoare.
Program4h/zi este posibil: HG1563art8 permite flexibilitate pânăla5h, excepțional10h pentruproiecteUE. Programul-cadru se aprobă deISJ. Cele4hcu copiii nu epuizează timpul de muncă: pregătire, evidență, familie, evaluare, igienă, predare/preluare, pauze, absențe și înlocuiri se includ explicit.
Art26 admite douăcadre calificate ori cadru+pedagogșcolar/instructor-animator/instructor pentrueducațieextrașcolară. Nu este permisă substituirea cu orice îngrijitor/voluntar ori certificatgeneric de animator. Diplomă, calificare pentrufuncție și act deîncadrare se validează nominal deoperator/ISJ. Art27: angajarea didactică prinCIMdeterminat/platăcuora, auxiliare princumul, concedii legale; convențiePFA nu se presupune substitut conform. Personalul administrativ se normează deangajator potrivitlegii. Alimentație, curățenie, sănătate și înlocuiri nu dispar la program4h; se pot asigura prinresurse existente/servicii doar peangajamente clare.
Art18 impune spații distincte, minimum2săli, zonăexterioară, vestiar și centru deresurse pentrupărinți; grădinița comunitară are cerințe pentru masă. Disponibilitatea unei camere nu demonstrează autorizabilitatea serviciului. CES impune adaptări pe nevoi, nu generic15camere identice.
Art11 păstrează structura anuluișcolar; plata10luni nu autorizează încetarea funcționării după10luni. Calendarul trebuie să arate lunile/zilele de activitate, vacanțele, concediile și sursa restuluidecost. Nu se presupune automat obligație de12luni×21zile pentrutoți copiii; dar trebuie acoperită continuitatea potrivit programului aprobat și durabilitatea3ani. MIN standard9luni și complementar10luni au nevoie deplanul tranziției și finanțării neacoperite. Nu se folosesc luni fictive pentruatingerea pragului201.000euro.

6. FORMARE ȘI DOTĂRI – CORECȚII DE DIMENSIONARE
GSCS A1.4 vizează personalul încadrat înservicii nouînființate/extinse. 120participanți nu sunt justificabili numai prinexistența1530copiiînserviciistandard. ScenariulA: formare pentru personalul efectiv încadrat în5servicii complementare, număr stabilit prinstate defuncții și evaluaredenevoi. ScenariulB:120numai dacă se documentează și extinderi standard cu minimumogrupănouă și120persoaneeligibile distincte, fiecare cu rol/angajare/competențe/ore. Cursurile suplimentare nu trebuie repetări inutile ale formărilor deja finanțate.
Primădotarea standard pe costreal este permisă pentru înființare/extindere, distinct de funcționarea acoperită de barem. 300locuri mobilier fațăde120locurinoi complementare lasă180locuri fărăjustificare până la fișe de extindere.20locații și15camereCES fațăde5servicii nu sunt automat ilegale, dar nu au legătura cantitativă dovedită. Fișapentru fiecarepoziție: operator/adresă/titluasupraimobilului, capacitateînainte/după, grupe noi, inventarexistent, deficit, beneficiarifolositori, utilitate, normativ, ofertă, sursăanterioarădefinanțare.
Risculdubleifinanțări este concret: HCL50/2026 mobilier/materiale/echipamentePNRR4188; HCL78/2026 materiale pentrucabineteasistențăpsihopedagogică PNRR; HCL242/2026 echipamenteIT dinproiect107777 cătreLiceulTehnologic și ȘcoalaMihailKogălniceanu. Sunt arhivatePDF33/11/5pagini. Achiziția similară nu înseamnă automat dublăfinanțare, dar trebuie confruntate inventarul și destinația/sala/capacitatea, cu justificarea deficituluirezidual. Fără aceasta, liniiledebuget se marchează condiționate; nu mutăm economiile înaltecosturi doar pentruapăstrarea plafonului.

7. MATRICE CERINȚĂ – DOVADĂ – VERDICT – RESPONSABIL
E01 EligibilitateONG peeducațietimpurie | contract/raport recepționat,min1proiectultimii3ani înariaGSCS | DESCHIS | ONG/jurist.
E02 Operatoractual | HCL235,OM5594,extrasSIIIR,acreditare,acord | PARȚIAL; HCLrecuperat | UAT/ISJ.
E03 GT65/1650 | bazeagregate2026,neînscriși/înscriși,nevoivulnerabilitate,metodologie șideduplicare | DESCHIS | DAS/școli/ONG.
E04 Capacitategrupe | matrice peadresă,vârstă,CES,cohortă,lună; totalcopiiînformațiune | DESCHIS; formula60grupeMAXnevalidată | ISJ/operator.
E05 Complementare |5respectiv1servicii,2grupefiecare,spații,minimeart18,programaprobat | DESCHIS | UAT/operator/ISJ.
E06 Personal | state,CIM,diplome,ore,pauze,concedii,înlocuiri,resurseîngrijire | DESCHIS | operator/jurist.
E07 Finanțarecontinuă | calendar9/10/12luni șibugetrest+durabilitate3ani | DESCHIS; fonduriasiguratedeuser,fărăacteanexate | UAT/economist.
E08 Formare120 | nevoidecompetențe,încadrareaînserviciinou/extins,participanțidistincți | DESCHIS,redimensionarecerută | operator/ONG.
E09 Dotări300/20/15 | planextindere,deficitrezidual/inventarPNRR,fișepoziții | DESCHIS | UAT/economist.
E10 Indicatorișipunctaj | EECO18unități×ani,rezultate>85%,Roma>50%,SIIIR,nesegregare | DESCHIS; pragurilematematiceverificate | manager/evaluator.
Niciunadintreacestecondițiideschise nu devine îndeplinită prin autoacordareapunelor sau prin presupuneri. ÎnchidereaE04trebuiesă declanșezerecalcululbugetuluișipersonalului,nu doar editareanarativului.

8. SWOT EDUCAȚIONAL
Punctetari: liderpubliccucompetențe; rețealocalărealăconfirmată; posibilitatealegală aserviciuluicomplementarflexibil; mecanismintegratcopil-familie; fonduripropriideclarateasigurate; baremulpermitebugettransparential serviciilorstandard.
Puncteslabe: lipsăcartografiere2026/GT, operatorinedesemnați; experiențaONGîneducațienedovedită; scenariulMAXnuarecapacitateși personal demonstrat; formare/dotărisupradimensionatefațădeserviciilenoidescrise; calendarnedetaliat.
Oportunități: valorificareadotărilorPNRRexistente; integrareDAS–CJRAE–școli; serviciiînzonecuaccesredusidentificateprinA1; acceslingvisticși sprijinparental; extinderistandardrealedacăexistăcerereșispațiu.
Amenințări: recrutareinsuficientă/absenteism; combinareaCEScu grupepreaîncărcate; deficitdepersonalcalificat; rețeareorganizată; întârziereavize; suprapunerecheltuieliproiecte; neatingerearezultatelor/indicatorilor; segregareprinrecrutareorientatăexclusivsprepunctaj.
Răspuns: alegereascenariuluidupăbazeprimare; operaționalizareșiresurse înainteaasumăriiscorului; valorificareinventareexistente și achizițiedoarpentrudeficituljustificat; monitorizareprezență/planuridesprijinindividual; auditlunarcapacitate-ore-activități-copii.

9. ÎNTREBĂRI PRECISE PENTRU ÎNCHIDERE
1.Care unitate acreditatăvaopera fiecare serviciu, dupăHCL235/2026, cucecodSIIIR și adresă?
2.Ce număr real de copii3luni–6ani există în2026,pean devârstă și localitate, înscriși/neînscriși,vulnerabilitate și cereri neacoperite? Date agregate inițial;fărălistenominaleînraportpublic.
3.Sunt1.650copii unici simultani saucohorteseccesive? Careluni exact primește fiecarecohortăserviciile12luni, înproiect24luni?
4.Cum se distribuie224CES și copiii cuasistențăsuplimentarăpegrupe? Cinecertificăcapacitatea ajustată, normași supravegherea?
5.Ce vârsteau7ante MIN? Cegrupeexistente/noi conțin34pre? Suntderogări aprobate necesare?
6.Cele5serviciicomplementare suntgrădinițicomunitare4–6ani saualtetipuri? Există2săli/serviciu,zonaexterioară,vestiar,masă,accesibilitateși titludeutilizare?
7.Cineasigurăînlocuirea,igiena,masa șisănătatea lacomplementare4h? CeCIM/qualificăriși bugetîntregevidențiate?
8.Ce120angajați suntîncadrațiînserviciinou/extinseși necesităceformare? Caresuntgrupele standardefectivnoucreate?
9.Care180locurisupplementare justificămobilierul300?Unde sunt20locații/15camereCESși cedeficitrămâne dupăPNRR4188/proiect107777?
10.CareHCL/angajamentbugetarfinanțeazăluniineacoperiteșitreianidurabilitate? Cândîncepșiseîncheieoperarea/calendarulanuluișcolar?
11.Ce10unitățidistincte potraporta20EECO18peste2ani? CareplanSIIIRpentru5SR09?
12.CaresuntdovezileexperiențeieducaționaleONGînultimii3ani? ServiciuldevârstniciROSEsingurnuacoperăaceastăcerință.

10. CONDIȚIE PENTRU AUDIT 10/10
Se potînchide acum eroriledeformulă,versiuninormative,tipurideactivități șidenumireoperator. Nu potfi închise fărădovezi E01–E10. Runda3trebuie săprimeascămatriceagrupelorșiaprobareoperator/ISJ,fișelespațiilor/inventarelorși planfinanciar;apoi seface recalculindependent,verificareaîncadrăriiînGSCSși reevaluareapunctajului. Aforța10/10înainteadovezilorarascunde riscurileidentificate.

SURSE OFICIALE LOCALE (copii înacestfolder)
https://www.primariasebes.ro/wp-content/uploads/2025/12/hcl-392-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/09/hcl-235-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2022/10/SIDU_Sebes-2021-2030.pdf
https://www.liceulgermansebes.ro/inscrieregradi.html
https://www.primariasebes.ro/wp-content/uploads/2026/03/hcl-50-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/03/hcl-78-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/09/hcl-242-site.pdf
Norme:https://legislatie.just.ro/Public/DetaliiDocument/292195 ; https://legislatie.just.ro/Public/DetaliiDocument/306009
GSCS și grila: documentele oficiale locale din1.DOCUMENTEOFFICIALE; extrasele în3.1.
'''
text='''AUDIT EDUCAȚIONAL, FEZABILITATE ȘI SWOT – RUNDA 2
07.10.2026 | Lider: Municipiul Sebeș | Partener propus: Asociația ROMANIAN SOUL ENTITY, CUI 29433614

VERDICT
Varianta minimă poate fi dimensionată, dar depinde încă de operator, grupe, spațiu și situația copiilor. Varianta maximă de 1.650 copii nu are demonstrația capacității locale, a grupului vulnerabil și a resurselor. Nu poate primi onest verdict final 10/10. Fondurile asigurate de beneficiar nu înlocuiesc aprobările, resursa umană sau dovada nevoii. Buget maxim de lucru comunicat: 26.272.446 lei; plafon legal: 26.292.000 lei. Apropierea de plafon nu justifică cheltuielile. Acesta este audit intern de pregătire, nu punctaj oficial AM.

1. DOMENIUL VERIFICĂRII
Am citit detaliat secțiunile GSCS despre activități, grup țintă, indicatori, bareme, dotări și formare, plus grila. Din HG 1563/2024 am verificat constituirea, programul, anul școlar, spațiile, evaluarea și personalul. Efectivele art. 23 și posturile art. 207 din Legea 198 sunt confirmate de jurist pe forma 18.01.2026; certificarea ultimei consolidări din septembrie 2026 rămâne deschisă. Forma de bază nu este tratată drept text actual.
Am citit vizual toate paginile HCL 392/2025 și HCL 235/2026, scanate. Din SIDU am citit capitolul de educație și tabelele 23–26, nu toate cele 219 pagini. Pagina Liceului German pentru înscriere 2026–2027 a fost citită integral. Pentru HCL 50/78/242 am verificat titlul și pagini din dispozitiv; anexele de inventar nu au fost încă confruntate articol cu articol. Arhivarea integrală nu înseamnă auditarea integrală.

2. REȚEAUA ȘCOLARĂ ACTUALĂ
HCL 235/09.09.2026 actualizează situația din HCL 392/22.12.2025 și se bazează pe OM 5594/31.08.2026. Anexa include:
• LPS Florin Fleșeriu: GPP nr. 4 și GPN nr. 6;
• Școala Gimnazială Petrești: GPN și GPP Petrești;
• Liceul German: GPP Germană Petrești; pagina școlii prezintă și alte locații proprii;
• Școala Mihail Kogălniceanu: Școala Silviu Cărpinișian, GPN Lancrăm, GPN nr. 8, GPP nr. 7;
• Școala nr. 2: GPN Răhău și Școala Răhău;
• Grădinița Copiilor Voioși, cu personalitate juridică: Creșa Copiilor Voioși, GPP nr. 2 și GPP nr. 3;
• grădinițele particulare Heidi, Sfântul Nicolae și Mirela;
• Colegiul Lucian Blaga, Liceul Tehnologic și Școala Postliceală Henri Coandă. Prezența în rețea nu demonstrează nivel eligibil de educație timpurie pentru fiecare entitate.
Lista identifică entități reale, fără a le desemna parteneri sau locații ale proiectului. Paginile vechi ale Școlii nr. 2 și Liceului Tehnologic nu sunt suficiente pentru identificarea operatorului actual. Se cer OM 5594 cu anexele și extras SIIIR actual.
EECO18=20 poate reprezenta, în condițiile definiției din ghid, 10 unități sprijinite în doi ani școlari succesivi. Nu înseamnă automat 20 operatori sau spații. Nu sunt confirmate încă 10 unități eligibile distincte. Grupele, serviciile și locațiile nu multiplică arbitrar unitățile raportabile.

3. CAPACITATEA ȘI GRUPUL ȚINTĂ
Liceul German publică pentru 2026–2027: 28 locuri antepreșcolare și 124 preșcolare. Cele 152 sunt locuri aprobate, nu locuri libere sau copii vulnerabili eligibili PEO. Datele preced reorganizarea din septembrie și trebuie confirmate.
SIDU indică 1.161 copii înscriși în grădinițe în 2020, după 760 în 2019. Saltul seriei și vechimea nu permit estimarea sigură a GT 2026. Propunerea de 1.380 preșcolari, dintre care 1.260 standard și 120 complementar, depășește reperul istoric cu 219. Aceasta impune verificare, fără a demonstra singură imposibilitatea. Copiii noi din anul al doilea se pot număra distinct; aceeași persoană nu se renumără. Calendarul trebuie să susțină durata finanțată pentru fiecare cohortă.
Nu există încă dovezi pentru 826 copii romi, 224 CES sau 1.452 rezultate. Etnia nu se deduce din adresă/nume; este necesară documentarea legală și voluntară. CES se documentează distinct. Recrutarea nu trebuie să producă segregare. Pragurile de punctaj: pentru 65 copii, peste 50% romi înseamnă 33 și peste 85% rezultate înseamnă 56; pentru 1.650, pragurile sunt 826 și 1.403. 58/65 și 1.452/1.650 sunt ținte propuse, nu rezultate constatate.

4. EFECTIVE, COHORTE ȘI PERSONAL
Referința verificată de jurist, art. 23: ante grupa mică medie 9/minim 7/maxim 11; mijlocie 14/10/17; mare 16/10/22; preșcolar 17/12/22. Limita 26 nu este generală: presupune derogare individuală +4 aprobată. Art. 23(9) reduce maximul cu 3 pentru fiecare copil CES integrat. Se verifică separat regulile despre medie și constituire; o sumă agregată nu certifică grupele.
MIN: cei 7 ante pot constitui o grupă mică dacă vârstele și aprobările permit. Nu pot constitui automat o grupă mijlocie/mare de 7. Cei 34 pre pot ocupa aritmetic 2 grupe de 17, dar regula actuală privind constituirea peste medie și cel mult o grupă sub medie/nivel/PJ trebuie verificată. Nu declarăm automat legală formula 2×17. Dacă sunt copii din grupe existente, contează efectivul TOTAL al grupelor, inclusiv copiii care nu sunt finanțați prin proiect.
MAX: 60 grupe ×21 copii =1.260 nu absorb 224 CES simultan. Dacă toți cei 224 CES sunt în aceste grupe, condiția necesară este G≥ceil((1260+3×224)/22)=88 grupe. Fără CES: minimum 58. Formula se aplică fiecărei cohorte simultane și fiecărei locații. Două cohorte de 630 copii cu 112 CES fiecare ar necesita minimum 44 grupe simultane/cohortă, dar 12 luni pentru fiecare cohortă consecutivă consumă 24 luni de serviciu, fără timp de pregătire. Nu se presupune că încap într-un proiect de 24 luni.
Pentru 270 ante simultan, fără CES, limitele aritmetice sunt 25 grupe dacă toți sunt mici, 16 dacă toți sunt mijlocii, 13 dacă toți sunt mari. Mixul de vârste, spațiile și CES pot crește necesarul. Art. 207(4) indică un post/grupă normală și două/grupă prelungită; se confirmă încadrarea și norma orară actuală. Salariile standard sunt incluse în barem, dar statul de funcții și costul complet al operatorului sunt indispensabile pentru fezabilitate.

5. COMPLEMENTARE: 24 COPII MIN /120 MAX
Fiecare serviciu necesită minimum două grupe. Modelul 2×12 respectă pragul conservator GSCS și intervalul HG 1563 de 10–20 copii. Grădinița comunitară vizează 4–6 ani; pentru copii sub 4 ani se verifică tipul complementar adecvat. Fiecare serviciu trebuie asociat unei unități acreditate și aprobat/înregistrat legal.
Programul de 4 ore/zi este posibil: art. 8 permite flexibilitate până la 5 ore, excepțional 10 în proiecte UE. Programul-cadru se aprobă de ISJ. Cele 4 ore cu copiii nu includ automat toate sarcinile de muncă: pregătire, evidență, comunicare, igienă, primire/predare, pauze și înlocuiri.
Art. 26 admite două cadre calificate ori un cadru plus pedagog școlar/instructor-animator/instructor pentru educație extrașcolară. Un îngrijitor, voluntar sau certificat generic de animator nu este substitut automat. Diplomele și calificarea pentru funcție se verifică nominal de operator/ISJ. Art. 27 prevede CIM determinat/plată cu ora pentru predare și cumul pentru auxiliar, plus concediile legale. Nu se presupune că PFA substituie aceste forme. Administrativul se normează de angajator. Masa, curățenia, sănătatea și înlocuirile trebuie asigurate, inclusiv prin resurse existente documentate.
Art. 18 impune minimum două săli, spațiu exterior, vestiar și centru de resurse pentru părinți, precum și condițiile de masă pentru grădinița comunitară. O singură cameră disponibilă nu dovedește autorizabilitatea. Adaptările CES se bazează pe nevoi, nu pe 15 camere identice presupuse.
Art. 11 păstrează structura anului școlar. Finanțarea a 10 luni nu autorizează închiderea arbitrară după 10 luni. Calendarul trebuie să arate activitatea, vacanțele, concediile și sursa costurilor rămase. Nu presupunem automat 12 luni×21 zile pentru toți copiii, dar continuitatea programului aprobat și durabilitatea de 3 ani trebuie asigurate. MIN standard 9 luni/complementar 10 luni necesită plan de tranziție și finanțare pentru rest. Nu se folosesc luni fictive pentru pragul de 201.000 euro.

6. FORMARE, DOTĂRI ȘI FINANȚĂRI ANTERIOARE
A1.4 finanțează personalul încadrat în servicii nou înființate/extinse. 120 participanți nu se justifică doar prin cei 1.530 copii din servicii standard existente. Scenariul A: formare pentru personalul efectiv al celor 5 complementare, stabilit prin state și analiza nevoilor. Scenariul B: 120 numai dacă se demonstrează și extinderi standard reale cu minimum o grupă nouă și 120 persoane eligibile, cu rol, încadrare și nevoi individuale. Se evită repetarea inutilă a formărilor deja finanțate.
GSCS permite primă dotare standard pe cost real pentru înființare/extindere; funcționarea este acoperită de barem. Mobilierul pentru 300 locuri versus 120 noi complementare lasă 180 fără justificare până la fișe de extindere. Cele 20 locații și 15 camere CES nu sunt automat ilegale, dar nu au legătura cantitativă dovedită. Fiecare poziție necesită adresă/operator, drept de utilizare, capacitate înainte/după, grupe noi, inventar, deficit, utilizatori, normativ, oferte și surse anterioare.
Riscul suprapunerii este concret: HCL 50/2026 transferă mobilier/materiale/echipamente PNRR 4188; HCL 78/2026 transferă materiale pentru cabinete de asistență psihopedagogică; HCL 242/2026 transferă IT din proiectul 107777 către Liceul Tehnologic și Școala Mihail Kogălniceanu. PDF-urile de 33/11/5 pagini sunt arhivate. Achiziția similară nu înseamnă automat dublă finanțare, dar trebuie demonstrat deficitul rezidual pe sală/capacitate. Până atunci liniile rămân condiționate. Economiile nu se mută artificial pentru păstrarea plafonului.

7. MATRICEA CERINȚELOR ȘI DOVEZILOR
E01 Experiență ONG: contract și raport recepționat, minimum un proiect în ultimii 3 ani în aria GSCS. DESCHIS. Responsabil ONG/jurist.
E02 Operator: HCL actual, OM 5594, SIIIR, acreditare, acord. PARȚIAL: HCL recuperat. Responsabil UAT/ISJ.
E03 GT: baze agregate 2026, înscriși/neînscriși, vulnerabilitate, metodologie, deduplicare. DESCHIS. DAS/școli/ONG.
E04 Capacitate: matrice adresă–vârstă–CES–cohortă–lună și efectiv total al grupei. DESCHIS. ISJ/operator.
E05 Complementare: spații, minimum două grupe, cerințe art. 18, program aprobat. DESCHIS. UAT/operator/ISJ.
E06 Personal: state, CIM, diplome, ore, concedii, înlocuiri, îngrijire. DESCHIS. Operator/jurist.
E07 Continuitate: calendar și buget pentru lunile neacoperite plus durabilitate. DESCHIS: fonduri declarate asigurate, fără acte anexate. UAT/economist.
E08 Formare: încadrare în servicii noi/extinse și nevoi de competențe. DESCHIS, redimensionare necesară. Operator/ONG.
E09 Dotări: extindere, deficit rezidual, inventare PNRR, fișe individuale. DESCHIS. UAT/economist.
E10 Indicatori: unități×ani EECO18, rezultate, structură GT, SIIIR, nesegregare. DESCHIS; pragurile matematice verificate. Manager/evaluator.
Închiderea E04 declanșează recalcularea bugetului și personalului, nu doar schimbarea textului.

8. SWOT EDUCAȚIONAL
Puncte tari: lider public competent; rețea locală confirmată; program complementar flexibil legal; intervenție copil–familie; fonduri proprii declarate; bareme transparente.
Puncte slabe: lipsă cartografiere 2026 și operatori desemnați; experiență educațională ONG nedovedită; capacitate/personal MAX neconfirmate; dotări/formare fără fundamentare completă; calendar incomplet.
Oportunități: valorificarea dotărilor PNRR existente; colaborare DAS–CJRAE–școli; servicii în zone cu acces redus; sprijin lingvistic și parental; extinderi reale unde există cerere și spații.
Amenințări: recrutare insuficientă, absenteism, încărcare excesivă a grupelor cu CES, deficit de personal calificat, reorganizarea rețelei, avize întârziate, suprapunerea finanțărilor, rezultate sub ținte și segregare.
Răspuns: selectarea scenariului după date primare; resurse și funcționare demonstrate înainte de asumarea punctajului; achiziție numai pentru deficitul justificat; monitorizarea prezenței și sprijin individual; verificare lunară copii–grupe–ore–costuri.

9. ÎNTREBĂRI PENTRU ÎNCHIDERE
1. Ce unitate acreditată operează fiecare serviciu după HCL 235/2026, cu ce cod SIIIR și adresă?
2. Câți copii eligibili există în 2026, pe vârstă/localitate, înscriși/neînscriși, vulnerabilitate și cereri neacoperite? Inițial date agregate, fără liste nominale în raportul public.
3. Cei 1.650 sunt simultani sau în cohorte? Care luni exacte asigură fiecăruia cele 12 luni standard în proiectul de 24 luni?
4. Cum se distribuie cei 224 CES? Cine certifică efectivele ajustate, norma și supravegherea?
5. Ce vârste au cei 7 ante MIN? În ce grupe sunt cei 34 pre și ce derogări sunt necesare?
6. Ce tip legal au cele 5 complementare? Există două săli/serviciu, exterior, vestiar, masă, accesibilitate și drept de utilizare?
7. Cine asigură înlocuirea, igiena, masa și sănătatea? Cu ce calificări, contracte și cost complet?
8. Care sunt cei 120 angajați eligibili pentru formare și grupele standard efectiv nou create?
9. Ce extinderi justifică 180 locuri suplimentare? Unde sunt 20 locații/15 camere și ce lipsește după PNRR 4188/proiectul 107777?
10. Ce acte finanțează lunile neacoperite și cei 3 ani de durabilitate? Care este calendarul real?
11. Ce 10 unități distincte susțin EECO18=20 în doi ani și cum se verifică rezultatele SIIIR?
12. Ce documente probează experiența educațională ONG în ultimii 3 ani? Serviciul ROSE pentru vârstnici nu acoperă singur cerința.

10. CONDIȚIE PENTRU VERDICT 10/10
Se pot remedia acum formulele, versiunile surselor și operatorii. Condițiile E01–E10 nu se închid fără dovezi. Runda următoare necesită matricea grupelor confirmată de operator/ISJ, fișele spațiilor/inventarelor și planul financiar. Urmează recalcul independent și reevaluarea punctajului. A acorda 10/10 înaintea acestor dovezi ar ascunde riscurile găsite.

SURSE OFICIALE ARHIVATE
https://www.primariasebes.ro/wp-content/uploads/2025/12/hcl-392-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/09/hcl-235-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2022/10/SIDU_Sebes-2021-2030.pdf
https://www.liceulgermansebes.ro/inscrieregradi.html
https://www.primariasebes.ro/wp-content/uploads/2026/03/hcl-50-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/03/hcl-78-site.pdf
https://www.primariasebes.ro/wp-content/uploads/2026/09/hcl-242-site.pdf
Norme: https://legislatie.just.ro/Public/DetaliiDocument/292195 și https://legislatie.just.ro/Public/DetaliiDocument/306009
GSCS și grila: documentele oficiale din folderul proiectului; extrase în 3.1.
'''
# Preserve readable output and harmonize numeric labels.
replacements={'10/10':'10/10','20operatori':'20 operatori','20spații':'20 spații','10unități':'10 unități','5servicii':'5 servicii','120participanți':'120 participanți','300locuri':'300 locuri','120locuri':'120 locuri','180locuri':'180 locuri','20locații':'20 locații','15camere':'15 camere','224CES':'224 CES','1260':'1.260','1650':'1.650','65copii':'65 copii','7ante':'7 ante','34pre':'34 pre','2grupe':'2 grupe','88grupe':'88 grupe','60grupe':'60 grupe','44grupe':'44 grupe','26grupe':'26 grupe','12luni':'12 luni','24luni':'24 luni','10luni':'10 luni','9luni':'9 luni','3ani':'3 ani','4h':'4 h','5h':'5 h','10h':'10 h','art23':'art. 23','art207':'art. 207','art26':'art. 26','art27':'art. 27','art18':'art. 18','HG1563':'HG 1563','Legea198':'Legea 198','HCL235':'HCL 235','HCL392':'HCL 392','HCL78':'HCL 78','HCL50':'HCL 50','HCL242':'HCL 242'}
for a,b in replacements.items():text=text.replace(a,b)
(D/'Audit_educational_Runda2.txt').write_text(text,encoding='utf-8-sig')
(D/'Audit_educational_Runda2.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Audit educațional Sebeș</title><style>body{max-width:1050px;margin:40px auto;padding:20px;font:16px/1.6 system-ui;color:#173047}pre{white-space:pre-wrap;font:inherit}a{color:#116d92}</style><h1>Audit educațional și SWOT · Runda 2</h1><pre>'+html.escape(text)+'</pre></html>',encoding='utf-8-sig')
reg=[]
for p in D.glob('*.pdf'):
 r=PdfReader(p);reg.append({'file':p.name,'bytes':p.stat().st_size,'pages':len(r.pages),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'Registru_validare_surse.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8-sig')
print(str(D));print('Raport',len(text),'caractere; PDF',len(reg))
