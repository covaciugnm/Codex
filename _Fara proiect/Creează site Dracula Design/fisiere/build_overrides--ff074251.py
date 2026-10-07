"""Food editorial content, independent of the shared shop engine. UTF-8."""
import json
from pathlib import Path

def tri(ro, en, de):
    return dict(ro=ro, en=en, de=de)

ui = {}
def add(key, ro, en, de):
    ui[key] = tri(ro, en, de)

add('nav.collection', 'Selecția', 'The selection', 'Die Auswahl')
add('nav.story', 'Povestea noastră', 'Our story', 'Unsere Geschichte')
add('nav.universe', 'Dracula-Farm', 'Dracula-Farm', 'Dracula-Farm')
add('nav.bag', 'Coșul meu', 'My basket', 'Mein Warenkorb')
add('hero.eyebrow', 'DRACULA FOOD', 'DRACULA FOOD', 'DRACULA FOOD')
add('hero.title', 'Gust.', 'Taste.', 'Geschmack.')
add('hero.emphasis', 'Cu personalitate.', 'With character.', 'Mit Charakter.')
add('hero.description', 'O invitație la masa Dracula. O poveste despre gust, loc și bucuria de a împărți.', 'An invitation to the Dracula table. A story of taste, place and the pleasure of sharing.', 'Eine Einladung an den Dracula-Tisch. Eine Geschichte von Geschmack, Herkunft und der Freude am Teilen.')
add('hero.cta', 'Descoperă selecția', 'Discover the selection', 'Auswahl entdecken')
add('hero.motto', 'GUST. RĂGAZ. BUCURIE.', 'TASTE. PAUSE. ENJOY.', 'GENIESSEN. INNEHALTEN. TEILEN.')
add('hero.caption', 'DRACULA-FOOD.COM · DRACULA-FARM', 'DRACULA-FOOD.COM · DRACULA-FARM', 'DRACULA-FOOD.COM · DRACULA-FARM')
add('collection.eyebrow', 'SELECȚIA DRACULA FOOD', 'THE DRACULA FOOD SELECTION', 'DIE DRACULA FOOD AUSWAHL')
add('collection.title', 'Un gust.', 'A taste.', 'Ein Geschmack.')
add('collection.emphasis', 'O poveste de descoperit.', 'A story to discover.', 'Eine Geschichte zum Entdecken.')
add("collection.description", "Nuci și alune de pădure. Două selecții Dracula-Farm, prezentate cu aceeași atenție pentru detaliu.", "Walnuts and hazelnuts. Two Dracula-Farm selections, presented with the same attention to detail.", "Walnüsse und Haselnüsse. Zwei Dracula-Farm Auswahlen, präsentiert mit derselben Liebe zum Detail.")
add('collection.all', 'Toată selecția', 'All selections', 'Gesamte Auswahl')
add('collection.gourmet', 'Gusturi', 'Flavours', 'Geschmackswelten')
add('collection.pantry', 'Cămara', 'The pantry', 'Vorratskammer')
add('collection.gifts', 'De oferit', 'For sharing', 'Zum Verschenken')
add('collection.search', 'Caută un produs', 'Find a product', 'Produkt suchen')
add("collection.noresults", "Niciun produs nu corespunde selecției. Explorează întreaga colecție.", "No products match your selection. Explore the full collection.", "Keine Produkte entsprechen Ihrer Auswahl. Entdecken Sie die gesamte Kollektion.")
add('signature.eyebrow', 'LA MASA DRACULA', 'AT THE DRACULA TABLE', 'AM DRACULA-TISCH')
add('signature.title', 'Rafinamentul începe', 'Refinement begins', 'Raffinesse beginnt')
add('signature.emphasis', 'cu un moment simplu.', 'with a simple moment.', 'mit einem einfachen Moment.')
add('signature.body', 'O masă pregătită cu grijă. Un gust care rămâne în memorie. Timp pentru oamenii care contează.', 'A thoughtfully set table. A flavour that stays in the memory. Time for the people who matter.', 'Ein liebevoll gedeckter Tisch. Ein Geschmack, der in Erinnerung bleibt. Zeit für die Menschen, die wichtig sind.')
add('signature.more', 'Dracula Food aduce această stare de spirit în universul Dracula-Company. Un limbaj vizual discret, o identitate puternică și o invitație de a descoperi.', 'Dracula Food brings this spirit to the Dracula-Company universe. A restrained visual language, a distinctive identity and an invitation to discover.', 'Dracula Food bringt diesen Geist in die Welt von Dracula-Company. Eine ruhige Bildsprache, eine unverwechselbare Identität und eine Einladung zum Entdecken.')
add('universe.eyebrow', 'DRACULA-FARM', 'DRACULA-FARM', 'DRACULA-FARM')
add('universe.title', 'Un loc în poveste.', 'A place in the story.', 'Ein Ort in der Geschichte.')
add('universe.emphasis', 'Un loc la masă.', 'A place at the table.', 'Ein Platz am Tisch.')
add('universe.body', 'Dracula-Farm este locul care dă identitate proiectului Dracula Food. Fiecare produs va avea propria prezentare, cu informații clare despre compoziție și păstrare.', 'Dracula-Farm gives the Dracula Food project its sense of place. Each product will have its own presentation, with clear composition and storage information.', 'Dracula-Farm verleiht dem Projekt Dracula Food seinen örtlichen Bezug. Jedes Produkt erhält eine eigene Vorstellung mit klaren Angaben zu Zusammensetzung und Aufbewahrung.')
add('universe.motto', 'GUST. CARACTER. DRACULA.', 'TASTE. CHARACTER. DRACULA.', 'GESCHMACK. CHARAKTER. DRACULA.')
add('product.discover', 'Descoperă produsul', 'Discover the product', 'Produkt entdecken')
add('product.add', 'Adaugă în coș', 'Add to basket', 'In den Warenkorb')
add('product.care', 'Păstrare și consum', 'Storage and serving', 'Aufbewahrung und Verzehr')
add('product.caretext', 'Consultă eticheta și informațiile specifice produsului pentru ingrediente, alergeni, condiții de păstrare și termenul de consum.', 'Refer to the label and product-specific information for ingredients, allergens, storage conditions and the consumption date.', 'Beachten Sie das Etikett und die produktspezifischen Angaben zu Zutaten, Allergenen, Aufbewahrung und Verbrauchsdatum.')
add('product.details', 'Produs și ingrediente', 'Product and ingredients', 'Produkt und Zutaten')
add('product.code', 'Cod produs', 'Product reference', 'Artikelnummer')
add('product.related', 'De descoperit împreună', 'Discover together', 'Gemeinsam entdecken')
add('bag.empty', 'Prima alegere își așteaptă locul în coș.', 'Your first choice is waiting for a place in your basket.', 'Ihre erste Auswahl wartet auf einen Platz im Warenkorb.')
add('bag.added', 'Produsul a fost adăugat în coș.', 'The product has been added to your basket.', 'Das Produkt wurde zum Warenkorb hinzugefügt.')
add('favorites.title', 'Gusturi de păstrat aproape', 'Flavours to keep close', 'Geschmack zum Wiederentdecken')
add('favorites.empty', 'Păstrează aici produsele pe care vrei să le redescoperi.', 'Save the products you want to rediscover here.', 'Speichern Sie hier die Produkte, die Sie wiederentdecken möchten.')
add('favorites.saved', 'Produsul a fost salvat în favorite.', 'The product has been saved to favourites.', 'Das Produkt wurde auf der Merkliste gespeichert.')
add('favorites.removed', 'Produsul a fost eliminat din favorite.', 'The product has been removed from favourites.', 'Das Produkt wurde von der Merkliste entfernt.')
add('account.intro', 'Selecția ta, comenzile tale și povestea Dracula Food, într-un singur loc.', 'Your selection, your orders and the Dracula Food story, in one place.', 'Ihre Auswahl, Ihre Bestellungen und die Dracula Food Geschichte an einem Ort.')
add('auth.newaccount', 'Primul pas în universul Dracula Food.', 'Your first step into the Dracula Food universe.', 'Ihr erster Schritt in die Dracula Food Welt.')

pages = {}
pages['about'] = {'body': tri(
    'Dracula Food este proiectul dedicat gustului din universul Dracula-Company. Identitatea sa începe la Dracula-Farm și se exprimă printr-un stil sobru: negru, accente roșii și detalii aurii.\n\nNe propunem o experiență în care descoperirea produsului este la fel de îngrijită ca prezentarea lui. Compoziția, alergenii, cantitatea și condițiile de păstrare vor fi prezentate pentru fiecare produs.\n\nPrima selecție se află în pregătire. Produsele vor fi publicate după adăugarea imaginilor și verificarea informațiilor specifice.',
    'Dracula Food is the project devoted to taste within the Dracula-Company universe. Its identity begins at Dracula-Farm and is expressed through a restrained style: black, red accents and golden details.\n\nWe aim for an experience in which discovering a product receives the same care as its presentation. Composition, allergens, quantity and storage conditions will be provided for each product.\n\nThe first selection is being prepared. Products will be published after their images and specific information have been supplied and checked.',
    'Dracula Food ist das dem Geschmack gewidmete Projekt in der Welt von Dracula-Company. Seine Identität beginnt bei Dracula-Farm und zeigt sich in einem ruhigen Stil: Schwarz, rote Akzente und goldene Details.\n\nWir möchten, dass die Entdeckung eines Produkts ebenso sorgfältig gestaltet ist wie seine Präsentation. Zusammensetzung, Allergene, Menge und Aufbewahrung werden für jedes Produkt angegeben.\n\nDie erste Auswahl wird vorbereitet. Produkte werden veröffentlicht, sobald Bilder und produktspezifische Informationen vorliegen und geprüft sind.')}
pages['returns'] = {'body': tri(
    'Dreptul de retragere și procedura de retur depind de natura produsului. Bunurile susceptibile să se deterioreze sau să expire rapid pot fi exceptate de la dreptul de retragere. Aceasta nu înlătură drepturile aplicabile pentru produse neconforme.\n\nPentru o problemă la primire, menționează comanda, produsul și situația observată prin formularul de reclamații. Urmează condițiile de păstrare de pe etichetă.\n\nAdresa completă pentru retur, costurile și procedura de rambursare vor fi confirmate înainte de vânzare. Dracula-Farm este reperul furnizat pentru proiect și nu este încă o adresă poștală completă.',
    'Withdrawal rights and return procedures depend on the nature of the product. Goods liable to deteriorate or expire rapidly may be excluded from the withdrawal right. This does not remove applicable rights for non-conforming products.\n\nFor an issue on receipt, use the complaints form and include the order, product and issue observed. Follow the storage conditions on the label.\n\nThe complete return address, costs and refund procedure will be confirmed before sales begin. Dracula-Farm is the project location reference supplied and is not yet a complete postal address.',
    'Widerrufsrecht und Rückgabeverfahren hängen von der Art des Produkts ab. Schnell verderbliche Waren oder Waren mit rasch überschrittenem Verfallsdatum können vom Widerrufsrecht ausgenommen sein. Rechte bei nicht vertragsgemäßen Produkten bleiben unberührt.\n\nMelden Sie Probleme bei Erhalt über das Beschwerdeformular mit Bestellung, Produkt und Beschreibung. Beachten Sie die Aufbewahrungshinweise auf dem Etikett.\n\nVollständige Rücksendeadresse, Kosten und Erstattungsverfahren werden vor Verkaufsbeginn bestätigt. Dracula-Farm ist der angegebene Projektstandort und noch keine vollständige Postanschrift.')}
pages['faq'] = {'body': tri(
    'Unde găsesc ingredientele și alergenii?\nÎn prezentarea fiecărui produs și pe eticheta acestuia, după publicarea selecției.\n\nCum păstrez produsele?\nUrmează condițiile specifice indicate pe etichetă. Nu toate produsele alimentare au aceleași cerințe.\n\nCum salvez un produs?\nFolosește simbolul de favorite. Selecția este păstrată în cont.\n\nPot comanda acum?\nCatalogul este în pregătire. Magazinul rulează în mod de prezentare, fără încasări reale.',
    'Where can I find ingredients and allergens?\nIn each product presentation and on its label once the selection is published.\n\nHow should products be stored?\nFollow the specific conditions on the label. Food products do not all share the same requirements.\n\nHow do I save a product?\nUse the favourites symbol. Your selection is saved in your account.\n\nCan I order now?\nThe catalogue is being prepared. The store runs in preview mode without real payments.',
    'Wo finde ich Zutaten und Allergene?\nNach Veröffentlichung der Auswahl in der jeweiligen Produktbeschreibung und auf dem Etikett.\n\nWie bewahre ich Produkte auf?\nBeachten Sie die produktspezifischen Angaben auf dem Etikett. Lebensmittel haben unterschiedliche Anforderungen.\n\nWie speichere ich ein Produkt?\nNutzen Sie das Merkliste-Symbol. Ihre Auswahl wird im Konto gespeichert.\n\nKann ich schon bestellen?\nDer Katalog wird vorbereitet. Der Shop läuft im Vorschaumodus ohne echte Zahlungen.')}

overlay = {
    'brand': {'name': 'Dracula Food', 'full_name': 'Dracula Food', 'domain': 'dracula-food.com', 'company': 'Dracula-Company', 'address': 'Dracula-Farm', 'logo': '/assets/brand/dracula-food-logo.jpeg'},
    'categories': [['gourmet', tri('Gusturi', 'Flavours', 'Geschmackswelten')], ['pantry', tri('Cămara', 'The pantry', 'Vorratskammer')], ['gifts', tri('De oferit', 'For sharing', 'Zum Verschenken')], ['stafide-naturale', tri('Stafide naturale & soiuri', 'Natural raisins & varieties', 'Naturrosinen & Sorten')], ['stafide-aromatizate', tri('Stafide aromatizate & infuzate', 'Flavoured & infused raisins', 'Aromatisierte & verfeinerte Rosinen')]],
    'images': {"hero":"/assets/brand/dracula-food-logo.jpeg","collection":"/assets/produse/dracula-food-nuci-dracula-farm.png","scarf":"/assets/produse/dracula-food-alune-de-padure-dracula-farm.png"},
    'ui': ui, 'pages': pages,
    'sources': ['https://food.ec.europa.eu/food-safety/labelling-and-nutrition/food-information-consumers-legislation/distance-selling_en', 'https://europa.eu/youreurope/citizens/consumers/shopping/returns/indexamp_en.htm']
}
(Path(__file__).parent/'overrides.json').write_text(json.dumps(overlay, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
