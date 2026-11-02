from a12_r8_review import *
import os
t=Path(os.environ['TEMP'])
rep={
'a12_r8_measurements.py':{'Cinco fallos Windows':'Cinci abateri legate de mediul Windows','La CESIRO acum sunt 1/50/1/5/1; deriva jurnalizată de 10 coloane nu demonstrează regresie de comportament.':'La CESIRO toate coloanele sunt 50; etalonul planului de 40 se referă la coloanele EVA_. Confirmarea separată de proveniență numără ambele domenii.'},
'a12_r8_t06_count.py':{'Le même dénominateur doit être comparé.':'Comparația folosește aceleași domenii.'},
'a12_r8_publish.py':{'DICȚIONAR_ISTORIC_40_CESIRO_ACTUAL_50_COLOANE':'DICȚIONAR_50_TOTALE_40_EVA_ISTORIC_ȘI_CESIRO','La livrare este documentat 1/40/1/5/1. În CESIRO curent s-au numărat 1/50/1/5/1 și indexul unic. Cele zece coloane suplimentare nu demonstrează o regresie.':'În istoricul q31 și în CESIRO curent sunt 50 de coloane totale pentru EVA_ComparatieBanca, dintre care 40 EVA_. Există o tabelă, un proces cu cinci parametri, o formă și indexul unic.','Chipul popup-ului nu a fost exercitat din nou.':'Dialogul ZK nu a fost acționat în această reexecuție.'}}
for k,map_ in rep.items():
 p=t/k;s=p.read_text(encoding='utf8')
 for a,b in map_.items():assert a in s;s=s.replace(a,b)
 p.write_text(s,encoding='utf8')

