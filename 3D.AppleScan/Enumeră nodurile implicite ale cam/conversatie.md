# Enumeră nodurile implicite ale cam

ID: `01a13459-cc01-77b3-a892-11b6bbc1a24c`  
Proiect: 3D.AppleScan  
Export UTC: 2026-10-13T08:28:59.767902+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Utilizator

# Files mentioned by the user:

## Photo 1.jpg: C:\Users\User\.codex\codex-remote-attachments\01a13459-cc01-77b3-a892-11b6bbc1a24c\F3565DB1-9E38-4593-B4DB-F12787601E4E\1-Photo-1.jpg

## My request:
Ce noduri rulează implicit pe procesorul camerei ? Care este lista completă care sunt încărcate implicit în cameră și dacă sunt sau nu pornite / ce are în aplicație și se pot încărca ulterior.

[Atașament / conținut non-text: {"type": "localImage", "detail": null, "path": "C:\\Users\\User\\.codex\\codex-remote-attachments\\01a13459-cc01-77b3-a892-11b6bbc1a24c\\F3565DB1-9E38-4593-B4DB-F12787601E4E\\1-Photo-1.jpg"}]

## Asistent

Voi verifica modelul OAK-D-Pro AF din fotografie și codul aplicației, ca să separ nodurile pornite implicit de cele disponibile pentru activare ulterioară.


## Asistent

Documentația confirmă că nodurile de procesare sunt definite de pipeline-ul aplicației; modelul camerei nu stabilește singur ce rulează. Unitatea S: nu este accesibilă în această sesiune, așa că nu pot confirma încă lista activată de aplicația voastră. Voi distinge această limită de capabilitățile camerei.


## Asistent

Camera din fotografie este **Luxonis OAK-D-Pro AF, SKU A00546**, cu procesor **RVC2**. „AF” înseamnă autofocus pentru camera RGB. [Specificațiile modelului](https://docs.luxonis.com/hardware/products/OAK-D%20Pro)

**Nu există o listă fixă de noduri de procesare care pornesc automat din fabrică.** În utilizarea obișnuită prin USB, aplicația construiește un *pipeline* — nodurile și conexiunile dintre ele — și îl încarcă în cameră împreună cu firmware-ul și resursele necesare. Așadar, „disponibil în DepthAI”, „încărcat în cameră” și „rulează” sunt trei lucruri diferite. [Funcționarea Device/Pipeline](https://docs.luxonis.com/software-v3/ai-inference/conversion/rvc-conversion/offline/)

**Ce este implicit și ce trebuie activat**

| Componentă / funcție | Starea implicită, fără un pipeline al aplicației |
|---|---|
| Captură RGB | Nu există un flux de aplicație pornit automat; trebuie configurat nodul camerei |
| Captură stereo stânga/dreapta | Trebuie configurate nodurile camerelor |
| Calcul adâncime | Nu pornește doar prin conectarea camerei; trebuie `StereoDepth` |
| Inferență AI / detecție obiecte | Nu există un model universal pornit; aplicația trebuie să furnizeze modelul și nodurile |
| Tracking, procesare imagine, codare video | Se execută dacă sunt incluse și alimentate cu date în pipeline |
| Date IMU | Aplicația trebuie să configureze nodul și rapoartele dorite |
| Proiector IR cu puncte | **Oprit implicit** |
| Iluminator IR | **Oprit implicit** |

Ultimele două sunt dispozitive hardware controlate prin API, **nu noduri separate**. Luxonis confirmă explicit că ambele sunt oprite implicit. [Controlul IR](https://docs.luxonis.com/hardware/products/OAK-D%20Pro)

**Ce se poate executa pe procesorul camerei**

Tabelul de mai jos este un inventar al principalelor funcții disponibile, **nu lista confirmată a nodurilor încărcate în aplicația voastră**. Numele și disponibilitatea exactă depind de versiunea DepthAI.

| Nod / familie de noduri | Ce face în cameră |
|---|---|
| `Camera`; în API-ul v2, `ColorCamera`, `MonoCamera` | Captură RGB și monocromă |
| `StereoDepth` | Rectificare stereo, disparitate, adâncime și filtrare configurată |
| `ImageManip` | Redimensionare, decupare și transformări de imagine |
| `NeuralNetwork` | Inferență cu un model compatibil RVC2, încărcat de aplicație |
| Noduri de detecție, inclusiv variantele YOLO/MobileNet din v2 | Inferență și interpretarea detecțiilor, conform versiunii API |
| `SpatialLocationCalculator` | Coordonate XYZ pentru regiuni din harta de adâncime |
| `ObjectTracker` | Urmărirea obiectelor detectate |
| `FeatureTracker` | Detectarea și urmărirea punctelor caracteristice |
| `EdgeDetector` | Detectarea contururilor |
| `VideoEncoder` | Codare H.264, H.265 sau MJPEG |
| `IMU` | Citirea senzorilor inerțiali |
| `Script` | Logică personalizată în mediul Python limitat al camerei |
| `Sync`, `MessageDemux` | Sincronizarea și separarea mesajelor |
| `SystemLogger` | Telemetrie despre dispozitiv |
| `XLinkIn`, `XLinkOut`, în special în v2 | Transferul datelor între calculator și cameră |

Aceste funcții folosesc diferite resurse ale RVC2: procesoare, acceleratoare de imagine, stereo și AI. Nu toate rulează pe același nucleu CPU. [Arhitectura RVC2](https://docs.luxonis.com/hardware/platform/rvc/rvc2), [API-ul nodurilor](https://docs.luxonis.com/software-v3/depthai/api/cpp)

**Pentru scanare 3D, contează mult ce rămâne pe calculator:**

- În documentația actuală DepthAI v3, `PointCloud` rulează **pe calculator pentru RVC2**. Faptul că adâncimea este calculată în cameră nu înseamnă că și norul de puncte este calculat acolo. [PointCloud](https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes/pointcloud)
- `RGBD` procesează datele pe host, iar `AprilTag` rulează tot pe calculator la RVC2. [RGBD](https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/rgbd), [AprilTag](https://docs.luxonis.com/software-v3/depthai/depthai-components/nodes/april_tag)
- Nodurile host precum `BasaltVIO` și `RTABMapSLAM` folosesc calculatorul conectat prin USB. [Host Nodes](https://docs.luxonis.com/software-v3/depthai/depthai-components/host_nodes)

**Se pot adăuga ulterior?** Da, prin modificarea pipeline-ului și, unde este cazul, furnizarea modelelor AI. Nu sunt neapărat module deja încărcate care așteaptă un buton „Pornit”. Adăugarea unui nod poate necesita recrearea pipeline-ului; unele setări ale nodurilor existente pot fi schimbate în timpul funcționării.

**Lista completă pentru aplicația voastră rămâne de verificat:** unitatea `S:\3dscan.eva-org.com` nu este vizibilă în această sesiune, nici după încercarea cu acces extins. Am nevoie de o cale accesibilă către proiect sau de fișierul care construiește pipeline-ul și versiunea DepthAI. Din acestea pot determina exact: **nod, loc de execuție, încărcat la pornire, condiție de activare și funcții disponibile ulterior**.
