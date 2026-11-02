from pathlib import Path
import json,base64,hashlib,datetime
from email.message import EmailMessage
from email.utils import format_datetime
BASE=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
TEMP=Path(__file__).with_name('2026.10.11 Manifest Eva-Mail temporar.json')
M=json.loads(TEMP.read_text(encoding='utf-8'))
OUT=BASE/'08. Corespondenta/2026.10.11 Verificare zilnica';OUT.mkdir(exist_ok=True)
ARCH=BASE/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
old=json.loads((ARCH/'2026.10.08 Registru comunicatii.json').read_text(encoding='utf-8-sig'))
oldatt=json.loads((ARCH/'2026.10.08 Registru atasamente.json').read_text(encoding='utf-8-sig'))
oldids={r['id'] for r in old['comunicatii']}
e=next(r for r in M['emails'] if r['id']=='cdd301b0-457e-4452-a394-6eea21256e61');d=e['data']
stem='2026.10.11 PRIMIT TOMS cdd301b0'
src=(OUT/(stem+'.txt')).relative_to(BASE).as_posix()
(OUT/(stem+'.json')).write_text(json.dumps({'data_lizibila_verificare':'2026.10.11','statut':'PRIMIT','email_original_api':d,'raspuns_tehnic':e['raw']},ensure_ascii=False,indent=2),encoding='utf-8')
metadata='\n'.join(['2026.10.11 | Export Eva-Mail','Statut: PRIMIT','Data mesajului: 2026.10.08 10:07:36 România','Data tehnică originală: '+d['received_at'],'Subiect: '+d['subject'],'Expeditor: '+d['from_address'],'Destinatari: '+', '.join(d['to']),'CC: '+', '.join(d['cc']),'ID Eva-Mail: '+d['id'],'Corp complet în API; exportul nu este MIME integral.','\nTEXT ORIGINAL\n'])
(OUT/(stem+'.txt')).write_text(metadata+d['text'],encoding='utf-8')
em=EmailMessage();em['From']=d['from_address'];em['To']=', '.join(d['to']);em['Cc']=', '.join(d['cc']);em['Subject']=d['subject'].replace('\r','').replace('\n',' ')
em['Date']=format_datetime(datetime.datetime.fromisoformat(d['received_at'].replace('Z','+00:00')));em['X-Eva-Mail-ID']=d['id'];em['X-Eva-Export']='API reconstructed text; not original MIME';em.set_content(d['text'])
(OUT/(stem+'.eml')).write_bytes(em.as_bytes())
a=M['original'];data=base64.b64decode(a['content_base64'])
assert a['eof'] and a['offset']==0 and len(data)==a['size']==8850
digest=hashlib.sha256(data).hexdigest();assert digest==a['chunk_sha256']
attpath=OUT/'2026.10.11 ORIGINAL f3723e10 image001.png';attpath.write_bytes(data)
ar={'id':a['id'],'email_id':d['id'],'data':'2026.10.11','partener':'TOMS','nume_original':a['filename'],'octeti':len(data),'sha256':digest,'cale':attpath.relative_to(BASE).as_posix(),'stare':'salvat original integral'}
(OUT/'2026.10.11 Registru descarcari.json').write_text(json.dumps([ar],ensure_ascii=False,indent=2),encoding='utf-8')
proof={k:M[k] for k in ['data_lizibila','last_verification','searches','mailboxes','audit_local']}
proof['comparatie_iduri']=[{'id':r['id'],'deja_arhivat':r['id'] in oldids,'relevant':r['id']==d['id']} for r in M['emails']]
proof['excluderi']='Cele două mesaje test de pe office, un link Facebook și rezultate comerciale fără legătură cu proiectul au fost excluse. Sunt păstrate metadatele căutărilor; cele două teste au fost citite integral.'
proof['paginare']='Toate cele 44 căutări sunt complete: totalul fiecăreia este sub limita primei pagini de 50.'
(OUT/'2026.10.11 Dovezi cautari si audit.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
status='2026.10.08: TOMS/Dagmar Zottl anunță că nu poate accepta în prezent comanda amplă și intensivă din motive de resurse. Mesaj primit la 10:07:36 România, CC Ferdinand Toms. Răspunde firului despre v3 și oferta suplimentară; nu precizează separat toate componentele ori statutul v4.1. Nu există acceptare, semnare sau începere confirmată. Niciun preț nou și niciun contract nou anexat.'
nextstep='Clarificarea întinderii refuzului (întregul pachet sau o parte) și identificarea unui prestator alternativ pentru serviciile necesare. Calendarul de lucru nu se consideră pornit; data efectivă cere un acord confirmat.'
row={'data':'2026.10.08','ora_utc':'07:07','partener':'TOMS','domeniu':'Tragwerksplanung și Prüfingenieur','sens':'PRIMIT','subiect':d['subject'],'expeditor':d['from_address'],'destinatari':', '.join(d['to']),'cc':', '.join(d['cc']),'id':d['id'],'cale':src,'atasamente':1,'trunchiat':False}
if d['id'] not in oldids:old['comunicatii'].append(row)
entry=next(s for s in old['statusuri'] if s['partener']=='TOMS')
entry.update({'status':status,'ultima_comunicare':'2026.10.08','ultimul_primit':'2026.10.08','subiect_ultimul_primit':d['subject'],'urmatorul_pas':nextstep,'sursa_status':[src],'nivel':'Sinteză verificată pe mesaj integral','mesaje':int(entry.get('mesaje',0))+1})
if a['id'] not in {r['id'] for r in oldatt}:oldatt.append(ar)
cover=old['acoperire'];cover['mesaje_salvate']=len(old['comunicatii']);cover['atasamente_salvate']+=1;cover['atasamente_identificate']+=1;cover['mesaje_suplimentare_fata_de_lista']+=1
cover['verificare_incrementala']={'data':'2026.10.11','mesaje_noi':1,'originale_noi':1,'pdf_salvate':0,'imagini_salvate':1,'office_sincronizat':'2026.10.11 08:00:13 România','cosmin_sincronizat':'2026.10.10 02:30:10 România','perioada':'2026.10.07–11','ultima_verificare_salvata':'2026.10.08','cautari_complete':44,'limita':'Office până la2026.10.11 08:00:13; cosmin@ig.ro numai până la2026.10.10 02:30:10; alte conturi au sincronizări diferite. Export API, nu copie MIME integrală. PDF local mixt de39pagini verificat parțial.'}
old['data_actualizarii']='2026.10.11';old['actualizari_punctuale'].append({'data':'2026.10.11','subiect':'TOMS refuză preluarea din motive de resurse; recuperare după ultima verificare salvată2026.10.08','mesaje':1,'originale':1,'sursa':src})
(ARCH/'2026.10.11 Registru comunicatii.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
(ARCH/'2026.10.11 Registru atasamente.json').write_text(json.dumps(oldatt,ensure_ascii=False,indent=2),encoding='utf-8')
partnerlog='2026.10.11 | Verificare zilnică\nStatus scurt: '+status+'\nUltimul răspuns: 2026.10.08 | '+d['subject'].replace('\r','').replace('\n',' ')+'\nUrmătorul pas: '+nextstep+'\nSursa: '+src+'; ID '+d['id']+'\n\nISTORIC\n\n'
prior=sorted((ARCH/'Parteneri').glob('* Log discutii - TOMS.txt'))
if prior:partnerlog+=prior[-1].read_text(encoding='utf-8-sig')
(ARCH/'Parteneri/2026.10.11 Log discutii - TOMS.txt').write_text(partnerlog,encoding='utf-8')
report='2026.10.11 | Noutăți față de ultima verificare salvată2026.10.08\n\n'+status+'\nUrmătorul pas: '+nextstep+'\nSursa: '+src+'; ID '+d['id']+'\n\nFișiere salvate: mesaj complet API înJSON/TXT și EML reconstruit; originalul image001.png (8.850octeți), SHA-256 '+digest+'. Nu există PDF sau ofertă nouă în acest mesaj.\n\nNu sunt comunicări relevante noi din2026.10.09–11 în rezultatele accesibile. DONAU/Commerz, SCHAUERLEUTE și ofertanții de lift nu au răspuns nou față de arhivă. Vizita SCHAUERLEUTE propusă pentru2026.10.09 nu este considerată efectuată în lipsa unei dovezi.\n\nReper existent, fără noutate de plată: Commerz a comunicat termenul2026.10.12 pentru5.326,15EUR. Nu s-a identificat o amânare, încasare sau restabilire a acoperirii; nu este un sold recunoscut.\n\nAcoperire: '+json.dumps(cover['verificare_incrementala'],ensure_ascii=False)+'\n\nAudit local:34EML cu timestamp schimbat au hashuri identice, deci nu sunt mesaje noi. Inbox/Documente-germana.pdf este un scan nou local de39pagini cu material mixt istoric, verificat parțial; nu îl prezentăm ca o comunicare externă nouă. Originalul este păstrat.\n\nNiciun mesaj trimis, contract semnat ori plată efectuată prin această verificare. Cele două mesaje test (unul trimis de utilizator, unul primit) nu sunt comunicări de proiect și nu au fost generate de această verificare. Istoricul este păstrat; TXT/JSON2026.10.11 sunt actuale, documentele vechi rămân istorice.\n'
(OUT/'2026.10.11 Raport verificare.txt').write_text(report,encoding='utf-8')
for name in ['Status proiect.txt','Log progres proiect.txt']:
    prior=BASE/('2026.10.08 '+name)
    history=prior.read_text(encoding='utf-8-sig') if prior.exists() else ''
    (BASE/('2026.10.11 '+name)).write_text(report+'\nISTORIC\n\n'+history,encoding='utf-8')
readme=BASE/'folder map/README.md';history=readme.read_text(encoding='utf-8-sig')
intro='''# 2026.10.11 — TOMS nu poate prelua comanda

Puncte curente: ../2026.10.11 Status proiect.txt; ../2026.10.11 Log progres proiect.txt; registrele2026.10.11 în arhivaEva-Mail și ../08. Corespondenta/2026.10.11 Verificare zilnica/2026.10.11 Raport verificare.txt. TOMS răspunde la2026.10.08, refuză preluarea în prezent din motive de resurse. Mesaj integral și imagine originală salvate. Nu este contract acceptat ori lucrare începută; întinderea exactă față de v4.1 cere clarificare. Verificarea recuperează perioada de la ultima preluare salvată2026.10.08, cu suprapunere din2026.10.07. Alte noutăți relevante din2026.10.09–11 nu sunt identificate. Office sincronizat2026.10.11 08:00:13România; cosmin@ig.ro numai2026.10.10 02:30:10. VizitaSCHAUERLEUTE nu este confirmată efectuată; termenulCommerz2026.10.12 nu este suspendat. Scanul localInbox/Documente-germana.pdf are39pagini istorice mixte, verificare parțială; nu este dovadă de comunicare nouă.34EML retimestampate au hash identic. Nicio trimitere, semnare sau plată. Istoricul este păstrat.

'''
if not history.startswith('# 2026.10.11'):readme.write_text(intro+history,encoding='utf-8')
print(json.dumps({'mesaje_total':cover['mesaje_salvate'],'atasamente_salvate_total':cover['atasamente_salvate'],'original_nou_salvat':str(attpath),'raport':str(OUT/'2026.10.11 Raport verificare.txt')},ensure_ascii=False))
