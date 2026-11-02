# Loomy, skillul de traducere și TransAAS CLI — 1 noiembrie 2026

Au fost descărcate și verificate **67 de skilluri din catalogul public Loomy**, plus arhiva istorică `transaas01` 1.0.3, **patru executabile TransAAS CLI**, HeyCyan pentru alt hardware și documentația aferentă. În total: **86 de artefacte unice**, 380.352.911 octeți. Conținutul identic deja indexat în GitHub sau repetat între URL-uri este reutilizat prin referințe.

[Descărcări și toate skillurile](SKILLS.md) · [SUA/UE: conturi, aplicații și ce rămâne neconfirmat](INTERNATIONAL.md) · [Inventar SHA-256](file-inventory.json) · [Verificări](verification-summary.json)

## Skillul căutat și CLI-ul găsit

- [Skill oficial 1.0.4](skills/transaas01-1.0.4.zip), identificator `transaas01`, denumire „讯飞翻译”.
- [Arhivă 1.0.3](skills/transaas01-1.0.3.zip), disponibilă la adresa publică a distribuției. Variantele candidate 1.0.0–1.0.2 au răspuns 404; nu sunt prezentate drept descărcate.
- CLI pentru **Windows x64, macOS Intel, macOS Apple Silicon și Linux x64**: [Release cu executabilele](https://github.com/covaciugnm/iFLYTEK/releases/tag/iflytek-loomy-skills-2026-11-01).

Arhivele skillului includ `SKILL.md`, metadate și referințe pentru instalare, autentificare, MCP, traducere, istoricul traducerilor și teleprompter. Documentația identifică explicit `transaas login --web`, autentificarea SMS și serverul MCP integrat prin `transaas serve`. Acesta este CLI-ul TransAAS folosit de skill, distinct de CLI-ul generic `@xfyun/cli` arhivat anterior. Nu este un SDK Bluetooth pentru ochelari.

Catalogul a fost obținut printr-un **GET public fără sesiune sau token** la [serviciul oficial Loomy](https://loomyad.xunfei.cn/api/v1/skills/store/list). URL-urile ZIP provin din câmpul `download_url`, nu dintr-o instalare efectuată în contul unui utilizator. [Catalogul original](sources/loomy-skill-catalog.json) și [proveniența adresei publice](configuration-provenance.json) sunt păstrate.

Instrucțiunile skillului indică URL-uri HTTP pentru CLI; am verificat și **aceleași patru URL-uri prin HTTPS**, cu hashuri identice, fără a salva o a doua copie. Nu au fost folosite oglinzi neconfirmate pentru aceste executabile.

## Versiuni și verificări

Distribuția Loomy este 1.0.4; `SKILL.md` declară separat metadate interne 1.8.1 și `minimumCliVersion: v1.8.1`. Exemplul din referința de instalare menționează încă v1.7.0. Fișierele oficiale au fost păstrate nemodificate; diferența nu este ascunsă.

Nu s-au executat binarele pentru a confirma versiunea CLI sau funcționarea autentificării. [Metadatele statice Go](cli-static-metadata.json) identifică arhitecturile, Go 1.26.3 și revizia `8bc446660123751dae0f45a24fd99d8ded0eeb1a`, cu `vcs.modified=true`; acestea nu sunt echivalente cu o versiune semantică verificată prin rulare.

Verificările efectuate: SHA-256 și dimensiuni pentru toate cele 86 de artefacte, CRC32 și SHA-256 pentru conținutul celor **69 de arhive ZIP/XAPK**, inclusiv APK-urile split din XAPK, prezența `SKILL.md` în pachetele de skill și identitatea Android pentru HeyCyan. Formatele executabilelor sunt PE, Mach-O și ELF, corespunzătoare platformelor. Nu se pretinde verificarea semnăturii editorului sau validarea funcțională.

```powershell
node tools/verify-loomy-translate-skill-20261101.cjs --restore --remote
```

Comanda restaurează fișierele din Release, dacă lipsesc, și verifică hashurile locale și digesturile publicate în GitHub. Necesită Node.js și `gh` autentificat pentru repository-ul privat. Arhivele mici, documentele și inventarele sunt în Git; cele patru executabile CLI, pachetul mare `beautiful-html` și XAPK-ul HeyCyan sunt în Release.

## Alte modele de ochelari

HeyCyan **1.0.173_20261017**, pachet `com.glasssutdio.wear`, a fost descărcat ca XAPK și verificat din manifestele componentelor. Este arhivat separat în `other-hardware`, împreună cu două manuale și listările iOS/Google Play. [Identitate Android](other-hardware-android-identity.json). Nu este confirmat compatibil cu XF-AIGlasses-01.

Pentru iOS sunt păstrate linkurile și metadatele App Store. Nu a fost identificat un IPA public descărcabil pentru aceste aplicații.

„Lumi Samp” apare în fișele G100 de la [Gold Optical](https://gold-optical.com/ai-glasses/) și [Goodway](https://www.goodwaytechs.com/es/goodway-g100-smart-ai-camera-glasses.html), dar nu a fost identificat un pachet verificabil sub această denumire. Nu există un fișier descărcat prezentat drept aplicația Lumi Samp.

Skillurile au fost doar arhivate, nu instalate sau activate. Instrucțiunile din ele sunt conținut colectat, nu comenzi executate. Nu s-au modificat PATH-ul sau configurația aplicațiilor, nu s-au trimis SMS-uri și nu s-au accesat conturi, istorice de traducere sau alte date private.
