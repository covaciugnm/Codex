# Copii plate de referință pentru metaauditul r02

24.09.2026. Acest director păstrează 12 copii byte-identice ale indexurilor și sidecar-urilor celor șase capturi r01-after-audit/r02-before-audit, pentru SYS, SEL și RES. Proveniența, căile originale și SHA-256 sunt în provenienta.json. Originalele din 08_ARHIVA nu au fost mutate sau modificate.

Motiv: metaraporturile r02 inițiale declarau direct acele căi 08_ARHIVA ca probe suplimentare. Arhivatorul a refuzat corect ingestia recursivă a arhivelor. OBS-MANAGER-002 consemnează tentativa reală; capturile r02-meta-archive-return păstrează declarațiile inițiale și disponibilitatea observată, fără să pretindă coerență ori aprobare.

Reviziile de ambalare r02-v02 trebuie să citeze aceste copii plate, nu arborele 08_ARHIVA. Digestul fiecărei copii este identic cu al originalului; schimbarea căii de referință nu este un nou audit semantic și nu schimbă scorurile ori verdictul produsului. Verificarea și acceptarea efectivă a noii ambalări sunt consemnate separat după executare.

Acestea sunt copii ale INDEXURILOR, nu copii suplimentare ale întregului conținut al arhivelor. Fișierele enumerate de un index se verifică în captura originală; arhivatorul nu urmărește recursiv JSON-ul indexului drept instrucțiune de copiere.
