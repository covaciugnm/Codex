# Unelte de traducere specializate pe limbi — cercetare 2026-10-05

Context: aplicație comercială → licența contează. Volumul (~13 M caractere × 36 de limbi ≈ 470 M) depășește
cu mult nivelurile gratuite online (Azure F0: 2 M caractere/lună, Google: 500 k/lună), care rămân doar
pentru verificări pe eșantioane.

## Modele locale, cu licență comercială

| Model | Licență | Limbi relevante pentru noi |
|---|---|---|
| **TranslateGemma** 4B/12B/27B (Google) | Gemma Terms (comercial DA) | Tamazight Tifinagh + latin, arz, ar-MA (ary), apd, pa-Arab (Shahmukhi), yue, ha, ig, yo, am, si, km, my, ne, fa, vi, th, kk, Indic |
| **IndicTrans2** 1B (AI4Bharat) | MIT | bn, ur, mr, te, ta, kn, gu, ml, or, ne (doar din engleză; fără Sinhala) |
| **MiLMMT-46** 12B (Xiaomi) | Gemma | kk, uz, az, fa, km, my, th, vi, yue (de validat) |
| **MADLAD-400** 10B | Apache-2.0 | kab, shi, tzm, wuu, azb (calitate slabă, „a doua opinie”) |
| Atlas-Chat 27B / Nile-Chat 12B | Gemma | araba marocană / egipteană (post-editare dialectală) |

Excluse pentru uz comercial: NLLB-200, Aya Expanse, Tower+, KazLLM, Taigi-Llama (CC-BY-NC);
Hunyuan-MT (licența Tencent nu se aplică în UE).

Fără unealtă comercială dedicată: **wuu** (Qwen e cel mai stabil), **nan** în caractere Han, **ars** (Najdi).
**kk-Latn**: traducere în chirilică + transliterare deterministă (alfabetul oficial 2021).

## Flux recomandat (de testat pe FLORES+ / eșantion EVA înainte de adoptare)

EN (sursa verificată) → model specializat → Qwen ca post-editor cu referințele RO/EN/DE/FR/ES + glosarul.

## Surse principale
- TranslateGemma: https://arxiv.org/pdf/2601.09012 · https://blog.google/innovation-and-ai/technology/developers-tools/translategemma/
- IndicTrans2: https://github.com/AI4Bharat/IndicTrans2
- MADLAD-400: https://huggingface.co/google/madlad400-10b-mt
- MiLMMT-46: https://huggingface.co/xiaomi-research/MiLMMT-46-12B-v1.0
- Atlas-Chat / Nile-Chat: https://huggingface.co/MBZUAI-Paris/Atlas-Chat-9B · https://huggingface.co/MBZUAI-Paris/Nile-Chat-12B
- Wu (SiniticMTError): https://arxiv.org/html/2509.20557
- Azure / Google limbi: https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support · https://docs.cloud.google.com/translate/docs/languages
