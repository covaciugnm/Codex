from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json, hashlib
from pypdf import PdfReader

BASE = Path.cwd()
WORK = BASE / '00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
R06 = BASE / '00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/2026.10.13 R06 propuneri negociere'
D = Decimal

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def money(v):
    return str(D(v).quantize(D('0.01'), rounding=ROUND_HALF_UP))

def parse_de(v):
    return D(v.replace('.', '').replace(',', '.'))

def save(name, value):
    p = WORK / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return p

specs = {
 'BERGER': {
  'original': '00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Verhandlungsentwurf R06/2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf',
  'original_sha': 'b9d4297e8e68277cc146d00dc5527711640c0da61f1b32f74cddafa6071fc80b',
  'r06_sha': 'b2a5254c4806e4067eadd6d17613b815bcb5d7d85020f672cc32b1964a420d56',
  'mail': '08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/Markus Berger/2026.08.17 20-05 PRIMIT AW AW Angebotsanfrage Ausführungsstatik  ce6905cb.json',
  'offer_date': '2026.08.17',
  'net': 45000,
  'positions': [('Berechnung / Ausführungsstatik',13000,2),('Konstruktions- und Ausführungspläne',20000,2),('Statische Betreuung',2000,2),('Prüfingenieur',10000,3)],
  'hourly': [('Baumeister / Ziviltechniker',150),('Qualifizierter Techniker',135),('Techniker',95),('Sekretariat',75)],
  'original_visits': 8,
  'to': ['office@bmberger.at'], 'cc': [],
  'greeting': 'Sehr geehrter Herr Berger,',
 },
 'PECH': {
  'original': '00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Verhandlungsentwurf R06/2026.10.13 Anlage 5 Originalangebot PECH 2026.09.17.pdf',
  'original_sha': '29495a44171efd95e99b68de2b646d6f0eaf3ecf440e89bd00a9adb82cb74ef1',
  'r06_sha': 'edf8d2831118f5137cb5e616df0a96172ff4aa3781617ded5291668bda84e101',
  'mail': '08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Emailuri/Pech/2026.09.17 11-10 PRIMIT P2026-470 Angebot 63cd2bcb.json',
  'offer_date': '2026.09.17',
  'net': 69300,
  'positions': [('01 Ausführungsstatik',42000,1),('02 Durchbruchsplanung Bestand',6000,1),('03 Baugrubensicherung',5000,1),('04 Untergrundbeschau',800,1),('05 Baubegleitung – 12 Abnahmen',14000,1),('06 Schlussunterlagen',1500,1)],
  'hourly': [('Ziviltechniker',195),('Projektleiter',145),('Techniker',125),('Technischer Zeichner',95)],
  'original_visits': 12,
  'to': ['sekretariat@zt-pech.at'], 'cc': ['ployer@zt-pech.at'],
  'greeting': 'Sehr geehrte Damen und Herren,',
 },
}

results = []
emails = []
for who, s in specs.items():
    original = BASE / s['original']
    assert sha(original) == s['original_sha'], (who, 'original changed')
    reader = PdfReader(str(original))
    texts = [p.extract_text() or '' for p in reader.pages]
    assert len(texts) == 4
    r06p = R06 / f'2026.10.13 Werkvertrag {who} R06 Entwurf.json'
    assert sha(r06p) == s['r06_sha'], (who, 'R06 changed')
    r06 = json.loads(r06p.read_text(encoding='utf-8-sig'))
    a4 = r06['annexes'][3]
    rows = a4['tables'][0]['rows']
    expected = [D(x[1]) for x in s['positions']]
    assert [parse_de(row[1]) for row in rows[:-1]] == expected
    assert sum(expected) == D(s['net'])
    assert parse_de(rows[-1][1]) == D(s['net'])
    assert parse_de(rows[-1][2]) == D(s['net']) * D('.20')
    assert parse_de(rows[-1][3]) == D(s['net']) * D('1.20')
    hr = a4['tables'][4]['rows']
    assert [parse_de(row[1]) for row in hr] == [D(v) for _, v in s['hourly']]
    assert [row[0] for row in hr] == [role for role, _ in s['hourly']]
    alloc = a4['tables'][2]['rows']
    for col, v in enumerate(expected, 1):
        assert sum(parse_de(row[col]) for row in alloc[:-1]) == v
    payment = a4['tables'][3]['rows']
    for row in payment:
        n, tax, gross, ret, cash = [parse_de(v) for v in row[1:]]
        assert tax == n * D('.20') and gross == n + tax
        assert ret == n * D('.05') and cash == gross - ret
    percentages = [10,20,25,15,10,10,10]
    assert sum(percentages) == 100
    assert [parse_de(row[-1]) for row in a4['tables'][1]['rows'][:-1]] == [D(s['net']) * D(p) / 100 for p in percentages]
    budget = a4['tables'][5]['rows']
    option_net = D('1000') if who == 'BERGER' else D('2700')
    assert parse_de(budget[0][2]) == option_net
    assert parse_de(budget[0][3]) == option_net * D('1.20')
    assert parse_de(budget[1][2]) == D(s['net']) + option_net
    assert parse_de(budget[1][3]) == (D(s['net']) + option_net) * D('1.20')
    mailp = BASE / s['mail']
    mail = json.loads(mailp.read_text(encoding='utf-8-sig'))
    assert mail['from_address'].lower() == s['to'][0]
    assert [v.lower() for v in mail['cc']] == s['cc']
    record = {
     'provider': who, 'original_date': s['offer_date'],
     'sources': {'original_pdf':s['original'],'original_sha256':sha(original),'pages':4,'r06_json':str(r06p.relative_to(BASE)),'r06_sha256':sha(r06p),'source_mail':s['mail'],'source_mail_sha256':sha(mailp),'eva_mail_id':mail['id'],'source_mail_status':'PRIMIT'},
     'positions_exact': [{'name':name,'net_eur':money(n),'vat20_eur':money(D(n)*D('.20')),'gross_eur':money(D(n)*D('1.20')),'source_page':page} for name,n,page in s['positions']],
     'net_eur':money(s['net']),'vat20_eur':money(D(s['net'])*D('.20')),'gross_eur':money(D(s['net'])*D('1.20')),
     'hourly_net_eur_exact':[{'role':role,'rate':money(rate),'source_page':3} for role,rate in s['hourly']],
     'original_included_visits':s['original_visits'],
     'supplementary_rate':{'formula':'n × 2.000 EUR / 12; cent rounding only on cumulative net amount','status':'PROPUNERE AG deja autorizată; oferta originală nu indică acest tarif suplimentar'} if who=='BERGER' else {'formula':'n × 450 EUR net','status':'Tarif din oferta originală, p. 1–2; maximum 6 opțiuni este condiția proiectului AG'},
     'six_options_net_eur':money(option_net),'six_options_vat20_eur':money(option_net*D('.20')),'six_options_gross_eur':money(option_net*D('1.20')),
     'package_if_all_six_net_eur':money(D(s['net'])+option_net),'package_if_all_six_gross_eur':money((D(s['net'])+option_net)*D('1.20')),
     'r06_controls':{'position_values_exact':True,'hourly_rates_exact':True,'allocation_columns_exact':True,'seven_payments_total100_exact':True,'vat_gross_retention_cash_exact':True,'options_exact':True},
     'preserve_exact':['Valorile fiecărei poziții și totalurile; fără tarif PI/Bauwerksbuch distinct nou, fără tarif lunar nou.','Regia are aceleași valori și se aplică numai în condițiile contractului pentru suplimente reale aprobate; nu se adaugă automat pachetului.','Pos. 04 PECH 800 EUR este deja inclusă în 69.300 EUR; se facturează o singură dată, fără dublare cu prezența comună.','Repartizarea E1–E7 și retenția nu schimbă onorariul; reducerea temporară a plății prin retenție nu reprezintă reducere de preț.','Opțiunile necomandate nu sunt sumă fixă datorată; consecințele legale ale unei opțiuni deja comandate și apoi abbestellt rămân distincte.'],
    }
    results.append(record)
    body = s['greeting'] + '\n\n' + 'anbei übermitteln wir Ihnen unseren Vertragsvorschlag für das Projekt Schallergasse 35, 1120 Wien. Bitte prüfen Sie den Vorschlag und teilen Sie uns Ihre Anmerkungen mit.\n\n' + 'Sollten Sie den Vorschlag in der übermittelten Form nicht annehmen können, bitten wir um einen konkreten Gegenvorschlag mit den von Ihnen gewünschten Formulierungen.\n\n' + 'Wenn Sie keine Anmerkungen haben, bitten wir um schriftliche Bestätigung Ihres Einverständnisses. Die beiderseitige Unterzeichnung des Vertrags erfolgt anschließend gesondert.\n\n' + 'Mit freundlichen Grüßen\nA&C Wohnart Immobilien GmbH\n'
    email = {'date':'2026.10.13','provider':who,'status':'DRAFT LOCAL / NETRIMIS','eva_mail_draft_id':None,'from':'office@ac-wohnart.at','to':s['to'],'cc':s['cc'],'subject':'Schallergasse35 - Unser Vertragsvorschlag','body_de':body,'attachments':[],'attachment_instruction_ro':'Agentul principal atașează exclusiv PDF-ul final al propriei propuneri pentru acest destinatar. Text local; niciun atașament nu este pretins trimis.','recipient_evidence':{'source_mail':s['mail'],'sha256':sha(mailp),'eva_mail_id':mail['id'],'received_date_readable':s['offer_date'],'sender_original':mail['from_address'],'cc_original':mail['cc']}}
    emails.append(email)
    save(f'2026.10.13 Email {who} Unser Vertragsvorschlag DRAFT LOCAL.json',email)
    (WORK/f'2026.10.13 Email {who} Unser Vertragsvorschlag DRAFT LOCAL.txt').write_text('2026.10.13 — DRAFT LOCAL / NETRIMIS\n\nVon: office@ac-wohnart.at\nAn: '+', '.join(s['to'])+'\nCc: '+(', '.join(s['cc']) or '—')+'\nBetreff: '+email['subject']+'\n\n'+body+'\nNotă internă: PDF-ul final al propriei propuneri va fi atașat separat. Nu este draft EVA și nu a fost trimis.\nSursa destinatari: '+s['mail']+'; ID '+mail['id']+'; '+s['offer_date']+' PRIMIT.\n',encoding='utf-8')

report={'date':'2026.10.13','title':'Reverificare independentă a prețurilor pentru propunerile externe R07','status':'PASS surse originale și R06; R07 nu este încă verificat','scope':'Recitire integrală a celor două PDF originale de câte 4 pagini, hash reconfirmat; verificare aritmetică pe tabelele R06, fără modificarea lor.','providers':results,'no_new_fees_added':True,'limitations':['R07 nu exista în snapshotul acestei verificări; trebuie verificat după redactare.','Sumele noi nu sunt autorizate; extinderea de conținut se propune în totalurile păstrate, fără a pretinde acceptarea prestatorului.','Oferta originală BERGER avea maximum 8 vizite și nu un tarif suplimentar 2.000/12; formula R06 este poziția AG autorizată, păstrată exact.','Nu a fost efectuată o nouă căutare live Eva-Mail; destinatarii au fost confirmați din mesajele originale arhivate.','Nu se afirmă reînnoirea ofertei, acceptarea contractului, acoperirea de asigurare actuală sau trimiterea emailurilor.']}
reportp=save('2026.10.13 Reverificare preturi originale pentru R07.json',report)
lines=['2026.10.13 — Reverificare independentă a prețurilor pentru R07','PASS pentru ofertele originale și R06. Nu certifică încă R07.','']
for r in results:
 lines += [r['provider']+' — oferta '+r['original_date']+'; SHA '+r['sources']['original_sha256'],'Total: '+r['net_eur']+' EUR net + '+r['vat20_eur']+' TVA = '+r['gross_eur']+' brut.']
 lines += ['Poziție: '+p['name']+' — '+p['net_eur']+' net; sursa p. '+str(p['source_page']) for p in r['positions_exact']]
 lines += ['Regie: '+p['role']+' — '+p['rate']+' EUR net/oră.' for p in r['hourly_net_eur_exact']]
 lines += ['Opțiuni: '+r['supplementary_rate']['formula']+'; '+r['supplementary_rate']['status']+'.','Toate cele 6 opțiuni: '+r['six_options_net_eur']+' net / '+r['six_options_gross_eur']+' brut; total condiționat: '+r['package_if_all_six_net_eur']+' net / '+r['package_if_all_six_gross_eur']+' brut.','R06: poziții, regie, alocări, 7 rate 100%, TVA/brut/retenție/plată și opțiuni — toate controlate exact.','R06 SHA '+r['sources']['r06_sha256'],'']
lines += ['DE PĂSTRAT EXACT','Fără majorarea celor 4/6 poziții, a onorariului de bază sau a regiei. Fără taxe noi separate pentru PI, Bauwerksbuch, durata de 18 luni ori întâlnirea inițială inclusă.','BERGER: 166,67 este doar valoare afișată rotunjit; calculul cumulativ rămâne n × 2.000/12, cu 6 = 1.000,00 exact, nu 1.000,02.','PECH: suplimentul este 450,00 net, nu 14.000/12. Cei 800,00 pentru Untergrundbeschau sunt deja în total și se alocă o singură dată.','Noua repartizare a facturării nu este majorare de onorariu și nu generează avans pentru PI neefectuat.','Limite: '+ ' '.join(report['limitations'])]
(WORK/'2026.10.13 Reverificare preturi originale pentru R07.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','report':str(reportp.relative_to(BASE)),'sha256':sha(reportp),'emails':[{'provider':e['provider'],'to':e['to'],'cc':e['cc'],'status':e['status']} for e in emails]},ensure_ascii=True))
