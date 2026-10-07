# EVA 3dScan de la scanare metrică la percepție robotică

Dosar separat de cercetare, specificație și organizare a dezvoltării. Acoperă aplicația iPhone, măsurarea obiectelor, camerele și clădirile, urmărirea poziției 6D și transmiterea continuă către un robot humanoid descris prin URDF/Xacro.

**Statut:** propunere tehnică și protocol de cercetare. Implementarea iOS, integrarea robotică și experimentele fizice nu sunt realizate prin acest dosar. „Nivel doctoral” descrie profunzimea întrebărilor, formalizarea și reproductibilitatea propuse; nu reprezintă o teză susținută sau rezultate științifice demonstrate.

## Începe de aici

- [Documentul complet pentru lectură](08_livrabile/DOSAR_COMPLET.html)
- [Documentul complet PDF](08_livrabile/DOSAR_COMPLET.pdf)
- [Documentul complet editabil](08_livrabile/DOSAR_COMPLET.md)
- [Starea curentă și următorul pas](00_control/STATUS.json)
- [Instrucțiuni de reluare](00_control/RELUARE.md)
- [Echipa și fișele de post](02_echipa/FISE_DE_POST.md)
- [Promptul coordonatorului](02_echipa/PROMPT_MASTER.md)
- [Planul cu rezultate cuantificabile](03_plan/PLAN_EXECUTIE.md)
- [Criteriile de acceptare](05_validare/CRITERII_CANONICE.md)
- [Registrul auditurilor](07_audit/REGISTRU.json)
- [Sinteza auditurilor închise](07_audit/AUDIT_FINAL_INTEGRAT.md)

Versiunea documentară livrată are 11 capitole de fond, 28 de roluri, 26 de sarcini, 42 de cerințe, 19 experimente principale și 41 de subteste. Patru audituri independente au închis 13 constatări și au acceptat 62/62 criterii în domeniile declarate. Rapoartele inițiale și remedierea sunt păstrate. Testele produsului rămân planificate.

## Organizarea folderelor

| Folder | Conținut |
|---|---|
| 00_control | Stare, inventar, reluare, decizii și limite |
| 01_capitole | Capitolele de fond și argumentele tehnice |
| 02_echipa | Roluri, independența auditorilor, prompturi și agenți ai aplicației |
| 03_plan | Cerințe, activități, dependențe, livrabile și riscuri |
| 04_contracte | Exemple de mesaje, model de date și montaj robotic |
| 05_validare | Experimente, praguri, protocoale și șabloane de rezultate |
| 06_surse | Bibliografie, fișe de lectură și proveniență |
| 07_audit | Constatări, remedieri, re-audit și verificări automate |
| 08_livrabile | Documente reunite și versiunea pentru tipărire |
| 09_jurnale | Evenimente reale, rezultate și checkpointuri pe autor |
| tools | Instrumentul de jurnalizare, verificare, construire și integritate |

Documentația anterioară din `Aplicație/documentatie` rămâne reper istoric. Pragurile dimensionale adoptate sunt păstrate într-o copie locală identificată; extinderea robotică primește criterii proprii. Site-ul și documentația precedentă nu sunt modificate.

## Sensul acceptării

Închiderea auditului presupune îndeplinirea tuturor criteriilor documentare aplicabile și zero constatări documentare deschise. Auditorul nu certifică performanțe nemăsurate. Testele ce necesită telefon, Mac, robot, instrumente metrologice sau persoane rămân planificate, cu dovezi necesare și responsabil explicit.

Jurnalele consemnează evenimentele la executare sau la cel mai apropiat checkpoint. O întrerupere poate pierde lucru încă nesalvat; nu promitem recuperarea exactă a raționamentului sau a unui cadru intern ARKit. Reluarea pornește de la ultimul artefact confirmat.
