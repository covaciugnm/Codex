# OBS-EXPORT-001 — extinderea consemnării la captura de integrare
24.09.2026, Europe/Bucharest; P-MANAGER. Nu modifică indexul original și nu închide o constatare prin autoaudit.

Captura ROM001-G01-integrare-r02 folosește configurația nouă ROM-001_surse_export_G01_v04.json: **17 surse**, 2.571 înregistrări și 428 mesaje publice, 34 fișiere derivate. SHA-256 index: c91068f62646a4bb22ffcb9d8f9369129e7148fd2ce93fd452771a7e06713dca. Au fost verificate egalitatea cu sidecarul și recipisa, toate34amprente/dimensiuni ale derivatelor și toate17prefixe originale la ultimulLF existent.

Literalul index.scope continuă să spună „Only these nine task logs...”, fiind text fix în exportatorul aprobat. **9 este greșit pentru această captură; numărul efectiv este17.** Captura veche de pregătire r01 avea10, nu17. Indexurile și codul înghețat nu sunt cosmetizate. Numărul de înregistrări nu se compară direct între configurații fără a ține cont de sursele adăugate și de timpul capturii.

V04 adaugă P-SYSTEMS la cele16surse dinv03. Configurația, indexul și verificările prezintă explicit actorii. Captura acoperă prefixe observabile până la momentul ei; editorul r02 era încă în producție. Nu include evenimente viitoare, predarea finală/editorul/auditurile încă inexistente. Predările și capturile ulterioare vor completa dosarul. G00 păstrează separat sursele și rundele proprii; nu este refăcut.

Probe: ROM001-G01-EXPORT_INTEGRARE-r02.json, ROM001-G01-EXPORT_INTEGRARE-VERIFICARE-r02.json și ROM001-G01-EXPORT_INTEGRARE-PREFIXE-r02.json din acest dosar. Acesta este un erratum de interpretare și o verificare tehnică de producător, nu acceptare G01, certificare externă sau garanție de capturare a conținutului deja trunchiat de un instrument.

