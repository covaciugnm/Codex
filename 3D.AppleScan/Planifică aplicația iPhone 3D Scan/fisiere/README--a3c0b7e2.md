# EVA 3D Scan

Dosar de cercetare și proiectare pentru o aplicație iPhone cu trei componente: scanare de obiecte cu dimensiuni, măsurare live fără salvarea implicită a mediului și scanare de camere unite în apartamente și case.

**Data:** 2 octombrie 2026. **Statut:** documentație pentru dezvoltare; aplicația și experimentele fizice nu au fost realizate. Verdictul actual se citește în [starea proiectului](00_management/STATUS.json) și în ultimul raport din `08_audit`.

## Începe de aici

- [PDF complet pentru citire și distribuire](09_livrabile/DOSAR_COMPLET.pdf)
- [Documentul complet pentru lectură și tipărire](09_livrabile/DOSAR_COMPLET.html)
- [Documentul complet editabil](09_livrabile/DOSAR_COMPLET.md)
- [Promptul profesional pentru echipa de dezvoltare](06_prompturi/PROMPT_MASTER.md)
- [Promptul pentru reluare](06_prompturi/PROMPT_RELUARE.md)
- [Criteriile canonice de acceptare](05_validare/CRITERII_CANONICE.md)
- [Registrul sarcinilor](00_management/tasks.json)
- [Auditul final acceptat](08_audit/AUDIT_02_FINAL.md)
- [Bibliografie și fișe locale](07_surse/BIBLIOGRAFIE.md)

## Conținut

| Folder | Ce conține |
|---|---|
| 00_management | Inventar, echipă, sarcini, decizii, riscuri, stare și jurnalele rolurilor |
| 01_cercetare | Șase produse comparate, feedback documentat și UX pentru trei moduri |
| 02_specificatie | Scop, utilizatori, funcții, date, priorități și cerințe |
| 03_arhitectura | Hardware și software Apple, pipeline, stocare, API și recuperare |
| 04_cad_printare | Formate, conversii, DWG, point cloud, imprimare, metrologie și exemple sintetice |
| 05_validare | Praguri canonice, experimente, șablon de rezultate și trasabilitate |
| 06_prompturi | Instrucțiuni complete pentru echipă și pentru reluare |
| 07_surse | 71 înregistrări de surse, fișe originale, PDF NIST și licențe GitHub |
| 08_audit | Audit inițial, remedieri, re-audit și verificări automate |
| 09_livrabile | Documente reunite pentru citire și distribuire |
| tools | Instrumente pentru construire, verificare, jurnalizare și manifest |

Sursele includ 69 de înregistrări consultate în gradele consemnate de specialiști și două articole găsite, dar cu acces integral blocat. Nu toate cele 71 de intrări au fost citite integral și nu toate au fost verificate independent de auditor. Numărul de surse nu dovedește exhaustivitate sau validitate științifică.

## Exemple și documente salvate

[Exemplele sintetice](04_cad_printare/exemple_sintetice/README.md) includ cubul STL 100 mm, un nor PLY cu coordonate cunoscute și conturul DXF al unei camere 4 × 3 m. Controalele interne nu substituie importul în CAD, slicer sau imprimarea fizică.

[Ghidul NIST TN1297](07_surse/fisiere_publice/NIST_TN1297.pdf) este păstrat local pentru documentare. Licențele Open3D, PDAL, ezdxf, lib3mf și COLMAP se află în `07_surse/cad_fisiere_primare`. Aceste capturi ale licențelor nu înlocuiesc analiza dependențelor și a versiunii integrate în viitoarea aplicație. Manifestele păstrează inclusiv eșecurile inițiale și recuperarea descărcărilor.

## Reluare și verificare

Citește STATUS, tasks, ultimul audit și promptul de reluare. Nu începe prin rescrierea întregului dosar. După o întrerupere se reia de la ultimul pas confirmat în fișiere, nu se presupune că o sarcină începută a fost terminată.

Cu Node.js disponibil, din acest folder:

```text
node tools/manage.cjs verify
node tools/manage.cjs validate
```

`verify` citește manifestul fără a schimba fișierele. `validate` scrie un raport nou; după orice editare legitimă se regenerează livrabilele și manifestul. `build` reunește capitolele în Markdown și HTML. `manifest` generează SHA-256. `init` este numai pentru crearea inițială și NU se rulează la reluare, deoarece ar reinițializa registrele. `remediate.cjs` consemnează transformarea unică din primul audit și nu este un pas normal de reluare.

## Limitări și pasul următor

Nu există încă build iOS, benchmark pe telefon, validare CAD/slicer ori imprimare efectivă. Pragurile sunt ținte propuse. Nivelul doctoral privește structura, rigoarea și protocolul; rezultatele cercetării și contribuția originală trebuie demonstrate ulterior.

Primul pas de implementare este inventarierea unui Mac cu Xcode și a telefoanelor disponibile, apoi cele cinci probe Apple din P03. Acest dosar nu efectuează achiziții, publicări sau activări de servicii externe.
