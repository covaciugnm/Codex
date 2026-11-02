# Fara titlu

ID: `01a168de-a466-7f60-84c0-a9b6e60b148d`  
Proiect: iDempiere  
Export UTC: 2026-11-02T15:26:35.221418+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Verificare read-only terminată. **Niciunul dintre cele 8 taskuri nu poate fi anulat integral numai pe baza funcțiilor native.** Majoritatea specifică deja reutilizarea lor; trebuie delimitată integrarea EVA de motorul existent.

Toate referințele de mai jos sunt în `C:\Users\User\AppData\Local\Temp\idempiere13-c03-audit\org.adempiere.base\src\org\compiere\model\`.

| Task | Ce există nativ, cu dovezi | Recomandare și limite |
|---|---|---|
| **T323 – locatori** | `MLocator.java:145–178`: locator pe depozit, coordonate X/Y/Z și tip; `:279`: prioritate; `:353–357`: coordonate. | **Păstrat ca integrare UI EVA.** Documentul cere explicit eliminarea selecției implicite în 7 locuri EVA și filtru stoc pe locator. Existența nativă nu rezolvă aceste ecrane. Nu reconstruiți modelul de locatori. Numărul 7 trebuie reverificat în codul EVA actual. |
| **T329 – loturi și cost** | `MAttributeSetInstance.java:315–333`: asociere lot și produs. `MCost.java:1973–1985`: nivelul Batch/Lot păstrează ASI; nivelurile Client/Organization îl anulează. | **Modificat în configurare, expunere și propagare ASI pe toate documentele EVA.** Urmărirea lotului nu înseamnă automat CMP pe lot. Cerința exemplului 607=48 necesită nivel/metodă de cost și probe contabile. `MCost.java:2006–2008`: Batch/Lot fără ASI duce la omiterea procesării costului. |
| **T330 – FEFO** | `MStorageOnHand.java:464–474`: filtrare termen și sortare după GuaranteeDate când configurarea o cere. | **Motorul nu se rescrie.** Rămân introducerea termenelor, configurare, adaptarea fluxurilor și raportul. **Capcană:** `:470` ordonează întâi `l.PriorityNo DESC`, apoi termenul; `:471–474` depinde și de FIFO. `:466` admite termen NULL. Ramura cu ASI fix `:427–440` nu aplică filtrul termenului. Promisiunea „întotdeauna lotul care expiră primul” trebuie condiționată de locatori/priorități, FIFO și selecția ASI. |
| **T337 – confirmare pick** | `MInOut.java:1160–1211`: creează confirmările după tipul documentului; `:1633–1635`: ține livrarea InProgress cât există confirmări relevante deschise; `:2185–2196`: verificarea. `MInOutLineConfirm.java:147–153`: cantitatea confirmată devine MovementQty și PickedQty. | **Păstrat pentru orchestrarea valului EVA în două faze și reluarea facturării.** Documentele și blocarea sunt native. **Corectați formularea despre lipsuri:** `MInOutConfirm.java:418–428` face split doar dacă există dispută și tipul documentului este configurat pentru split; `:611–620` nota de credit se aplică unui caz de recepție furnizor legată, iar `:637–653` inventarul de diferență se creează pentru ScrappedQty. O simplă lipsă la pick nu înseamnă automat inventar de diferență. |
| **T354 – seturi BOM** | `MOrder.java:1873–1935`, apel `:1654`: explodează BOM ne-stocat. Condiții `:1878`: IsBOM, IsVerified, IsStocked=N; BOM implicit `:1897`. | **Candidat la reducere mare, nu anulare automată.** `:1905` multiplică componentele; `:1908` le setează prețurile; `:1913–1918` transformă setul în comentariu cu preț zero. Trebuie verificat că prețul comercial al setului, factura și importul EVA rămân corecte și că fluxul trece prin prepareIt. Scăderea stocului are loc la livrare, nu la simpla introducere a vânzării. |
| **T315 – retururi** | `MRMA.java:46`: document nativ RMA; `MInOut.java:3249–3252`: linie recepție/livrare din RMA; `MInvoice.java:1068–1074`: note de credit AR/AP native. | **Reformulat ca integrare retururi externe → documente native**, alegerea gestiunii retur, legarea rambursului și blocarea explicită a scrierilor către platforme cerută de D-15. Nu implementați documente contabile paralele. Existența modelelor nu dovedește automat fluxul integrat EVA. |
| **T316 – B2B** | `MBPartner.java:923–929`: lista de prețuri partener sau fallback pe grup; `I_C_BP_Group.java:200–211`: discount pe grup; `I_C_BPartner.java:216–227,820–831`: termen de plată și limită de credit pe partener. | **Păstrat pentru canal ↔ grupe, unicitatea apartenenței și aplicarea politicii canalului la comenzi.** Nu confundați creditul pe partener cu o limită agregată pe canal; aceasta trebuie definită separat. Site-ul canalului nu rezultă din existența listelor de prețuri. |
| **T353 – traduceri** | `MAcctSchemaElement.java:186`: join nativ `M_Product_Trl` pe produs și `AD_Language`. | **Reutilizare traduceri comune, extensie numai pentru diferențele pe canal.** Dimensiunea canal, traducerea automată ca propunere confirmată și publicarea API rămân cerințe suplimentare. Dovada citată confirmă traducerea pe limbă, nu implementarea integrală a cerinței. |

Precizare pentru raport: acestea sunt dovezi din **upstream release-13**, nu dovadă că exact aceste versiuni și configurări rulează pe `acc.eva-org.com`. Nu prezentați capabilitatea nativă drept validare de producție.

## Asistent

Verificarea nu a identificat omisiuni de taskuri: **38 în surse și 38 în raport**, fără ID-uri lipsă sau suplimentare. Delimitarea dintre codul existent și funcționalitatea validată în producție este corectă.

O corecție de trasabilitate:

- **T329:** afirmația „EVA are deja integrarea seriilor” citează `[E10, N2]`. E10 documentează TipGestiune/MotorStraturi, iar N2 documentează capacitatea nativă. Adăugați dovada concretă din codul EVA pentru seriile T162/SeriiArticole sau atribuiți afirmația documentației D2.

Concluziile native verificate anterior sunt redate corect, inclusiv limitele BOM, prioritățile FEFO, confirmările de pick și costul pe lot. Nu am identificat alte probleme factuale în domeniul verificat independent.

## Asistent

Materialul corectat este pregătit pentru verdictul independent:

- Analiză: `Analiza_C03_C10_reutilizare_2026-10-23.html`
- Jurnal: `Jurnal_corectii_autoverificare_C03_C10_2026-10-23.html`
- Export: `Checklist_C03_C10_stare_implementator_2026-10-23.json`
- Control: `Verificare_structurala_C03_C10_2026-10-23.json`

Toate sunt în folderul utilizatorului. Originalele exacte sunt păstrate în `Versiuni/2026-10-23_inainte_corectii_EE1C064F/`.

**Autoverificare: 117/119** — 55 corecții, 54 fișe și 8 condiții finale. C-03/C-08 așteaptă auditorul. Zero erori structurale; linkul auditului final devine disponibil când auditorul salvează documentul.

SHA256 analiză stabilă:
`A969984175349E2A3CE44D0BA608C3D2285CF82C616CCB61BA6711A8DCF84A41`

Nu am modificat ERP-ul, registrul sau producția și nu am publicat pe GitHub.
