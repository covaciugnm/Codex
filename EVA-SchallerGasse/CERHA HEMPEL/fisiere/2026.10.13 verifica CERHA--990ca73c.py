from pathlib import Path
import json,base64,hashlib,re
R=Path(__file__).resolve().parent.parent
O=R/'08. Corespondenta/2026.10.13 CERHA notificare 26-30363'
S=json.loads((R/'folder map/2026.10.13 CERHA surse temporare.json').read_text(encoding='utf-8'))
E=S['email']; records=[]
for item in json.loads((R/'folder map/2026.10.13 CERHA octeti temporari.json').read_text(encoding='utf-8')):
 a=item['a'];parts=[];pos=0
 for c in item['chunks']:
  b=base64.b64decode(c['content_base64']);assert c['offset']==pos;assert hashlib.sha256(b).hexdigest()==c['chunk_sha256'];parts.append(b);pos+=len(b)
 b=b''.join(parts);assert len(b)==a['size'];assert b.startswith(b'%PDF')
 p=O/('2026.10.13 '+re.sub(r'[\r\n]+',' ',a['name']));p.write_bytes(b)
 records.append(dict(id=a['id'],nume_original=a['name'],cale=p.relative_to(R).as_posix(),sha256=hashlib.sha256(b).hexdigest(),octeti=len(b),status='PRIMIT; original integral'))
(O/'2026.10.13 PRIMIT Notificare CERHA.json').write_text(json.dumps(E,ensure_ascii=False,indent=2),encoding='utf-8')
header=f"2026.10.13 | PRIMIT\nData tehnica: {E['received_at']}\nDe la: {E['from_address']}\nCatre: {', '.join(E['to'])}\nCC: {', '.join(E['cc']) or 'fara CC'}\nSubiect: {E['subject']}\nID Eva-Mail: {E['id']}\nExport text integral API, nu MIME original.\n\n"
(O/'2026.10.13 PRIMIT Notificare CERHA.txt').write_text(header+E['text'],encoding='utf-8')
(O/'2026.10.13 Registru anexe.json').write_text(json.dumps({'documente':records,'imagini_semnatura':'3 imagini mici: numai metadate in exportul mesajului; nu documente financiare'},ensure_ascii=False,indent=2),encoding='utf-8')
note='''2026.10.13 | Verificare CERHA HEMPEL - Honorarnote 26/30363
Status scurt: 2.640,22 EUR fara plata identificata in extrasele disponibile AT22 (firma) si AT13 (personal), ambele pana la 2026.09.28. Creditorul declara suma neachitata la 2026.10.13. Lipseste acoperirea bancara pentru 2026.09.29-2026.10.13; nu este confirmat soldul bancar la zi.
Ultimul raspuns: notificare PRIMITA de la Bogdan Capra la 2026.10.13; cere plata pana vineri 2026.10.16. Scadenta initiala 2026.05.05; factura din 2026.04.21, servicii 2026.03.16-2026.03.31.
Urmatorul pas: verificarea extrasului/istoricului bancar pentru 2026.09.29-2026.10.13 inainte de o eventuala noua plata; daca exista debit, comunicarea dovezii catre avocat. Nicio plata sau comunicare efectuata prin aceasta verificare.
Surse: email EVA d2bb3a63-79fd-4d31-b497-2a13f570fab9, export si trei anexe originale in 08. Corespondenta/2026.10.13 CERHA notificare 26-30363; extrase originale in 10. Banci + Extrase de cont/Extrase de cont A&C Wohnart (RLB AT22 3200 0000 1503 7500) si Extrase de cont Cosmin Covaciu (RLB AT13 3200 0000 1191 2516).
Factura era deja inregistrata: 2026.09.30 Reconciliere completa facturi si plati.xlsx, Registru documente, rand 17, F016, FARA PLATA IDENTIFICATA; 2026.09.30 De platit - Schallergasse 35 - verificat.xlsx, Fara plata identificata, rand 2. Exista si PDF in Facturi neachitate, pozitia 04. Notificarea nu adauga o a doua datorie.
Plati CERHA identificate in AT22: 2026.02.16 6.147,70 EUR referinta Honorarnote 25/31404; 2026.03.31 24.116,00 EUR referinta bancara exacta Honorarnote 26/301186. Aceste referinte nu sunt 26/30363. Celelalte doua transferuri CERHA din 2026.02.23, 75.900,00 EUR si 1.650.000,00 EUR, mentioneaza taxele si pretul tranzactiei imobiliare. Nicio plata CERHA dupa emiterea facturii in extrasul firmei. Nicio plata CERHA identificata in extrasul personal.
Verificare: SHA-256 identic cu indexul pentru cele doua extrase generale, factura si doua copii ale extrasului Conrad. Texte indexate reutilizate; factura si toate cele 5 pagini ale extraselor generale verificate vizual. Cautare dupa suma, beneficiar si numar factura; nu s-au identificat extrase generale mai recente in arhiva locala. Extrasele generale nu contin IBAN-ul beneficiarului pentru fiecare tranzactie, deci nu este pretinsa verificarea tuturor IBAN-urilor din banca.
Acoperire: actualizare punctuala CERHA; un mesaj nou arhivat integral ca text/JSON si trei PDF originale. Nu este o noua sincronizare generala. Registrele centrale anterioare si toate versiunile istorice raman pastrate; acest dosar este suplimentul de acoperire pentru verificarea curenta.
'''
report=R/'10. Banci + Extrase de cont/2026.10.13 Verificare CERHA 26-30363/2026.10.13 Raport verificare plata.txt'
report.write_text(note,encoding='utf-8')
for p in [R/'2026.10.13 Status proiect.txt',R/'2026.10.13 Log progres proiect.txt']:
 old=p.read_text(encoding='utf-8-sig');p.write_text(note+'\nISTORIC PASTRAT\n\n'+old,encoding='utf-8')
partner=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.13 Log discutii - CERHA HEMPEL.txt'
old=R/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.07 Log discutii - CERHA HEMPEL.txt'
partner.write_text(note+'\nISTORIC PASTRAT\n\n'+old.read_text(encoding='utf-8-sig'),encoding='utf-8')
readme=R/'folder map/README.md'
readme.write_text('# 2026.10.13 — CERHA: verificare plata 26/30363\n\nRaport: ../'+report.relative_to(R).as_posix()+'. Fara debit identificat pana la 2026.09.28 in AT22/AT13. Notificare PRIMITA 2026.10.13, termen 2026.10.16; mesaj integral si trei PDF originale salvate in ../08. Corespondenta/2026.10.13 CERHA notificare 26-30363/. Factura era deja F016 in lista de platit. Perioada bancara 2026.09.29–2026.10.13 ramane neverificata. Supliment punctual la acoperirea centrala, fara dublare de datorie. Jurnalele TXT actualizate, istoricul pastrat.\n\nISTORIC PASTRAT\n\n'+readme.read_text(encoding='utf-8'),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
