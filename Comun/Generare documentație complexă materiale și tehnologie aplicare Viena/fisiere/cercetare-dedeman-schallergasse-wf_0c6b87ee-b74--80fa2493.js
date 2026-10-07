export const meta = {
  name: 'cercetare-dedeman-schallergasse',
  description: 'Cercetare produse premium pe dedeman.ro pentru toate categoriile de materiale ale proiectului',
  phases: [{ title: 'Cercetare Dedeman', detail: '12 categorii de materiale' }],
}

const SCHEMA = {
  type: 'object',
  required: ['categorie', 'produse'],
  properties: {
    categorie: { type: 'string' },
    produse: { type: 'array', items: { type: 'object',
      required: ['material', 'producator', 'denumire_produs', 'link', 'pret_cu_tva', 'um_vanzare', 'disponibil_dedeman'],
      properties: {
        material: { type: 'string', description: 'denumirea generica din centralizator' },
        producator: { type: 'string' },
        denumire_produs: { type: 'string', description: 'denumirea EXACTA a produsului de pe dedeman.ro' },
        cod_dedeman: { type: 'string' },
        link: { type: 'string' },
        link_verificat: { type: 'boolean', description: 'true doar daca ai deschis pagina cu WebFetch si ai vazut produsul' },
        disponibil_dedeman: { type: 'boolean' },
        pret_cu_tva: { type: 'number', description: 'pret in lei per unitate de vanzare, cu TVA, vazut pe pagina' },
        um_vanzare: { type: 'string', description: 'ex: sac 25 kg, placa 1200x2600 mm, galeata 15 L, buc' },
        continut_ambalaj: { type: 'number', description: 'cantitatea dintr-un ambalaj exprimata in UM de proiect (ex: placa 3.12 mp -> 3.12)' },
        um_proiect: { type: 'string', description: 'mp / ml / kg / l / buc / mc' },
        consum_specific: { type: 'string', description: 'ex: 1 kg/mp/mm; 4-5 kg/mp la pieptene 8mm; 0.16 L/mp/strat' },
        randament_ambalaj: { type: 'string', description: 'ex: 1 sac acopera ~5 mp la strat 3 mm' },
        nivel: { type: 'string', enum: ['standard', 'premium', 'super-premium'] },
        observatii: { type: 'string' },
        alternative: { type: 'array', items: { type: 'object', properties: {
          denumire: { type: 'string' }, producator: { type: 'string' }, link: { type: 'string' },
          pret_cu_tva: { type: 'number' }, um_vanzare: { type: 'string' }, nivel: { type: 'string' },
          observatii: { type: 'string' } } } }
      } } },
    note: { type: 'string' }
  }
}

phase('Cercetare Dedeman')

const COMMON = `Esti specialist in achizitii de materiale de constructii, membru al echipei care pregateste lista de achizitie de la Dedeman pentru renovarea premium a unui imobil in Viena (proiect Schallergasse 35: demisol yoga + parter + 3 etaje + mansarda noua pe 2 niveluri, recompartimentari cu gips-carton, finisaje premium).

REGULI OBLIGATORII:
1. Cauta produsele pe dedeman.ro. Foloseste WebSearch cu allowed_domains ["dedeman.ro"] si/sau WebFetch direct pe https://www.dedeman.ro/ro/cauta?q=... (pagina de cautare) sau pe categorii.
2. VERIFICA fiecare produs principal cu WebFetch pe pagina lui de produs. Seteaza link_verificat=true DOAR daca ai vazut efectiv pagina cu pretul. NU inventa linkuri sau coduri - un link inventat e mai rau decat lipsa lui.
3. Prefera marci PREMIUM si SUPER-PREMIUM disponibile la Dedeman (ex: Knauf, Rigips/Saint-Gobain, Baumit, Caparol, Ceresit/Henkel, Mapei, weber, Isover, Ursa, Rockwool, Austrotherm, Legrand, Schneider, Grohe, Geberit, Ideal Standard, Villeroy&Boch, Hansgrohe, Egger, Krono, Bosch, Wago). Pentru fiecare material da produsul principal recomandat + 1-3 alternative (macar una super-premium daca exista).
4. Noteaza consumul specific REAL (din fisa tehnica a producatorului / descrierea Dedeman) si randamentul pe ambalaj.
5. Preturile pe dedeman.ro sunt afisate CU TVA (TVA Romania = 21%). Raporteaza pretul exact vazut.
6. Daca un material NU exista la Dedeman (ex. anumite membrane FPO, fibrociment de fatada), seteaza disponibil_dedeman=false, propune cel mai apropiat substitut de la Dedeman in "alternative" si explica in observatii.
7. Raspunde in limba romana. Fii exhaustiv: acopera TOATE materialele din lista ta.

LINKURI DEJA VERIFICATE ANTERIOR (iunie 2026, re-verifica pretul actual daca produsul e in lista ta):
- Caparol TiefGrund 10L: https://www.dedeman.ro/ro/grund-acrilic-caparol-tiefgrund-interior/-exterior-transparent-10-l/p/5011335
- Caparol CapaMaXX / Ceramic Matt 15L+2.5L: https://www.dedeman.ro/ro/vopsea-ultralavabila-caparol-ceramic-matt-mat-alb-interior-15-l-2-5-l/p/5019335
- Caparol Silicon-Fassadenputz K15 25kg: https://www.dedeman.ro/ro/tencuiala-siliconica-structurabila-caparol-silicon-fassadenputz-k15-1-5-mm-alb-25-kg/p/5000939
- Caparol PutzGrund 25kg: https://www.dedeman.ro/ro/grund-de-aderenta-caparol-putzgrund-interior/-exterior-alb-25-kg/p/5004494
- Baumit DuoContact 25kg: https://www.dedeman.ro/ro/adeziv-si-masa-pe-spaclu-pentru-placi-termoizolante-baumit-duocontact-interior/-exterior-25-kg/p/4006590
- Baumit MosaikTop 25kg: https://www.dedeman.ro/ro/tencuiala-decorativa-mozaicata-pentru-soclu-baumit-mosaiktop-331-interior/-exterior-25-kg/p/5009915
- Rigips Rimano TEN 25kg: https://www.dedeman.ro/ro/tencuiala-de-ipsos-rigips-rimano-ten-interior-25-kg/p/5002442
- Rigips Rimano Bianco 20kg: https://www.dedeman.ro/ro/glet-de-finisaj-rigips-rimano-bianco-pe-baza-de-ipsos-interior-20-kg/p/5007470
- Knauf Super Finish 20kg: https://www.dedeman.ro/ro/glet-de-finisaj-knauf-super-finish-interior-20-kg/p/5019211
- Knauf HP Finish 20kg: https://www.dedeman.ro/ro/glet-de-finisare-superfin-knauf-hp-finish-interior-20-kg/p/5019835
- Plasa fibra sticla 160g 50mp: https://www.dedeman.ro/ro/plasa-fibra-sticla-premium-interior/-exterior-160-g-50-m/p/5009244
- Banda fibra sticla Rigips 25m: https://www.dedeman.ro/ro/banda-fibra-sticla-pentru-imbinare-rigips-25-m/p/5000262

`

const cats = [
  { label: 'gips-carton', prompt: `CATEGORIA TA: GIPS-CARTON + PROFILE + ACCESORII MONTAJ.
Materiale de gasit (cantitatile aproximative din proiect, pentru alegerea ambalajelor):
- Placa gips-carton standard GKB 12.5 mm (~700 mp total)
- Placa gips-carton hidrofuga GKBI/RBI 12.5 mm (~120 mp, bai)
- Placa gips-carton rezistenta la foc GKF 15 mm si 12.5 mm (~1100 mp - pereti REI90, invelitoare)
- Placa gips-carton antifoc+hidrofuga GKFI 15 mm (~100 mp)
- Placa exterior tip Aquapanel / cement board (~65 mp, fatada ventilata)
- Profile CW/UW 50, 75, 100 (pereti 10/12.5/15 cm), profile CD 60/UD 27 pentru placari si tavane, cu cantitati tipice la mp de perete
- Prelungitoare/imbinari, bride/nonius, tija M8
- Suruburi autofiletante gips 25mm/35mm/45mm (cutii mari), dibluri metalice pentru placi, suruburi metal-metal
- Banda de etansare sub profile (banda acustica/dichtung), banda decuplare acustica din spuma 0.25cm (~135 ml)
- Vinclu/coltar metalic, banda imbinare hartie/fibra, chit rosturi (Uniflott / Super finish la rosturi)
- Masca gips-carton pentru rezervor WC Geberit (~24 mp - placa + structura)
- Tabla otel zincata 1 mm ca strat in perete antiefractie WTW01 (~32 mp) - cauta tabla plana zincata
Include si o estimare de consum: profile CW la 60 cm, UW pe perimetru, ~2 ml profil/mp perete, suruburi ~15 buc/mp/strat.` },

  { label: 'izolatii', prompt: `CATEGORIA TA: TERMOIZOLATII + FOLII/BARIERE.
Materiale de gasit (grosimi si cantitati aproximative):
- Vata bazaltica placi 10 cm pentru pereti gips-carton 15cm (~125 mp) - ex. Rockwool
- Vata minerala moale rulou/placi: 3 cm (~100 mp), 5 cm (~400 mp), 6-6.5 cm (~200 mp), 7.5 cm (~160 mp), 12 cm (~15 mp), 16 cm (~70 mp), 20 cm (~450 mp - acoperis/pereti mansarda, clasa A2) - ex. Isover, Ursa, Knauf Insulation
- Vata minerala rigida de fatada 18 cm (~11 mp) si 5 cm (~150 mp) - ex. Rockwool Frontrock
- Placi vata minerala rigida acoperis 20 cm intre grinzi (~250 mp)
- Placi vata pentru rost de separatie 6 cm (~50 mp)
- Polistiren extrudat XPS 5 cm (~5 mp) si 18 cm (~3 mp) - Austrotherm
- Polistiren EPS rigid pentru pante 7-12 cm (~60 mp) - EPS200
- Placa tacker 3 cm pentru incalzire in pardoseala (~260 mp) + folie/capse tacker
- Folie PE pardoseala (~380 mp)
- Bariera de vapori sd>=100 m (~500 mp) - ex. folie aluminizata
- Membrana anticondens / folie difuzie deschisa pentru acoperis si fatada ventilata (~250 mp)
- Membrana de etansare sub fibrociment (~140 mp)
- Geotextil (~80 mp)
- Adeziv + dibluri pentru vata bazaltica de fatada
Pentru fiecare: pret/ambalaj, mp/pachet, lambda daca e afisat.` },

  { label: 'gleturi-vopsele', prompt: `CATEGORIA TA: GLETURI, AMORSE, VOPSELE, TENCUIELI INTERIOARE.
Cantitati aproximative din proiect:
- Glet de finisaj premium (2 straturi pe ~1000 mp interior => ~2000 mp de strat; consum ~1 kg/mp/strat) - Knauf Super Finish / HP Finish, Rigips Rimano Bianco/Glet Extra, Baumit FinoFinish
- Tencuiala de ipsos interioara (reparatii + spaleti ~50 mp) - Rimano TEN / Knauf MP75-Goldband
- Tencuiala var-ciment interioara (~100 mp) si tencuiala interioara pentru zidarie noua
- Amorsa/grund pereti inainte de glet si vopsea (~2500 mp) - Caparol TiefGrund, Knauf Tiefengrund
- Vopsea lavabila premium alba interior (~1370 mp pereti + ~560 mp tavane, 2 straturi) - Caparol CeramicMatt/Indeko, alternativ super-premium
- Vopsea lavabila pentru spatii umede / anti-mucegai (~110 mp) - Caparol Fungitex / similar
- Vopsea lavabila TEXTURATA pentru sala yoga (~215 mp)
- Plasa fibra sticla pentru glet (~1200 mp)
- Coltare aluminiu/PVC cu si fara plasa (~200 ml + rezerva)
- Profil colt cu picurator
- Banda maskare, folie protectie, hartie abraziva/discuri slefuit P120/P150/P220 (Bosch Expert M480 225mm)
Include consumuri specifice reale si randamente pe galeata/sac.` },

  { label: 'ceramice', prompt: `CATEGORIA TA: GRESIE, FAIANTA, ADEZIVI, HIDROIZOLATII SUB PLACAJ.
Cantitati aproximative:
- Gresie portelanata premium 60x60 si 60x120 cm (total ~72 mp + terasa 27 mp exterior antiderapanta R10/R11 + balcon 44.5 mp gresie 30x60 exterior)
- Faianta / placi ceramice premium 60x60 sau 60x120 pana la H=2.40 (~150 mp bai + ~17 mp bucatarii)
- Placaj ceramic pentru ghene tehnice (~35 mp)
- Adeziv flexibil C2TE S1 alb/gri premium (~240 mp placari; consum 4-5 kg/mp) - Mapei Keraflex Maxi S1, weberset, Ceresit CM17
- Chit de rosturi premium (Mapei Ultracolor Plus / Ceresit CE40) + silicon sanitar
- Hidroizolatie pensulabila bicomponenta/monocomponenta pentru bai si dus (~160 mp, 2 straturi) - Mapei Mapelastic, Mapegum WPS, Ceresit CL51
- Banda de etansare colturi + mansete pentru treceri - Mapeband / Ceresit CL152
- Profile de colt/trecere pentru gresie-faianta, distantieri/sistem nivelare
- Plinta gresie h=7cm (~60 ml - se poate taia din placi; noteaza si plinte gata facute)
Include consumuri reale per produs.` },

  { label: 'sape-betoane', prompt: `CATEGORIA TA: SAPE, BETOANE, AGREGATE.
Cantitati aproximative:
- Sapa slab armata 5 cm (~230 mp; ~100 kg/mp la 5cm => ~23 t material sapa M10 sau sapa gata preparata) - saci 40kg Baumit/CT
- Fibre polipropilena pentru armare dispersa + plasa sudata Ø4 100x100 (~230 mp)
- Sapa autonivelanta premium (~270 mp la 3-10 mm; consum ~1.6-1.7 kg/mp/mm) - weberfloor, Mapei Ultraplan, Ceresit CN76/CN69
- Sapa pentru incalzire in pardoseala 7 cm (~260 mp) - sapa CT-C25 cu aditiv, saci
- Sapa usoara de egalizare 5-8.5 cm (~15.3 mc + 97 mp x 5cm) - sapa usoara cu perlit / polistiren granule
- Suprabeton C20/25 7cm armat (~13 mc) - beton sac 40kg sau statie? noteaza optiuni Dedeman (ciment+agregat+cofraj)
- Beton de panta 6 cm (~0.2 mc) si placa beton armat 20cm (~0.6 mc) - ciment premium, nisip, pietris, armatura
- Amorsa/punte aderenta pentru sape (Baumit Grund / weber)
- Pietris 16/32 (~4.5 mc + 6 mc terasa/balcon), folie PE
- Profil dilatatie sapa, banda perimetrala spuma
Da si reteta orientativa: saci ciment 40kg per mc, etc.` },

  { label: 'parchet-plinte', prompt: `CATEGORIA TA: PARCHET, PLINTE, PERVAZE/GLAFURI INTERIOARE.
Cantitati aproximative:
- Parchet stratificat PREMIUM stejar (triplustratificat, clasa 33 sau echivalent rezidential premium; ~480 mp total cu tot cu mansarda) - la Dedeman: gama premium (ex. Barlinek, Egger PRO, HERZ parchet stratificat) - da si varianta laminat premium 12mm AC5 ca alternativa economica si varianta super-premium
- Folie/substrat parchet premium (fonoizolant, ~480 mp) - ex. Arbiton Secura
- Adeziv parchet (daca lipit; parchetul stratificat se poate si flota - explica in observatii) + cleme/distantieri
- Plinta parchet H=7cm premium (MDF alb / furnir stejar, ~460 ml) + colturi/imbinari/adeziv plinta
- Plinta gresie H=7cm (~60 ml)
- Pervaze interioare / glafuri ferestre interioare latime 23-68 cm (~40 ml) - glaf PVC/lemn masiv/MDF - la unghi
- Profile de trecere parchet-gresie, profile dilatatie (alama/aluminiu premium)
- Bariera vapori sub parchet la parter/demisol
Include consumuri si mp/pachet la parchet.` },

  { label: 'usi-tamplarie', prompt: `CATEGORIA TA: USI INTERIOARE + STICLA NEVADA.
Cantitati exacte din proiect:
- Usa intrare apartament 90x210 (3 buc etaje existente + 4 buc mansarda EI2 30-C metalica/antifoc cu clasa) - cauta usi metalice intrare apartament premium si usi antifoc EI30 daca exista
- Usa interior lemn 80x210 (13 buc mansarda + 4 buc yoga demisol)
- Usa interior lemn 90x210 (6 buc), 100x210 (2 buc)
- Usa glisanta 90x210 + CASETA de glisare in perete (5 buc) - cauta caseta glisare Eclisse/porta + foaie usa compatibila
- Usa glisanta aplicata 70x210 pentru WC (1 buc)
- Usa sticla mata dubla pentru dus 100x210 (2 buc, demisol yoga) - cabina/paravan sticla premium
- Usi premium: furnir lemn natural / vopsite premium; da game disponibile la Dedeman (ex. usi Porta Doors premium, Pamate etc.) cu preturi pe foaie+toc+balamale+maner
- Manere/broaste/balamale premium, opritori
- STICLA NEVADA / caramizi de sticla 19x19x8 cm (~100 buc: 2 randuri la partea superioara a unor pereti) + mortar/distantieri/armatura montaj caramida sticla
- Rigidizare metalica sustinere randuri Nevada (~15 ml) - profile/tije
Preturi pe bucata cu tot cu toc unde e cazul.` },

  { label: 'fatade', prompt: `CATEGORIA TA: FATADE + TENCUIELI EXTERIOARE DECORATIVE.
Cantitati din proiect (fatada istorica stradala + fatade curte + extindere mansarda):
- Tencuiala decorativa siliconica premium 1.5mm (~350 mp fatade curte: 272+49+28.3 mp) - Caparol Silicon-Fassadenputz K15 (verificat), Baumit SilikonTop, weber.pas silicon
- Tencuiala silicata armata pentru atic/calcan (~57 mp: 44+12.8)
- Tencuiala minerala exterioara + finisaj pentru AW01a (~11 mp)
- Finisaj fin fatada istorica stradala: vopsea silicat/siloxan fatada premium (~140 mp: decorativa 76.6 + ancadramente 91.1 - partial) - Caparol muresko/AmphiSilan sau Baumit
- Soclu: Baumit MosaikTop (~12 mp) (verificat)
- Bosaj fatada (~45 mp) - profile/tencuiala de modelare
- Profile decorative fatada (ancadramente, cornise) - polistiren acoperit - cca 91 mp zone
- Adeziv+spaclu Baumit DuoContact (~350 mp sistem) + plasa fibra sticla exterior + dibluri fatada
- Amorsa Caparol PutzGrund / Baumit UniPrimer (~400 mp)
- Glafuri exterioare aluminiu (20 ml + 11.4 ml + 2 ml; latime ~20-25cm) RAL istoric
- Sort tabla fatada principala (~116.5 ml!) - tabla plana zincata vopsita / sistem
- Vopsea + grund metal pentru balustrade metalice (~75 ml balustrada: 60.65+14.4) - Hammerite
- Tencuiala exterioara de etansare pt zidarie (~44 mp)
Include consumuri (tencuiala decorativa 2.5-2.9 kg/mp la K1.5).` },

  { label: 'invelitoare-lemn', prompt: `CATEGORIA TA: INVELITOARE, LEMN DE CONSTRUCTIE, MEMBRANE ACOPERIS.
Cantitati din proiect (acoperis nou mansarda REI30/60):
- Placi fibrociment pentru invelitoare si fatada (1cm, ~140 mp invelitoare DA01 + ~65 mp fatada) - daca nu exista la Dedeman, substitut: tigla metalica premium / placi fibrociment ondulate; marcheaza disponibilitatea real
- Tabla faltuita pentru lucarna (~24 mp) - tabla plana zincata prevopsita in rulou/click-falz (ex. Bilka retail) 
- Membrana de etansare / folie difuzie premium (~140 mp + 24 mp) - ex. Delta, Dorken? la Dedeman: folie anticondens premium 
- Astereala lemn 2.4 cm (~500 mp total!) - scandura rindeluita/bruta, calcul mc
- Sipci 3x5 si contrasipci 5x5 (~140 mp acoperis => ~2 mc) - lemn ecarisat
- OSB3 2 cm (~100 mp)
- Grinzi lemn 25 cm (0.4 mc) + lemn ecarisat divers
- Hidroizolatie terasa: membrana FPO/TPO 1.5mm (~70 mp) - daca nu e la Dedeman, substitut membrana bituminoasa premium; membrane bituminoase SBS 2 straturi (~40 mp + 9 mp)
- Bariera vapori bituminoasa cu insertie aluminiu pentru terasa
- Covor granule cauciuc 1cm (~27 mp)
- Placa protectie foc silicat de calciu 2.5cm (~45 mp) - daca nu e la Dedeman noteaza substitut
- Tabla cutata aluminiu/otel pentru balcon (~45 mp)
- Pietris rotund 16/32 pentru terase (~6.5 mc), dale beton 30x60 sau gresie exterior (44.5 mp - coordoneaza cu categoria ceramice, tu da dale/plot-uri)
- Jgheaburi/burlane premium (sistem pluvial ~30 ml jgheab + 4 burlane, estimare) - Bilka/Wetterbest premium
- Solzi/accesorii: parazapezi, aerisitoare, sort streasina, picurator
Atentie la ce e realist la Dedeman vs. comanda speciala.` },

  { label: 'electrice', prompt: `CATEGORIA TA: MATERIALE ELECTRICE (re-verificare preturi + completare).
Lista de baza (cantitati de achizitie deja calculate din planse IE01-IE05):
- Priza dubla Schuko Legrand Valena Life 128 buc; priza simpla 60 buc; priza IP44 cu capac 25 buc
- Intrerupator simplu 70, dublu 30, cap scara 25, cruce 10 - Legrand Valena Life
- Rame 1/2/3/4/5 posturi (176/66/39/17/16)
- Priza RJ45 Cat6 16 buc, priza TV 16 buc
- Plafoniere LED premium IP20 44 buc; corpuri suspendate decorative 59 buc (buget); plafoniere IP44 baie 21 buc; aplice IP44 21 buc; corp liniar LED IP65 10 buc
- Senzor miscare 360 incastrat 18 buc (Legrand 048944 sau echivalent)
- Tablouri: 11x apartament 24-36 module incastrate premium (Schneider Resi9/Legrand), 1x spatii comune 36-54 mod, 1x yoga 24 mod
- RCBO 1P+N 16A B 30mA tip A: 49 buc (Schneider Acti9 iCV40N); MCB 10A: 37 buc; protectii speciale 20-32A: 25 buc; SPD tip 2: 14 buc
- Cabluri: CYY-F 3x1.5 1800m, 3x2.5 2100m, 5x2.5 250m, 5x6 450m; UTP Cat6 915m; RG6 500m; conductor CU v-g 16mm 150m
- Copex: 16mm 1600m, 20mm 2400m, 25mm 500m, 32mm 150m (Legrand cu fir tragere)
- Doze aparat 290, doze module 180, doze derivatie 130; Wago 221-413 6 seturi, 221-415 4 seturi, cleme corp iluminat 160
LINKURI VECHI DE RE-VERIFICAT (au fost valide in mai 2026): 
- https://www.dedeman.ro/ro/rola-cablu-electric-cyy-f-3-x-1-5-mmp-100-m-cupru/p/1073159
- https://www.dedeman.ro/ro/rola-cablu-electric-cyy-f-600/-1000-3-x-2-5-mmp-100-m-cupru/p/1073161
- https://www.dedeman.ro/ro/siguranta-automata-modulara-schneider-electric-acti-9-icv40n-a9dg4616-10-ka-1p-n-16-a-curba-b/p/1063331
- https://www.dedeman.ro/ro/conector-wago-221-413-compact-3-fire-0-02-4-mmp-set-50-bucati/p/1062639
- https://www.dedeman.ro/ro/conector-wago-221-415-compact-5-fire-0-02-4-mmp-set-25-bucati/p/1062640
- https://www.dedeman.ro/ro/priza-internet-valena-life-753140-rj45-cat-5e-incastrat-alb/p/1044705
- https://www.dedeman.ro/ro/copex/-tub-riflat-poliolefina-legrand-651216-d-exterior-16-mm-d-interior-10-7-mm-750-n-cu-fir-de-tragere-rola-100-m/p/1011580
- https://www.dedeman.ro/ro/plafoniera-led-osram-36-w-2880-lm-lumina-rece-alb-modern/p/1116000
- https://www.dedeman.ro/ro/plafoniera-led-pentru-baie-ledvance-24-w-1800-lm-lumina-rece-6500k-cu-senzor-d-32-5-cm-ip44-alb-modern/p/1082528
- https://www.dedeman.ro/ro/corp-de-iluminat-led-liniar-hoff-36-w-3600-lm-120-cm-lumina-neutra-ip65-interior/-exterior/p/1070699
- https://www.dedeman.ro/ro/senzor-de-miscare-legrand-048944-ip41-alb-360-grade-incastrat/p/1049222
Verifica preturile actuale si gaseste variantele premium lipsa (tablouri exacte, MCB, SPD, doze).` },

  { label: 'sanitare-termice', prompt: `CATEGORIA TA: INSTALATII SANITARE + TERMICE + OBIECTE SANITARE PREMIUM.
Estimari din proiect (11 apartamente noi/renovate + spatiu yoga cu 2 dusuri + bai multiple; WC-uri suspendate cu rezervoare incastrate tip Geberit - "masca gheberit" apare in centralizator ~24 mp):
- Rezervor WC incastrat Geberit Duofix + clapeta premium (est. 14 buc) - verifica gama Geberit la Dedeman
- Vas WC suspendat premium rimless + capac soft-close (14 buc) - Geberit/Ideal Standard/Villeroy&Boch/Grohe
- Lavoar premium + baterie lavoar premium Grohe/Hansgrohe (est. 14 buc)
- Cada incastrata/ingropata (1 buc parter - "cada ingropata" pe plan; 170x75) + cazi normale est. 4 buc
- Coloana dus premium + baterie dus termostatata (est. 12 buc) + rigola dus / cadita
- Chiuveta bucatarie + baterie premium (est. 12 buc)
- Sifoane pardoseala, racorduri flexibile, robineti coltar premium (Schell?)
- Tevi PPR Stabi/PEX cu insertie 20/25/32 (est. 800 ml total) + fitinguri, coliere, izolatie teava (tub izolant)
- Canalizare PP 32/40/50/110 (est. 350 ml) + coturi/ramificatii/reductii/piese curatire + coloane ventilate (caciuli ventilatie / aeratoare cu membrana)
- Incalzire in pardoseala: teava PEX-a/PE-RT 16/17mm (~260 mp x 5.5 ml/mp = ~1450 ml), distribuitoare inox 6-10 cai cu debitmetre premium, banda perimetrala, aditiv sapa, automatizare termostate zona premium
- Radiatoare otel premium tip 22 (est. 25 buc, diverse lungimi 600/1200-1800) - Vogel&Noot? la Dedeman gama premium + robineti termostatati Danfoss/Heimeier
- Ventilatie bai: ventilatoare axiale silentioase premium cu clapeta+timer (est. 10 buc) + tubulatura flexibila/rigida 100-125mm + guri evacuare peste acoperis
Fii atent la ce se vinde efectiv la Dedeman si include alternative premium/super-premium la obiectele sanitare.` },

  { label: 'metal-diverse', prompt: `CATEGORIA TA: CONFECTII METALICE + MATERIALE DIVERSE RAMASE.
Din proiect:
- Scara metalica interioara yoga: 7 trepte L=1.50m + 8 contratrepte + podest metalic 1.65x1.50m - la Dedeman: profile metalice (teava rectangulara, cornier, platbanda, tabla striata/expandata) - estimeaza necesarul de profile pentru confectie (kg/ml) + vopsea + electrozi/discuri
- Balustrade metalice noi (~75 ml, H=100cm) - teava rectangulara/rotunda, mana curenta
- Profile metalice U 12 cm pentru structura balcon (conform proiect structura - doar mentioneaza optiuni)
- Rigidizari metalice pentru sticla Nevada (~15 ml) - profile/otel lat
- Grinzi lemn 25 cm (~0.4 mc) si grinzi transversale - lemn ecarisat C24
- Polistiren extrudat 5cm (~5 mp - inaltare pardoseala baie parter), folie PVC (~5 mp), astereala 2cm (~5 mp)
- Spume PU premium (Soudal/Den Braven), silicoane, ancore chimice, dibluri/suruburi universale, banda butilica
- Etansari antifoc traversari (mastic/spuma/mansoane intumescente EI90) - lot
- Scule/consumabile mari de santier: folie protectie, banda mascare, saci moloz, discuri taiere/slefuit
- Trape de vizitare gips-carton (est. 15 buc 30x30/60x60), profile dilatatie
- Vopsea + grund metal premium Hammerite (balustrade, scari) - re-verifica: https://www.dedeman.ro/ro/vopsea-alchidica-pentru-metal-hammerite-efect-fier-forjat-interior/-exterior-negru-2-5-l/p/5002366
Estimeaza cantitatile unde lipsesc, cu logica de inginer.` },
]

const results = await parallel(cats.map(c => () =>
  agent(COMMON + c.prompt, { label: 'dedeman:' + c.label, phase: 'Cercetare Dedeman', schema: SCHEMA })
))

const ok = results.filter(Boolean)
log(`Cercetare completa: ${ok.length}/${cats.length} categorii; total produse: ${ok.reduce((s, r) => s + (r.produse ? r.produse.length : 0), 0)}`)
return { categorii: cats.map((c, i) => ({ cheie: c.label, rezultat: results[i] })) }