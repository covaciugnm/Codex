# Remedierea guvernanței R1

Autorul manager a întărit manage.cjs. GOV-A01: validează rolurile, stările, referințele bidirecționale cerință–experiment, subtestele, auditul și dovezile sarcinilor accepted; o sarcină W nu poate fi acceptată cu experimente neexecutate. GOV-A02: registrul accepted cere un raport independent pentru fiecare domeniu obligatoriu, cu agent autor diferit de auditor. GOV-A03: event refuză câmpurile de bază absente; event-json acceptă un checkpoint structurat cu attempt, input_hashes, checks și next. Validarea verifică evenimentele noi și minimul declarat pentru cele istorice. GOV-A04: manifest și verify folosesc aceleași excluderi; fișierele temporare sunt incluse în integritate, iar validate respinge un temporar de lucru din afara fixture-urilor de audit.

Fixture-urile negative rămân în pachet ca dovezi istorice. Registrele lor nu sunt registrele proiectului. Validarea semantică vizează registrele canonice, iar manifestul include și fixture-urile. Rulările R1 nu sunt rescrise pentru a ascunde comportamentul anterior.

Protocolul RELUARE este completat cu event-json și diferența dintre jurnalul sumar și checkpoint. Nu pretindem validarea integrală JSON Schema printr-un motor extern, autentificare criptografică a autorului sau rezistență la un administrator rău intenționat. Auditorul independent reexecută probele R2.
