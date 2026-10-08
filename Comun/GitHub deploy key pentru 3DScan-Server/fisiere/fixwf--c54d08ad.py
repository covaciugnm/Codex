import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("""CERINTA PROPRIETARULUI: "daca sunt mai multe modele pe care le putem implementa pentru a obtine [rezultatul cel mai bun]" — adica: mai multe modele per sarcina,""",
    """CERINTA PROPRIETARULUI (trei mesaje): "daca sunt mai multe modele pe care le putem implementa pentru a obtine [rezultatul cel mai bun]"; "daca sunt mai multe modele / codecuri / versiuni de soft similare sau concurentiale pe care le putem implementa pentru a obtine - folosi in diverse sarcini - instaleaza toate si pune selector in setings - sa putem sa oprim din butoane"; "sau schimba aplicatia" (= comutarea trebuie posibila si din aplicatia iPhone) — adica: INSTALEAZA TOATE variantele concurente fezabile (nu doar 2-3) pentru fiecare sarcina — modele, codecuri, motoare software, backend-uri de inferenta si versiuni diferite ale aceluiasi soft side-by-side — fiecare pornit/oprit dintr-un SELECTOR IN SETARI cu butoane, pe site SI din aplicatia iOS; mai multe modele per sarcina,""")

rep("""F. (optional, daca timpul permite) Descriptori""", """G. CODECURI (pentru fluxurile scenei: inregistrare, transport, arhivare, previzualizare — calea bruta implicita ramane raw/necodificata, codecurile sunt OPTIUNI selectabile, iar cele cu pierderi sunt etichetate clar ca atare): video — raw YUV, FFV1 (lossless), H.264 (x264/openh264 — atentie licente/patente), HEVC/H.265 (x265), AV1 (SVT-AV1, libaom, dav1d), VP9; imagini — PNG, WebP lossless, JPEG XL lossless, JPEG; audio — PCM float32/int16, FLAC, WavPack, Opus, AAC; adancime — raw f32, zstd/lz4 lossless, RVL, PNG 16-bit; nor de puncte/mesh — PLY, Draco, glTF/GLB, meshoptimizer, LAS/LAZ. Toate prin ffmpeg/biblioteci in containere; transcodare la cerere din arhiva bruta (bruta nu se modifica); benchmark: raport de compresie, viteza, eroare (0 pentru lossless — verificat bit-exact).
H. MOTOARE SOFTWARE CONCURENTE: reconstructie 3D / fuziune — Open3D TSDF (ScalableTSDFVolume si VoxelBlockGrid), alternative CPU (ex. Voxblox / RTAB-Map / KinectFusion open-source — verifica licente si fezabilitate in container), GPU (nvblox — doar profil GPU, instalat dar dezactivat fara driver); backend-uri de inferenta — ONNX Runtime CPU, OpenVINO, (TensorRT/CUDA doar profil GPU); versiuni diferite ale aceluiasi model/soft instalate side-by-side cu selector (ex. D-FINE S/M/L, Whisper tiny/base/small/medium/large-v3-turbo, SAM 2.1 tiny/small/base/large).
F. (optional, daca timpul permite) Descriptori""")

rep("""6. Teste: fiecare adaptor""", """7. SELECTOR IN SETARI (obligatoriu), pe site SI in aplicatia iOS: API /api/admin/engines (listare cu stare, licenta, profil cpu/gpu, resurse, cifre de benchmark; PUT pentru pornit/oprit, alegere implicita per sarcina, ordine/ponderi in ansamblu, set productie vs cercetare) cu autorizare de admin — refoloseste mecanismul de rol al zonei admin (citeste Site/docs/ADMIN_ARHITECTURA.md pe origin/feat/admin-live; daca nu e inca disponibil, izoleaza verificarea intr-o singura functie usor de inlocuit la merge) si jurnal de audit al fiecarei comutari (cine, de unde: web sau aplicatie); aplicare LIVE fara redeploy (model-server si consumatorii reincarca configuratia; oprirea unui motor elibereaza memoria; un motor care nu poate porni — ex. GPU fara driver — apare dezactivat cu motivul); eveniment de schimbare propagat live (SSE/WebSocket) catre toti clientii, inclusiv aplicatia. Pagina web public/setari/ (fara inline, CSP, vendor local, responsive, tema intunecata): grupuri pe sarcini (Detectie, Vocabular deschis, Segmentare, Re-identificare, Sunete, Voce, Codecuri video/imagine/audio/adancime/3D, Reconstructie, Backend inferenta, Versiuni), fiecare intrare cu buton pornit/oprit, radio pentru implicit, badge licenta (comercial/cercetare/neclar), badge cpu/gpu, cifre benchmark, consum memorie live, stare (incarcat/oprit/eroare). Link din /admin/ fara a edita fisierele echipei admin. APLICATIA iOS: GET /api/app/settings (setarile pe care telefonul trebuie sa le respecte: codec de transport, ce fluxuri trimite, rezolutie/cadenta, motoare on-device vs server) + aceleasi operatii de comutare ca pe web pentru un utilizator admin autentificat din aplicatie (acelasi API, aceeasi autorizare), cu notificare live a schimbarilor; contract complet pentru ecranul de Setari din iOS in Site/docs/SETARI_MOTOARE.md (lista de controale, stari, erori, chei i18n propuse in cele 7 limbi).
6. Teste: fiecare adaptor""")

rep("""Alege candidatii de implementat acum pe CPU (minim 2-3 per domeniu A, B, C, D si 2 pentru E unde e fezabil), justificat. Imparte pe 3 echipe care nu editeaza aceleasi fisiere: platform (registru, model-server, evaluator, fuziune generica, compose), vision (adaptoare A/B/C/F + exporturi), audio (adaptoare D/E + exporturi). Push.""",
    """Include TOTI candidatii fezabili (pe CPU acum; cei doar-GPU instalati ca definitie si dezactivati cu motivul), cu set productie (licente comerciale) si set cercetare (necomercial/AGPL, oprit implicit, etichetat). Imparte pe 5 echipe care nu editeaza aceleasi fisiere: platform (registru, model-server, evaluator, fuziune generica, compose, API /api/admin/engines + /api/app/settings, aplicare si notificare live), vision (adaptoare A/B/C/F + exporturi + versiuni), audio (adaptoare D/E + versiuni), codecs-engines (G + H: codecuri, transcodare la cerere, motoare de reconstructie, backend-uri inferenta, benchmark bit-exact), settings-ui (public/setari/ + SETARI_MOTOARE.md pentru ecranul iOS). Push.""")

rep("""tasks: { type: 'object', properties: { vision: { type: 'array', items: { type: 'string' } }, audio: { type: 'array', items: { type: 'string' } }, platform: { type: 'array', items: { type: 'string' } } }, required: ['vision', 'audio', 'platform'] }""",
    """tasks: { type: 'object', properties: { vision: { type: 'array', items: { type: 'string' } }, audio: { type: 'array', items: { type: 'string' } }, platform: { type: 'array', items: { type: 'string' } }, 'codecs-engines': { type: 'array', items: { type: 'string' } }, 'settings-ui': { type: 'array', items: { type: 'string' } } }, required: ['vision', 'audio', 'platform', 'codecs-engines', 'settings-ui'] }""")

rep("""const impl = await parallel(['platform', 'vision', 'audio'].map(""", """const impl = await parallel(['platform', 'vision', 'audio', 'codecs-engines', 'settings-ui'].map(""")

rep("""  ['audio-voce', 'domeniile D, E'],""", """  ['audio-voce', 'domeniile D, E'],
  ['codecuri-motoare', 'domeniile G, H (codecuri, motoare de reconstructie/SLAM, backend-uri de inferenta, versiuni)'],""")

rep("""'OPERARE SI SECURITATE: limite CPU/RAM""", """'SELECTOR SI OPERARE: E2E prin tunel ssh -L + browserul integrat (mcp__Claude_Browser__*) pe pagina /setari/: fiecare buton porneste/opreste efectiv motorul (verifica in model-server si memoria eliberata), implicitul per sarcina se aplica live, /api/app/settings reflecta schimbarea si comutarea prin API ca din aplicatie (admin) functioneaza identic, notificare live, autorizare admin + jurnal de audit, codecurile lossless verificate bit-exact, SETARI_MOTOARE.md complet pentru iOS; limite CPU/RAM""")

rep("description: 'Registru de modele + evaluator + ansambluri", "description: 'Toate modelele/codecurile/motoarele concurente + selector pornit/oprit in setari (site si aplicatie) + evaluator + ansambluri")

rep("ROL: CERCETATOR ${k} (${d}). ", "ROL: CERCETATOR ${k} (${d}). Scopul e LISTA COMPLETA a variantelor concurente fezabile (proprietarul vrea sa le instalam pe toate cu selector), nu doar cele mai bune. ")

open(p, 'w', encoding='utf-8', newline='\n').write(s)
print("written")
