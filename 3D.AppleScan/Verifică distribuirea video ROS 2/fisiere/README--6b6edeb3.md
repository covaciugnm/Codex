# Planul EVA Robot din 6 octombrie 2026

**Documentație finală acceptată de auditorul independent cu10/10, fără constatări blocante.** Dosarul definește utilizarea iPhone18 Pro Max1TB pentru percepție și interacțiune pe humanoid, procesarea avansată pe server și colaborarea mai multor telefoane/roboți. Implementarea și probele hardware sunt etapa următoare.

## Documentele de pornire

- [Plan final](PLAN_FINAL.md), copie exactă a V2 acceptat.
- [Audit final V2](audit-v2.md), rubrică fixă, surse verificate și hash-uri.
- [Contracte de date și execuție](CONTRACTE_V2.md), repere/timp, mesaje, memorie comună, sync și RobotProfile.
- [Instalare roadmap și teste](EXECUTIE_TESTE_V2.md), servicii,17 taskuri,15 familii de teste și rollback.
- [Manifest SHA256](MANIFEST_SHA256.json), identitatea fișierelor; nu include manifestul însuși.
- [Punct de continuare](RELUARE.md), starea și următorul pas.

## Echipa și rapoartele

| Rol | Sarcină și raport |
|---|---|
| Specialist iPhone hardware și iOS | [API-uri, captură, resurse și probe](01-specialist-iphone-ios.md) |
| Specialist viziune și robotică distribuită | [Metode6D, hărți, server și multi-robot](vision-robotics.md) |
| Specialist iOS, aprofundare modele | [LLM/VLM, voce și identificare facială](03-modele-voce-llm.md) |
| Specialist viziune, aprofundare research | [Alternative fără filtru comercial](04-candidati-research.md) |
| Coordonator | Consolidarea planului, contractelor, testelor și publicării |
| Auditor independent | [Rubrică A1–A10](auditor-preaudit.md), audit V1 și re-audit V2 |

Sunt incluse API-urile iOS27/CoreAI/ARKit object tracking, SAM3.1, FoundationPose, VGGT-Omega, DA3, SLAM colaborativ, GraspGenX/cuRoboV2 și modele audio/VLM actuale. Opțiunile research/necomerciale rămân în comparația tehnică; condițiile de acces/utilizare sunt păstrate pentru instalare.

## Versiunile păstrate

| Versiune | Audit |
|---|---|
| [V1](versiuni/PLAN_V1.md) | [5,5/10](audit-v1.md), observațiile originale păstrate |
| [V2](PLAN_V2.md) | [10/10](audit-v2.md), AV1-01–AV1-08 și observațiile suplimentare închise |
| [Final](PLAN_FINAL.md) | Identic cu V2: SHA256 DB8A63F1E97569B1D44D690FF5AE958877ECFA52D0D27F443B271B3F7870D1EF |

Commit V1 inițial20ae05bc3affcae687880c7279592f233fc46067; checkpoint complet V2 ebedfecdba8b077a11007b42f1cce805b8a8a265. Newline-ul suplimentar adăugat de transport la prima publicare V1 a fost normalizat în checkpoint pentru identitate cu fișierul auditat; istoricul inițial rămâne păstrat. Auditul V1 nu a fost rescris.

Baseline: app0e71d84abeb603db4daf81c5917bab58d36dd728 și main98abc15fbdc5b6ee8c746be637a8094db8e6be3b. Dosarul adaugă documentație; codul aplicației/serverului nu a fost modificat.

## Utilizare și limite

Citiți PLAN_FINAL, apoi CONTRACTE și EXECUTIE_TESTE. Contractele prevalează pentru semantica datelor, EXECUTIE_TESTE pentru praguri/pași, iar planul final și addendumul04 pentru eligibilitatea research. Rapoartele păstrează sursele și alternativele.

Nota10/10 acoperă completitudinea, coerența și verificabilitatea documentației. Nu afirmă instalări efectuate, performanță validată ori o metodă universal superioară. Următorul pas este B01/R0: inventarul real al telefonului, serverului și robotului; apoi corecțiile P0 și benchmark. Modificarea documentelor normative cere o versiune nouă și re-audit.
