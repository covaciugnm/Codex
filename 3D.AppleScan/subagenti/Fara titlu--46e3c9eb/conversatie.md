# Fara titlu

ID: `01a1123b-7251-7df1-8f4a-24df46e3c9eb`  
Proiect: 3D.AppleScan  
Export UTC: 2026-10-08T14:13:28.280906+00:00

Mesajele sunt redate integral mai jos. Rezultatele instrumentelor sunt în rezultate.md și istoric.json. Fișierele recuperate sunt în fisiere/.

## Asistent

Raportul specialistului iPhone/iOS este salvat:

[01-specialist-iphone-ios.md](C:/Users/User/.codex/visualizations/2026/10/05/01a10ade-37d0-7f91-95c0-23125e63e891/plan-2026-10-06/01-specialist-iphone-ios.md)

Constatări care trebuie incluse în planul principal:

- **Hardware confirmat:** Apple listează iPhone 18 Pro Max 1 TB, iOS 27, A20 Pro, LiDAR, TrueDepth, USB 3 și UWB. Stocarea nu determină memoria disponibilă modelelor.
- **Stack modern:** evaluare Core AI și Foundation Models iOS 27, păstrând Core ML ca baseline. Toolkit-ul Foundation Models adapter 26.0.0 este incompatibil cu iOS 27.
- **6DoF:** noul ARKit iOS urmărește referințe Create ML pentru obiecte mobile. Maximum **10 `.referenceobject`** cumulat; fără amestec cu `.arobject`. Catalogul server poate fi mare, setul activ se selectează după sarcină.
- **Mai mulți roboți:** ARKit CollaborationData pentru aliniere locală, recomandat până la **patru participanți**; memorie semantică și reconciliere versionată pe server. UWB oferă observații auxiliare, nu poziție 6DoF completă.
- **Captură:** un coordonator distribuie cadre timestamped. Compatibilitatea ARKit/TrueDepth/LiDAR/MultiCam trebuie demonstrată pe telefon; nu rezultă din existența camerelor.
- **Voce:** benchmark SpeechAnalyzer versus FluidAudio/Argmax; FluidAudio oferă diarizare și speaker embeddings. Româna, zgomotul motoarelor și anularea ecoului trebuie testate.
- **LLM:** opțiuni local Foundation Models, model propriu Core AI, server propriu și PCC. PCC necesită entitlement, disponibilitate și cote; nu devine dependență obligatorie.
- **Verificare:** probe de relocalizare, identități, două telefoane, cadre întârziate, întreruperi și test prelungit în montura finală.

Raportul separă explicit capabilitățile documentate de propunerile și performanțele încă nevalidate. Auditorul a fost notificat.

## Asistent

Addendumul este salvat: [03-modele-voce-llm.md](C:/Users/User/.codex/visualizations/2026/10/05/01a10ade-37d0-7f91-95c0-23125e63e891/plan-2026-10-06/03-modele-voce-llm.md).

Include:

- LLM/VLM: Qwen3.5-9B, Qwen3.6-35B-A3B și Gemma4-31B-it.
- TTS română: Apple, Piper și XTTS Romanian v2, cu restricțiile explicate.
- Fețe: AuraFace, SFace și InsightFace condiționat de licența greutăților.
- Calculul memoriei, compatibilitatea telefon/server și verificările obligatorii R0.

Auditorul a primit fișierul. Raportul original nu a fost modificat.
