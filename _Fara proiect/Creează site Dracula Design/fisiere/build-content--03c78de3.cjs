const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../outputs/dracula-design-office');
const ui={};
const lines=`
nav.collection|Colecția|The collection|Die Kollektion
nav.story|Semnătura|Our signature|Unsere Handschrift
nav.universe|Universul Dracula|The Dracula universe|Die Dracula-Welt
nav.account|Contul meu|My account|Mein Konto
nav.favorites|Favorite|Favourites|Merkliste
nav.bag|Coșul meu|My bag|Meine Tasche
nav.language|Limba|Language|Sprache
nav.menu|Meniu|Menu|Menü
hero.eyebrow|DRACULA DESIGN OFFICE|DRACULA DESIGN OFFICE|DRACULA DESIGN OFFICE
hero.title|Eleganță.|Elegance.|Eleganz.
hero.emphasis|Fără compromis.|Without compromise.|Ohne Kompromisse.
hero.description|Pentru cei care poartă mai mult decât un accesoriu.|For those who carry more than an accessory.|Für alle, die mehr als ein Accessoire tragen.
hero.cta|Explorează colecția|Explore the collection|Kollektion entdecken
hero.motto|WORK. TRAVEL. LIVE.|WORK. TRAVEL. LIVE.|WORK. TRAVEL. LIVE.
hero.caption|INSPIRED BY TRANSYLVANIA.|INSPIRED BY TRANSYLVANIA.|INSPIRED BY TRANSYLVANIA.
hero.scroll|DESCOPERĂ|DISCOVER|ENTDECKEN
collection.eyebrow|THE SIGNATURE COLLECTION|THE SIGNATURE COLLECTION|THE SIGNATURE COLLECTION
collection.title|Cinci piese.|Five pieces.|Fünf Stücke.
collection.emphasis|Aceeași semnătură.|One signature.|Eine Handschrift.
collection.description|De la întâlnirile de business la momentele care îți aparțin. Obiecte cu personalitate, unite de contrast, proporție și detaliu.|From business meetings to moments of your own. Distinctive pieces, united by contrast, proportion and detail.|Von Geschäftsterminen bis zu Ihren persönlichen Momenten. Ausgewählte Stücke, verbunden durch Kontrast, Proportion und Detail.
collection.all|Toate piesele|All pieces|Alle Stücke
collection.business|Business|Business|Business
collection.women|Feminin|Women|Damen
collection.everyday|Esențiale|Essentials|Essentials
collection.search|Caută în colecție|Search the collection|Kollektion durchsuchen
collection.noresults|Nicio piesă nu corespunde căutării.|No pieces match your search.|Keine Stücke entsprechen Ihrer Suche.
signature.eyebrow|THE ART OF DETAIL|THE ART OF DETAIL|THE ART OF DETAIL
signature.title|Caracterul stă|Character lives|Charakter liegt
signature.emphasis|în detalii.|in the details.|im Detail.
signature.body|O linie roșie pe negru. O monogramă discretă. O proporție care se simte firesc.|A red line on black. A discreet monogram. A proportion that feels natural.|Eine rote Linie auf Schwarz. Ein dezentes Monogramm. Eine Proportion, die sich natürlich anfühlt.
signature.more|Fiecare piesă păstrează echilibrul între forță și rafinament. O identitate care se recunoaște fără să ridice vocea.|Each piece balances strength and refinement. An identity recognised without raising its voice.|Jedes Stück verbindet Stärke und Raffinesse. Eine Identität, die ohne laute Worte erkennbar ist.
universe.eyebrow|THE DRACULA UNIVERSE|THE DRACULA UNIVERSE|THE DRACULA UNIVERSE
universe.title|Mai mult decât un obiect.|More than an object.|Mehr als ein Objekt.
universe.emphasis|O poveste.|A story.|Eine Geschichte.
universe.body|Inspirat de Transilvania. Exprimat prin contrast. Purtat cu încredere.|Inspired by Transylvania. Expressed through contrast. Worn with confidence.|Von Transsilvanien inspiriert. Durch Kontraste ausgedrückt. Mit Selbstbewusstsein getragen.
universe.motto|ELEGANȚĂ. FORȚĂ. INDEPENDENȚĂ.|ELEGANCE. STRENGTH. INDEPENDENCE.|ELEGANZ. STÄRKE. UNABHÄNGIGKEIT.
product.discover|Descoperă piesa|Discover the piece|Das Stück entdecken
product.add|Adaugă în coș|Add to bag|In die Tasche
product.buy|Cumpără acum|Buy now|Jetzt kaufen
product.favorite|Adaugă la favorite|Save to favourites|Auf die Merkliste
product.unfavorite|Elimină din favorite|Remove from favourites|Von Merkliste entfernen
product.details|Detalii|Details|Details
product.care|Îngrijire|Care|Pflege
product.caretext|Păstrează accesoriul ferit de umezeală și căldură directă. Urmează instrucțiunile specifice livrate împreună cu produsul.|Keep the accessory away from moisture and direct heat. Follow the specific care instructions supplied with the product.|Vor Feuchtigkeit und direkter Hitze schützen. Beachten Sie die produktspezifischen Pflegehinweise.
product.delivery|Livrare și retur|Delivery & returns|Versand & Rückgabe
product.deliverytext|Opțiunile și costul livrării sunt afișate înainte de confirmarea comenzii. Consultă politica de retur pentru condițiile aplicabile.|Delivery options and costs are shown before confirming your order. Please consult the returns policy for applicable conditions.|Versandoptionen und Kosten werden vor der Bestellung angezeigt. Die geltenden Bedingungen finden Sie in der Rückgaberichtlinie.
product.available|Disponibil|Available|Verfügbar
product.unavailable|Indisponibil momentan|Currently unavailable|Derzeit nicht verfügbar
product.quantity|Cantitate|Quantity|Menge
product.fullimage|Vezi imaginea completă|View full image|Vollständiges Bild ansehen
product.related|Din aceeași poveste|From the same story|Aus derselben Geschichte
product.code|Cod piesă|Piece reference|Artikelnummer
product.price_note|Prețul final și livrarea sunt afișate la comandă.|Final price and shipping are shown at checkout.|Endpreis und Versand werden an der Kasse angezeigt.
action.continue|Continuă explorarea|Continue exploring|Weiter entdecken
action.close|Închide|Close|Schließen
action.remove|Elimină|Remove|Entfernen
action.save|Salvează|Save|Speichern
action.send|Trimite solicitarea|Send request|Anfrage senden
action.back|Înapoi|Back|Zurück
action.view|Vezi detalii|View details|Details ansehen
action.loading|Se încarcă…|Loading…|Wird geladen…
action.retry|Încearcă din nou|Try again|Erneut versuchen
action.top|Înapoi la început|Back to top|Nach oben
bag.title|Selecția ta|Your selection|Ihre Auswahl
bag.empty|Povestea ta începe cu prima piesă.|Your story begins with the first piece.|Ihre Geschichte beginnt mit dem ersten Stück.
bag.subtotal|Produse|Subtotal|Zwischensumme
bag.shipping|Livrare|Delivery|Versand
bag.total|Total|Total|Gesamt
bag.checkout|Continuă spre comandă|Proceed to checkout|Zur Kasse
bag.added|Piesa a fost adăugată în coș.|The piece has been added to your bag.|Das Stück wurde Ihrer Tasche hinzugefügt.
bag.updated|Selecția a fost actualizată.|Your selection has been updated.|Ihre Auswahl wurde aktualisiert.
favorites.title|Piese de păstrat aproape|Pieces to keep close|Stücke, die bleiben
favorites.empty|Salvează aici piesele care te reprezintă.|Save the pieces that speak to you here.|Speichern Sie hier die Stücke, die Sie ansprechen.
favorites.saved|Piesa a fost salvată în favorite.|The piece has been saved to favourites.|Das Stück wurde auf Ihrer Merkliste gespeichert.
favorites.removed|Piesa a fost eliminată din favorite.|The piece has been removed from favourites.|Das Stück wurde von Ihrer Merkliste entfernt.
account.title|Spațiul tău personal|Your private space|Ihr persönlicher Bereich
account.intro|Colecția ta, comenzile tale, într-un singur loc.|Your collection and your orders, in one place.|Ihre Kollektion und Ihre Bestellungen an einem Ort.
account.orders|Comenzile mele|My orders|Meine Bestellungen
account.profile|Date personale|Personal details|Persönliche Daten
account.password|Schimbă parola|Change password|Passwort ändern
account.addresses|Adresele mele|My addresses|Meine Adressen
account.noorders|Încă nu ai comenzi.|You have no orders yet.|Sie haben noch keine Bestellungen.
account.logout|Deconectare|Sign out|Abmelden
account.saved|Datele au fost salvate.|Your details have been saved.|Ihre Angaben wurden gespeichert.
auth.login|Bine ai revenit|Welcome back|Willkommen zurück
auth.login_action|Intră în cont|Sign in|Anmelden
auth.register|Creează-ți contul|Create your account|Konto erstellen
auth.register_action|Creează cont|Create account|Konto erstellen
auth.haveaccount|Ai deja un cont?|Already have an account?|Sie haben bereits ein Konto?
auth.newaccount|Primul pas în universul Dracula.|Your first step into the Dracula universe.|Ihr erster Schritt in die Dracula-Welt.
auth.required|Autentifică-te pentru a păstra selecția și comenzile în contul tău.|Sign in to keep your selection and orders in your account.|Melden Sie sich an, um Ihre Auswahl und Bestellungen zu speichern.
auth.email|E-mail|Email|E-Mail
auth.password|Parolă|Password|Passwort
auth.confirm|Confirmă parola|Confirm password|Passwort bestätigen
auth.password_hint|Cel puțin 10 caractere.|At least 10 characters.|Mindestens 10 Zeichen.
auth.name|Nume complet|Full name|Vollständiger Name
auth.phone|Telefon|Phone|Telefon
auth.forgot|Ai uitat parola?|Forgot your password?|Passwort vergessen?
auth.reset_title|Un nou început|A fresh start|Ein neuer Anfang
auth.reset_action|Trimite linkul de resetare|Send reset link|Link zum Zurücksetzen senden
auth.reset_sent|Dacă există un cont, solicitarea de resetare a fost înregistrată. Linkul va fi trimis prin e-mail când serviciul de e-mail este configurat.|If an account exists, the reset request has been recorded. The link will be sent when email delivery is configured.|Falls ein Konto existiert, wurde die Anfrage gespeichert. Der Link wird gesendet, sobald der E-Mail-Dienst eingerichtet ist.
auth.newpassword|Parolă nouă|New password|Neues Passwort
auth.currentpassword|Parolă actuală|Current password|Aktuelles Passwort
auth.terms|Accept termenii și condițiile.|I accept the terms and conditions.|Ich akzeptiere die Allgemeinen Geschäftsbedingungen.
auth.privacy|Am citit informarea privind datele personale.|I have read the privacy notice.|Ich habe die Datenschutzhinweise gelesen.
auth.verify_sent|Contul a fost creat. Verificarea e-mailului se finalizează prin linkul trimis de magazin.|Your account has been created. Verify your email using the link sent by the store.|Ihr Konto wurde erstellt. Bestätigen Sie Ihre E-Mail über den Link des Shops.
checkout.title|Ultimul detaliu|The final detail|Das letzte Detail
checkout.subtitle|Completează datele pentru selecția ta.|Complete the details for your selection.|Vervollständigen Sie die Angaben zu Ihrer Auswahl.
checkout.contact|Date de contact|Contact details|Kontaktdaten
checkout.first_name|Prenume|First name|Vorname
checkout.last_name|Nume|Last name|Nachname
checkout.address|Adresa de livrare|Delivery address|Lieferadresse
checkout.line1|Stradă și număr|Street and number|Straße und Hausnummer
checkout.line2|Apartament / detalii suplimentare|Apartment / additional details|Wohnung / weitere Angaben
checkout.city|Localitate|City|Ort
checkout.county|Județ / regiune|County / region|Region / Bundesland
checkout.postal|Cod poștal|Postal code|Postleitzahl
checkout.country|Țară|Country|Land
checkout.delivery|Metodă de livrare|Delivery method|Versandart
checkout.payment|Metodă de plată|Payment method|Zahlungsart
checkout.notes|Observații pentru comandă|Order notes|Bestellhinweise
checkout.review|Selecția ta|Your selection|Ihre Auswahl
checkout.place|Comandă cu obligație de plată|Place order with obligation to pay|Zahlungspflichtig bestellen
checkout.place_demo|Plasează comanda de test|Place test order|Testbestellung aufgeben
checkout.demo_notice|Mod de prezentare: prețurile și stocurile sunt demonstrative. Comanda se salvează ca test; nu se încasează bani și nu se expediază produse.|Preview mode: prices and stock are illustrative. Your order is saved as a test; no payment is collected and no goods are dispatched.|Vorschaumodus: Preise und Bestände sind Beispiele. Die Bestellung wird als Test gespeichert. Es erfolgt keine Zahlung oder Lieferung.
checkout.billing_same|Facturare la aceeași adresă|Use delivery address for billing|Rechnungsadresse entspricht Lieferadresse
checkout.confirmed|Selecția ta este înregistrată.|Your selection has been received.|Ihre Auswahl ist eingegangen.
checkout.reference|Referință comandă|Order reference|Bestellnummer
checkout.test_saved|Comanda de test a fost salvată în magazin și este vizibilă în cont și în administrare.|Your test order has been saved and is visible in your account and in administration.|Ihre Testbestellung wurde gespeichert und ist im Konto und in der Verwaltung sichtbar.
checkout.received|Comanda a fost salvată. Statusul și detaliile sunt disponibile în contul tău.|Your order has been saved. Its status and details are available in your account.|Ihre Bestellung wurde gespeichert. Status und Details finden Sie in Ihrem Konto.
checkout.pending|Plata așteaptă confirmarea procesatorului.|Payment is awaiting confirmation from the provider.|Die Zahlung wartet auf Bestätigung des Zahlungsdienstleisters.
payment.cash_on_delivery|Ramburs|Cash on delivery|Nachnahme
payment.bank_transfer|Transfer bancar|Bank transfer|Banküberweisung
payment.card|Card bancar — plată securizată|Card — secure payment|Karte — sichere Zahlung
checkout.delivery.courier|Curier|Courier|Kurier
checkout.delivery.pickup|Ridicare personală|Collection|Abholung
demo.label|PREVIZUALIZARE PRIVATĂ · PREȚURI DEMONSTRATIVE|PRIVATE PREVIEW · ILLUSTRATIVE PRICES|PRIVATE VORSCHAU · BEISPIELPREISE
demo.price|Preț demonstrativ|Illustrative price|Beispielpreis
demo.order|COMANDĂ DE TEST|TEST ORDER|TESTBESTELLUNG
footer.client|Servicii pentru clienți|Client services|Kundenservice
footer.house|Casa Dracula|The house of Dracula|Das Haus Dracula
footer.legal|Informații legale|Legal information|Rechtliche Informationen
footer.rights|Toate drepturile rezervate.|All rights reserved.|Alle Rechte vorbehalten.
footer.admin|Administrare|Administration|Verwaltung
legal.pending|De completat înainte de deschiderea vânzărilor.|To be completed before sales open.|Vor Verkaufsstart zu ergänzen.
legal.draft|Document de lucru pentru previzualizare. Datele juridice și condițiile comerciale trebuie completate și verificate înainte de lansare.|Preview working document. Legal details and commercial conditions must be completed and checked before launch.|Arbeitsfassung zur Vorschau. Rechtliche Angaben und Geschäftsbedingungen müssen vor dem Start ergänzt und geprüft werden.
contact.title|La dispoziția ta|At your service|Für Sie da
contact.message|Mesajul tău|Your message|Ihre Nachricht
contact.saved|Solicitarea a fost înregistrată. Referința ei este disponibilă echipei în administrare.|Your request has been recorded for the team in administration.|Ihre Anfrage wurde für das Team in der Verwaltung gespeichert.
cookie.title|Discreție, și online.|Discretion, online too.|Diskretion, auch online.
cookie.body|Folosim numai cookie-uri necesare pentru autentificare, coș și securitate. Nu activăm publicitate sau analiză fără acord.|We use only essential cookies for sign-in, your bag and security. Advertising and analytics are not enabled without consent.|Wir verwenden nur notwendige Cookies für Anmeldung, Tasche und Sicherheit. Werbung und Analyse werden nicht ohne Einwilligung aktiviert.
cookie.accept|Am înțeles|Understood|Verstanden
cookie.more|Politica de cookies|Cookie policy|Cookie-Richtlinie
error.general|Nu am putut finaliza acțiunea. Încearcă din nou.|We could not complete this action. Please try again.|Die Aktion konnte nicht abgeschlossen werden. Bitte erneut versuchen.
error.validation_failed|Verifică toate câmpurile obligatorii și acceptarea termenilor.|Check all required fields and accept the terms.|Prüfen Sie alle Pflichtfelder und akzeptieren Sie die Bedingungen.
error.invalid_login|E-mailul sau parola nu este corectă.|Your email or password is incorrect.|E-Mail oder Passwort ist falsch.
error.email_taken|Există deja un cont cu această adresă.|An account with this email already exists.|Ein Konto mit dieser E-Mail existiert bereits.
error.weak_password|Alege o parolă de cel puțin 10 caractere.|Choose a password with at least 10 characters.|Wählen Sie ein Passwort mit mindestens 10 Zeichen.
error.password_mismatch|Parolele nu coincid.|The passwords do not match.|Die Passwörter stimmen nicht überein.
error.out_of_stock|Cantitatea dorită nu mai este disponibilă. Actualizează selecția.|The requested quantity is no longer available. Update your selection.|Die gewünschte Menge ist nicht mehr verfügbar. Aktualisieren Sie Ihre Auswahl.
error.price_changed|Prețul sau transportul s-a schimbat. Verifică noul total înainte de confirmare.|The price or delivery cost changed. Review the updated total before confirming.|Preis oder Versandkosten haben sich geändert. Prüfen Sie den neuen Gesamtbetrag.
error.rate_limited|Prea multe încercări. Te rugăm să revii în câteva minute.|Too many attempts. Please try again in a few minutes.|Zu viele Versuche. Bitte in einigen Minuten erneut versuchen.
error.login_required|Intră în cont pentru a continua.|Sign in to continue.|Melden Sie sich an, um fortzufahren.
error.empty_cart|Coșul tău este gol.|Your bag is empty.|Ihre Tasche ist leer.
error.shop_not_ready|Magazinul nu a deschis încă vânzările reale.|The store has not opened live sales yet.|Der Shop hat den Verkauf noch nicht eröffnet.
error.not_found|Această pagină nu a fost găsită.|This page could not be found.|Diese Seite wurde nicht gefunden.
error.load|Magazinul nu este disponibil momentan. Reîncearcă încărcarea paginii.|The store is temporarily unavailable. Reload the page to try again.|Der Shop ist vorübergehend nicht verfügbar. Laden Sie die Seite erneut.
status.placed|Înregistrată|Received|Eingegangen
status.pending_payment|Așteaptă plata|Awaiting payment|Zahlung ausstehend
status.paid|Plătită|Paid|Bezahlt
status.processing|În pregătire|In preparation|In Vorbereitung
status.shipped|Expediată|Dispatched|Versandt
status.delivered|Livrată|Delivered|Zugestellt
status.cancelled|Anulată|Cancelled|Storniert
status.refunded|Rambursată|Refunded|Erstattet
order.date|Data|Date|Datum
order.status|Status|Status|Status
order.items|Piese|Pieces|Stücke
access.skip|Mergi la conținut|Skip to content|Zum Inhalt springen
access.navigation|Navigare principală|Main navigation|Hauptnavigation
access.image|Imagine produs|Product image|Produktbild
`;
for(const line of lines.trim().split('\n')){const [key,ro,en,de]=line.split('|');if(!de)throw Error(key);ui[key]={ro,en,de};}
const tr=(ro,en,de)=>({ro,en,de});
const products=[
{id:'rucsac-business',sku:'DDO-001',category:'business',price:1490,image:'rucsac-business',name:tr('Rucsac Business','Business Backpack','Business-Rucksack'),description:tr('O siluetă precisă, pentru ritmul zilelor de lucru.','A precise silhouette for the rhythm of your working day.','Eine klare Silhouette für den Rhythmus Ihres Arbeitstages.'),details:tr('Formă structurată. Detalii negre. Cusături contrastante. Compartimentare interioară.','Structured form. Black detailing. Contrast stitching. Interior organisation.','Strukturierte Form. Schwarze Details. Kontrastnähte. Innenaufteilung.')},
{id:'servieta-business',sku:'DDO-002',category:'business',price:1790,image:'servieta-business',name:tr('Servietă Business','Business Briefcase','Business-Aktentasche'),description:tr('Linii clasice. O prezență sigură, fără exces.','Classic lines. A confident presence, without excess.','Klassische Linien. Ein souveräner Auftritt, ohne Übertreibung.'),details:tr('Mânere duble. Baretă de umăr. Organizare interioară. Accente roșii discrete.','Twin handles. Shoulder strap. Organised interior. Subtle red accents.','Zwei Griffe. Schulterriemen. Durchdachter Innenraum. Dezente rote Akzente.')},
{id:'portofel-signature',sku:'DDO-003',category:'everyday',price:490,image:'portofel',name:tr('Portofel Signature','Signature Wallet','Signature-Portemonnaie'),description:tr('Esențialul, păstrat aproape. Semnat discret.','Essentials, kept close. Quietly signed.','Das Wesentliche, immer dabei. Dezent signiert.'),details:tr('Format pliabil. Compartimente pentru carduri. Cusături roșii. Monogramă discretă.','Folded format. Card compartments. Red stitching. Discreet monogram.','Faltformat. Kartenfächer. Rote Nähte. Dezentes Monogramm.')},
{id:'geanta-tote',sku:'DDO-004',category:'women',price:1890,image:'geanta-tote',name:tr('Geantă Tote','Signature Tote','Signature-Tote'),description:tr('Forță și feminitate, într-un contrast inconfundabil.','Strength and femininity in an unmistakable contrast.','Stärke und Weiblichkeit in einem unverwechselbaren Kontrast.'),details:tr('Siluetă structurată. Mânere contrastante. Accente roșii. Semnătură metalică.','Structured silhouette. Contrast handles. Red accents. Metallic signature.','Strukturierte Silhouette. Kontrastierende Griffe. Rote Akzente. Metallische Signatur.')},
{id:'esarfa-signature',sku:'DDO-005',category:'women',price:390,image:'esarfa-signature',name:tr('Eșarfă Signature','Signature Scarf','Signature-Schal'),description:tr('Un gest fluid. O notă de roșu care schimbă totul.','A fluid gesture. A touch of red that changes everything.','Eine fließende Geste. Ein Hauch Rot, der alles verändert.'),details:tr('Compoziție roșu–negru. Monogramă. Drapaj fluid.','Red and black composition. Monogram. Fluid drape.','Komposition in Rot und Schwarz. Monogramm. Fließender Fall.')}
];
const pages=[];const page=(slug,kind,title,body)=>pages.push({slug,kind,title,body});
page('about','company',tr('Despre Dracula Design','About Dracula Design','Über Dracula Design'),tr('Dracula Design este universul de accesorii al {{company_name}}. Negrul, roșul și o semnătură discretă definesc colecția.\n\nDe la rucsacul business la eșarfa Signature, cele cinci piese explorează echilibrul dintre forță și rafinament.\n\nReperul nostru: {{address}}.','Dracula Design is the accessories universe of {{company_name}}. Black, red and a discreet signature define the collection.\n\nFrom the Business Backpack to the Signature Scarf, five pieces explore the balance between strength and refinement.\n\nOur reference point: {{address}}.','Dracula Design ist die Accessoire-Welt von {{company_name}}. Schwarz, Rot und eine dezente Signatur prägen die Kollektion.\n\nVom Business-Rucksack bis zum Signature-Schal erkunden fünf Stücke das Gleichgewicht von Stärke und Raffinesse.\n\nUnser Bezugspunkt: {{address}}.'));
page('contact','service',tr('Contact','Contact','Kontakt'),tr('Companie: {{company_name}}\nAdresă indicată: {{address}}\nE-mail: {{email}}\nTelefon: {{phone}}\n\nFolosește formularul pentru întrebări despre colecție, comenzi sau servicii. Solicitarea este înregistrată în sistemul magazinului.','Company: {{company_name}}\nListed address: {{address}}\nEmail: {{email}}\nTelephone: {{phone}}\n\nUse the form for questions about the collection, orders or services. Your request is recorded in the store system.','Unternehmen: {{company_name}}\nAngegebene Adresse: {{address}}\nE-Mail: {{email}}\nTelefon: {{phone}}\n\nNutzen Sie das Formular für Fragen zur Kollektion, zu Bestellungen oder zum Service. Ihre Anfrage wird im Shopsystem gespeichert.'));
page('terms','legal',tr('Termeni și condiții','Terms and conditions','Allgemeine Geschäftsbedingungen'),tr('1. Vânzătorul\nMagazinul este operat de {{company_name}}, la adresa {{address}}. Identificare fiscală: {{cui}}. Registrul comerțului: {{registration}}. Contact: {{email}}.\n\n2. Produse și prețuri\nDescrierile și prețurile aplicabile sunt cele prezentate la confirmarea comenzii. Costul transportului este afișat separat. În modul de prezentare, toate valorile comerciale sunt demonstrative.\n\n3. Comanda\nClientul poate revizui produsele, cantitățile și adresa înainte de confirmare. Primirea comenzii este înregistrată în cont. Plata online este confirmată exclusiv de procesatorul autorizat.\n\n4. Executarea contractului\nCondițiile finale de acceptare, livrare, facturare și plată se publică după completarea informațiilor comerciale ale vânzătorului. Drepturile legale ale consumatorului nu sunt limitate de acești termeni.','1. Seller\nThe store is operated by {{company_name}} at {{address}}. Tax ID: {{cui}}. Company registration: {{registration}}. Contact: {{email}}.\n\n2. Products and prices\nThe descriptions and prices applicable are those displayed when confirming the order. Delivery is itemised separately. In preview mode, commercial values are illustrative.\n\n3. Ordering\nCustomers can review products, quantities and addresses before confirmation. Receipt is recorded in the account. Online payment is confirmed exclusively by the authorised provider.\n\n4. Contract performance\nFinal acceptance, delivery, invoicing and payment terms will be published once the seller’s commercial details are completed. Statutory consumer rights remain unaffected.','1. Verkäufer\nDer Shop wird von {{company_name}}, {{address}}, betrieben. Steuer-ID: {{cui}}. Handelsregister: {{registration}}. Kontakt: {{email}}.\n\n2. Produkte und Preise\nEs gelten die bei Bestellbestätigung angezeigten Beschreibungen und Preise. Versandkosten werden gesondert ausgewiesen. Im Vorschaumodus dienen kaufmännische Werte nur als Beispiele.\n\n3. Bestellung\nProdukte, Mengen und Adresse können vor Bestätigung geprüft werden. Der Eingang wird im Konto gespeichert. Onlinezahlungen bestätigt ausschließlich der autorisierte Zahlungsdienstleister.\n\n4. Vertragsabwicklung\nEndgültige Bedingungen zu Annahme, Lieferung, Rechnungsstellung und Zahlung werden nach Ergänzung der Unternehmensdaten veröffentlicht. Gesetzliche Verbraucherrechte bleiben unberührt.'));
page('privacy','legal',tr('Confidențialitate','Privacy notice','Datenschutzhinweise'),tr('Operator: {{company_name}}, {{address}}. Contact pentru date personale: {{email}}.\n\nPrelucrăm informațiile de cont, adresă și comandă pentru furnizarea serviciilor solicitate și îndeplinirea obligațiilor legale. Parolele sunt stocate sub formă de hash. Datele cardului nu sunt colectate de magazin.\n\nInformațiile necesare pot fi furnizate procesatorilor de plată, curierilor și furnizorilor tehnici configurați pentru magazin. Lista furnizorilor, termenele de păstrare și temeiurile aplicabile trebuie completate înainte de lansare.\n\nPoți solicita acces, rectificare, ștergere sau alte drepturi aplicabile prin formularul dedicat. Cererile sunt verificate înainte de executare. Poți depune o plângere la autoritatea de supraveghere competentă.','Controller: {{company_name}}, {{address}}. Personal data contact: {{email}}.\n\nAccount, address and order information is processed to provide requested services and fulfil legal obligations. Passwords are stored as hashes. The store does not collect card details.\n\nNecessary information may be shared with configured payment, delivery and technical providers. The provider list, retention periods and applicable legal bases must be completed before launch.\n\nYou may request access, correction, deletion or other applicable rights using the dedicated form. Requests are verified before fulfilment. You may lodge a complaint with the competent supervisory authority.','Verantwortlicher: {{company_name}}, {{address}}. Datenschutzkontakt: {{email}}.\n\nKonto-, Adress- und Bestelldaten werden zur Erbringung angeforderter Leistungen und zur Erfüllung gesetzlicher Pflichten verarbeitet. Passwörter werden als Hash gespeichert. Der Shop erhebt keine Kartendaten.\n\nErforderliche Daten können an eingerichtete Zahlungs-, Versand- und technische Dienstleister weitergegeben werden. Anbieter, Aufbewahrungsfristen und Rechtsgrundlagen sind vor dem Start zu ergänzen.\n\nÜber das Formular können Sie Auskunft, Berichtigung, Löschung und weitere anwendbare Rechte beantragen. Anfragen werden vor Bearbeitung geprüft. Sie können sich bei der zuständigen Aufsichtsbehörde beschweren.'));
page('data-deletion','legal',tr('Date personale și ștergere','Personal data and deletion','Personenbezogene Daten und Löschung'),tr('Poți cere ștergerea contului sau a datelor personale prin formularul de mai jos. Include adresa de e-mail a contului și natura cererii, fără a trimite parole.\n\nVerificăm identitatea solicitantului înainte de aplicare. Datele care trebuie păstrate pentru obligații legale sau litigii nu pot fi șterse imediat; îți vom explica situația aplicabilă.','Request account or personal data deletion using the form below. Include your account email and the nature of your request, without sending passwords.\n\nWe verify the requester’s identity before acting. Data required for legal obligations or disputes cannot always be deleted immediately; we will explain the applicable position.','Die Löschung Ihres Kontos oder personenbezogener Daten können Sie mit dem Formular beantragen. Geben Sie die Konto-E-Mail und Ihr Anliegen an, jedoch keine Passwörter.\n\nVor Umsetzung prüfen wir Ihre Identität. Gesetzlich aufzubewahrende oder für Rechtsstreitigkeiten benötigte Daten können nicht immer sofort gelöscht werden; wir erläutern Ihnen die Situation.'));
page('returns','service',tr('Retur și garanție','Returns and guarantee','Rückgabe und Gewährleistung'),tr('Pentru achizițiile online eligibile ale consumatorilor din UE se aplică, în general, dreptul de retragere în 14 zile de la primirea bunurilor și o garanție legală minimă de conformitate de doi ani. Excepțiile prevăzute de lege rămân aplicabile.\n\nAnunță intenția de retur prin formularul de retragere, indicând comanda și produsele. Nu expedia un colet la reperul „Dracula-Castel” fără o adresă poștală completă confirmată.\n\nCosturile de retur, procedura de rambursare și adresa de retur trebuie confirmate și publicate înainte de lansare.','Eligible EU consumer online purchases generally carry a 14-day withdrawal right from receipt of goods and a minimum two-year legal conformity guarantee. Statutory exceptions remain applicable.\n\nNotify us using the withdrawal form with your order and items. Do not dispatch a parcel to the “Dracula-Castel” reference without a confirmed full postal address.\n\nReturn costs, refund procedure and the return address must be confirmed and published before launch.','Für berechtigte Onlinekäufe von EU-Verbrauchern gelten grundsätzlich ein 14-tägiges Widerrufsrecht ab Warenerhalt und eine mindestens zweijährige gesetzliche Gewährleistung. Gesetzliche Ausnahmen bleiben anwendbar.\n\nNutzen Sie das Widerrufsformular und nennen Sie Bestellung und Artikel. Versenden Sie keine Pakete an „Dracula-Castel“, solange keine vollständige Postadresse bestätigt wurde.\n\nRücksendekosten, Erstattungsverfahren und Rücksendeadresse müssen vor Verkaufsstart festgelegt und veröffentlicht werden.'));
page('withdrawal','service',tr('Formular de retragere','Withdrawal form','Widerrufsformular'),tr('Către {{company_name}}.\n\nComunică intenția de retragere din contract și menționează numărul comenzii, produsele, data primirii, numele și adresa cumpărătorului. Formularul online înregistrează solicitarea în magazin; păstrează o copie a datelor trimise.','To {{company_name}}.\n\nState your intention to withdraw and include the order number, items, delivery date, purchaser name and address. The online form records your request in the store; retain a copy of the submitted information.','An {{company_name}}.\n\nTeilen Sie Ihren Widerruf mit und nennen Sie Bestellnummer, Artikel, Empfangsdatum sowie Namen und Anschrift des Käufers. Das Onlineformular speichert Ihre Anfrage im Shop; bewahren Sie eine Kopie Ihrer Angaben auf.'));
page('shipping','service',tr('Livrare','Delivery','Versand'),tr('Țările, metodele și costurile de livrare sunt configurate în magazin și afișate la comandă înainte de confirmare.\n\nÎn previzualizare, opțiunile pentru România și Germania și tarifele afișate sunt de test. Nu se generează expedieri reale.\n\nDupă lansare, informațiile privind termenul de pregătire, curierul și urmărirea expedierii vor fi disponibile în detaliile comenzii, conform configurației comerciale aprobate.','Delivery countries, methods and costs are configured in the store and shown before confirmation.\n\nDuring preview, Romania and Germany options and displayed rates are test settings. No real shipments are created.\n\nAfter launch, preparation times, courier and tracking information will be available in order details according to the approved commercial setup.','Lieferländer, Versandarten und Kosten werden im Shop konfiguriert und vor Bestätigung angezeigt.\n\nIn der Vorschau sind Rumänien, Deutschland und angezeigte Tarife Testeinstellungen. Es werden keine echten Sendungen erstellt.\n\nNach dem Start stehen Bearbeitungszeit, Kurier und Sendungsverfolgung entsprechend der freigegebenen Konfiguration in den Bestelldetails bereit.'));
page('payments','service',tr('Modalități de plată','Payment methods','Zahlungsarten'),tr('Metodele disponibile apar la finalizarea comenzii. Plata cu cardul este disponibilă numai după conectarea procesatorului și activarea magazinului. Datele cardului sunt introduse pe pagina securizată a procesatorului.\n\nÎn modul de prezentare, comenzile sunt teste și nu se încasează bani. Nu efectua transferuri bancare pentru aceste comenzi.','Available methods appear at checkout. Card payment is offered only after the provider is connected and sales are enabled. Card details are entered on the provider’s secure page.\n\nIn preview mode, orders are tests and no funds are collected. Do not make bank transfers for these orders.','Verfügbare Zahlungsarten erscheinen an der Kasse. Kartenzahlung wird erst nach Anbindung des Dienstleisters und Verkaufsfreigabe angeboten. Kartendaten werden auf der sicheren Seite des Zahlungsdienstleisters eingegeben.\n\nIm Vorschaumodus sind Bestellungen Tests ohne Zahlung. Überweisen Sie für solche Bestellungen kein Geld.'));
page('cookies','legal',tr('Politica de cookies','Cookie policy','Cookie-Richtlinie'),tr('Magazinul utilizează cookie-uri necesare pentru sesiunea de autentificare, coș, protecția CSRF și preferințele de limbă. Acestea permit funcționarea serviciilor solicitate.\n\nNu sunt încărcate servicii de publicitate sau analiză în această versiune. Dacă vor fi adăugate, vor fi activate numai după alegerea corespunzătoare a utilizatorului.\n\nPoți șterge cookie-urile din browser; autentificarea și selecția din coș pot fi afectate.','The store uses necessary cookies for sign-in sessions, the bag, CSRF protection and language preferences. These enable the services you request.\n\nThis version does not load advertising or analytics services. If added later, they will be enabled only after the appropriate user choice.\n\nYou can delete cookies in your browser; this may affect sign-in and your bag.','Der Shop verwendet notwendige Cookies für Anmeldung, Tasche, CSRF-Schutz und Spracheinstellungen. Sie ermöglichen die angeforderten Funktionen.\n\nDiese Version lädt keine Werbe- oder Analysedienste. Werden solche später ergänzt, erfolgen sie erst nach entsprechender Auswahl des Nutzers.\n\nCookies können im Browser gelöscht werden. Dies kann Anmeldung und Tasche beeinflussen.'));
page('complaints','service',tr('Reclamații și soluționare','Complaints and resolution','Beschwerden und Streitbeilegung'),tr('Trimite reclamația prin formular, cu referința comenzii și o descriere a situației. Echipa magazinului o poate urmări în administrare.\n\nPoți contacta ANPC sau organismul competent de soluționare alternativă. Platforma europeană ODR a fost închisă; nu o folosim pentru depunerea reclamațiilor.','Send your complaint using the form, with the order reference and a description. The store team can follow it in administration.\n\nYou may contact ANPC or the competent alternative dispute resolution body. The European ODR platform has closed and is not used for complaints.','Senden Sie Ihre Beschwerde mit Bestellnummer und Beschreibung über das Formular. Das Team kann sie in der Verwaltung bearbeiten.\n\nSie können sich an ANPC oder die zuständige Streitbeilegungsstelle wenden. Die europäische OS-Plattform wurde eingestellt und wird nicht für Beschwerden genutzt.'));
page('faq','service',tr('Întrebări frecvente','Frequently asked questions','Häufige Fragen'),tr('Cum salvez o piesă?\nFolosește simbolul de favorite de lângă produs. Favoritele sunt păstrate în contul tău.\n\nPot schimba limba?\nDa. Selectorul de limbă păstrează pagina curentă, iar produsele și textele sunt încărcate în limba aleasă.\n\nCum văd comenzile?\nÎn Contul meu → Comenzile mele.\n\nSe poate cumpăra acum?\nÎn previzualizare poți parcurge o comandă de test. Încasările reale vor fi disponibile după configurarea comercială a magazinului.','How do I save a piece?\nUse the favourite symbol beside the product. Favourites are saved in your account.\n\nCan I change language?\nYes. The selector keeps your current page and loads products and text in the selected language.\n\nWhere are my orders?\nIn My account → My orders.\n\nCan I purchase now?\nDuring preview you can complete a test order. Real payments become available after commercial setup.','Wie speichere ich ein Stück?\nNutzen Sie das Merkliste-Symbol am Produkt. Die Auswahl bleibt in Ihrem Konto gespeichert.\n\nKann ich die Sprache wechseln?\nJa. Die aktuelle Seite bleibt erhalten; Produkte und Texte werden in der gewählten Sprache geladen.\n\nWo finde ich Bestellungen?\nUnter Mein Konto → Meine Bestellungen.\n\nKann ich schon kaufen?\nIn der Vorschau sind Testbestellungen möglich. Echte Zahlungen werden nach Einrichtung freigeschaltet.'));
page('legal-notice','legal',tr('Informații despre companie','Company information','Impressum'),tr('Denumire furnizată: {{company_name}}\nAdresă furnizată: {{address}}\nIdentificare fiscală: {{cui}}\nRegistrul comerțului: {{registration}}\nE-mail: {{email}}\nTelefon: {{phone}}\n\nDenumirea juridică completă, sediul poștal și identificatorii legali trebuie validați înainte de lansarea comercială.','Supplied company name: {{company_name}}\nSupplied address: {{address}}\nTax ID: {{cui}}\nCompany registration: {{registration}}\nEmail: {{email}}\nPhone: {{phone}}\n\nThe complete legal name, postal address and legal identifiers must be validated before commercial launch.','Angegebene Firma: {{company_name}}\nAngegebene Adresse: {{address}}\nSteuer-ID: {{cui}}\nHandelsregister: {{registration}}\nE-Mail: {{email}}\nTelefon: {{phone}}\n\nVollständige Firmierung, Postanschrift und gesetzliche Angaben müssen vor dem Verkaufsstart bestätigt werden.'));
page('accessibility','legal',tr('Accesibilitate','Accessibility','Barrierefreiheit'),tr('Magazinul este conceput pentru navigare cu tastatura, etichete text pentru simboluri, contrast ridicat și afișare adaptată dispozitivului.\n\nDacă întâmpini o barieră, trimite pagina și o descriere prin formularul de contact. Această declarație descrie intenția de proiectare și nu reprezintă certificarea unei conformități auditate.','The store is designed for keyboard navigation, text labels for symbols, high contrast and responsive layouts.\n\nIf you encounter a barrier, send the page and a description through the contact form. This statement describes design intent and is not a certification of audited compliance.','Der Shop ist für Tastaturbedienung, Textbeschriftungen an Symbolen, hohe Kontraste und flexible Bildschirmgrößen gestaltet.\n\nMelden Sie Barrieren mit Seitenangabe und Beschreibung über das Kontaktformular. Diese Erklärung beschreibt das Gestaltungsziel und ist keine geprüfte Konformitätszertifizierung.'));
// Store the existing administrative labels in PostgreSQL as well.
for(const lang of ['ro','en','de']){
 const data=JSON.parse(fs.readFileSync(path.join(root,'frontend/src/i18n/locales',lang+'.json'),'utf8'));
 function flatten(obj,prefix=''){for(const [key,value] of Object.entries(obj)){const k=prefix?prefix+'.'+key:key;if(typeof value==='string'){(ui['admin.'+k]??={})[lang]=value;}else if(value&&typeof value==='object')flatten(value,k)}}flatten(data);
}
const content={ui,products,pages};
fs.writeFileSync(path.join(root,'backend/dracula-content.json'),JSON.stringify(content,null,2));
console.log('Prepared '+Object.keys(ui).length+' database translation keys, '+products.length+' products, '+pages.length+' pages.');
