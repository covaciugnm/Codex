# TTS la nivel F5 pentru limbile noi EVA Learn — cercetare 2026-10-05

Doar cercetare: nimic descărcat sau instalat. Marcajele „neverificat” trebuie testate înainte de adoptare.

## 0. Licențe — de clarificat întâi

- **Greutățile oficiale F5-TTS (SWivid) sunt CC-BY-NC** (din cauza datelor Emilia); codul e MIT. Fine-tune-urile
  pornite din acel checkpoint moștenesc probabil restricția necomercială — **posibil și f5de/fr/es/en-eva existente**
  (de verificat juridic).
- Tot NC: OmniVoice (600+ limbi), Fish Audio S2 Pro, XTTS-v2, MMS-TTS, Habibi (pornit din F5), WenetSpeech-Yue/Wu,
  fine-tune-urile F5 comunitare (vietnameză, sinhala, thai).
- **Baze curate comercial:** VoxCPM2 (Apache-2.0, 2B, clonare cross-lingvală, 30 limbi + 9 dialecte chinezești),
  Fun-CosyVoice3 (Apache-2.0, deja descărcat), Qwen3-TTS-1.7B-Base (Apache-2.0), MOSS-TTS (Apache-2.0),
  IndicF5 (MIT; clonare doar cu permisiune), Indic Parler-TTS (Apache-2.0, fără clonare), Spark-TTS African (Apache).

## 1. Niveluri

**Gata acum (licență curată, de validat prin ascultare):**
- bn, mr, te, ta, kn, gu, ml, or → **IndicF5**
- yue, wuu, nan → **CosyVoice3 / VoxCPM2** (la nan: scriere Han vs Tâi-lô de testat)
- vi, th, my, km → **VoxCPM2**
- fa → **MOSS-TTS**
- ha, ig, yo → **Spark-TTS African** (calitate față de F5 nedovedită)

**Necesită fine-tune, date existente:**
- kk → KazakhTTS2 (271 h, CC-BY-4.0, comercial permis)
- uz → Common Voice (101 h, CC0), bază Qwen3-TTS
- kab → Common Voice (572 h, CC0)
- ur, ne, pnb → IndicVoices-R (CC-BY-4.0); pnb prin transliterare Shahmukhi→Gurmukhi (de testat)
- si → Google crowdsourced (CC-BY-SA); az → date slabe
- arz, ary → date există, reantrenare pe bază curată (VoxCPM2/Qwen3), nu pe Habibi
- am → WaxalNLP ~200 h (licență neverificată)

**Fără cale comercială viabilă azi:** tzm, rif, shi, apd, azb (ars: doar Azure ar-SA, mai aproape de araba standard).

## 2. Plan de pregătire

1. Clarificare licențe (inclusiv f5*-eva existente); pentru tot ce e nou: doar baze Apache/MIT.
2. Ordinea descărcărilor: VoxCPM2 → IndicF5 → MOSS-TTS-Local-1.7B → Qwen3-TTS-1.7B-Base → Indic Parler-TTS →
   (Habibi doar evaluare) → seturi de date KazakhTTS2, CV kab/uz/ur, IVR ur/ne, BibleTTS ha/yo.
   CosyVoice3 și Spark-TTS African sunt deja locale → test imediat.
3. **Aceeași voce Eva:** un clip master Eva 8–12 s, curat, cu transcriere exactă; direct pentru modelele cu clonare
   cross-lingvală (VoxCPM2, CosyVoice3, Qwen3, MOSS). Pentru IndicF5: întâi un clip „Eva” în limba țintă generat cu
   VoxCPM2 și validat cu Whisper, folosit apoi ca referință fixă pe limbă. Similaritate de vorbitor (ECAPA/WavLM-SV)
   față de master, prag inițial cos ≥ 0,75. Consimțământ documentat pentru vocea Eva.
4. **Verificare** (pipeline tts_cache): Whisper large-v3; MMS-1B-all pentru kab/tzm/shi/ha/ig/yo/am/my/km/si;
   Dolphin pentru yue/wuu/nan; respingere la CER > 5–8% / similaritate sub prag / UTMOS scăzut; 100 de clipuri
   ascultate de un nativ pe limbă.
5. **Fine-tune propriu:** ținta realistă ≥ 100–200 h, mai mulți vorbitori, pe bază Apache multilingvă;
   ~3–10 zile pe RTX 5080 / GB10 pe limbă (estimare neverificată).
6. Hardware: PyTorch pur pe GB10 aarch64 + CUDA 13; modelele 0,3–0,6B (CosyVoice3, IndicF5) și pe Jetson Orin;
   VoxCPM2 (2B) pe GB10 / RTX 5080. Compatibilitatea ARM64 neverificată pe model.
7. Fallback comercial (nivelul 3 / comparație): Azure Neural ~40 $/limbă (personal voice ~60 $),
   Google Chirp 3 HD ~75 $/limbă, ElevenLabs v3 ~250 $/limbă (pentru ~2,5 M caractere).

## Surse
https://github.com/SWivid/F5-TTS · https://huggingface.co/openbmb/VoxCPM2 · https://huggingface.co/ai4bharat/IndicF5 ·
https://huggingface.co/ai4bharat/indic-parler-tts-pretrained · https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 ·
https://github.com/QwenLM/Qwen3-TTS · https://huggingface.co/OpenMOSS-Team/MOSS-TTS · https://huggingface.co/k2-fsa/OmniVoice ·
https://huggingface.co/SWivid/Habibi-TTS · https://github.com/IS2AI/Kazakh_TTS · https://huggingface.co/datasets/ai4bharat/indicvoices_r ·
https://www.openslr.org/80/ · https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support ·
https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd · https://elevenlabs.io/docs/overview/models
