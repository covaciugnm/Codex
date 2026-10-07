# Plan de măsuri — export observabil, după auditul r02

24.09.2026. Responsabil P-SYSTEMS, integrare P-MANAGER; verificare independentă A-SYSTEMS + A-GOVERNANCE, apoi A-QAMANAGER. Produs r02 înghețat; corecții exclusiv staging r03 până la conservarea auditului r02.

## Constatări și rezultate cerute

| ID original | Cauză demonstrată | Acțiune | Rezultat verificabil |
|---|---|---|---|
| SYS-A-SYSTEMS-r02-F05 | Se adaugă LF inexistent dacă sursa nu are terminator. | Calcul exclusiv pe prefix real complet; fără normalizare ascunsă. | Pentru orice captură acceptată, lungimea prefixului nu depășește sursa și hashul este al sursei[:lungime]. |
| SYS-A-SYSTEMS-r02-F06 | Numele rolului și părinții destinației pot redirecționa scrierea. | Nume sigure și unice; verificare confinare, coliziuni și reparse/symlink înaintea scrierii. | Caz normal acceptat; traversări/aliasuri/coliziuni refuzate, fără scrieri exterioare sau captură aparent încheiată. |

## Livrabile și teste

Versiuni noi ale exportatorului, suitei de teste și instrucțiunilor; raport de rezultate cu comanda executată, mediul, numărul real de teste și orice omisiune. Cele 17 teste inițiale se păstrează. F05: sursă goală, record fără LF, primă linie parțială, LF, CRLF, coadă incompletă. F06: configurație validă, rol-cale relativ/absolut, duplicat/alias/rezervat/coliziune index, symlink/junction pe părinți, rundă existentă. Se verifică și menținerea excluderii mesajelor ascunse și a nemodificării surselor.

Date exclusiv sintetice în directoare temporare izolate și validate. Nu se testează evadări asupra datelor beneficiarului. Configurația reală și capturile existente nu sunt declarate compromise: auditorul a verificat prefixele reale conforme. Un test trecut nu închide findingul fără retestul auditorului.

## Secvență și acceptare

1. P-SYSTEMS depune r03 în 06_REGISTRU/r03_staging și declară probele.
2. Main păstrează rapoartele/metaauditul/rezultatul r02 și arhiva nouă, fără rescriere.
3. Main integrează numai fișierele corectate, fixează contract SYS r03 și reface contractele dependente.
4. Auditorii reexecută testele de închidere și regresiile relevante pe bytes integrați; fiecare criteriu trebuie să depășească 950/1000, fără finding deschis.
5. QA verifică rapoartele. Validatorul decide trecerea cumulativă; arhivarea include și orice nou RETURN.

Stare la emitere: PLAN ÎN EXECUȚIE, nu rezultat și nu aprobare. Probe originale: 05_AUDIT/SYS-001/A-SYSTEMS-r02.md/.json și A-SYSTEMS-r02-tests.txt; mandat exact în 06_REGISTRU/PROMPTURI/P-SYSTEMS-remediere-r03.md.
