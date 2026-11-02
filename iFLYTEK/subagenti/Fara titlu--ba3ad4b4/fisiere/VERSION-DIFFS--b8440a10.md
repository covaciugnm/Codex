# Comparatia statica a versiunilor APK/XAPK

Data: 1 noiembrie 2026. Sunt comparate toate cele 14 intrari unice din catalog: 12 ale furnizorilor si doua derivate local. Manifestele de intrare nu au fost modificate.

Constatare relevanta: fiecare canal FY10030001/FY10030002 difera fata de APK-ul oficial implicit prin cinci fisiere: trei intrari de semnatura v1 si doua biblioteci native, `libapp.so` si `libdartjni.so`. `assets/channel.config` si DEX-urile sunt identice. Aceste variante nu pot fi descrise corect ca diferind numai printr-un fisier de canal; cauza si efectele diferentelor native nu sunt stabilite de comparatia hashurilor.

La Bavvo, seturile de splituri difera in perechile 1112->1179 si 1211->1222. De exemplu, pachetul 1222 disponibil contine armeabi-v7a/mdpi, iar 1211 contine arm64-v8a/hdpi si franceza. Numarul de fisiere adaugate/eliminate reflecta si aceasta selectie de pachete, nu numai evolutia aplicatiei.

Comparatia foloseste SHA-256 pe cheia `component/path`. Componenta principala XAPK `package.apk` devine `base.apk`; numele spliturilor sunt pastrate. Listele complete added/changed/removed/identical, hashurile si numarul de octeti sunt in [VERSION-DIFFS.json](VERSION-DIFFS.json). `rawEntriesDigest` identifica exact inventarul brut comparat, chiar daca ulterior se adauga rezultate de decompilare in manifest.

| De la | La | Identice | Schimbate | Adaugate | Eliminate |
|---|---|---:|---:|---:|---:|
| bavvo-1.0.1112 | bavvo-1.0.1179 | 1262 | 65 | 186 | 142 |
| bavvo-1.0.1179 | bavvo-1.0.1197 | 1477 | 36 | 0 | 0 |
| bavvo-1.0.1197 | bavvo-1.0.1205 | 1489 | 24 | 0 | 0 |
| bavvo-1.0.1205 | bavvo-1.0.1211 | 1486 | 27 | 1 | 0 |
| bavvo-1.0.1211 | bavvo-1.0.1222 | 1398 | 20 | 97 | 96 |
| iflytranslate-official | translate-channel-FY10030001 | 2336 | 5 | 0 | 0 |
| iflytranslate-official | translate-channel-FY10030002 | 2336 | 5 | 0 | 0 |
| iflytranslate-official | translate-xlhs-current | 2318 | 21 | 2 | 2 |
| iflytranslate-official | iflytek-1.0.3899-full-rebuilt | 1269 | 199 | 870 | 873 |
| iflytranslate-official | iflytek-1.0.3899-romania40 | 1268 | 200 | 870 | 873 |

## bavvo-1.0.1112 -> bavvo-1.0.1179

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 3 | 2 | 1 |
| android-resources | 706 | 9 | 48 | 134 |
| dex | 0 | 2 | 0 | 0 |
| flutter-assets | 468 | 18 | 41 | 1 |
| native | 2 | 8 | 17 | 0 |
| other | 18 | 2 | 33 | 1 |
| other-assets | 13 | 2 | 31 | 0 |
| other-metadata | 55 | 15 | 8 | 2 |
| signature-v1 | 0 | 6 | 6 | 3 |

Splituri adaugate: config.fr.apk, config.hdpi.apk. Splituri eliminate: config.mdpi.apk. Diferentele de ABI, limba si densitate trebuie separate de modificari functionale.

## bavvo-1.0.1179 -> bavvo-1.0.1197

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 5 | 0 | 0 |
| android-resources | 763 | 0 | 0 | 0 |
| dex | 0 | 2 | 0 | 0 |
| flutter-assets | 515 | 12 | 0 | 0 |
| native | 24 | 3 | 0 | 0 |
| other | 53 | 0 | 0 | 0 |
| other-assets | 44 | 2 | 0 | 0 |
| other-metadata | 78 | 0 | 0 | 0 |
| signature-v1 | 0 | 12 | 0 | 0 |

## bavvo-1.0.1197 -> bavvo-1.0.1205

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 5 | 0 | 0 |
| android-resources | 763 | 0 | 0 | 0 |
| dex | 0 | 2 | 0 | 0 |
| flutter-assets | 527 | 0 | 0 | 0 |
| native | 24 | 3 | 0 | 0 |
| other | 53 | 0 | 0 | 0 |
| other-assets | 44 | 2 | 0 | 0 |
| other-metadata | 78 | 0 | 0 | 0 |
| signature-v1 | 0 | 12 | 0 | 0 |

## bavvo-1.0.1205 -> bavvo-1.0.1211

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 5 | 0 | 0 |
| android-resources | 763 | 0 | 0 | 0 |
| dex | 0 | 2 | 0 | 0 |
| flutter-assets | 524 | 3 | 1 | 0 |
| native | 24 | 3 | 0 | 0 |
| other | 53 | 0 | 0 | 0 |
| other-assets | 44 | 2 | 0 | 0 |
| other-metadata | 78 | 0 | 0 | 0 |
| signature-v1 | 0 | 12 | 0 | 0 |

## bavvo-1.0.1211 -> bavvo-1.0.1222

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 2 | 2 | 3 |
| android-resources | 715 | 0 | 47 | 48 |
| dex | 0 | 2 | 0 | 0 |
| flutter-assets | 518 | 4 | 31 | 6 |
| native | 0 | 0 | 9 | 27 |
| other | 43 | 7 | 2 | 3 |
| other-assets | 44 | 2 | 0 | 0 |
| other-metadata | 78 | 0 | 0 | 0 |
| signature-v1 | 0 | 3 | 6 | 9 |

Splituri adaugate: config.armeabi_v7a.apk, config.mdpi.apk. Splituri eliminate: config.arm64_v8a.apk, config.fr.apk, config.hdpi.apk. Diferentele de ABI, limba si densitate trebuie separate de modificari functionale.

## iflytranslate-official -> translate-channel-FY10030001

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 1 | 0 | 0 | 0 |
| android-resources | 1062 | 0 | 0 | 0 |
| channel-config | 1 | 0 | 0 | 0 |
| dex | 6 | 0 | 0 | 0 |
| flutter-assets | 1002 | 0 | 0 | 0 |
| native | 78 | 2 | 0 | 0 |
| other | 43 | 0 | 0 | 0 |
| other-assets | 43 | 0 | 0 | 0 |
| other-metadata | 100 | 0 | 0 | 0 |
| signature-v1 | 0 | 3 | 0 | 0 |

Cai neidentice:
- `base.apk/META-INF/CERT.RSA` (signature-v1).
- `base.apk/META-INF/CERT.SF` (signature-v1).
- `base.apk/META-INF/MANIFEST.MF` (signature-v1).
- `base.apk/lib/arm64-v8a/libapp.so` (native).
- `base.apk/lib/arm64-v8a/libdartjni.so` (native).

Diferentele nu se limiteaza la configuratia de canal; consultati categoriile si listele complete.

## iflytranslate-official -> translate-channel-FY10030002

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 1 | 0 | 0 | 0 |
| android-resources | 1062 | 0 | 0 | 0 |
| channel-config | 1 | 0 | 0 | 0 |
| dex | 6 | 0 | 0 | 0 |
| flutter-assets | 1002 | 0 | 0 | 0 |
| native | 78 | 2 | 0 | 0 |
| other | 43 | 0 | 0 | 0 |
| other-assets | 43 | 0 | 0 | 0 |
| other-metadata | 100 | 0 | 0 | 0 |
| signature-v1 | 0 | 3 | 0 | 0 |

Cai neidentice:
- `base.apk/META-INF/CERT.RSA` (signature-v1).
- `base.apk/META-INF/CERT.SF` (signature-v1).
- `base.apk/META-INF/MANIFEST.MF` (signature-v1).
- `base.apk/lib/arm64-v8a/libapp.so` (native).
- `base.apk/lib/arm64-v8a/libdartjni.so` (native).

Diferentele nu se limiteaza la configuratia de canal; consultati categoriile si listele complete.

## iflytranslate-official -> translate-xlhs-current

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 1 | 0 | 0 |
| android-resources | 1062 | 0 | 0 | 0 |
| channel-config | 1 | 0 | 0 | 0 |
| dex | 0 | 6 | 0 | 0 |
| flutter-assets | 995 | 7 | 0 | 0 |
| native | 78 | 2 | 0 | 0 |
| other | 43 | 0 | 0 | 0 |
| other-assets | 41 | 2 | 0 | 0 |
| other-metadata | 98 | 0 | 2 | 2 |
| signature-v1 | 0 | 3 | 0 | 0 |

## iflytranslate-official -> iflytek-1.0.3899-full-rebuilt

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 1 | 0 | 0 |
| android-resources | 0 | 192 | 870 | 870 |
| channel-config | 1 | 0 | 0 | 0 |
| dex | 0 | 6 | 0 | 0 |
| flutter-assets | 1002 | 0 | 0 | 0 |
| native | 80 | 0 | 0 | 0 |
| other | 43 | 0 | 0 | 0 |
| other-assets | 43 | 0 | 0 | 0 |
| other-metadata | 100 | 0 | 0 | 0 |
| signature-v1 | 0 | 0 | 0 | 3 |

## iflytranslate-official -> iflytek-1.0.3899-romania40

| Categorie | Identice | Schimbate | Adaugate | Eliminate |
|---|---:|---:|---:|---:|
| android-manifest | 0 | 1 | 0 | 0 |
| android-resources | 0 | 192 | 870 | 870 |
| channel-config | 1 | 0 | 0 | 0 |
| dex | 0 | 6 | 0 | 0 |
| flutter-assets | 1002 | 0 | 0 | 0 |
| native | 79 | 1 | 0 | 0 |
| other | 43 | 0 | 0 | 0 |
| other-assets | 43 | 0 | 0 | 0 |
| other-metadata | 100 | 0 | 0 | 0 |
| signature-v1 | 0 | 0 | 0 | 3 |

## Aplicatii fara pereche

- `com.ainote.mobile.doxent_oversea_app` 3.1.5: exista un singur input descarcat in inventarul curent; nu este posibila o comparatie intre versiuni.
- `com.iflytek.loomy.mobile` 0.0.8: exista un singur input descarcat in inventarul curent; nu este posibila o comparatie intre versiuni.

## Limite

Sunt comparate fisierele brute, nu pseudocodul decompilat. Categoria `signature-v1` acopera numai fisierele de semnatura din ZIP; blocurile APK v2/v3 si metadatele containerului nu sunt analizate aici. Nu se deduc certificate valide sau aceeasi identitate a semnatarului numai din aceste liste. Manifestele si resursele Android binare pot varia din cauza reambalarii. Schimbarea unui DEX ori a unei biblioteci native nu probeaza o functie noua. Nu au fost executate aplicatii, autentificari sau servicii cloud.
