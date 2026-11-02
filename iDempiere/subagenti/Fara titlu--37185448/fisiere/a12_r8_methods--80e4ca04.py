from a12_r8_review import *
import shutil,os
R=E/'R8';M=R/'metoda';M.mkdir(exist_ok=True)
names='review list arch arch_survs jvm extra_jvm mock static static_tail pg native t06_count offline cases measurements extend menu_case cov zones publish qa ui'.split()
for n in names:
 p=Path(os.environ['TEMP'])/('a12_r8_'+n+'.py');shutil.copyfile(p,M/p.name)
for n in ['a12_r3_survey.py','a12_r6_exec.py']:shutil.copyfile(Path(os.environ['TEMP'])/n,M/n)
wr(M/'Manifest.json',{p.name:sha(p)for p in M.glob('*.py')})
doc='''# Reproducerea auditului individual R8

Ediția pornește de la cele 652 de fișe R7 și cele 2.619 de criterii ale acestora. Data din interfața proiectului, momentul integrării și data din logul unei probe sunt câmpuri diferite. R8 citește documentele și codul de la commitul fixat.

## Citirea unei fișe

Deschideți Audit_individual_P01_R8.html și filtrați după ID original, alias P01, capitol sau titlu. Fiecare criteriu păstrează cererea originală, starea R7, starea efectivă R8, încercările și pasul rămas. Din fișa JSON se poate urmări pointerul exact spre sursa verificată și legătura inversă din Dovezi_criterii.json.

¤current¤ înseamnă că runda a executat sau a confruntat o probă măsurată pe calea numită de autorul ei. ¤historical¤ consemnează o observație dintr-o fotografie anterioară, citită sau recalculată în această rundă. ¤old_current_evidence¤ și ¤context¤ păstrează probe existente, fără o nouă execuție. ¤correction¤ schimbă sensul relației. ¤pending¤ identifică o precondiție sau un experiment datorat. Scorul auditului aparține auditorului independent.

## Originea măsurătorilor

A12 a confruntat documentele testelor cu Git prin ¤git cat-file --batch¤, a recalculat identificatorii de blob și a verificat rândurile folosite. Comenzile de citire a dicționarului din CESIRO sunt limitate la metadate sau totaluri, în tranzacție ¤BEGIN READ ONLY ... ROLLBACK¤. Cele două JAR-uri sunt verificate separat. JVM a executat suitele proiectului cu acces la rețea interzis. Există un fișier de execuție pentru lotul de 50 și unul pentru lotul de 14. Legăturile indică aserțiunea individuală și condiția. Un cod de ieșire al clasei nu certifică toate cerințele.

Experimentul D107 folosește două sesiuni PostgreSQL reale, același rând sintetic și metoda ¤inConflict¤ din fiecare JAR. Clusterul acestei probe s-a oprit după executare. Prima încercare de inițializare a depășit termenul din cauza moștenirii pipe-ului stdout în Windows. Relansarea a folosit un fișier de log al serverului separat de stdio al inițiatorului. Ambele resurse ale probei au fost restituite. Cele patru suite de pregătire T224 au folosit un export temporar și un ¤docker¤ simulat.

## Relectură și integritate

Registru_reexecutare_R8.json conține un rând pentru fiecare criteriu, inclusiv pentru cele din afara lotului de 467. Pozițiile R7 corectate arată ce a fost reclasificat de A11. R8 folosește raportul final A05. Indexul celor 883 de candidați este o listă de căutare distinctă. Metoda separă subcazurile executate, probele documentare și dovezile funcționale.

¤metoda¤ conține scripturile auditate cu SHA-256 în manifest. Verificare_R8.json reconciliază dosarele, HTML-ul, relațiile inverse și proveniența atlasului. Verificare_UX_R8.json consemnează măsurarea indexului la 390 și 1.366 de pixeli. Edițiile R1–R7 rămân neschimbate.
'''
(R/'Metoda_reproducere.md').write_text(doc.replace('¤',chr(96)),encoding='utf8');print(sha(R/'Metoda_reproducere.md'),sha(M/'Manifest.json'))

