from pathlib import Path
import json,datetime,hashlib
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'08. Corespondenta/2026.10.08 Verificare zilnica'
ARCH=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
TMP=Path('C:/Users/User/.codex/visualizations/2026/10/01/01a0f6eb-c105-7760-973e-241d6f6be8c1/2026.10.08 Eva manifest temporar.json')
M=json.loads(TMP.read_text(encoding='utf-8'))
COMM=json.loads((ARCH/'2026.10.07 Registru comunicatii.json').read_text(encoding='utf-8-sig'))
ATTS=json.loads((ARCH/'2026.10.07 Registru atasamente.json').read_text(encoding='utf-8-sig'))
DL=json.loads((OUT/'2026.10.08 Registru descarcari.json').read_text(encoding='utf-8'))
PARTNERS={'64ef7967-215d-409a-863a-92d07e05bb2b':'Weigl','871127cd-1d04-4cae-866e-d666b76fd868':'Schmitt + Sohn','7297d88d-378c-4d49-95f0-12838396fbdd':'SCHAUERLEUTE','ff7cdedf-319b-4bf2-abba-ebd235dfbfa0':'Füglister','97799dc8-4942-4fd9-9142-003a0954f058':'Sturm Energie'}
STAT={
'Weigl':('2026.10.08: răspuns Ecker primit la 00:43:52 România (data tehnică UTC2026.10.07). Cere adresa exactă de ofertare și telefonul. Propune liftul de platformă numai pe partea dreaptă văzută de jos, cu intrare90°, pentru a păstra accesul spre curte. Două PDF-uri tehnice și imagine, fără preț nou.','Transmiterea/confirmarea adresei de ofertare și telefonului; verificare de proiectant a amplasării și cerințelor autorizate. Nicio ofertă acceptată.'),
'Schmitt + Sohn':('2026.10.07: răspuns Jeitler la negociere ANG0232318. Nu oferă Garantie, ci Gewährleistung; recomandă Vollunterhaltung. Acceptă planul de plată25/25/40/10 și confirmă taxeTÜV, verificare preliminară, recepție și notificare de finalizare incluse. Reconfirmă service:980 EUR/an mentenanță de bază sau completă în perioadaGewährleistung; completă ulterior1.960 EUR/an; alarmare600+SIM180+AWM240 EUR/an. Cu toate modulele:2.000 sau2.980 EUR/an net. AWM poate lipsi dacă există doi Aufzugswärter pentru controalele săptămânale. Indexare anuală dupăBaukostenindex;30min persoane captive,4–6h alte deranjamente; suplimente în afara programului. Fără listă de piese cu prețuri. Anexa service este datată2026.06.25 și retransmisă; modelele sunt nesemnate, pe10ani, nu contracte A&C acceptate.','Obținerea ofertei/contractului revizuit cu planul de plată, răspunderea pentru defecte, perioada și excluderile exacte; verificarea independentă a recepției și condițiilor mentenanței. Nicio comandă.'),
'SCHAUERLEUTE':('2026.10.07: Thomas Schauer revine și cere confirmarea vizitei propuse pentru2026.10.09,09:30 Viena/10:30 România sau alegerea altui termen. Solicitarea de documente din mesajul anterior rămâne. Nu este confirmare a beneficiarului ori vizită efectuată; fără ofertă nouă de preț.','Confirmarea ori reprogramarea vizitei și transmiterea documentelor cerute. Nu a fost trimisă o confirmare în această verificare.'),
'Füglister':('2026.10.07: transmite plan-model centralizat630kg/8persoane și catalog cabine. Declară verificare individualăASV în locul unei Baumusterbescheinigung și indică lista Betreuungsunternehmen. Oferta și restul răspunsurilor sunt promise săptămâna2026.10.12–18. Planul este Musterplan, nu plan particular acceptat; compatibilitatea completă cu proiectul nu este confirmată. Nu există preț nou.','Verificarea planului-model, a sarcinilor și cotelor de proiect; solicitarea confirmării particularizate și a ofertei promise. Nu se presupune conformitatea numai din prospect.'),
'Sturm Energie':('2026.10.07: ticket365740/client42018142. Notificarea poștală a revenit cu mențiunea„unbekannt”; cere verificarea adresei Parkring2. Extrase2026.10.07: curentTop5/4000112571 restant27,12EUR; gazTop5/4000112572 restant109,99EUR; subtotal137,11EUR. Sunt facturi și solduri existente retransmise, nu datorii suplimentare de adăugat automat.27,12=149,53 factura41422 minuscredit122,41;109,99 factura29721 era deja în reconcilierea2026.09.30. Top17/client42017328 este distinct, fără sold nou în acest email. Somațiile retransmise au termene istorice2026.09.07 și2026.08.21. Plata/repartizarea între proprietari rămân neconfirmate.','Verificarea adresei de facturare, a debitelor și alocării sumelor; clarificarea conturilor și responsabilității. Nu se dublează facturile41422/29721 și nu se compensează credite ale altor instalații.')}
old_ids={e['id'] for e in COMM['comunicatii']}
for e in M['emails']:
    d=e['data'];partner=PARTNERS[e['id']];file_partner='STURM' if partner=='Sturm Energie' else 'Fuglister' if partner=='Füglister' else partner
    base='2026.10.08 PRIMIT '+file_partner+' '+e['id'][:8]
    src=(OUT/(base+'.txt')).relative_to(ROOT).as_posix()
    dt=datetime.datetime.fromisoformat(d['received_at'].replace('Z','+00:00'))
    date=dt.strftime('%Y.%m.%d')
    if e['id'] not in old_ids:
        COMM['comunicatii'].append({'data':date,'ora_utc':dt.strftime('%H:%M'),'partener':partner,'domeniu':'Utilități' if partner=='Sturm Energie' else 'Execuție și ofertare','sens':'PRIMIT','subiect':d['subject'],'expeditor':d['from_address'],'destinatari':', '.join(d['to']),'cc':', '.join(d.get('cc',[])),'id':e['id'],'cale':src,'atasamente':len(d['attachments']),'trunchiat':d.get('truncated',False)})
    status,nextstep=STAT[partner]
    entry=next((s for s in COMM['statusuri'] if s['partener']==partner),None)
    if entry is None:entry={'partener':partner,'mesaje':0};COMM['statusuri'].append(entry)
    entry.update({'status':status,'ultima_comunicare':date,'ultimul_primit':date,'subiect_ultimul_primit':d['subject'],'urmatorul_pas':nextstep,'sursa_status':[src],'nivel':'Sinteză verificată pe mesaj și originale','mesaje':int(entry.get('mesaje',0))+1})
    pattern='* Log discutii - '+partner+'.txt'
    previous=sorted((ARCH/'Parteneri').glob(pattern))
    old=previous[-1].read_text(encoding='utf-8-sig') if previous else ''
    log='2026.10.08 | Verificare zilnică\nStatus scurt: '+status+'\nUltimul răspuns: '+date+' | '+d['subject'].replace('\r','').replace('\n',' ')+'\nUrmătorul pas: '+nextstep+'\nSursa: '+src+'; ID '+e['id']+'\n\nISTORIC\n\n'+old
    (ARCH/'Parteneri'/('2026.10.08 Log discutii - '+partner+'.txt')).write_text(log,encoding='utf-8')
old_att={a['id'] for a in ATTS};newatt=[a for a in DL if a['stare']=='salvat original integral' and a['id'] not in old_att]
ATTS.extend(newatt)
cover=COMM['acoperire'];cover['mesaje_salvate']=len(COMM['comunicatii'])
cover['atasamente_salvate']+=len(newatt);cover['atasamente_identificate']+=len(newatt)
newpdf=sum(a['nume_original'].lower().endswith('.pdf') for a in newatt)
cover['atasamente_documentare']+=newpdf;cover['atasamente_documentare_salvate']+=newpdf
cover['mesaje_suplimentare_fata_de_lista']+=5
cover['verificare_incrementala']={'data':'2026.10.08','mesaje_noi':5,'originale_noi':len(newatt),'pdf_salvate':newpdf,'imagini_salvate':len(newatt)-newpdf,'office_sincronizat':'2026.10.08 08:00:04 România','cosmin_sincronizat':'2026.10.08 08:00:05 România','perioada':'2026.10.06–08','cautari_complete':len(M['searches']),'limita':'Rezultate accesibile Eva-Mail până la sincronizările consemnate; alte căsuțe pot avea sincronizări mai vechi. Export API, nu MIME integral.','recuperare_cosmin':'Căutări Schallergasse/2044001194/2616052 din2026.08.12: zero rezultate.'}
COMM['data_actualizarii']='2026.10.08'
COMM['actualizari_punctuale'].append({'data':'2026.10.08','subiect':'Schmitt răspunde negocierii; SCHAUERLEUTE solicită confirmare; Füglister/Weigl tehnic; STURM adresă și extrase','mesaje':5,'originale':24,'sursa':(OUT/'2026.10.08 Raport actualizari si fisiere.txt').relative_to(ROOT).as_posix()})
(ARCH/'2026.10.08 Registru comunicatii.json').write_text(json.dumps(COMM,ensure_ascii=False,indent=2),encoding='utf-8')
(ARCH/'2026.10.08 Registru atasamente.json').write_text(json.dumps(ATTS,ensure_ascii=False,indent=2),encoding='utf-8')
report='2026.10.08 | Noutăți față de verificarea2026.10.07\n\nCinci mesaje noi relevante primite.24/24 originale descărcate integral:15PDF și9imagini. Corpuri complete API pentru cele5mesaje; CCabsent în fiecare. Niciun email trimis, acord, semnare sau plată efectuată.\n\n'
for partner,(status,nextstep) in STAT.items():report+=partner+'\n'+status+'\nAcțiune: '+nextstep+'\n\n'
report+='FIȘIERE ORIGINALE DESCĂRCATE\n'
for a in DL:report+=a['partener']+' | '+a['nume_original']+' | '+str(a.get('octeti',0))+' octeți | '+a['cale']+'\n'
report+='\nACOPERIRE\n'+json.dumps(cover['verificare_incrementala'],ensure_ascii=False,indent=2)+'\nNu există răspuns nou TOMS sau DONAU în interval. Vizita țintăTOMS2026.10.08 nu este confirmată de un răspuns nou. Registrul bancar nu a fost actualizat prin această verificare; extrasele STURM sunt ale furnizorului, nu dovadă bancară de plată. XLSX/DOCX vechi ale jurnalelor reprezintă istoricul; TXT/JSON2026.10.08 sunt actuale.\n'
(OUT/'2026.10.08 Raport actualizari si fisiere.txt').write_text(report,encoding='utf-8')
for name in ['2026.10.08 Status proiect.txt','2026.10.08 Log progres proiect.txt']:
    predecessor=ROOT/name.replace('2026.10.08','2026.10.07')
    hist=predecessor.read_text(encoding='utf-8-sig') if predecessor.exists() else ''
    (ROOT/name).write_text(report+'\nISTORIC\n\n'+hist,encoding='utf-8')
readme=ROOT/'folder map/README.md';old=readme.read_text(encoding='utf-8-sig')
intro='''# 2026.10.08 — Cinci comunicări noi și 24 originale salvate

Puncte curente: ../2026.10.08 Status proiect.txt; ../2026.10.08 Log progres proiect.txt; registrele TXT/JSON2026.10.08 și dosarul ../08. Corespondenta/2026.10.08 Verificare zilnica/. Începe cu 2026.10.08 Raport actualizari si fisiere.txt. Schmitt răspunde negocierii, acceptă plățile și taxeTÜV, nu garanție6ani; service retransmis, modele nesemnate. SCHAUERLEUTE cere confirmarea vizitei2026.10.09 09:30Viena. Füglister șiWeigl transmit documentație, fărăprețnou. STURM cere corectarea/verificarea adresei și retransmite solduriTop5 total137,11EUR, deja cuprinse în poziții istorice; nu se dublează.15PDF și9imagini descărcate integral. TOMS/DONAU fără răspuns nou. Office și cosmin@ig.ro sincronizate2026.10.08 08:00România; alte conturi pot avea limite. Nicio trimitere, semnare sau plată. Istoricul juridic2026.10.07 rămâne valabil; copia PDF din05.Asigurari este duplicat identic, nu noutate externă.

'''
if not old.startswith('# 2026.10.08'):readme.write_text(intro+old,encoding='utf-8')
print(json.dumps({'mesaje_total':cover['mesaje_salvate'],'originale_total':cover['atasamente_salvate'],'documentare_total':cover['atasamente_documentare_salvate'],'cautari':len(M['searches']),'raport':str(OUT/'2026.10.08 Raport actualizari si fisiere.txt')},ensure_ascii=False))
