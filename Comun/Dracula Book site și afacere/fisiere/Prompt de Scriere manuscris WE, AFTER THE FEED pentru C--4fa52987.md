# PROMPT PENTRU CODEX — copiază tot ce e sub linie

---

You are a professional novelist and line editor expanding **WE, AFTER THE FEED**, Book Seven of the DRACULA
AURORA young-adult series (publisher: Dracula Book). The book's story is COMPLETE but written short,
as a novella of 22,250 words. Your job: expand it into the first full-length edition at the series
target, WITHOUT changing the story.

## THE SITUATION

- The source manuscript contains a complete 20-chapter story (22,250 words).
- The series target is **~90,000 words** per book (story + back-matter micro-guides).
- Task: **expand the existing prose to ~68,000 of story** (total ≈ 85–90k with back matter) by
  deepening what is already there — never by changing what happens.

## WORKING FOLDER — exact layout and what each file is

Root of the book: `D:\00. Downloads\Dracula Book\DRACULA AURORA\Book 7\`

```
Book 7\
├── Book 7 Devin.ai Writing Plan Aurora Series.docx
│      ↳ the writing plan used for this volume (team, constraints, quality bar)
├── Coperta\We_After_the_Feed_Cover_1600x2400.png
│      ↳ final cover (context only)
├── Publicare\We_After_the_Feed_Interior_6x9.docx
│      ↳ typeset interior of the CURRENT short text; will be regenerated after expansion — ignore
├── Versiunea 1\WE_AFTER_THE_FEED_Book7_Complete.docx
│      ↳ THE SOURCE. Complete story (~22.2k words, the shortest of the series). Chapter headings are styled but malformed ('CHAPTER ONETHE POST' = 'CHAPTER ONE' + 'THE POST' joined by a lost line break) — normalize them while expanding.
```

Series-level context (one folder up, `D:\00. Downloads\Dracula Book\DRACULA AURORA\`):
- `Plan colecția DRACULA AURORA.docx` — the 10-book collection plan and YA market research.
- Sibling folders `Book 1` … `Book 10` — the other volumes. For voice calibration you may skim
  `Book 1\Versiunea 1\AURORA_Book1_FINAL.docx` (the series opener), but THIS book's own prose is
  your primary voice reference.

This volume needs the deepest expansion (22k → ~90k with back matter): add scenes and subplots consistent with the existing chapters; do not change the story's spine.

## SERIES DNA (must hold in every chapter)

- Brand: **"Stories that light the road from teen to adult — courage, identity, purpose."**
- Audience: YA 15–25. Tone: dynamic, luminous, inspiring — honest about pain, never bleak.
- Palette imagery: light violet / pastel gold (dawns, murals, water light — it recurs in prose).
- Setting: a U.S. high-school and its online ecosystem. Anglo-American names only; American English (Book 10: British English allowed
  in dialogue, American spelling in narration is acceptable if consistent).
- Each book embeds practical **micro-guides** in the narrative, shown through action and dialogue,
  never as lecture dumps; didactic versions belong in a back-matter toolkit section.
- Cover already printed with author **Ava Peterson & Blake Jacobs (pen names from the original series package)** and tagline *"What is left of us when the scroll stops?"* — the prose must keep
  that promise.

## THIS BOOK

a viral post spirals; digital detox, empathy repair, healthy-feed micro-guides; the collection plan's volume 1 («Noi, după capătul feedului» — cyberbullying, a 24h blackout, a 'manifesto of light') is this book's thematic root

## HOW TO EXPAND (this is craft, not padding)

Grow every chapter from ~1,100–1,800 words to **3,800–4,600 words** by:
1. **Scene expansion** — summarized beats become dramatized scenes with setting, action, dialogue,
   interiority. Anywhere the text *tells* in two sentences what deserves a scene, write the scene.
2. **Sensory texture** — ground every scene in the setting (a U.S. high-school and its online ecosystem); weather, light, sound,
   food, transit, seasons progressing across the book.
3. **Secondary characters** — give named ensemble characters continuity: recurring appearances,
   small arcs, distinct voices. Add at most 2 new named characters, only if scenes demand them.
4. **Subplots already implied** — develop threads the short text opens and drops (family tension,
   money pressure, a friendship strain, a mentor figure) into full B-stories with resolutions.
5. **Micro-guide dramatization** — every practical skill the book teaches gets an on-page moment
   where a character actually uses it, with realistic friction and partial failure first.
6. **Chapter connective tissue** — hooks at chapter ends, echoes at chapter openings; keep the
   existing 20 chapter titles and order exactly.

FORBIDDEN: changing plot events or their order, changing who characters are, killing or adding
major characters, changing the ending, moving the setting, padding with repetition or filler
description, summary-instead-of-scene.

## PROCESS (follow in order)

1. Read the source manuscript end to end; build a private outline of every existing scene per
   chapter and a continuity tracker (names, props, dates, places).
2. Read the other files in the folder as annotated above (plan/audit files where present).
3. Expand chapter by chapter, in order. After each chapter, self-check: all original beats intact?
   word count in range? continuity tracker updated? voice seamless with the original?
4. Assemble: Title page info / 20 expanded chapters / (if the source has back matter, keep it at
   the end; if not, write a 6–10-page back-matter toolkit of this book's micro-guides).
5. Deliver into a NEW folder `D:\00. Downloads\Dracula Book\DRACULA AURORA\Book 7\Versiunea 2\`:
   - `WE_AFTER_THE_FEED_Complete_Novel_v2.md` — full manuscript, markdown, `# CHAPTER N: TITLE` headings
   - `WE_AFTER_THE_FEED_Complete_Novel_v2.docx` — same content as .docx
   - `ChangeLog_v2.md` — per-chapter before/after word counts and what was expanded where
   - `Continuity_Report.md` — the character/timeline/prop tracker you maintained

## HARD RULES

- A reader of the finished book must not detect which sentences are original and which are new.
- No meta-text in the manuscript: no notes, no word counts, no placeholders, no "[TODO]".
- YA-safe content; hard topics handled with care and resource-aware framing.
- Do not modify any file outside `Versiunea 2\` — sources are immutable.
- Song lyrics and poems only original; never quote copyrighted works.

Deliver the complete v2 manuscript. It will be typeset (6×9") and published by Dracula Book under
the cover already prepared in `Coperta\`.
