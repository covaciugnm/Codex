import json,pathlib,re,hashlib,datetime,html,collections
W=pathlib.Path(__file__).parent
R=pathlib.Path(r'Z:\00. Proiecte 2025\AFIR FotoVoltaic 1')
O=R/'outputs'/'registru-cesiro-2026-10-16';O.mkdir(parents=True,exist_ok=True)
E=json.loads((W/'emails_complete.json').read_text(encoding='utf-8'))
old=json.loads((R/'Comunicatii oficiale AFIR'/'export_eva.json').read_text(encoding='utf-8'))['emails']
E=list({e['id']:e for e in old+E}.values())
exclude={'756316b7-5b1c-4bae-8412-ebdbaeb6cadd','6f20d0d5-3296-450b-aef3-2ceac3e12ccd','a73e62e5-2bcc-460c-afeb-a763547819dc','bc8a0c9a-2240-42b5-8add-39ea60f7536d'}
E=[e for e in E if e['id'] not in exclude and 'Acte PT Alba' not in e['subject']]
E.sort(key=lambda e:e.get('received_at') or '')
L=json.loads((W/'local.json').read_text(encoding='utf-8'))
A=json.loads((W/'archives.json').read_text(encoding='utf-8'))
def clean(s):return re.sub(r'\s+',' ',s or '').strip()
def related(r):return not r['relative'].startswith(('50.','51.','52.','0. Arhiva','0.0 Documente Oficiale Ghid','Extrase echipamente','Justificare activitate','Audit Clarificare'))
def stage(p):
 if p.startswith(('4.','5.','3.')):return 'Depunere / eligibilitate'
 if p.startswith(('10.','11.')):return 'Contractare'
 if p.startswith('16.'):return 'Modificare contract'
 if p.startswith('30.'):return 'Rambursare tranșa 1'
 if p.startswith('20.'):return 'Racordare'
 if p.startswith('40.'):return 'Cofinanțare / bancă'
 if p.startswith('Comunicatii'):return 'Corespondență AFIR'
 return 'Implementare / documente suport'
def status(r):
 p=r['relative'].lower()
 if '2026-10-15 solicitare' in p and ('raspuns' in p or 'răspuns' in p):return 'Proiect răspuns; netransmis conform notei locale'
 if 'descarcate de pe afir' in p:return 'Copie din dosar etichetat descărcat de pe AFIR'
 if 'semnat si depus' in p:return 'Depus conform denumirii dosarului; recipisă neidentificată'
 if 'draft' in p or 'arhiva' in p or '\\word\\' in p or '\\editabile\\' in p:return 'Versiune de lucru / arhivă'
 if 'ce s-a trimis la tamas' in p:return 'Pachet pentru auditor; nu dovedește depunere AFIR'
 if 'de depus' in p:return 'Pregătit pentru depunere; confirmare de verificat'
 return 'Document local; transmiterea individuală neconfirmată'
S=O/'Surse email';S.mkdir(exist_ok=True)
emailrows=[];attachmentrows=[];sources={}; numbers=[]
for i,e in enumerate(E,1):
 eid='E'+str(i).zfill(3);e['regid']=eid
 path=S/(eid+'.txt');sources[e['id']]=str(path)
 path.write_text('Data UTC: '+str(e.get('received_at'))+'\nDe la: '+str(e.get('from_address'))+'\nCătre: '+', '.join(e.get('to') or [])+'\nCC: '+', '.join(e.get('cc') or [])+'\nSubiect: '+e['subject']+'\nID EVA: '+e['id']+'\n\n'+(e.get('text') or '')+'\n\nATAȘAMENTE\n'+'\n'.join(a['name'] for a in e.get('attachments',[])),encoding='utf-8')
 direct=bool(re.search('@afir\\.',e.get('from_address','')+' '+' '.join(e.get('to') or []),re.I))
 emailrows.append([eid,e.get('received_at',''), 'Trimis' if e.get('is_sent') else 'Primit','AFIR direct' if direct else 'Corespondență conexă',e['subject'],e.get('from_address',''),'; '.join(e.get('to') or []),'; '.join(e.get('cc') or []),len(e.get('attachments',[])),clean(e.get('text',''))[:1100],e.get('account_email',''),e['id'],str(path),'Metadatele EVA pot conține duplicate de sincronizare.'])
 for j,a in enumerate(e.get('attachments',[]),1):
  ap=S/(eid+'-A'+str(j).zfill(2)+'.txt');ap.write_text('Nume: '+a['name']+'\nID: '+str(a.get('id'))+'\nEmail: '+eid+'\n\n'+(a.get('text') or '[Fără text extras disponibil]'),encoding='utf-8')
  sources[a.get('id','')]=str(ap)
  t=a.get('text') or ''; h=hashlib.sha256(t.encode()).hexdigest() if t else ''
  attachmentrows.append([eid+'-A'+str(j).zfill(2),eid,a['name'],a.get('size'),a.get('id',''),'Text extras disponibil' if t else 'Original necitit / fără text',str(ap),h])
(O/'Surse email'/'export_eva_registru.json').write_text(json.dumps(E,ensure_ascii=False),encoding='utf-8')
# Registrul evenimentelor și al perechilor de numere, verificat din documente.
main=[]
def add(title,issuer,bn='',bd='',an='',ad='',code='',when='',state='',src='',note=''):
 main.append(['R'+str(len(main)+1).zfill(3),title,issuer,bn,bd,an,ad,code,when,state,sources.get(src,src),note])
add('Notificare selectare cerere de finanțare E6.8.3','AFIR','','','1263007','2024-12-09','FMSES011011372801030','2024-12-10','Primit de la AFIR','99c889d9-f766-4d7c-9200-6b06c0f2d28f')
add('Contract de finanțare și anexele I–IV','AFIR / Cesiro','','','','','CFMSES011011372801030','2024-12-30','Contract transmis de AFIR; copie semnată în proiect','fed1cb54-b25b-420f-bb58-b5650d05f782','Data contractului 30.12.2024 este confirmată în actele adiționale. Codul nu este număr intern Cesiro.')
add('Transmitere / clarificări studiu de fezabilitate','Cesiro','','','','','','2025-02-28','Email trimis; încărcarea SF în platformă neconfirmată','1df0ce9b-cbaf-401e-b3f3-da0e8b07325a')
add('Transmitere ATR Prosumator și confirmare primire','Cesiro / AFIR','','','','','','2025-05-23','Primire confirmată în firul email','25a0d2a0-53a6-4fdc-869b-66c6e0266ab2')
add('Notificare schimbare acționariat și act de identitate','Cesiro','','2026-01-15','','','','2026-01-15','Trimis prin email; retransmis 19.01.2026','ee9eb7ce-2d59-4586-92a2-0fc116c8164d','Număr propriu neidentificat în notificare.')
add('Solicitare avizare actualizare tehnică','Cesiro','','','','','CFMSES011011372801030','2026-02-19','Documentație transmisă prin email','d66689ce-f055-433c-8d2e-2647b694f5e6')
add('Notificare privind diminuarea valorii contractului','AFIR','','','R1 SIBA SE 242','2026-03-24','','2026-03-24','Primit de la AFIR','b5216659-eb77-4ff7-88f1-859c10b41699')
add('Notă explicativă – schimbarea structurii acționariatului','Cesiro','FN','2026-04-21','R1-SIBA-SE-450','2026-04-27','','','Depunere confirmată prin nota AFIR C3.2.2','9b2ecb07-cfde-4cb3-91f3-6fb1db663a18','FN = fără număr; identificator citat de AFIR.')
add('Solicitare informații suplimentare – acționariat','AFIR','','','1353061','','','2026-04-28','Primit de la AFIR','4103514e-e610-427f-9ed1-f5b72fa123a6','Data numărului de înregistrare nu apare în text; data emailului este separată.')
add('Răspuns Partea II – completări ONRC','Cesiro','17','2026-05-08','','','','2026-05-08','Atașament transmis către AFIR','3accd584-4909-40fe-8664-14421947d6b0','Există retransmiteri / duplicate în mai 2026. Nu reprezintă depuneri distincte demonstrate.')
add('Notă aprobare schimbare acționariat C3.2.2','AFIR','','','1353060','','','2026-05-08','Aprobare primită','9b2ecb07-cfde-4cb3-91f3-6fb1db663a18','Data înregistrării nu este explicită în antet.')
add('Notă explicativă și memoriu – actualizare tehnică','Cesiro','FN','2026-06-11','R1 SE-SIBA 575','2026-06-11','','','Depunere citată în notificarea de rectificare','1d465e35-e575-46cf-8277-011023da7249')
add('Act adițional nr. 1 la contractul de finanțare','AFIR / Cesiro','','','1.360.244','2026-06-30','AA1 / CFMSES011011372801030','2026-06-30','Semnare menționată în notificarea beneficiarului','1d465e35-e575-46cf-8277-011023da7249')
add('Adresă de înaintare și notificare rectificare panouri','Cesiro','','','','','','2026-07-09','Transmis AFIR; redirecționat secretariatului 10.07.2026','f94f48f2-6fa9-48f2-ad98-0c82c2f5272a','Numărul 1.360.244 din subiect se referă la AA1, nu la adresa de înaintare.')
add('Notă explicativă / memoriu pentru rectificare tehnică','Cesiro','FN','2026-07-13','671','2026-07-14','','','Depunere confirmată în notificarea AFIR C3.3.8','b6b36f4e-9064-4794-b1c6-ee59492c8c4c')
add('Completări pentru actul adițional tehnic solicitat','Cesiro','','','','','','2026-07-24','Email către Stelian Popa cu 3 atașamente','31cb3eb8-3d10-4595-b3da-501b14b829c3')
add('Notificare neacceptare modificare tehnică C3.3.8','AFIR','','','1.370.394','','','2026-08-07','Neacceptat','b6b36f4e-9064-4794-b1c6-ee59492c8c4c','Distinctă de AA2 pentru prelungire, acceptat în octombrie.')
add('Raport audit financiar','ATTA Consulting','','','','','206/12.08.2026','2026-08-12','Primit de la auditor','26a69bca-54ff-43ec-81bc-b359d48b079b','Număr al auditorului, nu număr Cesiro sau AFIR.')
add('Acceptare grafic de eșalonare','AFIR','','','','','','2026-08-13','Grafic acceptat prin email','c4596d80-b7d9-4b3b-a3bc-2ccf93c5de08','Fără număr de adresă în corpul mesajului.')
add('Memoriu justificativ – prelungire termen','Cesiro','145','2026-08-18','R1-SIBA-SE-765','2026-08-19','','','Depunere confirmată de AFIR','c5b271c2-8812-4079-bb02-efe267fe73e9','În AA2 apare și forma R1-SIBA-765; scrisoarea 1382394 folosește R1-SIBA-SE-765.')
add('Notă explicativă – prelungire termen','Cesiro','FN','2026-08-19','R1-SIBA-765','2026-08-19','','','Depunere confirmată de AFIR în AA2','c5b271c2-8812-4079-bb02-efe267fe73e9')
add('Cerere de rambursare – tranșa 1','Cesiro','','','','','RFMSES011011372801030.1','2026-08-25','Data depunerii confirmată în email AFIR 15.10.2026','496ab41f-9db6-4d34-b344-88cc4b531ce9','Codul dosarului este separat de numerele de corespondență.')
add('Notă convocare pentru vizita din 08.09.2026','AFIR','','','815','2026-09-07','','2026-09-07','Primit de la AFIR','08e8424c-8963-4a74-8c05-a08980a1aedb')
add('Solicitare informații suplimentare – tranșa 1','AFIR','','','816','2026-09-07','','','Existență și dată confirmate în solicitarea 961','3127d7c3-961e-4811-a7f5-98d9e16aac15','AFIR confirmă că a primit un răspuns la 816; data acelui răspuns trebuie stabilită din dovada de încărcare.')
add('Raport de analiză prelungire','AFIR','','','1376937','2026-09-21','','','Referință în AA2; original separat neidentificat','c5b271c2-8812-4079-bb02-efe267fe73e9')
add('Solicitare clarificări privind prelungirea','AFIR','','','1382394','2026-09-29','','2026-09-29','Primit de la AFIR','866c6edb-b62b-49ce-b286-ac964c402d04','Data este confirmată explicit prin referința din AA2.')
add('Confirmare primire și întrebare privind termenul de 8 luni','Cesiro','','','','','','2026-09-29','Email trimis; răspuns AFIR în aceeași zi','b97dfaf3-e09b-4387-bcdd-b739f23acafe')
add('Memoriu justificativ revizuit – răspuns clarificări','Cesiro','161','2026-09-30','R1-SIBA-SE-915','2026-09-30','','','Depunere confirmată de AFIR în AA2','c5b271c2-8812-4079-bb02-efe267fe73e9')
add('Notă explicativă revizuită – răspuns clarificări','Cesiro','FN','2026-09-30','R1-SIBA-SE-915','2026-09-30','','','Depunere confirmată de AFIR în AA2','c5b271c2-8812-4079-bb02-efe267fe73e9')
add('Raport de analiză – completare','AFIR','','','R1-SIBA-SE-919','2026-10-01','','','Referință în AA2; original separat neidentificat','c5b271c2-8812-4079-bb02-efe267fe73e9')
add('Act adițional nr. 2 – prelungire termen','AFIR / Cesiro','','','1379871','','AA2 / CFMSES011011372801030','2026-10-09','Acceptare comunicată; semnarea bilaterală de verificat','c5b271c2-8812-4079-bb02-efe267fe73e9','Data AA2 este necompletată în antet. Nu se confundă cu data emailului 09.10.2026.')
add('Solicitare informații suplimentare – registru-jurnal și 30 panouri','AFIR','','','961','2026-10-15','','2026-10-15','Primit de la AFIR','3127d7c3-961e-4811-a7f5-98d9e16aac15')
add('Proiect răspuns la solicitarea AFIR 961','Cesiro','','','','','','','Pregătit local; netransmis conform notei locale',str(R/'Comunicatii oficiale AFIR'/'2026-10-15 Solicitare 961 - transa 1'/'Citeste_inainte_de_depunere.txt'),'Numărul intern este încă de completat. Nu se preia 961 ca număr Cesiro.')
add('Contract achiziție / furnizare Cesiro – Suntree','Cesiro / Suntree','05','2024-02-01','','','275/01.02.2024','','Contract citat în notificarea semnată a beneficiarului','1d465e35-e575-46cf-8277-011023da7249','05 este numărul de înregistrare Cesiro; 275 este numărul contractului, nu număr AFIR.')
add('Act adițional nr. 1 la contractul Cesiro – Suntree','Cesiro / Suntree','','','','','AA1 / 275','2025-12-30','Copie semnată transmisă AFIR 24.07.2026','87aa35a0-4fbe-432d-ae34-e3d949efa5c9','Data încheierii actului: 30.12.2025. Nu se confundă cu AA1 la finanțare.')
add('Contract audit financiar ATTA – Cesiro','ATTA / Cesiro','','','','','186/15.07.2026','2026-07-15','Copie contract în corespondența cu auditorul','342299d9-e9d1-4a04-aa8f-1e58c335c271','Număr contractual al prestatorului; număr de registratură Cesiro neidentificat.')
add('Răspuns clarificări tranșa 1 – formular AP 1.13','Cesiro','123','2026-09-09','','','RFMSES011011372801030.1','','Formular local completat; răspunsul la 816 este confirmat de AFIR în 961',str(R/'30.1 Cerere Rambursare 1'/'Clarificare nr.1'/'AP_raspuns_informatii_suplimentare_-.pdf'),'Verificat vizual p. 1. În câmpul solicitării figurează nr. 1 / 09.09.2026, diferit de referința AFIR 816/07.09.2026; de reconciliat cu exemplarul depus.')
add('Solicitare informații suplimentare F3.4 – evaluare inițială','AFIR','','','1193319','','FFMSES011011372801030','','Document AFIR păstrat local',str(R/'4. Cerere de finantare'/'F3.4_CRFIR-ALBA-IULIA.pdf'),'Semnătură vizibilă datată 18.04.2024; nu este atribuită automat datei de înregistrare.')
add('Răspuns Partea II la clarificări evaluare inițială','Cesiro','','2024-04-25','','','','','Document semnat local; data depunerii de verificat',str(R/'4. Cerere de finantare'/'0. Raspuns Partea a 2-a Cesiro Production SRL 25.04.2024 semnat.pdf'),'Include cererea revizuită, planul de afaceri, documentele de eligibilitate și dosarul achiziției. Fără număr propriu vizibil.')
add('Raport de analiză – modificări tehnice AA1','AFIR','','','1.359.705','2026-06-22','','','Referință explicită în AA1',str(R/'16.1 Act aditional 1'/'Act de semnat AFIR'/'Act Aditional Semnat'/'C3.3.4_.pdf'))
add('Notă corectare eroare materială denumire structură','Cesiro','122','2026-09-08','','','','','Inclusă în formularul de răspuns 123',str(R/'30.1 Cerere Rambursare 1'/'Clarificare nr.1'/'4, Nota_eroare_materiala_pct4_Skybase.pdf'))
for r in main:
 if r[1]=='Cerere de rambursare – tranșa 1':
  r[3]='1';r[4]='2026-08-12';r[11]+=' Număr/data beneficiar: 1/12.08.2026, în formularul AP 1.1 SE v2 și nota explicativă revizuită.'
add('Declarație proprie răspundere – prelungire revizuită','Cesiro','160','2026-09-30','','','','','Document în pachetul local de răspuns clarificări',str(R/'16.3 Act aditional 2 - Prelungire termen'/'Clarificare nr1'/'5_Declaratie_proprie_raspundere_ss_.pdf'),'Versiunile de lucru poartă și nr. 150; păstrate separat în inventar.')
add('Decizie asumare traduceri și certificate','Cesiro','121','2026-09-08','','','','','Document în pachetul de clarificări tranșa 1',str(R/'30.1 Cerere Rambursare 1'/'Clarificare nr.1'/'3.2 Decizie_121_08092026_rev3_.pdf'))
main.sort(key=lambda r:r[8] or r[6] or r[4] or '9999')
for i,r in enumerate(main,1):r[0]='R'+str(i).zfill(3)
# Toate fișierele se păstrează în inventar; documentele suport și versiunile sunt diferențiate.
inv=[];docs=[];seen={}
for i,r in enumerate(L,1):
 rid='F'+str(i).zfill(4);r['rid']=rid;h=r.get('hash','');dup=seen.get(h,'') if h else ''
 if h and not dup:seen[h]=rid
 scope='Proiect fotovoltaic' if related(r) else 'Context / alte investiții / ghid / audit intern'
 inv.append([rid,r['name'],r['relative'].split('\\')[0],scope,r['ext'],r['size'],r['read'],status(r),dup,r['path']])
 if not related(r) or r['ext'] not in {'.pdf','.docx','.doc','.xlsx','.xls','.zip','.eml','.msg'}:continue
 if r['relative'].startswith('Comunicatii oficiale AFIR\\Emailuri'):continue
 if dup:continue
 t=r['text']; chunks=[]
 for m in re.finditer(r'(?i)(?:num[ăa]r(?:ul)?\s+de\s+[îi]nregistrare|nr\.?\s+(?:de\s+)?[îi]nregistrare|nr\.?|\bFN\s*/|\bR1\s*[- ])[^\n]{0,160}',t):
  x=clean(m.group());
  if re.search(r'\d',x) and not re.search(r'(?i)(cadastr|telefon|jude|strad|registrul comer|cod unic)',x):chunks.append(x)
 chunks=list(dict.fromkeys(chunks))[:20]
 own='';od='';af='';ad='';other=''
 isafir=bool(re.search(r'(C3\.3\.|C3\.2\.|Fisa de informatii suplimentare partea I|F3\.4|Informatii suplimentare - Partea I|AP_1\.11|NotificareSolicitant)',r['name'],re.I))
 head=t[:2200]
 m=re.search(r'(?i)(?:Num[ăa]r de [îi]nregistrare\s*(?:electronic)?|Nr\.?\s*(?:de\s+)?[îi]nregistrare(?:\s+beneficiar)?)\s*:\s*([\w .-]+?)(?:\s*/\s*(\d{1,2}\s*\.\s*\d{1,2}\s*\.\s*\d{4}))?(?=\n|$)',head)
 if m:
  val=clean(m.group(1));dt=clean(m.group(2)) if m.group(2) else ''
  if re.search(r'\d',val):
   if isafir:af,ad=val,dt
   elif 'beneficiar' in m.group().lower():own,od=val,dt
   else:other=val+(' / '+dt if dt else '')
 direct=re.search(r'(?im)^\s*(?:Nr\.?|Num[ăa]r)\s*[:.]?\s*(\d+|FN)\s*/\s*(\d{1,2}\.\d{1,2}\.\d{4})',t[:1500])
 if direct and not own and not af:
  if isafir:af,ad=direct.group(1),direct.group(2)
  elif re.search(r'CESIRO\s+PRODUCTION',t[:600],re.I) and not re.search(r'AFIR -|CONSULTING|SOLAR TECH|ONRC',t[:200],re.I):own,od=direct.group(1),direct.group(2)
  else:other=direct.group(1)+' / '+direct.group(2)
 # Nu atribuim registraturii Cesiro numărul unui contract citat sau al băncii.
 if own and (own in {'275','282','250012'} or r['name'].startswith('Referat')):other=own+' / '+od;own=od=''
 if direct and re.search(r'(?i)(Memoriu_justificativ_prelungire|Declaratie_proprie_raspundere|Solicitare oferta|Nota justificativa alegere furnizor)',r['name']):own,od=direct.group(1),direct.group(2);other=''
 if r['relative']=='30.1 Cerere Rambursare 1\\Clarificare nr.1\\AP_raspuns_informatii_suplimentare_-.pdf':own,od='123','09.09.2026'
 if r['name']=='3.2 Decizie_121_08092026_rev3_.pdf':own,od='121','08.09.2026'
 if r['name']=='Contract Suntree Solar Tech SRL - Cesiro Production SRL.docx':own,od,other='05','01.02.2024','Suntree 275 / 01.02.2024'
 if r['name']=='AP 1.1 SE Cerere de rambursare-v2.pdf':own,od='1','12.08.2026'
 if not t or 'Please wait...' in t[:100]:quality='Necesită citire vizuală / OCR / formular XFA'
 else:quality='Text extras; numerele din referințe sunt în coloana separată'
 docs.append([rid,r['name'],stage(r['relative']),own,od,af,ad,other,status(r),'\n'.join(chunks),quality,r['path']])
payload={'main':main,'emails':emailrows,'attachments':attachmentrows,'inventory':inv,'documents':docs,'archives':[[a['archive'],a['entry'],a['size']] for a in A if not a['archive'].startswith(('50.','51.','52.')) and not any(x in a['entry'].lower() for x in ['intrare cont','thumbs.db','~$'])],'out':str(O)}
(W/'data.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:len(v) for k,v in payload.items() if isinstance(v,list)},ensure_ascii=False))
