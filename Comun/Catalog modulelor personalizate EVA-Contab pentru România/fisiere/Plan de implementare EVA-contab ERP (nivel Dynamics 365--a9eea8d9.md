# Plan de implementare EVA-contab ERP — nivel comparabil cu MS Dynamics 365 Business Central

**Obiectiv strategic:** transformarea EVA-contab (iDempiere 13) dintr-un ERP open-source generic într-un **sistem ERP complet, localizat 100% pentru România**, comparabil ca acoperire funcțională cu **Microsoft Dynamics 365 Business Central** — capabil să înlocuiască SAGA și soluțiile SMB comerciale.

**Parametri asumați (conform deciziei):**
- **Nivel-țintă:** SMB / Business Central (ERP complet pentru firmă mică-mijlocie + conformitate fiscală RO integrală). *Nu* nivelul Finance & Operations (enterprise, multi-țară, producție grea) — acela e o extensie ulterioară.
- **Echipă:** mare (20+ persoane / mai mulți parteneri) → **6 echipe (squad-uri) paralele** + guild-uri transversale. Termenele presupun această capacitate; cu echipă mai mică se prelungesc proporțional.
- **Orizont:** ~**36 luni** până la paritate BC, cu **MVP de înlocuire SAGA la ~luna 10–12**.

> **Bază de pornire:** acest plan folosește direct „Catalogul de module și surse open-source" (fișierul companion) — fiecare pas indică sursa de portare concretă.

---

## 0. Încadrare realistă (de citit înainte de plan)

Dynamics 365 s-a construit în **mii de ani-om**. „Paritate" nu înseamnă a reproduce fiecare funcție, ci a **acoperi ≥90% din scenariile reale ale unei firme SMB românești** mai bine decât alternativele locale, cu conformitate fiscală **superioară** (avantajul nostru: control total pe legislația RO). Strategia:
1. **Livrare de valoare devreme** — un MVP care înlocuiește SAGA (finanțe + conformitate ANAF + salarizare) la luna ~10–12, nu la final.
2. **Nu reinventăm nucleul** — iDempiere are deja GL, AP/AR, stocuri, achiziții, vânzări, MRP (Libero), POS, mijloace fixe, workflow, REST API, Jasper. **Golul față de Dynamics e**: localizarea RO (tot), UX modern, AI/Copilot, SaaS multi-tenant, mobil, WMS avansat, BI șlefuit.
3. **Localizare ca overlay** (pattern LCO), cu parametri legislativi versionați pe perioade de valabilitate — niciodată hardcodat.
4. **SAGA = oracol de validare** în fazele 1–2 (comparație stat de salarii, D112, balanță, declarații — diferență țintă 0).

---

## 0.1 Matricea de paritate funcțională (BC → iDempiere azi → țintă EVA)

| Capabilitate Business Central | iDempiere azi | Gol de acoperit | Wave / Squad |
|---|---|---|---|
| Financial Management (GL, buget, cash flow, consolidare, multivalută) | Puternic (GL, buget, multivalută) | Consolidare, cockpit cash flow, plan conturi RO | W1 / Finanțe |
| Conformitate fiscală RO (e-Factura, SAF-T, D112, D300/390/394, REGES, e-Transport) | **Inexistent** | **Totul** (avantajul competitiv) | W1–W2 / Fiscal |
| Sales & Receivables (O2C) | Puternic | e-Factura B2C, UX, credit mgmt | W2 / Vânzări |
| Purchasing & Payables (P2P) | Puternic | Aprobări, OCR facturi furnizor | W2 / SCM |
| Inventory (loturi, serii, valorizare) | Bun | Gestiune cantitativ-valorică RO, NIR | W2 / SCM |
| Warehouse Management (WMS) | De bază | Locații, pick/pack, coduri de bare, mobil | W3 / SCM |
| Manufacturing / MRP | Libero (bun) | Costuri, planificare, UX | W3 / SCM |
| Project Mgmt / Jobs | De bază | Bugete proiect, pontaj pe proiect | W3 / SCM |
| Fixed Assets | Da (nucleu) | Amortizare fiscală RO, reevaluare | W1 / Finanțe |
| HR & Payroll RO | **Inexistent** | **Tot** (CDSoftware/AMERPSOFT + RO) | W1 / HR |
| SSM / ISU RO | **Inexistent** | **Tot** (greenfield) | W3 / HR |
| CRM / Relationship (Dynamics Sales) | De bază | Pipeline, oportunități, portal | W2–W3 / Vânzări |
| POS / Retail (Commerce) | POS de bază | Casă fiscală RO (AMEF), retail | W3 / Vânzări |
| BI / Reporting (Power BI) | Jasper | Dashboards pe roluri, warehouse semantic | W3 / BI-AI |
| AI / Copilot | **Inexistent** | Asistent NL, OCR, anomalii | W4 / BI-AI |
| Platformă / API / integrare (Power Platform) | REST API bun | Connectors, EDI, webhooks, low-code | W4 / Platformă |
| Cloud / SaaS multi-tenant | Self-host | Multi-tenant, K8s, billing | W4 / Platformă |
| Mobil | Slab | Aplicații mobile (aprobări, pontaj, depozit, vânzări) | W4 / Platformă |
| Role Centers / UX modern | ZK clasic | Temă modernă, role centers, personalizare | W5 / UX |
| Securitate / GDPR / SSO | RBAC de bază | SSO Azure/OIDC, GDPR, audit, pen-test | W4 / Platformă |
| Migrare / onboarding / ecosistem | — | Unelte migrare SAGA/BC, marketplace, training | W5 / GTM |

**Definiția „paritate atinsă":** scor ≥ **90%** pe această matrice (ponderat pe utilizare reală) + ≥ **N clienți pilot în producție**.

---

## 0.2 Structura echipei (20+) — 6 squad-uri + guild-uri

| Squad | Focus | Componență orientativă |
|---|---|---|
| **S0 Platform & DevOps** | Build, CI/CD, cloud, securitate, API, mobil | 4–5 (2 dev platformă, 1 DevOps, 1 securitate, 1 mobil) |
| **S1 Finanțe & Fiscal** | GL, plan conturi RO, TVA, e-Factura, SAF-T, declarații | 5–6 (3 dev + 1 expert contabil, 1 expert fiscal, 1 QA) |
| **S2 HR & Salarizare & SSM** | Salarizare RO, D112, REGES, pontaj, SSM/ISU | 4–5 (2–3 dev + 1 expert salarizare/HR RO, 1 QA) |
| **S3 SCM & Producție** | Stocuri, achiziții, WMS, MRP, proiecte | 3–4 |
| **S4 Vânzări, CRM & POS** | O2C, CRM, POS fiscal, portal/webstore | 3–4 |
| **S5 BI, AI & UX** | Dashboards, Copilot, role centers, UX | 3–4 |
| **Guild-uri transversale** | Arhitectură, QA/automatizare, Securitate/GDPR, Product/PM, Documentație | rotativ din squad-uri |

Cadență: sprint-uri 2 săptămâni, demo la fiecare sprint, release train lunar, gate de fază (quality gate) la fiecare milestone.

---

## 0.3 KPI globale de program

- **Acoperire paritate BC:** % din matricea 0.1 (țintă 90% la M36).
- **Conformitate fiscală:** % declarații RO generate + validate DUKIntegrator (țintă 100% la M18).
- **Acuratețe vs. SAGA:** diferență la stat salarii / balanță / D112 pe set de test (țintă **0**).
- **Calitate cod:** coverage teste ≥ 70% pe modulele EVA; 0 vulnerabilități critice.
- **Adopție:** nr. clienți pilot în producție; NPS; timp mediu de onboarding.
- **Performanță:** timp închidere lună; timp emitere+transmitere e-Factura; disponibilitate SaaS ≥ 99,5%.

---

# Planul pe faze (Waves) — obiective, sub-pași, rezultate măsurabile

> Waves se suprapun (echipă mare). Fiecare wave listează sub-pași cu **Activități** și **Rezultate măsurabile (RM)**.

---

## WAVE 0 — Fundație tehnică & guvernanță · M0–M3 · Squad S0 (+toate)

**Obiectiv:** mediu de dezvoltare industrial, arhitectură de plugin-uri EVA, pipeline CI/CD, standarde — astfel încât 6 squad-uri să livreze paralel fără a se bloca.

| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **0.1 Infrastructură dev** | iDempiere 13 base + PostgreSQL; repo Git (mono/multi-repo `eva.*`); build Maven/Tycho; update-site P2 | Build reproductibil < 15 min; mediu identic pe 3 dev; 1 plugin „hello EVA" instalat pe v13 |
| **0.2 CI/CD & calitate** | Pipeline build+test+package; SonarQube; teste automate; artefacte versionate | Pipeline verde la fiecare push; quality gate configurat; coverage baseline raportat |
| **0.3 Arhitectura EVA** | Namespace-uri (`eva.hr.*`, `eva.ro.*`, `eva.fin.*`…), grafic de dependențe, overlay LCO_RO, ADR-uri | Document de arhitectură + 20+ ADR; schema de dependențe aprobată |
| **0.4 Cadru parametri legislativi** | Model „parametru cu perioadă de valabilitate" (cote, praguri, salariu minim) | Motor de parametri testat; import cote 2024–2026; 0 valori hardcodate |
| **0.5 Mediu de testare & date** | Set date demo RO; instanță SAGA de referință; date de comparație | Set de test versionat; harness de comparație EVA↔SAGA funcțional |
| **0.6 Guvernanță** | Backlog, Definition of Done, politică licențiere (GPLv2/Apache/AGPL), roluri | Backlog priorizat; DoD aprobat; registru licențe pe fiecare dependență |

**Gate M3:** infrastructură + arhitectură + un plugin demo pe v13; toate squad-urile pot începe paralel.

---

## WAVE 1 — Nucleul „înlocuire SAGA": Finanțe RO + e-Factura + HR/Salarizare · M2–M12 · Squad S1 + S2

**Obiectiv:** contabilitate RO completă + prima conformitate ANAF (e-Factura, TVA) + salarizare RO + D112 + REGES → **MVP care poate ține contabilitatea și salariile unei firme reale**.

### 1A. Finanțe & Fiscal de bază (S1)
| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **1A.1 Plan de conturi & nomenclatoare RO** | 2Pack cu plan conturi OMFP 1802; CAEN; județe/localități; bănci; TVA; cursuri BNR automat | Plan de conturi RO instalabil; curs BNR importat zilnic; nomenclatoare complete |
| **1A.2 Validări RO (overlay LCO)** | Cifra de control CUI/CIF, CNP, IBAN pe interfața `ILCO_TaxIDDigit` | Validare 100% pe set de test de CUI/CNP; respinge input invalid |
| **1A.3 Motor TVA RO** | TVA la încasare, TVA nedeductibil, taxare inversă, pro-rata | Calcul TVA = SAGA pe 200 facturi de test (diferență 0) |
| **1A.4 e-Factura CIUS-RO** | Generare UBL 2.1 (**ph-ubl**), validare (**phive-rules-cius-ro**), OAuth2 SPV, upload/status/download, XML→PDF | Factură **acceptată în SPV sandbox + prod**; validare RO_CIUS trece; PDF generat |
| **1A.5 Jurnale & registre + D300/D390/D394** | Registru jurnal, carte mare, balanță, jurnale TVA; generatoare declarații (ref. `declaratii-anaf`) | Balanță = SAGA (diferență 0); D300/D394 **validate DUKIntegrator** |
| **1A.6 Bancă & plăți** | Import extrase CAMT053/MT940 (**BX Service**), reconciliere, plăți SEPA, fișiere bancare RO | Import extras + reconciliere ≥ 95% automat; fișier plăți acceptat de bancă |
| **1A.7 Mijloace fixe RO** | Amortizare fiscală + contabilă RO, reevaluare, registru mijloace fixe | Amortizare = SAGA pe set de test; registru mijloace fixe generat |

### 1B. HR & Salarizare RO (S2)
| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **1B.1 Model HR** (portare) | Dosar salariat, contracte, acte adiționale, structură org. (din **CDSoftware**/**AMERPSOFT**) | CRUD salariat/contract funcțional; import 500 salariați de test |
| **1B.2 Pontaj & concedii** | Terminale (Hikvision), ture, concedii, aprobări (din **CDSoftware Attendance**) | Import pontaj din terminal; ture rotative; flux aprobare concediu |
| **1B.3 Motor salarial RO** | CAS 25%, CASS 10%, CAM 2,25%, impozit 10%, deduceri, net↔brut (motor **adempiere-payroll-multi-engine** + formule **AMERPSOFT** + param. legislativi; formule ref. **PFASimplu**) | **Stat de salarii = SAGA pe set de test (diferență 0 lei)**; net↔brut validat vs. calculatoare web |
| **1B.4 Concedii medicale RO** | Calcul indemnizații (OUG 158), FNUASS, recuperări | Calcul concedii medicale = SAGA pe cazuri de test |
| **1B.5 D112** | Generare XML + validare DUKIntegrator + rectificative + recipise | **D112 validat DUKIntegrator**; rectificativă funcțională |
| **1B.6 REGES-ONLINE** | Transmitere contracte/modificări (schema **reges.xsd**, `reges-ro/integrare`) | Contract **transmis în REGES sandbox**; confirmare primită |
| **1B.7 Ieșiri salariale** | Fluturași, note contabile salariale, fișiere bancare, D205 | Fluturași generați; note contabile în GL; D205 generat |

**Gate M12 (MVP „SAGA replacement"):** o firmă reală poate ține în EVA contabilitatea + TVA + e-Factura + salariile + D112 + REGES, cu rezultate **identice cu SAGA** pe setul de validare.

---

## WAVE 2 — Fiscalitate avansată + Lanț valoric (O2C / P2P / Stocuri) · M9–M20 · Squad S1, S3, S4

**Obiectiv:** conformitate ANAF **integrală** (SAF-T, e-Transport, toate declarațiile) + fluxurile comerciale complete.

### 2A. Fiscalitate avansată (S1)
| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **2A.1 SAF-T D406** | Generator XML din XSD ANAF (greenfield; pattern export **DATEV metasfresh**) — nomenclatoare, conturi, parteneri, stocuri, active; validare DUKIntegrator | **D406 generat + validat** pe firmă reală; toate secțiunile obligatorii |
| **2A.2 e-Transport (UIT)** | Client API ANAF (ref. **e-factura-go**/**anafpy**) | **UIT emis** în sandbox+prod; anulare/modificare vehicul |
| **2A.3 Restul declarațiilor** | D100, D101, D390 (VIES), Intrastat, D700 | Toate generabile + validate DUKIntegrator |
| **2A.4 Modul transmitere unificat** | Certificate digitale, DUKIntegrator, recipise, arhivă, audit trail | Transmitere end-to-end + arhivă căutabilă; audit trail complet |

### 2B. Order-to-Cash & CRM light (S4)
| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **2B.1 Ciclu vânzări** | Ofertă→comandă→livrare→factură→încasare; e-Factura B2C automat | Ciclu O2C complet end-to-end; e-Factura B2C trimisă la SPV |
| **2B.2 Credit & clienți** | Limite de credit, blocaje, scadențar, penalități | Blocaj automat la depășire credit; scadențar corect |
| **2B.3 CRM pipeline** | Lead→oportunitate→ofertă; activități, pipeline | Pipeline vizual; conversie lead→comandă urmăribilă |

### 2C. Procure-to-Pay & Stocuri (S3)
| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **2C.1 Ciclu achiziții** | Cerere→comandă→recepție(NIR)→factură; fluxuri de aprobare | Ciclu P2P complet cu aprobări multi-nivel |
| **2C.2 Gestiune cantitativ-valorică RO** | Metode valorizare (FIFO/CMP), loturi, serii, NIR, bon consum | Gestiune = SAGA pe mișcări de test; NIR generat |
| **2C.3 OCR facturi furnizor** | Import + OCR + potrivire cu comanda (integrare AI din W4) | ≥ 80% facturi furnizor procesate semi-automat |

**Gate M20:** conformitate ANAF 100% (toate declarațiile) + fluxurile comerciale complete pe firmă pilot.

---

## WAVE 3 — WMS, Producție, POS/Retail, SSM/ISU, BI · M15–M26 · Squad S3, S4, S5, S2

**Obiectiv:** paritate operațională SMB + primele dashboards + zona SSM (diferențiator RO).

| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **3.1 WMS (S3)** | Locații, pick/pack, coduri de bare, inventariere, mobil depozit | Scanare mobilă funcțională; acuratețe inventar ≥ 99% |
| **3.2 Producție/MRP (S3)** | Libero Manufacturing + calcul cost, planificare, BOM/rute | Ordin de producție cu cost calculat; MRP generează necesar |
| **3.3 Proiecte (S3)** | Bugete proiect, pontaj pe proiect, facturare pe proiect | Proiect cu buget vs. realizat; facturare pe proiect |
| **3.4 POS/Retail fiscal RO (S4)** | POS + integrare casă de marcat fiscală RO (AMEF), bon fiscal | Tranzacție POS cu **bon fiscal RO** emis; raport Z |
| **3.5 Portal client/webstore (S4)** | Self-service, comenzi online, e-Factura | Client plasează comandă online → factură automată |
| **3.6 SSM/ISU RO (S2)** | Fișe instruire individuală, tematici, periodicități, medicina muncii, EPP, registre SSM, evidențe ISU/PSI (greenfield; model din **OCA/management-system**) | Fișă de instruire generată; alertă expirare instruire/aptitudine; registru SSM |
| **3.7 BI & dashboards (S5)** | Data warehouse semantic; dashboards pe roluri (CFO/HR/ops); Jasper + Metabase + SearchIndex | ≥ 15 dashboards live; drill-down funcțional; export |

**Gate M26:** ERP operațional complet SMB (finanțe+fiscal+HR+SCM+producție+vânzări+POS+SSM+BI) pe ≥ 3 firme pilot.

---

## WAVE 4 — AI/Copilot, Platformă, Cloud/SaaS, Mobil, Securitate/GDPR · M20–M32 · Squad S0, S5

**Obiectiv:** nivelul „modern cloud ERP" — AI, SaaS multi-tenant, mobil, securitate enterprise.

| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **4.1 AI Copilot (S5)** | Asistent limbaj natural (ref. **idempiere-mcp** + LLM); OCR facturi; detecție anomalii; sugestii contabile | Asistent răspunde la ≥ 20 intenții reale; OCR acuratețe ≥ 90%; anomalii detectate |
| **4.2 Automatizări/workflow (S5)** | Aprobări, alerte, reguli, RPA fiscal (depunere automată) | Flux de aprobare configurabil no-code; depunere automată declarații |
| **4.3 Cloud/SaaS multi-tenant (S0)** | Docker/Kubernetes, izolare tenant, provisioning, billing | Instanță multi-tenant; onboarding tenant nou < 1h; billing per tenant |
| **4.4 Aplicații mobile (S0)** | Aprobări, pontaj, vânzări teren, depozit | App mobil publicat (Android/iOS); 4 fluxuri cheie |
| **4.5 Securitate & SSO (S0)** | SSO Azure/OIDC, RBAC fin, criptare, audit, **pen-test** | SSO funcțional; **audit de securitate trecut**; 0 vulnerabilități critice |
| **4.6 GDPR (S0)** | Consimțământ, retenție, drept la ștergere, DPIA, jurnal acces | Registru prelucrări; export/ștergere date la cerere; DPIA aprobată |
| **4.7 Integrare/API (S0)** | Connectors (bănci, curieri, marketplace), EDI, webhooks | ≥ 5 connectors live; webhooks funcționale; EDI testat |

**Gate M32:** EVA rulează ca **SaaS multi-tenant** securizat, cu AI Copilot și aplicații mobile.

---

## WAVE 5 — UX modern, Paritate, Migrare, Ecosistem, Go-to-market · M27–M36 · Squad S5 + GTM

**Obiectiv:** experiență și ecosistem comparabile cu Dynamics + trecerea piloților în producție.

| Sub-pas | Activități | Rezultate măsurabile |
|---|---|---|
| **5.1 UX modern & Role Centers** | Temă modernă, role centers pe funcție, personalizare, onboarding în-app | Role center pentru ≥ 6 roluri; scor SUS usability ≥ 75 |
| **5.2 Unelte de migrare** | Migratoare din SAGA / Dynamics / Excel; validare | Migrare firmă SAGA în < 1 zi, cu reconciliere automată |
| **5.3 Documentație & training** | Manuale, cursuri, certificare, KB, video | Bibliotecă docs completă; program de certificare lansat |
| **5.4 Ecosistem / marketplace** | Repo de extensii (ref. `idempiere-extension-repository`), SDK parteneri | Marketplace intern cu ≥ 10 extensii; SDK publicat |
| **5.5 Benchmark paritate & pilot→prod** | Măsurare scor matrice 0.1; trecere piloți în producție | **Scor paritate ≥ 90%**; ≥ N clienți în producție; NPS măsurat |

**Gate M36 (final):** EVA-contab = ERP SMB complet, localizat RO, cloud, comparabil funcțional cu Dynamics 365 Business Central, cu clienți în producție.

---

## Rezumat milestone-uri & criterii de gate

| Milestone | Lună | Criteriu de trecere (măsurabil) |
|---|---|---|
| **M3 — Fundație** | 3 | Build < 15 min; arhitectură + ADR; plugin demo pe v13; squad-uri deblocate |
| **M12 — MVP SAGA replacement** | 12 | Contabilitate+TVA+e-Factura+salarii+D112+REGES = SAGA (diferență 0) pe firmă reală |
| **M20 — Conformitate + comercial** | 20 | 100% declarații ANAF validate DUKIntegrator; O2C+P2P+stocuri complete |
| **M26 — ERP operațional complet** | 26 | Toate modulele SMB + SSM + BI pe ≥ 3 piloți |
| **M32 — Cloud/AI/Mobil** | 32 | SaaS multi-tenant + Copilot + mobil + audit securitate trecut |
| **M36 — Paritate BC** | 36 | Scor paritate ≥ 90%; clienți în producție; NPS măsurat |

---

## Registru de riscuri (principale)

| Risc | Impact | Mitigare |
|---|---|---|
| **Schimbări legislative frecvente** (cote, declarații, e-Factura) | Ridicat | Parametri versionați + echipă fiscal dedicată + DUKIntegrator ca validator oficial |
| **SAF-T D406 fără bază open-source** (greenfield) | Ridicat | Start devreme din XSD ANAF; buffer de timp; pattern DATEV metasfresh |
| **Licențiere AGPL** (OCA l10n-romania, declaratii-anaf) | Mediu | Tratate ca *specificație*, nu copy-paste; alternative permisive (ph-ubl/phive Apache) |
| **Portare pe iDempiere 13** a modulelor testate pe v10–12 | Mediu | Faza 0 validează portarea; teste de regresie |
| **Dependență de furnizori externi** (AMEF/casă fiscală, bănci, ANAF API) | Mediu | Simulator ANAF (`anaf-api-simulator`); abstractizare integrări |
| **Complexitate coordonare 6 squad-uri** | Mediu | Guild de arhitectură, release train lunar, contracte de interfață între module |
| **Adopție / schimbare de la SAGA** | Mediu | Unelte de migrare + piloți + training + comparație paralelă |

---

## Principii de „Definition of Done" (calitate, la fiecare pas)

- Cod cu teste automate (unit + integrare), coverage ≥ 70% pe modul EVA.
- Fiecare funcție fiscală **validată cu DUKIntegrator** și/sau **comparată cu SAGA** (diferență 0).
- Parametri legislativi în cadrul versionat, niciodată hardcodați.
- Documentație de utilizator + release notes.
- Trecere quality gate (SonarQube) + review de securitate pentru zonele sensibile.
- Licența fiecărei dependențe verificată și înregistrată.

---

*Plan generat pe baza „Catalogului de module și surse open-source pentru localizarea RO — EVA-contab" (fișier companion). Termenele presupun echipă de 20+ persoane cu 6 squad-uri paralele; se ajustează proporțional cu resursele.*
