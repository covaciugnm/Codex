# PROMPT PENTRU CODEX — copiază tot ce e sub linie

---

You are a professional novelist and line editor completing **AURORA SIGNAL**, Book 9 of the DRACULA AURORA young-adult series (publisher: Dracula Book). Your job: write chapters 7–20 as full prose, seamlessly continuing the existing chapters 1–6, and deliver the first COMPLETE full-length manuscript of this book at the series target length.

## THE SITUATION

The manuscript file currently contains:
- **Chapters 1–6 as finished prose** (21,428 words) — Act I, complete and polished.
- **Chapters 7–20 only as outlines/synopses** (headings like "# CHAPTER 7: CLASSROOM DEMO (~4,400 words)" followed by summary text) — these were never written as prose.
- **SIGNAL LAB TOOLKIT** — a large educational back-matter section (media-literacy micro-guides). This is finished; keep it as back matter, do not rewrite it.

You must replace the chapter 7–20 outlines with real prose chapters, matching the voice, characters and continuity of chapters 1–6.

## WORKING FOLDER — exact layout and what each file is

Root of the book: `D:\00. Downloads\Dracula Book\DRACULA AURORA\Book 9\`

```
Book 9\
├── Book9_AuroraSignal_MasterPlan.txt      ← THE BIBLE. Full story architecture: logline, stakes,
│                                            character sheets (Jade, Rowan, Cameron, Lexi, ensemble),
│                                            Save-the-Cat beat sheet, Act structure, midpoint,
│                                            All-Is-Lost, finale "Signal Night", resolution.
│                                            (.docx and .pdf are the same content — read the .txt)
├── Book9_AuroraSignal_MasterPlan.docx
├── Book9_AuroraSignal_MasterPlan.pdf
├── PROMPT_CODEX_finalizare_manuscris.md   ← this prompt
├── Coperta\
│   └── Aurora_Signal_Cover_1600x2400.png  ← final cover (context only; tagline on it:
│                                            "What you share shapes who we become")
├── Publicare\
│   └── Aurora_Signal_Interior_6x9_INCOMPLET_cap1-6.docx  ← typeset interior of ch. 1–6 only;
│                                            will be regenerated after you finish — ignore
└── Versiunea 1\
    ├── AURORA_SIGNAL_Complete_Manuscript.docx  ← THE SOURCE. Ch. 1–6 prose + ch. 7–20 outlines
    │                                             + SIGNAL LAB TOOLKIT back matter. Read fully.
    ├── Chapter_SceneList.md               ← SCENE-BY-SCENE PLAN for ALL 20 chapters (~4,600 words):
    │                                        per-chapter POV, scenes, beats, word targets.
    │                                        This is your chapter-level contract — follow it.
    ├── Marketing_Package.md               ← hook ("A lie went viral. So did the truth."),
    │                                        pitch, blurb — the promise the prose must keep
    └── README_DELIVERABLES.md             ← original project's deliverables list (context)
```

Series-level context (one folder up, `D:\00. Downloads\Dracula Book\DRACULA AURORA\`):
- `Plan colecția DRACULA AURORA.docx` — the 10-book collection plan and market research.
- Sibling folders `Book 1` … `Book 10` — the other volumes. For voice calibration you may skim
  `Book 1\Versiunea 1\AURORA_Book1_FINAL.docx` (the series opener) — but chapters 1–6 of THIS
  book are your primary voice reference.

## SERIES DNA (must hold in every chapter)

- Brand: **"Stories that light the road from teen to adult — courage, identity, purpose."**
- Audience: YA 15–25. Tone: dynamic, luminous, inspiring — honest about pain, never bleak.
- Palette imagery: light violet / pastel gold (dawns, murals, river light — it recurs in prose).
- Setting: **Austin, Texas** — Congress Avenue Bridge bats, Colorado River, murals, SXSW-adjacent
  music scene, UT. Anglo-American names only.
- Each book embeds practical **micro-guides** in the narrative (here: verification steps,
  chain-of-custody, takedown reports, apology & repair, mental hygiene) — shown through action
  and dialogue, never as lecture dumps; the full guides live in the back-matter Toolkit.

## CONTINUITY (from ch. 1–6 and the master plan — do not contradict)

- **Jade Miller (17)** — singer-songwriter, café shifts, original song "Dawn Will Come",
  scholarship audition at stake; conflict-avoidant, over-trusts; arc: "hide from harm" → "own the mic".
  Mom is a night-shift nurse.
- **Rowan Blake (18)** — coder/debater, brilliant, blunt; control via code; arc: "I can fix
  everything" → "we fix it together". Builds the detection pipeline; his hard blocklist will
  wrongly flag a memorial post (ch. 11) — that error and his on-mic admission (ch. 15) are pivotal.
- **Cameron Brooks (18)** — JROTC + track, films on a hand-me-down DSLR; rule-bound; arc:
  "orders" → "ethics". Leads forensics & evidence chain. Slow-burn trust between Jade & Cameron.
- **Lexi** — influencer who amplifies the fake ("I'm just reflecting what's out there"), takes the
  mic at Signal Night: "I chased the clip for growth. I was wrong."
- Antagonist pressure: "MemeForge" mirror accounts, forged "raw" angles, school-board hearing,
  paused scholarship auditions, leaked out-of-context voice memo.
- Finale: **Signal Night** in the gym (waveform artifacts, breathing mismatch, lens ghosting,
  parallax demo, Attorney Porter on limits of law), reinstated auditions, Jade sings
  "Dawn Will Come", sunrise on the mural: **"Share light, not lies."**

## CHAPTERS TO WRITE (titles and word targets are fixed)

| Ch | Title | Target |
|----|-------------------|--------|
| 7  | Classroom Demo    | ~4,400 |
| 8  | Mirror Maze       | ~4,500 |
| 9  | Backyard Song     | ~4,200 |
| 10 | Raw Leak          | ~4,600 |
| 11 | Blocklist Burn    | ~4,700 |
| 12 | Splinter          | ~4,100 |
| 13 | Open Lab          | ~4,500 |
| 14 | Invite the Critic | ~4,400 |
| 15 | Signal Night      | ~4,800 |
| 16 | The Confession    | ~4,200 |
| 17 | The Vote          | ~3,800 |
| 18 | The Audition      | ~4,100 |
| 19 | The Toolkit       | ~3,600 |
| 20 | Mural Dawn        | ~4,500 |

Total new prose: ~60,000 words. Final book: ch. 1–6 (21,428) + ch. 7–20 (~60,000) ≈ **81–85,000
words of story** + Toolkit back matter ⇒ meets the series target (~90,000 words with back matter).

## PROCESS (follow in order)

1. Read `Versiunea 1\AURORA_SIGNAL_Complete_Manuscript.docx` end to end. Absorb the prose voice of
   ch. 1–6: POV rotation (Jade/Rowan/Cameron close-third), sentence rhythm, sensory Austin detail,
   chapter-opening and -closing patterns.
2. Read `Chapter_SceneList.md` (scene contract) and `Book9_AuroraSignal_MasterPlan.txt` (beats,
   character arcs). Where the two differ in small details, the Scene List wins for scene order,
   the Master Plan wins for character arc and theme.
3. Write chapters 7–20 one at a time, in order. After each chapter, self-check against the Scene
   List (all scenes present? POV correct? word target ±10%?) and against continuity (names, props,
   timeline, weather, song lyrics references) before moving on.
4. Assemble the complete manuscript in reading order: Title / ch. 1–6 (verbatim from source, typos
   may be silently fixed) / ch. 7–20 (new) / AUTHOR'S NOTE / SIGNAL LAB TOOLKIT / RESOURCES.
5. Deliver into a NEW folder `D:\00. Downloads\Dracula Book\DRACULA AURORA\Book 9\Versiunea 2\`:
   - `AURORA_SIGNAL_Complete_Novel_v2.md` — full manuscript, markdown, `# CHAPTER N: TITLE` headings
   - `AURORA_SIGNAL_Complete_Novel_v2.docx` — same content as .docx
   - `ChangeLog_v2.md` — what was written, per-chapter word counts, any continuity fixes made in ch. 1–6
   - `Continuity_Report.md` — character/timeline/prop tracker you maintained while writing

## HARD RULES

- Match the existing prose voice — a reader must not feel the seam after chapter 6.
- No meta-text in the manuscript: no "[END CHAPTER]", no word counts, no production notes, no
  placeholders, no summaries-instead-of-scenes. Every chapter is finished prose.
- No content that breaks YA: no explicit sex, no gratuitous violence; hard topics (harassment,
  despair, suicide-adjacent moments) handled with care and hotline-aware framing, as ch. 1–6 do.
- Keep the micro-guide material woven into action (a character DOES the verification step); the
  didactic versions stay in the Toolkit only.
- Do not modify any file in `Versiunea 1\` — it is the immutable source. All output goes to `Versiunea 2\`.
- American English throughout; song lyrics only original (never quote real songs).

Deliver the complete v2 manuscript. This makes AURORA SIGNAL the first Aurora volume finished at
full novel length — it will be typeset and published by Dracula Book.
