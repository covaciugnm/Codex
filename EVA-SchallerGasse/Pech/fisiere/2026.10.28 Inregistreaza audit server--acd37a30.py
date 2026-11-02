from pathlib import Path
R=Path.cwd()
src=(R/'folder map/2026.10.27 Inregistreaza audit autorizare.py').read_text(encoding='utf-8').replace('2026.10.27','2026.10.28').replace("Q=B/'2026.10.28 QA autorizare'","Q=B/'2026.10.28 QA server'")
start=src.index("body='''");end=src.index("'''",start+8)+3
body='''2026.10.28 | COMPLETARE AUDIT MA37 CU VERIFICAREA SERVERULUI
Status scurt: raport consolidat PDF, 18 pagini, cu inventar server incorporat. Versiunea 2026.10.27 pastrata. Acces in citire la \\192.168.100.151/site-uri/schallergasse35, stocarea activa data/uploads.
Constatare: toate cele 184 de fisiere descarcate online exista identic SHA-256 pe server. In pagini sunt 189 fisiere: 184 deja inventariate, un TXT de test P3 si patru fisiere P20 straine proiectului (cod web/imagini Eva-Learn, CSV produse, ODS import contabil). P18/P19 nu au fisiere stocate; P10 si P13-P17 fara documente. Un PNG personal este in afara paginilor, neinterpretat ca act de autorizare. Baza PostgreSQL si backup-urile istorice nu au fost auditate.
Ultimul raspuns: utilizatorul indica saga-server, folder site-uri, in conversatie. Nu este raspuns nou MA37/PECH; nu s-a verificat email nou.
Urmatorul pas: recuperare planset vizat MA37/Rechtskraft; coordonare si semnare dosar actual prin proiectant; reconciliere versiuni si denumire releveu P2.
Sursa: 00.Proiect/2026.10.28 Audit autorizare si servieta/2026.10.28 Schallergasse 35 - Audit acte MA37 si servieta.pdf; folder map/2026.10.28 QA server/2026.10.28 Inventar server.json; comparatia de baza 2026.10.27.
Site nemodificat, accesurile nemodificate, fara email trimis/depunere/acceptare. Datele de autentificare nu se salveaza in raport sau jurnal. Acoperirea Eva-Mail ramane neschimbata.
'''
src=src[:start]+'body='+repr(body)+src[end:]
src=src.replace("'pagini':16","'pagini':18").replace("'site':'read-only; P18-P20 neinspectate'","'site':'read-only; P18-P20 verificate fizic; DB neinterogata'")
src=src.replace('Solicitare: verificarea actelor Schallergasse necesare autorizarii la Viena, inclusiv stampile/semnaturi, inventarul existent si comparatia tuturor documentelor accesibile in servieta ac-wohnart.at; rezultat intr-un document.','Solicitare initiala: audit acte MA37 si servieta. Completare utilizator: Site-ul îl găsești pe saga-server în folderul site-uri.')
exec(compile(src,'2026.10.28 Inregistrare audit server','exec'))
