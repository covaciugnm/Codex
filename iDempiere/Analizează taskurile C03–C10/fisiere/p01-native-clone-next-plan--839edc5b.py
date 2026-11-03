from pathlib import Path
import datetime
import hashlib
import json

root = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
folder = root/'executie/R11_fisiere/A05/Val_04'
dest = folder/'Pregatire_clona_nativa_N05_propusa.json'
assert not dest.exists()
native = Path('D:/CodexWork/eva-audit-secondary-20261102/native/org.adempiere.base/src/org/compiere')
paths = [native/'db/Database.java',native/'db/CConnection.java',native/'util/DB.java',native/'Adempiere.java',
         Path('D:/CodexWork/p01-local-pg16/GardenWorld-A07.dump'),
         Path('D:/CodexWork/a12-r5-classes/all_deps/org.adempiere.base_13.0.0.202603090043.jar'),
         Path('D:/CodexWork/a05-support-jars/org.eclipse.osgi_3.18.500.v20230801-1826.jar'),
         Path('D:/CodexWork/a05-support-jars/org.postgresql.jdbc_42.7.8.jar')]
sources = [{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths]
plan = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'A05','peer':'A11','prepared_by':'COORDONATOR',
        'state':'PLAN DE MEDIU PROPUS; NICIO CLONĂ NATIVĂ NOUĂ PORNITĂ; NU CONFERĂ RECEPȚIE',
        'head':'2fe90ed3f128c33dff7cf9f8674e664a70679390',
        'problem':'Constructorul PO din martorul A05 se oprește în POInfo/PreparedStatementProxy. CConnection și DB au nevoie de adaptorul nativ PostgreSQL rezolvat prin Service.locator și de dicționarul complet.',
        'existing_cache':sources,
        'native_anchors':[
            {'file':'org/compiere/db/Database.java','lines':[63,75],'meaning':'Adaptorul AdempiereDatabase este rezolvat prin Service.locator().locate și filtrul id.'},
            {'file':'org/compiere/db/CConnection.java','lines':[622,624,1083],'meaning':'setType și getDatabase folosesc registrul de servicii Database, nu numai driverul JDBC.'},
            {'file':'org/compiere/util/DB.java','lines':[187,333],'meaning':'DB.setDBTarget stabilește contextul de conexiune; DB.getDatabase îl consultă.'},
            {'file':'org/compiere/Adempiere.java','lines':[664,670,680,689,729],'meaning':'startupEnvironment cere DB și build compatibil, MSystem, ModelValidationEngine și initializează workflow/archive; în mod server apelează DB.updateMail.'}
        ],
        'steps':[
            {'id':'N05-LAB-01','action':'Verifică proveniența/hashul seedului GardenWorld și comparația versiunii AD_System cu JAR-ul nativ. Refolosește arhiva demo; nu copia baza unui client.', 'oracle':'Dovadă de proveniență a seedului, versiune compatibilă și exclusiv rânduri demo/sintetice.'},
            {'id':'N05-LAB-02','action':'Inventariază din runtime-ul instalat, numai citire, manifestele adaptorului PostgreSQL, frameworkului și dependințelor OSGi; copiază numai binarele necesare într-un director de laborator. Creează de la zero configul local; nu copia proprietățile operaționale.', 'oracle':'Manifest de bundle/OID/SHA și dependențe rezolvate; DSN explicit loopback către cluster propriu.'},
            {'id':'N05-LAB-03','action':'Creează cluster PostgreSQL efemer propriu, port liber și roluri sintetice; restaurează GardenWorld și aplică doar migrările EVA necesare G1/G2/BOM din SHA-ul fixat, cu manifest înainte/după.', 'oracle':'AD_Table/Column și tabelele fizice concordă; sursele și migrările sunt identificabile; niciun endpoint extern configurat.'},
            {'id':'N05-LAB-04','action':'Pornește cadrul nativ OSGi în laborator, în mod fără interfață și fără scheduler/conectori externi. Înregistrează adaptorul nativ și datasource-ul; verifică POInfo, fabrica de modele, ModelValidationEngine și activarea abonatului EvaNotaSetBomEvents.', 'oracle':'Interogare de sănătate nativă și citirea PO reale; raport al serviciilor active; zero acces către sisteme operaționale. O dublură de Service.locator este doar comparator, nu recepție OSGi.'},
            {'id':'N05-LAB-05','action':'Pregătește actorii, CPP/CPA distincte, două gestiuni G2 și locatori, BOM inițial. Execută mai întâi salvare serială prin MPPProductBOMLine.saveEx și procesul AD normal, apoi cele două tranzacții concurente ale cursei deja demonstrate.', 'oracle':'Părinte BOM, linii, proces, mișcări și stoc recitite pe conexiune nouă; rețeta serială refuzată când există stoc; concurența are etalon independent de conservare.'},
            {'id':'N05-LAB-06','action':'Extinde separat la contabilizarea G1/cutii/manoperă și disponibilitatea G3 doar după ce constructorul și tranzacțiile PO sunt reale; nu transfera automat rezultatul stocului WMS.', 'oracle':'Fact_Acct și documentele native exacte, cost o singură dată și lipsa stocului contabil dublat; probele G1/G3 au propriul verdict.'},
            {'id':'N05-LAB-07','action':'Oprește procesul OSGi, închide tranzacțiile, oprește și elimină numai clusterul/directorul creat, după verificarea căii absolute. Păstrează manifestele, logurile mascate și martorii.', 'oracle':'Porturi închise și căi temporare absente; datele operaționale nu au fost scrise.'}
        ],
        'next_gate':'A11 verifică planul de laborator și canarii de izolare înainte de atribuirea unui rezultat PO/OSGi. Planul principal R11 v3 rămâne referința pentru testele de produs.',
        'not_external_blocker':'Dependența identificată este pregătirea internă a runtime-ului/clasei DB/serviciilor. Nu necesită stație hardware și nu justifică suspendarea auditului codului.',
        'limits':['Cache-ul sursă este un indiciu tehnic hashuit; identitatea față de binarul efectiv trebuie confirmată în preflight.','Prezența arhivei GardenWorld nu înseamnă că această rundă a restaurat-o sau a validat toate rândurile.','Planul nu execută bootstrapul sau migrările și nu schimbă concluzia A05 despre lipsa efectului PO persistent.']}
dest.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
print(hashlib.sha256(dest.read_bytes()).hexdigest())
