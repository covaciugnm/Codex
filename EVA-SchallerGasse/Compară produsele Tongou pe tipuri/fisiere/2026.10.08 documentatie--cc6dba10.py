from pathlib import Path
import json,shutil,html,hashlib
from urllib.parse import quote,unquote,urlparse
from bs4 import BeautifulSoup
from openpyxl import load_workbook
R=Path.cwd();A=R/'Acasa';D='2026.10.08';O=A/'Documentatie Tongou';(O/'PDF producator').mkdir(parents=True,exist_ok=True);(O/'Fise produse').mkdir(exist_ok=True)
C=R/'04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ'
P=json.loads((C/'Date structurate'/f'{D} produse-normalizate.json').read_text('utf8'))
M=json.loads((C/'Date structurate'/f'{D} registru manuale oficiale.json').read_text('utf8'))
docs=[]
for m in M:
 if m.get('status')!='DESCARCAT':continue
 src=C/Path(m['path']);dst=O/'PDF producator'/src.name;shutil.copy2(src,dst)
 assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(dst.read_bytes()).digest()
 docs.append(dict(m,local='PDF producator/'+src.name))
def e(x):return html.escape(str(x))
css='''body{font:16px/1.5 Segoe UI,Arial,sans-serif;color:#243b53;background:#f4f7fa;margin:0}main{max-width:1250px;margin:auto;padding:32px}h1{line-height:1.2}h2{margin-top:32px}a{color:#155ead}table{width:100%;border-collapse:collapse;background:white}th,td{padding:12px;border:1px solid #d7e1eb;text-align:left;vertical-align:top}th{background:#243b53;color:white;position:sticky;top:0}td:first-child{min-width:140px}.note{background:#fff2cc;padding:16px;border-left:5px solid #b07800}.good{color:#267347}.bad{color:#b42318}.muted{color:#64748b}.card{background:white;padding:20px;border-radius:8px;margin:16px 0}input{padding:12px;font:inherit;width:95%;max-width:700px;border:1px solid #abc;border-radius:6px}button{padding:10px;font:inherit;cursor:pointer}.tag{font-size:13px;padding:4px 8px;background:#eaf2fc;border-radius:4px}details{margin:12px 0}@media print{body{background:white}main{padding:0}input,button,nav{display:none}th{position:static}table{font-size:11px}tr{break-inside:avoid}}'''
def page(title,body):return '<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><style>'+css+'</style><main>'+body+'</main></html>'
def link(p,label):return f'<a href="{quote(p,safe="/")}">{e(label)}</a>'
def assigned(sku):
 if sku in ['43067','43068','43076','43077','43078']:return ['TOQCB2 manual']
 if sku in ['43070','43071','43079','43080','43081']:return ['TOQCB2L fisa','TOQCB2 manual']
 if sku=='43082':return ['TOSMR1']
 if sku=='43073':return ['TOSMR1','TOQCB2L']
 if sku in ['43074','43083']:return ['SY1 SY2']
 if sku in ['43084','43085','43086','43087']:return ['TOQCB2 manual','SY1 SY2']
 if sku=='43092':return ['TORD4']
 if sku in ['43094','43095','43096']:return ['TOSPO AC']
 if sku in ['43097','43098']:return ['TOSP DC']
 return []
registry=[];indexrows=[]
for p in P:
 sku=p['sku'];matches=[m for m in docs if any(m['titlu'].startswith(x) for x in assigned(sku))]
 title=f'{sku} — {p["name"]}';filename=f'{D} SKU {sku} fisa de sinteza.html'
 status='PDF-uri de familie disponibile; corespondența exactă SKU trebuie verificată' if matches else 'Fișă PDF oficială pentru acest model neidentificată în sursele verificate'
 body='<nav>'+link('../'+D+' Documentatie Tongou.html','← Toate produsele')+'</nav><h1>'+e(sku)+'<br>'+e(p['name'])+'</h1><p class="tag">Fișă de sinteză întocmită · '+D+'</p>'
 body+='<p class="note">Aceasta este o sinteză a informațiilor publicate de comerciant, nu fișa oficială a fabricantului, certificat sau confirmare de echivalență. Necunoscutele și contradicțiile sunt păstrate. Documentele originale sunt accesibile mai jos.</p>'
 body+='<p><a href="'+e(p['source'])+'">Pagina Conex a produsului</a> · Captură date: '+D+' · <button onclick="window.print()">Tipărește / salvează PDF</button></p>'
 body+='<h2>Fișe și manuale originale</h2><p>'+e(status)+'</p><ul>'
 for m in matches:body+='<li>'+link('../'+m['local'],m['titlu']+' — PDF, '+str(m['pages'])+' pagini')+' · <a href="'+e(m['url'])+'">sursa fabricantului</a><br><span class="muted">'+e(m['observatii'])+'</span></li>'
 body+='</ul>'
 if sku in ['43073','43083','43084','43085','43086','43087']:body+='<p class="note">Asociere documentară incertă: modelul, familia sau protocolul din descriere nu sunt concordante. PDF-urile sunt referințe de familie, nu dovada funcțiilor SKU.</p>'
 if sku in ['43094','43095','43096']:body+='<p class="note">PDF-ul disponibil este certificat, nu datasheet tehnic complet.</p>'
 if sku=='43092':body+='<p class="note">Declarația TORD4 indică RCCB, deși Conex îl prezintă RCBO. Nu presupune protecție la suprasarcină/scurtcircuit.</p>'
 body+='<h2>Specificații publicate pentru SKU</h2><table><thead><tr><th>Caracteristică</th><th>Valoare / statut</th></tr></thead><tbody>'
 for k,v in p['technical'].items():
  cl='good' if str(v).startswith('✓') else 'bad' if k=='Cantitate disponibilă (buc.)' and v==0 else ''
  body+='<tr><td>'+e(k)+'</td><td class="'+cl+'">'+e(v)+'</td></tr>'
 body+='</tbody></table><h2>Observații și diferențe</h2><ul>'+''.join('<li>'+e(o)+'</li>' for o in p['observations'])+'</ul>'
 body+='<details><summary>Textul comercial arhivat</summary><pre style="white-space:pre-wrap">'+e(p['source_text'])+'</pre></details>'
 body+='<p class="muted">Stocul nu este rezervat; prețul este orientativ de catalog. Funcțiile smart nu confirmă capacitatea de rupere, tipul diferențial sau adecvarea pentru un circuit existent.</p>'
 (O/'Fise produse'/filename).write_text(page(title,body),encoding='utf8')
 indexrows.append('<tr><td>'+link('Fise produse/'+filename,sku)+'</td><td>'+e(p['name'])+'</td><td>'+e(p['poles'])+'</td><td>'+e(p['technical'].get('Comunicație SKU','—'))+'</td><td>'+str(p['technical']['Cantitate disponibilă (buc.)'])+'</td><td>'+('PDF familie: '+str(len(matches)) if matches else 'Sinteză; PDF neidentificat')+'</td></tr>')
 registry.append({'sku':sku,'html':'Fise produse/'+filename,'statut':status,'pdf':[m['local'] for m in matches],'source':p['source']})
body='<h1>Tongou · Fișe, manuale și specificații</h1><p>'+D+' · 29 produse · 12 PDF-uri originale · 29 fișe de sinteză individuale</p><div class="note">Deschide codul produsului pentru toate specificațiile și documentele asociate. PDF-urile fabricantului sunt separate de sintezele întocmite. Cele 5 linkuri PDF din catalogul Conex au returnat 404 la colectare; documentele de mai jos provin din sursele oficiale alternative arhivate.</div>'
body+='<div class="card"><label for="q">Caută după cod, model, poli sau protocol</label><br><input id="q" placeholder="Exemplu: 43082, Zigbee, 4P" oninput="filterRows(this.value)"><p>'+link('../2026.10.08 Acasa inventar si echivalente.xlsx','Deschide Excelul cu inventar, necesar și stoc')+'</p></div><table id="products"><thead><tr><th>SKU / fișa</th><th>Produs</th><th>Poli</th><th>Protocol</th><th>Stoc</th><th>Documentație</th></tr></thead><tbody>'+''.join(indexrows)+'</tbody></table>'
body+='<h2>Toate PDF-urile originale</h2><ul>'+''.join('<li>'+link(m['local'],m['titlu']+' — '+str(m['pages'])+' pagini')+'</li>' for m in docs)+'</ul><p class="muted">Pagina funcționează local, fără internet pentru fișierele salvate. Linkurile către comerciant și fabricant necesită internet.</p><script>function filterRows(q){q=q.toLowerCase();document.querySelectorAll("#products tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}</script>'
(O/f'{D} Documentatie Tongou.html').write_text(page('Tongou — documentație',body),encoding='utf8')
(O/f'{D} Registru documentatie.json').write_text(json.dumps({'products':registry,'documents':docs},ensure_ascii=False,indent=2),encoding='utf8')
# Verify every relative link, all originals and previous workbook sheet values.
checked=0
for f in O.rglob('*.html'):
 for a in BeautifulSoup(f.read_text('utf8'),'html.parser').find_all('a',href=True):
  href=a['href']
  if urlparse(href).scheme:continue
  assert (f.parent/unquote(href)).exists(),(f,href)
  checked+=1
old=load_workbook(A/'Lucru'/f'{D} Istoric inainte de sumar.xlsx');new=load_workbook(A/f'{D} Acasa inventar si echivalente.xlsx')
for sn in old.sheetnames:
 for row in old[sn]:
  for cell in row:assert cell.value==new[sn][cell.coordinate].value,(sn,cell.coordinate)
 assert set(old[sn].tables)==set(new[sn].tables)
 assert old[sn].freeze_panes==new[sn].freeze_panes
ctrl=json.loads((A/'Lucru'/f'{D} Control sumar.json').read_text('utf8'));cached=load_workbook(A/f'{D} Acasa inventar si echivalente.xlsx',data_only=True)
for i,t in enumerate(ctrl['totals']):
 row=ctrl['start']+i
 assert [cached['Necesar si stoc'].cell(row,c).value for c in [2,3,5,6]]==[t['stock'],t['need'],t['now'],t['later']]
audit={'pagini_html':30,'pdf_originale':12,'linkuri_locale_verificate':checked,'foi_anterioare_valori_tabele_freeze_pastrate':4,'centralizator_formule_verificat':True}
(A/'Lucru'/f'{D} Verificare documentatie si sumar.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(audit))
