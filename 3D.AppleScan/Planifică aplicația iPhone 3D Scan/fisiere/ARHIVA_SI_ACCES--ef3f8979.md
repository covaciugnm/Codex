# Arhiva surselor și starea accesului

Bibliografia unificată conține 71 de înregistrări. Fiecare registru al specialiștilor precizează ce a fost consultat și ce afirmație susține sursa. Două articole MDPI au fost doar identificate: deschiderea integrală a returnat HTTP 429. Nu au fost folosite pentru validarea pragurilor aplicației.

## Fișiere originale salvate

- `fisiere_publice/NIST_TN1297.pdf`: ghidul NIST despre incertitudinea măsurării, descărcat de la URL oficial.
- `cad_fisiere_primare/CAD-S27_LICENSE.txt`: Open3D.
- `cad_fisiere_primare/CAD-S19_LICENSE.txt`: PDAL.
- `cad_fisiere_primare/CAD-S20_LICENSE.txt`: ezdxf.
- `cad_fisiere_primare/CAD-S28_LICENSE.txt`: lib3mf.
- `cad_fisiere_primare/CAD-S18_LICENSE.txt`: COLMAP.

Descărcările inițiale au eșuat deoarece mediul izolat nu avea credențialele TLS necesare. Accesul autorizat în afara izolării a permis descărcarea. Pentru COLMAP, vechea cale COPYING.txt a returnat 404; pagina GitHub a indicat fișierul curent LICENSE, care a fost salvat. Manifestele inițiale rămân în dosar pentru istoric; `manifest_recovery.json` și `manifest_colmap_recovery.json` consemnează recuperarea.

Fișierele de licență sunt instantanee de documentare ale ramurilor consultate, cu SHA-256. Ele nu fixează un commit al unei viitoare dependențe software. Înaintea implementării se aleg versiuni/commituri și se verifică toate dependențele, condițiile și drepturile relevante.

## Ce este păstrat prin rezumat și link

Documentația Apple, paginile furnizorilor, App Store și forumurile sunt reprezentate prin fișe originale și URL-uri. Nu au fost copiate integral pagini protejate sau recenzii. Schimbarea viitoare a unei pagini poate impune revalidarea afirmației înainte de implementare.

## Exemple

Fișierele STL, PLY și DXF din capitolul CAD au fost generate special pentru proiect. Ele sunt geometrii sintetice și nu provin dintr-o captură iPhone. Metadatele și controalele lor sunt salvate alături. DXF-ul exemplu este un contur minimal, fără cotele cerute viitorului exporter P0; rolul său este verificarea coordonatelor și unităților, nu demonstrarea funcției complete.
