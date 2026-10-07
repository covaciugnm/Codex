export const meta = {
  name: 'continut-tiparire-3d',
  description: 'Conținut pentru servicii de tipărire 3D & prototipare + pagini per echipament (Prusa XL, RatRig, Modix)',
  phases: [
    { title: 'Draft', detail: 'conținut inițial per pagină' },
    { title: 'Spectaculos', detail: 'îmbogățire + aplicații + polish' },
  ],
}

const ITEMS = [
  { type:'overview', slug:'tiparire3d', name:'Servicii de tipărire 3D & prototipare',
    ctx:`Serviciul folosește 3 echipamente proprii de fabricație aditivă (FDM/FFF):
1) Original Prusa XL cu 5 capete de imprimare independente (multi-tool), volum 360x360x360 mm — multicolor & multi-material fără turnuri de purjare, până la 5 materiale/culori simultan.
2) RatRig V-Core 4.1 (dimensiune 500, volum ~500x500x500 mm), IDEX (Independent Dual Extruder) + upgrade Hybrid, incintă închisă cu filtrare aer, electronică dedicată 220V, firmware Klipper — printare duplication/mirror, materiale tehnice (ABS, ASA, PC, Nylon, PA-CF), suporturi solubile.
3) Modix BIG-Meter, volum de printare 980x1000x1000 mm (~1 metru cub), cap unic sau dublu, structură profile aluminiu T-slot 40x40, operare autonomă SD/WiFi — format foarte mare, machete, componente industriale mari.
Oferim și servicii de PROIECTARE (CAD) și PROTOTIPARE.` },
  { type:'machine', slug:'print-prusaxl', name:'Original Prusa XL (5 capete)',
    ctx:`Specificații (folosește-le exact, nu inventa cifre care le contrazic):
- Configurație: 5 capete de imprimare independente (multi-tool), schimbare automată de unealtă (tool changer)
- Tehnologie: FDM/FFF, cinematică CoreXY
- Volum de printare: 360 x 360 x 360 mm
- Pat încălzit segmentat; senzor load-cell pentru calibrare first layer
- Avantaj-cheie: printare multicolor și multi-material cu până la 5 culori/materiale simultan, FĂRĂ turnuri de purjare (fără risipă), fără schimbare manuală de filament
- Materiale: PLA, PETG, ABS, ASA, PC, TPU flexibil, materiale compozite (fibră de sticlă/carbon) cu duze compatibile` },
  { type:'machine', slug:'print-ratrig', name:'RatRig V-Core 4.1 — IDEX 500',
    ctx:`Specificații (folosește-le exact):
- Model: RatRig V-Core 4.1, dimensiune 500 — volum ~500 x 500 x 500 mm; cinematică CoreXY
- IDEX (Independent Dual Extruder) + upgrade Hybrid (comutare între moduri de lucru)
- Incintă închisă (enclosure) cu sistem de filtrare a aerului (Rat Pack Large) — pentru materiale tehnice
- Kit electronică dedicat, alimentare 220V, firmware Klipper (viteze mari, input shaping)
- Avantaje IDEX: printarea simultană a 2 piese identice (mod duplication) sau în oglindă (mod mirror) — dublează productivitatea; 2 materiale/culori diferite; suporturi solubile (PVA/BVOH) pentru geometrii complexe
- Materiale tehnice: ABS, ASA, PC, Nylon (PA), PA-CF / PA-GF, PETG, PLA` },
  { type:'machine', slug:'print-modix', name:'Modix BIG-Meter (1 m³)',
    ctx:`Specificații (din fișa tehnică, folosește-le exact):
- Volum de printare (XYZ): 980 x 1.000 x 1.000 mm (~1 metru cub) cu un singur cap
- Dimensiuni mașină (L x A x Î): 1.739 x 1.424 x 1.958 mm
- Cap de printare: unic (implicit) sau dublu (opțional)
- Software: profiluri de printare pentru PrusaSlicer și Cura
- Operare autonomă: card SD sau interfață web (WiFi)
- Structură: profile de aluminiu T-slot 40x40 și colțare din aluminiu vopsit electrostatic
- Utilizare: piese de dimensiuni foarte mari, machete la scară 1:1, componente industriale, mobilier, prototipuri mari` },
]

const MACHINE_SCHEMA = {
  type:'object', additionalProperties:false,
  properties:{
    tagline:{type:'string'},
    intro:{type:'string'},
    specs:{type:'array', items:{type:'object', additionalProperties:false,
      properties:{k:{type:'string'}, v:{type:'string'}}, required:['k','v']}},
    capabilities:{type:'array', items:{type:'string'}},
    materials:{type:'array', items:{type:'string'}},
    strengths:{type:'array', items:{type:'string'}},
    applications:{type:'array', items:{type:'object', additionalProperties:false,
      properties:{title:{type:'string'}, desc:{type:'string'}}, required:['title','desc']}},
    ideal_for:{type:'array', items:{type:'string'}},
    sample_projects:{type:'array', items:{type:'string'}}
  },
  required:['tagline','intro','specs','capabilities','materials','strengths','applications','ideal_for','sample_projects']
}
const OVERVIEW_SCHEMA = {
  type:'object', additionalProperties:false,
  properties:{
    tagline:{type:'string'},
    intro:{type:'string'},
    services:{type:'array', items:{type:'object', additionalProperties:false,
      properties:{icon:{type:'string', description:'un emoji reprezentativ'}, title:{type:'string'}, desc:{type:'string'}}, required:['title','desc']}},
    workflow:{type:'array', items:{type:'object', additionalProperties:false,
      properties:{title:{type:'string'}, desc:{type:'string'}}, required:['title','desc']}},
    materials:{type:'array', items:{type:'string'}},
    industries:{type:'array', items:{type:'object', additionalProperties:false,
      properties:{name:{type:'string'}, desc:{type:'string'}}, required:['name','desc']}},
    why_us:{type:'array', items:{type:'string'}},
    what_we_make:{type:'array', items:{type:'string', description:'tot ce se poate realiza cu cele 3 echipamente'}}
  },
  required:['tagline','intro','services','workflow','materials','industries','why_us','what_we_make']
}

function draftMachine(it){ return `Ești specialist senior în fabricație aditivă (3D printing) și copywriter tehnic pentru un serviciu profesional de printare 3D și prototipare (firma RED INTERNET SALES).
Creează conținutul pentru pagina echipamentului „${it.name}".

${it.ctx}

Produ conform schemei: un tagline spectaculos și memorabil; un intro de 2-3 fraze; un tabel de specificații (specs = perechi cheie/valoare, minim 7 rânduri, incluzând volumul de printare, tehnologia, materialele, precizia/finețea, particularitățile); capabilities (ce poate face concret); materiale compatibile; puncte forte (strengths); aplicații reale (min 6, fiecare cu title + desc); ideal_for; exemple de proiecte (sample_projects, min 6).
Reguli: NU inventa specificații care contrazic datele date; poți adăuga capabilități/materiale reale general valabile pentru acest tip de echipament. Ton profesionist, modern, orientat spre client. Scrie în limba română.` }

function draftOverview(it){ return `Ești director de servicii de fabricație aditivă și copywriter. Creează conținutul pentru pagina principală „Servicii de tipărire 3D & prototipare" a firmei RED INTERNET SALES.

${it.ctx}

Produ conform schemei: tagline spectaculos; intro (3-4 fraze); services (tipuri de servicii — ex: proiectare/design CAD, prototipare rapidă, serii mici de producție, printare format mare până la 1m³, multi-material & multicolor, piese funcționale/tehnice, reverse engineering & scanare 3D, post-procesare & finisare — fiecare cu icon emoji, title, desc); workflow (pașii colaborării, 4-6 pași); materials (lista de materiale oferite); industries (industrii deservite, min 6, name+desc); why_us (de ce noi, avantaje incl. cele 3 echipamente complementare + energie verde proprie); what_we_make (listă amplă, min 12, cu TOT ce se poate realiza — de la prototipuri multicolor pe Prusa XL, piese tehnice/funcționale pe RatRig, la piese uriașe până la 1 metru cub pe Modix). Ton spectaculos, profesionist. Română.` }

function enrichPrompt(draft, it){ return `Ești editor senior. Îmbunătățește conținutul (JSON) pentru „${it.name}" până la nivel SPECTACULOS și impecabil:
- adaugă aplicații și exemple concrete, moderne și convingătoare
- verifică coerența cu specificațiile reale; păstrează cifrele date, nu le contrazice
- fă textele vii, orientate spre beneficiul clientului, dar precise tehnic
- îmbogățește listele (mai multe capabilities/materiale/aplicații/what_we_make relevante)
Returnează JSON FINAL complet, conform aceleiași scheme, în română.

DRAFT:
${JSON.stringify(draft)}` }

const results = await pipeline(
  ITEMS,
  (it)=> agent(it.type==='overview'?draftOverview(it):draftMachine(it),
    {schema: it.type==='overview'?OVERVIEW_SCHEMA:MACHINE_SCHEMA, phase:'Draft', label:`draft:${it.slug}`, effort:'high'}),
  (draft, it)=> agent(enrichPrompt(draft, it),
    {schema: it.type==='overview'?OVERVIEW_SCHEMA:MACHINE_SCHEMA, phase:'Spectaculos', label:`spec:${it.slug}`, effort:'high'})
)

const out = results.map((r,i)=> r ? ({slug:ITEMS[i].slug, type:ITEMS[i].type, name:ITEMS[i].name, ...r}) : null).filter(Boolean)
log(`Gata: ${out.length}/${ITEMS.length} pagini`)
return out
