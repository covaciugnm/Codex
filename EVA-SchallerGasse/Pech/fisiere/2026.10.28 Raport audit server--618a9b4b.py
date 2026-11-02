from pathlib import Path
import json
R=Path.cwd();S=R/'folder map/2026.10.27 Raport audit autorizare.py'
src=S.read_text(encoding='utf-8')
def change(a,b):
 global src
 assert a in src,a[:90]
 src=src.replace(a,b)
change("O=R/'00.Proiect/2026.10.27 Audit autorizare si servieta'","O=R/'00.Proiect/2026.10.28 Audit autorizare si servieta'")
change("'2026.10.27 • Schallergasse 35, 1120 Wien • Verificare documentară'","'2026.10.28 • Actualizare după verificarea serverului • Schallergasse 35, 1120 Wien'")
change('P10 și P13–P17 sunt goale. P18–P20 sunt blocate pentru contul folosit.','P10 și P13–P17 sunt goale. Controlul serverului: P18/P19 fără fișiere; P20 conține 4 fișiere străine proiectului.')
change('Verificat prin autentificare și descărcarea ZIP-urilor oferite de interfață la 2026.10.27. P1–P17 accesibile; P18–P20 blocate. Nu au fost încărcate, șterse sau redenumite documente pe site. Verificarea privește vizibilitatea contului PECH, nu inventarul administrativ al serverului.','Interfață verificată la 2026.10.27: 184 fișiere accesibile contului PECH. Server verificat direct la 2026.10.28: toate aceste fișiere sunt prezente identic SHA-256. În directoarele paginilor sunt 189 fișiere: cele 184, un TXT de test în P3 și patru fișiere fără legătură cu proiectul în P20. Detalii în secțiunea 7. Site-ul nu a fost modificat.')
change('Cele 66 versiuni online neidentice sunt marcate în anexa A.','Cele 66 versiuni online neidentice sunt marcate în anexa A. Comparația locală folosește baza inventariată la 2026.10.27; controlul serverului nu adaugă acte tehnice pentru Schallergasse.')
change('Nu s-a accesat dosarul intern MA37.','Nu s-a accesat dosarul intern MA37. La 2026.10.28 s-au citit directoarele active de documente de pe server; baza PostgreSQL și copiile istorice ale site-ului nu au fost auditate.')
change('PDF-ul include ca atașamente: inventarul online (184 intrări), comparația locală largă și sursele principale cu hash.','PDF-ul include ca atașamente: inventarul online (184 intrări), comparația locală largă, sursele principale cu hash și inventarul fizic al serverului.')
change('P18–P20 nu au fost accesibile. Duplicatele locale sunt păstrate pentru trasabilitate.','Controlul fizic al P18–P20 nu a identificat acte suplimentare pentru Schallergasse. Duplicatele locale sunt păstrate pentru trasabilitate.')
change("p(t,style),Spacer(1,7)","p(t,style),Spacer(1,7)")
change("def add(t,style='Normal'):story.extend([p(t,style),Spacer(1,7)])","def add(t,style='Normal'):\n sp=Spacer(1,7);sp.keepWithNext=style in ['Heading1','Heading2'];story.extend([p(t,style),sp])")
server_section=r'''
page('7. Completare: verificarea directă pe saga-server')
add(r'2026.10.28 • Cale Windows: \\192.168.100.151\site-uri\schallergasse35 (U:\schallergasse35). Documentația site-ului indică /home/saga-server/site-uri/schallergasse35 pe serverul eva-contab. S-au citit documentația, regulile de stocare din backend și fișierele active din data/uploads. Parolele nu sunt incluse în audit.')
table(['Loc / verificare','Constatare'],[
('P1–P17 / cele 184 fișiere','Toate cele 184 fișiere descărcate din interfață au corespondent identic SHA-256 pe server. Nu există fișier descărcat care să lipsească fizic din directoarele verificate.'),
('P3 / 68 fișiere fizice','67 documente din interfață plus un TXT de 17 octeți, cu text de test „fisier-secret-P3”. Nu este document de autorizare. Prezența lui fizică nu dovedește o înregistrare activă în baza de date.'),
('P10, P13–P19','Nu există directoare cu fișiere pentru aceste pagini în stocarea activă. Pentru P18/P19, documentația site-ului le descrie drept pagini libere. Restricția contului nu ascunde aici acte suplimentare stocate.'),
('P20 / 4 fișiere fizice','Două ZIP-uri (cod interfață și imagini Eva-Learn), un CSV cu categorii SKU de produse și un ODS cu probleme de import contabil/SAGA. Nu sunt acte pentru Schallergasse.'),
('Portal personal / în afara paginilor','Un PNG în data/uploads/7. Nu este inclus în inventarul documentelor paginilor P1–P20; conținutul său nu a fost evaluat ca act de autorizare.'),
('Concluzia comparației','Nu au fost găsite în P18–P20 documentele tehnice lipsă din dosarul Schallergasse. Constatările privind viza MA37, semnăturile și actualizarea documentației rămân valabile.')],[135,380])
add('Total fizic în pagini: 189 fișiere. Total data/uploads: 190 fișiere, incluzând PNG-ul portalului personal. Inventarul anexat include și 12 resurse auxiliare selectate din public, deci 202 intrări; acestea nu sunt 202 documente de proiect. Au fost verificate toate extensiile din data/uploads, inclusiv ODS.')
add('Limita rămasă: nu s-a interogat PostgreSQL (nume originale, înregistrări orfane, drepturi de acces). Fișierele sunt stocate sub UUID; identitatea celor 184 documente este stabilită prin hash față de descărcările cu nume originale. Nu s-au deschis accesuri, șters fișiere sau schimbat drepturi.')
add('Acțiune recomandată: corectarea denumirii releveului din P2; reconcilierea celor 66 versiuni diferite și a listei locale din anexa B; completarea cu actele semnate și actualizate după validarea proiectantului. Fișierele de test și materialele altor proiecte nu trebuie numărate ca documente de autorizare.')
'''
change("page('Anexa A • Toate fișierele online accesibile')",server_section+"\npage('Anexa A • Toate fișierele online accesibile')")
change("'2026.10.27 • Schallergasse 35 • Audit documentar'","'2026.10.28 • Schallergasse 35 • Audit documentar actualizat'")
change("Q/'2026.10.27 Raport fara atasamente.pdf'","R/'folder map/2026.10.28 QA server/2026.10.28 Raport fara atasamente.pdf'")
change("final=O/'2026.10.27 Schallergasse 35 - Audit acte MA37 si servieta.pdf'","w.add_attachment('2026.10.28 Inventar fizic server.json',(R/'folder map/2026.10.28 QA server/2026.10.28 Inventar server.json').read_bytes())\nfinal=O/'2026.10.28 Schallergasse 35 - Audit acte MA37 si servieta.pdf'")
change("renders=Q/'2026.10.27 Raport randat'","renders=R/'folder map/2026.10.28 QA server/2026.10.28 Raport randat'")
(R/'folder map/2026.10.28 QA server/2026.10.28 Sursa raport consolidat.py').write_text(src,encoding='utf-8')
exec(compile(src,str(S),'exec'))
