from pathlib import Path
from copy import deepcopy
from decimal import Decimal
import json,hashlib,re

root=Path.cwd();src=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.27 Observatii BERGER si comparatie/2026.10.27 BERGER R10 model comparativ si discutii.json'
m=json.loads(src.read_text(encoding='utf-8'));old=m['original'];new=deepcopy(m['vorschlag'])
folder=root/'00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11';folder.mkdir(parents=True,exist_ok=True)
answers=[
 {'id':'A01','data':'2026.10.29','tema':'Bauwerksbuch','raspuns':'Îl includem la 2.500 EUR net, cu obiectul complet explicit.'},
 {'id':'A02','data':'2026.10.29','tema':'PI/ZT','raspuns':'Lăsăm numele de completat de BERGER și cerem confirmarea serviciilor și includerii în preț.'},
 {'id':'A03','data':'2026.10.29','tema':'Polierplanung/Planwechsel/Bauführer','raspuns':'Nu sunt desemnați: păstrăm delimitarea și câmpurile de completat, fără atribuirea acestor funcții lui BERGER.'},
 {'id':'A04','data':'2026.10.29','tema':'Termene','raspuns':'5 zile lucrătoare pentru planurile de atelier; 3 zile pentru răspunsurile tehnice uzuale.'},
 {'id':'A05','data':'2026.10.29','tema':'Formate','raspuns':'PDF semnat, DWG/DXF editabile și calcule complete; IFC și fișiere native în măsura în care există.'},
 {'id':'A06','data':'2026.10.29','tema':'Raportare','raspuns':'Email săptămânal scurt în perioadele active și o listă comună simplă de decizii/documente.'}]
def section(n):return next(x for x in new['sections'] if x['number']==n)
def setp(n,i,text):section(n)['paragraphs'][i-1]=text
def repl(n,i,a,b):
 s=section(n)['paragraphs'][i-1];assert a in s,(n,i,a);section(n)['paragraphs'][i-1]=s.replace(a,b)

new['version']='R11';new['date']='2026.10.29';new['preamble']=[]
new['presentation']['cover'].update(base_net='EUR 47.500,00',vat='EUR 9.500,00',base_gross='EUR 57.000,00')
repl(1,4,'Die architektonische Ausführungs- und Polierplanung wird durch die in Anlage 6 bezeichnete Fachperson [vor Unterzeichnung zu ergänzen] erbracht;','Architektonische Ausführungs- und Polierplanung, Einreichplanung, verfahrensführende Planverfassung und Bauführung sind nicht an den AN vergeben. Sie werden durch die von der AG gesondert zu beauftragenden und in Anlage 6 zu ergänzenden Fachpersonen erbracht;')
repl(5,3,'werden im Vertragsvorschlag der eigenen Pauschale von EUR 10.000,00 zugeordnet;','werden der eigenen Pauschale von EUR 10.000,00 zugeordnet;')
section(5)['paragraphs'][5]+=' Der AN ergänzt vor Unterzeichnung in Anlage 6 die konkrete Person sowie die ausdrückliche Bestätigung, ob die vorstehend vollständig bezeichneten ZT-Leistungen im Gesamthonorar enthalten sind und welcher bestehenden Position sie zugeordnet sind. Eine abweichende Vergütung bedarf vor Unterzeichnung einer ausdrücklich beiderseits vereinbarten Anpassung; eine einseitige Zusatzrechnung wird dadurch nicht zugelassen.'
section(6)['paragraphs'].append('Für den vollständigen Leistungsumfang dieses § 6 einschließlich der erforderlichen geeigneten Fachbeiträge, der Erstprüfung des Bestands, der Dokumentation, der erforderlichen Registrierung und der Fortschreibung für neue beziehungsweise geänderte Bauteile bis zum vereinbarten Abschluss wird ein gesondertes Pauschalhonorar von EUR 2.500,00 netto zuzüglich gesetzlicher Umsatzsteuer vereinbart. Dieser Betrag ist im Gesamthonorar nach § 11 und Anlage 4 bereits enthalten und wird nicht nochmals zusätzlich zum dortigen Gesamtbetrag verrechnet. Die Prüfung kann sachgerechte Grenzen aufgrund fehlender Zugänglichkeit haben; sie sind im Befund konkret zu dokumentieren und ändern den geschuldeten Gesamtgebäudebezug nicht. Neue invasive Öffnungen, Laborprüfungen oder bauliche Mängelbehebungen sind nicht allein durch die Bucherstellung beauftragt; §§ 8 und 11 gelten. Bereits erkennbare notwendige Fachbeiträge zur vereinbarten Bucherstellung sind mit der Pauschale abgegolten.')
repl(10,1,'Ob darüber hinaus ein neues IFC-Modell oder ein bestimmtes natives Datenformat verpflichtend zu erstellen ist, ist vor Unterzeichnung ausdrücklich in Anlage 1 zu entscheiden; diese noch offene Wahl begründet weder dessen Abbestellung noch einen Zusatzpreis.','Die Neuerstellung eines IFC-/BIM-Modells oder die zusätzliche Konvertierung in ein bisher nicht verwendetes natives Datenformat wird nicht geschuldet. Vorhandene projektbezogene IFC- und native Dateien werden nach Maßgabe der vorstehenden rechtlichen und technischen Übertragbarkeit mitgeliefert. Die verpflichtende Übergabe der unterfertigten PDF-Unterlagen, bearbeitbaren DWG/DXF-Dateien und vollständigen nachvollziehbaren Berechnungen bleibt hiervon unberührt.')
setp(11,1,'Das feste Gesamthonorar für das vereinbarte Paket beträgt EUR 47.500,00 netto zuzüglich gesetzlicher Umsatzsteuer; bei zwanzig Prozent EUR 57.000,00 brutto. Es setzt sich aus den vier ursprünglichen Honorarpositionen von zusammen EUR 45.000,00 netto und dem gesondert ausgewiesenen Bauwerksbuchhonorar nach § 6 von EUR 2.500,00 netto zusammen. Die vier ursprünglichen Positionen und ihre Beträge bleiben unverändert; Anlage 4 weist den Zusatz und den Gesamtbetrag ausdrücklich aus. Teilrechnungen und Abschlagszahlungen werden entsprechend der Erfüllung des Leistungsbildes gelegt; eine feste prozentuale Zahlungsstaffel wird nicht vereinbart. Das Honorar umfasst die Planung ab T0, achtzehn Monate Bauphasenrahmen ab tatsächlichem B0 und die zugehörigen üblichen Schlussleistungen einschließlich der bezeichneten Bauwerksbuchleistungen. Umfang, personelle Besetzung und Preiszuordnung der PI-/ZT-Leistungen werden vor Unterzeichnung nach § 5 und Anlage 6 ausdrücklich bestätigt. Zusätzliche tatsächliche statische Betreuung nach § 7 wird nur in ausdrücklich bestellten Viererpaketen nach Anlage 4 gesondert vergütet. Der Bauwerksbuchbetrag ist bereits im Gesamtbetrag enthalten; weder dieselbe Buchleistung noch bloßer Zeitablauf begründen eine zweite Pauschale. Vor Unterzeichnung wird in Anlage 4 ein zum Bauablauf passender beiderseits bestätigter Leistungs- und Rechnungsplan mit konkreten Liefergegenständen, Daten, Nettobeträgen, Umsatzsteuer und Anrechnung früherer Teilzahlungen ergänzt. Eine pauschale prozentuale Vorauszahlung ohne den vereinbarten Leistungsbezug wird dadurch nicht eingeführt; noch leere Betrags- oder Datumsfelder gelten nicht als vereinbarte Tranche.')
repl(12,1,'die ursprünglichen Positionsbeträge und das Gesamtnettohonorar','die vereinbarten Positionsbeträge einschließlich der gesondert ausgewiesenen Bauwerksbuchposition und das Gesamtnettohonorar')
repl(9,2,'Vor Beginn ist die normale Ausführung innerhalb dieses achtzehnmonatigen Rahmens kein selbständiger Zusatzhonorargrund.','Die normale Ausführung innerhalb dieses achtzehnmonatigen Rahmens begründet für sich kein zusätzliches zeitabhängiges Honorar.')

for a in new['annexes']:
 n=a['number']
 if n==1:
  a['paragraphs']=[t for t in a['paragraphs'] if not t.startswith('Vor Unterzeichnung ausdrücklich zu entscheiden:')]
  a['paragraphs'].append('Verbindliche Datenübergabe: unterfertigtes PDF, bearbeitbare DWG/DXF-Dateien und vollständige nachvollziehbare Berechnungen. Vorhandene projektbezogene IFC- und native Dateien werden im rechtlich und technisch übertragbaren Umfang übergeben; eine neue IFC-/BIM-Modellerstellung oder zusätzliche Fremdformatkonvertierung ist nicht beauftragt. Die architektonische Polierplanung, verfahrensführende Einreich-/Planwechselplanung und Bauführung sind gesondert von der AG zu beauftragen; die statische Zuarbeit und der im Vertrag bezeichnete tragwerksbezogene Planwechsel bleiben beim AN.')
 if n==2:
  for t in a['tables']:
   for row in t['rows']:
    if row[0]=='Architektonische Polierplanung / Einreichplaner':row[1]='Von der AG gesondert zu beauftragen; derzeit nicht benannt. Umfang und Schnittstellen getrennt bestätigen; keine automatische Funktionsübernahme des AN.'
 if n==3:
  a['paragraphs']=[t.replace('Für übliche technische RFI werden drei Werktage nach § 7 Abs. 6 vorgeschlagen.','Für übliche technische RFI gelten drei Werktage nach § 7 Abs. 6; für die übliche Werkstattplanprüfung fünf Werktage nach § 4 Abs. 3.') for t in a['paragraphs']]
 if n==4:
  a['paragraphs'][0]='Die vier ursprünglichen Honorarpositionen bleiben mit zusammen EUR 45.000,00 netto unverändert. Hinzu kommt das gesonderte Pauschalhonorar für das vollständige Bauwerksbuch nach § 6 von EUR 2.500,00 netto. Das Gesamthonorar beträgt damit EUR 47.500,00 netto, bei zwanzig Prozent EUR 9.500,00 Umsatzsteuer und EUR 57.000,00 brutto. Es wird keine zusätzliche prozentuale Zahlungsstaffel oder vertragliche Retention vereinbart.'
  a['paragraphs'][5]=a['paragraphs'][5].replace('das Grundhonorar von EUR 45.000,00 bleibt unverändert','das Gesamthonorar ohne optionale Zusatzbesuche von EUR 47.500,00 bleibt unverändert')
  a['paragraphs'][7]='Vor Unterzeichnung ergänzen und bestätigen beide Parteien den konkreten Leistungs- und Rechnungsplan nach § 11 Abs. 1: jeweiliger Liefergegenstand, Datum, zugeordnete Honorarposition, etwaige Teilbeträge, USt und Bruttobetrag sowie Anrechnung früherer Teilzahlungen. Die Summe der innerhalb einer Position vereinbarten Teilbeträge darf deren nachstehendes Honorar nicht überschreiten. Die Bauwerksbuchposition ist bereits im Gesamtbetrag enthalten. Die konkrete PI-/ZT-Zuordnung und ihre Einbeziehung in die bestehenden Positionen bestätigt der AN ausdrücklich in Anlage 6; eine Abweichung wird vor Unterzeichnung gesondert vereinbart, nicht einseitig fakturiert.'
  fee=a['tables'][0];assert fee['rows'][:4]==old['annexes'][3]['tables'][0]['rows'][:4]
  fee['rows']=fee['rows'][:4]+[['Bauwerksbuch vollständig gemäß § 6','2.500,00','500,00','3.000,00'],['GESAMT','47.500,00','9.500,00','57.000,00']]
  options=a['tables'][2]['rows'];options[1][2:]=['48.500,00','58.200,00'];options[2][2:]=['49.500,00','59.400,00']
  for row in options[1:]:row[0]=row[0].replace('Grundhonorar','Gesamthonorar einschließlich Bauwerksbuch')
  a['tables'].append({'headers':['Honorarposition / Hauptetappe','Liefer- und Rechnungsgrundlage','Termin / vereinbarte Teilbeträge','Positionsbetrag netto EUR'],'widths_cm':[4,6,4,2.5],'rows':[
   ['Ausführungsstatik','D1/D2 und nachgewiesene vertragsgemäße statische Ergebnisse; konkrete Teilbeträge gemeinsam zuordnen','Datum / Teilbeträge: __________','13.000,00'],
   ['Konstruktions- und Ausführungspläne','Lieferpakete D2-D5; vollständige prüffähige Lieferstände und vereinbarte Korrekturen','Daten / Teilbeträge: __________','20.000,00'],
   ['Statische Betreuung','Vereinbartes Leistungsbild, maximal acht tatsächliche statische Betreuungsbesuche; kein monatlicher Abruf','Bauphasen / Rechnungsstände: __________','2.000,00'],
   ['Prüfingenieur','Bestätigter Prüfplan, tatsächlich erbrachte Beschauen, Befunde und vereinbarte Schlussleistungen; PI/ZT-Zuordnung in Anlage 6 bestätigen','Prüfphasen / Teilbeträge: __________','10.000,00'],
   ['Bauwerksbuch','Gesamtgebäude Bestand + neue/geänderte Teile, Erstprüfung, Buch, erforderliche Registrierung und Fortschreibung nach § 6','Bestand fristgerecht; Umbau vor Anzeige; Teilbeträge: __________','2.500,00'],
   ['GESAMT','Keine Doppelfakturierung; Teilbeträge innerhalb der Positionsbeträge','Vor Unterzeichnung beiderseits bestätigen','47.500,00']]})
 if n==5:
  a['paragraphs'][0]='Das vollständige vierseitige Originalangebot des AN vom 2026.08.17 ist diesem Vertrags-PDF als unveränderter Originalblock am Ende beigefügt und bildet sachlich Anlage 5. Die ergänzende Geltung richtet sich nach der Rangfolge in § 2 Abs. 3. Die mit diesem Vertrag vereinbarten Änderungen, insbesondere der achtzehnmonatige Bauphasenrahmen und die gesonderte Bauwerksbuchposition, ergeben sich aus Hauptvertrag und Anlagen 1-4 und 6.'
  a['paragraphs'].append('Der ergänzende Preisansatz von EUR 2.500,00 netto für das Bauwerksbuch wurde vom AN mit E-Mail vom 2026.10.27, Betreff «AW: 15., Schallergasse 35; Werkvertrag Anmerkungen», mitgeteilt. Der vollständige hierfür vereinbarte Leistungsumfang ist in § 6 und Anlage 1 bezeichnet; der Betrag ist in Anlage 4 bereits eingerechnet. Die E-Mail ersetzt nicht die beiderseitige Unterzeichnung dieses vollständigen Vertrages.')
 if n==6:
  rows=a['tables'][0]['rows'];rows[:]=[row for row in rows if row[0]!='Offene AG-Entscheidungen']
  for row in rows:
   if row[0]=='Architektonische Polierplanung / Einreichplaner / Bauführer':row[1]='Noch nicht benannt; von der AG gesondert zu beauftragen. Keine Übernahme durch den AN. Name, Firma, Befugnis, Zuständigkeit und Bestellstatus vor dem jeweiligen erforderlichen Beginn ergänzen: ________________'
   if row[0]=='PI / ZT: Namensklärung':row[1]='Vom AN vor Unterzeichnung zu ergänzen: vollständiger Name und Organisation je Funktion, aktuelle Befugnis, erforderliche Unabhängigkeit; konkreter Leistungsumfang und Einbeziehung in die Honorarpositionen ohne weiteren Preis: ________________'
   if row[0].startswith('Bauwerksbuch:'):row[1]='Ersteller, Erstprüfer und erforderliche weitere Fachpersonen mit jeweiliger Befugnis/Unabhängigkeit: ________________. Vollständiger Umfang nach § 6 in der Pauschale EUR 2.500,00 netto enthalten; keine zweite Verrechnung neben dem Gesamtbetrag.'
  rows.append(['Zusätzliche eigenständige Prüfstatik, soweit tatsächlich erforderlich','Vor Unterzeichnung Bedarf, Prüfgegenstand und verantwortliche Person klären. Nicht pauschal bestellt; kein offener Blankobetrag. Keine Verrechnung bereits geschuldeter eigener Planung/PI-Leistungen: ________________'])
  for row in a['tables'][1]['rows']:
   if row[0]=='PI / ZT / Bauwerksbuch':row[1]='PI-Leistungen und Preiszuordnung zur Pauschale EUR 10.000,00 sowie vollständige ZT-Schlussleistungen nach § 5 vor Unterzeichnung ausdrücklich bestätigen. Personen vom AN ergänzen. Vollständiges Bauwerksbuch für Bestand und neue/geänderte Bauteile einschließlich Erstprüfung und erforderlicher Registrierung als eigene Position EUR 2.500,00 netto im Gesamtpreis enthalten.'
   if row[0]=='Werkstatt / Material':row[1]=row[1].replace('RFI-Vorschlag drei Werktage','Technische RFI drei Werktage')
   if row[0]=='Preis / Zusatzverfahren':row[1]='Gesamthonorar EUR 47.500,00 netto / EUR 57.000,00 brutto bei 20 % USt, einschließlich EUR 2.500,00 netto Bauwerksbuch; ursprüngliche vier Positionen unverändert. Keine automatische Indexierung. Echte Änderungen konkret abgrenzen und vorher beauftragen; gesetzliche Ansprüche nach §§ 9 und 15 bleiben getrennt.'

mods=deepcopy(m['modificari'])
for x in mods:
 if x['id'] in ['M01','M02','M03','M04']:
  x['status']='FESTLEGUNG AG / Namen und tatsächliche Daten noch zu ergänzen';x['raspuns']=answers[2]['raspuns'];x['propunere_RO']+=' Funcțiile arhitecturale și Bauführer nu se atribuie lui BERGER; numele/datele se completează separat.'
 elif x['id'] in ['M07','M08','M09','M10']:
  x['status']='DE CONFIRMAT DE BERGER / persoane, întindere și preț';x['raspuns']=answers[1]['raspuns']
 elif x['id']=='M11':
  x['status']='DECIS DE PROPRIETAR / 2.500 EUR net inclus în total';x['raspuns']=answers[0]['raspuns'];x['propunere_RO']='Bauwerksbuch complet pentru existent și intervenții noi, prima verificare, documentație, înregistrare necesară și actualizări până la închidere: 2.500 EUR net. Total 47.500 EUR net / 57.000 EUR cu TVA. Fără dublarea poziției. Confirmarea BERGER privește obiectul complet explicit, nu doar suma.'
 elif x['id'] in ['M06','M13']:x['status']='DECIS DE PROPRIETAR / termene 5 și 3 zile';x['raspuns']=answers[3]['raspuns']
 elif x['id']=='M15':x['status']='DECIS DE PROPRIETAR / email scurt și listă comună';x['raspuns']=answers[5]['raspuns']
 elif x['id'] in ['M16','M17']:x['status']='DECIS DE PROPRIETAR / formate delimitate';x['raspuns']=answers[4]['raspuns'];x['propunere_RO']='PDF semnat, DWG/DXF editabile și calcule complete obligatorii. IFC și fișiere native existente, în limitele transferabilității tehnice și juridice; fără obligația unui model BIM nou.'
 elif x['id']=='M18':x['status']='DE COMPLETAT DE BERGER ȘI AG / calendar cu valori';x['raspuns']='Se păstrează cerința unui calendar de livrare/facturare cu valori; a fost adăugat tabelul celor cinci poziții, fără inventarea ratelor procentuale sau a datelor.'
 elif x['id']=='M19':x['status']='DE FURNIZAT DE BERGER / dovada existentă';x['raspuns']='Fără majorarea limitei de asigurare.'
 else:x['status']='IMPLEMENTAT / clarificare și corelare';x['raspuns']='Păstrat conform notelor clare și instrucțiunilor existente; fără tarif sau fapt presupus.'
 x['intrebare_istorica']=x['intrebare_proprietar']
 if x['status'].startswith('DECIS'):x['intrebare_proprietar']='Alegerea proprietarului este închisă prin răspunsul din 2026.10.29; BERGER confirmă textul contractual rezultat sau indică punctual o corectură.'
 elif x['id'] in ['M01','M02','M03','M04']:x['intrebare_proprietar']='Se completează persoanele desemnate, documentele și datele reale înainte de semnare/începerea funcției; funcțiile arhitecturale și Bauführer nu sunt atribuite lui BERGER.'
 elif x['id'] in ['M07','M08','M09','M10']:x['intrebare_proprietar']='BERGER completează identitățile, rolurile, întinderea și includerea în pozițiile de preț; nu se presupune un nume sau un cost nou. Orice abatere se agreează înainte de semnare.'
 elif x['id']=='M18':x['intrebare_proprietar']='BERGER propune datele și eventualele tranșe în tabelul celor cinci poziții; părțile confirmă calendarul valoric, fără depășirea sumelor.'
 elif x['id']=='M19':x['intrebare_proprietar']='BERGER furnizează dovada actuală promisă; nu există o nouă alegere de limită de asigurare.'
 else:x['intrebare_proprietar']='Nu se cere o nouă alegere proprietarului; verificarea factuală ori documentară rămasă se face de responsabilul desemnat.'

clean=json.dumps(new,ensure_ascii=False)
for banned in ['Offene AG-Entscheidungen','offene Arbeitsfassung','RFI-Vorschlag','abgelehnte Bauwerksbuch-Inklusion','vor Unterzeichnung ausdrücklich zu entscheiden']:
 assert banned not in clean,banned
assert new['annexes'][3]['tables'][0]['rows'][:4]==old['annexes'][3]['tables'][0]['rows'][:4]
assert sum(Decimal(row[1].replace('.','').replace(',','.')) for row in new['annexes'][3]['tables'][0]['rows'][:-1])==Decimal('47500')
assert len(new['sections'])==16 and len(new['annexes'])==6
email=root/'08. Corespondenta/2026.10.28 Verificare zilnica/2026.10.27 21-52-35 PRIMIT BERGER ed6dfacf.json'
assert '2.500 Euro netto' in json.loads(email.read_text(encoding='utf-8'))['original_EVA']['text']
sources=deepcopy(m['surse'])+[{'id':'S3','tip':'Email BERGER - preț Bauwerksbuch','cale':email.relative_to(root).as_posix(),'sha256':hashlib.sha256(email.read_bytes()).hexdigest()},{'id':'S4','tip':'Deciziile proprietarului din conversație, 2026.10.29','cale':(folder/'2026.10.29 Raspunsuri proprietar BERGER.json').relative_to(root).as_posix(),'sha256':''}]
(folder/'2026.10.29 Raspunsuri proprietar BERGER.json').write_text(json.dumps(answers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');sources[-1]['sha256']=hashlib.sha256((root/sources[-1]['cale']).read_bytes()).hexdigest()
model={'data':'2026.10.29','original':old,'vorschlag':new,'modificari':mods,'raspunsuri_primite':answers,'status':'VERSIUNE ACTUALIZATA PENTRU CONFIRMAREA BERGER; deciziile AG sunt integrate. Nume PI/ZT, roluri externe, date si calendar valoric raman de completat. Nu este contract semnat.','surse':sources,'surse_legale':m['surse_legale']}
(folder/'2026.10.29 Werkvertrag BERGER R11.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(folder/'2026.10.29 BERGER R11 model comparativ si decizii.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'folder':str(folder),'total_net':47500,'total_gross':57000,'answers':len(answers),'original_fee_rows_preserved':True,'mods':len(mods)},ensure_ascii=False))
