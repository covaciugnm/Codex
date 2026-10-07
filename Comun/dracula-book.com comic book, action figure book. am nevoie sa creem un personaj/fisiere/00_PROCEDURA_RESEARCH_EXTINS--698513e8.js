export const meta = {
  name: 'dracula-research-extins',
  description: 'DRACULA COMICS: research extins — surse de inspirație din romane, scenarii, francize, seriale, BD/manga, jocuri + moduri de prezentare',
  phases: [
    { title: 'Sweep domenii', detail: '6 cercetători paraleli pe domenii diferite' },
    { title: 'Sinteză', detail: 'fișiere 04, 05, extindere bancă mecanisme și recomandări' },
    { title: 'Critic completitudine', detail: 'ce lipsește — completare' },
  ],
}

const ROOT = String.raw`D:\00. Downloads\Dracula Book\DRACULA-COMICS`
const R = ROOT + '\\02_RESEARCH'
const CANON = ROOT + '\\01_CANON\\00_CANON_NUCLEU.md'
const TMP = R + '\\_lucru_research_extins'

const COMMON = `Proiect: seria BD color + povestiri „DRACULA — Contele Nopții” (editura Dracula Book). Eroul: VLAD al III-lea Drăculea, vampir POZITIV, nemuritor, aristocrat transilvănean foarte bogat, cu simțuri supradezvoltate tip The Mentalist, care trăiește 550 de ani prin capitalele lumii sub identități false, iar acum e consultant al Poliției Române; familie nemuritoare tip Saga; antagonist fratern (Radu cel Frumos) + un antagonist-umbră pe termen lung. Citește canonul: ${CANON}.
PRINCIPIUL PRODUCĂTORULUI: „ORICE scenariu sau roman de succes poate fi sursă de inspirație — nu doar serialele polițiste. Lumea este ceea ce este — MODUL în care o prezentăm e important.”
Research-ul polițist există deja în ${R} (01_TOP_SERIALE_FILME.md, 02_BANCA_MECANISME_PLOT.md cu M01–M45 și V01–V20, 03_RECOMANDARI_DRACULA.md) — nu-l duplica, completează-l.
Folosește WebSearch/WebFetch (încarcă cu ToolSearch "select:WebSearch,WebFetch") pentru date verificabile (vânzări, premii, ratinguri, an); marchează „aprox.” ce nu poți confirma. Extrage MECANISME și ARHETIPURI, nu copia povești/replici. Scrie în română cu diacritice.`

const DOMAINS = [
  { key: 'clasici', title: 'Literatură clasică de aventură, mister și gotic', hint: 'Dumas (Contele de Monte Cristo, Cei trei muschetari), Hugo, Jules Verne, Conan Doyle (Sherlock Holmes), Poe, Bram Stoker (Dracula — structura epistolară!), Mary Shelley, Stevenson (Jekyll & Hyde), Gaston Leroux (Fantoma de la Operă), Baroneasa Orczy (Pimpernelul Stacojiu), Maurice Leblanc (Arsène Lupin), Agatha Christie, Raymond Chandler, Dashiell Hammett, Simenon (Maigret), Daphne du Maurier (Rebecca), Umberto Eco (Numele trandafirului), Mircea Eliade (Domnișoara Christina), Bulgakov (Maestrul și Margareta), Wilde (Dorian Gray)' },
  { key: 'bestseller', title: 'Bestselleruri moderne: thriller, istoric, fantasy, vampiri', hint: 'Dan Brown (Codul lui Da Vinci — enigme în monumente celebre!), Carlos Ruiz Zafón (Umbra vântului), Patrick Süskind (Parfumul — simțuri supradezvoltate!), Ken Follett, Stieg Larsson, Thomas Harris (Hannibal), Gillian Flynn, Stephen King (Salem’s Lot), Elizabeth Kostova (The Historian — Vlad Dracula prin arhivele Europei!), Anne Rice (Interviu cu vampirul), Stephenie Meyer, Deborah Harkness (A Discovery of Witches), Diana Gabaldon (Outlander — timeline dublu), J.K. Rowling, George R.R. Martin, Tolkien, Neil Gaiman (American Gods, Sandman), Terry Pratchett, Anthony Horowitz (Magpie Murders — roman în roman), Richard Osman, Kate Morton (dual timeline)' },
  { key: 'film', title: 'Filme, scenarii și francize de succes (nu doar polițiste)', hint: 'Indiana Jones, James Bond, Pirații din Caraibe, Star Wars, Nașul, Casablanca, trilogia Batman (Nolan), Marvel (Iron Man — miliardarul-erou; Doctor Strange; Avengers — construcția de univers), Highlander (nemuritorul prin secole!), Interview with the Vampire (1994), Bram Stoker’s Dracula (1992), Mission: Impossible, National Treasure (comori în monumente), Sherlock Holmes (Guy Ritchie), Inception, Gladiator, Titanic (cadru narativ bătrână-poveste), Amadeus, Masca lui Zorro, Kingsman, Knives Out, The Grand Budapest Hotel (cadre narative imbricate), Forrest Gump (omul prezent la evenimente istorice!), Midnight in Paris (epoci), The Curious Case of Benjamin Button, The Age of Adaline (nemuritoarea care fuge de identitate!), The Man from Earth, Only Lovers Left Alive' },
  { key: 'tv', title: 'Seriale de prestigiu și de gen (nu polițiste)', hint: 'Game of Thrones, Downton Abbey (familie aristocratică bogată), The Crown, Peaky Blinders (stil, costum, încetinitor), Doctor Who (călătorie prin epoci, companionul uman!), Outlander, Lupin (Netflix — gentleman-hoț, planuri dezvăluite în flashback), Sherlock (BBC — vizualizarea deducției pe ecran!), Wednesday, The Witcher, Vikings, Arcane (stil vizual), Stranger Things, Succession, Bridgerton, Lucifer, Supernatural, Buffy (monster-of-the-week + arc), The Vampire Diaries (frați vampiri rivali prin secole!), What We Do in the Shadows (TV), Castlevania (animat, Netflix), The Umbrella Academy, Loki (variante în timp), Dark (timeline-uri), Masters of the Air/Band of Brothers (istorie reală)' },
  { key: 'bd', title: 'BD, manga, jocuri narative (și cum sunt PREZENTATE/vândute)', hint: 'Batman (Year One, The Long Halloween — misterul pe 12 luni!), Superman, Spider-Man, X-Men, Sandman, Hellboy, Saga, Watchmen (backmatter documentar), V for Vendetta, Tintin (aventura prin lume + hărți), Asterix, Corto Maltese, Blacksad, Blake & Mortimer, Lucky Luke; manga: Hellsing, Vampire Hunter D, JoJo’s Bizarre Adventure (parte = epocă nouă!), Detective Conan, Death Note, One Piece, Vinland Saga; jocuri: Assassin’s Creed (orașe istorice celebre pe epoci — model direct pentru traseul capitalelor!), Castlevania, The Witcher 3, Uncharted, Red Dead Redemption 2, Vampyr, Vampire: The Masquerade; + formatele de prezentare: single issue 22–24 p., trade paperback, omnibus, coperți variante, ediții de colecție, Webtoon vertical, motion comics, Free Comic Book Day' },
  { key: 'prezentare', title: 'Moduri de prezentare / naratologie / design de experiență', hint: 'încadrare narativă (frame story: 1001 de nopți, Titanic, Grand Budapest Hotel), roman epistolar și documente găsite (Dracula lui Stoker: jurnale, scrisori, tăieturi de ziar), narator nesigur (Usual Suspects, Gone Girl), timeline dublu/multiplu (Outlander, Dark, Kate Morton), antologie cu fir roșu, cold open, „Anterior în…”, cliffhanger, poveste spusă prin obiecte (A History of the World in 100 Objects, muzee), hărți și jurnale (Tintin, Indiana Jones), backmatter (Watchmen, Saga — scrisori ale cititorilor), mockumentary (What We Do in the Shadows), vizualizarea gândirii (Sherlock BBC, Mentalist, Hannibal „mind palace”), montaj paralel, perspectiva antagonistului, puzzle-box (Lost), ARG/transmedia, cronica în-univers („Cronica de Sânge”), glosar/dramatis personae, pagini de recapitulare, coperți ca afișe de film, lettering și paletă ca instrumente narative (flashback sepia), webtoon vertical, site-ul ca muzeu interactiv' },
]

const DOMAIN_SCHEMA = {
  type: 'object',
  properties: {
    works: { type: 'array', items: { type: 'object', properties: {
      title: { type: 'string' }, creator: { type: 'string' }, year: { type: 'string' }, medium: { type: 'string' },
      success_evidence: { type: 'string', description: 'vânzări/premii/rating + sursă sau aprox.' },
      why_it_works: { type: 'string' }, transferable: { type: 'string', description: 'mecanismul/arhetipul/modul de prezentare transferabil' },
      apply_to_dracula: { type: 'string' },
    }, required: ['title', 'creator', 'year', 'medium', 'success_evidence', 'why_it_works', 'transferable', 'apply_to_dracula'] } },
    new_mechanisms: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string' }, definition: { type: 'string' }, examples: { type: 'string' }, dracula_use: { type: 'string' }, cliche_risk: { type: 'string' },
    }, required: ['name', 'definition', 'examples', 'dracula_use', 'cliche_risk'] } },
    presentation_modes: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string' }, description: { type: 'string' }, examples: { type: 'string' }, dracula_application: { type: 'string' },
    }, required: ['name', 'description', 'examples', 'dracula_application'] } },
    plot_seeds: { type: 'array', items: { type: 'object', properties: {
      seed: { type: 'string' }, flashback_stop: { type: 'string', description: 'popas din canon §3/§5 (oraș + ani)' }, inspired_by: { type: 'string' },
    }, required: ['seed', 'flashback_stop', 'inspired_by'] } },
    key_insights: { type: 'array', items: { type: 'string' } },
  },
  required: ['works', 'new_mechanisms', 'presentation_modes', 'plot_seeds', 'key_insights'],
}

phase('Sweep domenii')
const sweeps = await parallel(DOMAINS.map(d => () => agent(`${COMMON}

DOMENIUL TĂU: ${d.title}.
Pornește de la (nu te limita la) : ${d.hint}.
Livrează: ≥15 opere de succes (${d.key === 'prezentare' ? 'ca exemple pentru modurile de prezentare' : 'cu dovada succesului'}), ≥8 mecanisme NOI de plot/suspans/arhetip care NU sunt deja în banca M01–M45 (citește ${R}\\02_BANCA_MECANISME_PLOT.md ca să eviți duplicatele), ≥${d.key === 'prezentare' ? 25 : 6} moduri de prezentare, ≥5 semințe de plot pentru DRACULA (fiecare legată de un popas din canon §3/§5), 3–6 idei-cheie. Salvează și notițele tale brute în ${TMP}\\${d.key}.md (creează folderul). Returnează structura cerută.`,
  { label: `research ${d.key}`, phase: 'Sweep domenii', schema: DOMAIN_SCHEMA })))

const ok = sweeps.filter(Boolean)
log(`Sweep: ${ok.length}/${DOMAINS.length} domenii; ${ok.reduce((s, x) => s + x.works.length, 0)} opere, ${ok.reduce((s, x) => s + x.new_mechanisms.length, 0)} mecanisme noi, ${ok.reduce((s, x) => s + x.presentation_modes.length, 0)} moduri de prezentare, ${ok.reduce((s, x) => s + x.plot_seeds.length, 0)} semințe`)

phase('Sinteză')
const synth = await agent(`${COMMON}

Ești Analistul-șef A (Research & Intelligence) al DRACULA COMICS STUDIO. Ai primit rezultatele a ${ok.length} cercetători pe domenii (JSON mai jos; notițele brute în ${TMP}).
SARCINĂ — scrie/actualizează în ${R}:
1) 04_SURSE_EXTINSE_ROMANE_SCENARII.md — introducere cu principiul Producătorului; tabele pe domenii (romane clasice; bestselleruri moderne; filme/scenarii/francize; seriale; BD/manga/jocuri): titlu, autor, an, mediu, dovada succesului, de ce funcționează, ce transferăm, aplicarea la DRACULA. Deduplică. KPI: ≥60 opere din afara genului polițist (≥15 romane, ≥15 filme/scenarii/francize, ≥10 seriale, ≥10 BD/manga/jocuri). Secțiune „Arhetipuri-cheie pentru Vlad” (aristocratul bogat cu identitate secretă: Monte Cristo/Zorro/Pimpernel/Batman/Lupin; nemuritorul prin epoci: Highlander/Adaline/Forrest Gump/Doctor Who; frații rivali nemuritori: Vampire Diaries; orașele istorice ca personaje: Assassin’s Creed/Dan Brown/Tintin; simțuri supradezvoltate: Parfumul/Sherlock) cu regulile de folosire fără copiere.
2) 05_MODURI_DE_PREZENTARE.md — ≥30 de moduri de prezentare (deduplicate), fiecare: descriere, exemple celebre, aplicare concretă la DRACULA (în BD, în povestiri, pe site); apoi „FORMULA DE PREZENTARE A SERIEI DRACULA” recomandată (structura fixă a unui episod BD: cold open, flashback cu paletă de epocă, pagina „Din Cronica de Sânge”, backmatter; structura povestirii; identitatea copertelor; site-ul ca muzeu/arhivă) + ce NU facem.
3) Actualizează ${R}\\02_BANCA_MECANISME_PLOT.md: ADAUGĂ la final secțiunea „Mecanisme din surse extinse” cu mecanismele noi numerotate în continuare (M46, M47, …; deduplicate față de M01–M45 și între ele), fiecare cu nume, definiție, 2 exemple, aplicare la Vlad, risc de clișeu. KPI total ≥50 mecanisme. Nu șterge nimic existent.
4) Actualizează ${R}\\03_RECOMANDARI_DRACULA.md: adaugă recomandări noi din sursele extinse și semințele de plot noi (numerotate în continuare), astfel încât totalul să fie ≥45 semințe, fiecare cu popasul de flashback din canon și sursa de inspirație.
5) Actualizează raportul ${ROOT}\\00_STUDIO\\rapoarte\\A_research.md (livrabile noi, KPI țintă vs realizat pe noile cerințe, decizii, riscuri).
Scrie la nivel de excepție (va trece prin audit cu prag 9,50/10). Returnează rezumat cu KPI realizați.

REZULTATE DOMENII (JSON):
${JSON.stringify(ok)}`, { label: 'sinteză research extins', phase: 'Sinteză' })

phase('Critic completitudine')
const critic = await agent(`${COMMON}
Ești criticul de completitudine. Citește integral ${R}\\04_SURSE_EXTINSE_ROMANE_SCENARII.md, ${R}\\05_MODURI_DE_PREZENTARE.md, ${R}\\02_BANCA_MECANISME_PLOT.md, ${R}\\03_RECOMANDARI_DRACULA.md. Numără efectiv (Python) KPI-urile: ≥60 opere din afara genului polițist (≥15 romane, ≥15 filme/francize, ≥10 seriale, ≥10 BD/manga/jocuri), ≥50 mecanisme total, ≥30 moduri de prezentare, ≥45 semințe. Întreabă-te: ce opere majore de succes lipsesc evident (inclusiv literatură română și est-europeană, anime, literatură non-anglofonă), ce modalitate de prezentare lipsește, ce afirmație e neverificată? COMPLETEAZĂ direct în fișiere tot ce lipsește (verifică pe web ce adaugi). Returnează lista KPI numărate după completare și ce ai adăugat.`, { label: 'critic completitudine', phase: 'Critic completitudine' })

return { domains: ok.length, synth, critic }
