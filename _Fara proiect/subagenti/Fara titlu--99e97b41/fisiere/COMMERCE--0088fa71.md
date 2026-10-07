# Date comerciale și verificarea activării

Compania rămâne **Dracula-Company**. Design folosește **Dracula-Castel (Castelul-Dracula)**; Food folosește **Dracula-Farm**. Aceste valori au fost furnizate și confirmate de proprietar. Nu cerem schimbarea sau reconfirmarea lor.

Site-urile funcționează în modul demonstrativ. Prețurile, stocurile și tarifele de transport inițiale sunt demonstrative. Datele care nu au fost furnizate rămân necompletate; nu se inventează CUI, înregistrare, contact, informații despre ingrediente sau condiții comerciale.

În fiecare proiect, `FORMULAR-DATE-COMERCIALE.json` și `FORMULAR-PRETURI-STOCURI.csv` conțin exact produsele acelui proiect. Formularul JSON include câmpurile pentru contact, taxare, livrare și plată. Pentru un catalog schimbat, regenerați formularele cu `python ops/export-commerce-form.py`; această comandă suprascrie doar formularele, deci păstrați separat un formular deja completat.

## Unde se introduc datele

| Date | Administrare / stocare |
|---|---|
| Denumire publică și identitate vânzător | `/admin` → Setări → Identitate; `seller` |
| CUI, înregistrare, contact, bancă | Setări → Date juridice; `legal` |
| Preț, stoc, descrieri, imagini, limbi | Produse; `catalog.products` / traduceri |
| TVA | Setări → TVA; `tax` (revizia trebuie confirmată explicit) |
| Țări, transport și metode de plată | Setări → Livrare / Plăți; `shipping_rules` |
| Textele paginilor în toate limbile | Pagini juridice / Traduceri; `cms.legal_pages` |
| Confirmări finale | `core.tenant_settings.settings.commerce_approval` |
| Chei Stripe | Mediul privat al stack-ului; niciodată în formular |

Paginile publice existente folosesc valorile din baza de date prin variabile precum `{{company_name}}`, `{{address}}`, `{{email}}` și `{{phone}}`. Textele RO/EN/DE rămân editabile în DB; limbi suplimentare se adaugă din administrare. Confirmarea juridică este confirmarea proprietarului asupra textelor, nu o certificare juridică făcută de software.

## Raport executabil, fără modificări

Din folderul proiectului de pe server:

```sh
docker compose exec -T backend python - < ops/check-commerce-readiness.py > commerce-readiness.json
```

Codul de ieșire `0` indică date comerciale complete; `2` indică lipsuri. Raportul JSON enumeră `missing[].field` și `missing[].reason`, fără valori ale secretelor. Datele sunt citite din PostgreSQL cu tenantul propriu. Checkerul nu activează plăți și nu trimite emailuri.

Pe lângă date, este necesară confirmarea explicită a paginilor, taxelor, livrării, metodelor de plată și a fiecărui SKU. Structura de confirmare stocată în `settings.commerce_approval` este:

```json
{
  "legal_pages_confirmed": false,
  "tax_confirmed": false,
  "shipping_confirmed": false,
  "payments_confirmed": false,
  "products": {
    "SKU_DIN_CATALOG": {
      "confirmed_price_ron": null,
      "stock_confirmed": false,
      "content_confirmed": false,
      "food_information_confirmed": false
    }
  }
}
```

`food_information_confirmed` este obligatoriu numai pentru Food. Confirmarea prețului trebuie să corespundă prețului curent, iar `needs_price_review` trebuie eliminat explicit pentru fiecare produs. `settings.demo_prices` devine `false`, iar `tax.requires_review` devine `false` numai după confirmări. Flagurile nu constituie date comerciale și nu înlocuiesc completarea lor. Setările generice sunt acceptate prin endpointul existent `PATCH /api/admin/v1/settings` cu rol owner; obiectele existente trebuie păstrate la actualizare.

## Plăți și activare

Motorul curent calculează în RON. Plata ramburs poate fi configurată fără Stripe. Transferul bancar necesită banca și IBAN. Pentru card, stack-ul propriu trebuie configurat cu `STRIPE_ENABLED`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` și `STRIPE_WEBHOOK_SECRET`; checkerul de live refuză cheile de test. Webhookul și o tranzacție de test trebuie verificate separat înainte de încasări reale.

`COMMERCE_MODE=demo` și `COMMERCE_READY=false` rămân valorile actuale. Simpla schimbare a celor două flaguri nu trebuie să ocolească validatorul de checkout. Emailurile și accesul public se verifică separat: un raport comercial favorabil nu certifică SMTP, Cloudflare sau livrarea fizică.
