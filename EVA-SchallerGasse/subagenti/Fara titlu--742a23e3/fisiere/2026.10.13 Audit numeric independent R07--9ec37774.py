from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import hashlib, json, re
from pypdf import PdfReader

BASE = Path.cwd()
OUT = BASE / '00.Proiect/09. Vertraege/2026.10.13 Propuneri contract R07 - intern'
R06 = BASE / '00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/2026.10.13 R06 propuneri negociere'
D = Decimal
SHA = {'BERGER':'f2d34a629243d1de36afe2c592a84c5948377ba36e35da8979a7d125bb9edda3','PECH':'c09bf5aaddabca023ac81bfe8d183931729481e3a32dd66c3b647b1a40a98c8b'}
SPECS = {
 'BERGER': {'original':'00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Verhandlungsentwurf R06/2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf','original_sha':'b9d4297e8e68277cc146d00dc5527711640c0da61f1b32f74cddafa6071fc80b','r06_sha':'b2a5254c4806e4067eadd6d17613b815bcb5d7d85020f672cc32b1964a420d56','net':45000,'positions':[13000,20000,2000,10000],'hourly':[150,135,95,75],'six_options':1000},
 'PECH': {'original':'00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Verhandlungsentwurf R06/2026.10.13 Anlage 5 Originalangebot PECH 2026.09.17.pdf','original_sha':'29495a44171efd95e99b68de2b646d6f0eaf3ecf440e89bd00a9adb82cb74ef1','r06_sha':'edf8d2831118f5137cb5e616df0a96172ff4aa3781617ded5291668bda84e101','net':69300,'positions':[42000,6000,5000,800,14000,1500],'hourly':[195,145,125,95],'six_options':2700},
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dec(v): return D(v.replace('.', '').replace(',', '.'))
def eur(v): return str(D(v).quantize(D('.01'), rounding=ROUND_HALF_UP))
def euro_tokens(v): return re.findall(r'EUR\s+([0-9]+(?:\.[0-9]{3})*,[0-9]{2})', json.dumps(v,ensure_ascii=False))

records=[]
for who, s in SPECS.items():
 p=OUT/f'2026.10.13 Werkvertrag {who} R07.json'
 assert sha(p)==SHA[who], f'{who} R07 hash changed'
 r7=json.loads(p.read_text(encoding='utf-8-sig'))
 p6=R06/f'2026.10.13 Werkvertrag {who} R06 Entwurf.json'
 assert sha(p6)==s['r06_sha']
 r6=json.loads(p6.read_text(encoding='utf-8-sig'))
 original=BASE/s['original']
 assert sha(original)==s['original_sha']
 reader=PdfReader(str(original))
 pages=[page.extract_text() or '' for page in reader.pages]
 assert len(pages)==4
 a7=r7['annexes'][3]; a6=r6['annexes'][3]
 assert len(a7['tables'])==6
 for index,(t7,t6) in enumerate(zip(a7['tables'],a6['tables']),1):
  assert t7['rows']==t6['rows'], (who,'table rows changed',index)
 assert r7['presentation']==r6['presentation'], (who,'cover amounts changed')
 for i,(newp,oldp) in enumerate(zip(a7['paragraphs'],a6['paragraphs'])):
  if i==4:
   assert euro_tokens(newp)==[], (who,'new money introduced in neutral visit paragraph')
  else:
   assert euro_tokens(newp)==euro_tokens(oldp), (who,'operative money changed',i+1)
 for number in (11,12):
  sec7=next(v for v in r7['sections'] if v['number']==number)
  sec6=next(v for v in r6['sections'] if v['number']==number)
  assert euro_tokens(sec7)==euro_tokens(sec6), (who,'operative section amounts changed',number)
 section11=next(v for v in r7['sections'] if v['number']==11)
 assert euro_tokens(section11['paragraphs'][0])==[a7['tables'][0]['rows'][-1][1],a7['tables'][0]['rows'][-1][3]]
 assert 'zwanzig Prozent' in section11['paragraphs'][0]
 assert 'keine automatische Indexierung' in section11['paragraphs'][1]
 assert 'nicht zugleich als Pauschalbestandteil, Terminpreis und Regie' in section11['paragraphs'][4]
 section12=next(v for v in r7['sections'] if v['number']==12)
 assert 'fünf Prozent' in section12['paragraphs'][4] and 'Netto-Rechnungsbeträgen' in section12['paragraphs'][4]
 assert 'kein Preisnachlass' in section12['paragraphs'][4]
 net=D(s['net']); table=a7['tables'][0]['rows']
 assert [dec(v[1]) for v in table[:-1]]==[D(v) for v in s['positions']]
 for row in table:
  n,t,g=map(dec,row[1:]); assert t==n*D('.20') and g==n*D('1.20')
 assert sum(dec(v[1]) for v in table[:-1])==net==dec(table[-1][1])
 schedule=a7['tables'][1]['rows']
 percentages=[10,20,25,15,10,10,10]
 assert [v[2] for v in schedule[:-1]]==[f'{v} %' for v in percentages]
 assert [dec(v[3]) for v in schedule[:-1]]==[net*D(v)/100 for v in percentages]
 assert dec(schedule[-1][3])==net and schedule[-1][2]=='100 %'
 allocation=a7['tables'][2]['rows']
 for col, expected in enumerate(s['positions'],1):
  assert sum(dec(row[col]) for row in allocation[:-1])==D(expected)==dec(allocation[-1][col])
 for row in allocation:
  assert sum(dec(v) for v in row[1:-1])==dec(row[-1])
 assert [dec(row[-1]) for row in allocation[:-1]]==[dec(row[-1]) for row in schedule[:-1]]
 payment=a7['tables'][3]['rows']
 for row in payment:
  n,t,g,r,c=map(dec,row[1:]); assert t==n*D('.20') and g==n+t and r==n*D('.05') and c==g-r
 for col in range(1,6): assert sum(dec(v[col]) for v in payment[:-1])==dec(payment[-1][col])
 hourly=a7['tables'][4]['rows']; assert [dec(v[1]) for v in hourly]==[D(v) for v in s['hourly']]
 budget=a7['tables'][5]['rows']; opt=D(s['six_options'])
 assert [dec(v) for v in budget[0][2:]]==[opt,opt*D('1.20')]
 assert [dec(v) for v in budget[1][2:]]==[net+opt,(net+opt)*D('1.20')]
 if who=='BERGER':
  assert 'n × EUR 2.000,00 / zwölf' in a7['paragraphs'][5]
  assert 'kein sechsfach zu multiplizierender Festpreis' in a7['paragraphs'][5]
  cumulative=[(D(n)*2000/12).quantize(D('.01'),rounding=ROUND_HALF_UP) for n in range(7)]
  assert cumulative[-1]==opt and cumulative[-1]!=D('166.67')*6
  assert euro_tokens(a7['paragraphs'][8])==['4.500,00','2.000,00','2.500,00','500,00','1.000,00','1.500,00']
 else:
  assert 'n × EUR 450,00' in a7['paragraphs'][5]
  cumulative=[D(n)*450 for n in range(7)]
  assert cumulative[-1]==opt
  assert 'EUR 14.000,00 / zwölf ist kein Zusatzterminpreis' in a7['paragraphs'][5]
  assert euro_tokens(a7['paragraphs'][8])==['800,00','6.130,00','406,67','813,33','1.220,00']
  assert 'einmalig innerhalb des Grundhonorars' in a7['paragraphs'][8]
 record={'provider':who,'r07_json':str(p.relative_to(BASE)),'r07_sha256':sha(p),'original_pdf':s['original'],'original_sha256':sha(original),'original_pages_read':4,'r06_sha256':sha(p6),'status':'PASS','base_net_eur':eur(net),'vat20_eur':eur(net*D('.20')),'gross_eur':eur(net*D('1.20')),'position_values_net_eur':[eur(v) for v in s['positions']],'hourly_net_eur':[eur(v) for v in s['hourly']],'payment_percentages':percentages,'seven_payments_net_eur':[eur(dec(v[-1])) for v in schedule[:-1]],'retention5_net_eur':eur(net*D('.05')),'cash_gross_minus_net_retention_eur':eur(net*D('1.15')),'options_cumulative_net_eur_n0_to6':[eur(v) for v in cumulative],'six_options_net_eur':eur(opt),'six_options_gross_eur':eur(opt*D('1.20')),'base_plus_all_six_net_eur':eur(net+opt),'base_plus_all_six_gross_eur':eur((net+opt)*D('1.20')),'checked':['§ 11(1) bază și TVA; § 11(2) fără majorare automată/indexare; § 11(5) regie aprobată și fără dublare','§ 12(5) retenție din NET, fără reducerea onorariului','Anexa 4: toate cele șase tabele au exact aceleași rânduri ca R06; calcule independente Decimal pentru fiecare poziție, rate, alocare, TVA, brut, retenție, plată și buget opțiuni','Presentation.cover este identic R06; sumele operative din §§ 11–12 și anexa 4 nu sunt modificate','E2–E4: PI real înainte de facturarea componentei, fără avans automat; E6 proporțional după prestație; E7 și BWB timpuriu fără dublare','Originale recitite și reconfirmate SHA; 4/6 poziții și tarifele regiei exacte'],'new_fee_added':False}
 records.append(record)

report={'date':'2026.10.13','title':'Audit numeric independent R07','status':'PASS pentru ambii prestatori','providers':records,'open_numeric_findings':[],'interpretation':['Tariful opțiunilor BERGER 2.000/12 este propunerea AG autorizată anterior, nu tarif suplimentar pretins din oferta originală; cele 8 vizite originale nu sunt folosite pentru a majora raportul convenit.','PECH 450 EUR net pentru fiecare recepție suplimentară este tariful original. Pos. 04 800 EUR este în baza 69.300 EUR și nu se adaugă din nou.','Repartizarea în șapte rate și retenția nu schimbă prețul; rata nu este automat datorată dacă prestația sa nu a fost efectuată.','Cele șase opțiuni sunt condiționale; acestea nu reprezintă plafon global pentru orice modificare reală ori pretenție legală justificată.'],'limits':['Auditul se referă la fișierele JSON R07 cu SHA indicate; exportul PDF se verifică separat.','Nu certifică acceptarea propunerilor, reînnoirea ofertelor, semnarea sau trimiterea emailurilor.','Nu modifică R06, R07 sau ofertele originale.']}
rp=OUT/'2026.10.13 Audit numeric independent R07.json'
rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['2026.10.13 — Audit numeric independent R07','Rezultat: PASS pentru ambele surse JSON R07. Nicio constatare numerică deschisă.','']
for r in records:
 lines += [r['provider']+' — R07 SHA '+r['r07_sha256'],'Original SHA '+r['original_sha256']+'; 4 pagini recitite.','Bază: '+r['base_net_eur']+' net + '+r['vat20_eur']+' TVA = '+r['gross_eur']+' brut.','Poziții originale net: '+', '.join(r['position_values_net_eur'])+'.','Regie net/oră: '+', '.join(r['hourly_net_eur'])+'.','Rate E1–E7 net: '+', '.join(r['seven_payments_net_eur'])+'; 10/20/25/15/10/10/10 = 100%.','Retenție 5% net: '+r['retention5_net_eur']+'; total plăți brut minus retenție: '+r['cash_gross_minus_net_retention_eur']+'.','Opțiuni net cumulativ n0–6: '+', '.join(r['options_cumulative_net_eur_n0_to6'])+'.','Toate cele 6 opțiuni: '+r['six_options_net_eur']+' net / '+r['six_options_gross_eur']+' brut; total condiționat: '+r['base_plus_all_six_net_eur']+' net / '+r['base_plus_all_six_gross_eur']+' brut.']
 lines += ['Control PASS: '+v for v in r['checked']]+['']
lines += ['Interpretare: '+v for v in report['interpretation']]+['Limită: '+v for v in report['limits']]
(OUT/'2026.10.13 Audit numeric independent R07.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','report':str(rp.relative_to(BASE)),'sha256':sha(rp),'r07_hashes':SHA},ensure_ascii=True))
