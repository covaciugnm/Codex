# Identitatea claselor și a metodelor

Aceste hărți leagă sursele Java decompilate de clasele și metodele din DEX original. O identitate verificată nu confirmă corectitudinea semantică a corpului Java și nu reprezintă o reparație.

- [Clasele celor 11 grupuri istorice](CLASS-MAP-RESULTS.json): 634 surse, dintre care 555 reconfirmări nominale și 79 aliasuri noi; audit independent PASS 10/10.
- [Clasele HeyCyan](HEYCYAN-CLASS-RESULTS.json): 24 surse, dintre care 7 reconfirmări nominale și 17 aliasuri noi; audit independent PASS 10/10.
- [Metodele: potrivire strictă pentru 798 de stuburi](METHOD-STRICT-RESULTS.json): 783 identități exacte și 15 cazuri nerezolvate. Auditul metodelor se raportează separat de auditul claselor.
- [Planul pentru cele 15 aliasuri locale](LOCAL-RENAME-PLAN.json): folosește numai comentariul explicit JADX din antetul metodei care conține exact stubul, cu verificarea completă a prototipului DEX.
- [Planul metodelor HeyCyan](HEYCYAN-METHOD-PLAN.json): extensie separată pentru cele 24 de evenimente noi.

Fiecare eveniment păstrează identificatorul, hashul și calea sursei, poziția UTF16 a literalului și descriptorul DEX, când acesta poate fi confirmat. `UNRESOLVED` și `AMBIGUOUS` rămân rezultate explicite. Identificatorii evenimentelor nu sunt un număr de metode unice.

Metadatele JADX au fost exportate prin `load()` și API-uri de identitate, fără `getCode()`, `decompile()` sau `save()`. Aplicațiile colectate nu au fost executate. Matcherul cere clasa, numele și întregul prototip; bridge-ul care primește `IResponse` nu înlocuiește corpul care primește `AISummaryResponse`.

Hărțile sunt derivate separate. Registrul problemelor, diagnosticele, APK-urile și sursele originale ale decompilării rămân nemodificate. Dovezile Smali, graful referințelor și semantica unui eventual corp reparat necesită verificări distincte.
