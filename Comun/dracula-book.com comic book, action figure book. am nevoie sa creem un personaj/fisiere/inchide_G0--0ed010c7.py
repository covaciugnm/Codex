from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(r'D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924')
A = ROOT / '00_STUDIO/audit'
SESSION = A / 'RELUARE_CODEX_20260924_120350'
P = SESSION / 'PACHET_AUDIT_02'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((P/'manifest.json').read_text(encoding='utf-8'))
for rel, meta in manifest['files'].items():
    assert sha(P/rel) == meta['sha256'], rel
    if meta['kind'] == 'deliverable':
        assert sha(ROOT/rel) == meta['sha256'], rel

scores = {'canon': [9.80, 9.70, 9.90], 'studio': [9.75, 9.85, 9.65]}
for kind, folder, rnd in [('canon','G0-CANON-v4','R3'),('studio','G0-STUDIO-v4','R5')]:
    for lens, score in zip(['canon','craft','kpi'],scores[kind]):
        report = A/folder/f'{rnd}_audit_{lens}.md'
        txt = report.read_text(encoding='utf-8')
        assert f'{score:.2f}'.replace('.',',') in txt[:1500]
        assert 'PASS' in txt[:1500]
        assert '\ufffd' not in txt
        assert min(scores[kind]) >= 9.5

approved = A/'G0-STUDIO-v4/VERSIUNE_APROBATA'
approved.mkdir(exist_ok=True)
shutil.copytree(P,approved/'PACHET',dirs_exist_ok=True)
for lens in ['canon','craft','kpi']:
    shutil.copy2(A/'G0-STUDIO-v4'/f'R5_audit_{lens}.md',approved/f'R5_audit_{lens}.md')
approved_manifest = {str(p.relative_to(approved)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in approved.rglob('*') if p.is_file() and p != approved/'manifest.json'}
(approved/'manifest.json').write_text(json.dumps(approved_manifest,ensure_ascii=False,indent=2),encoding='utf-8')

studio_result = '''# Rezultat final — G0 Organizarea studioului v4.4

Data: 24.09.2026. **PASS: minimum 9,65 / 10.** Cele trei avize R5 sunt încheiate; coordonatorul a verificat rapoartele și amprentele înainte de arhivare.

| Rundă | Canon & Istorie | Meșteșug & Piață | KPI | Minimum | Verdict |
|---|---|---|---|---|---|
| R1 | 8,70 | 8,70 | 8,68 | 8,68 | FAIL |
| R2 | 8,85 | 8,78 | 8,88 | 8,78 | FAIL |
| R3 | 9,05 | 8,88 | 8,94 | 8,88 | FAIL |
| R4 | 8,20 | 9,10 | 8,35 | 8,20 | FAIL |
| R5 | 9,75 | 9,85 | 9,65 | 9,65 | PASS |

Auditorii R5: Darwin, Godel, Meitner. Autorul corecturilor R4: coordonatorul Codex. Notele nu sunt autoevaluări și nu au fost modificate de coordonator.

Rapoarte: [AU-C](R5_audit_canon.md), [AU-M](R5_audit_craft.md), [AU-K](R5_audit_kpi.md). [Plan R4](R4_plan_masuri.md), [execuție](R4_corecturi/EXECUTIE.md), [verificări](R4_corecturi/rezultat.json), [arhivă aprobată](VERSIUNE_APROBATA/manifest.json).

Pachetul aprobat cuprinde organizarea și jurnalul v4.4, anexa S, 25 de briefuri și referințele fixate în manifest. Etichetele istorice sau reziduale consemnate de auditori rămân vizibile în copia evaluată. Nu am rescris documentele după acordarea notelor.

Toate măsurile R4 au închiderile și limitele descrise în rapoarte. Observațiile minore sunt păstrate în [registrul separat](../OBSERVATII_MINORE_G0.md). Corectarea lor într-o versiune viitoare va necesita verificarea acelei versiuni; nu pretindem că au fost deja eliminate.

Defectul de export al primului raport craft a fost corectat de auditor; copia coruptă rămâne arhivată ca R5_audit_craft_export_initial_corupt.txt. Nota și constatările sunt neschimbate.

Acest PASS încheie G0 împreună cu canonul v4.3. Nu certifică realizarea produselor G1, site-ul, planșele ori avizele comerciale viitoare. Se aplică numai copiei izolate și amprentelor din manifest.
'''
(A/'G0-STUDIO-v4/REZULTAT_FINAL.md').write_text(studio_result,encoding='utf-8')

backlog='''# Observații minore rămase la închiderea G0

Data: 24.09.2026. Aceste observații au fost incluse în notele independente, toate peste 9,50. Nu sunt declarate remediate. Nu modifică retroactiv versiunile aprobate. Responsabil de integrare la următoarea revizie: Showrunner/coordonator; verificare: auditorul lentilei relevante.

| Grup | Constatare | Referință | Următoarea acțiune |
|---|---|---|---|
| Canon — glosar | „Dâra” rezumă prea larg aparatele; regula completă distinge lumina vizibilă de termoviziune. | R3 AU-C R3C-m01; AU-M CRAFT-R3-m01 | Precizarea excepției în glosar, înainte de derivarea fișelor pentru desenatori. |
| Canon — glosar | Regula însoțitorului omite în rezumat excepția frontului 1915–1916. | R3 AU-C R3C-m02 | Adăugarea trimiterii la excepția normativă. |
| Canon — formatare | Cinci rânduri din registrul V4 au probleme de randare a tabelului. | R3 AU-K §6 | Repararea delimitării și verificarea randării la următoarea versiune. |
| Studio — K7 | Rezumatul S indică două runde, fișa normativă și brief-ul cer ≤3. | R5 AU-K F1; AU-C; AU-M | Alinierea rezumatului și indicarea scadenței G5/final S1. |
| Studio — anexa S | Lipsesc unele ținte explicite din tabelul KPI și tabelul curent decizie–dovadă. | R5 AU-K F2 | Completarea celor 13 KPI și a celor 15 trimiteri la decizii, fără declararea produselor viitoare drept terminate. |
| Studio — trimiteri | Trimiterea secundară RS33, indexul RS27 și unele etichete de versiune nu reflectă integral regulile curente. | R5 AU-K F3; AU-C; AU-M | Actualizarea trimiterilor și etichetelor; regulile operative sunt cele auditate. |
| Studio — formatare | Linia goală din jurnal §5.3 rupe tabelul istoric. | R5 AU-K F4 | Repararea randării fără schimbarea conținutului istoric. |

Rapoartele integrale prevalează asupra acestei sinteze. Recomandarea AU-C de a preciza „primul zbor liber cu oameni” rămâne o precizare editorială, fără eroare de dată demonstrată. Nicio observație minoră nu este ascunsă sau eliminată prin medierea notelor.
'''
(A/'OBSERVATII_MINORE_G0.md').write_text(backlog,encoding='utf-8')

final='''# G0 închis — DRACULA

**24.09.2026: ambele livrabile au primit minimum 9,50 de la fiecare auditor independent.**

| Livrabil | Versiune / rundă | Canon & Istorie | Meșteșug & Piață | KPI | Minimum |
|---|---|---|---|---|---|
| Canon | v4.3 / R3 | 9,80 | 9,70 | 9,90 | **9,70** |
| Organizarea studioului | v4.4 / R5 | 9,75 | 9,85 | 9,65 | **9,65** |

Auditori: Darwin, Godel și Meitner, agenți independenți de autorii documentelor și corecturilor. Coordonatorul nu a acordat sau modificat aceste note. Rapoartele constată zero defecte critice și majore în perimetrul evaluat; observațiile minore rămân consemnate.

- [Rezultatul canonului și istoricul rundelor](00_STUDIO/audit/G0-CANON-v4/REZULTAT_FINAL.md)
- [Rezultatul organizării și istoricul rundelor](00_STUDIO/audit/G0-STUDIO-v4/REZULTAT_FINAL.md)
- [Registrul integral de audit](00_STUDIO/audit/00_REGISTRU_AUDIT.md)
- [Observațiile minore rămase](00_STUDIO/audit/OBSERVATII_MINORE_G0.md)
- [Mandatele auditorilor Studio R5](00_STUDIO/audit/RELUARE_CODEX_20260924_120350/DESCHIDERE_STUDIO_R5.md)

Au fost păstrate versiunile înainte/după, diferențele, rapoartele FAIL și PASS, planurile de măsuri și probele verificărilor. Cele 32 de fișiere din pachetul fix au amprente verificate; documentele de producție nu au fost modificate după evaluare. Închiderea măsurilor M2.3/M2.4 ale canonului este completată acum de avizele organizării și de completul celor trei auditori.

**Locul de lucru aprobat:** `D:/00. Downloads/Dracula Book/DRACULA-COMICS-CODEX-G0-20260924/`. Originalul DRACULA-COMICS nu a fost înlocuit, deoarece altă sesiune îl modifica în paralel. Verdictul nu se transferă automat acelui original.

G0 înseamnă aprobarea bazei canonice și a organizării producției. Nu înseamnă că cele 20 de episoade, povestirile, desenele, figurinele sau site-ul final au trecut auditul. Acestea își păstrează porțile proprii.
'''
(ROOT/'REZULTAT_G0.md').write_text(final,encoding='utf-8')
with (A/'G0-CANON-v4/REZULTAT_FINAL.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## Actualizare de închidere G0 — 24.09.2026\n\nOrganizarea v4.4 a trecut R5 cu 9,75 / 9,85 / 9,65. M2.3 și M2.4 sunt închise în perimetrul predării, alinierii și completului independent. Canonul aprobat și rapoartele R3 rămân intacte. [Rezultat general](../../../REZULTAT_G0.md).\n')
with (A/'00_REGISTRU_AUDIT.md').open('a',encoding='utf-8') as f:
    f.write('\n\n### Închidere G0 — 24.09.2026\n\n| Livrabil | Rundă | AU-C | AU-M | AU-K | Minimum | Verdict |\n|---|---|---|---|---|---|---|\n| Canon v4.3 | R3 | 9,80 | 9,70 | 9,90 | 9,70 | PASS |\n| Studio v4.4 | R5 | 9,75 | 9,85 | 9,65 | 9,65 | PASS |\n\nComplet: Darwin, Godel, Meitner. G0 închis în copia izolată. Rapoarte, amprente și limite: [rezultat general](../../REZULTAT_G0.md). Originalul concurent nu este înlocuit. Observațiile minore sunt păstrate separat; nu există declarație de corectare a lor după audit. Produsele G1 nu sunt promovate prin această închidere.\n')
shutil.copy2(A/'STARE_G0.json',SESSION/'STARE_G0_inainte_inchidere.json')
state=json.loads((A/'STARE_G0.json').read_text(encoding='utf-8'))
state['status']='PASS'
state['studio'].update({'scores':dict(zip(['AU-C','AU-M','AU-K'],scores['studio'])),'minimum':9.65,'status':'PASS'})
state['minor_observations_open']=True
(A/'STARE_G0.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')

# Inventarul de închidere exclude numai propriul fișier, pentru a evita autoreferința.
closing=A/'MANIFEST_INCHIDERE.json'
all_files={str(p.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in ROOT.rglob('*') if p.is_file() and p!=closing}
closing.write_text(json.dumps(all_files,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT.parent/(ROOT.name+'-AUDIT-INCHIS.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file():z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for rel,meta in all_files.items():
        assert hashlib.sha256(z.read(ROOT.name+'/'+rel)).hexdigest()==meta['sha256'],rel
archive.with_suffix('.zip.sha256').write_text(sha(archive)+'  '+archive.name+'\n',encoding='ascii')
print(json.dumps({'G0':'PASS','canon_min':9.70,'studio_min':9.65,'archived_files':len(all_files)+1,'archive':str(archive),'archive_sha256':sha(archive)},ensure_ascii=True))
