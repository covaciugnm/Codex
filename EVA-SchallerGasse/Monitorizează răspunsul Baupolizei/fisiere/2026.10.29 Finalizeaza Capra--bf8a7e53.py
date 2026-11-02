from pathlib import Path
import json,shutil,hashlib,datetime,olefile
root=Path.cwd();out=root/'08. Corespondenta/2026.10.29 Capra Baupolizei';day='2026.10.29'
p=next((root/'folder map/2026.10.29 MA37 original').glob('*.msg')); dest=out/'2025.11.19 MA37 Bianca Mitternast - Rechtskraft si Uberwachungsakt.msg';shutil.copy2(p,dest)
o=olefile.OleFileIO(dest)
def prop(k):
 for s in o.listdir():
  if len(s)==1 and s[0].startswith('__substg1.0_'+k):return o.openstream(s).read().decode('utf-16-le' if s[0].endswith('001F') else 'cp1252',errors='replace')
 return ''
original={'date_readable':'2025.11.19','status':'PRIMIT de Capra; original MSG anexat ulterior','eva_email_id':'5b856cc4-3328-47d2-816b-17ad61f6018b','eva_attachment_id':'bf1d6c20-ff68-4467-a4ab-53affa627f27','sender':prop('0C1F'),'subject':prop('0037'),'headers_original':prop('007D'),'body_original':prop('1000'),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(out/'2025.11.19 MA37 original extras.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'2025.11.19 MA37 original extras.txt').write_text('Data: 2025.11.19 | PRIMIT de Capra\nSursa: MSG original din anexa bf1d6c20 a emailului EVA 5b856cc4-3328-47d2-816b-17ad61f6018b.\n\n'+original['body_original'],encoding='utf-8')
data=json.loads((out/'2026.10.29 Dovezi cautari si acoperire.json').read_text(encoding='utf-8'))
report='''2026.10.29 | CAPRA – BAUPOLIZEI / MA37
Status scurt: Cereri TRIMISE la MA37 și Capra; răspuns nou al autorității neidentificat în căsuțele accesibile. Monitorizare activă luni–vineri, 10:00, 12:00 și 16:00, fusul aplicației UTC+02:00, până la oprirea expresă de către utilizator. Notificare numai la noutăți relevante, eșec sau acțiune necesară.

Ultima comunicare: Capra 2026.10.29 13:34:23 UTC+02:00, ID EVA 478abcb0-1094-4b10-b3e4-ecbc02840715, PRIMIT în CC de office@ac-wohnart.at; cerere efectiv expediată de Capra către sabine.cseh@wien.gv.at și ggw.kanzlei@ma37.wien.gv.at. CC original: office@ac-wohnart.at și «MA 37 GG West,» (adresa completă nu este rezolvată de API; nu este inventată).
Solicită existența în Bauakt/Überwachungsakt a planurilor vizate și reviziilor, deciziilor și anexelor, documentației de depunere și derogărilor; acces și date posibile pentru consultare.

CRONOLOGIE ȘI CONTEXT
2025.11.17–2025.11.18: ARESCO transmite procura Baupolizei; utilizatorul o retransmite. Procura și emailurile sunt salvate.
2025.11.19: Capra cere confirmarea caracterului definitiv al deciziilor din 2023.03.16 și 2023.04.21 și consultarea dosarului.
2025.11.19 10:49:47 UTC: răspuns original MA37, Bianca Mitternast, în numele ggw.stadterneuerung1@ma37.wien.gv.at, către Capra. Confirmă că deciziile sunt definitive din 2023.06.01. Indică Planeinsicht MA37 West, 01 4000 37720, și cere să se menționeze explicit Überwachungsakt. Explică faptul că proiectul nu este încă oficial finalizat, astfel documentația nu se află în Hauseinlage. Cere procura proprietarului. Acesta este răspuns administrativ original, nu numai afirmația avocatului. Nu confirmă însă stadiul actual din 2026.10.29 sau predarea planurilor.
2025.11.19: răspuns separat Sabine Cseh, citat în emailul Capra de azi: link de rezervare pentru consultare; pentru Rechtskraft indică 01 4000 37810. Acest mesaj separat nu conține confirmarea caracterului definitiv.
2025.11.20: Capra rezumă due diligence și anexează arhiva care conține MSG-ul original Mitternast. Arhiva 7z și MSG-ul sunt salvate și citite. Afirmațiile privind termenele din email sunt opinia istorică a avocatului, nu o nouă analiză juridică.
2026.03.17: Capra confirmă primirea electronică Bestandsunterlagen, Energieausweis DG și Bauphysikalische Unterlagen; proces-verbal anexat. Aceasta nu dovedește un inventar complet al planurilor vizate. Două corpuri de conversație sunt trunchiate de API, indicat în JSON/TXT.
2026.09.18: confirmare de rezervare Planeinsicht pentru 2026.09.25; rezervarea singură nu dovedește efectuarea vizitei. Vizita efectuată este relatată separat de utilizator în actualizarea 2026.10.28.
2026.09.22: cererea TRIMISĂ către autorități solicită actualizarea proprietarului, situația autorizației, termene, obligații și dosare. ID 05fba18c-d593-40d6-a310-4d076253fab6.
2026.10.28: ciorne locale/EVA către Capra și MA37, păstrate ca istoric. Nu sunt transformate retroactiv în mesaje trimise.
2026.10.29 12:49:12 UTC+02:00: cerere TRIMISĂ către Capra privind predarea contractuală a exemplarelor vizate, ID f36feb1c-1b40-43f8-b34b-7f7e47dcedac, fără atașamente.
2026.10.29 12:49:46 UTC+02:00: cerere TRIMISĂ direct la west@ma37.wien.gv.at, ID c45958f2-9372-4430-acfe-f175759221cf, șase atașamente. Solicită inclusiv cercetarea exemplarului C la Bauinspektion/Überwachungsarchiv, traseul documentelor, depunătorii, reprezentarea și dovezile predării. Acesta este textul efectiv trimis, care diferă de ciorna istorică.
2026.10.29 13:34:23 UTC+02:00: Capra revine la autoritate; cererea descrisă mai sus.

Următorul pas: urmărirea răspunsului MA37 și a mesajelor Capra; verificarea explicită a Überwachungsakt și exemplarului C; obținerea inventarului, copiilor vizate, stadiului actual și modalității de acces. Niciun termen de întâlnire nou confirmat, nicio predare a planurilor confirmată.

ACOPERIRE ȘI LIMITE
Căutări fără limită de dată în ambele conexiuni Eva-Mail: 1539234, Akteneinsicht, sabine.cseh, Baupolizei, ma37.wien.gv.at, Rechtskraft, Bestandsunterlagen, CH 251119, Einreichpläne, Vollmacht Baupolizei; căutări după expeditor wien.gv.at și CERHA + Schallergasse. Rezultatele CERHA și referinței dosarului au fost paginate integral. Metadatele includ și rezultate colaterale (oferte, utilități, tranzacția imobiliară), care nu sunt răspunsuri MA37 la cererea actuală. Sunt arhivate 11 mesaje centrale și 31 atașamente, plus MSG-ul original din 2025.11.19 și conversațiile citate în ele. Nu se afirmă acces la toate comunicările interne ale avocatului sau autorității.
Sincronizare office în Primary: 2026.10.29 15:30:14 UTC+02:00; office în a doua conexiune: 2026.10.29 15:03:44 UTC+02:00; Gmail Primary: 2026.10.29 12:32:39 UTC+02:00. Căsuțele shared/team necăutabile sunt excluse, celelalte au limitele proprii salvate în dovadă. Mesajele ulterioare sincronizării pot lipsi.
Descărcarea HTTP a returnat 403. Fișierele mici au fost salvate integral prin base64; pentru fișierele mari s-au reutilizat originalele locale neschimbate față de SHA-256 din index, cu dimensiune și primii 65.536 octeți identici celor returnați de EVA. Nu se pretinde o verificare integrală byte-for-byte cu EVA pentru aceste copii reutilizate. EML-urile sunt exporturi reconstruite, nu MIME original; JSON păstrează metadatele și semnalul de trunchiere. Originalul MSG Mitternast rămâne nemodificat.

Surse: 08. Corespondenta/2026.10.29 Capra Baupolizei; 2026.10.29 Dovezi cautari si acoperire.json; originalul MSG 2025.11.19; dosarele istorice 2026.10.28 Capra dosar autorizare și MA37 cerere planuri vizate.
Automatizare: capra-baupolizei-autoriza-ie-i-dosar-ma37, ACTIVE. Niciun email trimis de agent în această verificare.
'''
(out/'2026.10.29 Context si jurnal Capra Baupolizei.txt').write_text(report,encoding='utf-8')
hist=root/'folder map/2026.10.29 Istoric inainte Capra Baupolizei';hist.mkdir(exist_ok=True)
for rel in ['2026.10.29 Status proiect.txt','2026.10.29 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - CERHA HEMPEL.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.29 Log discutii - MA37 Baupolizei.txt','folder map/README.md']:
 q=root/rel;old=q.read_text(encoding='utf-8-sig') if q.exists() else ''
 if q.exists():
  backup=hist/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(q,backup)
 q.parent.mkdir(parents=True,exist_ok=True);q.write_text(report+'\n\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
print('Raport, originale, jurnale proiect si parteneri actualizate; istoric pastrat.')
