from a12_r10_publish import *
import shutil
def save(dest):
 m=dest/'metoda';m.mkdir(exist_ok=True)
 names='base plan 873 auth httptrace jvm jvmreg stock t227_mut gitbatch guard_test guard_diag guard_context guard_cal lease bank_run native_worker eur_worker eur_run bankrace race_run ui_config ui_activate cleanup jar171 pg201_fixed receipt registry_receipts bank_receipts bank_ui_receipts pg_reciept techzones two_boots 254 a08 a08rec a04historic c330_alternatives independent rootproof t58_bound t159role t314_gates pos tip tip_real pdf_harness pdf_real3 pdf_windows pdf_mut printrec a07source docadd publish qa ui method seal'.split()
 th={}
 for n in sorted(set(['a12_r10_'+x+'.py'for x in names]+[v.name for v in Path(__file__).parent.glob('a12_r10*handoff*py')])):
  f=Path(__file__).parent/n
  if f.exists():shutil.copyfile(f,m/n);th[n]=H(m/n)
 wr(m/'Manifest.json',th)
 md="""# Reproducerea auditului individual P01 · ediția R10

## Populație și versiune

Cele două fotografii de control ale registrului provin de la 2026-11-02T19:45:29Z și 20:46:47Z. Ultima numără 996 taskuri în total, 693 P01 și 652 în populația auditată. Prima variație privește T228/T321. Între cele două fotografii s-au schimbat T225, T232 și T343; toate sunt în afara populației înghețate. Commitul Git este 6df998aee0e514d30856c461962afe99ebd0d113. Edițiile R9 și R10 conțin aceleași 2.619 criterii.

## Citirea rezultatului

Începeți cu Audit_individual_P01_R10.html. Fișa reunește identitatea și aliasul istoric, starea din portal și criteriile originale. Citiți pentru fiecare observație etalonul, rezultatul, martorul negativ, limita și fișierul de probă. Dovezi_criterii.json permite urmărirea inversă, de la probă la fișă. Registru_reexecutare_R10.json are un singur rând pentru fiecare criteriu. Cele 164 de cazuri cu fixtură, 873 fără comparator proaspăt și 167 istorice sunt disjuncte la intrare.

## Reproducerea măsurătorilor

Directorul metoda conține scripturile auditului. Utilitarele comune sunt documentate în edițiile R6–R9. Pregătiți a12_r6_exec, a12_r8_jvm și a12_r9_publish folosind sursele istorice indicate acolo. Adaptați căile pentru o copie într-un director nou și scrieți rezultatele numai în copia proprie. Fișierele de intrare au semnături SHA256. Verificarea manifestului se face după ultima scriere, în ambele sensuri între fișă și probă.

1. T201 folosește un PostgreSQL 16 efemer ascultând pe 127.0.0.1 și copia sintetică GardenWorld. Testul JDBC al proiectului în fiecare dintre două JAR-uri verifică blocarea pe două conexiuni, rollbackul și protecția registrului. Verificați aserțiunile din testul original și efectul celor trei mutanți. Clusterul propriu a fost restituit.
2. T06 și T171 folosesc un cabinet r57 GardenWorld creat prin slotul oficial §61. O arhivă SQLite sintetică cu 168 de note și 152 de linii de extras pentru zece conturi stabilește oracolul. Verificați separat procesul AD, ZK, CSV, refuzurile, cursul EUR cu baza RON și concurența pe două sesiuni. T06_laborator_restituit.txt păstrează restituirea.
3. T210 folosește suita ASGI originală cu SQLite sintetic. Calea externă este oprită. Autoreglarea asyncio pe Windows rămâne disponibilă. Comparați numărul testelor, răspunsurile HTTP și mutația de autorizare pe două căi.
4. T227 utilizează suita Java originală și versiuni mutate exclusiv în copii pentru teste. Legați afirmația de aserțiunea din log și de marcajul ANCHOR pentru sursă. Clasa lipsește în JAR-ul instalat. Starea din tracker consemna închiderea fără montare.
5. T11 și T254 folosesc Git complet și obiecte adresate prin hash. Citiți criteriul în versiunea indicată. Pentru T254 comparați LIPSA, domeniul metodelor selectate și amendamentul scris al specificației. Două inventare din date diferite nu definesc singure o regresie a produsului.
6. Pentru A05/A07 folosiți și rapoartele originale și artefactele de restituire. Pentru G3 și livrări urmăriți aceleași ID-uri între site, antet importat și comandă nativă. O factură din altă origine nu închide criteriul.

## Recepție

A11 acordă nota auditului separat. Verificarea structurii și manifestul nu stabilesc scorul implementării. Stările taskurilor în aplicație au rămas cele raportate de server.
"""
 (dest/'Metoda_reproducere.md').write_text(md,encoding='utf8')
if __name__=='__main__':save(R10)
