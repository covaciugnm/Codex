# Reluarea verificabilă a proiectului

## Ordinea obligatorie

1. Citește STATUS.json și ultimul raport de audit. Starea de pe disc are prioritate față de o amintire din chat.
2. Rulează `node tools/manage.cjs verify` dacă există manifest. Un manifest absent indică un checkpoint de lucru, nu o livrare finală verificată.
3. Citește tasks, requirements și experiments. Identifică sarcinile in_progress, in_review, rework și blocked înainte de a începe una nouă.
4. Pentru fiecare sarcină activă citește ultimul eveniment al autorului, artefactele și input hashes. Verifică dacă rezultatul a fost confirmat ori doar început.
5. Cere verificarea unui alt agent pentru stările ambigue. Nu presupune că un fișier temporar este rezultat acceptat.
6. Înregistrează evenimentul resumed cu noul attempt și planul concret. Reia prima etapă fără dovadă, păstrând etapele confirmate.

## Mașina de stări a sarcinii

planned → ready → in_progress → in_review → accepted. Dacă auditul găsește probleme, in_review → rework → in_progress. Lipsa unei intrări necesare produce blocked cu motiv și condiție de deblocare. O sarcină abandoned păstrează motivul, rezultatele și dependențele afectate; nu dispare din registru.

Managerul schimbă starea comună numai după dovadă. Autorul scrie rezultatul, auditorul verdictul, managerul închide sarcina. Cine execută roluri multiple trebuie să păstreze independența auditului prin alt agent.

## Checkpointul minim

Un checkpoint conține task_id, attempt, timestamp UTC, actor, eveniment, artefacte, hashuri sau referința la manifest, verificări rulate, constatări și următoarea acțiune. Pentru sesiunea de redactare, jurnalele JSONL ale agenților sunt independente și pot avea câmpuri echivalente. Pentru implementare se folosește schema de evenimente din contracte și instrumentul manage.

Evenimentele se adaugă imediat după schimbări semnificative: alocare, început, rezultat, test, constatare, remediere, re-audit și livrare. Heartbeatul unui job lung se poate scrie la 5 minute. Timestampul consemnează momentul înregistrării, nu se antedatează pentru a părea „în timp real”. Prima inițializare și unele jurnale de agent nu au hashchain; această diferență este verificabilă și nu este ascunsă.

## Comenzi disponibile

Din rădăcina acestui dosar, cu Node.js disponibil:

```text
node tools/manage.cjs event manager W00 started "Inventar hardware început"
node tools/manage.cjs event-json checkpoint-input.json
node tools/manage.cjs validate
node tools/manage.cjs build
node tools/manage.cjs manifest
node tools/manage.cjs verify
```

`event` adaugă o linie fără să schimbe tasks sau STATUS. Managerul actualizează aceste registre separat prin scriere atomică și verificare. `validate` scrie un raport nou, deci invalidează un manifest anterior; `build` regenerează livrabilele. Ordinea finală este editări → audit → build → validare → manifest → verify → copiere → verificare destinație. Orice log adăugat după manifest cere regenerarea lui.

`event` este jurnalul sumar. Pentru un checkpoint complet, `event-json` citește un fișier cu actor, task, event, result, artifacts, next, attempt pozitiv, input_hashes și checks. Instrumentul adaugă ID, timp și legătura hash. Hashurile intrărilor și rezultatele testelor trebuie furnizate din verificări reale; instrumentul nu le inventează. În validare, acceptarea unei sarcini cere raport și dovezi existente, iar o sarcină W cere experimente trecute cu rezultat. Validarea structurală nu confirmă singură adevărul unui rezultat.

`artifacts` și `checks` sunt liste de șiruri nevidate; fiecare check descrie verificarea și rezultatul observat. `input_hashes` mapează căi sau identificatori la șiruri SHA-256 de64caractere hexazecimale. Forma este verificată; operatorul rămâne responsabil pentru asocierea cu fișierul real. Jurnalele istorice fără schema_version1.1 sunt păstrate ca atare, cu câmpurile echivalente și identitatea autorului din numele jurnalului/raport.

Fiecare fișier de jurnal are un singur scriitor activ. manage.cjs nu implementează blocare distribuită: doi producători nu pot folosi simultan același actor. Pentru paralelism se folosesc jurnale distincte și managerul integrează checkpointurile. Hashchainul verifică succesiunea locală; nu este semnătură digitală sau garanție antifraudă.

`create-registers.cjs` este generatorul istoric inițial și refuză registre existente. Nu se rulează la reluare. Nu șterge registre pentru a forța reinițializarea. Pentru un plan nou se creează o revizie cu istoric, nu se suprascrie istoria.

Scripturile `remediate-*.cjs` sunt evidența transformărilor acestei redactări și nu se rerulează la reluare. Unele ar putea suprascrie câmpuri actualizate ulterior. Comenzile curente permise de protocol sunt cele din manage.cjs; orice migrare nouă se revizuiește înainte de aplicare.

## Trei scenarii de reluare

Întrerupere în redactare: păstrează ultimul fișier complet și identifică secțiunea nesalvată din jurnal; sarcina rămâne in_progress. Întrerupere după rezultat dar înainte de audit: verifică fișierul și cere audit, fără refacerea automată a întregului conținut. Întrerupere după audit dar înainte de copiere: verifică verdictul și manifestul local, apoi livrează și compară hashurile.

Pentru implementare se adaugă stările tranzacționale din capitolul date. Modul live nu recuperează mediul după terminarea procesului. Stările interne opace ale frameworkurilor Apple se refac numai în măsura permisă de API; poate fi necesară recaptură. Nu promitem reluarea exactă a muncii încă nesalvate.

## Blocaje și reluarea pe alt calculator

Păstrează versiunile instrumentelor și căile relative în dosar. Calea de instalare Node nu face parte din contract. Dacă un fișier lipsește ori hashul diferă, deschide constatare, identifică o copie confirmată și compară înainte de reparare. Nu șterge automat diferențele: pot fi lucru nou legitim.

Copierea pe partajarea de rețea poate fi întreruptă și nu este atomică pentru întregul dosar. Numai LIVRARE_CONFIRMATA.json împreună cu verificarea manifestului confirmă o copie completă a versiunii. În lipsa lor, se poate relua din checkpointurile individuale, cu audit al fișierelor necesare.
