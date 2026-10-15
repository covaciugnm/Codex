import json,pathlib,hashlib,decimal
P=pathlib.Path(__file__).resolve().parent
N=P.parent
ROOT=P.parents[3]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mapping={}
def assign(ids,refs):
 for i in ids:mapping[f'N{i:03}']=refs
assign([1],['§ 2(1)','§§ 3–6','Anlage 1'])
assign([2,5],['§ 2(2)','§ 3(1)','Anlage 2','Anlage 3 D1'])
assign([3],['§ 1','Anlage 6 Vertretungsnachweise'])
assign([4],['§ 2(3)–(5)','§ 16(1)','Anlage 5'])
assign(range(6,12),['§ 3(2)–(5)','Anlage 1','Anlage 3 D2–D5'])
assign([12,13],['§ 4(1)–(2)','Anlage 1','Anlage 3 D2–D5'])
assign([14],['§ 4(3)','Anlage 3(5)','Anlage 4 E5'])
assign([15],['§ 4(4)–(5)','Anlage 1'])
assign([16],['§ 4(1)/(5)','§ 5(7)'])
assign([17],['§ 3(6)','§ 6(4)','§ 8(2)'])
assign([18],['§ 5(1)','Anlage 6 PI'])
assign([19],['§ 5(2)','§ 14(1)–(2)','Anlage 6 PI'])
assign([20],['§ 5(3)/(7)','§ 7','Anlage 3'])
assign([21],['§ 5(4)','Anlage 4(3)'])
assign([22],['§ 5(5)','§ 7(3)'])
assign([23],['§ 5(6)','Anlage 6 §128'])
assign([24],['§ 5(7)','§ 6(4)','§ 8(4)'])
assign([25],['§ 5(8)','§ 11(2)'])
assign(range(26,34),['§ 6','Anlage 1 Bauwerksbuch','Anlage 3(6)','Anlage 6 Rollen'])
assign([34,35],['§ 7(1)–(3)','§ 8(2)','Anlage 3(2)','Anlage 3 Termin1–12'])
assign([36,37,40],['§ 5(3)','§ 7(3)–(5)','§ 11(1)/(5)','Anlage 3(4)','Anlage 4 Optionen'])
assign([38,39],['§ 7(4)','Anlage 4 Optionstarif/Optionstabelle'])
assign([41],['§ 7(6)','§ 9(8)'])
assign([42],['§ 7(2)','Anlage 3 Termin1','Anlage 4 PECH Position04/05'])
assign([43],['§ 8(1)','Anlage 2'])
assign([44],['§ 8(2)','Anlage 3 T0-Begehung'])
assign([45,46],['§ 8(2)–(3)/(6)','§ 11','Anlage 6 Werkstatt/Material'])
assign([47,48],['§ 8(4)–(5)','§ 4(5)'])
assign([49],['§ 9(1)','Anlage 3 T0'])
assign([50],['§ 9(2)–(3)','Anlage 3 B0/B0+18'])
assign([51,52],['§ 9(6)','§ 13(1)','Anlage 3 D1–D5/(3)'])
assign([53],['§ 9(3)/(8)','§ 7(3)'])
assign([54,55],['§ 9(4)–(5)/(7)','§ 15(2)'])
assign([56,57],['§ 10(1)–(2)/(7)'])
assign([58,59,60],['§ 10(3)–(5)','§ 15(5)'])
assign([61],['§ 10(6)','Anlage 4 E7'])
assign([62,63,64],['§ 11(1)–(2)','Anlage 4 Originalpositionen/E1–E7/Allokation'])
assign([65,66,67],['§ 11(3)–(5)','§ 8(3)','Anlage 4 Zusatzregie/Optionen'])
assign([68,69,70,71,72,73],['§ 12(1)–(4)','Anlage 4 E1–E7/PI-Zuordnung','§ 15(2)/(4)/(6)'])
assign([74,75,76],['§ 12(5)–(7)','§ 13(3)–(4)','§ 15(6)','Anlage 6 Bankgarantie'])
assign([77,78,79,80,81],['§ 13(1)–(6)','§ 15(6)','Anlage 6 Gewährleistung/Verzug'])
assign([82,83],['§ 14(1)–(2)','Anlage 6 Personen'])
assign([84],['§ 14(3)–(5)','Anlage 6 Haftpflicht'])
assign([85],['§ 14(5)','§ 10(5)'])
assign(range(86,91),['§ 15(1)–(6)','§ 12(1)/(7)','§ 13(4)'])
assign([91,92,93,94],['§ 16(1)–(5)','Anlage 6 Vollmachten'])
assign([95,97],['§ 2(5)','Anlage 6(2)–(3)','Anlage 6 Kapazität/Preisgültigkeit'])
assign([96],['§ 10(7)'])
assign([98],['§ 3(7)','§ 11(2)'])
assign([99],['§ 2(5)','Anlage 2 Bauteilliste','§ 7(6)','§ 11'])
assign([100],['Präambel','§ 2(5)','Anlage 5','Quellen-/Änderungsregister'])
matrix=load(N/'2026.10.13 Cerinte comune negociere matrice.json')
assert set(mapping)=={r['id'] for r in matrix['matrice']}
js={pr:load(P/f'2026.10.13 Werkvertrag {pr} R06 Entwurf.json') for pr in ['BERGER','PECH']}
diff=[]
for sb,sp in zip(js['BERGER']['sections'],js['PECH']['sections']):
 assert sb['number']==sp['number'] and sb['title']==sp['title'] and len(sb['paragraphs'])==len(sp['paragraphs'])
 for i,(b,p) in enumerate(zip(sb['paragraphs'],sp['paragraphs']),1):
  if b!=p:diff.append(f'§ {sb["number"]}({i})')
assert diff==['§ 1(2)','§ 11(1)']
for i in [0,1,2,5]:assert js['BERGER']['annexes'][i]==js['PECH']['annexes'][i]
checks=[]
def D(x):return decimal.Decimal(x.replace('.','').replace(',','.'))
for pr,j in js.items():
 assert len(j['sections'])==16 and len(j['annexes'])==6
 table=j['annexes'][3]['tables'][2]
 for r in table['rows'][:-1]:assert sum(D(x) for x in r[1:-1])==D(r[-1])
 for c in range(1,len(table['headers'])):assert sum(D(r[c]) for r in table['rows'][:-1])==D(table['rows'][-1][c])
 assert sum(j['financial_check']['common_payment_percent'])==100
 assert j['financial_check']['payment_sum']==j['financial_check']['net']
 for r in j['annexes'][3]['tables'][3]['rows']:
  assert D(r[1])+D(r[2])==D(r[3])
  assert D(r[1])*decimal.Decimal('.05')==D(r[4])
  assert D(r[3])-D(r[4])==D(r[5])
 checks.append({'provider':pr,'r06_sha256':sha(P/f'2026.10.13 Werkvertrag {pr} R06 Entwurf.json'),'r05_sha256_copy':sha(P/f'2026.10.13 Historische Inhaltskopie {pr} R05.json'),'sections':16,'main_paragraphs':sum(len(s['paragraphs']) for s in j['sections']),'annexes':6,'allocation_row_column_sums':'PASS','base':j['financial_check']['net'],'option6':j['financial_check']['max_optional_net'],'with6':j['financial_check']['full_six_options_net'],'penalty5percent':j['financial_check']['penalty_max_net']})
coverage=[{'id':r['id'],'criterion':r['criteriu'],'r06_common_references':mapping[r['id']],'status':'Redaktionell zugeordnet; unabhängige inhaltliche Prüfung ausstehend'} for r in sorted(matrix['matrice'],key=lambda x:x['id'])]
report={'date':'2026.10.13','status':'Autorenkontrolle, keine unabhängige Schlussprüfung und keine Unterzeichnungsfreigabe','matrix_sha256':sha(N/'2026.10.13 Cerinte comune negociere matrice.json'),'coverage_count':len(coverage),'common_main_differences_only':diff,'common_annexes_identical':[1,2,3,6],'checks':checks,'coverage':coverage,'limitations':['R06 bleibt neue AG-Verhandlungsvorlage, nicht angenommen, nicht versendet.','Rechtliche Wirksamkeit und Berufs-/Versicherungsnachweise werden nicht durch arithmetische Kontrolle bestätigt.','Die Zuordnung sämtlicher 100 Kriterien ist eine konkrete Autoren-Konkordanz und keine Behauptung einer erfolgten unabhängigen Vollprüfung.','Offene Vertretungs-/Rollen-/tatsächliche Datumsfelder müssen vor Unterzeichnung rechtmäßig bestätigt werden.']}
save(P/'2026.10.13 R06 Autorenkontrolle und Konkordanz100.json',report)
(P/'2026.10.13 R06 Autorenkontrolle kurz.txt').write_text('2026.10.13 — Autorenkontrolle R06\n\nNeue Verhandlungsentwürfe der AG, keine angenommenen Verträge. Alle 100 Matrixkriterien haben konkrete R06-Verweise; diese Konkordanz ist die Kontrolle des Verfassers und ersetzt nicht die angeforderte unabhängige Prüfung. Beide Texte haben 16 Paragraphen, 96 Hauptabsätze und 6 Anlagen.\n\nUnterschiede im Haupttext ausschließlich § 1(2) (AN-Identität) und § 11(1) (Honorarwerte). Anlagen 1, 2, 3, 6 sind identisch. Anlage 4 unterscheidet nur Originalpositionen, wirtschaftliche Allokationen, Sätze, Beträge und deren Herkunft. Anlage 5 nennt das eigene unveränderte Originalangebot.\n\nAlle Allokationszeilen und -spalten stimmen; alle sieben Gesamtraten stimmen. Zahlungstabelle: netto + USt = brutto; Einbehalt = 5 % netto; Auszahlung = brutto minus Einbehalt. BERGER: Grundhonorar EUR 45.000 netto / EUR 54.000 brutto; sechs Optionen EUR 1.000 netto / EUR 1.200 brutto. PECH: EUR 69.300 netto / EUR 83.160 brutto; sechs Optionen EUR 2.700 netto / EUR 3.240 brutto. Der Optionspreis wirkt nicht als automatische Bestellung oder pauschaler Verzicht auf andere gesetzlich begründete Ansprüche.\n\nFunktionen und Befugnisse, aktuelle Vertretung, tatsächliche Daten, Garantieformular und bestehende Police sind vor Unterzeichnung zu bestätigen. Keine neue numerische Versicherungsforderung der AG. Keine behördliche Anerkennung, Mangelfreiheit historischer Substanz oder heutige Annahme wird bestätigt. Die R05-Kopien stimmen exakt mit den eingefrorenen Quellen überein. Die beigefügten Originalangebote werden nicht verändert.\n',encoding='utf-8')
print(json.dumps({'checks':checks,'common_differences':diff,'coverage_count':len(coverage)},ensure_ascii=False,indent=2))
