from pathlib import Path
import json, hashlib, shutil, html, re
R=Path(__file__).resolve().parent.parent
O=R/'06. Utilitati/UTILITATI Curent - Sturm Energie/2026.10.14 Situatie STURM'
E=O/'Surse'; E.mkdir(exist_ok=True)
inv=json.loads((R/'folder map/inventar.json').read_text('utf-8-sig')); ix={x['cale']:x for x in inv}
live=json.loads((O/'2026.10.14 Dovezi Eva-Mail.json').read_text('utf-8'))
sources={}; checks=[]
def check(p):
 rel=p.relative_to(R).as_posix(); old=ix.get(rel); h=hashlib.sha256(p.read_bytes()).hexdigest()
 checks.append({'cale':rel,'sha256':h,'identic_index':h==old['sha256'] if old else None})
 return h
for p in (R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri').rglob('*.txt'):
 if p.parent.name not in ['Sturm Energie','CERHA HEMPEL']:continue
 t=p.read_text('utf-8-sig')
 if 'sturm' not in t.lower():continue
 j=p.with_suffix('.json')
 if not j.exists():continue
 d=json.loads(j.read_text('utf-8-sig')); check(p);check(j)
 d['text']=t;d['sursa_locala']=p.relative_to(R).as_posix();sources[d['id']]=d
for d in live['emailuri']:
 d['data_lizibila']=(d.get('received_at') or '')[:10].replace('-','.')
 d['statut']='TRIMIS' if d.get('is_sent') else 'PRIMIT'
 sources[d['id']]=d
for d in sources.values():
 date=(d.get('received_at') or '')[:10].replace('-','.')
 stem=f"{date} {d['id'][:8]}"
 (E/(stem+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
 meta=f"Data lizibila: {date}\nStatut: {'TRIMIS' if d.get('is_sent') else 'PRIMIT'}\nSubiect: {d.get('subject')}\nExpeditor: {d.get('from_address')}\nDestinatari: {', '.join(d.get('to') or [])}\nCC: {', '.join(d.get('cc') or [])}\nID Eva-Mail: {d['id']}\nLimita corp API: {d.get('truncated',False)}\n\nTEXT ORIGINAL DISPONIBIL\n"
 (E/(stem+'.txt')).write_text(meta+d.get('text',''),'utf-8')
 d['export']=str((E/(stem+'.txt')).relative_to(O)).replace('\\','/')
# Originalele relevante sunt reutilizate, cu hash si calea explicita; nu duplicam arhiva.
pdf=[]
for e in inv:
 p=R/e['cale'];s=e['cale'].lower()
 if e['extensie'].lower()!='.pdf':continue
 if (s.startswith('06. utilitati/utilitati curent - sturm energie/') or ('2026.10.14 verificare zilnica' in s and 'original' in s and 'm_4000' in s) or 'schreiben von sturm' in s or ('2026.10.08 verificare zilnica' in s and any(k in s for k in ['kontoauszug_400011257','r_d_400011257','m_400011257','em_400011257'])) or '20260402153949876.pdf' in s):
  check(p);pdf.append({'cale':e['cale'],'sha256':checks[-1]['sha256'],'stare':'original salvat pe disc; reutilizat'})
(O/'2026.10.14 Registru surse si verificare index.json').write_text(json.dumps({'emailuri':[{k:d.get(k) for k in ['id','received_at','subject','from_address','to','cc','is_sent','export','truncated']} for d in sources.values()],'originale':pdf,'verificari':checks},ensure_ascii=False,indent=2),'utf-8')
# O linie reprezinta un schimb distinct; copiile intre casute raman in registrul de surse.
rows=[
('2026.03.25','Capra → noi','Contractul vechi de curent','Spune că furnizarea încă există și costurile până la sfârșitul contractului sunt ale vânzătorului.','Repartizarea costurilor rămâne deschisă; afirmație Capra, nu acceptare STURM.','7541c7a4'),
('2026.03.25','Noi → Capra; Capra → noi','Gaz și situația utilităților','Întrebăm despre gaz; Capra spune că probabil este decuplat și va verifica.','Informație probabilă atunci; lista STURM ulterioară confirmă încetarea furnizării.','4d4ae41f,1b461e74'),
('2026.03.25','STURM → Capra → noi','Oferta #323971','Tarif fix fără durată minimă, preaviz 14 zile; urma formular de semnat după confirmarea adresei.','OFERTĂ NEACCEPTATĂ. STURM confirmă ulterior lipsa răspunsului.','c49b8bb4'),
('2026.03.30','Capra → noi','Adresa societății','Anunță că va actualiza sediul la Schallergasse 35.','Nu dovedește că STURM a actualizat adresa de corespondență.','e7654d1a'),
('2026.04.07','Capra / Hofhans → noi','Reziliere și avertizare Wiener Netze','Capra anunță rezilierea; transmite avertizarea privind lipsa contractului și deconectarea.','Contractul vechi încetat; furnizorul actual se verifică separat la Wiener Netze.','f0c95518'),
('2026.05.27','Hofhans → STURM, prin Capra','Oprirea debitărilor și rambursărilor','Hofhans cere să nu îi mai fie debitat contul și să nu primească creditele; cere repartizare între proprietari.','Oprirea confirmată ulterior; repartizarea banilor rămâne deschisă.','bdbfaefe'),
('2026.05.27','Noi → STURM','Cerere situație completă #339194','Cerem contracte, conturi, deconturi, credite și blocarea operațiunilor spre Hofhans.','TRIMIS. Răspunsuri parțiale la 2026.06.01 și 2026.06.17.','1c657f52'),
('2026.05.27','STURM → noi','Confirmare automată #339194','Confirmă primirea cererii.','Confirmare de primire; nu soluționare.','d0076efb'),
('2026.06.01','STURM → noi','Contracte reziliate; ofertă fără răspuns','Confirmă rezilierea vechilor contracte și oprirea debitărilor/rambursărilor; întreabă cine primește facturile.','Încetarea confirmată; deconturile și titularul sumelor rămân de clarificat.','46501cec'),
('2026.06.08','Noi → STURM','Obiecții și documente #339194','Trimitem extras CF; cerem contracte, date de încetare, deconturi, statut și justificarea pretențiilor.','TRIMIS. Nu acceptăm prin acest mesaj datoriile vechi; nu comandăm furnizare.','4041dc7c'),
('2026.06.08','STURM → noi','Revenire la cererea de date','Solicită răspuns la mesajul din 2026.06.01.','Ulterior răspunde detaliat la 2026.06.17.','1337c803'),
('2026.06.08','Capra → STURM, copie noi','Destinatar facturi / credit','Precizează că CERHA nu este destinatarul facturării; noul proprietar este A&C. Consideră că un credit ar trebui să îi revină.','Beneficiarul creditelor nu este confirmat prin decont STURM.','27bf0629'),
('2026.06.17','STURM → noi','Răspuns complet #339194 și lista instalațiilor','Lista din 2026.06.16: 21 instalații cu furnizare încheiată. Datele bancare Hofhans eliminate; deconturi finale încă în curs atunci.','Contracte vechi închise; situația financiară nu este închisă.','f51d3f00'),
('2026.07.02','Capra → noi','Somații STURM','Transmite notificările de plată primite poștal.','Poziții istorice de reconciliat, nu de adunat la retransmiteri.','3f78b8ef'),
('2026.07.21','Capra → noi','Facturi de curent pentru cele două conturi','Transmite facturi; anunță că va cere STURM să nu mai trimită corespondența la CERHA.','Reconcilierea anterioară: 1.817,73 EUR în 9 facturi, fără debit identificat atunci. Suprapuneri cu somațiile ulterioare.','59ee9c56'),
('2026.08.04','Capra → noi','Facturi gaz / adresă','Transmite facturile de gaz și insistă asupra actualizării adresei.','Repartizarea între proprietari și adresa rămân deschise.','2bc1fedd'),
('2026.08.17','Capra → noi','Noi notificări STURM','Transmite documente pentru conturile 42017328 și 42018142.','Facturi/somații istorice; nu reprezintă contracte noi.','de89fdf0,07c2bfe4'),
('2026.08.19','STURM → noi','Somații #357112 / 42017328','Retrimite opt somații de gaz după retur poștal pentru adresă insuficientă.','Plata/alocarea și adresa rămân de verificat; gaz Top 15 plătit personal conform auditului anterior.','4fa309a0'),
('2026.08.26','STURM → noi','Top 5 gaz #358681','Retrimite factura 29721 și somația: 109,99 EUR.','Reluată în extrasul din 2026.10.07; nu se dublează.','f7bf25c4'),
('2026.09.17','Capra → noi; noi → Capra','Retransmitere documente istorice','Capra indică documentele STURM din martie/aprilie; noi spunem că am cerut comunicarea directă.','Fără contract nou și fără confirmare de sold zero.','b8bab41b,1fd0bddf'),
('2026.09.17','Capra → noi','Confirmare informală','Răspunde cordial mesajului de mulțumire; nu adaugă soluție STURM.','Informativ, fără modificarea situației contractuale sau financiare.','6b370ac8'),
('2026.10.01','Capra → noi','Scrisori STURM din 2026.09.24','Top 5 curent: 27,12 EUR; Top 17 curent: 432,66 EUR; termen 2026.10.07.','Termen depășit; fără încasare confirmată. Top 5 se repetă în mesajul din 2026.10.07.','ee452cda'),
('2026.10.07','STURM → noi','Cont 42018142 / #365740','Retur poștal «necunoscut» la Parkring 2; extrase Top 5: curent 27,12 EUR + gaz 109,99 EUR.','137,11 EUR pretinși; confirmarea plăților și corectarea adresei sunt deschise.','97799dc8'),
('2026.10.13','STURM → noi','Fost cont 42017328 / #365759','14 somații retrimise: 2.662,60 EUR, incluzând 98 EUR taxe. Cere plata sau dovezile de plată până la 2026.10.19.','DESCHIS. Reconciliere pe instalație; nu sunt 14 datorii noi de adăugat totalurilor vechi.','0fed52e8')]
def refs(prefixes):
 out=[]
 for pref in prefixes.split(','):
  d=next((d for k,d in sources.items() if k.startswith(pref)),None)
  if d:out.append(f'<a href="{html.escape(d["export"])}">{html.escape(d["id"][:8])}</a>')
 return ' · '.join(out)
summary='La 2026.10.14 nu este identificat niciun contract STURM nou sau activ pentru clădire. Lista STURM din 2026.06.16 confirmă furnizarea încheiată pentru toate cele 21 de instalații: 12 de curent și 9 de gaz. Trei au data de sfârșit 2026.03.18; celelalte 18 au 2026.04.08. Rămân deschise deconturile, alocarea plăților/creditelor și adresa de corespondență.'
issues=[('42017328 — 14 instalații','2.662,60 EUR','Somații retrimise 2026.10.13; termen 2026.10.19. Include 98 EUR taxe. Verificarea fiecărei plăți și a perioadei datorate.'),('42018142 — Top 5','137,11 EUR','27,12 EUR curent + 109,99 EUR gaz conform extraselor 2026.10.07. Nu se adaugă din nou 27,12 EUR din scrisoarea 2026.09.24.'),('42017328 — Top 17 curent','432,66 EUR','Instalația 4000114087, distinctă de cele 14; scrisoare 2026.09.24, termen 2026.10.07. Sunt cerute facturile 50457/49328/49327 plus taxa de 7 EUR.'),('Credit curent casa scării','846,92 EUR','Instalația 4000108283 / factura 29707. Nu există aici încasare ori compensare confirmată; anunțul automat din factură trebuie citit împreună cu oprirea rambursărilor confirmată de STURM.'),('Plata gaz Top 15','115,36 EUR','Auditul 2026.09.30 identifică plata personală din 2026.08.06 pentru factura 29700. Nu se plătește din nou fără verificarea alocării STURM.'),('Răspunderea între proprietari','De clarificat','Capra afirmă la 2026.03.25 că vânzătorul suportă energia până la finalul contractului. STURM nu confirmă o repartizare; facturile includ perioade anterioare achiziției și vechiul UID.'),('Adresă și conturi','Deschis','Parkring 2 produce retururi poștale. Eliminarea IBAN Hofhans a fost confirmată la 2026.06.17; actualizarea adresei nu este confirmată.'),('Furnizorul actual','Neconfirmat aici','STURM recomandă Wiener Netze pentru statutul actual al fiecărui punct de consum. Încetarea STURM nu confirmă deconectarea fizică sau un contract la alt furnizor.')]
css='body{font:16px/1.45 Segoe UI,Arial;color:#183047;background:#f5f7fa;margin:32px}main{max-width:1500px;margin:auto;background:white;padding:30px}h1{font-size:30px}h2{margin-top:36px}table{border-collapse:collapse;width:100%;margin:18px 0}th{background:#173d59;color:white;text-align:left}td,th{padding:12px;border:1px solid #d9e1e7;vertical-align:top}tr:nth-child(even){background:#f1f5f8}a{color:#12679a}small{color:#516371}.note{background:#fff4d9;padding:18px}td:first-child{white-space:nowrap}@media print{body{margin:0}main{padding:0}thead{display:table-header}tr{break-inside:avoid}}'
body=f'<!doctype html><html lang="ro"><meta charset="utf-8"><title>2026.10.14 STURM — conversații și contracte</title><style>{css}</style><main><h1>STURM Energie — conversații și situație</h1><p>Schallergasse 35 · Verificare 2026.10.14</p><p><strong>{summary}</strong></p><p>Oferta 2026.03.25 nu a fost acceptată, conform STURM la 2026.06.01 și 2026.06.17. Cont de client cu sold deschis nu înseamnă contract de furnizare activ.</p><h2>Probleme deschise</h2><table><thead><tr><th>Problemă</th><th>Sumă / stare</th><th>Ce rămâne de făcut</th></tr></thead><tbody>'
for row in issues:body+='<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in row)+'</tr>'
body+='</tbody></table><p class="note">Sumele sunt pretenții documentate ale STURM, nu un sold net acceptat sau reconciliat la zi. Nu adunați totalurile istorice cu retransmiterile și nu scădeți automat creditele. Nu s-a efectuat o plată și nu s-a trimis vreun mesaj în această verificare.</p><h2>Toate schimburile relevante identificate</h2><p>24 de rânduri cronologice; răspunsurile din aceeași zi și copiile între căsuțe sunt grupate unde tratează aceeași temă. Mesajele originale disponibile și metadatele sunt păstrate în Surse.</p><table><thead><tr><th>Data</th><th>Participanți</th><th>Subiect</th><th>Conținut / rezultat</th><th>Situație actuală</th><th>Surse Eva-Mail</th></tr></thead><tbody>'
for row in rows:body+='<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in row[:5])+'<td>'+refs(row[5])+'</td></tr>'
body+='</tbody></table><h2>Lista celor 21 de instalații</h2><p>Original verificat vizual; toate au statutul „beendete Belieferung”.</p><a href="../Anlagenliste_Schallergasse_35_16.06.2026.pdf">Deschide lista originală STURM</a><img style="width:100%;height:auto" src="2026.10.14 Verificare lista instalatii.png"><h2>Originale și limite</h2><p>Verificare punctuală în Eva-Mail: căutări STURM, sturmenergie și cele două numere de client, fără pagini restante la aceste căutări; completare din arhiva locală. Ultimul răspuns direct identificat: 2026.10.13. Office sincronizat 2026.10.14 13:44 România; Gmail 10:55, dar căutarea EVA în contul Gmail a returnat zero și corespondența sa este completată din arhivă și copiile EVA. Alte căsuțe pot fi întârziate; căsuțele shared/team nesearchable nu sunt acoperite. Nu se afirmă exhaustivitate în afara mesajelor accesibile. Unele corpuri sunt trunchiate de API, marcate în exporturi; acestea nu sunt copii MIME integrale.</p><p>Auditul plăților reutilizat este din 2026.09.30, cu extrase generale până la 2026.09.28; nu dovedește lipsa plăților ulterioare. Nu se trage o concluzie juridică definitivă asupra obligației cumpărătorului.</p><ul>'
for p in pdf:
 rel=Path(__import__('os').path.relpath(R/p['cale'],O)).as_posix();body+=f'<li><a href="{html.escape(rel)}">{html.escape(p["cale"])}</a></li>'
body+='</ul></main></html>'
(O/'2026.10.14 Tabel conversatii si contracte STURM.html').write_text(body,'utf-8')
txt=summary+'\n\nPROBLEME DESCHISE\n'+'\n'.join(' | '.join(r) for r in issues)+'\n\nCONVERSATII\n'+'\n\n'.join(' | '.join(r) for r in rows)
(O/'2026.10.14 Situatie STURM.txt').write_text(txt,'utf-8')
entry='2026.10.14 — STURM: conversații, contracte și probleme deschise\n\nStatus scurt: '+summary+'\nUltimul răspuns: 2026.10.13, ID 0fed52e8-a06b-47c5-ba04-84e5eb934d9f; 14 somații 2.662,60 EUR, termen 2026.10.19. Top 5 137,11 EUR și Top 17 curent 432,66 EUR sunt distincte, fără sold reconciliat actual.\nUrmătorul pas: decont actual pe instalație, alocarea plăților/creditului 846,92 EUR, repartizare între proprietari și corectarea adresei. Nicio trimitere/plată/acceptare nouă.\nSursă: '+O.relative_to(R).as_posix()+'/2026.10.14 Tabel conversatii si contracte STURM.html; lista originală STURM din 2026.06.16, verificată vizual și prin hash; mesaje originale în Surse.\n\n'
hist=O/'Istoric';hist.mkdir(exist_ok=True)
for rel in ['2026.10.14 Status proiect.txt','2026.10.14 Log progres proiect.txt','08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.14 Log discutii - STURM ENERGIE.txt','folder map/README.md']:
 p=R/rel;old=p.read_text('utf-8-sig');backup=hist/('2026.10.14 '+p.name if not p.name.startswith('2026.') else p.name)
 if not backup.exists():shutil.copy2(p,backup)
 p.write_text(('# ' if p.suffix=='.md' else '')+entry+'ISTORIC PĂSTRAT\n\n'+old,'utf-8')
assert len(rows)==24
assert all(refs(r[5]) for r in rows)
print(json.dumps({'conversatii':len(rows),'exporturi_email':len(sources),'originale_reutilizate':len(pdf),'surse_modificate':sum(c['identic_index'] is False for c in checks),'raport':str(O/'2026.10.14 Tabel conversatii si contracte STURM.html')},ensure_ascii=False))
