const fs = require('fs');
const path = require('path');
const root = 'D:/CodexWork/eva-audit-p01-readonly-20261101';
const dest = '\\\\192.168.100.169\\Comun\\00.Roboti\\EVA.Pro\\Eva-contab\\Audit_P01_2026-11-01\\A01_plan.json';
const sha = '76470fedb51e273012e137c4c5847ec41a849848';
const P = {
 auth:'backend/app/auth.py', login:'backend/app/routers/auth.py', middleware:'backend/app/middleware.py',
 tenant:'backend/app/idempiere/tenant_authz.py', perms:'backend/app/idempiere/perms.py', map:'backend/app/idempiere/client_map_migration.py',
 identity:'backend/app/idempiere/cabinet_identity.py', iam:'backend/app/routers/iam.py', admin:'backend/app/routers/admin_users.py',
 cabinets:'backend/app/routers/cabinets.py', tenants:'backend/app/routers/tenants.py', stores:'backend/app/routers/stores.py',
 data:'backend/app/routers/idempiere_data.py', meta:'backend/app/routers/idempiere_meta.py', remote:'backend/app/routers/idempiere_remote.py',
 reports:'backend/app/routers/reports.py', exports:'backend/app/routers/export.py', documents:'backend/app/routers/documente.py',
 office:'backend/app/routers/office.py', models:'backend/app/models.py', front:'frontend/app.py',
 loginUI:'frontend/portal/eva_login.html', usersUI:'frontend/portal/eva_users.html', cabinetsUI:'frontend/portal/eva_cabinets.html',
 noFirmUI:'frontend/portal/eva_fara_firma.html', firmsUI:'frontend/portal/eva_admin_firme.html'
};
const j = 'idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/';
Object.assign(P, {
 access:j+'acces/AccesGestiune.java', accessTables:j+'acces/AccesTabele.java', mobileGuard:j+'acces/GardaMobil.java', mobileToken:j+'acces/JetonMobil.java',
 mobileDevice:j+'acces/DispozitivMobil.java', mobileLog:j+'acces/JurnalMobil.java', mobileApi:j+'acces/ApiMobil.java',
 inventoryApi:j+'acces/ApiInventar.java', packingApi:j+'acces/ApiAmbalare.java', mobileForm:j+'form/WEvaAccesMobilForm.java',
 userForm:j+'form/WSagaUtilizatoriForm.java', wmsGuard:j+'wms/GardaWms.java', auditGuard:j+'audit/GardaAudit.java',
 accessReview:j+'audit/administrare/AuditRecertificaAcces.java', firmIdentity:j+'corelare/IdentitateFirma.java',
 site:j+'corelare/ApiSite.java', siteProducts:j+'corelare/ApiSiteProduse.java', b2b:j+'corelare/CanalB2B.java',
 channels:j+'corelare/OperatiiCanale.java', salesChannel:j+'corelare/VanzariPeCanal.java', b2bForm:j+'form/WEvaCanalB2BForm.java',
 salesForm:j+'form/WEvaVanzariPeCanalForm.java', channelForm:j+'form/DialogCanal.java', channelPanel:j+'form/PanouCanale.java'
});
const basePrereq = ['GATE-A11: planul integrat este aprobat explicit 10/10; înainte de aprobare nu se execută controlul.', 'Mediu de test izolat, identități și date sintetice autorizate; fără efecte în producție sau la parteneri.', 'Versiunea executată și schema sunt identificate; abaterea față de SHA de referință se înregistrează înainte de concluzie.'];
const controls = [];
function add(n, title, criterion, sources, steps, expected, negative, db, native, ux, owners, prereq=[], kind='REVIZIE_COD + TEST_INTEGRARE_IZOLAT + UI_MANUAL + SQL_READ_ONLY') {
 const id = `A01.C${String(n).padStart(2,'0')}`;
 controls.push({id, titlu:title, obiectiv:criterion, criteriu_exact:criterion, proprietar:'A01', co_verificatori:owners, stare:'NEEXECUTAT', tip_proba:kind,
  prerechizite:[...basePrereq,...prereq], pasi:steps.map((text,i)=>({pas:i+1,activitate:text})), rezultat_asteptat:expected, scenariu_negativ:negative,
  surse_candidate_de_confirmat:sources, evidence:{
   FE:{cerut:'Captură înainte/după, adresă canonică și contextul vizibil; cererile reale ale interfeței se corelează cu API.', surse_candidate:sources.filter(s=>s.startsWith('frontend/')||s.includes('/form/')), lipsa_interfetei:'Dacă nu există ecran propriu, se folosește interfața apelantă identificată în pipeline; N/A necesită justificare și verificare A11.'},
   BE:{cerut:'Traseu complet de autorizare cu fișier:linie, intrare/ieșire mascată, actor și context rezolvat; probe pozitive și negative.',surse_candidate:sources.filter(s=>!s.startsWith('frontend/'))},
   DB:{cerut:db, metoda:'Interogare numai citire cu aceleași filtre tenant/rol; se consemnează diferența înainte/după și absența efectelor în alte firme.'},
   UX:{cerut:ux},
   native:{cerut:native, comparatie_obligatorie:'NR-01: sursa iDempiere nativă identificată/pinuită + metadatele și comportamentul instanței instalate; codul EVA se mapează separat.'}
  }, criteriu_inchidere:'Rezultat efectiv + probe FE/BE/DB/UX/native sau N/A justificat și acceptat de A11; fiecare abatere are finding și trasabilitate task. Existența unui test în repo nu este probă de execuție.', rezultat_efectiv:null, evidence_ids:[], finding_ids:[]});
}
add(1,'Inventar complet de suprafețe și puncte de autorizare',
 'Fiecare rută activă, metodă, formular, proces, export și operație de fundal din domeniu are actor, context, politică și punct de control server identificabile; nicio suprafață nu rămâne implicit exclusă.',
 [P.middleware,P.login,P.iam,P.cabinets,P.stores,P.data,P.meta,P.remote,P.mobileApi,P.site,P.front],
 ['Extrage inventarul din routere/middleware, registrul de servicii Java și configurarea deploymentului; distinge activ/inactiv/necunoscut cu probă.', 'Construiește registrul endpoint→metodă→autentificare→autorizare→tenant→owner și numără denominatorul.', 'Corelează fiecare intrare activă cu minimum un control și un pipeline; examinează rute alternative, slash final, metode HEAD/OPTIONS și versiuni.', 'După gate, eșantionează numai pentru validarea inventarului; acoperirea exhaustivă de politici nu se substituie cu eșantionul.'],
 '100% din suprafețele active inventariate au control și owner; cele necunoscute sunt BLOCAT, nu eliminate din denominator.',
 'Apel direct la o rută absentă din meniu și metodă alternativă fără sesiune; accesul nu este permis prin lipsa interfeței.',
 'Inventar AD_Form/AD_Window/AD_Process/AD_Menu și tabelele de acces; compară active/inactive cu expunerea gateway.',
 'AD_Role, AD_Form_Access, AD_Window_Access, AD_Process_Access și rolurile efectiv instalate.',
 'Meniurile ascund acțiunile nepermise și accesul direct rămâne controlat server; răspunsul permite revenirea sigură.', ['A02','A09','A10']);
add(2,'Login, parole și recuperare fără enumerare',
 'Loginul validează parola prin mecanismul configurat, nu divulgă existența contului prin corpul răspunsului și nu permite încercări necontrolate; politica de recuperare/parole este documentată înainte de a fi evaluată.',
 [P.auth,P.login,P.loginUI,P.front,P.models],
 ['Inventariază algoritmul de hash, parametrii și fluxul de creare/schimbare/recuperare; identifică politica aprobată.', 'În mediul izolat compară cont existent/parolă greșită și cont inexistent; verifică răspunsul și mesajele UI.', 'Verifică limitarea încercărilor printr-un număr mic de probe controlate; nu face test de volum.', 'Inspectează numai metadatele stocării hashului, niciodată parole sau hashuri reale în raport.'],
 'Parola nu apare în stocare/log în clar; erorile nu enumeră conturi; politica de încercări/recuperare este aplicată și măsurată.',
 'Cont inexistent, parolă goală/lungă, reset pentru alt cont și încercare după blocare temporară.',
 'iam_credentials: tipul câmpurilor și metadatele hashului pentru identități sintetice; nicio extragere a credentialelor reale.',
 'Identifică mecanismul nativ AD_User/Login și justificarea oricărei parole duplicate în gateway.',
 'Mesaje în română, focalizare accesibilă pe eroare, nu se pierde utilizatorul introdus și parola nu se reafișează.', ['A09','A10'], ['Politica aprobată pentru parole, recuperare, rate limit și retenție; lipsa ei se raportează drept decizie necesară, fără prag inventat.']);
add(3,'Integritatea și separarea tokenurilor',
 'Un token modificat, expirat, cu tip greșit sau context nepermis nu autorizează nicio operație; cheia/algoritmul și eventualele audience/issuer sunt validate conform contractului explicit.',
 [P.auth,P.login,P.middleware,P.tenant],
 ['Documentează claims, semnătura, tipurile access/refresh/service/mobile și contractele de validare.', 'Testează token sintetic valid versus payload/semnătură modificate, expirat și tip schimbat.', 'Tracează transformarea claims→utilizator→cabinet→firmă; nu accepta claims necorelate cu politica server.', 'Verifică lipsa tokenurilor în URL, log, capturi și mesaje de eroare.'],
 'Numai tipul permis și identitatea/contextul verificate ajung la operație; respingerea precede orice efect.',
 'Refresh folosit ca access, access de alt cabinet, algoritm nepermis și schimbarea claimului de rol.',
 'iam_credentials.token_epoch și legătura iam_users/managing_firms/firm_access; zero modificări business la respingere.',
 'Mapează tokenul EVA la sesiunea/rolul nativ; nu presupune că autentificarea gateway înlocuiește AD_Role.',
 'Sesiunea expirată conduce la autentificare fără reluarea automată a unei operații distructive.', ['A10']);
add(4,'Refresh concurent, reutilizare și revocare',
 'Reîmprospătarea tokenului respectă politica documentată de expirare/rotație/revocare și nu reînnoiește accesul după revocare; două cereri simultane nu resuscitează o sesiune revocată.',
 [P.login,P.auth,P.models,P.front],
 ['Urmărește /auth/refresh, validarea epoch și politica de reutilizare.', 'Execută în fixture refresh valid, expirat și după logout-all/dezactivare.', 'Coordonează două refreshuri simultane cu barieră și apoi revocare; verifică ambele rezultate și accesul ulterior.', 'Verifică retryul UI după timeout și lipsa buclei infinite de refresh.'],
 'Sesiunile revocate rămân revocate; comportamentul tokenurilor concurente este determinist și conform politicii explicite.',
 'Refresh vechi după schimbarea parolei și refresh paralel cu dezactivarea contului.',
 'Snapshot token_epoch și status utilizator înainte/după; nu păstra tokenurile în raport.',
 'Verifică dacă sesiunea AD_Session asociată este invalidată/sincronizată; documentează orice limită nativă.',
 'Un singur flux clar de reautentificare; datele firmei anterioare nu mai rămân interactive.', ['A09','A10'], ['Politica refresh/rotație acceptată; dacă rotația nu este cerută, nu o declara automat obligație, dar dovedește revocarea.']);
add(5,'Revocare integrală portal–native–mobil',
 'Schimbarea parolei, logout-all, dezactivarea utilizatorului/firmei și eliminarea rolului produc efectul de revocare aprobat în toate suprafețele, inclusiv sesiuni deja deschise.',
 [P.login,P.admin,P.identity,P.mobileGuard,P.mobileToken,P.mobileDevice,P.remote],
 ['Definește pentru fiecare eveniment ce sesiuni și drepturi trebuie invalidate și limita temporală aprobată.', 'Deschide sesiuni sintetice portal, native și mobil; aplică pe rând evenimentele autorizate în mediul izolat.', 'Repetă citire și operație nouă din fiecare sesiune; verifică și o filă inactivă reactivată.', 'Compară timestampul revocării cu primul refuz și cu logurile de sincronizare.'],
 'Nicio sesiune nu păstrează drepturi eliminate peste limita aprobată; lipsa sincronizării este finding explicit.',
 'Cont dezactivat cu token încă neexpirat și rol eliminat în timp ce formularul nativ este deschis.',
 'iam_users/iam_credentials, AD_User.IsActive, AD_Role.IsActive, AD_User_Roles, AD_Session; compară starea revocării.',
 'AD_Session și rolurile native sunt verificate direct, nu deduse dintr-un răspuns /auth/me.',
 'Ecranul anunță pierderea accesului fără a salva automat datele și fără a afișa alte firme.', ['A02','A09','A10']);
add(6,'MFA: înscriere, confirmare, dezactivare',
 'Dacă MFA este activat/cerut prin politică, numai utilizatorul autorizat își poate înscrie/confirma/dezactiva factorul; codurile invalide/expirate nu autentifică și secretul nu este expus după înscriere.',
 [P.login,P.auth,P.loginUI,P.models],
 ['Identifică politica MFA per rol și modul de păstrare/afișare a secretului.', 'Cu cont sintetic execută enroll→verify→login și disable autorizat.', 'Testează cod expirat/greșit, cerere fără sesiune și țintirea altui utilizator; verifică regulile de reutilizare aprobate.', 'Inspectează răspunsurile, logurile și cacheul pentru secret/QR fără a publica valorile.'],
 'Starea MFA și autorizarea sunt coerente; un cont fără politica MFA nu este inventat drept neconform, iar lipsa politicii rămâne de decis.',
 'Confirmare MFA pentru alt cont, dezactivare cu sesiune revocată și retry după timeout.',
 'Metadatele MFA din iam_credentials; secretul sintetic este mascat în probe și eliminat conform fixture cleanup.',
 'Documentează compatibilitatea cu loginul nativ și orice cale de ocolire a MFA prin acces direct la instanță.',
 'Instrucțiuni clare pentru cod expirat, accesibilitate și recuperare fără divulgarea secretului.', ['A09','A10']);
add(7,'Roluri, aliasuri și refuz implicit',
 'Rolurile super/manager/team_leader/member și aliasurile lor au drepturi explicite; un rol necunoscut, gol sau alterat nu obține privilegii administrative ori operaționale neacordate.',
 [P.perms,P.iam,P.middleware,P.identity,P.usersUI,P.userForm],
 ['Construiește matricea rol gateway→rol AD→acțiune→scope și cere ownerilor confirmarea funcțiilor de business.', 'Verifică normalize_role și toate ramurile care folosesc rol brut ori alias.', 'Testează rolurile reale, aliasurile acceptate și un rol necunoscut în fixture.', 'Compară disponibilitatea UI cu decizia /auth/can și cu autorizarea operației efective.'],
 'Aceeași politică este aplicată pe toate suprafețele; aliasul nu extinde scope și necunoscutul nu escaladează.',
 'Header/body/claim cu admin, owner, super ori rol necunoscut pentru un cont member.',
 'iam_users.role, firm_access, AD_User_Roles și drepturile native efective; nu compara numai eticheta rolului.',
 'Folosește AD_Role și tabelele de acces ca bază; extensiile EVA justifică exclusiv reguli inexistente nativ.',
 'Denumirile rolurilor de business și limitele lor sunt inteligibile; acțiunile refuzate au explicație utilă.', ['A02','A09']);
add(8,'Identitatea nu este furnizată de client prin antete',
 'X-User, X-User-Role, X-Tenant și alte antete/context client nu pot suprascrie identitatea sau privilegiile obținute din autentificarea server.',
 [P.middleware,P.auth,P.tenant,P.front,P.remote,P.mobileApi],
 ['Inventariază toate sursele de identitate/context: token, cookie, header, query, path și body.', 'Urmărește proxyul care poate introduce antete de încredere și frontiera rețelei.', 'În fixture adaugă antete contradictorii și elimină sesiunea; compară decizia server.', 'Verifică accesul direct la upstreamul disponibil în mediul de test.'],
 'Antetele neîncredere nu acordă drepturi; proxyul verifică identitatea, iar upstreamul respectă frontiera definită.',
 'Membru firmă A cu X-User-Role:super și X-Tenant:B, inclusiv prin ruta nativă.',
 'Contextul efectiv al tranzacției/recordului rămâne cel autorizat; probele DB nu conțin rânduri din B.',
 'Verifică Env/AD_Session/AD_Role în native și nu echivala un header cu un rol nativ.',
 'Schimbarea manuală a adresei/parametrilor oferă refuz coerent, nu ecran cu context fals.', ['A10']);
add(9,'Rute cabinet/CUI firmă/canal și canonicalizare',
 'Rutele /cui_cabinet, /cui_cabinet/cui_firma și /cui_cabinet/cui_firma/nume_canal identifică resursele fără să acorde acces; normalizarea CUI/slug nu produce coliziuni sau trecere în alt cabinet.',
 [P.front,P.cabinets,P.tenant,P.firmIdentity,P.stores,P.channelForm,P.channelPanel],
 ['Mapează cerința utilizatorului la rutele existente și la configurația proxy; marchează separat rutele propuse/neimplementate.', 'Testează CUI cu prefix RO/spații conform politicii și sluguri cu majuscule/diacritice/encoding/trailing slash.', 'Verifică denumire schimbată de canal, nume rezervate și două firme/canale cu nume similare.', 'Testează direct linkul cu context străin și back/forward după schimbare de firmă.'],
 'Adresă canonică univocă, control server al apartenenței și redirect sigur; implementarea incompletă nu este declarată conformă.',
 'Înlocuiește numai primul sau al doilea CUI din URL; slug codificat pentru traversal sau rută administrativă rezervată.',
 'managing_firms/managed_firms/commerce_stores și maparea cabinet→instanță→AD_Client sunt univoce.',
 'Rutele reutilizează contextul client/org nativ; CUI/slug este adresare de business, nu substitut pentru identitate AD.',
 'Breadcrumb arată cabinet→firmă→canal; linkul partajat nu deschide implicit firma curentă greșită.', ['A06','A08','A09','A10']);
add(10,'Același CUI în cabinete diferite și AD_Client_ID repetat',
 'Rezolvarea tenantului folosește identitatea cabinetului/instanței împreună cu firma; același CUI sau același AD_Client_ID numeric în două instanțe nu poate selecta datele celeilalte.',
 [P.tenant,P.map,P.cabinets,P.models],
 ['Identifică toate cheile de mapare/cache și fallbackurile pentru CUI→AD_Client.', 'Creează două cabinete sintetice cu același CUI într-o firmă și ID-uri AD_Client numerice repetate între instanțe.', 'Execută rezolvări, liste și citire de document din fiecare context, apoi context fără mapare proprie.', 'Corelează host DB/REST, client, org și cabinet în aceeași probă mascată.'],
 'Fiecare context rezolvă propria instanță; lipsa mapării este refuz explicit, fără împrumutarea mapării altui cabinet.',
 'Cabinet A fără mapare pentru CUI X, dar cabinet B are mapare validă pentru X.',
 'Inventar mapări din schema efectivă + managed_firms și AD_Client în ambele fixture DB; cheia exactă se confirmă din migrare.',
 'Respectă separarea nativă AD_Client în interiorul instanței și separarea fizică între instanțe.',
 'Firma cu același CUI este identificată și prin cabinet; erorile de mapare nu selectează automat altă firmă.', ['A02','A10']);
add(11,'Context contradictoriu sau absent',
 'Cookie/path/query/body/header cu firme diferite sunt reconciliate printr-o regulă server explicită sau respinse; lipsa firmei active nu produce fallback privilegiat.',
 [P.tenant,P.middleware,P.front,P.noFirmUI,P.tenants],
 ['Documentează precedența surselor de context și separă contextul de afișare de cel autorizat.', 'Testează combinații A/B între cookie, path, body și header plus lipsa fiecărei surse.', 'Testează cont cu zero firme, o firmă și mai multe firme autorizate.', 'Verifică firma_activa/fara_firma_activa și cererile declanșate înaintea selectării firmei.'],
 'Nu apare nicio cerere business cu tenant implicit neautorizat; utilizatorul fără firmă vede o stare explicată.',
 'Filă pentru A trimite body tenant B și cookie expirat; cont fără portofoliu accesează link direct.',
 'Zero rânduri citite/modificate în firma implicită/system ca urmare a contextului absent; probe query scoping.',
 'AD_Client_ID/AD_Org_ID se stabilesc înaintea operației și nu sunt moștenite accidental de la sesiune veche.',
 'Starea fără firmă permite alegerea/solicitarea accesului, fără formular aparent funcțional pe firma greșită.', ['A09','A10']);
add(12,'Liste, căutări, numărători și referințe',
 'Filtrarea de acces se aplică identic listelor, totalurilor, paginării, autocompleteului, lookupurilor și rezultatelor goale; metadatele nu divulgă resurse private din alt scope.',
 [P.tenant,P.data,P.meta,P.tenants,P.stores,P.cabinets,P.front],
 ['Selectează toate familiile de listare din inventarul C01 și identifică filtrul de tenant/rol.', 'Pregătește canari diferiți în A1/A2/B1 și caută exact canarul neautorizat.', 'Compară listă, count, paginile următoare, exportul și autocompleteul cu aceleași filtre.', 'Testează sortare/filtrare pe câmpuri ascunse și referințe globale aprobate.'],
 'Rezultatele, numărătorile și timpii/mesajele documentate nu conțin date private străine; shared refs sunt limitate prin allowlist.',
 'Căutare după UUID/documentno străin, pagină dincolo de limită și filtru OR construit din UI.',
 'SQL efectiv sau predicate documentate pe AD_Client/AD_Org/firm_access; rândurile canar străine nu sunt returnate.',
 'Compară lookupurile native și filtrele de rol cu metadatele gateway; nu reimplementa incomplet filtrarea nativă.',
 'Count și listă sunt coerente; fără sugestii ale firmelor inaccesibile și fără erori tehnice care divulgă SQL.', ['A02','A03','A04','A05','A06','A09']);
add(13,'Apartenența obiectului la fiecare acces direct',
 'Citirea/modificarea/ștergerea logică/exportul/downloadul verifică apartenența obiectului și acțiunea permisă, independent de faptul că obiectul a fost vizibil într-o listă.',
 [P.tenant,P.data,P.reports,P.exports,P.documents,P.office,P.front],
 ['Enumeră tipurile de obiecte și identificatorii acceptați: ID numeric, UUID, filename, job ID.', 'Pentru fiecare familie execută acces autorizat și schimbă numai identificatorul cu cel din alt scope.', 'Verifică obiecte copil: linie factură/comandă, atașament, rezultat raport și document office.', 'Repetă pentru modificare numai în fixture și inspectează absența efectelor în obiectul străin.'],
 'Apartenența părinte/copil este verificată server; răspunsurile nu divulgă payloadul obiectului străin.',
 'Atașament al documentului B cerut prin URL A și line ID B asociat unui header A.',
 'Legături părinte/copil, office_documents și documentele native; snapshot înainte/după pentru ambele firme.',
 'assert_record_belongs_to_tenant/owned se corelează cu verificarea native PO/AD_Role, fără a presupune echivalența.',
 'Linkurile expirate/inaccesibile au explicație și revenire; interfața nu păstrează previewul obiectului anterior.', ['A02','A03','A04','A05','A06','A07','A09']);
add(14,'AD_Client 0 / AD_Org 0 și referințe partajate',
 'Înregistrările system/client/org zero sunt accesibile numai în clasele de referințe explicit permise; datele financiare, documentele și setările private nu devin globale prin valoarea zero.',
 [P.perms,P.tenant,P.data,P.meta,P.models],
 ['Extrage allowlisturile și clasifică fiecare tabel global-safe/shared-by-client/tenant-forbidden.', 'Compară clasificarea cu AccessLevel nativ și cu utilizarea în ecrane.', 'Testează citire și referințe pentru un exemplu din fiecare clasă, inclusiv încercare de write.', 'Inspectează importuri și operații de fundal care pot crea client/org zero accidental.'],
 'Referințele partajate aprobate funcționează, iar datele private nu sunt citite/scrise prin zero sau fallback.',
 'C_INVOICE sau C_ORDER cu client/org zero în fixture; alegerea unei referințe din alt client.',
 'AD_Table.AccessLevel, AD_Client_ID/AD_Org_ID din fixture, FK și constrângeri relevante.',
 'AD_Table AccessLevel și regulile native sunt sursa principală; orice excepție EVA este justificată și testată.',
 'Lookupurile arată numai referințele utilizabile; validarea explică de ce o referință nu este admisă.', ['A02','A03','A04','A05']);
add(15,'Documente: autorizare și acțiuni native protejate',
 'processed/posted/docstatus/docaction/documentno și câmpurile de audit/context nu pot fi modificate arbitrar; tranzițiile documentelor trec prin acțiunea nativă autorizată.',
 [P.perms,P.data,P.tenant,P.middleware],
 ['Inventariază protecțiile de câmp și allowlistul documentelor/acțiunilor.', 'Corelează CO/CL/VO/RE/RC/PR/AP/RJ cu drepturile și stările native, pentru documentele folosite efectiv.', 'În fixture încearcă update direct al câmpurilor protejate și aceeași tranziție prin procesul nativ.', 'Verifică rolul actorului, rezultatul financiar/logistic și jurnalul împreună cu ownerii de domeniu.'],
 'Updateul arbitrar este respins; tranziția permisă respectă validările și atomicitatea native.',
 'Member setează Posted=Y sau DocStatus=CO, schimbă AD_Client_ID ori invocă acțiunea unui document străin.',
 'Snapshot document, linii, Fact_Acct/stock relevante numai în fixture; câmpurile protejate nu sunt rescrise la refuz.',
 'DocAction/DocumentEngine și PO/ProcessUtil existente sunt verificate în versiunea instalată înaintea propunerii unui proces nou.',
 'Butonul exprimă acțiunea reală și starea documentului; refuzul nu lasă un succes vizual fals.', ['A02','A03','A04','A05','A06','A07']);
add(16,'Drepturi native formular/fereastră/proces și proxy',
 'Drepturile efective din iDempiere sunt coerente cu portalul și gatewayul; ruta proxy/directă nu oferă un formular, proces sau tabel refuzat rolului nativ.',
 [P.remote,P.front,P.identity,P.perms,P.userForm,P.access,P.accessTables],
 ['Inventariază form/window/process/table și rolurile AD instalate pentru fiecare rol gateway.', 'Deschide aceeași funcție din meniu, deep link, proxy și ruta nativă autorizată de test.', 'Invocă procesul server după retragerea dreptului nativ și compară cu UI cache.', 'Documentează orice service role folosit de gateway și controalele compensatoare obligatorii.'],
 'UI și backend respectă același scope; contul tehnic nu ocolește autorizarea utilizatorului final.',
 'Formular ascuns în meniu accesat direct și proces lansat cu ID cunoscut după revocarea rolului.',
 'AD_User_Roles, AD_Role, AD_Form_Access, AD_Window_Access, AD_Process_Access și AD_Table_Access efective.',
 'Verifică MRole.getFormAccess și APIurile native echivalente; privilegii explicite, nu rol etichetat generic.',
 'Meniul rămâne conform designului existent; accesul refuzat afișează motiv util fără a altera navigația.', ['A02','A09','A10']);
add(17,'Schimbare firmă, file multiple și răspunsuri întârziate',
 'Datele și acțiunile rămân legate de contextul în care au fost cerute; un răspuns întârziat pentru A nu se afișează ca datele B după schimbarea firmei.',
 [P.front,P.tenant,P.login,P.noFirmUI,P.cabinetsUI],
 ['Identifică stocarea contextului în cookie/session/local storage și scopeul per filă.', 'Deschide A și B în două file; execută o citire întârziată controlat și schimbă contextul.', 'Testează back/forward, reload, tab suspendat și expirarea sesiunii.', 'Verifică anularea cererilor, eticheta firmei și refuzul salvării formularului din context vechi.'],
 'Niciun formular/rezultat nu se atribuie firmei greșite; contextul acțiunii este vizibil și verificat server.',
 'Cerere A răspunde după ce headerul UI arată B; salvare din fila A după switch global.',
 'Rândul creat/modificat și traceul indică numai firma corectă; lipsa unui efect la refuz se probează.',
 'Compară sesiunea și Env nativ la schimbarea clientului/rolului; nu presupune că refreshul vizual schimbă contextul server.',
 'Antet/breadcrumb persistent cu cabinet și firmă; avertizare clară pentru formularul cu context schimbat.', ['A09','A10']);
add(18,'Cache, fișiere, joburi și rezultate scopeate',
 'Cheile cache, fișierele generate, joburile și rezultatele asincrone includ identitatea suficientă cabinet/firmă/rol/canal; o cheie comună nu livrează rezultatul altui scope.',
 [P.front,P.cabinets,P.reports,P.exports,P.documents,P.tenant],
 ['Inventariază cacheuri browser/server, directoare export și stocarea status/result job.', 'Testează aceleași criterii și identificatori sintetici în două cabinete, firme și roluri.', 'Verifică autorizarea la polling/download, nu doar la creare.', 'Testează invalidarea după revocare și retry după restart controlat împreună cu A10.'],
 'Nu se reutilizează rezultate între scopeuri; fiecare citire de rezultat reevaluează accesul necesar.',
 'Utilizator B solicită job ID/export URL creat de A; aceeași denumire de fișier în două firme.',
 'Metadate job/fișier și contextul ownerului; paths fizice se maschează în raportul public dacă sunt sensibile.',
 'Pentru procese native verifică AD_PInstance/AD_Attachment și regulile accesului la rezultat.',
 'Pollingul și descărcarea refuzate nu devin succes sau buclă; rezultatele vechi sunt eliminate din ecran.', ['A02','A09','A10']);
add(19,'Administrator cabinet versus administrator platformă',
 'Administratorul cabinetului poate administra numai propriul cabinet și firmele autorizate; rolul super are acțiunile platformă explicit delimitate și auditate, fără asumarea accesului contabil nelimitat.',
 [P.cabinets,P.iam,P.admin,P.middleware,P.cabinetsUI,P.firmsUI],
 ['Separă acțiuni platformă, cabinet, firmă și operații contabile; documentează politica super.', 'Testează manager A pentru list/create/update/deactivate și endpointuri sensibile ale B.', 'Verifică protecția la schimbarea managing_uuid, user_uuid și client_id în body/path.', 'Pentru delete/upgrade inspectează codul și folosește numai simulare/fixture autorizat, fără ștergeri reale.'],
 'Administrarea nu trece frontiera cabinetului; acțiunile super sunt explicite, jurnalizate și nu se confundă cu rolul de contabil.',
 'Manager A adaugă utilizator în B sau dezactivează firmă B prin client_id colizionat.',
 'managing_firms/managed_firms/iam_users/firm_access și AD_Client status; zero modificări în cabinetul B.',
 'Compară System Administrator, client admin și AD_Role.UserLevel în nativ cu rolurile gateway.',
 'UI arată scopeul administrării și impactul; nu prezintă opțiuni de alt cabinet pentru manager.', ['A02','A09','A10']);
add(20,'Grant/revoke și prevenirea auto-escaladării',
 'Acordarea/retragerea drepturilor verifică puterea actorului, cabinetul țintei și grantul solicitat; un utilizator nu se poate promova sau acorda acces altui cabinet prin API.',
 [P.iam,P.admin,P.identity,P.usersUI,P.userForm,P.accessReview],
 ['Urmărește /users/{uuid}/access și operațiile de rol, inclusiv _user_din_cabinet.', 'Testează grant valid, grant peste drepturile actorului, auto-promovare și țintă străină.', 'Retrage grantul și verifică accesul efectiv portal/native/mobil.', 'Verifică duplicate, grant concurent/revoke și conturi orfane în ambele modele.'],
 'Drepturile sunt acordate numai de actor autorizat, fără escaladare și fără resturi active în nativ.',
 'Team_leader își acordă manager; manager A acordă firmă B unui user A; retry grant după revoke.',
 'firm_access unicitate, iam_users, AD_User_Roles și rolurile de gestiune; diferență completă înainte/după.',
 'Folosește mecanismele native de rol/grant și compară sincronizarea cu recertificarea accesului existentă.',
 'Ecranul diferențiază dreptul solicitat de cel efectiv și arată rezultatul sincronizării.', ['A02','A09','A10']);
add(21,'Provizionare identitate idempotentă și recuperabilă',
 'Retryul și eșecul parțial la creare utilizator/cabinet/firmă nu dublează identități și nu le leagă de alt cabinet; starea incompletă este vizibilă și nu acordă acces prematur.',
 [P.identity,P.cabinets,P.iam,P.models,P.cabinetsUI],
 ['Desenează pașii DB gateway→instanță→AD_User/role→mapare și commiturile.', 'În fixture simulează timeout înainte/după efectul nativ și repetă aceeași operație.', 'Testează două cereri concurente de creare a aceleiași identități.', 'Inspectează reconcilierea/compensarea fără ștergere de date de producție.'],
 'O singură identitate validă și mapare coerentă sau stare incompletă explicită, fără acces străin.',
 'Timeout după AD_User creat dar înainte de răspuns; retry cu cabinet diferit și aceeași cheie.',
 'iam_users/managed_firms și AD_User/AD_User_Roles; număr rânduri și legături înainte/după.',
 'Provision/sync_login refolosește identitatea AD_User existentă numai după verificarea contextului și cheii univoce.',
 'Progresul, eroarea recuperabilă și opțiunea de reluare sunt clare; nu se arată succes înainte de final.', ['A02','A09','A10']);
add(22,'Context și drepturi în operații de fundal',
 'Jobul păstrează actorul și contextul inițial, revalidează politica necesară la execuție și nu moștenește contextul altui job/thread; accesul la status/rezultat este autorizat.',
 [P.cabinets,P.identity,P.tenant,P.reports,P.exports,P.middleware],
 ['Inventariază create firm job, sync_login_in_fundal și procesele asincrone relevante.', 'Urmărește serializarea actor/cabinet/client/org/rol și politica de revocare între enqueue și run.', 'Rulează două joburi sintetice A/B intercalate și revocă accesul înaintea unuia.', 'Testează status/result polling cu alt actor și retry la timeout.'],
 'Joburile și rezultatele rămân în scope; politica pentru drepturi retrase este explicită și respectată.',
 'Worker reutilizat din A pentru B, rol revocat înainte de execuție și polling cu job ID străin.',
 'Stare job și efectul business au același cabinet/AD_Client/actor; corelare trace→job→tranzacție.',
 'AD_PInstance, contextul proceselor native și mecanismul de sesiune al workerului sunt verificate separat.',
 'Statusul diferențiază în așteptare/eșuat/refuzat/finalizat; butonul retry nu schimbă contextul.', ['A02','A09','A10']);
add(23,'Acces mobil: dispozitiv, token, sesiune și API',
 'Tokenul mobil este legat de utilizator/rol/client/dispozitiv conform contractului; contul, rolul, firma sau sesiunea dezactivate blochează toate operațiile mobile.',
 [P.mobileGuard,P.mobileToken,P.mobileDevice,P.mobileApi,P.inventoryApi,P.packingApi,P.mobileForm,P.mobileLog],
 ['Mapează enroll dispozitiv→token→GardaMobil→API→jurnal și toate excepțiile.', 'Testează dispozitiv valid, token expirat/modificat și cont/rol/client inactiv.', 'Repetă cererea cu aceeași idempotency key în contextul corect și apoi în alt context.', 'Verifică revocarea dispozitivului și sesiunea nativă asociată.'],
 'Nicio operație mobilă nu ocolește starea curentă a identității; retryul nu dublează efectul sau jurnalul greșit.',
 'Token dispozitiv A folosit cu warehouse B; AD_Session invalidată dar token încă valid criptografic.',
 'AD_User/AD_Role/AD_Client/AD_Session, EVA_JurnalMobil și dispozitivele din schema reală.',
 'Reutilizează AD_Session și rolurile native; documentează strict extensia necesară pentru dispozitiv/jeton.',
 'Dispozitivul primește mesaj recuperabil și nu confirmă inventarul/ambalarea la eroare de acces.', ['A05','A09','A10']);
add(24,'Drepturi pe G1.n/G2.n/locatori și validare',
 'Drepturile read/write/validate sunt verificate pe gestiunea și locatorul efectiv, pentru fiecare G1.n și G2.n; accesul la o gestiune nu se extinde la alta prin locator ori document mixt.',
 [P.access,P.accessTables,P.wmsGuard,P.inventoryApi,P.packingApi,P.mobileForm],
 ['Mapează EVA_AccesGestiune și AD_Role la M_Warehouse/M_Locator și rolurile de gestionar.', 'Creează două G1 și două G2 sintetice cu drepturi diferite; testează read/write/validate separat.', 'Testează locator străin, mutare între gestiuni și document cu linii mixte.', 'Verifică autorizarea server la validarea finală după revocarea dreptului.'],
 'Fiecare efect se produce numai în gestiunile/locatorii autorizați; validarea cere drept distinct dacă politica îl definește.',
 'Gestionar cu IsCitire schimbă IsValidare prin payload; locator din G2.2 introdus în document G2.1.',
 'EVA_AccesGestiune, M_Warehouse/M_Locator și documentele/liniile afectate; unicitate user/role/client/warehouse.',
 'Compară Warehouse/Locator/AD_Role native cu extensia EVA, evitând o nouă structură paralelă de gestiuni.',
 'Selectoarele arată tipul G1/G2, locația și dreptul; combinațiile imposibile sunt prevenite și verificate server.', ['A02','A05','A09']);
add(25,'Comisionar: canal, propriile situații și plasare comenzi',
 'Comisionarul vede catalogul permis, plasează comenzi și vede numai situațiile proprii ale canalelor acordate; administrarea comenzilor, pickul, avizul și validarea/AWB/facturarea rămân în iDempiere EVA conform cerinței.',
 [P.stores,P.site,P.siteProducts,P.b2b,P.b2bForm,P.salesChannel,P.salesForm,P.tenant],
 ['Identifică modelul efectiv comisionar→partener/user→canal și drepturile disponibile; nu presupune că rolul există.', 'Testează două persoane în același canal și aceeași persoană în două canale cu granturi distincte.', 'Verifică catalog, creare comandă, listă/detail situații proprii și acces direct la comanda altuia.', 'Încearcă din site tranziții rezervate ERP; corelează cu A06/A07/A08.'],
 'Accesul este limitat pe persoană și canal; lipsa funcției se consemnează ca gap, iar tranzițiile administrative nu sunt expuse siteului.',
 'Comisionar A citește situația B ori validează un aviz/AWB prin endpoint ascuns, chiar în același canal.',
 'commerce_stores și tabelele native efective de canal/comisionar/comandă; FK și predicate proprietar sunt identificate la execuție.',
 'Evaluează C_BPartner/SalesRep/Commission și drepturile native existente înaintea unui model nou de comisionar.',
 'Siteul explică diferența între comandă plasată și comandă preluată/validată în ERP; situațiile sunt clar personale.', ['A06','A07','A08','A09'], ['Politica nominală pentru comisionari și mappingul la modelul nativ sunt confirmate de owner; necunoscutul nu se marchează PASS.']);
add(26,'Catalog public, previzualizare platformă și date private',
 'Catalogul/previzualizarea pe canal expune numai câmpurile publicate pentru acel canal; costuri, marje, date contabile, clienți și credențiale nu sunt livrate browserului public.',
 [P.site,P.siteProducts,P.stores,P.channels,P.channelForm,P.channelPanel,P.front],
 ['Inventariază DTOurile publice/private și conversiile pe canal incluzând CPP/CPA și cod intern versus SKU/EAN.', 'Compară payloadul anonim cu cel al responsabilului/comisionarului.', 'Testează preview eMag/Trendyol din canalul altui utilizator și slugul unui canal nepublicat.', 'Inspectează HTML/JSON/cache/asset pentru câmpuri ascunse doar vizual.'],
 'Câmpurile sunt proiectate server conform politicii, iar previewul administrativ cere rol/canal; identitățile CPP și CPA nu se confundă.',
 'Parametru fields=* ori expand solicită cost și date personale; canal privat accesat prin slug cunoscut.',
 'Mapping canal și proiecția de produs/partener; selecția include numai câmpurile contractului public.',
 'Reutilizează M_Product și cataloage/prețuri native unde acoperă cerința; nu considera SKU/EAN drept identitate CPP/CPA.',
 'Responsabilul vede eticheta preview și canalul; publicul nu primește instrumentele ERP.', ['A02','A06','A08','A09']);
add(27,'Sesiuni web, cookie, CSRF, CORS și redirect',
 'Operațiile autentificate din browser verifică frontiera origin/sesiune conform mecanismului folosit; cookieurile și redirecturile nu expun sesiunea către alt cabinet/origin.',
 [P.front,P.login,P.middleware,P.remote,P.loginUI],
 ['Inventariază cookie flags/domain/path și modelul CSRF/CORS pentru portal, native și siteuri.', 'Testează în mediu izolat origin nepermis, cerere fără protecția cerută și redirect extern.', 'Verifică subpathurile cabinet/firmă/canal și proxyul native pentru propagarea cookieurilor.', 'Inspectează browser storage, referrer și URL fără a înregistra secrete.'],
 'Cererea cross-origin neautorizată nu produce efect; sesiunea nu trece accidental la alt origin/scope.',
 'Formular de pe origin sintetic atacator trimite POST cu cookie; return_url extern ori protocol-relative.',
 'Zero efect business la respingere și jurnalul session/security necesar; fără valori cookie în raport.',
 'Verifică cookie/sesiune ZK native și compatibilitatea proxyului, nu doar cookieul Flask.',
 'Reloginul/redirectul revine la o destinație locală sigură; mesajele CSRF nu dezvăluie tokenul.', ['A08','A09','A10']);
add(28,'Input, proxy și căi de fișier la frontiera tenant',
 'Parametrii tabel/câmp/filtru/path/URL sunt validați astfel încât să nu permită interogare, acces fișier ori cerere de rețea în afara resurselor autorizate.',
 [P.data,P.meta,P.remote,P.front,P.reports,P.exports,P.documents],
 ['Identifică SQL dinamic, nume de tabel/câmp, căi download și destinații proxy.', 'Verifică allowlist/parametrizare/canonicalizare și frontiera de rețea.', 'Folosește numai probe inofensive în fixture pentru input invalid, traversal și destinație locală de test.', 'Confirmă că eroarea nu întoarce SQL, path sensibil sau corpul upstream neautorizat.'],
 'Inputul invalid este respins înainte de acces extern/fișier/interogare nepermisă; resursele autorizate rămân funcționale.',
 'Nume tabel system, ../ în download, URL de upstream nepermis și filtre cu identificator neallowlisted.',
 'Log de interogare controlat și snapshot fără modificări; nu efectua scanări sau citiri de secrete reale.',
 'Preferă APIurile native de metadate/PO/query cu rol și limitează gatewayul la contractele necesare.',
 'Mesaj de validare util, fără stacktrace; formularul păstrează câmpurile valide și contextul.', ['A02','A09','A10']);
add(29,'Jurnal identitate–context–efect fără secrete',
 'Evenimentele sensibile permit corelarea actorului, cabinetului, firmei, rolului, canalului/gestiunii, rezultatului și traceului, fără parole/tokenuri/secrete și fără PII excesivă.',
 [P.middleware,P.iam,P.admin,P.cabinets,P.mobileLog,P.auditGuard,P.models],
 ['Definește setul de evenimente: login refuzat, grant/revoke, context refuzat, admin, mobil și operație business autorizată.', 'Leagă fiecare probă de request trace→job/process→tranzacție→audit event.', 'Verifică cine poate citi/șterge/modifica jurnalul și filtrarea lui pe cabinet/firmă.', 'Inspectează probe sintetice de eroare pentru mascarea credentialelor și minimizarea datelor.'],
 'Evenimentul poate fi atribuit și reconstruit, refuzurile sunt vizibile conform politicii, iar jurnalul nu divulgă secrete altui rol.',
 'Utilizator citește auditul altui cabinet; payload cu token produce eroare și este logat; modificare jurnal prin API generic.',
 'audit_events/activity_log/EVA_JurnalMobil și mecanismele native de audit instalate; verifică integritatea și accesul.',
 'Compară AD_ChangeLog și jurnalul proceselor native cu extensiile EVA înaintea propunerii unui jurnal redundant.',
 'Mesajul utilizatorului include referința de suport utilă, fără detalii interne sensibile.', ['A02','A09','A10']);
add(30,'Refuz, timeout și recuperare UI fără efect fals',
 '401/403/404, timeoutul și eșecul de sincronizare nu sunt afișate drept succes; retryul păstrează contextul și nu dublează o operație confirmată server.',
 [P.front,P.login,P.cabinets,P.stores,P.mobileApi,P.mobileLog],
 ['Pentru fiecare pipeline identifică stările UI și contractul de eroare/retry.', 'Injectează în fixture refuz, timeout înainte/după commit și răspuns întârziat.', 'Verifică reîncercarea cu aceeași cheie/context și schimbarea contextului între încercări.', 'Compară starea UI cu DB și jurnalul, inclusiv reload după eroare.'],
 'Rezultat unic și explicabil; UI nu ascunde starea necunoscută și nu confirmă operația fără probă.',
 'Dublu click după timeout la grant/provision/mobile; 403 convertit în listă goală fără explicație.',
 'Numărul efectelor și cheile idempotente sunt verificate pe scope; nu deduce succesul numai din HTTP.',
 'Evaluează starea procesului/documentului nativ și mecanismul de retry existent înaintea unei implementări paralele.',
 'Stări distincte în curs/eșuat/refuzat/necunoscut/finalizat și recuperare accesibilă; fără refresh forțat care ascunde problema.', ['A09','A10']);
add(31,'Conturi tehnice, secrete și privilegii minime',
 'Tokenurile/conturile de serviciu au scope și utilizări documentate, nu sunt trimise frontendului și nu permit operații umane administrative în afara contractului lor.',
 [P.middleware,P.auth,P.stores,P.identity,P.remote,P.front],
 ['Inventariază numai numele și locurile configurărilor de secret, fără a tipări valorile.', 'Mapează fiecare cont tehnic la rol AD, endpointuri, firme și operații necesare.', 'Testează cu credențială sintetică de serviciu accesul permis și endpointuri administrative nepermise.', 'Verifică rotația/revocarea în fixture și comportamentul când secretul lipsește.'],
 'Secretele rămân server-side și contul tehnic nu devine super implicit; lipsa secretului nu activează bypass de producție.',
 'Service token de rezolvare canal folosit la grant user/export contabil; configurare auth goală într-un profil non-dev.',
 'AD_User/AD_Role ale serviciilor și accesul la tenant mapping; nicio valoare secretă în artefact.',
 'Folosește roluri native restrânse și APIurile existente; justifică separat orice acces cross-client necesar.',
 'Erorile de conectare nu expun credentiale și indică serviciul indisponibil în termeni de business.', ['A08','A10']);
add(32,'Înregistrare și legare cont–cabinet fără confuzii',
 'Înregistrarea/legarea utilizatorului normalizează identificatorii conform regulilor documentate, verifică apartenența și nu preia automat identitatea sau drepturile unui cont omonim din alt cabinet.',
 [P.login,P.iam,P.identity,P.models,P.usersUI,P.cabinetsUI],
 ['Inventariază identificatori email/login/UUID/cabinet și constrângerile de unicitate.', 'Testează email cu variație de capitalizare/spații, utilizator omonim în alt cabinet și înregistrare duplicată.', 'Verifică cine poate asocia identitatea cu firma și dacă există invitație/verificare; marchează lipsurile fără a inventa flux.', 'Testează concurența a două înregistrări identice și eventualul cont nativ preexistent.'],
 'O asociere explicită și verificată, fără conturi privilegiate duplicate ori fuziune accidentală cross-cabinet.',
 'Registrare cu CUI/UUID al cabinetului altuia și aceeași adresă a unui administrator existent.',
 'iam_users/iam_credentials/managing_firms și AD_User; indexuri unice și maparea explicită a identităților.',
 'AD_User existent se reutilizează numai cu identitate/apartenență dovedită; loginul și CUI nu sunt chei interschimbabile.',
 'Formularul indică exact cabinetul și rolul solicitat; conflictul de identificator nu divulgă alte conturi.', ['A02','A09','A10']);
add(33,'Matrice exhaustivă și nevoi contabile transversale',
 'Fiecare categorie de acțiune și tip de date din contabilitate, aprovizionare, G1/G2/G3, comenzi, plăți, canale și administrare are caz pozitiv și caz cross-scope/refuz în registrul de acoperire.',
 [P.perms,P.tenant,P.data,P.meta,P.reports,P.exports,P.access,P.site],
 ['Leagă inventarul de suprafețe de matricea rol×scope×acțiune și de ownerii A02–A10.', 'Pentru fiecare familie verifică acțiuni read/create/update/validate/export/admin/status-result aplicabile.', 'Stabilește fixtures și probe la frontierele comune; reutilizează o probă numai dacă arată exact aceeași frontieră și versiune.', 'Publică denominatorul, PASS/FAIL/BLOCAT/NEEXECUTAT și N/A cu justificare; A11 verifică rândurile fără probă.'],
 'Nicio familie activă și niciun capitol contabil nu este exclus doar pentru că A01 nu deține logica business; interfața are owner nominal.',
 'O rută nouă sau capitol contabil fără test de scope; un rol business fără mapare AD; se blochează închiderea acoperirii.',
 'Registru tabele/client/org și date sensibile furnizat de A02/A03; comparație cu endpointurile și formele efective.',
 'Native forms/processes și drepturile lor acoperă aceleași capitole ca gatewayul; lipsa ecranului nu elimină APIul.',
 'Accesul la meniuri și ecrane rămâne predictibil pe rol, fără duplicarea funcțiilor native.', ['A02','A03','A04','A05','A06','A07','A08','A09','A10']);
add(34,'Reutilizare nativă demonstrată din două surse',
 'Nicio propunere de tabel/rol/mecanism nou de autorizare nu este acceptată înaintea comparației cu codul nativ al versiunii țintă și cu funcția/AD efectiv instalate în EVA.',
 [P.perms,P.tenant,P.identity,P.access,P.accessTables,P.mobileGuard,P.auditGuard,P.accessReview],
 ['Pentru fiecare necesitate identifică obiectul nativ candidat: AD_Role/User/User_Roles, client/org, acces form/window/process/table, sesiune, audit.', 'Obține sursa nativă pinuită și contractul/metadatele funcției; consemnează exact versiunea.', 'Verifică în instanța de test configurația și comportamentul disponibil, cu rol permis/refuzat.', 'Clasifică soluția: CONFIGUREAZĂ NATIV / ADAPTEAZĂ EXISTENT EVA / EXTINDE MINIMAL / NOU JUSTIFICAT, cu gap și dovadă.'],
 'Fiecare propunere are două probe independente și motive concrete; verificarea doar în cod EVA nu satisface cerința.',
 'Propunere de RBAC/gestiuni/audit paralel deși AD oferă mecanismul; ori clasă upstream existentă dar neinstalată confundată cu funcție disponibilă.',
 'Export read-only al AD relevant și configurării efective, fără credențiale; nume/versiune bundle și migrații asociate.',
 'Sursa 1: cod iDempiere exact/pinuit. Sursa 2: metadate AD + comportament instalat. Sursa EVA este comparația suplimentară, nu înlocuiește cele două.',
 'Soluția preferată reduce meniuri/configurări duplicate și menține experiența iDempiere învățabilă.', ['A02','A05','A06','A09','A10'], ['Acces read-only la metadate și mediu nativ de test; fără acestea verdictul native rămâne BLOCAT.']);
add(35,'Versiune auditabilă, transport izolat și revalidare',
 'Concluzia se referă la SHA/build/schema identificate; testele nu trimit comenzi sau modificări la parteneri, iar o versiune schimbată invalidează controlat probele afectate.',
 [P.middleware,P.tenant,P.cabinets,P.stores,P.mobileApi,P.site],
 ['Înregistrează SHA, hashuri fișiere, build/bundle, endpoint base și migrații fără secrete.', 'Confirmă cu A10 izolarea transporturilor externe și fixtures; nu apela parteneri direct pentru audit.', 'Pentru un task remediat mapează diff→controale→pipelineuri→probe de reexecutat.', 'Predă A11 raportul cu toate limitările, inclusiv controale BLOCAT, și păstrează separat verdictul auditului de cel al produsului.'],
 'Probe reproductibile pe versiunea declarată, zero efecte externe neautorizate și nicio notă de conformitate din lipsă de acces.',
 'Deployment diferit de SHA, test care ar trimite AWB/comandă reală sau raport vechi reutilizat după schimbarea tenant_authz.',
 'Manifest schema/build și snapshoturile fixture; nicio resetare de DB sau volum.',
 'Versiunea iDempiere și pluginurile native/EVA efectiv instalate sunt parte din identificarea probei.',
 'Capturile arată versiunea/contextul fără date private; defectele de audit sunt corectate înaintea predării.', ['A02','A07','A08','A09','A10','A11','A12']);

add(36,'XSS reflectat/stocat/DOM și conținut din canale',
 'Numele de firmă/canal/utilizator, notele și mesajele de eroare sunt randate ca date în contextul HTML/atribut/JS corect; conținutul unui tenant nu execută script în sesiunea altui utilizator.',
 [P.front,P.usersUI,P.cabinetsUI,P.channelForm,P.channelPanel,P.site,P.siteProducts,P.documents],
 ['Inventariază punctele de randare și filtrele template/DOM din suprafețele reale, inclusiv preview și raport.', 'În fixture folosește payloaduri inofensive care marchează doar execuția locală, fără exfiltrare sau acces extern.', 'Testează reflected/stored/DOM pentru fiecare sink aplicabil și examinează protecția server/browser.', 'Verifică afișarea în portal, native, mobil și site a aceleiași valori sintetice; orice N/A are justificare pe inventar.'],
 'Valoarea este afișată ca text/conținut sanitizat conform contractului; nicio execuție de script și nicio citire a datelor altui scope.',
 'Nume canal cu markup/atribute, mesaj upstream cu script și notă stocată afișată unui administrator în alt ecran.',
 'Valoarea fixture și apartenența ei sunt identificate; nu introduce payloaduri în date reale și nu exporta conținut sensibil.',
 'Verifică randarea/escapingul componentelor ZK existente înainte de a propune filtre paralele; protecția unui ecran nu se presupune globală.',
 'Textul legitim cu diacritice și caractere speciale rămâne lizibil; validarea nu alterează tacit denumirea firmei/canalului.', ['A08','A09','A10'], ['Payloaduri locale inofensive aprobate pentru fixture, fără rețea/exfiltrare.']);
add(37,'Upload/atașament: proprietar, tip, dimensiune și parser',
 'Uploadul verifică actorul și părintele înainte de stocare/procesare, aplică limitele aprobate și nu permite executarea/servirea activă a fișierului ori traversarea căii între firme.',
 [P.documents,P.office,P.front,P.tenant,P.exports],
 ['Inventariază uploadurile active și contractele: tip/magic bytes, extensie, limită, destinație, parser, download și cleanup.', 'În fixture testează fișier valid, extensie/MIME contradictorii, nume cu cale, limită depășită și document părinte străin.', 'Simulează întrerupere/eroare de parser și retry; verifică artefactele parțiale și autorizarea downloadului.', 'Coordonează cu A04 importurile și cu A10 scanarea/parsingul, fără încărcarea de malware sau archive bomb.'],
 'Fișierul aparține scopeului autorizat, nu devine executabil, iar eșecul nu lasă un artefact accesibil altui rol sau tenant.',
 'Fișier HTML servit inline necontrolat, filename ../, părinte B în upload A și fișier peste limita configurată.',
 'office_documents/AD_Attachment sau modelul real, metadate owner și fișiere temporare; după refuz nu există obiect business orfan.',
 'Evaluează AD_Attachment și procesarea nativă existentă, limitele instalate și extensia minimă necesară.',
 'Progress, eroare limită/tip și retry clare; nu se raportează atașat înainte de persistare și validare.', ['A02','A04','A09','A10'], ['Limitele și tipurile acceptate sunt aprobate/configurate; dacă lipsesc, se înregistrează decizie necesară.']);
add(38,'Costul autorizării, paginare și regresie de performanță',
 'Verificarea drepturilor și tenantului rămâne activă la volumul și concurența aprobate; optimizarea cache/paginare nu elimină filtrarea și nu produce epuizare necontrolată a resurselor.',
 [P.tenant,P.perms,P.data,P.meta,P.iam,P.stores,P.cabinets,P.access],
 ['Stabilește cu A02/A10 volumele reprezentative pentru firme/granturi/documente/gestiuni și bugetele observabile înainte de test.', 'Examinează query plan/indexurile pentru filtrele cabinet/client/org/actor și cardinalitatea listelor.', 'În mediul și intervalul de resurse aprobat măsoară p50/p95/erori pentru citire/paginare/export și acces refuzat.', 'Compară cu baseline și repetă după invalidarea cacheului/revocare; nu face teste de încărcare în producție.'],
 'Bugetele aprobate sunt măsurate pe același dataset; scopul și revocarea rămân corecte cu cache cald/rece și la concurență.',
 'Utilizator cu multe granturi, pagină foarte mare/nelimitată, export concurent și cache încă valabil după revoke.',
 'EXPLAIN read-only/plan echivalent și indexurile filtrelor; volume și număr queryuri, fără extract de date reale.',
 'Compară rol-cache și queryurile native cu cele EVA; reutilizarea native nu este presupusă performantă fără măsurare.',
 'Loading și progres sunt explicite; cancel/timeout nu afișează date parțiale ca total și nu blochează schimbarea sigură a contextului.', ['A02','A09','A10'], ['Bugete și volume aprobate de owner, slot/coadă de resurse conform regulilor proiectului; fără acestea măsurarea este BLOCAT.'], 'REVIZIE_COD + QUERY_PLAN_READ_ONLY + MASURARE_IZOLATA_APROBATA + UI_MANUAL');

const pipelines = [];
function pipe(id,name,fe,api,service,db,effect,obs,negative,controls,owners) {
 pipelines.push({id,nume:name,stare:'NEEXECUTAT',statut_traseu:'CANDIDAT_DE_CONFIRMAT_LA_AUDIT',
  traseu:[{etapa:'FE',surse_candidate:fe,proba:'Captură și cerere reală cu actor/context vizibile.'},{etapa:'API',surse_candidate:api,proba:'Metodă/rută, contract, validare și refuz autorizare.'},{etapa:'serviciu',surse_candidate:service,proba:'Call graph fișier:linie, identitate și context propagate.'},{etapa:'DB',obiecte_candidate:db,proba:'Metadate/read-only și snapshot înainte/după în fixture.'},{etapa:'efect',contract:effect,proba:'Starea business efectivă, inclusiv absența efectului la refuz.'},{etapa:'observabilitate',contract:obs,proba:'Trace/job/process/audit corelate, fără tokenuri/PII.'}],
  scenariu_pozitiv:'Actor permis, scope propriu și stare validă; se verifică toate cele șase verigi, nu doar răspunsul HTTP.',scenarii_negative:negative,
  retries_races_errors_recovery:['Dublu click/retry cu aceeași identitate și context; efect unic conform contractului.', 'Revocare sau schimbare firmă între solicitare și executare; fără migrare accidentală a efectului.', 'Timeout înainte/după efect; UI arată starea verificată sau necunoscută și permite recuperare sigură.'],
  controale:controls.map(n=>`A01.C${String(n).padStart(2,'0')}`),owners, criteriu_completitudine:'Cele șase verigi și negativele sunt dovedite pe aceeași versiune. O verigă lipsă = BLOCAT/NEEXECUTAT, niciodată presupusă.'});
}
pipe('A01.P01','Login → sesiune portal → identitate nativă',[P.loginUI,P.front],[P.login],[P.auth,P.middleware,P.identity],['iam_credentials','iam_users','AD_User','AD_User_Roles','AD_Session'],'Sesiune numai pentru identitatea validă și contextul permis.','TraceId + audit autentificare și sincronizare rol fără credentiale.',['Parolă greșită','Token alterat','Cont dezactivat','Sync AD indisponibil','Refresh paralel cu logout-all'],[2,3,4,5,6,7,8,16,21,27,29,30],['A01','A09','A10']);
pipe('A01.P02','Selecție cabinet/firmă → context → listă autorizată',[P.cabinetsUI,P.noFirmUI,P.front],[P.tenants,P.login,P.cabinets],[P.tenant,P.map,P.middleware],['managing_firms','managed_firms','firm_access','mapare client cabinet: numele exact de confirmat','AD_Client','AD_Org'],'Datele apar în firma selectată autorizată; fără firmă apare starea dedicată.','Trace cu cabinet/client/org și captură antet/breadcrumb.',['Același CUI în două cabinete','AD_Client_ID repetat între instanțe','Cookie A/body B','Filă veche','Mapare lipsă'],[9,10,11,12,17,18],['A01','A02','A09','A10']);
pipe('A01.P03','Deschidere iDempiere nativ → formular/proces permis',[P.front,P.userForm],[P.remote],[P.identity,P.perms,P.access],['AD_Session','AD_User_Roles','AD_Role','AD_Form_Access','AD_Window_Access','AD_Process_Access','AD_Table_Access'],'Formularul/procesul respectă drepturile native efective.','Sesiune nativă, trace proxy și rezultat proces corelate.',['Deep link către formular refuzat','Rol retras cu ecran deschis','Acces direct upstream','Service role excesiv'],[5,7,8,15,16,27,31,34],['A01','A02','A09','A10']);
pipe('A01.P04','Fereastră/date → gateway generic → document nativ',[P.front],[P.data,P.meta],[P.tenant,P.perms],['AD_Table','AD_Column','AD_Role','C_Order/C_Invoice/M_InOut/M_Inventory/M_Movement: după fixture','linii și efecte native asociate'],'Citire/editare permisă; tranziția documentului trece prin acțiunea nativă validată.','Trace→proces/tranzacție→audit și verificare UI.',['IDOR header/line','DocStatus direct','Client/org zero nepermis','Parametru tabel/câmp nepermis'],[1,12,13,14,15,16,28,33],['A01','A02','A03','A04','A05','A06','A07','A09']);
pipe('A01.P05','Mobil WMS → identitate/dispozitiv → gestiune/locator',[P.mobileForm],[P.mobileApi,P.inventoryApi,P.packingApi],[P.mobileGuard,P.mobileToken,P.mobileDevice,P.access,P.wmsGuard],['AD_User','AD_Role','AD_Client','AD_Session','EVA_AccesGestiune','M_Warehouse','M_Locator','EVA_JurnalMobil'],'Read/write/validate numai în G1.n/G2.n autorizate, efect unic la retry.','EVA_JurnalMobil cu idempotency key mascată/hash și cod rezultat, legat de efect.',['Dispozitiv revocat','Warehouse străin','Locator din altă gestiune','IsCitire fără IsValidare','Retry cross-client'],[5,23,24,29,30],['A01','A02','A05','A09','A10']);
pipe('A01.P06','Administrare utilizatori → grant/revoke → sincronizare AD',[P.usersUI,P.userForm],[P.iam,P.admin],[P.identity,P.middleware],['iam_users','firm_access','iam_credentials.token_epoch','AD_User','AD_User_Roles'],'Drept efectiv limitat la actor/scope și revocare propagată.','activity_log/audit_events + rezultat sync nativ și acces ulterior.',['Auto-escaladare','Țintă alt cabinet','Grant/revoke concurent','Timeout după grant nativ','Sesiune veche'],[5,7,19,20,21,22,29,32],['A01','A02','A09','A10']);
pipe('A01.P07','Canal/comisionar → catalog/comandă proprie → context ERP',[P.b2bForm,P.salesForm,P.channelPanel,P.front],[P.stores,P.site,P.siteProducts],[P.b2b,P.salesChannel,P.channels,P.tenant],['commerce_stores','tabele canal/comisionar: de confirmat din model instalat','C_BPartner','M_Product','C_Order/C_OrderLine'],'Catalog și comandă proprie pe canal; administrarea ulterioară rămâne în ERP.','Trace canal+actor→comandă și audit refuz pentru alte persoane/canale.',['Situația altui comisionar','Alt canal cu același produs','Preview privat','Validare/AWB din site','Cost ascuns numai CSS'],[9,13,25,26,27,31],['A01','A02','A06','A07','A08','A09']);
pipe('A01.P08','Creare firmă → job provizionare → status și mapare',[P.cabinetsUI,P.firmsUI],[P.cabinets],[P.identity,P.tenant,P.map],['managing_firms','managed_firms','mapare client cabinet: de confirmat','AD_Client','AD_User_Roles','stocare job: de confirmat'],'O firmă mapată în cabinetul corect sau eroare recuperabilă explicită.','Trace→job→instanță→mapare→audit; status accesibil doar actorului autorizat.',['Manager din alt cabinet','Timeout după creare','Două cereri identice','Job ID străin','Revocare înainte de run'],[10,18,19,21,22,29,30,35],['A01','A02','A09','A10']);
pipe('A01.P09','Raport/export/atașament → descărcare autorizată',[P.front],[P.reports,P.exports,P.documents,P.office],[P.tenant,P.middleware],['office_documents','documente native aferente','AD_PInstance/AD_Attachment dacă folosite','metadate rezultat/job/fișier: de confirmat'],'Numai datele și documentele scopeului permis sunt livrate, cu același control la download.','Trace cerere→job/proces→fișier→download/audit; hash artefact și context.',['Filename traversal','Job/attachment străin','Revocare după generare','Cache comun A/B','Export fără filtre de rol'],[12,13,18,22,28,29,30],['A01','A02','A03','A04','A06','A07','A09','A10']);

const matrixActions=['catalog_public','citire_date_private','creare_modificare','validare_document','export_situatii','administrare_acces','status_rezultat_job'];
const matrix=[
 {rol:'anonim',mapping:'Fără identitate',propriu:{catalog_public:'PERMIS numai publicat',citire_date_private:'REFUZ',creare_modificare:'REFUZ; excepții publice explicit contractate separat',validare_document:'REFUZ',export_situatii:'REFUZ',administrare_acces:'REFUZ',status_rezultat_job:'REFUZ'},alta_firma:'REFUZ date private',alt_cabinet:'REFUZ date private',alt_canal:'Numai catalog public publicat'},
 {rol:'member',mapping:'Rol real gateway; funcția business se confirmă',propriu:{catalog_public:'PERMIS publicat',citire_date_private:'NUMAI grant explicit',creare_modificare:'NUMAI grant explicit',validare_document:'NUMAI grant nativ explicit',export_situatii:'NUMAI grant explicit',administrare_acces:'REFUZ în lipsa delegării explicite',status_rezultat_job:'NUMAI job autorizat și scope propriu'},alta_firma:'Numai firm_access explicit; altfel REFUZ',alt_cabinet:'REFUZ',alt_canal:'Numai grant explicit'},
 {rol:'team_leader',mapping:'Rol real + aliasuri contabil/expert_contabil/accountant/operator de confirmat',propriu:{catalog_public:'PERMIS publicat',citire_date_private:'NUMAI grant explicit',creare_modificare:'NUMAI grant nativ explicit',validare_document:'NUMAI grant nativ explicit',export_situatii:'NUMAI grant explicit',administrare_acces:'NUMAI delegare aprobată, fără auto-escaladare',status_rezultat_job:'NUMAI scope/job autorizat'},alta_firma:'Numai firm_access explicit; altfel REFUZ',alt_cabinet:'REFUZ',alt_canal:'Numai grant explicit'},
 {rol:'manager cabinet',mapping:'Rol real manager; alias admin/administrator/owner de confirmat',propriu:{catalog_public:'PERMIS publicat',citire_date_private:'Conform grant business, nu implicit din rolul de administrare',creare_modificare:'Conform grant business',validare_document:'NUMAI grant nativ explicit',export_situatii:'NUMAI grant explicit',administrare_acces:'PERMIS numai cabinetul propriu și drepturile delegabile',status_rezultat_job:'NUMAI joburile cabinetului conform politicii'},alta_firma:'Administrare în cabinet și date business numai prin grant aprobat',alt_cabinet:'REFUZ',alt_canal:'Numai canal din firma autorizată și grant necesar'},
 {rol:'super platformă',mapping:'Rol real super; politica operațiilor business trebuie confirmată',propriu:{catalog_public:'PERMIS publicat',citire_date_private:'NUMAI politică explicită auditată; fără presupunere de acces contabil total',creare_modificare:'NUMAI politică explicită',validare_document:'NUMAI rol/acțiune nativă autorizată',export_situatii:'NUMAI politică explicită și audit',administrare_acces:'PERMIS acțiuni platformă contractate',status_rezultat_job:'NUMAI scop de administrare documentat'},alta_firma:'Administrare explicită; acces business după politică',alt_cabinet:'Administrare explicită; acces business după politică',alt_canal:'Configurare/depanare numai după contract și audit'},
 {rol:'gestionar G1/G2',mapping:'Rol business candidat → AD_Role Gestionar + EVA_AccesGestiune; mapping real de confirmat',propriu:{catalog_public:'PERMIS publicat',citire_date_private:'NUMAI gestiunile/locatorii acordați',creare_modificare:'NUMAI IsScriere și procesul permis',validare_document:'NUMAI IsValidare + drept nativ',export_situatii:'NUMAI raportul și gestiunea acordate',administrare_acces:'REFUZ în lipsa delegării',status_rezultat_job:'NUMAI operațiile WMS autorizate'},alta_firma:'REFUZ fără grant separat',alt_cabinet:'REFUZ',alt_canal:'Nicio extindere a dreptului doar din comanda canalului'},
 {rol:'responsabil vânzări',mapping:'Rol business candidat → roluri AD efective, de confirmat',propriu:{catalog_public:'PERMIS publicat/preview autorizat',citire_date_private:'NUMAI canale și firme acordate',creare_modificare:'NUMAI funcții vânzări acordate în ERP',validare_document:'NUMAI validare/AWB/factură conform politicii native',export_situatii:'NUMAI scope vânzări autorizat',administrare_acces:'REFUZ în lipsa delegării',status_rezultat_job:'NUMAI joburile autorizate'},alta_firma:'REFUZ fără grant separat',alt_cabinet:'REFUZ',alt_canal:'REFUZ fără grant separat'},
 {rol:'comisionar',mapping:'Rol business cerut; existența și mappingul se confirmă, nu se presupun',propriu:{catalog_public:'PERMIS catalog canal autorizat',citire_date_private:'NUMAI propriile comenzi/situații',creare_modificare:'Plasare comandă și numai modificări explicit permise',validare_document:'REFUZ administrare ERP/pick/aviz/AWB/factură',export_situatii:'NUMAI propriile situații autorizate',administrare_acces:'REFUZ',status_rezultat_job:'NUMAI propriile operații autorizate'},alta_firma:'REFUZ fără grant propriu separat',alt_cabinet:'REFUZ',alt_canal:'REFUZ fără grant separat; alt comisionar din același canal rămâne REFUZ'},
 {rol:'cont tehnic commerce/job',mapping:'token_de_serviciu + rol nativ minimal, de confirmat',propriu:{catalog_public:'Conform contract serviciu',citire_date_private:'NUMAI câmpuri/operații contractate',creare_modificare:'NUMAI operații contractate cu tenant explicit',validare_document:'REFUZ dacă nu există contract și rol nativ explicit',export_situatii:'REFUZ în afara contractului',administrare_acces:'REFUZ',status_rezultat_job:'NUMAI joburi contractate'},alta_firma:'Numai rezolvare/operare explicită necesară contractului',alt_cabinet:'Numai dacă este explicit necesar și auditat; altfel REFUZ',alt_canal:'Conform contractului minimal, fără privilegii umane'},
 {rol:'dezactivat / grant revocat / token invalid',mapping:'Se testează transversal pentru toate rolurile',propriu:{catalog_public:'Doar ca anonim, dacă public',citire_date_private:'REFUZ',creare_modificare:'REFUZ',validare_document:'REFUZ',export_situatii:'REFUZ',administrare_acces:'REFUZ',status_rezultat_job:'REFUZ'},alta_firma:'REFUZ',alt_cabinet:'REFUZ',alt_canal:'REFUZ date private'}
];

const plan={
 document:'A01 — Plan audit identitate, acces și izolare cabinet/firmă/canal',versiune:'1.0',data:'2026-11-01',limba:'ro',agent:'A01',faza:'PLAN',stare:'NEEXECUTAT',
 gate:{audit_implementare_permis:false,conditie:'A11 aprobă explicit planul integrat 10/10 după corectarea tuturor lacunelor. Acest document nu acordă scor.',interdictii:['Nu se execută auditul implementării/testele înainte de gate.','Nu se modifică repo, ERP, date de producție, taskuri sau servicii externe.','Inventarul surselor nu reprezintă constatări de produs.'],calitatea_auditului:'Scorul verifică rigoarea și completitudinea planului/auditului, nu absența defectelor produsului. Lipsa probei nu este PASS.'},
 sursa:{repository:'https://github.com/cesiroproduction/Eva-Accounting',commit:sha,copie_lectura:root,inventar:root+'/SOURCE_INVENTORY.json',data_inventariere:'2026-11-01',metoda:'Citire locală numai pentru identificarea căilor și a contractelor candidate; funcțiile, deploymentul și comportamentul rămân de confirmat la execuție.',runtime_native:'NEIDENTIFICAT ÎNCĂ — se pin-uiește buildul/versiunea/bundle/schema înainte de probe.',surse_candidate:Object.values(P).map(p=>({cale:p,prezent_in_copia_locala:fs.existsSync(path.join(root,p)),statut:'CANDIDAT_DE_CONFIRMAT_LA_AUDIT'}))},
 reguli_aplicabile:[{sursa:'AGENTS.md',aplicare:'Native-first; fără secrete; fără modificări/ștergeri producție; izolarea fiecărui store; instrucțiunile subcomponentelor se citesc înainte de auditul lor.'},{sursa:'Documentatie/echipa-2026-10-09/00_REGULI_SI_ROLURI.md',aplicare:'Designul ecranelor ERP se respectă; partenerii externi numai prin fluxurile autorizate și fără scrieri; checklisturi/trasabilitate; coada de resurse pentru teste/builduri; A11 controlează gateul.'},{sursa:'Cerințele utilizatorului în conversație',aplicare:'Cabinet/firmă/canal prin CUI/slug; G1.n și G2.n multiple; CPP/CPA cu identități distincte; comisionari cu catalog/comenzi/situații proprii; administrare comenzi numai în ERP; native-first demonstrat de două ori.'}],
 obiective:['Dovedește că identitatea și contextul autorizat sunt consecvente în portal, API, iDempiere nativ, mobil și canale.', 'Dovedește separarea cabinetelor/firmelor/gestiunilor/canalelor inclusiv la concurență, retry, export și execuție asincronă.', 'Corelează UI→API→serviciu→DB→efect→observabilitate pentru toate frontierele domeniului.', 'Preferă configurarea nativă și adaptarea codului EVA existent; justifică orice extensie prin două verificări independente.', 'Produce probe și checklisturi utilizabile de implementator, A11 și A12 fără a confunda auditul planului cu auditul produsului.'],
 scope:['Autentificare, parole, MFA, tokenuri, sesiuni și revocare.', 'Roluri gateway și native, acces la forms/windows/processes/tables și acțiuni document.', 'Cabinet/instanță/firma AD_Client/AD_Org, CUI, sluguri și mapare canale.', 'Conturi tehnice, joburi, proxy, mobil și permisiuni pe gestiune/locator.', 'Comisionari și acces propriu pe canal; public/private catalog și preview platformă.', 'Export, raport, atașament, cache și log/audit la frontiera de autorizare.'],
 excluderi_cu_owner:[{subiect:'Corectitudinea formulelor contabile/fiscale și închiderilor',owner:'A03',retinut_A01:'Drepturi, separare date, tranziții protejate și export.'},{subiect:'Migrations/constraints/date master și identitatea CPP/CPA',owner:'A02',retinut_A01:'Tenant keys, ownership, AD access și consecințe de confuzie.'},{subiect:'Logica operațională WMS/stock/assembly',owner:'A05',retinut_A01:'G1/G2/locator și read/write/validate; native role checks.'},{subiect:'Logica vânzări/G3/prețuri/comisioane',owner:'A06',retinut_A01:'Scope propriu comisionar/canal și restricția administrării ERP.'},{subiect:'AWB/retur/plăți/ramburs',owner:'A07',retinut_A01:'Actor, scope și autorizație tranziție; fără apeluri partener live.'},{subiect:'Storefront/Spree și conversii marketing',owner:'A08',retinut_A01:'Sesiune, separare canal și proiecții publice/private.'},{subiect:'Design/UX integral, accesibilitate și meniuri',owner:'A09',retinut_A01:'Context vizibil, stări de acces, recuperare, FE/BE consistency.'},{subiect:'Deployment/rețea/jobs/resurse și hardening infrastructură',owner:'A10',retinut_A01:'Frontiere trust, credențiale, identitate în job și auditabilitate.'}],
 interfete_si_responsabili:[
  {cu:'A02',contract:'cabinet→instanță→AD_Client/Org, keys/constraints, AD access metadata și DB read-only',intrare:'Inventar schema/migrare și fixtures',iesire:'C10/C14/C20/C24 + probe ownership și native comparison'},
  {cu:'A03',contract:'drepturi în toate capitolele contabile, document actions, raport/export',intrare:'Matrice capitole→documente/tabele/procese',iesire:'C12–C16/C33 și probe cross-tenant pe date financiare'},
  {cu:'A04',contract:'achiziții/furnizori/importuri/SAGA',intrare:'Pipelineuri import și documente',iesire:'Actor/context la import și IDOR părinte/copil'},
  {cu:'A05',contract:'gestiuni G1.n/G2.n, locatori, mobil, inventar, asamblare',intrare:'Matrice rol→gestiune→operație și fixtures',iesire:'P05/C23/C24 cu drepturi distincte read/write/validate'},
  {cu:'A06',contract:'G3, comenzi, canale, comisionari',intrare:'Proprietar comandă/situație și puncte de administrare ERP',iesire:'P07/C25 și acces propriu per persoană/canal'},
  {cu:'A07',contract:'validare vânzări, AWB/factură, plăți și retur',intrare:'Tranziții și roluri autorizate',iesire:'Refuz operații din site și identificare actor ERP'},
  {cu:'A08',contract:'site per canal, public/private, token service și preview',intrare:'Endpoint inventory storefront și rutare reală',iesire:'C09/C25–C28/C31 și teste de izolare canal'},
  {cu:'A09',contract:'meniu/context/401–403/no firm/multi-tab/mobile',intrare:'Ecrane și baseline UX aprobat',iesire:'Capturi cu context și erori, fără redesign necerut'},
  {cu:'A10',contract:'proxy/upstream, secret, worker/cache, observabilitate și fixtures',intrare:'Manifest mediu/version, transport izolat și coadă resurse',iesire:'P01/P08/P09 și revocare/retry/race pe frontieră'},
  {cu:'A11',contract:'gate plan și review independent al probelor',intrare:'Checklist rubrică și observații',iesire:'Plan, registru de acoperire, evidence/finding și remediere proprie'},
  {cu:'A12',contract:'audit fiecare task P01 finalizat',intrare:'ID canonic/status/descriere/acceptance/commit',iesire:'Task→control→pipeline→probă→finding; niciun task fără verificare'}
 ],
 fixtures:{mediu:'Izolat, cu transport parteneri blocat/simulat; nicio acțiune live.',topologie:['Cabinet A și cabinet B în instanțe distincte.', 'A1/A2 în A și B1/B2 în B; include același CUI în A1/B1 dacă modelul permite acest caz de cabinet și AD_Client_ID numeric identic în DB separate.', 'Două canale per firmă, două persoane comisionar per canal, G1.1/G1.2/G2.1/G2.2 și locatori distincți.', 'CPP și CPA pentru produs aparent identic au ID-uri interne distincte; coduri canar sintetice fără SKU/EAN ca identitate.', 'Documente/părinți/linii/export/job cu canari diferiți, identități active/dezactivate și granturi read/write/validate.'],politica_date:'Numai date sintetice; identificatori reali pseudonimizați în probe. Curățare reversibilă a fixtureului numai de ownerul mediului, niciodată resetare de producție.',politici_de_confirmat:['MFA și recuperare/parole/rate limit.', 'TTL/revocare/rotație token și sesiune native.', 'Puterea super, delegarea manager/team_leader și rolurile business.', 'Comisionar→user/partner/channel și propriile situații.', 'Politica joburilor începute înaintea revocării.', 'Referințe globale AD_Client/Org zero și publicarea câmpurilor catalog.'],regula_lipsa:'Politica neconfirmată este BLOCAT sau decizie de cerut ownerului; nu se inventează un prag și nu se marchează PASS.'},
 role_tenant_matrix:{stare:'PROPUNERE_DE_VALIDAT_CU_OWNERII înaintea execuției',actiuni:matrixActions,regula:'Fiecare celulă aplicabilă primește caz pozitiv/refuz cu firma/cabinet/canal propriu și străin. Eticheta unui rol business nu dovedește existența lui în runtime.',randuri:matrix},
 controale:controls,pipelineuri:pipelines,
 native_reuse_check:{id:'NR-01',stare:'NEEXECUTAT',obiecte:['AD_User','AD_User_Roles','AD_Role','AD_Client','AD_Org','AD_Session','AD_Form_Access','AD_Window_Access','AD_Process_Access','AD_Table_Access','AD_Table.AccessLevel','M_Warehouse','M_Locator','AD_PInstance','AD_Attachment','AD_ChangeLog','DocAction/DocumentEngine','C_BPartner/SalesRep/Commission: după nevoie'],sursa_1:'Codul iDempiere nativ exact/pinuit pentru versiunea instalată; fișier:linie, commit/tag și contract.',sursa_2:'Instanța EVA: metadata AD/configurare + comportament real în mediu de test, rol permis/refuzat, versiune bundle și captură.',comparatie_EVA:'Calea EVA și liniile care adaptează/verifică mecanismul nativ; se separă clar nativ/configurare/EVA/noi cerințe.',decizie_permisa:['CONFIGUREAZĂ NATIV','ADAPTEAZĂ EXISTENT EVA','EXTINDE MINIMAL','NOU JUSTIFICAT'],template:{nevoie:null,mecanism_nativ:null,proba_sursa_1:null,proba_sursa_2:null,cod_EVA:null,gap_demonstrat:null,decizie:null,motivatie:null,frontend_impact:null,backend_impact:null,db_impact:null,ux_impact:null,taskuri_afectate:[]}},
 template_proba:{evidence_id:'A01.E0001',control_id:null,pipeline_id:null,task_ids:[],timestamp_UTC:null,sha:sha,runtime_build:null,schema_version:null,mediu:null,actor_rol:null,scope_pseudonimizat:{cabinet:null,firma:null,AD_Client_ID:null,AD_Org_ID:null,canal:null,gestiune:null},preconditii:null,pasi_reproductibili:[],expected:null,actual:null,FE_capture:null,BE_file_line_and_sanitized_request:null,DB_readonly_before_after:null,native_proof_1:null,native_proof_2:null,UX_recovery:null,trace_job_process_transaction_ids:[],artefacte_hashuri:[],rezultat:'NEEXECUTAT',limitari:[],reviewer_A11:null},
 template_finding:{finding_id:'A01.F0001',titlu:null,control_ids:[],pipeline_ids:[],task_ids:[],versiune:null,actor_scope:null,preconditii:null,repro_pasi:[],expected:null,actual:null,probe:[],severitate:null,criteriu_severitate:'Impact demonstrat + scope afectat + reproductibilitate; se folosește rubrica integrată A11, nu etichete alarmiste.',risc_business:null,cauza_confirmata_sau_ipoteza:null,native_reuse_decision:null,remediere_propunere:null,owner:null,checklist_implementator:[],autoverificare_implementator:[],retest_evidence:[],stare:'DESCHIS după confirmare, nu înainte'},
 checklist_implementator:['Reproduce findingul pe SHA/build și fixture declarate; confirmă cauza, nu doar simptomul UI.', 'Identifică mecanismul nativ din două surse și consemnează de ce configurarea/adaptarea este sau nu suficientă.', 'Corectează toate suprafețele aceleiași politici: UI, API, native, mobil, job, export și cache relevante.', 'Verifică propriul scope și fiecare frontieră străină din matrice; include rol revocat/dezactivat.', 'Verifică retry, concurență, timeout și starea UI după eșec, fără efecte externe.', 'Atașează probe FE/BE/DB/UX/native și corelația task→commit→control→pipeline.', 'Reexecută probele afectate de diff și regresiile justificate, fără a marca test neexecutat drept trecut.', 'Fă autoverificarea completitudinii și predă A11 toate lipsurile; taskul rămâne neînchis dacă lipsesc condițiile de acceptare.'],
 acoperire_taskuri:{regula_ID:'Păstrează ID-ul canonic din inventarul proiectului, de exemplu P01.C03.T0019 sau C03.T0019 dacă acesta este formatul sursei; nu redenumi și nu inventa echivalențe. Referințele istorice din comentarii se înregistrează separat.',status:'Inventarul live/export actual al taskurilor este furnizat de A12/root; statusul finalizat nu se deduce din comentarii de cod.',template:{task_id:null,status_sursa:null,status_timestamp:null,obiectiv_acceptance:null,commits:[],controale:[],pipelineuri:[],probe:[],findings:[],native_reuse:null,verdict:'NEEXECUTAT'},regula_completitudine:'Fiecare task finalizat cu atingere A01 are mapare explicită; taskurile transversale primesc owner principal și co-review, nu sunt pierdute între domenii.'},
 executie_dupa_gate:['Confirmă politica/fixtures/versiunea și citește instrucțiunile suplimentare ale componentelor vizate.', 'Închide inventarul activ și denominatorul împreună cu A02/A09/A10/A12.', 'Rulează controalele de identitate/context înaintea operațiilor business, cu transport izolat.', 'Rulează pipelineurile complete și scenariile negative/concurente cu probe corelate.', 'Efectuează comparația native-first și redactează findings numai pe dovezi.', 'Predă auditul A11; reia probele/analiza cerute până când toate punctele de calitate sunt satisfăcute; nu ascunde blocajele.'],
 auto_control_plan:{scope_clar:true,controale_specifice:controls.length,pipelineuri_complete_candidate:pipelines.length,fiecare_control_NEEXECUTAT:controls.every(c=>c.stare==='NEEXECUTAT'),matrice_rol_scope:true,evidence_FE_BE_DB_UX_native:true,negative_retries_races_recovery:true,native_doua_surse:true,owners_interfete:true,task_traceability_template:true,audit_produs_executat:false,scor_acordat:false},
 limite_actuale:['Nu s-a auditat implementarea și nu s-au executat teste.', 'Căile sunt candidate reale din inventar/copia materializată; fluxurile active și runtimeul trebuie confirmate după gate.', 'Numele unor tabele de canal/job/mapping sunt intenționat lăsate de confirmat, pentru a nu inventa schema.', 'Cerințele nerealizate/necunoscute nu sunt tratate ca existente doar pentru că apar în plan.', 'Acest agent nu folosește browserul, nu schimbă taskuri și nu trimite mesaje externe.']
};
plan.schema='eva.audit.executor-plan.v1';
plan.generated_utc=new Date().toISOString();
plan.sursa.ramura='Ramura implicită și momentul fetchului: din manifestul coordonatorului; SHA-ul fixat mai sus este autoritativ pentru acest plan.';
plan.sursa.inventory_sha256=require('crypto').createHash('sha256').update(fs.readFileSync(path.join(root,'SOURCE_INVENTORY.json'))).digest('hex');
plan.matrice_acces_disponibil=[
 {resursa:'Cod materializat la SHA pinuit',acces:'DISPONIBIL pentru citire',proba:'Toate cele '+Object.keys(P).length+' căi candidate A01 există în copia de lectură.',limitare:'Nu dovedește că sunt active în deployment.'},
 {resursa:'Git upstream/branch și inventarul global',acces:'FURNIZAT de coordonator',proba:'SHA + SOURCE_INVENTORY.json',limitare:'A01 nu face fetch independent.'},
 {resursa:'UI live și iDempiere nativ',acces:'NEEXECUTAT; root gestionează accesul browserului',proba:null,limitare:'A01 nu folosește browserul în faza PLAN.'},
 {resursa:'DB runtime read-only / metadata AD',acces:'DE CONFIRMAT cu A02/root',proba:null,limitare:'Nicio concluzie privind schema instalată.'},
 {resursa:'Mediu fixture + conturi roluri + transport izolat',acces:'DE CONFIRMAT cu A10/root',proba:null,limitare:'Teste blocate până la gate și precondiții.'},
 {resursa:'Inventar actual taskuri P01',acces:'DE FURNIZAT de A12/root',proba:null,limitare:'Nu se deduce starea taskului din cod/commit.'}
];
plan.acoperire_taskuri.sursa_autoritativa='eva-org.com/claude — inventarul curent și criteriile originale capturate de A12/root cu URL/export, filtre, paginare, total declarat/extras, timestamp și hash.';
plan.acoperire_taskuri.template.stari_separate={portal_task:null,commit_exista:null,test_executat:null,instalat_runtime:null};
plan.acoperire_taskuri.template.cerintele_originale_nemodificate=null;
plan.acoperire_taskuri.template.cerintele_clarificate=[];
plan.acoperire_taskuri.template.cod_frontend_backend_db=[];
plan.acoperire_taskuri.template.review_A11=null;
plan.acoperire_taskuri.regula_bidirectionala='La predare se generează atât cerință/task→control/pipeline/cod/probă/finding/A11, cât și control/cod/probă→cerință/task; se enumeră orfanele și duplicările. Codul scurt Tnnnn nu identifică global taskul.';
plan.dispozitie_istoric=[
 {idee:'Reutilizare maximă iDempiere/EVA și verificare în cod plus nativ',dispozitie:'MENȚINUT',controale:['A01.C16','A01.C34'],owners:['A01','A02','A10']},
 {idee:'Cabinet/firma/canal prin rutele CUI și numele canalului',dispozitie:'MENȚINUT; runtime DE VERIFICAT',controale:['A01.C09','A01.C10','A01.C11'],owners:['A01','A08','A09','A10']},
 {idee:'G1.n și G2.n multiple, locatori, G3 capacitate combinată',dispozitie:'MENȚINUT; logica stoc/capacitate la A05/A06',controale:['A01.C24','A01.C33'],owners:['A01','A05','A06']},
 {idee:'CPP și CPA păstrează aceeași identitate',dispozitie:'ÎNLOCUIT PRIN CLARIFICAREA UTILIZATORULUI: identități diferite, cod intern permanent distinct de SKU/EAN.',controale:['A01.C26','A01.C33'],owners:['A02','A01','A06']},
 {idee:'Cutii/muncă în G2; cost și consum o singură dată în G1 fără stoc contabil suplimentar de set dezasamblabil',dispozitie:'MENȚINUT; invariant financiar la A03/A05, acces la A01',controale:['A01.C15','A01.C24','A01.C33'],owners:['A03','A05','A01']},
 {idee:'Comisionar pe site: catalog, plasare comenzi și situațiile proprii cu drepturi pe canal',dispozitie:'MENȚINUT',controale:['A01.C25','A01.C26'],owners:['A01','A06','A08']},
 {idee:'Administrarea comenzilor numai în iDempiere: gestionar→pregătire/pick/aviz→responsabil/automat→AWB/factură după setări',dispozitie:'MENȚINUT; ordinea business la A05/A06/A07',controale:['A01.C15','A01.C25','A01.C33'],owners:['A01','A05','A06','A07']},
 {idee:'Site distinct per canal, inclusiv preview platformă; setări și UX clare; toate capitolele contabile',dispozitie:'MENȚINUT',controale:['A01.C01','A01.C26','A01.C33'],owners:['A01','A03','A08','A09','A10']},
 {idee:'Manualele/auditurile precedente și fișierele C03/C10/explicativ',dispozitie:'DOCUMENTARE DE CORELAT cu A12/root; nu sunt dovadă de instalare/execuție. Constatările istorice se reverifică la SHA nou.',controale:['A01.C33','A01.C35'],owners:['A11','A12','A01']}
];
plan.inventar_acoperire_template={denominatori:{module_active:null,ecrane_active:null,rute_metode_active:null,joburi_active:null,tabele_migrari_relevante:null,rol_scope_actiune_celule_aplicabile:null,taskuri_P01_finalizate_relevante:null},rand:{inventar_id:null,tip:null,sursa_exacta:null,activ_in_runtime:'NECONFIRMAT',owner:null,coowners:[],control_ids:[],pipeline_ids:[],task_ids:[],evidence_ids:[],stare:'NEEXECUTAT'},regula:'Denominatorul nu este numărul de controale. Un element activ fără owner/control/probă rămâne vizibil și blochează completitudinea; N/A se aprobă explicit de A11.'};
plan.contracte_interfata_template={furnizor:null,consumator:null,actor:null,intrare:{cabinet_id:null,tenant_cui:null,AD_Client_ID:null,AD_Org_ID:null,actor_id:null,role_id:null,channel_id:null,warehouse_id:null,object_id:null,idempotency_key_hash:null,trace_id:null},iesire:{status:null,scope_confirmat:null,business_id:null,state:null,error_code:null},invariante:['Contextul autorizat este stabil și verificat la frontieră.', 'Cheile externe sunt validate față de părinte și tenant.', 'Identitatea clientului nu se preia din input neîncredere fără verificare.', 'Retryul nu traversează cabinetul/firma/canalul.', 'Eșecul lasă o stare explicită, reconciliabilă.'],proba_integrare:null,owner_acceptanta:null};
plan.regresie_si_reaudit={
 schimbare_SHA:'Se păstrează manifestul/probele vechi, se pin-uiește noul SHA și se construiește diff→controale/pipelineuri/taskuri; se reexecută toate frontierele afectate și vecinătățile justificate.',
 schimbare_task:'A12 recapturează starea/criteriile, păstrează originalul și versiunea nouă; schimbarea criteriilor nu rescrie retroactiv verdictul.',
 selectia_testelor:'Revizie/static pentru toate căile inventariate; teste unitare numai pentru politica pură unde aduc probă independentă; integrare/UI/manual/DB pentru frontiere și efecte. Testul care reproduce implementarea nu substituie rezultatul business.',
 tinte_regresie:['Login/refresh/revoke în portal/native/mobil.', 'Tenant resolver, client map, role aliases și org0 policy.', 'Grant/revoke/provision și job status/result.', 'Gestiuni/locatori și canal/comisionar.', 'Export/download/cache și document actions native.'],
 flaky:'Se păstrează toate rulările și condițiile; o rerulare trecută nu șterge eșecul. Se identifică sursa (timing/cache/date/runtime), se stabilizează fixtureul și A11 decide suficiența probei.',
 reproducere_independenta:'A11 primește datele sintetice, pașii exacți, versiunea, artefactele hash și rezultatul așteptat; cel puțin frontierele critice se reproduc fără ajutorul autorului.',
 bucla:'RESPINS_A11→corecție plan/raport→versiune nouă cu hash→reverificare independentă; fără număr maxim care aprobă automat.',
 fals_pozitiv:'Constatarea contestată rămâne în istoric cu proba inițială; se adaugă contra-proba, cauza diferenței și decizia A11. Nu se șterge tacit.',
 stari_distincte:['NEEXECUTAT','BLOCAT','PASS','FAIL','NEEXECUTAT_DEPENDENTA_FAIL cu acceptare A11','N/A justificat și acceptat A11'],
 inchidere:'Nota calității se acordă numai de A11; severitatea/încrederea/starea findingului și sănătatea produsului sunt câmpuri separate.'
};
plan.template_finding.incredere=null;
plan.acoperire_taskuri.regula_ID='ID-ul canonic de audit include proiect și capitol, de exemplu P01.C03.T0001. Codul original și aliasurile se păstrează separat; dacă sursa spune C03.T0001, completarea cu proiect se face numai prin contextul P01 verificat, fără echivalențe inventate. T0001 nu este unic global.';
plan.acoperire_taskuri.template.cod_original=null;
plan.acoperire_taskuri.template.aliasuri=[];
plan.template_finding.istoric_contestare_retest=[];
plan.template_proba.cleanup_executat=null;
for(const c of controls){
 c.fixture_refs=['fixtures.topologie','role_tenant_matrix'];
 c.cleanup='După probă, restabilește numai fixtureurile și granturile sintetice create de control, cu ownerul mediului; verifică absența artefactelor/joburilor/tokenurilor de test reziduale. Producția rămâne read-only; fără resetări de DB/volume.';
 c.comanda_proba='Se completează după gate cu pașii/comenzile exacte aferente mediului și fără secrete; comenzile nu se inventează înaintea identificării runtimeului.';
}
for(const p of pipelines){
 p.preconditii=['GATE-A11 aprobat', 'Versiune/runtime/fixture pin-uite', 'Rol și scope explicite din matrice', 'Transport extern izolat'];
 p.trigger_actor='Acțiunea utilizatorului/serviciului autorizat din etapa FE/API; identitatea exactă se completează în fișa probei.';
 p.stari=['inițial','în curs','confirmat','refuzat','eșuat','rezultat necunoscut după timeout','recuperat'];
 p.iesire_din_flux='Stare finală business confirmată prin DB/native sau eroare/refuz explicit cu context păstrat; nu rămâne spinner fără explicație.';
 p.checklist_UI=['empty','loading','error','timeout','partial','success','keyboard/focus','responsive/mobil dacă suprafața este disponibilă','scanner pentru fluxul mobil/WMS cu A05/A09','păstrarea datelor valide','recuperare fără schimbare scope'];
}
pipelines.find(p=>p.id==='A01.P07').controale.push('A01.C36');
pipelines.find(p=>p.id==='A01.P09').controale.push('A01.C37');
pipelines.find(p=>p.id==='A01.P04').controale.push('A01.C38');
fs.writeFileSync(dest,JSON.stringify(plan,null,2)+'\n','utf8');
const missing = plan.sursa.surse_candidate.filter(x=>!x.prezent_in_copia_locala);
process.stdout.write(JSON.stringify({output:dest,controls:controls.length,pipelines:pipelines.length,all_NEEXECUTAT:controls.every(c=>c.stare==='NEEXECUTAT'),missing_candidate_files:missing.map(x=>x.cale),bytes:fs.statSync(dest).size},null,2));
