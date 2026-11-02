from pathlib import Path
import json, hashlib, shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root=Path.cwd()
out=root/'00.Proiect/09. Vertraege/zt-pech.at/2026.10.27 Kurzvertrag Checkliste'
out.mkdir(exist_ok=True)
d=Document(); s=d.sections[0]
for st in d.styles:
 for el in list(st.element.iter(qn('w:pBdr'))): el.getparent().remove(el)
s.page_width=Inches(8.5); s.page_height=Inches(11)
s.top_margin=s.bottom_margin=Inches(.65); s.left_margin=s.right_margin=Inches(.72)
style=d.styles['Normal']; style.font.name='Arial'; style.font.size=Pt(11)
style.paragraph_format.space_after=Pt(6)
style.paragraph_format.line_spacing=1.04
for name,size in [('Title',20),('Heading 1',13),('Heading 2',11)]:
 st=d.styles[name]; st.font.name='Arial'; st.font.size=Pt(size); st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_before=Pt(9); st.paragraph_format.space_after=Pt(5)
def p(t,bold=False):
 a=d.add_paragraph(); a.add_run(t).bold=bold; return a
def h(t):d.add_heading(t,1)
def ck(t):p('☐ '+t)
def table(rows,widths):
 t=d.add_table(rows=0,cols=len(widths));t.autofit=False
 for col,w in zip(t.columns,widths):col.width=Inches(w)
 for n,row in enumerate(rows):
  cells=t.add_row().cells
  for c,w,txt in zip(cells,widths,row):
   c.width=Inches(w); c.text=txt
   for a in c.paragraphs:
    a.paragraph_format.space_after=Pt(4);a.paragraph_format.space_before=Pt(4)
    for r in a.runs:r.font.size=Pt(10.5);r.bold=n==0
  trPr=t.rows[-1]._tr.get_or_add_trPr();trPr.append(OxmlElement('w:cantSplit'))
 return t
header=s.header.paragraphs[0];header.text='SCHALLERGASSE 35  |  PECH';header.runs[0].font.size=Pt(9)
f=s.footer.paragraphs[0];f.text='2026.10.27 · Entwurf zur Abstimmung · Seite '
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
for r in f.runs:r.font.size=Pt(9)
d.add_heading('Kurzvertrag mit Leistungscheckliste',0)
p('Schallergasse 35 in 1120 Wien',True)
p('Entwurf zur gemeinsamen Abstimmung. Offene Felder und Abweichungen vor Unterzeichnung ausfüllen; keine bisherige Beauftragung oder Einigung wird vorausgesetzt.')
p('Auftraggeber (AG): A&C Wohnart Immobilien GmbH, FN 668224h\nRechnungsanschrift / UID: __________________________________________\nAuftragnehmer (AN): Dr. PECH Ziviltechnikergesellschaft mbH, FN 426034x\nAnschrift laut Angebot: Johann-Strauß-Gasse 32/11, 1040 Wien\nAktuelle Vertragsanschrift bestätigen: _________________________________')
h('1 Grundlagen und Honorar')
p('Grundlage sind AN01 vom 2026.09.17, AN02 vom 2026.10.21 und die Leistungsbeschreibung zur Anfrage vom 2026.07.20. Diese Kurzvereinbarung fasst den Auftrag zusammen und regelt die ausdrücklich vereinbarten Abweichungen.')
table([
['Position','Leistung','EUR netto'],
['AN01 01','Ausführungsstatik','42.000'],['AN01 02','Durchbruchsplanung Bestand','6.000'],['AN01 03','Baugrubensicherung','5.000'],['AN01 04','Untergrundbeschau','800'],['AN01 05','Baubegleitung mit 12 Abnahmen','14.000'],['AN01 06','Schlussunterlagen','1.500'],
['AN02 01','Prüfingenieur','3.500'],['AN02 02','Fertigstellungsanzeige','1.800'],['AN02 03','Bauwerksbuch','3.000'],['Gesamt','AN01 69.300 + AN02 8.300','77.600']], [1.05,4.95,1.0])
p('Bei unverändertem Gesamtumfang: 77.600 EUR netto + 15.520 EUR USt. = 93.120 EUR brutto. Zusatzleistungen und eine vereinbarte Indexierung sind darin nicht enthalten.')
ck('Alle neun Positionen werden beauftragt. Abweichungen / Preisänderungen: ______________________________________________________________')
p('Vereinbarter Gesamtpreis netto: __________________ EUR',True)

d.add_page_break();h('2 Technischer Umfang aus der ersten Anfrage')
p('Die Häkchen bestätigen den vereinbarten Umfang. Abweichungen und deren Preisfolgen sind unten festzuhalten. Eingeklammerte Mengen der ersten Anfrage werden hier verbindlich konkretisiert.')
ck('Ausführungsstatik: Fundamentplatte einschließlich Baugrund- und Setzungsnachweisen; Verbunddecke über dem 3. OG samt Anschlüssen und Bauzuständen; DG 1 und 2 mit Terrassen und Dachaufbauten; Aufzugsschacht samt Gründung; Mauerwerksertüchtigung. Vorbemessung 2021 als Grundlage; erforderliche Überarbeitungen vorab benennen.')
ck('Durchbrüche: sämtliche Positionen der abgestimmten Liste einschließlich Abfangungen, Auflagern und Einbauhinweisen; Lastnachweise neuer Nassräume auf Bestandsdecken; statische Freigabe der Auswechslungsplanung. Inkludiert: ____ Positionen (Anfrage: 15); weitere: ____ EUR netto je Position.')
ck('Baugrubensicherung und Unterfangungen: Berechnungen, Ausführungsdetails, Aushubabschnitte und Bauzustände einschließlich Auswirkungen auf Nachbarobjekte.')
ck('Untergrundbeschau: ein Termin mit Prüfingenieur und Bauführer; schriftlicher Abgleich mit den Berechnungsannahmen und nötige Anpassungen. Weiterer Termin: ____ EUR netto. Zusätzliche Untersuchungen nur nach gesonderter Freigabe.')
ck('Baubegleitung: 12 Bewehrungsabnahmen; zusätzliche Abnahme 450 EUR netto. Abnahmevermerk binnen 2 Werktagen; bis zu 20 statische Baustellenanfragen, Antwort binnen 3 Werktagen. Planungsbesprechungen: 6, davon 3 vor Ort. Abweichungen: siehe unten.')
ck('Schlussunterlagen: Zuverlässigkeitsnachweis der Tragwerke, Mitwirkung an der ZT-Bestätigung und As-built-Statik. Berechnungen als prüffähige PDF; Pläne als PDF und DWG/DXF, Positionspläne sowie Stahl- und Einbauteillisten; Modelle/Rechenfiles auf Anforderung.')
h('3 Ergänzungen aus AN02')
ck('Prüfingenieur: verantwortliche Person __________________; Kontrollen und Berichte bis Abschluss gemäß vereinbartem Prüfprogramm. Unabhängigkeit und mögliche Rollenüberschneidungen vor Bestellung klären; Abgrenzung zu AN01 ohne Doppelverrechnung.')
ck('Fertigstellungsanzeige: PECH beschafft die Unterlagen und stellt die Formulare zusammen; Einreichung durch AG/Vertreter. Vollständige ZT-Bestätigung durch __________________; Honorar ☐ enthalten ☐ zusätzlich ____ EUR netto.')
ck('Bauwerksbuch mit Bauteilprüfungen und Prüfintervallen. Umfang bestätigen: ☐ Bestand und Neubau ☐ Erstbegehung ☐ erforderliche Registrierung. Fehlende Teile / Mehrpreis: ______________________________')
p('Abweichungen zu den Punkten oben einschließlich Kosten:\n________________________________________________________________\n________________________________________________________________')

d.add_page_break();h('4 Termine und praktische Abwicklung')
p('Planungsstart nach schriftlicher Beauftragung und vollständigen Grundlagen: __________. Baubeginn: __________. Enthaltene Baubegleitung: ____ Monate ab Baubeginn. Ansprechpartner PECH: __________________.')
p('Schalungs- und Bewehrungspläne: 4 Wochen Bearbeitungsvorlauf ab vollständigen Grundlagen. AG/Baufirma melden den Bedarf entsprechend früher. Verzögerungen und ihre Auswirkungen werden umgehend schriftlich mitgeteilt.')
table([['Lieferung','Vereinbarter Termin'],['Fundament und Verbunddecke','________________'],['DG und Aufzug','________________'],['Durchbrüche und Baugrubensicherung','________________'],['Schlussunterlagen und AN02','________________']], [4.9,2.1])
p('Kurzer Bericht je Kontrolle, aktuelle Planliste und schriftliche Freigaben genügen; keine zusätzlichen wöchentlichen Statusberichte oder separaten Terminregister. Änderungen und offene Entscheidungen werden per E-Mail festgehalten.')
h('5 Zahlungsbedingungen und Mehrkosten')
p('Abrechnung nach nachgewiesenem Leistungsfortschritt, nachvollziehbar je Position; keine Anzahlung. Zahlungsziel: ☐ 14 Tage ab Rechnung gemäß Angebot ☐ abweichend: __________. Haftrücklass: ☐ keiner gemäß Angebot ☐ abweichend: __________. Vertragsstrafe: ☐ keine gemäß PECH-Wunsch ☐ gesonderte Regelung: __________.')
p('Preisbindung – eine Variante wählen: ☐ Fixpreis bis 2028.06.30 gemäß Anfrage ☐ ZT-Index gemäß Angebot; Basis __________, erste Anpassung __________, Obergrenze __________. Nebenkosten/Fahrten: ☐ enthalten ☐ zusätzlich ausschließlich: __________________.')
p('Zusatzleistungen, weitere Besuche und Stehzeiten nur nach vorheriger schriftlicher Freigabe von Umfang, Preis und Terminfolgen. Regie netto je Stunde: ZT 195 EUR; Projektleitung 145 EUR; Techniker 125 EUR; Zeichner 95 EUR. Eigene Fehlerkorrekturen werden nicht zusätzlich verrechnet.')
h('6 Abschluss und Unterschriften')
p('AG darf die bezahlten Unterlagen für dieses Gebäude nutzen und an ausführende Firmen sowie weiterbearbeitende Fachplaner geben. Bei Beendigung werden die erarbeiteten Unterlagen gegen Abrechnung der erbrachten Leistungen übergeben. Befugnis und Berufshaftpflicht nachweisen; gewünschte Deckung gemäß Anfrage: 2 Mio. EUR je Schadenfall, Abweichung: __________.')
p('Rangfolge bei Widersprüchen: diese ausgefüllte, beidseitig unterzeichnete Vereinbarung; technische Leistungsbeschreibung der Anfrage; AN01/AN02; deren AGB ergänzend. Frühere Vertragsentwürfe einschließlich R09 werden nicht Vertragsbestandteil. Offene Felder sind vor Unterzeichnung zu schließen.')
p('Ort / Datum: ____________________\n\nAG: __________________________    PECH: __________________________')
target=out/'2026.10.27 Kurzvertrag PECH Checkliste.docx';d.save(target)
sources=json.loads((root/'00.Proiect/09. Vertraege/2026.10.26 Checklisturi intalniri/2026.10.26 Surse si continut checklisturi.json').read_text(encoding='utf-8'))['sources']
sources={k:v for k,v in sources.items() if k.startswith('PECH')}
initial='08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Atasamente/Pech/2026.07.20 a856a9fb Anfrage_Ausfuehrungsstatik.docx'
sources['CERERE_INITIALA']={'cale':initial}
idx={r['cale']:r for r in json.loads((root/'folder map/inventar.json').read_text(encoding='utf-8'))}
for v in sources.values():
 path=root/v['cale']; digest=hashlib.sha256(path.read_bytes()).hexdigest();v['sha256_actual']=digest;v['neschimbat_fata_de_index']=digest==idx[v['cale']]['sha256']
 # Opening the original request verifies its text against the reusable cache.
original=Document(root/initial)
assert any('Fundamentplatte' in x.text for x in original.paragraphs)
(out/'2026.10.27 Surse si diferente.json').write_text(json.dumps({'data':'2026.10.27','statut':'DRAFT NETRIMIS NESEMNAT','surse':sources,'baza':'Cererea trimisa la 2026.07.20, AN01, AN02 si observatiile PECH din 2026.10.21','diferente':'Nu se preiau automat extensiile R09: 18 luni, IFC, termenele D1-D5 si penalitatile. Conditiile contestate au optiuni necompletate. Cerintele tehnice initiale sunt pastrate; mentiunile suplimentare AN02 necesita bifare si completare.','informare_utilizator':'PECH solicita o versiune mai simpla de contract tip checklist; comunicare relatata de utilizator, fara ID EVA nou.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(target)
