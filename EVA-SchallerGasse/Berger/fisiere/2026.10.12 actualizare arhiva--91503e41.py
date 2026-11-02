from pathlib import Path
import json,shutil,hashlib
from pypdf import PdfReader
root=Path.cwd();dest=Path(__file__).resolve().parent
relative=dest.relative_to(root).as_posix()
base=root/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
history=dest/'2026.10.12 Istoric inainte de contracte';history.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
art=[]
for name,net,vat,gross in [('BERGER',45000,9000,54000),('PECH',69300,13860,83160)]:
    for ext in ['docx','pdf']:
        p=dest/f'2026.10.12 Propunere contract {name}.{ext}'
        rec={'prestator':name,'cale':p.relative_to(root).as_posix(),'format':ext,'sha256':sha(p),'net_EUR':net,'TVA_EUR':vat,'brut_EUR':gross,'statut':'Propunere AG NETRIMISĂ și NESEMNATĂ; extinderi neacceptate'}
        if ext=='pdf':rec['pagini']=len(PdfReader(p).pages)
        art.append(rec)
manifest={'data':'2026.10.12','documente':art,'acoperire':'Servicii structurale complete, asistență, Prüfingenieur, §128 și Bauwerksbuch întreg existent+nou; fără BauKG și fără management general REALIG.','originale':'Copiile ofertelor și mesajelor primite au hash identic cu sursele existente; nu reprezintă emailuri ori oferte noi.','audit':'2026.10.12 Audit contracte.txt și 2026.10.12 Surse audit contracte.json','QA':'Toate cele 41 de pagini au fost inspectate vizual. După ultimele corecții au fost comparate hashurile PNG; toate paginile modificate au fost reexaminate.','noi_mesaje':0,'trimiteri':0,'semnaturi':0,'plati':0}
(dest/'2026.10.12 Registru propuneri contracte.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa='''2026.10.12 | Verificare vizuală finală a propunerilor contractuale

Verdict: PASS. Word a exportat direct documentele DOCX în PDF cu fereastra ascunsă, macrocomenzi dezactivate și fișierele deschise read-only. Helperul Documents și Poppler din runtime au produs imaginile paginilor. LibreOffice bundled nu este disponibil pe această gazdă Windows; nu s-a utilizat LibreOffice desktop al utilizatorului.
BERGER: 18 pagini. Agentul principal a inspectat p.1–4, redactorul p.5–18 la rezoluția completă. Ultimele modificări de coloană și câmpuri au schimbat numai p.16–18; acestea au fost reexaminate de agentul principal. Ultima scurtare a antetului a schimbat numai p.17–18, reexaminate din nou. Celelalte PNG-uri au hash identic cu setul deja inspectat.
PECH: 23 pagini. Agentul principal a inspectat p.1–4, redactorul PECH p.5–23 la rezoluția completă. Ultima modificare a etichetei D5 a schimbat numai p.14, reexaminată de agentul principal. Celelalte PNG-uri au hash identic cu setul deja inspectat.
Antetele tabelelor sunt legate de primul rând, coloanele și câmpurile sunt lizibile, semnăturile sunt păstrate integral, fără pagini goale, suprapuneri, text tăiat ori cuvinte rupte fără motiv. Prețurile și eșalonările sunt verificate separat în audit.
Fișierele livrabile sunt numai propunerile Word și PDF. Imaginile și scripturile de lucru nu sunt propuneri comerciale și nu sunt emailuri trimise.
'''
(dest/'2026.10.12 Verificare vizuala contracte.txt').write_text(qa,encoding='utf-8')
summary=f'''2026.10.12 | Propuneri contracte BERGER și PECH pentru lectură

Status scurt: pregătite două propuneri complete în germană, cu sinteză în română, Word și PDF. BERGER: 45.000 EUR net /54.000 EUR cu TVA, 18 pagini. PECH: 69.300 EUR net /83.160 EUR cu TVA, 23 pagini. Cele patru poziții BERGER și cele șase poziții PECH sunt păstrate ca sume. Extinderile sunt propuneri noi AG în același total, neacceptate de prestatori.
Servicii: întregul proiect structural și detaliile necesare, asistență, Prüfingenieur până la final, confirmare §128 prin persoană legal abilitată și Bauwerksbuch pentru întregul existent și intervențiile noi. BauKG și managementul general REALIG nu sunt comandate.
Calendar: BERGER, început prin acord/imediat după semnare și documente, circa12luni din ofertă; termenele D1–D5 la3/6/8/10/12săptămâni sunt noi propuneri AG. PECH, început după comandă scrisă și documente, calendar prin acord;12luni/15luni condiționat și D1la3săptămâni sunt propuneri AG, nu durată fixă ofertată. D2–D5 sunt legate de etapele efective și se confirmă înainte de execuție.
Clauze: preț fix, suplimente aprobate, drepturi de utilizare/modificare/terți, predări editabile, remedierea erorilor, plăți la30zile pe livrabile, retenție5%net și garanție contractuală minimum3ani cu rezervarea drepturilor legale, încetare/decont și predare. Drepturile imperative §1170b sunt păstrate; încetarea liberă nu promite cost zero în contradicție cu §1168.
Ultimele răspunsuri reale rămân: BERGER2026.08.17 și PECH2026.09.17. Originalele ofertelor și mesajelor relevante sunt copiate cu hash identic; nu sunt comunicări externe noi.
Următorul pas: lectura utilizatorului și observațiile asupra propunerilor; confirmarea ulterioară a volumului/prețului/calendarului, persoanelor PI/§128/BWB, asigurării și datelor de semnare. Documentele sunt NETRIMISE și NESEMNATE; fără acceptare, debut, plată sau comunicare externă nouă.
Sursa: {relative}/2026.10.12 Registru propuneri contracte.json; Word/PDF în același dosar; audit comun și sursele RIS, verificare vizuală completă. Numerele de mesaje și originale din arhiva EVA rămân neschimbate.
'''
for a,b in [('circa12luni','circa 12 luni'),('la3/6/8/10/12săptămâni','la 3/6/8/10/12 săptămâni'),('12luni/15luni','12 luni/15 luni'),('D1la3săptămâni','D1 la 3 săptămâni'),('la30zile','la 30 zile'),('retenție5%net','retenție 5% net'),('minimum3ani','minimum 3 ani'),('BERGER2026','BERGER 2026'),('PECH2026','PECH 2026')]:summary=summary.replace(a,b)
(dest/'2026.10.12 Jurnal actualizare contracte.txt').write_text(summary,encoding='utf-8')
def prepend(p,text):
    backup=history/p.name
    if not backup.exists():shutil.copy2(p,backup)
    old=p.read_text(encoding='utf-8-sig')
    if text.splitlines()[0] not in old[:300]:p.write_text(text+'\nISTORIC PĂSTRAT\n\n'+old,encoding='utf-8')
for name in ['2026.10.12 Status proiect.txt','2026.10.12 Log progres proiect.txt']:prepend(root/name,summary)
for provider,last,eid,net,nextstep in [
    ('Markus Berger','2026.08.17','ce6905cb-0c93-4e6b-8cde-7e300dfc874c',45000,'Lectura draftului, confirmarea disponibilității, extinderilor în același total și a persoanelor eligibile PI/§128/BWB; actualizare date AN.'),
    ('Pech','2026.09.17','63cd2bcb-2160-4027-b6c8-25bb42d9ae50',69300,'Lectura draftului, acceptarea explicită PI și Bauwerksbuch în pozițiile05/06, calendar, nominalizări și asigurare.')]:
    pr='BERGER' if provider=='Markus Berger' else 'PECH'
    entry=f'''2026.10.12 | Propunere de contract pregătită pentru lectură
Status scurt: propunere AG în germană cu sinteză RO, Word/PDF, total {net:,.0f} EUR net păstrat. Toate extinderile, inclusiv Bauwerksbuch existent+nou și funcția Prüfingenieur până la final, sunt propuse în totalul păstrat; nu sunt acceptate automat. NETRIMISĂ și NESEMNATĂ.
Ultimul răspuns: {last}, ofertă primită; ID Eva-Mail {eid}. Nu este identificat un răspuns nou prin această redactare locală.
Următorul pas: {nextstep}
Sursa: {relative}/2026.10.12 Propunere contract {pr}.docx și PDF; audit comun și registru de propuneri în același dosar. Originalul ofertei și mesajul primit sunt copiate identic.
Nu s-a trimis email, semnat sau plătit.
'''.replace(f'{net:,.0f}',f'{net:,}'.replace(',','.')).replace('pozițiile05/06','pozițiile 05/06')
    prepend(base/'Parteneri'/f'2026.10.12 Log discutii - {provider}.txt',entry)
prepend(root/'folder map/README.md',f'''# 2026.10.12 — Propuneri contracte BERGER și PECH pentru lectură

Dosar: ../{relative}/. Propuneri Word/PDF în germană cu sinteză română: BERGER 45.000 EUR net, 18 pagini; PECH 69.300 EUR net, 23 pagini. Originalele ofertelor și mesajelor sunt copii identice. Toate extinderile structurale, Prüfingenieur și Bauwerksbuch pentru existent+nou sunt propuse în totalurile păstrate. Fără BauKG și management general REALIG. NETRIMISE/NESEMNATE; acceptarea și calendarul efectiv nu sunt confirmate. Începe cu 2026.10.12 Propunere contract BERGER.docx sau PECH.docx, apoi 2026.10.12 Audit contracte.txt și registrul de propuneri. Jurnalele proiectului și partenerilor au fost completate, istoricul păstrat; nu sunt mesaje noi.
''')
register=base/'2026.10.12 Registru comunicatii.json'
if not (history/register.name).exists():shutil.copy2(register,history/register.name)
r=json.loads(register.read_text(encoding='utf-8'));up=r.setdefault('actualizari_punctuale',[])
entry={'data':'2026.10.12','tip':'propuneri_contracte_BERGER_PECH','sursa':relative+'/2026.10.12 Registru propuneri contracte.json','mesaje_noi':0,'originale_noi':0,'trimiteri':0,'statut':'NETRIMISE/NESEMNATE; totaluri păstrate; extinderi neacceptate','net_EUR':{'BERGER':45000,'PECH':69300}}
if isinstance(up,list):
    if not any(isinstance(x,dict) and x.get('tip')==entry['tip'] for x in up):up.append(entry)
else:up[entry['tip']]=entry
register.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Final proposals saved, sources preserved, journals and reference registry updated. No message counts changed.')
