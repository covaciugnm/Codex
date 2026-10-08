---
name: email-check-sent-too
description: "inainte de orice raspuns despre emailuri, verifica MEREU si trimisele, nu doar inbox-ul"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fdbf626c-59fb-496d-b71c-ef3e86448e46
  modified: 2026-09-22T19:00:19.743Z
---

Cand userul intreaba ceva despre un email ("a raspuns?", "unde suntem cu X?"), nu te uita doar la mesajele primite. Verifica MEREU si folderul de trimise (`eva_search_emails` cu `is_sent: true`, plus un sweep pe intreg contul cu `date_from` pe ziua curenta) si abia apoi formuleaza raspunsul.

**Why:** userul scrie frecvent el insusi emailuri direct din EVA/client, fara sa treaca prin mine. Daca citesc doar inbox-ul, raportez ca „asteptam raspuns" cand de fapt conversatia a avansat deja cu 2 mesaje — imagine gresita si sfaturi inutile.

**How to apply:** intotdeauna doua cautari in paralel — una pe corespondentul respectiv (primite + trimise) si una pe contul de email cu `date_from` = azi, ca sa vezi firul complet si contextul zilei. Apoi rezuma: ultimul mesaj cine l-a trimis, cand, ce e deschis. Vezi si [[draft-contact-details]], [[german-diacritics-emails]].
