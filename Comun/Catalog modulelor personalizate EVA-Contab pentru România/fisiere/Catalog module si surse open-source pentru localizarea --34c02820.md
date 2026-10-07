# Catalog de module și surse open-source pentru localizarea românească — EVA-contab (iDempiere)

**Scop:** inventar exhaustiv al soluțiilor cu **cod sursă public** din care ne putem inspira, pe care le putem instala/testa sau pe care le putem **porta în Java/iDempiere** pentru EVA-contab — pe zonele Contabilitate / Fiscalitate / Financiar / ERP / HR / Salarizare / Declarații ANAF / e-Factura / e-Transport / SAF-T / REGES / SSM / ISU.

**Domeniu extins (la cererea beneficiarului):** modulele **nu trebuie să fie exclusiv iDempiere**. Orice proiect open-source (orice limbaj) care poate fi sursă de inspirație și portat ulterior în Java/iDempiere este inclus — indiferent cât de mare pare efortul de portare.

**Data cercetării:** ~mijloc 2026. **Versiunea stabilă iDempiere:** 13 „Orion" (lansată 6 martie 2026).

> **Sursa acestui catalog:** analiza celor două documente interne („Module instalabile de HR și declarații.docx" și „…1.docx") + 6 investigații web independente (GitHub API, Bitbucket, Wayback Machine, Odoo Store, Packagist/PyPI/npm/Maven). Elementele neconfirmabile sunt marcate explicit `⚠️`.

---

## 0. Legendă

**Portabilitate spre Java/iDempiere:**
- **ÎNALTĂ** = același model de date `AD_`/`C_`/`M_` (descendență Compiere/ADempiere) → cod aproape direct transferabil, sau bibliotecă Java direct integrabilă în plugin OSGi.
- **MEDIE** = bibliotecă standalone (Java sau alt limbaj) al cărei model/flux se mapează ușor în Java.
- **SCĂZUTĂ** = stack/model diferit → doar referință de arhitectură/logică.

**Mod de instalare (iDempiere):** `P2` = update site Eclipse din consola Plugin Management; `JAR` = drop în consola OSGi/Apache Felix; `SRC` = compilare din sursă (Tycho/Maven).

**Licențe (important pentru reutilizare):**
- `GPLv2` — iDempiere/ADempiere/metasfresh; un plugin derivat moștenește GPL (acceptabil pentru noi).
- `AGPL-3.0` — copyleft puternic (OCA l10n-romania, declaratii-anaf). Se poate **studia** liber; portarea codului direct cere prudență juridică → tratat ca **specificație**, nu copy-paste.
- `Apache-2.0` / `MIT` — permisive, sigure de reutilizat/încorporat.
- ⚠️ **De evitat**: `Konik` (AGPL, e-invoice) — există alternative permisive.

---

## 1. Rezumat executiv (concluzii)

1. **Nu există niciun plugin public complet de localizare RO pentru iDempiere** (nici HR/salarizare RO, nici e-Factura, nici D112, nici SAF-T, nici REGES). Zona românească este, practic, **greenfield**.
2. Pe wiki există un cadru oficial „**Plugin: Localization Romania**" (mentainer **Marco Longo / iDempiere Consulting**, status „**in Progress**"), dar repo-ul asociat este **un stub gol**, iar traducerea `ro_RO` datează din **2020**. Deci: schelet de pornire, fără conținut funcțional.
3. **Cea mai bună bază HR/salarizare** rămâne (confirmat și actualizat față de documentele interne): **suita CDSoftware** (Bitbucket, **întreținută activ în 2026**) + **AMERPSOFT Personnel & Payroll** (GitHub, **release-12**, activ). Nu sunt localizate RO.
4. **Pentru e-Factura / e-Transport / declarații**, deși nu există plugin iDempiere, există **multe implementări open-source portabile** (Go, Python, PHP, TS, .NET și câteva Java) + **biblioteci Java Apache-2.0** pentru UBL/EN16931/CIUS-RO gata de încorporat într-un plugin OSGi.
5. **Cele mai portabile surse de cod** (același model de date) sunt **metasfresh** (contabilitate/fiscal) și **ADempiere Libero + payroll-multi-engine** (HR/salarizare), plus **idempierelbr (Brazilia)** ca **șablon** de plugin de e-Factură + fiscalitate de țară.
6. **Goluri reale (nimic public utilizabil):** motor de salarizare RO (CAS/CASS/CAM/impozit), generator SAF-T D406, client Java modern OAuth2 pentru e-Factura, module SSM/ISU românești.

---

# PARTEA A — Module HR / Salarizare pentru iDempiere (actualizare + corecturi la documentele interne)

> Toate mai jos sunt pentru **modelul iDempiere**. Status actualizat 2026 (documentele interne le dădeau „testat pe 10").

| Modul | Sursă / URL | Versiune / status 2026 | Licență | Instalare | Portabilitate | Note / corecturi |
|---|---|---|---|---|---|---|
| **AMERPSOFT Personnel & Payroll** | `github.com/luisamesty/Amerpsoft-iDempiere-community` (+ editors: `github.com/victorsuarezis/org.amerpsoft.com.idempiere.editors-com`) | **Activ**, ultimul push 2026-07; branch max **release-12** (⚠️ **NU există release-13**) | ⚠️ nedeclarată (verificat înainte de reutilizare) | SRC + update sites (fără JAR-uri în Releases) | ÎNALTĂ | Cel mai bun motor de formule salariale (JavaScript). Module: `personnelpayroll`, `financial`, `lco.withholding` + localizări LVE/LPY/LES. De portat pe release-13. |
| **Suita CDSoftware** — Base, Payroll, Attendance, PayrollReport, EmployeeTraining, EmployeeRecruitment, PerformanceEvaluation, Education, Finreport | `bitbucket.org/cdsoftware/` (24 repo-uri publice) | **Întreținută activ** — majoritatea actualizate **2026-06/07** (nu „doar testat pe 10") | ⚠️ nedeclarată | SRC (`com.cdsoftware.*`) | ÎNALTĂ | Cel mai complet pachet HR: pontaj (terminale Hikvision, ture, întârzieri), recrutare, instruire, evaluare 360°. Dependențe: PayrollReport→Payroll+Attendance; Recruitment→Payroll+EmployeeTraining. Necesită `LCO Detailed Names`. |
| **Ingeint Payroll (original)** | ⚠️ `github.com/ingeint/ingeint-idempiere-payroll` → **404 (dispărut/privat)** | — | — | — | — | Sursa nu mai e disponibilă la URL-ul citat. |
| **Ingeint Payroll (fork-uri supraviețuitoare)** | `github.com/Frontuari/ingeint-idempiere-payroll` (2023) · `github.com/vcappugi/ingeint-idempiere-payroll-master` (2026, Venezuela) | vechi (7.1/8.2) | — | SRC | SCĂZUTĂ | Doar referință istorică / laborator. |
| **NSoft Payroll** | ⚠️ **NECONFIRMAT** — nu am putut găsi repo-ul pe GitHub | — | — | — | — | Posibil eroare în documentul intern. De verificat. |
| **Libero HR & Payroll** | `github.com/adempiere/extension_libero_hr_and_payroll` (titlu: **[DEPRECATED]**) + Maven `io.github.adempiere:adempiere-payroll-multi-engine` (v1.1.7) | deprecated (ADempiere, nu OSGi) | GPLv2 | SRC | ÎNALTĂ (doar modelul + motorul) | Modulul e mort, **DAR** `adempiere-payroll-multi-engine` (motor de salarizare pe reguli) este pe Maven Central și **direct reutilizabil** ca bază pentru calculul RO. |
| **GlobalQSS LCO Detailed Names** | modul în `github.com/globalqss/globalqss-idempiere-lco` (`org.globalqss.idempiere.LCO.detailednames`) | master activ (2026-06); ⚠️ „sync release-13" **neconfirmat** direct (branch-uri până la release-10) | GPLv2 (prin convenție) | P2 / JAR | ÎNALTĂ | Dependență obligatorie a modulelor CDSoftware (nume/prenume + cifra de control tax-ID). |
| **Traducerea RO iDempiere** | `github.com/idempiere-consulting/idempiere-romanian-translation` | **abandonat (2020-05)** | nedeclarată | import XML | — | Doar traducere UI. Fără payroll/declarații. |

**Ordinea de implementare HR (din documentele interne, validă):** 1) dosar salariat + contracte + structură; 2) pontaj + concedii + aprobări; 3) motor salarial RO; 4) note contabile + plăți + fluturași; 5) D112 + validare DUKIntegrator; 6) REGES-ONLINE; 7) restul declarațiilor; 8) recrutare + instruire + evaluare.

---

# PARTEA B — Ecosistemul iDempiere: Contabilitate / Fiscalitate / Financiar / ERP / Integrare

> Wiki oficial: `wiki.idempiere.org/en/Category:Available_Plugins` (~162 pagini de plugin). Aproape toate GPLv2, OSGi.

## B1. Bancă / Extrase / Plăți / SEPA
| Plugin | URL | Ce face | Status |
|---|---|---|---|
| **BX Service SEPA** | `github.com/bxservice/de.bxservice.sepa` | Generează fișiere XML SEPA (Credit Transfer / Direct Debit) | GPLv2, activ 2026 — **cea mai bună bază SEPA reutilizabilă** |
| **BX Service CAMT053 Loader** | `github.com/bxservice/de.bxservice.camt053loader` | Import extrase ISO-20022 CAMT.053 | Activ 2026 |
| **BX Service Hibiscus** | `github.com/bxservice/de.bxservice.hibiscus` | Integrare online-banking Hibiscus/HBCI | Activ 2026 |
| **Bank Statement Matching (nTier)** | `za.co.ntier.bankmatch` (mirror `github.com/idempiere-consulting/za.co.ntier.bankmatch`) | Reconciliere automată linii extras ↔ plăți | ~2020 |
| **e-Evolution PaymentProcessor** | `github.com/e-Evolution/org.eevolution.PaymentProcessor` | Procesatoare Stripe & PayPal | ~2020 |
| **Australian ABA Export** | wiki `Plugin:_Australian_ABA_Export` | Fișiere de plată ABA (AU) | — |

## B2. Taxe / TVA
| Plugin | URL | Ce face |
|---|---|---|
| **BX Service European Tax Provider** | `github.com/bxservice/de.bxservice.europeantaxprovider` | Implementare `TaxProvider` pe adresa de livrare — **bază reutilizabilă pentru TVA UE/RO** |
| **BX Service VAT Number Validator** | `github.com/bxservice/de.bxservice.vatvalidation` | Validare TVA prin VIES |
| **VAT (MTD)** | wiki `Plugin:_VAT_(MTD)` | Making-Tax-Digital HMRC (UK) — model de raportare digitală către fisc |

## B3. E-Factură / Export fiscal (frameworkuri de bază pentru e-Factura RO)
| Plugin | URL | Ce face | Relevanță RO |
|---|---|---|---|
| **ZUGFeRDXInvoice** (Auler/BX Service) | `github.com/bxservice/auler.gmbh.zugferdxinvoice` | Generează ZUGFeRD/Factur-X/XRechnung + emite XML **CII sau UBL 2.1–2.4**, Leitweg-ID (B2G). iDempiere 11, GPLv2, „Testing" | ★★★ **Cea mai apropiată bază reutilizabilă** — emite deja UBL 2.1, exact ce cere CIUS-RO |
| **Facturación Electrónica DIAN (LCOFE)** | `github.com/globalqss/globalqss-idempiere-lcofe` | e-Factură Columbia (DIAN), Carlos Ruiz, activ 2026-04 | ★★★ Șablon de mandat național de e-factură pe model LCO |
| **BX Service DATEV** | `github.com/bxservice/de.bxservice.datev` (+ `de.action42.idempiere.datevexport`) | Export contabil DATEV (DE) | Model de export standardizat către fisc |
| **GoBD / GDPdU** | `Plugin:_GoBD_Plugin` · `github.com/bxservice/de.aulerlichtkabel.gdpdu` | Export audit fiscal (DE) | Analog conceptual pentru SAF-T |
| **BX Service EDI Generator** | `github.com/bxservice/de.bxservice.edi` | Generare documente EDI | — |
| **Intrastat** | `github.com/cloudempiere/eu.idempiere.intrastat` · `idempiere-consulting/LIT_Intrastat` | Declarații Intrastat UE | Direct util RO |
| **Italia SDI / FatturaPA** | `github.com/idempiere-consulting/com.metalsistem.credemsftp` + `idempiere-italia` | e-Factură Italia via SdI (Credemtel) | ★★★ vezi Partea C |
| **Taiwan e-invoice / 401 VAT** | `github.com/tm731531/idempiere-tw-invoice-system` | e-factură + raportare TVA (TW) | Pattern plugin single-country |

## B4. Fixed Assets / Buget / Rapoarte financiare / MRP
- **Fixed Assets**: nucleul iDempiere are deja modul de mijloace fixe/amortizare; plugin suplimentar **Asset Maintenance** (`Plugin:_Asset_Maintenance`).
- **Buget**: **Budgetary Control**, **Import Budget**, `org.idempiere.budget`, **CashForecasting**, Sales/Purchasing Forecast.
- **Rapoarte financiare**: **CDSoftware Finreport** (`Plugin:_CDSoftware_Finreport`), **SFinReport**, **AccountInfoCockpit**, **AulerAccountsInfo**, **idempiereacctedit** (`github.com/globalqss/idempiereacctedit` — editor plan de conturi).
- **MRP / producție**: **Libero Manufacturing** & **Libero Warehousing** (e-Evolution), **TOC Buffer Management** (`globalqss-idempiere-plugins`).

## B5. Raportare (JasperReports)
- **JasperReports** (red1 / Redhuan Oon, GPLv2) — `Plugin:_JasperReports`, integrare clasică cu vizualizatorul Jasper din iDempiere.
- **Extend Jasper Engine**, **BX Service report.jasper** (`github.com/bxservice/de.bxservice.report.jasper`), **Chart Maker**, **ZK Charts**.

## B6. REST API / Integrare / AI (esențial pentru conectarea la ANAF/SPV)
| Componentă | URL | Rol |
|---|---|---|
| **idempiere-rest** | `github.com/bxservice/idempiere-rest` (`com.trekglobal.idempiere.rest.api`) | **Standardul de facto** pentru API REST (JWT, CRUD /models, /processes, /files). iDempiere 12. Docs: `bxservice.github.io/idempiere-rest-docs` — vehiculul de integrare cu ANAF/SPV |
| **Swagger** | `github.com/icreated/swagger` | OpenAPI UI peste REST |
| **idempiere-mcp** | `github.com/hengsin/idempiere-mcp` | Servere MCP (AI) peste iDempiere |
| **Cloudempiere AI / chatGPT** | `github.com/cloudempiere/com.cloudempiere.ai` · `org.idempiere.chatGPT` | LLM / predictiv |

## B7. Managementul documentelor / SSO
- **DMS**: **Logilite DMS** (`github.com/cloudempiere/com.logilite.dms.public`), Alfresco, S3, Google Drive (`hengsin/idempiere-gdrive`), OpenKM.
- **SSO**: Azure MSAL, OIDC (`hengsin/com.trekglobal.sso.oidc`).

## B8. Colecții / furnizori de plugin-uri (unde căutăm cod)
- **BX Service GmbH** — `github.com/bxservice` (~40 repo-uri) — **cea mai activă colecție contabilă** (SEPA, CAMT053, DATEV, tax provider, VIES, EDI, ZUGFeRD, REST).
- **GlobalQSS / Carlos Ruiz** — `github.com/globalqss` — framework **LCO**, **LCOFE** (Columbia), TOC, editor plan de conturi. (Carlos Ruiz = release manager iDempiere → cod autoritativ.)
- **iDempiere Consulting / Marco Longo** — `github.com/idempiere-consulting` (~40 repo-uri) — localizări Italia + Romania (stub) + mirror-uri.
- **Cloudempiere** — `github.com/cloudempiere` — SearchIndex (Elasticsearch), AI, DataExtractor, Intrastat, DMS.
- **hengsin (Heng Sin Low, arhitect core)** — `github.com/hengsin` — REST, MCP, SSO, gdrive.
- **nmicoud (Nicolas Micoud / TGI)** — `github.com/nmicoud` — localizare **franceză** (`idempiere-fr`, `comptaFR_poc`) + `org.tgi.*`.
- **e-Evolution / Victor Perez** — `github.com/e-Evolution` — Libero MRP, PaymentProcessor.
- **red1** — JasperReports, WMS.

---

# PARTEA C — Localizări din alte țări (șabloane de portat pentru RO)

> Cele mai valoroase ca **model de arhitectură** pentru pachetul RO. `★★★` = șablon puternic pentru e-Factura/D112/SAF-T.

| Țară | Sursă | Ce oferă | Relevanță RO |
|---|---|---|---|
| **Italia (LIT)** ★★★ | wiki `Plugin:_Localization_Italy`; `idempiere.it`; `github.com/idempiere-consulting/idempiere-italia`; SdI: `com.metalsistem.credemsftp` | e-Factură **FatturaPA via SdI**, plan de conturi IT, ISTAT, 2Pack. GPLv2, „in progress" | **Cel mai bun analog structural** pentru e-Factura/SPV (XML structurat printr-o platformă statală). Același mentainer ca „Localization Romania" |
| **Columbia (LCO + LCOFE)** ★★★ | `github.com/globalqss/globalqss-idempiere-lco` + `…-lcofe` | Withholding, **`magneticmedia`** (declarații periodice către DIAN), plan de conturi, e-factură DIAN. Carlos Ruiz. Activ 2026 | `magneticmedia` ≈ **D112/SAF-T** (raportare batch); `lcofe` ≈ **e-Factura**. Cod curent, autoritativ |
| **Brazilia (LBR)** ★★★ | `github.com/KenosSGI/org.kenos.idempiere.lbr` (+ predecesor ADempiere `github.com/adempierelbr/adempierelbr`) | **NF-e / NFS-e**, **SPED/EFD/ECD/ECF** (raportare fiscală), boletos, CNAB | Cel mai complet analog **e-Factură + declarații periodice (SPED ≈ SAF-T)** într-o singură localizare. ⚠️ Releases vechi (i6.2, 2020) — verifică branch curent |
| **Venezuela (LVE)** ★★ | Amerpsoft (`release-12_LVE`) · `bitbucket.org/cdsoftware/idempiere-lve-features` (2026) | Withholding, tax-ID, formulare fiscale | Activ |
| **Chile (LCL)** ★★ | EGS Group / Bitbucket; `Plugin:_LCL_Rut_Taxid` | Plan de conturi + cifra de control RUT | Parțial deschis |
| **Peru (LPE)** ★★ | EGS Group / Bitbucket | Plan de conturi; ⚠️ stagnat (r2.0, 2014). Există `iDempiere Perú` comercial cu SUNAT e-invoice | Bază veche |
| **Spania (LES)** ★★ | modul Amerpsoft; `bitbucket.org/tecnoxperience/idempiere_spanish_location` (~70%, 2014) | TVA UE / SEPA-adiacent | Parțial |
| **Franța** ★ | `github.com/nmicoud/idempiere-fr`, `comptaFR_poc` | Plan de conturi FR, `fr_FR` | Referință UE |
| **Japonia (JPiere)** ★ | `github.com/jpiere/idempiere` | Distro JP, practici de afaceri | Pattern de împachetare |
| **Germania** ★ | BX Service (SEPA/DATEV/ZUGFeRD/GoBD) | Fără localizare fiscală completă, dar plugin-uri UE utile | Vezi Partea B |
| **Nicaragua / Kenya / Uganda / Taiwan** | wiki `Localizations` | Withholding / geografie / e-invoice TW | Referință de pattern LCO |
| ⚠️ **Costa Rica, Mexic (CFDI), Argentina (AFIP), Portugalia, India/Indonezia/Thailanda** | — | **Nu s-au găsit** localizări iDempiere (doar traduceri sau biblioteci non-iDempiere) | — |

**Cadrul „LCO" (Localización Colombia → framework reutilizabil):** plugin-uri `org.globalqss.idempiere.LCO.*` peste nucleu, prin **2Pack** (XML de dicționar) + callout-uri/model-validators + servicii OSGi. Interfața `ILCO_TaxIDDigit` permite fiecărei țări să-și înregistreze validarea tax-ID **fără fork**. **RO ar crea** un overlay `…LCO.ro.*` cu: (1) 2Pack cu planul de conturi RO + cote TVA + geografie + `ro_RO`; (2) validare cifră de control **CUI/CIF și CNP**; (3) config withholding; (4) modul e-Factura pe model LIT/LCOFE.

---

# PARTEA D — ERP-uri Java (descendență ADempiere) și biblioteci Java (cod direct portabil)

## D1. ERP-uri din familia Compiere/ADempiere (același model de date → portabilitate ÎNALTĂ)
| Sistem | URL | Ce e relevant | Licență | Portabilitate |
|---|---|---|---|---|
| **metasfresh** | `github.com/metasfresh/metasfresh` | Fork ADempiere 2015, **același model `AD_`/`C_`/`M_`**. Contabilitate, **export DATEV**, SEPA, EDI (EDIFACT). ⚠️ fără XRechnung/ZUGFeRD nativ confirmat (de verificat în repo), fără SAF-T, fără payroll. Foarte activ (~2.4k★) | GPLv2 | **ÎNALTĂ** — cea mai bună sursă de arhitectură/cod contabil-fiscal; pattern-ul de export DATEV = analog pentru **SAF-T** |
| **ADempiere** | `github.com/adempiere/adempiere` | **Libero HR & Payroll** + **`adempiere-payroll-multi-engine`** (Maven `io.github.adempiere`, v1.1.7, motor pe reguli), withholding-engine, localizări LatAm | GPLv2 | **ÎNALTĂ (HR/payroll)** — cel mai relevant cod existent pentru portarea salarizării RO |
| **idempierelbr (Brazilia)** | `github.com/idempierelbr/idempierelbr` (+ `KenosSGI/org.kenos.idempiere.lbr`) | Plugin iDempiere nativ: e-factură NF-e + SPED fiscal + tax engine | GPLv2 | **ÎNALTĂ** — **cel mai bun șablon** de plugin de e-Factură + fiscalitate de țară |
| **Openbravo (CE)** | `gitlab.com/openbravo` | Model propriu; **CE discontinuat ~2020-2021** | OBPL | SCĂZUTĂ (doar referință) |
| **Apache OFBiz** | `github.com/apache/ofbiz-framework` | Contabilitate/HR/payroll de bază; model Entity Engine diferit | **Apache-2.0** (permisiv!) | SCĂZUTĂ cod / bună referință de domeniu |
| **Compiere** | Aptean (CE downloadable) | Strămoșul modelului; îngheșat comercial | GPLv2-derivat | model ÎNALT / valoare practică scăzută |

## D2. Biblioteci Java UBL / EN16931 / Factur-X (încorporabile direct în plugin OSGi → e-Factura RO)
> RO e-Factura = **EN16931 CIUS „RO_CIUS" peste UBL 2.1**, trimisă la ANAF SPV.

| Bibliotecă | URL | Rol | Licență |
|---|---|---|---|
| **ph-ubl** (Philip Helger) | `github.com/phax/ph-ubl` | Citește/scrie **UBL 2.1** ca obiecte JAXB — **prima alegere** pentru generarea RO_CIUS | **Apache-2.0** |
| **phive + phive-rules** (modul **`phive-rules-cius-ro`**) | `github.com/phax/phive` · `github.com/phax/phive-rules` | Motor de validare + reguli **EN16931 + CIUS-RO (v1.0.9)** — **validare nativă Java**, gata cu artefactele ANAF | **Apache-2.0** |
| **Mustang / mustangproject** | `github.com/ZUGFeRD/mustangproject` | Factur-X / ZUGFeRD / XRechnung (CII) + embed XML în PDF/A-3 | **Apache-2.0** |
| **KoSIT validator** (+ `validator-configuration-xrechnung`) | `github.com/itplr-kosit/validator` | Motor oficial DE de validare (XSD+Schematron) — **reutilizabil** cu schematron-ul RO_CIUS | **Apache-2.0** |
| **en16931-cii2ubl / ubl2cii** | `github.com/phax/en16931-cii2ubl` | Conversie CII ↔ UBL 2.1 | **Apache-2.0** |
| **ConnectingEurope/eInvoicing-EN16931** | `github.com/ConnectingEurope/eInvoicing-EN16931` | Artefacte Schematron EN16931 de bază | Apache-2.0 |
| ⚠️ **Konik** | `github.com/konik-io/konik` | ZUGFeRD (CII) — **AGPL, de evitat** (preferă Mustang) | AGPL |

---

# PARTEA E — Implementări RO standalone open-source (orice limbaj, de portat în Java)

## E1. e-Factura (ANAF SPV) — categoria cea mai bogată
| Proiect | URL | Limbaj / Licență | Ce implementează | Portabilitate |
|---|---|---|---|---|
| **printesoi/e-factura-go** ⭐ | `github.com/printesoi/e-factura-go` | Go / **Apache-2.0** (~54★, activ) | **e-Factura + e-Transport + TVA v9**, OAuth2, structuri UBL Invoice-2 (CIUS-RO 1.0.9), XML→PDF, semnătură | **#1 sursă de portare** — model curat al schemei UBL + fluxul OAuth2/upload/status/download (→ JAXB) |
| **robert-malai/anafpy** | `github.com/robert-malai/anafpy` | Python / **Apache-2.0** (~22★, activ 2026) | e-Factura, e-Transport, SPV inbox, registre, **declarații + validare DUKIntegrator + semnare**, MCP | **Cel mai bun șablon de arhitectură** (separarea public/OAuth/SPV/declarații) + lanțul DUK complet |
| **andalisolutions/anaf-php** (+ `oauth2-anaf`) | `github.com/andalisolutions/anaf-php` | PHP / **MIT** (~93★, activ 2026) | Lookup CUI, e-Factura upload/download, provider OAuth2 ANAF (PHP League) | Handshake OAuth2 + DTO-uri, mapare curată în POJO |
| **TecsiAron/ANAF-API-Client-PHP** (+ `ublrenderer`) | `github.com/TecsiAron/ANAF-API-Client-PHP` | PHP / **MIT** (~23★, 2026) | Upload UBL, OAuth2 cert, listare/download SPV; `ublrenderer` = UBL→PDF local | Hartă câmp-cu-câmp UBL→print (util pentru print format iDempiere) |
| **florin-szilagyi/efactura-anaf-ts-sdk** („ts-anaf") | `github.com/florin-szilagyi/efactura-anaf-ts-sdk` | TypeScript / **MIT** (~24★) | OAuth2, upload/status/download, **UblBuilder**, validare, PDF, CLI + MCP | Model concis CIUS-RO (TS→Java direct) |
| **boobo94/efactura-sdk** | `github.com/boobo94/efactura-sdk` | TS / **MIT** (~10★) | „Toate endpoint-urile din OpenAPI ANAF" | idem |
| **Rammer-Tech/ro-efactura (RoEFactura)** | `github.com/Rammer-Tech/ro-efactura` | C# / .NET / **MIT** (activ 2026) | OAuth2 + cert, serializare UBL 2.1, **validare RO_CIUS offline**, upload/download | Bine structurat, referință de flux |
| **Rebootcodesoft/efactura_anaf** | `github.com/Rebootcodesoft/efactura_anaf` | PHP (~42★) | Upload SPV, generare XML, download mesaje | Pragmatic |
| **Meriegg/node-eFactura-generator** | `github.com/Meriegg/node-eFactura-generator` | Node | Generator **UBL 2.1 / CIUS-RO** | Exemplu compact de construire XML |
| **itrack/anaf** | `github.com/itrack/anaf` | PHP / **MIT** (~155★ — cel mai popular, dar stagnat ~2020) | **Lookup plătitor/CUI** (registru art. 316), status TVA + eligibilitate e-factură, batch 100 | Mapare request/response trivială în Java |

## E2. e-Transport (UIT)
- **printesoi/e-factura-go** (`pkg/etransport`) — cea mai completă implementare deschisă.
- **robert-malai/anafpy** — declarații UIT (creare/ștergere/schimbare vehicul/confirmare).
- **OCA `l10n_ro_etransport`** (Odoo) — implementare integrată în ERP (referință funcțională).

## E3. SAF-T D406 — ⚠️ GOL MAJOR
- **Niciun generator open-source** de XML D406. Piața e comercială (SAP, Sovos, SNI, BITSoftware).
- Singurul instrument public = **DUKIntegrator** (Java **închis** al ANAF) care **validează** (nu generează).
- Referință publică: **XSD-ul + structura XLS + validatorul** de la `static.anaf.ro/static/10/Anaf/Informatii_R/saf_t.htm`; index de scheme: `github.com/stefanache/MFP-ANAF-RO`.
- `anafpy` (Python) **orchestrează** DUKIntegrator headless (cel mai bun exemplu de flux).
- **Concluzie:** de construit din XSD-ul ANAF; pattern-ul de export **DATEV din metasfresh** e un bun analog arhitectural. (Odoo `l10n_ro_declaration_D406` = **proprietar**, ~€13.000, neutilizabil.)

## E4. Declarații ANAF (D112, D300, D390, D394, D205, D100…)
| Proiect | URL | Limbaj / Licență | Ce face |
|---|---|---|---|
| **IncrementalCommunity/declaratii-anaf** ⭐ | `github.com/IncrementalCommunity/declaratii-anaf` | **Java** + Gradle, REST + Docker + CLI / **AGPL-3.0** (prin iText5) | **Validare + PDF pentru 127+ tipuri** (D112/D300/D390/D394/D205/D100) — driver headless peste JAR-urile ANAF. **Cel mai apropiat drop-in Java**. ⚠️ atenție AGPL |
| **mihaikelemen/DUKIntegrator** | `github.com/mihaikelemen/DUKIntegrator` | shell + Docker / **MIT** | Dockerizează DUK: validare + PDF pentru D100/D106/D112/D390/D394 |
| **SkipTheDragon/DUKIntegrator-MAC** | `github.com/SkipTheDragon/DUKIntegrator-MAC` | — | Build DUK pentru macOS |
| **Lorin-Cristian/…D205** | `github.com/Lorin-Cristian/Generare-fisier-TXT-pentru-import-PDF-D205-ANAF-Romania` | Python | Generator TXT pentru importul D205 |
| **MfpAnaf/ClientSPV** | `github.com/MfpAnaf/ClientSPV` | **Java** / **MIT** (~54★, **2018, SOAP legacy**) | Exemplu „aproape oficial" de citire inbox SPV / descărcare mesaje. Pattern Java direct, dar API vechi (pre-OAuth2) |

## E5. REGES-ONLINE / Revisal
| Proiect | URL | Ce oferă |
|---|---|---|
| **reges-ro/integrare** ⭐ | `github.com/reges-ro/integrare` | **Resursa principală de portare**: schema **`reges.xsd`**, specificații API, exemple XML/JSON, colecție **Postman**, director **`example/java`**, ghiduri. Test: `dev.inspectiamuncii.org`; prod: `api.inspectiamuncii.ro`. REGES-ONLINE lansat apr. 2025 |

Din XSD generezi direct clase JAXB; exemplele Java arată auth cu token + submit. Nu există încă un client third-party matur (sistemul e nou).

## E6. Aplicații RO cu cod sursă (contabilitate/facturare)
| Proiect | URL | Limbaj / Licență | Ce e valoros |
|---|---|---|---|
| **OCA/l10n-romania** ⭐ | `github.com/OCA/l10n-romania` (fork dev `github.com/dhongu/l10n-romania`) | Odoo/Python / **AGPL-3.0** (~2.500 commit-uri, foarte activ) | **Cea mai matură localizare RO open-source.** Module: `l10n_ro_account_edi_ubl` (**e-Factură CIUS-RO UBL**), `l10n_ro_account_anaf_sync` (OAuth ANAF), `l10n_ro_etransport`, `l10n_ro_message_spv`, TVA la încasare, TVA nedeductibil, cursuri BNR, import MT940, gestiune cantitativ-valorică. **Cea mai bună specificație de mapare** contabilă RO. ⚠️ AGPL = referință, nu copy-paste |
| **ClimenteA/PFASimplu** ⭐ | `github.com/ClimenteA/PFASimplu` | Django / **MIT** (~41★) | **Singurul OSS cu formule fiscale RO lizibile**: **CASS**, deductibilitate parțială (auto 50%, protocol 2%), amortizare, e-Factura UBL 1.0.3, Registru Jurnal/Fiscal/Inventar. (Pentru PFA, nu salarizare de firmă) |
| **stornoro/storno** | `github.com/stornoro/storno` | Symfony + Nuxt | Platformă de facturare RO self-hosted cu integrare **e-Factura SPV** |
| **captainpragmatic/PRAHO** · **CrockyHost/WHMCS-Oblio** · **ContaGo-App/contago** | (GitHub) | Django / PHP / Android | Exemple de wiring e-Factura în aplicații reale |

## E7. Testare / validare
- **phax/phive-rules-cius-ro** (Java, Apache-2.0) — validatorul RO_CIUS de referință (vezi D2).
- **aperta-sync/anaf-api-simulator** (`github.com/aperta-sync/anaf-api-simulator`, TS/NestJS, MIT, ~37★) — **simulator ANAF** (OAuth2 + e-Factura UBL + registru TVA) pentru teste de integrare fără a lovi ANAF prod/sandbox.

---

# PARTEA F — SSM (Securitate și Sănătate în Muncă) și ISU / PSI

> **Concluzie: aproape nimic open-source și specific RO.** Zona e acoperită de SaaS comercial închis (ssm.ro etc.). De construit de la zero.

| Proiect | URL | Ce oferă | Relevanță |
|---|---|---|---|
| **OCA/management-system** | `github.com/OCA/management-system` | Odoo / AGPL-3.0 (~234★, activ). Module ISO 45001: `mgmtsystem_health_safety`, `mgmtsystem_hazard`, `_hazard_risk`, `_nonconformity`, `_claim`, manual HSE | **Cel mai bun schelet HSE generic** — model de date (incidente, pericole, evaluare riscuri) de studiat. **Fără** instructaje/fișe RO, medicina muncii, EPP, registre, ISU/PSI |
| Odoo Apps HSE (`occupational_safety_health_HSE`, `hse_management`, `xf_ehs_incident`) | apps.odoo.com | Incidente, inspecții, PPE, permise | Generic, majoritatea **plătite/proprietare** |
| **civicnet/archived-fiipregatit.ro** | `github.com/civicnet/archived-fiipregatit.ro` | Platformă națională de informare la situații de urgență (WordPress, cu DSU) | **Arhivat**, educație publică — **nu** evidențe PSI de firmă |

**Golul RO SSM/ISU (de dezvoltat de la zero):** fișe de instruire individuală + tematici + periodicități, medicina muncii / fișe de aptitudine, evidență EPP, registre SSM, evidențe ISU/PSI (avize/autorizații, registre PSI, planuri de evacuare, instruiri PSI). Niciun precedent open-source RO.

---

# PARTEA G — Ce lipsește complet (goluri care necesită dezvoltare proprie)

| Domeniu | Situație OSS | Cum procedăm |
|---|---|---|
| **Motor de salarizare RO** (CAS 25%, CASS 10%, CAM 2.25%, impozit 10%, deducere personală, salariu minim, net↔brut) | ⚠️ **Niciun OSS serios.** Calculatoarele web (salariucalculator.ro etc.) au JS închis; `davidbanu/Calculator-Salariu` = toy; PFASimplu = doar PFA | Implementare din **lege** (Codul Fiscal). Motor: `adempiere-payroll-multi-engine` + formule AMERPSOFT. Calculatoarele web = **oracole de test** |
| **Generator SAF-T D406** | ⚠️ **Niciun generator OSS** | Construit din **XSD-ul ANAF**; validare cu DUKIntegrator; pattern DATEV din metasfresh |
| **Client Java modern e-Factura (OAuth2 REST)** | ⚠️ **Niciunul** (MfpAnaf/ClientSPV e SOAP legacy 2018) | Portare din **e-factura-go** (Go) / **anafpy** (Py) + **ph-ubl** + **phive-rules-cius-ro** |
| **Localizare RO iDempiere** (plan de conturi, D112, REGES, declarații) | ⚠️ Doar stub + traducere 2020 | Overlay `LCO.ro.*` nou (vezi Partea C) |
| **Module SSM/ISU RO** | ⚠️ Niciunul | De la zero; `OCA/management-system` ca schiță de model |

---

# PARTEA H — Arhitectura recomandată EVA + harta de portare

> Structura de plugin-uri propusă în documentele interne (validă), cu **sursa de portare** recomandată pentru fiecare.

| Plugin EVA propus | Responsabilitate | Sursă(e) de portare recomandate |
|---|---|---|
| **eva.hr.core** | Persoane, salariați, contracte, acte adiționale, funcții, departamente, dosar electronic | **CDSoftware Base + Payroll** + **AMERPSOFT personnelpayroll** (model), **ADempiere Libero** (model HR) |
| **eva.hr.time** | Ture, pontaje, terminale, ore suplimentare, întârzieri, absențe, concedii, aprobări | **CDSoftware Attendance** (terminale Hikvision, ture rotative) |
| **eva.hr.payroll.ro** | Calcul RO: formule, CAS/CASS/CAM, impozit, deduceri, concedii medicale, recalculări | **`adempiere-payroll-multi-engine`** (motor reguli) + **AMERPSOFT** (formule JS) + **PFASimplu** (formule) + **lege** |
| **eva.hr.accounting** | Note contabile salariale, centre de cost, plăți, fișiere bancare | nucleu iDempiere + **BX Service SEPA / CAMT053** |
| **eva.hr.recruitment** | Posturi, candidați, interviuri, oferte, angajare | **CDSoftware EmployeeRecruitment** |
| **eva.hr.training** | Cursuri, certificări, expirări, planuri de instruire | **CDSoftware EmployeeTraining** |
| **eva.hr.performance** | Obiective, KPI, evaluări periodice, 360° | **CDSoftware PerformanceEvaluation** |
| **eva.ro.reges** | Sincronizare/transmitere REGES-ONLINE, istoric, audit | **reges-ro/integrare** (XSD + `example/java` + Postman) |
| **eva.ro.d112** | Generare XML/PDF D112, rectificative, validare DUK, recipise | **declaratii-anaf** (Java) + **DUKIntegrator** |
| **eva.ro.efactura** *(nou)* | Emitere/primire e-Factura CIUS-RO prin SPV | **e-factura-go / anafpy** (flux) + **ph-ubl** + **phive-rules-cius-ro** (validare Java) + **ZUGFeRDXInvoice** (bază plugin) + **Italia LIT / Columbia LCOFE** (șablon) + **OCA l10n_ro_account_edi_ubl** (mapare) |
| **eva.ro.etransport** *(nou)* | Declarații UIT e-Transport | **e-factura-go / anafpy** (`etransport`) + **OCA l10n_ro_etransport** |
| **eva.ro.anaf.tax** | D100, D101, D205, D300, D301, D390, D394, D398, D700 | **declaratii-anaf** + **DUKIntegrator**; pattern **LCO magneticmedia** |
| **eva.ro.saft** | D406 / SAF-T | **XSD ANAF** (greenfield) + pattern export **DATEV metasfresh** |
| **eva.ro.submission** | Certificate digitale, DUKIntegrator, transmitere, recipise, arhivă | **declaratii-anaf** + **anafpy** (lanț DUK-semnare-depunere) |
| **eva.ssm / eva.isu** *(nou)* | Instructaje, fișe, medicina muncii, EPP, registre, PSI/ISU | Greenfield; **OCA/management-system** ca schiță de model |

**Recomandarea de fond (din documentele interne, confirmată):** pentru EVA soluția corectă **nu** e instalarea unui plugin existent, ci **portarea componentelor utile** (CDSoftware + AMERPSOFT pentru HR, bibliotecile Java pentru e-Factura) și **construirea unei localizări RO proprii, modularizate**. SAGA se folosește în prima etapă ca **reper de calcul și verificare** (D112, salarii, declarații), nu ca motor permanent.

---

## Anexă — Note de licențiere (rezumat)
- **Permisive (sigure de încorporat în plugin GPL):** `e-factura-go`, `anafpy`, `ph-ubl`, `phive`/`phive-rules-cius-ro`, `Mustang`, `KoSIT`, `RoEFactura`, majoritatea bibliotecilor PHP/TS (MIT), `anaf-api-simulator`, `PFASimplu` (MIT), `Apache OFBiz` (Apache-2.0).
- **Copyleft puternic (studiu/specificație, prudență la copy-paste):** `OCA/l10n-romania` (AGPL-3.0), `IncrementalCommunity/declaratii-anaf` (AGPL-3.0), `OCA/management-system` (AGPL-3.0). ⚠️ `Konik` (AGPL) — de evitat.
- **GPLv2 (compatibil cu plugin-ul nostru derivat):** iDempiere, metasfresh, ADempiere, plugin-urile BX Service / GlobalQSS / idempierelbr.
- ⚠️ **Nedeclarate (de clarificat înainte de reutilizare):** AMERPSOFT, suita CDSoftware, unele repo-uri Java ANAF mici (`cui4j`, `declaratii-anaf` marcat AGPL prin dependență).

---

## Note de verificare / avertismente
- `wiki.idempiere.org` are protecție Cloudflare — o parte din datele de wiki provin din Wayback Machine / indexări; pagina „Plugin: Localization Romania" a fost confirmată prin Wayback, dar repo-ul e gol.
- „release-13" pentru AMERPSOFT / LCO Detailed Names **nu** a fost confirmat direct (branch-uri max release-10/12) — de verificat `MANIFEST.MF` pe `master`.
- „NSoft Payroll" din documentul intern **nu a putut fi confirmat** — posibil eroare.
- Numărul de stele / datele ultimului commit sunt la momentul cercetării (mijloc 2026) și se pot schimba.

*Document generat pe baza analizei celor două fișiere interne + cercetare web (6 investigații independente).*
