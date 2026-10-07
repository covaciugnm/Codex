const fs = require('fs');
const path = require('path');
const out = path.resolve('outputs/dracula-design-office/design');
fs.mkdirSync(out, {recursive:true});
const langs=['ro','en','de'];
const sources=[
 {id:'fjallraven-kanken',title:'Fjällräven — Kånken: A history',url:'https://experience.fjallraven.com/us/en-us/blog/kanken-invention-history'},
 {id:'vam-bags',title:'Victoria and Albert Museum — Bags: Inside Out',url:'https://www.vam.ac.uk/exhibitions/bags'},
 {id:'williamsburg-pocketbook',title:'Colonial Williamsburg — Pocketbook, 1794, object 2024-344',url:'https://emuseum.colonialwilliamsburg.org/objects/113465/pocketbook'},
 {id:'llbean-tote',title:'L.L.Bean — How the 1944 Ice Carrier Became America’s Go-To Tote',url:'https://www.llbean.com/llb/shop/518259?page=newsroom-tbd-08'},
 {id:'hermes-scarf',title:'Hermès — Par un beau soir de carrés…',url:'https://www.hermes.com/be/en/content/323861-thesilkyway-stories/'}
].map(x=>({...x,accessed_at:'2026-09-25',type:'primary'}));
const labels={
 appearance:['Aspect observabil în imagine','Visible appearance in the image','Sichtbare Gestaltung im Bild'],
 material:['Material și compoziție','Material and composition','Material und Zusammensetzung'],
 dimensions:['Dimensiuni','Dimensions','Maße'],
 weight:['Greutate netă','Net weight','Nettogewicht'],
 lining:['Căptușeală','Lining','Futter'],
 closure:['Închidere','Closure','Verschluss'],
 capacity:['Capacitate și compatibilitate','Capacity and compatibility','Volumen und Kompatibilität'],
 hardware:['Accesorii și finisaje','Hardware and finishes','Beschläge und Oberflächen'],
 care:['Îngrijire','Care','Pflege'],
 origin:['Origine și fabricație','Origin and manufacture','Herkunft und Herstellung'],
 included:['Conținutul livrării','What is included','Lieferumfang']
};
const pending={
 material:['În așteptarea fișei producătorului. Fotografia nu confirmă pielea naturală, specia, proveniența sau compoziția materialului.','Awaiting the manufacturer’s specification. The photograph does not verify genuine leather, species, provenance or material composition.','Herstellerangaben stehen aus. Das Foto bestätigt weder echtes Leder noch Tierart, Herkunft oder Materialzusammensetzung.'],
 dimensions:['În așteptarea măsurătorilor produsului finit, în centimetri.','Final-product measurements in centimetres are pending.','Maße des fertigen Produkts in Zentimetern stehen aus.'],
 weight:['În așteptarea cântăririi produsului fără ambalaj.','Product weight without packaging is pending.','Gewicht des Produkts ohne Verpackung steht aus.'],
 lining:['Materialul, culoarea și structura căptușelii trebuie confirmate de producător.','Lining material, colour and construction require manufacturer confirmation.','Material, Farbe und Aufbau des Futters müssen vom Hersteller bestätigt werden.'],
 hardware:['Compoziția, furnizorul și tratamentul componentelor nu sunt confirmate.','Component composition, supplier and surface treatment are unconfirmed.','Material, Lieferant und Oberflächenbehandlung der Beschläge sind unbestätigt.'],
 origin:['Țara de fabricație și originea materialelor sunt în așteptarea documentelor furnizorului. Mențiunile din vizual nu constituie o verificare.','Country of manufacture and material origin await supplier documentation. Claims shown in the visual have not been independently verified.','Herstellungsland und Materialherkunft erfordern Lieferantenunterlagen. Aussagen im Bild sind nicht unabhängig bestätigt.'],
 included:['Produsul listat; ambalajul și eventualele accesorii incluse trebuie confirmate. Obiectele de decor din fotografie nu sunt incluse implicit.','The listed product; packaging and any included accessories require confirmation. Styling props in the photograph are not automatically included.','Der aufgeführte Artikel; Verpackung und enthaltenes Zubehör müssen bestätigt werden. Dekorationsobjekte im Foto gehören nicht automatisch zum Lieferumfang.'],
 care:['Protocolul specific de curățare este în așteptarea confirmării materialului și a etichetei de întreținere.','The specific cleaning procedure awaits confirmation of the material and care label.','Die genaue Reinigung richtet sich nach noch zu bestätigendem Material und Pflegeetikett.']
};
const baseCare=[
 'Până la confirmarea materialului, păstrează piesa într-un loc uscat, ferit de soare și căldură directă. Nu aplica solvenți, alcool, creme pentru piele sau tratamente de impermeabilizare fără acordul producătorului. Evită supraîncărcarea și contactul cu obiecte ascuțite. Curățarea și eventualele reparații se stabilesc după eticheta finală de întreținere.',
 'Until the material is confirmed, keep the piece in a dry place away from direct sunlight and heat. Do not apply solvents, alcohol, leather conditioners or waterproofing products without manufacturer approval. Avoid overfilling and contact with sharp objects. Cleaning and repairs must follow the final care label.',
 'Bis zur Bestätigung des Materials trocken sowie vor direkter Sonne und Wärme geschützt aufbewahren. Ohne Freigabe des Herstellers keine Lösungsmittel, Alkohol, Lederpflege oder Imprägniermittel auftragen. Überfüllung und Kontakt mit scharfen Gegenständen vermeiden. Reinigung und Reparaturen richten sich nach dem endgültigen Pflegeetikett.'
];
const rows=[];
function product(id, intro, appearance, closure, capacity, history, source, story, styling, extra={}){
 const content={};
 langs.forEach((lang,i)=>{
  const specs={...pending,appearance,closure,capacity,...extra};
  content[lang]={intro:intro[i],technical:Object.keys(labels).map(key=>({key,label:labels[key][i],value:specs[key][i],status:key==='appearance'?'visual_reference':'pending_confirmation'})),care:(extra.careText||baseCare)[i],history:{text:history[i],source_ids:[source]},brand_story:story[i],brand_story_type:'editorial',styling:styling.map(s=>({title:s[0][i],pieces:s[1][i],occasion:s[2][i],instructions:s[3][i]}))};
 });
 rows.push({id,content});
}
product('rucsac-business',[
 'O arhitectură verticală în negru, conturată de cusături roșii și o monogramă tonală discretă. Rucsacul Business propune o prezență ordonată pentru ziua dintre birou și oraș. Imaginea de prezentare arată un mâner superior, bretele și o deschidere amplă cu fermoar; configurația finală se confirmă prin fișa producătorului.',
 'A vertical black silhouette outlined by red stitching and a discreet tonal monogram. The Business Backpack brings visual order to the journey between office and city. The presentation image shows a top handle, shoulder straps and a broad zip opening; the final configuration requires the manufacturer’s specification.',
 'Eine aufrechte schwarze Silhouette, umrissen von roten Nähten und einem dezenten, tonalen Monogramm. Der Business-Rucksack setzt einen klaren Akzent zwischen Büro und Stadt. Das Präsentationsbild zeigt Tragegriff, Schultergurte und eine weit verlaufende Reißverschlussöffnung; die endgültige Ausführung muss der Hersteller bestätigen.'
],[
 'Corp negru cu aspect granulat, contur dreptunghiular cu colțuri rotunjite, cusături roșii, monogramă închisă la culoare; observații din vizual.',
 'Black body with a grained appearance, rounded rectangular outline, red stitching and dark monogram; observations from the visual.',
 'Schwarzer Korpus mit genarbter Optik, rechteckiger Form mit abgerundeten Ecken, roten Nähten und dunklem Monogramm; Beobachtungen am Bild.'
],[
 'Fermoare vizibile în imagine. Tipul, numărul cursorelor și rezistența la apă nu sunt confirmate.',
 'Zips are visible in the image. Type, number of sliders and water resistance are unconfirmed.',
 'Reißverschlüsse sind im Bild sichtbar. Ausführung, Anzahl der Schieber und Wasserbeständigkeit sind unbestätigt.'
],[
 'Volumul, sarcina maximă, dimensiunea compartimentelor și compatibilitatea cu laptopuri sunt în așteptare; dispozitivele din fotografie nu dovedesc o diagonală compatibilă.',
 'Volume, maximum load, compartment dimensions and laptop fit are pending; devices pictured do not establish a compatible screen size.',
 'Volumen, Höchstbelastung, Fachmaße und Laptop-Kompatibilität stehen aus; abgebildete Geräte belegen keine passende Bildschirmdiagonale.'
],[
 'Un reper documentat al rucsacului cotidian este Kånken: Fjällräven relatează că modelul a fost produs pentru anul școlar 1978, în colaborare cu asociația suedeză de cercetași. Este un exemplu de design pornit de la nevoile zilnice, nu originea tuturor rucsacurilor și nici istoria produsului Dracula.',
 'One documented milestone in the everyday backpack is Kånken: Fjällräven records its production for the 1978 school year with the Swedish Guide and Scout Association. It illustrates design shaped by daily needs, rather than the origin of all backpacks or the history of the Dracula product.',
 'Ein dokumentierter Meilenstein des Alltagsrucksacks ist Kånken: Laut Fjällräven entstand er zum Schuljahr 1978 gemeinsam mit dem schwedischen Pfadfinderverband. Er veranschaulicht alltagsbezogenes Design, ist aber weder der Ursprung sämtlicher Rucksäcke noch Teil der Geschichte des Dracula-Produkts.'
],'fjallraven-kanken',[
 'Poveste editorială Dracula: dimineața începe între ziduri întunecate și o lumină subțire de roșu. Linia cusăturii devine traseul unei zile cu destinații precise. Rucsacul este imaginat ca o mică arhitectură personală: calm la exterior, aproape de lucrurile care contează.',
 'Dracula editorial story: morning begins between dark walls and a fine line of red light. The stitching becomes the route of a day with clear destinations. The backpack is imagined as personal architecture: composed on the outside, close to what matters.',
 'Redaktionelle Dracula-Geschichte: Der Morgen beginnt zwischen dunklen Mauern und einem schmalen roten Lichtstreifen. Die Naht wird zum Weg eines Tages mit klaren Zielen. Der Rucksack erscheint als persönliche Architektur: außen ruhig, den wichtigen Dingen nah.'
],[
 [['Arhitectură urbană','Urban architecture','Urbane Architektur'],['Palton antracit, helancă neagră, pantaloni drepți, ghete negre.','Charcoal coat, black roll-neck, straight trousers and black boots.','Anthrazitfarbener Mantel, schwarzer Rollkragenpullover, gerade Hose und schwarze Stiefel.'],['Întâlnire creativă și galerie de artă.','Creative meeting and gallery visit.','Kreativtermin und Galeriebesuch.'],['Păstrează ținuta monocromă și lasă cusăturile roșii să fie singurul accent. Reglează bretelele după instrucțiunile produsului final.','Keep the outfit monochrome and let the red stitching supply the only colour accent. Adjust the straps according to the final product instructions.','Das Outfit monochrom halten und die roten Nähte als einzigen Farbakzent einsetzen. Die Gurte nach der endgültigen Produktanleitung einstellen.']],
 [['Weekend la castel','Castle weekend','Wochenende am Schloss'],['Jachetă neagră simplă, tricot crem, pantaloni cărbune, pantofi confortabili.','Plain black jacket, cream knitwear, charcoal trousers and comfortable shoes.','Schlichte schwarze Jacke, cremefarbener Strick, anthrazitfarbene Hose und bequeme Schuhe.'],['Plimbare urbană și escapadă de weekend.','City walk and weekend escape.','Stadtspaziergang und Wochenendausflug.'],['Alege straturi curate și puține accesorii. Verifică separat capacitatea și limita de încărcare înainte de a pregăti bagajul.','Choose clean layers and few accessories. Check capacity and load limits separately before packing.','Klare Lagen und wenige Accessoires wählen. Volumen und Belastungsgrenze vor dem Packen gesondert prüfen.']]
]);
product('servieta-business',[
 'O siluetă orizontală, precisă, în care negrul și roșul se întâlnesc la marginea fiecărui detaliu. Servieta Business pune accentul pe proporție și pe gestul de a purta un obiect bine definit. Vizualul arată două mânere, o baretă și un buzunar frontal; specificațiile funcționale rămân de confirmat.',
 'A precise horizontal silhouette where black meets red at the edge of each detail. The Business Briefcase centres on proportion and the gesture of carrying a clearly defined object. The visual shows twin handles, a shoulder strap and a front pocket; functional specifications remain to be confirmed.',
 'Eine präzise horizontale Silhouette, bei der Schwarz und Rot an den Konturen zusammentreffen. Die Business-Aktentasche betont Proportion und den bewussten Griff zu einem klar gestalteten Objekt. Das Bild zeigt zwei Griffe, einen Schulterriemen und eine Fronttasche; funktionale Angaben stehen noch aus.'
],[
 'Format dreptunghiular negru, textură cu aspect granulat, mânere duble, baretă neagră și cusături roșii; descriere a imaginii.',
 'Black rectangular shape, grained visual texture, twin handles, black strap and red stitching; image description.',
 'Schwarze rechteckige Form, genarbte Optik, zwei Griffe, schwarzer Riemen und rote Nähte; Bildbeschreibung.'
],[
 'Vizualul arată un fermoar superior și o închidere cu fermoar la buzunarul frontal. Configurația și componentele finale sunt în așteptare.',
 'The visual shows a top zip and a zipped front pocket. Final configuration and components are pending.',
 'Das Bild zeigt einen oberen Reißverschluss und eine Fronttasche mit Reißverschluss. Endgültige Ausführung und Komponenten stehen aus.'
],[
 'Compatibilitatea A4, diagonala laptopului, protecția compartimentului și sarcina admisă trebuie măsurate și confirmate. Nu sunt deduse din obiectele de decor.',
 'A4 fit, laptop size, compartment protection and load rating require measurement and confirmation. They are not inferred from styling props.',
 'Eignung für A4, Laptop-Größe, Fachpolsterung und Traglast müssen gemessen und bestätigt werden. Sie werden nicht aus Dekorationsobjekten abgeleitet.'
],[
 'Expoziția V&A Bags: Inside Out a inclus o cutie pentru documente a lui Winston Churchill, realizată de John Peck & Son în jurul anului 1921. Obiectul oferă un reper concret pentru relația dintre transportul documentelor și imaginea publică. Această referință culturală nu reprezintă proveniența servietei Dracula.',
 'The V&A exhibition Bags: Inside Out included Winston Churchill’s despatch box, made by John Peck & Son around 1921. It offers a concrete reference for the relationship between carrying documents and public image. This cultural reference does not describe the provenance of the Dracula briefcase.',
 'Die V&A-Ausstellung Bags: Inside Out zeigte Winston Churchills Dokumentenkasten von John Peck & Son, datiert um 1921. Er ist ein konkretes Beispiel für die Verbindung zwischen Dokumententransport und öffentlichem Auftreten. Dieser kulturgeschichtliche Bezug beschreibt nicht die Herkunft der Dracula-Aktentasche.'
],'vam-bags',[
 'Poveste editorială Dracula: o masă de piatră, o scrisoare și câteva decizii importante. Roșul urmărește geometria neagră ca o semnătură finală. Servieta devine, în universul vizual al colecției, ritualul dintre pregătire și prezență.',
 'Dracula editorial story: a stone table, a letter and a few important decisions. Red follows the black geometry like a final signature. In the collection’s visual world, the briefcase becomes the ritual between preparation and presence.',
 'Redaktionelle Dracula-Geschichte: ein Steintisch, ein Brief und einige wichtige Entscheidungen. Rot folgt der schwarzen Geometrie wie eine abschließende Unterschrift. In der Bildwelt der Kollektion wird die Aktentasche zum Ritual zwischen Vorbereitung und Auftritt.'
],[
 [['Consiliu de seară','Evening boardroom','Sitzung am Abend'],['Costum antracit, cămașă albă, pantofi negri, ceas discret.','Charcoal suit, white shirt, black shoes and a discreet watch.','Anthrazitfarbener Anzug, weißes Hemd, schwarze Schuhe und dezente Uhr.'],['Prezentare, conferință sau întâlnire formală.','Presentation, conference or formal meeting.','Präsentation, Konferenz oder formeller Termin.'],['Poartă servieta de mânere pentru o linie clară. Repetă roșul cel mult într-un detaliu mic, precum o batistă de buzunar.','Carry the briefcase by its handles for a clean line. Repeat red in no more than one small detail, such as a pocket square.','Die Aktentasche für eine klare Linie an den Griffen tragen. Rot höchstens in einem kleinen Detail wie einem Einstecktuch wiederholen.']],
 [['Atelier și oraș','Studio and city','Atelier und Stadt'],['Sacou negru nestructurat, tricou crem, pantaloni gri și loafers.','Unstructured black blazer, cream T-shirt, grey trousers and loafers.','Unstrukturierter schwarzer Blazer, cremefarbenes T-Shirt, graue Hose und Loafer.'],['Întâlnire de design și cină după birou.','Design meeting and after-work dinner.','Designtermin und Abendessen nach der Arbeit.'],['Lasă textura vizuală a servietei să contrasteze cu suprafețe mate. Bareta se folosește numai în configurația confirmată a produsului.','Let the briefcase’s visible texture contrast with matte surfaces. Use the shoulder strap only in the confirmed product configuration.','Die sichtbare Taschenstruktur mit matten Flächen kombinieren. Den Schulterriemen nur entsprechend der bestätigten Produktausführung verwenden.']]
]);
product('portofel-signature',[
 'Un dreptunghi negru, o linie roșie continuă și o monogramă aproape tăcută. Portofelul Signature concentrează limbajul colecției într-un obiect personal. Imaginea arată formatul pliabil și compartimente pentru carduri; numărul și dimensiunile lor vor fi confirmate prin fișa tehnică.',
 'A black rectangle, a continuous red line and an almost silent monogram. The Signature Wallet concentrates the collection’s language into a personal object. The image shows a folding format and card slots; their number and dimensions await the technical specification.',
 'Ein schwarzes Rechteck, eine durchgehende rote Linie und ein beinahe stilles Monogramm. Das Signature-Portemonnaie verdichtet die Gestaltung der Kollektion zu einem persönlichen Objekt. Das Bild zeigt ein Faltformat und Kartenfächer; Anzahl und Maße werden erst durch das technische Datenblatt bestätigt.'
],[
 'Format pliabil în două, suprafață neagră cu aspect granulat, cusături roșii perimetrale și monogramă tonală; observate în imagine.',
 'Bifold appearance, black grained-looking surface, red perimeter stitching and tonal monogram; observed in the image.',
 'Zweifach gefaltete Form, schwarz genarbte Optik, umlaufende rote Nähte und tonales Monogramm; im Bild beobachtet.'
],[
 'Formatul se pliază în imagine; un mecanism suplimentar de închidere nu este confirmat.',
 'The pictured format folds; an additional fastening mechanism is not confirmed.',
 'Das gezeigte Format wird gefaltet; ein zusätzlicher Verschluss ist nicht bestätigt.'
],[
 'Numărul final de sloturi, tipul bancnotelor compatibile și dimensiunile utile sunt în așteptare. Nu este confirmată protecție RFID.',
 'Final slot count, banknote compatibility and usable dimensions are pending. RFID protection is not confirmed.',
 'Endgültige Fachanzahl, Banknoten-Kompatibilität und nutzbare Maße stehen aus. RFID-Schutz ist nicht bestätigt.'
],[
 'Colonial Williamsburg păstrează un portofel brodat datat 1794. Fișa muzeului arată că astfel de obiecte păstrau bani, hârtii și mici accesorii și puteau fi personalizate cu inițiale. Este o mărturie despre caracterul personal al portofelului, nu o filiație a modelului Signature.',
 'Colonial Williamsburg holds an embroidered pocketbook dated 1794. Its record explains that such objects held money, papers and small accessories and could carry personal initials. It documents the wallet’s personal character, rather than a lineage for the Signature model.',
 'Colonial Williamsburg bewahrt eine bestickte Brieftasche von 1794. Laut Museumsbeschreibung dienten solche Stücke Geld, Papieren und kleinen Accessoires und trugen oft persönliche Initialen. Das belegt den persönlichen Charakter dieser Objektgattung, nicht eine Abstammung des Signature-Modells.'
],'williamsburg-pocketbook',[
 'Poveste editorială Dracula: unele lucruri nu au nevoie să fie expuse. O monogramă descoperită de aproape, un contur roșu care apare pentru o clipă, apoi dispare în buzunar. Signature vorbește despre alegerea atentă a obiectelor pe care le atingi în fiecare zi.',
 'Dracula editorial story: some things do not need to be displayed. A monogram discovered close up, a red outline visible for a moment before returning to a pocket. Signature speaks of choosing carefully the objects you touch every day.',
 'Redaktionelle Dracula-Geschichte: Manche Dinge müssen nicht ausgestellt werden. Ein Monogramm, das erst aus der Nähe auffällt, ein roter Umriss, der kurz erscheint und wieder in der Tasche verschwindet. Signature erzählt von bewusst ausgewählten Alltagsobjekten.'
],[
 [['Semnătură de business','Business signature','Business-Signatur'],['Servietă neagră, costum gri închis, cămașă albă.','Black briefcase, dark grey suit and white shirt.','Schwarze Aktentasche, dunkelgrauer Anzug und weißes Hemd.'],['Zi de birou și întâlniri.','Office day and meetings.','Bürotag und Besprechungen.'],['Asociază portofelul cu o singură piesă din aceeași paletă. Păstrează strictul necesar pentru a evita deformarea prin supraîncărcare.','Pair the wallet with one piece in the same palette. Carry only essentials to avoid distortion from overfilling.','Das Portemonnaie mit einem Stück derselben Farbwelt kombinieren. Nur das Nötigste mitnehmen, um Verformung durch Überfüllung zu vermeiden.']],
 [['Nocturn minimalist','Minimalist nocturne','Minimalistisches Nocturne'],['Sacou negru, tricot fin, pantaloni drepți și pantofi simpli.','Black blazer, fine knitwear, straight trousers and simple shoes.','Schwarzer Blazer, feiner Strick, gerade Hose und schlichte Schuhe.'],['Cină sau spectacol.','Dinner or a performance.','Abendessen oder Theaterbesuch.'],['Lasă portofelul să fie accentul discret al gestului, fără alte accesorii roșii dominante. Verifică dimensiunea buzunarului înainte de purtare.','Let the wallet provide a discreet accent without other dominant red accessories. Check pocket dimensions before carrying.','Das Portemonnaie als dezenten Akzent ohne weitere dominante rote Accessoires einsetzen. Vor dem Tragen die Taschenmaße prüfen.']]
]);
product('geanta-tote',[
 'Negrul formează centrul compoziției, iar roșul desenează mânerele și lateralele. Geanta Tote aduce un contrast amplu, cu o siluetă structurată și monogramă discretă în imagine. Fotografia prezintă un univers de accesorii coordonate; pagina se referă exclusiv la geanta Tote, nu la întregul set.',
 'Black anchors the composition while red defines the handles and sides. The Signature Tote makes a broad contrast, with a structured silhouette and discreet monogram in the image. The photograph presents a coordinated accessories world; this listing is for the tote alone, not the entire set.',
 'Schwarz bildet das Zentrum, Rot zeichnet Griffe und Seiten nach. Die Signature-Tote setzt einen ausdrucksstarken Kontrast mit strukturierter Silhouette und dezentem Monogramm im Bild. Das Foto zeigt eine abgestimmte Accessoire-Welt; dieses Angebot bezieht sich ausschließlich auf die Tote, nicht auf das gesamte Set.'
],[
 'Geantă mare din centrul imaginii: corp negru, laterale și mânere roșii, element suspendat cu monogramă. Celelalte obiecte sunt elemente de prezentare.',
 'Large central bag in the image: black body, red sides and handles, hanging monogram detail. Other objects are presentation elements.',
 'Große Tasche in der Bildmitte: schwarzer Korpus, rote Seiten und Griffe sowie Anhänger mit Monogramm. Die übrigen Gegenstände dienen der Präsentation.'
],[
 'Tipul închiderii principale nu poate fi stabilit sigur din fotografia disponibilă; în așteptarea confirmării.',
 'The main closure cannot be established reliably from the available photograph; confirmation is pending.',
 'Der Hauptverschluss lässt sich aus dem verfügbaren Foto nicht zuverlässig bestimmen; Bestätigung steht aus.'
],[
 'Dimensiunile interioare, volumul, lungimea mânerelor, sarcina admisă și compatibilitatea cu documente sau dispozitive sunt în așteptare.',
 'Interior dimensions, volume, handle drop, load limit and document or device compatibility are pending.',
 'Innenmaße, Volumen, Griffhöhe, Traglast sowie Eignung für Dokumente oder Geräte stehen aus.'
],[
 'Un episod documentat din istoria tote-ului: L.L.Bean a lansat în 1944 o geantă pentru transportul gheții, revenită în 1965 sub numele Boat and Tote. Acest traseu de la utilitate la accesoriu cotidian oferă context cultural; nu indică originea sau construcția genții Dracula.',
 'A documented chapter in tote history: L.L.Bean introduced an ice-carrying bag in 1944, returning in 1965 as the Boat and Tote. That journey from utility to everyday accessory offers cultural context; it does not establish the origin or construction of the Dracula bag.',
 'Ein dokumentiertes Kapitel der Tote-Geschichte: L.L.Bean führte 1944 eine Tasche zum Transport von Eis ein, die 1965 als Boat and Tote zurückkehrte. Dieser Weg vom Nutzgegenstand zum Alltagsaccessoire bietet kulturellen Kontext, belegt aber weder Herkunft noch Konstruktion der Dracula-Tasche.'
],'llbean-tote',[
 'Poveste editorială Dracula: o intrare în hol, un palton negru, un buchet de trandafiri roșii. Tote transformă contrastul în prezență. Silueta este imaginată pentru cineva care intră într-o încăpere cu o direcție proprie și lasă detaliile să vorbească încet.',
 'Dracula editorial story: a hall entrance, a black coat and a bouquet of red roses. The Tote turns contrast into presence. Its silhouette is imagined for someone who enters a room with their own direction and lets the details speak softly.',
 'Redaktionelle Dracula-Geschichte: ein Eingang in die Halle, ein schwarzer Mantel, ein Strauß roter Rosen. Die Tote verwandelt Kontrast in Präsenz. Ihre Silhouette steht für jemanden, der mit eigener Richtung einen Raum betritt und Details leise sprechen lässt.'
],[
 [['Vernisaj în roșu și negru','Red-and-black vernissage','Vernissage in Rot und Schwarz'],['Rochie midi neagră, pantofi negri, cercei mici aurii.','Black midi dress, black shoes and small gold-coloured earrings.','Schwarzes Midikleid, schwarze Schuhe und kleine goldfarbene Ohrringe.'],['Vernisaj sau recepție.','Gallery opening or reception.','Vernissage oder Empfang.'],['Păstrează geanta ca principal accent cromatic. Limitează metalul auriu la un detaliu mic pentru echilibru.','Keep the bag as the main colour accent. Limit gold-coloured metal to one small detail for balance.','Die Tasche als Hauptfarbakzent einsetzen. Goldfarbenes Metall für ein ausgewogenes Bild auf ein kleines Detail beschränken.']],
 [['Oraș, după ploaie','City after rain','Stadt nach dem Regen'],['Trenci bej, cămașă albă, pantaloni negri și loafers.','Beige trench, white shirt, black trousers and loafers.','Beiger Trenchcoat, weißes Hemd, schwarze Hose und Loafer.'],['Întâlnire de zi și plimbare urbană.','Daytime meeting and city walk.','Tagestermin und Stadtspaziergang.'],['Folosește bejul ca fundal calm pentru roșu. Titlul ținutei descrie atmosfera; nu presupune că geanta este impermeabilă. Protejeaz-o de umezeală.','Use beige as a quiet backdrop for red. The look’s title describes a mood, not waterproof performance. Protect the bag from moisture.','Beige als ruhigen Hintergrund für Rot nutzen. Der Titel beschreibt eine Stimmung, keine Wasserdichtigkeit. Die Tasche vor Feuchtigkeit schützen.']]
]);
product('esarfa-signature',[
 'Benzi roșii și negre, reflexii satinate și o monogramă așezată la margine. Eșarfa Signature aduce mișcare într-o garderobă cu linii precise. Vizualul sugerează un drapaj fluid; compoziția fibrelor, dimensiunea și tehnica de finisare nu pot fi stabilite doar din fotografie.',
 'Red and black bands, a satin-like sheen and a monogram near the edge. The Signature Scarf introduces movement into a wardrobe of precise lines. The visual suggests a fluid drape; fibre composition, size and finishing technique cannot be established from the photograph alone.',
 'Rote und schwarze Flächen, satinartiger Glanz und ein Monogramm am Rand. Der Signature-Schal bringt Bewegung in eine Garderobe klarer Linien. Das Bild vermittelt einen fließenden Fall; Faserzusammensetzung, Maße und Verarbeitung lassen sich daraus allein nicht bestimmen.'
],[
 'Suprafață cu aspect lucios, contrast roșu-negru, monogramă și margine conturată; observații vizuale, fără confirmarea fibrei.',
 'Glossy-looking surface, red-black contrast, monogram and defined edge; visual observations without fibre verification.',
 'Glänzende Optik, Rot-Schwarz-Kontrast, Monogramm und betonte Kante; visuelle Beobachtungen ohne Faserbestätigung.'
],[
 'Nu este vizibil un sistem mecanic de închidere. Modalitățile de înnodare depind de dimensiunile și materialul final.',
 'No mechanical fastening is visible. Knotting options depend on final dimensions and material.',
 'Kein mechanischer Verschluss ist sichtbar. Knotentechniken hängen von den endgültigen Maßen und dem Material ab.'
],[
 'Nu se aplică o capacitate de transport. Lungimea, lățimea și utilizările prin înnodare sunt în așteptarea măsurătorilor.',
 'Carrying capacity is not applicable. Length, width and knotting options await measurement.',
 'Ein Transportvolumen ist nicht anwendbar. Länge, Breite und mögliche Knotentechniken erfordern die endgültigen Maße.'
],[
 'În istoria eșarfei imprimate, Hermès datează din 1937 începutul propriilor carrés și le descrie ca suporturi pentru culoare, imagine și poveste. Este un reper al accesoriului ca suprafață narativă; nu afirmă că Hermès a inventat eșarfa și nu sugerează o legătură cu Dracula.',
 'In the history of printed scarves, Hermès dates its own carrés to 1937 and presents them as spaces for colour, imagery and narrative. This is a reference for the accessory as a storytelling surface; it neither credits Hermès with inventing scarves nor implies a connection with Dracula.',
 'In der Geschichte bedruckter Tücher datiert Hermès seine eigenen Carrés auf 1937 und beschreibt sie als Flächen für Farbe, Bilder und Geschichten. Das ist ein Bezug zum Accessoire als Erzählfläche, keine Behauptung, Hermès habe Schals erfunden, und keine Verbindung zu Dracula.'
],'hermes-scarf',[
 'Poveste editorială Dracula: catifeaua nopții întâlnește o lumină roșie. O singură mișcare schimbă proporția culorilor, ca o cortină trasă încet într-un salon. Signature este imaginată ca un gest, nu ca un ornament fix: aceeași paletă, o altă expresie de fiecare dată.',
 'Dracula editorial story: the velvet of night meets a red light. One movement changes the balance of colours, like a curtain slowly drawn in a salon. Signature is imagined as a gesture rather than a fixed ornament: the same palette, a different expression each time.',
 'Redaktionelle Dracula-Geschichte: Der Samt der Nacht trifft auf rotes Licht. Eine Bewegung verändert das Verhältnis der Farben wie ein langsam zurückgezogener Vorhang im Salon. Signature erscheint als Geste statt als starres Ornament: dieselbe Farbwelt, jedes Mal ein anderer Ausdruck.'
],[
 [['Nocturn la operă','Opera nocturne','Nocturne in der Oper'],['Rochie neagră simplă, cercei discreți și pantofi uni.','Simple black dress, discreet earrings and plain shoes.','Schlichtes schwarzes Kleid, dezente Ohrringe und einfarbige Schuhe.'],['Operă, concert sau cină festivă.','Opera, concert or celebratory dinner.','Oper, Konzert oder festliches Abendessen.'],['Așază eșarfa lejer la gât, lăsând monograma vizibilă într-un singur punct. Evită nodurile strânse; adaptează drapajul la dimensiunea finală.','Drape the scarf loosely at the neck, showing the monogram at one point. Avoid tight knots and adapt the drape to the final size.','Das Tuch locker am Hals drapieren und das Monogramm an einer Stelle zeigen. Enge Knoten vermeiden und den Fall an die endgültige Größe anpassen.']],
 [['Linie roșie, ziua','A red line by day','Eine rote Linie am Tag'],['Cămașă albă, sacou antracit, pantaloni negri și geantă simplă.','White shirt, charcoal blazer, black trousers and a simple bag.','Weißes Hemd, anthrazitfarbener Blazer, schwarze Hose und schlichte Tasche.'],['Birou, brunch sau întâlnire în oraș.','Office, brunch or a city meeting.','Büro, Brunch oder Treffen in der Stadt.'],['Pliază lejer pe lungime și lasă capetele să cadă sub rever, dacă măsurile permit. Păstrează celelalte imprimeuri la minimum.','Fold loosely lengthways and let the ends fall beneath the lapel if dimensions allow. Keep other patterns to a minimum.','Locker längs falten und die Enden unter das Revers fallen lassen, sofern die Maße passen. Weitere Muster sparsam einsetzen.']]
],{
 material:['Compoziția fibrelor și procentele sunt în așteptarea etichetei. Aspectul satinat nu confirmă mătasea naturală.','Fibre composition and percentages await the label. A satin-like appearance does not verify natural silk.','Faserzusammensetzung und Anteile stehen bis zum Etikett aus. Satinartige Optik bestätigt keine Naturseide.'],
 lining:['Nu este identificabilă o căptușeală distinctă în vizual; construcția și numărul straturilor se confirmă de producător.','No separate lining is identifiable in the visual; construction and layer count require manufacturer confirmation.','Im Bild ist kein separates Futter erkennbar; Aufbau und Lagenzahl muss der Hersteller bestätigen.'],
 hardware:['Nu sunt vizibile componente metalice. Tivul, cusătura marginii și procedeul de imprimare sunt în așteptare.','No metal components are visible. Hem construction, edge stitching and printing method are pending.','Keine Metallteile sichtbar. Saumverarbeitung, Randnaht und Druckverfahren stehen aus.'],
 careText:[
 'Păstrează eșarfa ferită de soare, umezeală și suprafețe care pot agăța fibra. Nu aplica parfum direct pe material. Până la confirmarea compoziției și a etichetei, nu presupune că sunt permise spălarea, curățarea chimică sau călcarea. Depozitează lejer, fără noduri strânse; protocolul final va fi cel furnizat de producător.',
 'Keep the scarf away from sunlight, moisture and surfaces that could snag the fibres. Do not spray perfume directly onto it. Until composition and care labelling are confirmed, do not assume washing, dry cleaning or ironing are permitted. Store loosely without tight knots; follow the manufacturer’s final care procedure.',
 'Das Tuch vor Sonne, Feuchtigkeit und Oberflächen schützen, die Fäden ziehen könnten. Kein Parfüm direkt aufs Material sprühen. Bis Zusammensetzung und Pflegeetikett bestätigt sind, weder Waschen noch chemische Reinigung oder Bügeln voraussetzen. Locker ohne enge Knoten lagern; maßgeblich sind die endgültigen Herstellerhinweise.'
]
});
const document={schema_version:1,researched_at:'2026-09-25',scope:'Five existing Dracula Design product concepts. Editorial and visual material separated from verified technical specifications.',sources,products:rows};
fs.writeFileSync(path.join(out,'product-enrichment.json'),JSON.stringify(document,null,2)+'\n','utf8');
let md='# Surse pentru conținutul Dracula Design\n\nCercetare: 25 septembrie 2026. Cinci produse, fiecare în RO / EN / DE.\n\n';
md+='## Separarea faptelor de conținutul editorial\n\nFișele au fost redactate după inspectarea celor cinci imagini originale aprobate. Aspectul, culoarea și elementele vizibile sunt observații din fotografii, nu confirmări tehnice. Materialele, dimensiunile, greutatea, rezistența, capacitatea și originea rămân explicit în așteptarea documentației furnizorului. Nu sunt inventate performanțe RFID, impermeabilitate, compatibilități de laptop sau certificări.\n\nTextele `brand_story` și propunerile de ținute sunt creații editoriale originale. Textele `history` sunt parafraze scurte ale surselor primare de mai jos, despre categoria obiectului; nu atribuie brandului Dracula istoria altui producător și nu sugerează afiliere. Nu sunt necesare valori calorice pentru produse nealimentare.\n\n';
md+='## Surse istorice\n\n';
for(const s of sources)md+=`- **${s.id}** — [${s.title}](${s.url}). Consultat: ${s.accessed_at}.\n`;
md+='\n## Mapare\n\n| Produs | Sursă | Fapt utilizat |\n|---|---|---|\n| Rucsac Business | fjallraven-kanken | Exemplul Kånken, anul școlar 1978 și colaborarea cu cercetașii suedezi; nu o origine universală a rucsacului. |\n| Servietă Business | vam-bags | Cutia pentru documente a lui Churchill, John Peck & Son, circa 1921, în expoziția V&A. |\n| Portofel Signature | williamsburg-pocketbook | Portofelul brodat din 1794 și utilizarea acestei categorii pentru bani, hârtii și obiecte mici. |\n| Geantă Tote | llbean-tote | Ice Carrier din 1944 și revenirea ca Boat and Tote în 1965; nu afirmația că acesta a fost primul tote din lume. |\n| Eșarfă Signature | hermes-scarf | Începutul propriilor carrés Hermès în 1937 și rolul lor narativ; nu inventarea eșarfei. |\n\n';
md+='## Observații despre vizualurile existente\n\nImaginile furnizate conțin deja mențiuni precum „Made in România” și, în cazul portofelului, „Premium Italian Leather”. Conținutul nou nu le preia ca date verificate. Imaginile nu au fost modificate. Scena Tote arată mai multe accesorii: fișa precizează că oferta se referă doar la geanta Tote, iar restul sunt elemente de prezentare.\n\n## Validare\n\n15 versiuni lingvistice complete; 11 rânduri tehnice per produs și limbă; două ținute pentru fiecare produs și limbă. Fiecare istoric are un identificator de sursă valid. Textele sunt stocate ca date, fără HTML sau cod executabil.\n';
fs.writeFileSync(path.join(out,'DESIGN-SOURCES.md'),md,'utf8');
for(const p of rows)for(const l of langs){const c=p.content[l];if(c.technical.length!==11||c.styling.length<2||!c.history.source_ids.every(id=>sources.some(s=>s.id===id)))throw Error('Invalid '+p.id+' '+l);}
console.log(JSON.stringify({products:rows.length,locales:langs,technical_rows_per_locale:11,styling_looks_per_locale:2,output:out}));
