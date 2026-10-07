"""Textele e-mailurilor, în cele 6 limbi ale magazinului.

Cheile sunt aceleași pentru toate limbile; `tr(locale, key)` cade pe română dacă o
traducere lipsește. Textele sunt scurte și comerciale, fără jargon intern.
"""
from __future__ import annotations
from contextvars import ContextVar

_tenant_texts = ContextVar("dracula_mail_texts", default={})

def bind_translations(values):
    _tenant_texts.set(values)


LANGS = ("ro", "en", "de", "hu", "bg", "el")

TEXTS: dict[str, dict[str, str]] = {
    # ── comune ──────────────────────────────────────────────────────────────
    "greeting": {
        "ro": "Bună ziua, {name},", "en": "Hello {name},", "de": "Guten Tag {name},",
        "hu": "Jó napot, {name}!", "bg": "Здравейте, {name},", "el": "Γεια σας {name},",
    },
    "signature": {
        "ro": "Cu stimă,\nEchipa {store}", "en": "Kind regards,\nThe {store} team",
        "de": "Mit freundlichen Grüßen,\nIhr {store}-Team",
        "hu": "Üdvözlettel,\na {store} csapata",
        "bg": "С уважение,\nЕкипът на {store}",
        "el": "Με εκτίμηση,\nΗ ομάδα {store}",
    },
    "my_account": {
        "ro": "Contul meu", "en": "My account", "de": "Mein Konto",
        "hu": "Fiókom", "bg": "Моят профил", "el": "Ο λογαριασμός μου",
    },
    # Expeditorul e o cutie care nu se citeşte (`noreply@…`), deci „răspundeţi la acest
    # e-mail" trimitea clientul în gol. Adresa vine din setările firmei
    # (`core.tenant_settings.legal.email`), nu e scrisă aici: dacă operatorul o schimbă
    # din panou, se schimbă în toate e-mailurile deodată.
    "questions": {
        "ro": "Dacă aveți întrebări, scrieți-ne la {email}",
        "en": "If you have any questions, write to us at {email}",
        "de": "Bei Fragen schreiben Sie uns an {email}",
        "hu": "Ha kérdése van, írjon nekünk a következő címre: {email}",
        "bg": "Ако имате въпроси, пишете ни на {email}",
        "el": "Αν έχετε απορίες, γράψτε μας στο {email}",
    },
    # ── plata confirmată ────────────────────────────────────────────────────
    # ── rambursare (inițiată de proprietar din panou) ─────────────────────────
    "refund.subject": {
        "ro": "Rambursarea pentru comanda {number} a fost inițiată",
        "en": "The refund for order {number} has been initiated",
        "de": "Die Erstattung für Bestellung {number} wurde veranlasst",
        "hu": "A(z) {number} rendelés visszatérítését elindítottuk",
        "bg": "Възстановяването на сумата за поръчка {number} е започнато",
        "el": "Η επιστροφή χρημάτων για την παραγγελία {number} ξεκίνησε",
    },
    "refund.body_card": {
        "ro": "Am inițiat rambursarea sumei de {amount} pentru comanda {number}, pe cardul cu care ați plătit. În funcție de bancă, suma apare în cont în 5–10 zile lucrătoare.",
        "en": "We have initiated a refund of {amount} for order {number} to the card you paid with. Depending on your bank, it will appear in your account within 5–10 business days.",
        "de": "Wir haben die Erstattung von {amount} für die Bestellung {number} auf die Karte veranlasst, mit der Sie bezahlt haben. Je nach Bank erscheint der Betrag innerhalb von 5–10 Werktagen auf Ihrem Konto.",
        "hu": "Elindítottuk a(z) {amount} összeg visszatérítését a(z) {number} rendeléshez arra a kártyára, amellyel fizetett. Banktól függően 5–10 munkanapon belül jelenik meg a számláján.",
        "bg": "Започнахме възстановяване на {amount} за поръчка {number} по картата, с която платихте. В зависимост от банката сумата ще се появи в сметката ви до 5–10 работни дни.",
        "el": "Ξεκινήσαμε την επιστροφή {amount} για την παραγγελία {number} στην κάρτα με την οποία πληρώσατε. Ανάλογα με την τράπεζα, το ποσό θα εμφανιστεί στον λογαριασμό σας σε 5–10 εργάσιμες ημέρες.",
    },
    "refund.body_transfer": {
        "ro": "Am rambursat suma de {amount} pentru comanda {number} prin transfer bancar.",
        "en": "We have refunded {amount} for order {number} by bank transfer.",
        "de": "Wir haben {amount} für die Bestellung {number} per Banküberweisung erstattet.",
        "hu": "A(z) {number} rendeléshez {amount} összeget banki átutalással visszatérítettünk.",
        "bg": "Възстановихме {amount} за поръчка {number} с банков превод.",
        "el": "Επιστρέψαμε {amount} για την παραγγελία {number} με τραπεζική μεταφορά.",
    },
    "paid.subject": {
        "ro": "Plata pentru comanda {number} a fost confirmată",
        "en": "Payment for order {number} confirmed",
        "de": "Zahlung für Bestellung {number} bestätigt",
        "hu": "A(z) {number} rendelés fizetése megerősítve",
        "bg": "Плащането за поръчка {number} е потвърдено",
        "el": "Η πληρωμή για την παραγγελία {number} επιβεβαιώθηκε",
    },
    "paid.body": {
        "ro": "Am primit plata de {total} pentru comanda {number}. Pregătim coletul și vă anunțăm când pleacă.",
        "en": "We received your payment of {total} for order {number}. We are preparing your parcel and will let you know when it ships.",
        "de": "Wir haben Ihre Zahlung über {total} für die Bestellung {number} erhalten. Wir bereiten Ihr Paket vor und melden uns beim Versand.",
        "hu": "Megkaptuk a(z) {total} összegű fizetést a(z) {number} rendeléshez. Előkészítjük a csomagot, és jelezzük, amikor elindul.",
        "bg": "Получихме плащането от {total} за поръчка {number}. Подготвяме пратката и ще ви уведомим при изпращане.",
        "el": "Λάβαμε την πληρωμή σας {total} για την παραγγελία {number}. Ετοιμάζουμε το δέμα και θα σας ενημερώσουμε με την αποστολή.",
    },
    # ── confirmare comandă ──────────────────────────────────────────────────
    "order.subject": {
        "ro": "Comanda {number} a fost înregistrată",
        "en": "Order {number} received", "de": "Bestellung {number} eingegangen",
        "hu": "A(z) {number} rendelés rögzítve", "bg": "Поръчка {number} е приета",
        "el": "Η παραγγελία {number} καταχωρήθηκε",
    },
    "order.intro": {
        "ro": "Vă mulțumim pentru comandă. Am înregistrat-o cu numărul {number} și o pregătim.",
        "en": "Thank you for your order. We have registered it as {number} and are preparing it.",
        "de": "Vielen Dank für Ihre Bestellung. Wir haben sie unter {number} erfasst.",
        "hu": "Köszönjük a rendelését. {number} számon rögzítettük és feldolgozzuk.",
        "bg": "Благодарим за поръчката. Регистрирахме я с номер {number}.",
        "el": "Ευχαριστούμε για την παραγγελία σας. Καταχωρήθηκε με αριθμό {number}.",
    },
    # Varianta pentru plata cu cardul: confirmarea pleacă abia DUPĂ încasare, deci
    # spune ambele lucruri deodată — comanda e primită şi e plătită.
    "order.subject_paid": {
        "ro": "Comanda {number} a fost primită și plătită",
        "en": "Order {number} received and paid",
        "de": "Bestellung {number} eingegangen und bezahlt",
        "hu": "A(z) {number} rendelés beérkezett és kifizetve",
        "bg": "Поръчка {number} е приета и платена",
        "el": "Η παραγγελία {number} παραλήφθηκε και πληρώθηκε",
    },
    "order.intro_paid": {
        "ro": "Vă mulțumim pentru comandă. Am primit plata și am înregistrat comanda cu numărul {number}. O pregătim.",
        "en": "Thank you for your order. We have received your payment and registered the order as {number}. We are preparing it.",
        "de": "Vielen Dank für Ihre Bestellung. Wir haben Ihre Zahlung erhalten und die Bestellung unter {number} erfasst.",
        "hu": "Köszönjük a rendelését. A fizetés megérkezett, a rendelést {number} számon rögzítettük és feldolgozzuk.",
        "bg": "Благодарим за поръчката. Получихме плащането и регистрирахме поръчката с номер {number}.",
        "el": "Ευχαριστούμε για την παραγγελία σας. Λάβαμε την πληρωμή και καταχωρήσαμε την παραγγελία με αριθμό {number}.",
    },
    "order.products": {
        "ro": "Produse", "en": "Products", "de": "Artikel", "hu": "Termékek",
        "bg": "Продукти", "el": "Προϊόντα",
    },
    "order.subtotal": {
        "ro": "Produse (cu TVA)", "en": "Products (incl. VAT)", "de": "Artikel (inkl. MwSt.)",
        "hu": "Termékek (áfával)", "bg": "Продукти (с ДДС)", "el": "Προϊόντα (με ΦΠΑ)",
    },
    "order.shipping": {
        "ro": "Transport", "en": "Shipping", "de": "Versand", "hu": "Szállítás",
        "bg": "Доставка", "el": "Αποστολή",
    },
    "order.total": {
        "ro": "Total de plată", "en": "Total", "de": "Gesamtbetrag",
        "hu": "Fizetendő összesen", "bg": "Общо за плащане", "el": "Σύνολο",
    },
    # Totalul spune clar situaţia plăţii (cererea proprietarului, 21.09.2026): la o
    # comandă plătită cu cardul nu apare nicăieri „de plată".
    "order.total_paid": {
        "ro": "Total plătit", "en": "Total paid", "de": "Bezahlter Gesamtbetrag",
        "hu": "Kifizetett összeg", "bg": "Платена сума", "el": "Σύνολο που πληρώθηκε",
    },
    "order.total_cod": {
        "ro": "Total de plată la livrare", "en": "Total to pay on delivery",
        "de": "Bei Lieferung zu zahlen", "hu": "Átvételkor fizetendő",
        "bg": "Сума за плащане при доставка", "el": "Ποσό πληρωμής κατά την παράδοση",
    },
    "order.total_transfer": {
        "ro": "Total de plată", "en": "Total to pay", "de": "Zu zahlender Betrag",
        "hu": "Fizetendő összeg", "bg": "Сума за плащане", "el": "Ποσό πληρωμής",
    },
    "order.total_plain": {
        "ro": "Total", "en": "Total", "de": "Gesamtbetrag", "hu": "Összesen",
        "bg": "Общо", "el": "Σύνολο",
    },
    # AWB-ul, în e-mailul de expediere (şi în confirmare, dacă există deja)
    "tracking.awb": {
        "ro": "AWB {courier}: {awb}", "en": "{courier} tracking number: {awb}",
        "de": "{courier}-Sendungsnummer: {awb}", "hu": "{courier} csomagszám: {awb}",
        "bg": "Товарителница {courier}: {awb}", "el": "Αριθμός αποστολής {courier}: {awb}",
    },
    "tracking.follow": {
        "ro": "Urmărește coletul", "en": "Track your parcel", "de": "Sendung verfolgen",
        "hu": "Csomag követése", "bg": "Проследете пратката", "el": "Παρακολούθηση δέματος",
    },
    "order.delivery_address": {
        "ro": "Adresa de livrare", "en": "Delivery address", "de": "Lieferadresse",
        "hu": "Szállítási cím", "bg": "Адрес за доставка", "el": "Διεύθυνση παράδοσης",
    },
    "order.payment": {
        "ro": "Plată", "en": "Payment", "de": "Zahlung", "hu": "Fizetés",
        "bg": "Плащане", "el": "Πληρωμή",
    },
    "order.delivery": {
        "ro": "Livrare", "en": "Delivery", "de": "Lieferung", "hu": "Szállítás",
        "bg": "Доставка", "el": "Παράδοση",
    },
    # ── notificare către magazin ────────────────────────────────────────────
    "notify.subject": {
        "ro": "Comandă nouă {number} — {total}", "en": "New order {number} — {total}",
        "de": "Neue Bestellung {number} — {total}", "hu": "Új rendelés {number} — {total}",
        "bg": "Нова поръчка {number} — {total}", "el": "Νέα παραγγελία {number} — {total}",
    },
    # ── schimbare de status ─────────────────────────────────────────────────
    "status.subject": {
        "ro": "Comanda {number}: {status}", "en": "Order {number}: {status}",
        "de": "Bestellung {number}: {status}", "hu": "{number} rendelés: {status}",
        "bg": "Поръчка {number}: {status}", "el": "Παραγγελία {number}: {status}",
    },
    "status.confirmed": {
        "ro": "Comanda dumneavoastră a fost confirmată.",
        "en": "Your order has been confirmed.",
        "de": "Ihre Bestellung wurde bestätigt.",
        "hu": "Rendelését visszaigazoltuk.",
        "bg": "Вашата поръчка е потвърдена.",
        "el": "Η παραγγελία σας επιβεβαιώθηκε.",
    },
    "status.processing": {
        "ro": "Pregătim comanda pentru expediere.",
        "en": "We are preparing your order for shipping.",
        "de": "Wir bereiten Ihre Bestellung für den Versand vor.",
        "hu": "Előkészítjük a rendelését a szállításhoz.",
        "bg": "Подготвяме поръчката за изпращане.",
        "el": "Ετοιμάζουμε την παραγγελία σας για αποστολή.",
    },
    "status.shipped": {
        "ro": "Comanda a fost predată curierului.",
        "en": "Your order has been handed to the courier.",
        "de": "Ihre Bestellung wurde dem Kurier übergeben.",
        "hu": "A rendelést átadtuk a futárnak.",
        "bg": "Поръчката е предадена на куриера.",
        "el": "Η παραγγελία παραδόθηκε στον κούριερ.",
    },
    "status.delivered": {
        "ro": "Comanda a fost livrată. Vă mulțumim!",
        "en": "Your order has been delivered. Thank you!",
        "de": "Ihre Bestellung wurde zugestellt. Vielen Dank!",
        "hu": "A rendelést kézbesítettük. Köszönjük!",
        "bg": "Поръчката е доставена. Благодарим!",
        "el": "Η παραγγελία παραδόθηκε. Ευχαριστούμε!",
    },
    "status.cancelled": {
        "ro": "Comanda a fost anulată. Dacă nu ați cerut anularea, contactați-ne.",
        "en": "Your order has been cancelled. If you did not request this, please contact us.",
        "de": "Ihre Bestellung wurde storniert. Bitte kontaktieren Sie uns, falls nicht gewünscht.",
        "hu": "A rendelést töröltük. Ha nem Ön kérte, vegye fel velünk a kapcsolatot.",
        "bg": "Поръчката е анулирана. Ако не сте я анулирали вие, свържете се с нас.",
        "el": "Η παραγγελία ακυρώθηκε. Αν δεν το ζητήσατε εσείς, επικοινωνήστε μαζί μας.",
    },
    "status.returned": {
        "ro": "Am înregistrat returul comenzii.", "en": "We have registered the return.",
        "de": "Die Rücksendung wurde erfasst.", "hu": "A visszaküldést rögzítettük.",
        "bg": "Регистрирахме връщането.", "el": "Καταχωρήσαμε την επιστροφή.",
    },
    "status.refunded": {
        "ro": "Am returnat suma achitată.", "en": "Your refund has been issued.",
        "de": "Der Betrag wurde erstattet.", "hu": "Az összeget visszatérítettük.",
        "bg": "Сумата е възстановена.", "el": "Το ποσό επιστράφηκε.",
    },
    # ── cont ────────────────────────────────────────────────────────────────
    "welcome.subject": {
        "ro": "Bine ați venit la {store}", "en": "Welcome to {store}",
        "de": "Willkommen bei {store}", "hu": "Üdvözöljük a {store} oldalán",
        "bg": "Добре дошли в {store}", "el": "Καλώς ήρθατε στο {store}",
    },
    "welcome.body": {
        "ro": "Contul dumneavoastră a fost creat. De acum puteți urmări comenzile și salva adrese de livrare.",
        "en": "Your account has been created. You can now track your orders and save delivery addresses.",
        "de": "Ihr Konto wurde erstellt. Sie können nun Bestellungen verfolgen und Adressen speichern.",
        "hu": "Fiókja elkészült. Mostantól nyomon követheti rendeléseit és címeket menthet.",
        "bg": "Профилът ви е създаден. Вече можете да следите поръчките си и да запазвате адреси.",
        "el": "Ο λογαριασμός σας δημιουργήθηκε. Μπορείτε να παρακολουθείτε τις παραγγελίες σας.",
    },
    "verify.subject": {
        "ro": "Confirmați adresa de e-mail", "en": "Confirm your email address",
        "de": "Bestätigen Sie Ihre E-Mail-Adresse", "hu": "Erősítse meg az e-mail-címét",
        "bg": "Потвърдете имейл адреса си", "el": "Επιβεβαιώστε το email σας",
    },
    "verify.body": {
        "ro": "Confirmați adresa de e-mail apăsând butonul de mai jos. Linkul este valabil 48 de ore.",
        "en": "Please confirm your email address using the button below. The link is valid for 48 hours.",
        "de": "Bitte bestätigen Sie Ihre E-Mail-Adresse. Der Link ist 48 Stunden gültig.",
        "hu": "Kérjük, erősítse meg e-mail-címét az alábbi gombbal. A link 48 óráig érvényes.",
        "bg": "Моля, потвърдете имейла си с бутона по-долу. Връзката е валидна 48 часа.",
        "el": "Επιβεβαιώστε το email σας με το κουμπί παρακάτω. Ο σύνδεσμος ισχύει για 48 ώρες.",
    },
    "verify.cta": {
        "ro": "Confirmă adresa", "en": "Confirm address", "de": "Adresse bestätigen",
        "hu": "Cím megerősítése", "bg": "Потвърди адреса", "el": "Επιβεβαίωση",
    },
    "reset.subject": {
        "ro": "Resetarea parolei", "en": "Password reset", "de": "Passwort zurücksetzen",
        "hu": "Jelszó visszaállítása", "bg": "Смяна на паролата",
        "el": "Επαναφορά κωδικού",
    },
    "reset.body": {
        "ro": "Ați cerut resetarea parolei. Apăsați butonul de mai jos; linkul expiră într-o oră. Dacă nu ați cerut asta, ignorați mesajul.",
        "en": "You asked to reset your password. Use the button below; the link expires in one hour. If this was not you, ignore this email.",
        "de": "Sie haben eine Passwortzurücksetzung angefordert. Der Link ist eine Stunde gültig. Andernfalls ignorieren Sie diese E-Mail.",
        "hu": "Jelszó-visszaállítást kért. A link egy óráig érvényes. Ha nem Ön kérte, hagyja figyelmen kívül.",
        "bg": "Поискахте смяна на паролата. Връзката е валидна един час. Ако не сте вие, игнорирайте това писмо.",
        "el": "Ζητήσατε επαναφορά κωδικού. Ο σύνδεσμος λήγει σε μία ώρα. Αν δεν το ζητήσατε, αγνοήστε το.",
    },
    "reset.cta": {
        "ro": "Setează parola nouă", "en": "Set a new password", "de": "Neues Passwort setzen",
        "hu": "Új jelszó beállítása", "bg": "Задай нова парола", "el": "Ορισμός νέου κωδικού",
    },
    # ── e-mail HTML: antet, tabel de produse, pași următori, subsol ─────────
    "order.date": {
        "ro": "Data comenzii", "en": "Order date", "de": "Bestelldatum",
        "hu": "Rendelés dátuma", "bg": "Дата на поръчката", "el": "Ημερομηνία παραγγελίας",
    },
    "order.number": {
        "ro": "Comanda", "en": "Order", "de": "Bestellung", "hu": "Rendelés",
        "bg": "Поръчка", "el": "Παραγγελία",
    },
    "order.item": {
        "ro": "Produs", "en": "Item", "de": "Artikel", "hu": "Termék",
        "bg": "Продукт", "el": "Προϊόν",
    },
    "order.qty": {
        "ro": "Cant.", "en": "Qty", "de": "Menge", "hu": "Db",
        "bg": "Кол.", "el": "Ποσ.",
    },
    "order.line_total": {
        "ro": "Valoare", "en": "Amount", "de": "Betrag", "hu": "Összeg",
        "bg": "Сума", "el": "Αξία",
    },
    "order.sku": {
        "ro": "Cod", "en": "Code", "de": "Art.-Nr.", "hu": "Cikkszám",
        "bg": "Код", "el": "Κωδικός",
    },
    "order.vat_included": {
        "ro": "din care TVA", "en": "of which VAT", "de": "davon MwSt.",
        "hu": "ebből áfa", "bg": "от които ДДС", "el": "εκ των οποίων ΦΠΑ",
    },
    "order.billing_address": {
        "ro": "Adresa de facturare", "en": "Billing address", "de": "Rechnungsadresse",
        "hu": "Számlázási cím", "bg": "Адрес за фактуриране", "el": "Διεύθυνση τιμολόγησης",
    },
    "order.same_as_shipping": {
        "ro": "Aceeași cu adresa de livrare", "en": "Same as the delivery address",
        "de": "Wie die Lieferadresse", "hu": "Megegyezik a szállítási címmel",
        "bg": "Същият като адреса за доставка", "el": "Ίδια με τη διεύθυνση παράδοσης",
    },
    "next_steps": {
        "ro": "Ce urmează", "en": "What happens next", "de": "Wie es weitergeht",
        "hu": "Mi következik", "bg": "Какво следва", "el": "Τι ακολουθεί",
    },
    "next_1": {
        "ro": "Verificăm stocul și confirmăm comanda — de obicei în aceeași zi lucrătoare.",
        "en": "We check stock and confirm your order — usually the same working day.",
        "de": "Wir prüfen den Bestand und bestätigen Ihre Bestellung — meist am selben Werktag.",
        "hu": "Ellenőrizzük a készletet és visszaigazoljuk a rendelést — általában még aznap.",
        "bg": "Проверяваме наличността и потвърждаваме поръчката — обикновено в същия работен ден.",
        "el": "Ελέγχουμε το απόθεμα και επιβεβαιώνουμε την παραγγελία — συνήθως την ίδια εργάσιμη ημέρα.",
    },
    "next_2": {
        "ro": "Pregătim coletul și îl predăm curierului; primiți numărul de urmărire pe e-mail.",
        "en": "We pack your parcel and hand it to the courier; you will get the tracking number by email.",
        "de": "Wir verpacken Ihr Paket und übergeben es dem Kurier; die Sendungsnummer erhalten Sie per E-Mail.",
        "hu": "Összekészítjük a csomagot és átadjuk a futárnak; a nyomkövetési számot e-mailben küldjük.",
        "bg": "Опаковаме пратката и я предаваме на куриера; ще получите номер за проследяване по имейл.",
        "el": "Ετοιμάζουμε το δέμα και το παραδίδουμε στον κούριερ· θα λάβετε τον αριθμό αποστολής με email.",
    },
    "next_3": {
        "ro": "Puteți urmări comanda oricând din contul dumneavoastră.",
        "en": "You can follow your order at any time from your account.",
        "de": "Sie können Ihre Bestellung jederzeit in Ihrem Konto verfolgen.",
        "hu": "Rendelését bármikor nyomon követheti a fiókjában.",
        "bg": "Можете да следите поръчката си по всяко време от профила си.",
        "el": "Μπορείτε να παρακολουθείτε την παραγγελία σας ανά πάσα στιγμή από τον λογαριασμό σας.",
    },
    "footer.legal_links": {
        "ro": "Informații utile", "en": "Useful links", "de": "Nützliche Links",
        "hu": "Hasznos linkek", "bg": "Полезни връзки", "el": "Χρήσιμοι σύνδεσμοι",
    },
    "footer.terms": {
        "ro": "Termeni și condiții", "en": "Terms and conditions",
        "de": "Allgemeine Geschäftsbedingungen", "hu": "Általános szerződési feltételek",
        "bg": "Общи условия", "el": "Όροι χρήσης",
    },
    "footer.privacy": {
        "ro": "Politica de confidențialitate", "en": "Privacy policy",
        "de": "Datenschutzerklärung", "hu": "Adatvédelmi tájékoztató",
        "bg": "Политика за поверителност", "el": "Πολιτική απορρήτου",
    },
    "footer.returns": {
        "ro": "Retur și garanție", "en": "Returns and warranty",
        "de": "Rücksendung und Garantie", "hu": "Visszaküldés és garancia",
        "bg": "Връщане и гаранция", "el": "Επιστροφές και εγγύηση",
    },
    "footer.contact": {
        "ro": "Contact", "en": "Contact", "de": "Kontakt", "hu": "Kapcsolat",
        "bg": "Контакти", "el": "Επικοινωνία",
    },
    "footer.automated": {
        "ro": "Acest mesaj a fost trimis automat de magazinul {store}.",
        "en": "This message was sent automatically by the {store} store.",
        "de": "Diese Nachricht wurde automatisch vom Shop {store} gesendet.",
        "hu": "Ezt az üzenetet a(z) {store} webáruház küldte automatikusan.",
        "bg": "Това съобщение е изпратено автоматично от магазин {store}.",
        "el": "Αυτό το μήνυμα στάλθηκε αυτόματα από το κατάστημα {store}.",
    },
    "welcome.cta": {
        "ro": "Intră în cont", "en": "Go to my account", "de": "Zum Konto",
        "hu": "Belépés a fiókba", "bg": "Към профила", "el": "Στον λογαριασμό μου",
    },
    "order.view_in_account": {
        "ro": "Vezi comanda în contul tău", "en": "View your order in your account",
        "de": "Bestellung in Ihrem Konto ansehen", "hu": "Rendelés megtekintése a fiókjában",
        "bg": "Вижте поръчката в профила си", "el": "Δείτε την παραγγελία στον λογαριασμό σας",
    },
    "status.view_order": {
        "ro": "Vezi comanda", "en": "View order", "de": "Bestellung ansehen",
        "hu": "Rendelés megtekintése", "bg": "Виж поръчката", "el": "Δείτε την παραγγελία",
    },
    "status.placed": {
        "ro": "Am înregistrat comanda dumneavoastră.",
        "en": "We have registered your order.",
        "de": "Wir haben Ihre Bestellung erfasst.",
        "hu": "Rögzítettük a rendelését.",
        "bg": "Регистрирахме вашата поръчка.",
        "el": "Καταχωρήσαμε την παραγγελία σας.",
    },
    "status.pending_payment": {
        "ro": "Comanda așteaptă plata cu cardul.",
        "en": "The order is awaiting card payment.",
        "de": "Die Bestellung wartet auf die Kartenzahlung.",
        "hu": "A rendelés kártyás fizetésre vár.",
        "bg": "Поръчката очаква плащане с карта.",
        "el": "Η παραγγελία αναμένει πληρωμή με κάρτα.",
    },
    "status.pending_stock_mapping": {
        "ro": "Verificăm disponibilitatea produselor din comandă.",
        "en": "We are checking the availability of the items in your order.",
        "de": "Wir prüfen die Verfügbarkeit der bestellten Artikel.",
        "hu": "Ellenőrizzük a rendelt termékek elérhetőségét.",
        "bg": "Проверяваме наличността на продуктите от поръчката.",
        "el": "Ελέγχουμε τη διαθεσιμότητα των προϊόντων της παραγγελίας.",
    },
    # ── metode de livrare și de plată ───────────────────────────────────────
    # În e-mailuri apăreau codurile brute („courier", „cash_on_delivery"), adică
    # jargonul bazei de date, trimis clientului. Etichetele sunt aici, nu în
    # `core.ui_translations`, fiindcă e-mailul se randează și din worker, unde nu
    # avem contextul cererii (tenant, limbă din URL).
    "method.delivery.courier": {
        "ro": "Curier", "en": "Courier", "de": "Kurier", "hu": "Futár",
        "bg": "Куриер", "el": "Κούριερ",
    },
    "method.delivery.pickup": {
        "ro": "Ridicare personală", "en": "Store pickup", "de": "Selbstabholung",
        "hu": "Személyes átvétel", "bg": "Вземане от магазина", "el": "Παραλαβή από το κατάστημα",
    },
    "method.delivery.locker": {
        "ro": "Easybox / locker", "en": "Parcel locker", "de": "Paketstation",
        "hu": "Csomagautomata", "bg": "Автомат за пратки", "el": "Θυρίδα δεμάτων",
    },
    "method.payment.cash_on_delivery": {
        "ro": "Ramburs la livrare", "en": "Cash on delivery", "de": "Nachnahme",
        "hu": "Utánvét", "bg": "Наложен платеж", "el": "Αντικαταβολή",
    },
    "method.payment.bank_transfer": {
        "ro": "Transfer bancar", "en": "Bank transfer", "de": "Banküberweisung",
        "hu": "Banki átutalás", "bg": "Банков превод", "el": "Τραπεζικό έμβασμα",
    },
    "method.payment.card": {
        "ro": "Card online", "en": "Card online", "de": "Kartenzahlung online",
        "hu": "Online bankkártya", "bg": "Онлайн с карта", "el": "Κάρτα online",
    },
    # ── contul creat automat la prima comandă ───────────────────────────────
    "auto_account.subject": {
        "ro": "Bine ai venit la {store}", "en": "Welcome to {store}",
        "de": "Willkommen bei {store}", "hu": "Üdvözlünk a {store} oldalán",
        "bg": "Добре дошли в {store}", "el": "Καλώς ήρθατε στη {store}",
    },
    "auto_account.body": {
        "ro": "Ți-am creat automat un cont la prima comandă, ca să-ți poți urmări "
              "comenzile fără să te înregistrezi separat.",
        "en": "We created an account for you automatically with your first order, so you "
              "can follow your orders without registering separately.",
        "de": "Mit Ihrer ersten Bestellung haben wir automatisch ein Konto für Sie "
              "angelegt, damit Sie Ihre Bestellungen ohne separate Registrierung verfolgen können.",
        "hu": "Az első rendeléssel automatikusan létrehoztunk Önnek egy fiókot, hogy "
              "külön regisztráció nélkül követhesse a rendeléseit.",
        "bg": "Създадохме ви автоматично профил с първата поръчка, за да следите "
              "поръчките си без отделна регистрация.",
        "el": "Δημιουργήσαμε αυτόματα λογαριασμό με την πρώτη σας παραγγελία, ώστε να "
              "παρακολουθείτε τις παραγγελίες σας χωρίς ξεχωριστή εγγραφή.",
    },
    "auto_account.password": {
        "ro": "Nu ai nevoie de parolă acum. Când vrei una, o poți alege din „Setări cont”.",
        "en": "You do not need a password right now. You can choose one anytime from "
              "“Account settings”.",
        "de": "Sie brauchen jetzt kein Passwort. Sie können jederzeit eines unter "
              "„Kontoeinstellungen“ festlegen.",
        "hu": "Most nincs szüksége jelszóra. Bármikor beállíthat egyet a „Fiókbeállítások” "
              "menüben.",
        "bg": "Засега не ви е нужна парола. Можете да зададете по всяко време от "
              "„Настройки на профила“.",
        "el": "Δεν χρειάζεστε κωδικό τώρα. Μπορείτε να ορίσετε έναν όποτε θέλετε από τις "
              "«Ρυθμίσεις λογαριασμού».",
    },
    "auto_account.existing_subject": {
        "ro": "Comanda a fost adăugată în contul tău {store}",
        "en": "Your order was added to your {store} account",
        "de": "Ihre Bestellung wurde Ihrem {store}-Konto hinzugefügt",
        "hu": "A rendelését hozzáadtuk a {store} fiókjához",
        "bg": "Поръчката е добавена към профила ви в {store}",
        "el": "Η παραγγελία προστέθηκε στον λογαριασμό σας {store}",
    },
    "auto_account.existing_body": {
        "ro": "Adresa ta are deja cont la noi, așa că am adăugat comanda acolo. "
              "O găsești autentificându-te pe site.",
        "en": "Your address already has an account with us, so we added the order there. "
              "Sign in on the site to see it.",
        "de": "Für Ihre Adresse besteht bereits ein Konto, deshalb haben wir die Bestellung "
              "dort hinzugefügt. Melden Sie sich auf der Website an, um sie zu sehen.",
        "hu": "A címéhez már tartozik fiók, ezért a rendelést oda tettük. Jelentkezzen be "
              "az oldalon, hogy lássa.",
        "bg": "Вашият адрес вече има профил при нас, затова добавихме поръчката там. "
              "Влезте в сайта, за да я видите.",
        "el": "Η διεύθυνσή σας έχει ήδη λογαριασμό, οπότε προσθέσαμε εκεί την παραγγελία. "
              "Συνδεθείτε στον ιστότοπο για να τη δείτε.",
    },
    "auto_account.cta": {
        "ro": "Vezi contul meu", "en": "Go to my account", "de": "Zu meinem Konto",
        "hu": "A fiókom", "bg": "Към моя профил", "el": "Στον λογαριασμό μου",
    },
    "admin_pwd.subject": {
        "ro": "Parola contului a fost schimbată", "en": "Your account password was changed",
        "de": "Ihr Kontopasswort wurde geändert", "hu": "Fiókja jelszava megváltozott",
        "bg": "Паролата на профила ви е сменена", "el": "Ο κωδικός του λογαριασμού άλλαξε",
    },
    "admin_pwd.body": {
        "de": "Ihr Kontopasswort wurde von einem Administrator des Shops geändert. Alle Sitzungen wurden abgemeldet. Melden Sie sich mit dem mitgeteilten Passwort an. Wenn Sie diese Änderung nicht angefordert haben, kontaktieren Sie uns bitte.",
        "ro": "Parola contului dumneavoastră a fost schimbată de un administrator al "
              "magazinului. Toate sesiunile deschise au fost închise; autentificați-vă cu "
              "parola comunicată de noi. Dacă nu ați cerut această schimbare, contactați-ne.",
        "en": "Your account password was changed by a store administrator. All open "
              "sessions were signed out; sign in with the password we gave you. If you did "
              "not ask for this change, please contact us.",
    },
}


def total_label_key(payment_method: str, payment_status: str, paid: bool = False) -> str:
    """Cheia etichetei de total: plătit / la livrare / transfer / simplu."""
    method = str(payment_method or "")
    if paid or (method == "card" and str(payment_status or "") == "paid"):
        return "order.total_paid"
    if method == "cash_on_delivery":
        return "order.total_cod"
    if method == "bank_transfer":
        return "order.total_transfer"
    return "order.total_plain"


def method_label(locale: str, kind: str, code: str) -> str:
    """Eticheta tradusă a unei metode de livrare/plată; codul, dacă nu o cunoaștem.

    `kind` e „delivery" sau „payment". O metodă nouă, adăugată din panou, apare cu
    numele ei brut — vizibil, dar nu rupt: mai bine „easybox_24" decât gol.
    """
    code = str(code or "").strip()
    if not code:
        return "-"
    key = f"method.{kind}.{code}"
    return tr(locale, key) if key in TEXTS else code


def tr(locale: str, key: str, **kwargs: object) -> str:
    entry = _tenant_texts.get().get(key) or TEXTS.get(key) or {}
    template = entry.get(locale) or entry.get("ro") or TEXTS.get(key, {}).get(locale) or TEXTS.get(key, {}).get("ro") or key
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template
