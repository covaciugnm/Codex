from pathlib import Path
import json,shutil,hashlib
ROOT=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
TEMP=Path(__file__).with_name('2026.10.12 Dovezi temporare Eva.json');D=json.loads(TEMP.read_text(encoding='utf-8'))
OUT=ROOT/'08. Corespondenta/2026.10.12 Verificare zilnica';OUT.mkdir(exist_ok=True)
ARCH=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail';PART=ARCH/'Parteneri'
C=json.loads((ARCH/'2026.10.11 Registru comunicatii.json').read_text(encoding='utf-8-sig'))
IDS={r['id'] for r in C['comunicatii']}
unique={e['id']:e for q in D['searches'] for e in q['data'].get('items',[])}
D['comparatie_arhiva']=[{'id':eid,'deja_in_registru':eid in IDS,'relevant_proiect':False,'motiv':'Mesaj test cunoscut' if eid in D['known_excluded_ids'][:2] else 'Notificare cont Google, fără legătură cu proiectul'} for eid in unique]
assert set(unique).issubset(set(D['known_excluded_ids']))
assert all(not q['raw'].get('isError') and q['data']['total']<=len(q['data']['items']) for q in D['searches'])
assert len(D['searches'])==46
D['rezultat']={'mesaje_relevante_noi':0,'atasamente_relevante_noi':0,'cautari_complete':46,'perioada':'2026.10.10–12'}
(OUT/'2026.10.12 Dovezi verificare Eva-Mail.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf-8')
status='2026.10.12: nu au fost identificate comunicări relevante noi față de verificarea generală2026.10.11 și reverificarea punctualăTOMS din aceeași zi. Au fost preluate toate rezultatele celor46căutări, pentru2026.10.10–12. Cele două mesaje test office și o notificareGoogle fără legătură cu proiectul sunt excluse. Zero mesaje și zero atașamente relevante noi; nu există originale noi de descărcat.'
coverage='Office sincronizat până la2026.10.12 08:00:19 România; cosmin@ig.ro numai până la2026.10.10 02:30:10 România. Căutările globale acoperă căsuțele accesibile, cu sincronizări diferite. Exportul/API nu garantează copia MIME integrală. Nicio modificare locală față de indexul2026.10.11 12:44:00 România.'
source=(OUT/'2026.10.12 Dovezi verificare Eva-Mail.json').relative_to(ROOT).as_posix()
report='2026.10.12 | Verificare zilnică Schallergasse35\n\nStatus scurt: '+status+'\nAcoperire: '+coverage+'\nSursa: '+source+'\n\nRepere existente, fără comunicare nouă:\n- TOMS: refuz2026.10.08 din lipsă de resurse; întinderea față de v4.1 rămâne de clarificat. Acceptarea, semnarea și începerea nu sunt confirmate.\n- DONAU/Commerz: termen comunicat2026.10.12 pentru5.326,15EUR; fără plată, amânare sau restabilire a acoperirii confirmată în comunicările disponibile. Nu se adaugă Q4 din nou.\n- MarkusBerger: oferta2026.08.17,45.000EUR net; termen calculat de8săptămâni2026.10.12, fără prelungire confirmată.\n- Dr.PECH: ofertă2026.09.17,69.300EUR net; numai statica de execuție42.000EUR;90zile, calendar/disponibilitate neconfirmate.\n- SCHAUERLEUTE: vizita propusă2026.10.09 nu este documentată ca efectuată.\n- Füglister: oferta promisă în săptămâna2026.10.12–18, fără zi fixă; nu există preț nou primit.\n\nUrmătorul pas: urmărirea răspunsurilor și clarificărilor existente; fără deducerea acceptării, semnării, efectuării întâlnirilor sau plății din simpla scurgere a termenelor.\n\nNicio comunicare trimisă, semnare ori plată efectuată. Arhiva păstrează801mesaje și825originale salvate; numărul mesajelor/anexelor nu a fost majorat. TXT/JSON2026.10.12 sunt actuale; versiunile anterioare sunt păstrate.\n'
(OUT/'2026.10.12 Raport verificare.txt').write_text(report,encoding='utf-8')
for label in ['Status proiect.txt','Log progres proiect.txt']:
    prior=ROOT/('2026.10.11 '+label)
    hist=prior.read_text(encoding='utf-8-sig') if prior.exists() else ''
    (ROOT/('2026.10.12 '+label)).write_text(report+'\nISTORIC\n\n'+hist,encoding='utf-8')
C['data_actualizarii']='2026.10.12'
C['acoperire']['verificare_incrementala']={'data':'2026.10.12','mesaje_noi':0,'originale_noi':0,'pdf_salvate':0,'imagini_salvate':0,'office_sincronizat':'2026.10.12 08:00:19 România','cosmin_sincronizat':'2026.10.10 02:30:10 România','perioada':'2026.10.10–12','cautari_complete':46,'limita':coverage}
C.setdefault('actualizari_punctuale',[]).append({'data':'2026.10.12','subiect':'Verificare zilnică fără comunicări relevante noi','mesaje':0,'originale':0,'sursa':source})
updates={
'TOMS':('Ultimul răspuns primit2026.10.08: refuz de preluare în prezent din motive de resurse; citează firulv3, fără analiză explicită av4.1. Nu există acceptare, semnare sau începere confirmate.','Clarificarea întinderii refuzului față dev4.1 și identificarea unui înlocuitor; D1 nu este pornit fără semnare confirmată.','cdd301b0-457e-4452-a394-6eea21256e61'),
'Donau Versicherung':('Ultimul răspuns primit2026.10.06: DONAU refuză încetarea și declară lipsa acoperirii pentru prime restante. Nu există răspuns nou, decont acceptat, plată sau restabilire confirmată.','Clarificarea acoperirii, decontului și condițiilor plății; termenulCommerz2026.10.12 nu este suspendat prin această verificare.','2c273256-a0bf-408b-bb22-09718372e888'),
'Maritczak - Commerz Inkasso':('Ultimul răspuns directCommerz2026.09.30:5.326,15EUR, termen2026.10.12. IncludeQ4; nu există răspuns nou sau încasare/amânare confirmată.','Verificarea situației actuale și a decontului, fără dublareaQ4 sau marcarea unui ordin de plată ca încasare.','1fa19552-d1fd-459e-92b3-57ed5319d18c'),
'Markus Berger':('Ofertă primită2026.08.17:45.000EUR net pentru calcule, planuri, asistență șiPrüfingenieur. Valabilitate8săptămâni, termen calculat2026.10.12; fără prelungire/acceptare/disponibilitate confirmate.','Reconfirmarea valabilității, disponibilității și calendarului înainte de atribuire.','ce6905cb-0c93-4e6b-8cde-7e300dfc874c'),
'Pech':('Oferta2026-470/AN01 primită2026.09.17:69.300EUR net pentru pachet, cu42.000EUR statică de execuție. Valabilitate90zile, termen calculat2026.12.16. Nu este comandă semnată; oferta nu numește expres funcțiaPrüfingenieur.','Reconfirmarea disponibilității și calendarului; clarificarea întinderii și a funcțieiPrüfingenieur separat deBaubegleitung.','63cd2bcb-2160-4027-b6c8-25bb42d9ae50'),
'SCHAUERLEUTE':('Ultimul răspuns2026.10.07 cere confirmarea vizitei2026.10.09 09:30Viena. Nicio confirmare de efectuare, reprogramare sau ofertă ulterioară identificată.','Clarificarea dacă vizita a avut loc și urmărirea documentelor/ofertei, fără presupunerea efectuării.','7297d88d-378c-4d49-95f0-12838396fbdd')}
for partner,(current,nextstep,eid) in updates.items():
    row=next(r for r in C['comunicatii'] if r['id']==eid)
    previous=sorted(PART.glob('* Log discutii - '+partner+'.txt'))
    hist=previous[-1].read_text(encoding='utf-8-sig') if previous else ''
    log='2026.10.12 | Verificare fără mesaj nou\nStatus scurt: '+current+'\nUltimul răspuns: '+row['data']+' | '+row['subiect'].replace('\r','').replace('\n',' ')+'\nUrmătorul pas: '+nextstep+'\nSurse: '+row['cale']+'; ID '+eid+'; '+source+'\n\nISTORIC\n\n'+hist
    (PART/('2026.10.12 Log discutii - '+partner+'.txt')).write_text(log,encoding='utf-8')
    entry=next((s for s in C['statusuri'] if s['partener']==partner),None)
    if entry is not None:
        entry.update({'status':current,'ultimul_primit':row['data'],'subiect_ultimul_primit':row['subiect'],'urmatorul_pas':nextstep,'sursa_status':[row['cale'],source],'verificat':'2026.10.12'})
(ARCH/'2026.10.12 Registru comunicatii.json').write_text(json.dumps(C,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(ARCH/'2026.10.11 Registru atasamente.json',ARCH/'2026.10.12 Registru atasamente.json')
readme=ROOT/'folder map/README.md';old=readme.read_text(encoding='utf-8-sig')
intro='''# 2026.10.12 — Verificare fără comunicări noi

Puncte curente: ../2026.10.12 Status proiect.txt; ../2026.10.12 Log progres proiect.txt; registrele2026.10.12 din arhivaEva-Mail; ../08. Corespondenta/2026.10.12 Verificare zilnica/2026.10.12 Raport verificare.txt.46căutări complete pentru2026.10.10–12; niciun mesaj relevant nou și nicio anexă relevantă nouă. Office sincronizat2026.10.12 08:00:19România; cosmin@ig.ro numai2026.10.10 02:30:10. Jurnalele partenerilor păstrează ultimele răspunsuri reale. Pech actualizat pe oferta deja arhivată2026.09.17, fără a o prezenta ca ofertă nouă. TermenCommerz și expirarea calculatăBerger sunt astăzi2026.10.12, fără amânare/prelungire confirmată. Nu s-au trimis mesaje, semnat sau plătit. Istoricul este păstrat;801mesaje și825originale în arhivă.

'''
if not old.startswith('# 2026.10.12'):readme.write_text(intro+old,encoding='utf-8')
print(json.dumps({'raport':str(OUT/'2026.10.12 Raport verificare.txt'),'mesaje_total':len(C['comunicatii']),'mesaje_noi':0,'atasamente_noi':0,'cautari':len(D['searches'])},ensure_ascii=False))
