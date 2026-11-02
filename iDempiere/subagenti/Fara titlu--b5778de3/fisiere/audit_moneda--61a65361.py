import json,hashlib,re
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
import pymupdf
root=Path(__file__).resolve().parent
exe=root.parents[1]
prev=exe/'R6_pregatire/ERP/nir/postconfig_A04'
mon=json.loads((root/'moneda-sursa.json').read_text(encoding='utf-8-sig'));assert all(r[5:7]==["100","USD"] for r in mon['rows'])
def hashp(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(p):return {'path':str(p.relative_to(exe)).replace('\\','/'),'sha256':hashp(p)}
records=[]
for subset,labels in [(prev/'run3',['control','blank','invalid']),(root/'a04-nir-r3',['zero-first','invalid-first','manual-recovery'])]:
 obs=json.loads((subset/'obs.json').read_text(encoding='utf-8'))
 for label in labels:
  c=next(c for c in obs['cases'] if c['id']==label);html=subset/(label+'.html');pdf=subset/(label+'.pdf')
  assert hashp(html)==c['html_sha256'] and hashp(pdf)==c['pdf_sha256']
  view=BeautifulSoup(html.read_text(encoding='utf8'),'html.parser');r=view.select_one('tr.total');cells=[x.get_text(' ',strip=True) for x in r.select('td')];body=view.body.get_text('\n',strip=True)
  explicit=[t.get_text(' ',strip=True) for t in view.select('p') if re.search(r'\blei\b',t.get_text(' ',strip=True),re.I)]
  assert cells[0]=='TOTAL' and len(cells)==2 and explicit
  head=[x.get_text(' ',strip=True) for x in view.select('th')]
  with pymupdf.open(pdf) as doc:
   assert len(doc)==1
   txt=doc[0].get_text()
  pdf_labels=[x.strip() for x in txt.splitlines() if re.search(r'\blei\b',x,re.I)]
  assert cells[1] in txt and pdf_labels
  assert not re.search(r'\b(USD|RON)\b',body,re.I) and not re.search(r'\b(USD|RON)\b',txt,re.I)
  records.append({'id':label,'input':c['field_readback'],'total_cells_exact':cells,'unit_on_total':'nespecificată','headers_no_currency':[x for x in head if 'Preț' in x or x=='Valoare'],'visible_html_difference_text':explicit,'visible_pdf_lines_with_currency':pdf_labels,'ISO_USD_or_RON_visible_in_HTML_or_PDF':False,'role_ui_title_subset':obs.get('ui_session_visible_titles'),'source_links':[source(html),source(pdf),source(subset/'obs.json')]})
actual={r['id']:r['total_cells_exact'][-1] for r in records};assert actual=={'control':'370,00','blank':'530,00','invalid':'530,00','zero-first':'300,00','invalid-first':'530,00','manual-recovery':'370,00'}
summary={'schema':'eva.A04.NIR.currency-corrigendum.v1','time_utc':datetime.now(timezone.utc).isoformat(),'finding':'A04-F01','corrects_immutable_source':source(prev/'rezultat.json'),'invoice_db_source':source(root/'moneda-sursa.json'),'invoice':{'id':1000002,'document':'NIR-P01-R6-002','client':11,'org':11,'docstatus':'CO','currency_id':100,'ISO_Code':'USD','TotalLines':'570.0','GrandTotal':'570.0','lines':'7×10 USD și 5×100 USD'},'correction':'Afirmația anterioară „370 lei, 530 lei, diferență 160 lei” atribuie în mod greșit moneda RON totalurilor și este înlocuită de observațiile de față. Factura sursă este în USD. În previzualizare, totalurile sunt afișate numeric fără unitate: 370,00 și 530,00. Diferența aritmetică este 160,00 în unitățile prețurilor preluate din liniile facturii USD. Nu există în aceste dovezi un curs, o conversie sau o justificare pentru exprimarea totalurilor în lei.','observed_currency_label':'Parantezele din rubrica diferențelor conțin literal «lei». Textul vizibil al TOTAL și antetele «Preț unitar», «Valoare» nu indică o monedă. Nici PDF-ul, nici HTML-ul nu afișează un cod ISO USD sau RON. Sumele din rubrica diferențelor reproduc numeric diferențele × prețul din factura USD și poartă o etichetă inconsecventă; linia «Azalea Bush Azalea Bush: -4 Ea (-40,00 lei)» este imprimată în cazul gol/invalid.','recovery':'În aceeași sesiune ZK: 0 urmat de 3 → 300,00; invalida urmat de 3 → 530,00 fără blocaj; corectarea manuală în formular la 7 și 3 → 370,00. Valoarea zero numerică nu echivalează cu un rând gol. Nu s-a dovedit că operatorul primește vreun avertisment sau îndrumare automată; recuperarea demonstrată este manuală.','monetary_scope':'Acest caz demonstrează poziționarea greșită a cantităților și eticheta monetară afișată. Nu există dovadă că o sumă de 160 RON/USD a fost postată sau pierdută. Nu a fost emis documentul și nici nu s-a mutat stoc.','cases':records,'review_status':'Predat către A12 și A11 pentru reevaluare; raportul inițial este păstrat.'}
(root/'Addendum_moneda_NIR.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(hashp(root/'Addendum_moneda_NIR.json')); print([(x['id'], x['visible_pdf_lines_with_currency']) for x in records])
