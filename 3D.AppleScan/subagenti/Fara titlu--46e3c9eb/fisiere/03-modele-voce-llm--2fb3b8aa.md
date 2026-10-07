# Addendum — shortlist LLM/VLM, voce română și embeddings faciale

Data verificării: **2026-10-06, Europe/Bucharest**. Cercetare concentrată în surse primare; shortlist executabil pentru benchmark, nu clasament universal și nici rezultate măsurate pe serverul EVA. Nu s-au instalat modele. GPU-ul, VRAM-ul disponibil, sistemul de operare și numărul maxim simultan de roboți ai serverului rămân de inventariat în R0.

## 1. LLM/VLM pe server: trei candidați concreți

| Rol | Checkpoint first-party | Motivație pentru EVA | Licență greutăți verificată |
|---|---|---|---|
| Primar de integrare și baseline compact | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Text + imagini într-un model relativ compact; potrivit pentru prima integrare cu obiecte/context și evaluarea costului pe robot | Apache-2.0 |
| Challenger pentru calitate și sarcini complexe | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | Model cu encoder vizual, 35B parametri totali ai componentei de limbaj și 3B activați; comparație pentru alegerea obiectului, plan de sarcină și răspuns structurat | Apache-2.0 |
| Challenger din altă familie | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) | Instrucțiuni și imagini; permite verificarea erorilor sistematice ale familiei Qwen pe aceleași scene | Apache-2.0 în cardul acestui checkpoint; nu extrapolăm licența modelelor Gemma mai vechi |

Aceste modele au greutăți publicate și documentație de integrare verificabile la data planului. Nu echivalăm un model anunțat sau disponibil numai prin API cu unul instalabil pe server. Nu declarăm acest shortlist exhaustiv; verificarea release-urilor first-party se repetă în R0 înaintea blocării versiunilor.

Runtime primar propus: vLLM, cu versiunea validată pentru checkpoint, CUDA și GPU. Pentru Qwen3.6, cardul recomandă vLLM >=0.19.0 sau SGLang >=0.5.10. În livrare se blochează versiunea exactă și digestul imaginii, nu `latest`. Transformers este traseul de referință pentru smoke test/paritate. **Licența runtime-ului este distinctă de licența greutăților**: [vLLM LICENSE](https://github.com/vllm-project/vllm/blob/main/LICENSE) și [Transformers LICENSE](https://github.com/huggingface/transformers/blob/main/LICENSE) sunt Apache-2.0; dependențele și driverele se inventariază separat.

Integrare iPhone: telefonul trimite doar keyframes/cropuri necesare, împreună cu `frame_id`, `capture_time`, ID-urile obiectelor și relațiile validate geometric. Serverul răspunde în schemă structurată cu sursele folosite. VLM-ul nu furnizează autoritatea metrică pentru navigare: estimările sale semantice se verifică prin depth/TF/world model. Modelele server nu trebuie convertite și încărcate automat integral pe iPhone; acesta păstrează modelul compact local și fallback-ul descrise în raportul iOS.

### Calculul memoriei, fără promisiuni de viteză

Estimare aritmetică pentru greutăți: `N_parametri × biți / 8`. GB este zecimal; GiB = bytes/2^30. Valorile de mai jos folosesc numărul nominal din numele modelului, nu înlocuiesc suma tensorilor checkpoint-ului.

| Mărime nominală | BF16, numai greutăți | 4 biți ideal, numai greutăți |
|---|---:|---:|
| 9B | 18 GB / 16,76 GiB | 4,5 GB / 4,19 GiB |
| 35B | 70 GB / 65,19 GiB | 17,5 GB / 16,30 GiB |
| 31B | 62 GB / 57,74 GiB | 15,5 GB / 14,44 GiB |

La acestea se adaugă scale/zero-points și tensori necuantizați, encoderul vizual dacă nu este inclus în numărul nominal, KV/state cache, activări, workspace, CUDA graphs și costul concurenței. Arhitecturile hibride au și stare recurentă; formula KV a unui Transformer standard nu se aplică integral. La MoE, 3B activați descriu calculul, nu înlocuiesc stocarea tuturor experților. Offload-ul modifică distribuția RAM/VRAM și latența, fără a elimina memoria necesară.

R0 determină memoria reală pentru 1, 2, 4 și numărul țintă de cereri simultane, cu imagini și contextul EVA. Nu deducem tokens/s din VRAM și nu afirmăm că un GPU de 24 GB poate susține un model 35B la 4 biți pentru orice context. Bugetul de context se justifică prin test: pornim cu context scurt și retrieval; cererile lungi merg în coadă separată. Hardware-ul se alege după acest profil, nu după numele modelului.

## 2. TTS română: trei trasee, cu statut diferit

| Rol | Implementare | Telefon/server | Licență și condiții |
|---|---|---|---|
| Primar offline pe telefon | AVSpeechSynthesizer + voce cu locale ro-RO găsită prin `speechVoices()` | iPhone | API/voce de sistem Apple; nu distribuim greutăți proprii. Disponibilitatea exactă și funcționarea offline se verifică pe dispozitiv, inclusiv după descărcarea vocii. [API Apple](https://developer.apple.com/documentation/avfaudio/avspeechsynthesisvoice/speechvoices()) |
| Primar de evaluare server cu resurse reduse | Piper `ro_RO-mihai-medium` | CPU server, apoi opțional port mobil numai după analiza distribuției | Engine actual OHF piper1-gpl: GPL-3.0. Repo de voci afișează MIT; cardul specific declară dataset CC0 și finetuning din lessac. R0 verifică explicit licența greutăților/derivării și păstrează fișierele de licență; CC0 al datelor singur nu dovedește licența greutăților. [Engine](https://github.com/OHF-Voice/piper1-gpl), [card voce](https://huggingface.co/rhasspy/piper-voices/blob/main/ro/ro_RO/mihai/medium/MODEL_CARD) |
| Challenger pentru evaluare necomercială a calității | `eduardem/xtts-v2-romanian-v2` | Server | Greutăți CPML; codul runtime Coqui este MPL-2.0. CPML permite numai utilizare necomercială a modelului și outputului: nu selectăm acest checkpoint pentru livrare comercială fără drepturi distincte. [Card autor](https://huggingface.co/eduardem/xtts-v2-romanian-v2), [licența modelului de bază](https://huggingface.co/coqui/XTTS-v2/blob/main/LICENSE.txt), [runtime menținut](https://github.com/idiap/coqui-ai-TTS) |

XTTS Romanian v2 cere normalizarea diacriticelor cu sedilă la virgulă dedesubt și utilizarea pipeline-ului autorului. Acesta este un candidat de cercetare, nu fallback-ul implicit al producției. Nu înlocuim un motor valid cu unul nou doar pentru naturalitatea câtorva mostre. Comparăm inteligibilitatea, numere/adrese/nume de obiecte, timpii până la primul audio, întreruperea enunțului, RAM și evaluarea umană în română. Pentru voce personalizată se păstrează proveniența și autorizarea înrolării.

Nu deducem suportul românei pentru Kokoro, PocketTTS sau alte variante din sintagma „multilingual”; selecția presupune model card care listează limba și probe locale. Pentru producție, dacă vocea Apple/Piper nu trece criteriile, R0 extinde compararea cu un furnizor comercial care documentează ro-RO și condițiile de prelucrare a textului. Nu se achiziționează serviciu prin acest plan.

## 3. Embeddings faciale: păstrare baseline și două alternative

| Rol | Checkpoint/metodă | Licență cod vs greutăți | Compatibilitate și gate |
|---|---|---|---|
| Primar, continuitate cu proiectul | [fal/AuraFace-v1](https://huggingface.co/fal/AuraFace-v1) | Model card: Apache-2.0. InsightFace folosit ca wrapper are cod MIT; nu înseamnă că orice model descărcat de wrapper este Apache/MIT | ONNX pe server; Core ML existent/convertit pe telefon verificat prin paritatea embeddingurilor, crop, RGB/BGR și normalizare |
| Challenger compact | [OpenCV Zoo SFace / MobileFaceNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface) | README declară toate fișierele directorului Apache-2.0, incluzând modelele ONNX publicate | Baseline cu amprentă redusă; conversie Core ML numai după verificarea operatorilor și scorurilor; nu pretindem că modelul din 2021 este cel mai nou |
| Challenger server condiționat de drepturi | [InsightFace actual, ex. buffalo_l sau pachet licențiat](https://github.com/deepinsight/insightface) | Cod MIT; greutățile publicate/descărcate automat sunt în general pentru cercetare necomercială conform proiectului. Pentru utilizare comercială se verifică pachetul și licența obținută | Evaluare izolată numai în condițiile permise; în producție se activează exclusiv modelul verificat, fără autodownload implicit |

Proiectul InsightFace indică actualizări 2.1 din 2026-10-03, dar existența lor nu transformă automat toate modelele în resurse cu utilizare comercială permisă. AuraFace/SFace reprezintă alegeri verificabile pentru comparație; sursa modelelor FaceNet deja din aplicație trebuie de asemenea inclusă în inventarul R0.

Fiecare embedding persistent păstrează `model_id`, `model_revision`, `preprocessing_version`, dimensiune și spațiul vectorial. Nu comparăm direct vectori AuraFace cu SFace și nu suprascriem enrollments la schimbarea motorului. Testul măsoară false accept/reject și unknown rejection pe persoane din cohorta autorizată, diverse distanțe/iluminări și replay. Pragul se calibrează pe date separate de evaluare. Identificarea facială nu dovedește singură persoană vie și nu este echivalentă cu Face ID.

## 4. R0: ce trebuie înghețat înainte de instalare

Pentru fiecare model ales, inginerul ML și auditorul completează manifestul: repo first-party, commit SHA complet, SHA-256 pentru toate greutățile/tokenizer/config, text licență greutăți, cod și dependențe, format/precizie, script de conversie și container digest. Hash-urile artefactelor nu au fost calculate în această cercetare și rămân gate obligatoriu R0; nu se folosesc hash-uri de pagini README drept hash de checkpoint.

Inventarul serverului include GPU/compute capability/VRAM liber, RAM, disc, driver, CUDA și arhitectura CPU. Se verifică suportul runtime pentru model și cuantizarea aleasă; FP8/FP4 nu se activează doar pentru că fișierul există. Se execută smoke test cu schema EVA, input imagine și tool call, apoi sarcină concurentă cu geometrie+STT. Manifestul rezultat stabilește exact ce se instalează pe server și ce pe telefon.

Criteriu de promovare propus: modelul nou trece toate testele de schemă/izolare/timeout și îmbunătățește metricile de task sau reduce costul fără regresie acceptată. Rezultatele nesigure cer reobservare ori clarificare, iar executorul respinge coordonate/referințe inventate. Flota distribuie versiuni prin rollout limitat, păstrează versiunea anterioară și poate reveni automat după degradare. Acestea sunt condiții de implementare, nu rezultate obținute deja.
