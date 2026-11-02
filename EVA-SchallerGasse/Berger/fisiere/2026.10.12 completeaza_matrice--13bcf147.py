import json
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'2026.10.12 Matrice comparatie.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['coverageHeaders'][2]='Propunere de contract TOMS v4.1 trimisă'
for r in d['prices']:
    for i,x in enumerate(r):
        if isinstance(x,str):
            r[i]=x.replace('Datesle','Datele').replace('Ofertă, neacceptată','Acceptarea A&C neconfirmată').replace('totalul37.900','totalul 37.900').replace('TOMS300','TOMS 300').replace('PECH450','PECH 450').replace('max8','max. 8').replace('BERGER:8','BERGER: 8').replace('PECH:90','PECH: 90').replace('refuz2026','refuz 2026')
for r in d['coverage']:
    if r[1]=='Asistență statică și vizite de șantier':
        r[3]='ANG 855: 1.500 EUR, fără număr de vizite în ofertă. Q1 F5 confirmă 6 faze critice + ședință de început + întâlniri după nevoie. V4.1 nu este acceptat integral.'
        r[6]='T1 §4; T2 pos1.2.2; T10 F5; B1 p2–3; P1 pos05'
    if r[1]=='Prüfingenieur §127 / verificare pe șantier':
        r[3]='ANG 839: 8.000 EUR, ipoteză 15 vizite. Q1 F7 confirmă 24 h și o singură Rohbaubeschau. Aceste confirmări nu sunt acceptarea întregului v4.1.'
        r[6]='T1 §5; T3; T10 F7; B1 p3; P1 pos04–06'
updates={
 'Calcule de execuție și preluarea predimensionării': ('Q1 F3 confirmă un calcul nou pe planul actual și preluarea pe răspundere proprie, în pachetul ANG 855. Întregul v4.1 rămâne neacceptat.','T1 §2; T2 pos1.2.1; T10 F3; B1 p2; P1 pos01'),
 'Fundații și placa de 30 cm': ('Confirmat în Q1 F1/F12: placă de 30 cm și racord la fundațiile existente. Fără preț separat pe element. V4.1 nu este acceptat integral.','T1 §2.1; T2; T10 F1,F12; B1 p1–3; P1 pos01'),
 'Puț lift, groapă și fundare': ('Confirmat în Q1 F1/F6: liftul și preluarea sarcinilor furnizate de fabricant. TOMS le verifică static; nu generează aceste sarcini.','T1 §2.2,6; T10 F1,F6; B1 p1; P1 pos01'),
 'Planșee existente, ziduri, goluri și buiandrugi': ('Confirmat Q1 F1 pentru planșee, pereți, buiandrugi și goluri. Fără preț separat pe element/gol.','T1 §2.3–4; T2; T10 F1; B1 p1–2; P1 pos01–02'),
 'Mansardă, acoperiș, lucarne și terase': ('Führungsplanung confirmată în Q1 F1 și ANG 855. Detaliile de atelier și dimensionările de noduri sunt excluse.','T1 §2.5,3,6; T2; T10 F1; B1 p1–2; P1 pos01'),
 'Contravântuire și traseul încărcărilor': ('Principiul structural confirmat Q1. Detaliile conexiunilor de contravântuire sunt excluse Q2 A10.','T1 §2.6,6; T10 F1; T5 A10; B1 p2; P1 pos01'),
 'Balcoane în curte și transmiterea sarcinilor': ('Sistemul și transferul sarcinilor sunt confirmate în principiu în Q1. Ancorele/diblurile detaliate: Aufpreis Q2 A5, excluse v4.1.','T1 §2.7,6; T10 F1; T5 A5; B1; P1 pos01'),
 'Scări, pereți antifoc, vecini și coșuri': ('Confirmate structural în Q1 F1. Dimensionarea la foc pe clase R nu este inclusă.','T1 §2.8–9,6; T10 F1; B1 p2; P1 pos01'),
 'Subzidiri etapizate': ('Q1 F6 confirmă calculul și desenul de principiu pentru subzidiri. Proiectul sprijinirii excavării rămâne distinct, la terți.','T1 §2.10,6; T10 F6; B1 p2; P1 pos03'),
 'Planuri de poziții, cofraj și armare': ('ANG 855 include toate planurile cofraj/armare. Q1 F2 confirmă planurile de poziții/sarcini. Detalierea completă de atelier este exclusă.','T1 §2.11,3,9; T2; T10 F2; B1 p2; P1 pos01'),
 'Liste de armare și liste de piese': ('Q1 F2 confirmă listele armare/fasonare. Q2 exclude Excel/CSV separat și liste de piese direct în plan.','T1 §2.12,6,9; T10 F2; T5 A8,C; B1 p2; P1 pos01'),
 'Planuri de atelier și documente ale executantului': ('Q1 F2 confirmă REVIZUIREA planurilor atelier și documentelor furnizorilor. Întocmirea Werkstätten-/Abbundpläne este exclusă.','T1 §2.13,3,6; T10 F2; T5 A12; T6; B1 p2; P1'),
 'Încărcări ale furnizorilor și verificarea sprijinirilor': ('Q1 F6 confirmă revizuirea documentelor terților și sarcinilor. Proiectele de sprijinire și generarea sarcinilor sunt la terți.','T1 §2.14,6; T10 F6; B1 p2–3; P1 pos03'),
 'Revizii, corecții și întrebări tehnice': ('Q1 F2 confirmă două cicluri de corecții și răspunsuri tehnice ofertanților. Evaluarea comercială și negocierile de atribuire sunt excluse.','T1 §2,3,4; T10 F2; B1 p2–3; P1 p3–4'),
 'Asistență statică și vizite de șantier': ('ANG 855: 1.500 EUR, fără număr de vizite. Q1 F5 confirmă 6 faze + început + după nevoie, răspunsuri în 2 zile și deplasare. Protocolul în 3 zile este cerință AG.','T1 §4; T2 pos1.2.2; T10 F5; B1 p2–3; P1 pos05'),
 'Durată, prelungire și vizite suplimentare': ('Q1 F5 confirmă prelungirea condiționată la 15 luni și 300 EUR net/vizită suplimentară cu deplasare. Pragul numeric de peste 3 vizite este completare AG neacceptată.','T1 §4; T10 F5; B1 p1–3; P1 pos05,p4'),
 'Certificat §128 și relația MA37': ('Q1 F8/F10 confirmă certificatul final, documentele și colaborarea cu autoritatea. As-built la arhitect. Nu este acceptare integrală v4.1.','T1 §5; T3; T10 F8,F10; B1 p3; P1 pos06'),
 'Control intern și costuri de verificare externe': ('Q1 F7/F10 confirmă controlul, coordonarea verificării externe dacă o cere MA37 și declarația fără alte costuri de verificare. Nu este ofertă separată de elaborare Prüfstatik extern.','T1 §5; T3; T10 F7,F10; B1; P1'),
 'Drepturi de utilizare, modificare și terți': ('Q1 F17 confirmă principiul utilizării nelimitate, accesului terților și predării. Întregul contract v4.1 nu este acceptat.','T1 §9; T10 F17; B1; P1 p4'),
 'Preț, modificări și cheltuieli': ('Ofertele prevăd convenire separată/recalcul la efort crescut peste 10%. Q1 F18 limitează la schimbări AG și acord prealabil; erorile proprii nu sunt supliment.','T1 §11; T2–T4; T10 F18; B1 p2–3; P1 p1–4'),
 'Plăți și rețineri': ('30 zile în ofertele originale. Q1 F18: după progres, plan de plăți de propus de TOMS. Repartizările AG și plata fără avans nu sunt acceptate automat.','T1 §11; T2–T4; T10 F18; B1 p3; P1 p1,4'),
 'Planwechsel și cerințe MA37': ('Q1 F11/F13 confirmă colaborarea structurală. Încadrarea Planwechsel/nouă depunere și bucla exactă v4.1 rămân de clarificat.','T1 §14; T10 F11,F13; B1 p2–3; P1 p3–4')
}
for r in d['coverage']:
    if r[1] in updates: r[3],r[6]=updates[r[1]]
    r[6]=r[6].replace('T5 A/B','T5 A/C').replace('T5 B','T5 C')
    if r[1]=='ÖBA, Bauführung, demolare și As-built':
        r[2]=r[2].replace('planuri As-built de arhitectură','planuri structurale As-built, la arhitect')
    if r[1] in ['PDF, DWG, DXF, IFC și revizii','Model nativ, CSV/Excel, fișiere utilaj și layere']:
        r[3]=r[3].replace('Q2 B','Q2 C')
    if r[1]=='Foc, protecții speciale și verificare seismică':
        r[6]='T1 §6; T10 F1,F3; T5 A11; B1; P1'
    if r[1]=='Noduri lemn/oțel, ancore și îmbinări':
        r[6]='T1 §3,6; T5 A1,A2,A3–A6; T6; B1 p2; P1 pos01'
for r in d['prices']:
    if r[1].startswith('Vizită / recepție suplimentară'):
        r[5]='TOMS 300: confirmat Q1 F5 cu deplasare. Pragul de peste 3 vizite este completare AG neacceptată. PECH 450: fiecare recepție suplimentară. Nu se adaugă automat la pachet.'
        r[6]='T1 §4; T10 F5; B1 p3; P1 pos05'
    if r[1]=='Termen de plată și indexare':
        r[2]='30 zile'
        r[5]='TOMS: 30 zile în ofertele originale, planul de plăți AG neacceptat; recalcul efort >10% cu acord, limitat Q1 F18 la modificări AG. BERGER după progres. PECH facturi lunare, ZT-Index, fără Haftrücklass.'
        r[6]='T1 §11; T2–T4; T10 F18; B1 p3; P1 p1,4'
    if r[1].startswith('BauKG TOMS'):
        r[5]='ANG 840 separat: 1.200 EUR planificare + 9.840 EUR șantier, ipoteză 12 luni. Total 11.040 EXCLUS din v4.1. Oferta originală: 125 EUR/oră suplimente; fără disponibilitate confirmată.'
    if r[1]=='Asistență statică / Baubegleitung':
        r[5]='TOMS: Q1 F5, început + 6 faze critice + după nevoie. BERGER: maximum 8 vizite asistență. PECH: 12 Abnahmen, fără numire PI explicită.'
        r[6]='T1 §4; T2 pos1.2.2; T10 F5; B1 p2; P1 pos05'
    if r[1]=='Goluri în existent / Durchbruchsplanung':
        r[2]='Confirmat în pachet'
        r[5]=r[5].replace('La TOMS cerut în v4.1','La TOMS confirmat în Q1 și cerut în v4.1')
        r[6]='T1 §2.4; T10 F1; B1 p1–2; P1 pos02'
if not any(r[1]=='Prüfingenieur, tarif orar original' for r in d['prices']):
    d['prices'].insert(18,['Supliment','Prüfingenieur, tarif orar original',155,'Nespecificat PI','Rol PI neconfirmat','TOMS ANG 839: 155 EUR net/oră. Tarif specific PI; nu se aplică automat întregii proiectări TWP și nu este un supliment comandat.','T3 p1'])
d['calcule_asteptate']={'net':[37900,45000,69300],'TVA':[7580,9000,13860],'brut':[45480,54000,83160],'subtotal_fara_PI_BWB':[26500,35000,None]}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(d['coverage']),len(d['prices']))
