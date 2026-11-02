from pathlib import Path
import re
O=Path(__file__).parent
p=O/'build_v3.py';s=p.read_text(encoding='utf-8')
s=s.replace('Regulile exacte de randare se fixează pentru versiunea Next.js aleasă în ADR03. [T1]','Regulile de randare Flask și cache se documentează după comportamentul existent, în ADR03; nu se adaugă un server Next.js.')
s=s.replace('până la finalul valului 4, dintre care 10 la primul val','până la finalul T4, dintre care 10 în T2')
s=s.replace('Fișierul de producție este, în milimetri','Fișierul de producție se definește în milimetri')
s=s.replace('Programul lucrător este 09–18, luni–vineri, Europe/Bucharest, exceptând sărbătorile, în afara P1.','Programul mentenanței temei este 09–18, luni–vineri, Europe/Bucharest, exceptând sărbătorile. Pentru P1 în afara programului se aplică exclusiv contractul separat de operare, dacă există.')
# Use existing template context and APIs, never mandate new API semantics.
s=s.replace('Înainte de plată, backendul întoarce o ofertă cu versiune și expirare; modificarea totalului este prezentată clientului.','Înainte de plată se folosește validarea actuală a backendului; modificarea totalului este prezentată clientului. Versiunea și expirarea se folosesc dacă există în contract, fără introducerea unui API nou.')
s=s.replace('Instanțe multiple; cache invalidat prin evenimente','Mecanismul de invalidare existent demonstrat')
p.write_text(s,encoding='utf-8')

p=O/'build_trace_v3.py';s=p.read_text(encoding='utf-8')
anchor='used=[i for g in groups for i in g[\'ids\']]'
new=r'''# Clarificarea finală a beneficiarului prevalează asupra propunerilor auditorilor.
overrides={
'D01 din sursa actuală':('§1; §11; §22','D01 din sursa operațională existentă, prin export actual sau SQL de citire versionat; fără API de export nou. U:/cesiro.com este baza indicată; șase fișiere tehnice comparate sunt identice cu cesiro1-site.','Date/platformă S2: snapshot, contracte actuale și demonstrații.','Date curente necesare'),
'Producția și SLO':('§9.1; §13; §17.1','Se păstrează Dockerul existent. ADR04 verifică disponibilitatea, backupurile și RPO/RTO; dacă există deficit, modernizarea se estimează separat. Tema nu poate garanta99,9% și nu include migrare implicită.','Inventar domeniu/tenant/imagine, backup și rollback temă≤15min.','Specificat ca verificare a platformei'),
'Alternative React':('§9 ADR01','Se alege tema înregistrată Flask + componente React, cu asseturi statice. Backendul și API-ul rămân existente; Next.js separat și runtime Node de producție nu sunt necesare.','Mecanism de teme confirmat static în U:/cesiro.com; demonstrație runtime în D01.','Decizie aliniată beneficiarului'),
'Bugetul AI':('§8.1; §17.1','600 EUR/lună și≤0,06 EUR/sesiune sunt plafon și țintă pentru o extensie aprobată separat; consumul AI nou nu este inclus în bugetul temei. Se conectează doar un serviciu existent demonstrat.','D01 inventariază capabilitatea; fără serviciu, căutare clasică și suport uman.','Condiționat de serviciul existent'),
'Calendar recalibrat':('§16; §17','Domeniul final este temă pe API existent, cu16 săptămâni și160–200 zile. Nu se promite programul complet din audit în același efort: backendurile și serviciile inexistente sunt excluse, ideile rămân proiectate separat.','Registru disponibil/condiționat/viitor, plan nominal și recepție pe etape.','Reestimat pentru domeniul clarificat'),
'Efort de jos în sus':('§17; §17.1','11 pachete de temă, UX/React/integrare/QA, însumează160 zile; interval160–200. Integrarea Python nu construiește API. Efortul pentru întregul program extins nu se confundă cu cel al temei.','Aritmetică verificată; ofertare după D01.','Reestimat independent'),
'Capacitatea echipei':('§17','Medie2–2,5 FTE pe80 zile nominale, vârf3–4, plus PO și editori CESIRO separați. Funcțiile backend absente nu sunt ascunse în alocări.','Plan nominal S2 și actualizare după demonstrația contractelor.' ,'Specificat'),
'Garanție și SLA':('§17.3; §17.1','90 zile garanție pentru temă, ofertă180; mentenanță750–1.500 EUR/lună în program09–18. Permanența de infrastructură24/7 și remedierea backendului sunt separate.','Contract de mentenanță și operare distinct; nu se declară permanență fără acoperire.','Specificat'),
'Motor EVA comun':('§9; §11','Tema se livrează ca modul în registrul actual și respectă contractele comune. Nu se creează versiune API nouă sau ramură independentă a logicii comerciale.','Matrice de ecrane → contracte existente; fără copierea coșului/prețului/stocului în temă.','Specificat'),
}
conditional={'Asistent după cumpărare','Etaloane inovare','Valoarea asistenței','Capacitate de producție','Personalizare și retragere','Date de firmă și TVA','Obiective Pro'}
for g in groups:
    if g['topic'] in overrides:
        g['where'],g['decision'],g['proof'],g['status']=overrides[g['topic']]
    elif g['topic'] in conditional:
        g['status']='Condiționat de capabilitatea existentă'
        g['decision']='Tema nu construiește API sau serviciu nou. Cerința se activează numai cu suport existent demonstrat; altfel rămâne extensie separată. '+g['decision']
    elif g['topic'] in {'Autoservire','Funcția de retragere','Matrice și recepție legală'}:
        g['decision']+=' Interfața folosește rutele existente; un deficit legal al platformei este escaladat separat și blochează domeniul afectat, fără API paralel în temă.'

'''
assert anchor in s;s=s.replace(anchor,new+anchor)
s=s.replace('Calendar 26 săptămâni; efort 360–450 zile, justificat pe funcții. Topologie de producție cu condiții de verificare.','Temă React integrată în platforma Flask existentă, fără sistem API nou.16 săptămâni și160–200 zile pentru domeniul de bază; verificarea Dockerului actual, fără migrare implicită.')
s=s.replace('Răspuns la auditurile CESIRO versiunea 2','Răspuns la auditurile CESIRO versiunea 2')
# Replace technical directives with decisions for the selected architecture.
a=s.index('tech=[');b=s.index('for code,decision,proof in tech:',a)
s=s[:a]+r'''tech=[
('T2-01 Cache Sync','Adaptat arhitecturii alese. Se păstrează randarea Flask și cacheul actual; nu există un strat Next.js nou de sincronizat. Se demonstrează consistența preț/stoc și validarea comenzii pe contractele actuale. Un deficit al motorului comun se tratează separat.','§9.2; §10. Zero confirmări comerciale invalide; nicio interfață API nouă.'),
('T2-02 Search Engine','Neintrodus în tema de bază. Se reutilizează căutarea și filtrele existente. Meilisearch/pgvector rămân opțiuni pentru o extensie aprobată separat, fără obligația de a construi un API de căutare nou.','§9 ADR02; §11. Catalog și filtre actuale demonstrate în D01.'),
('T2-03 Experiență UX','Adoptat. Configurator2D cu fotografii aprobate, selecție locală și operațiile actuale de coș; AR este extensie. AOV rămâne ipoteză de test, nu rezultat deja obținut.','§8.2; §17.2; §21.6.12 scene și alternativă accesibilă.'),
('T2-04 Personalizare','Condiționat. Designul și standardul SVG/PDF sunt definite. Tema se conectează la funcția existentă dacă aceasta poate produce fișierul corect; în lipsă, folosește cererea de ofertă existentă, fără serviciu nou în bugetul temei.','§8.2; §17.10 produse/proofuri doar într-un pilot activat explicit.'),
('T2-05 e-Factura B2C','Separat de temă. Se reutilizează integrarea fiscală existentă după demonstrație. Dacă lipsește, este deficit al platformei care trebuie soluționat distinct; tema nu construiește API ANAF sau OAuth nou.','§12.1; R09. Responsabilul fiscal probează conformitatea înaintea domeniului afectat.'),
('T2-06 Documente Food','Adoptat la nivel de date și prezentare. Tema afișează actele aprobate disponibile în mecanismul existent. Documente reale, versiune și acces potrivit; nu se presupune obligația universală de publicare a fiecărui PDF de lot.','§2; §13.2; R09. Documentele inexistente se obțin de la producător, nu se generează cu AI.'),
('T2-07 Premise de arhitectură','Clarificat. Backendul Python, API-ul și Dockerul existente rămân baza; React nu presupune Next.js sau backend nou. Registry și contractele de teme sunt confirmate static; commitul GitHub și containerele active nu sunt certificate.','§1; §9; I6. U:/cesiro.com și verificare runtime D01.'),
('T2-08 Decizie de execuție','Clarificat. Recomandarea de aprobare din audit nu autorizează implementarea. Cerința beneficiarului de a nu construi un sistem API nou prevalează; această revizie produce doar documentație.','§0; §22. Site, Docker, backend și repository nemodificate.')]
''' +s[b:]
s=s.replace('calendar26 săptămâni în loc de18','calendar16 săptămâni pentru tema cu domeniu redus')
s=s.replace('calendar 26 săptămâni în loc de 18','calendar16 săptămâni pentru tema cu domeniu redus')
s=s.replace('§17 WBS 360–450','§17 WBS160–200')
s=s.replace('Înlocuite de WBS:106/360 zile = 29,4% și interval360–450. Bugetele V2 nu se folosesc la ofertarea V3.','Înlocuite de11 pachete pentru temă:160–200 zile. Funcțiile backend inexistente sunt separate; bugetele V2 nu se folosesc la ofertarea V3.')
s=s.replace('ADR01/03/04 la S2, ADR02 și deviz final la S4','ADR01–04 și mapare la contractele actuale la S2; deviz după inventar')
s=s.replace('S2/S4','S2')
s=s.replace('o decizie explicită în proiectul V3.','o decizie explicită în proiectul V3. Precizarea finală a beneficiarului este obligatorie: temă nouă pe backendul și API-ul existente, fără sistem API nou; funcțiile nesusținute sunt extensii separate.')
for a,b in {'garanție99':'garanție 99','garanta99':'garanta 99','temă≤15min':'temă ≤15 min','și≤0,06':'și ≤0,06','cu16':'cu 16','și160':'și 160','însumează160':'însumează 160','interval160':'interval 160','Medie2':'Medie 2','pe80':'pe 80','vârf3':'vârf 3','ofertă180':'ofertă 180','mentenanță750':'mentenanță 750','program09':'program 09','infrastructură24':'infrastructură 24','API nou.16':'API nou. 16','Configurator2D':'Configurator 2D','§21.6.12':'§21.6. 12','§17.10':'§17. 10','calendar16':'calendar 16','WBS160':'WBS 160','de11':'de 11','temă:160':'temă: 160'}.items():s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
print('Matricea a fost aliniată domeniului de temă')
