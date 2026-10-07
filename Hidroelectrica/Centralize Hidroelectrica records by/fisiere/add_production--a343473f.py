from pathlib import Path
import json,html
root=Path.cwd();work=root/'99. Evidenta verificarii/Date de lucru'
d=json.loads((work/'report_data.json').read_text(encoding='utf-8'))
rows=[]
for x in d['invoices']:
    loc=next(l for l in d['locations'] if l['pod']==x['pod'])
    if not loc['pros']:continue
    n=x['number'];p={'number':n,'location':x['location'],'pod':x['pod'],'from':x['from'],'to':x['to'],'path':x['path']}
    if 'Pallady' in x['location']:
        p.update(kwh=None,value=None,current=None,pages='p. 1–2',note='Nu există rubrică de energie produsă/livrată și nici măsurare EA prod. Neînscris nu înseamnă zero produs.')
    elif '26107829179' in n:
        p.update(kwh=9471,value=-4261.95,current=-4261.95,pages='p. 2',note='Energie activă livrată report: -9.471 kWh × 0,45 lei/kWh. Aceeași energie din FX-26107829180; nu se adună de două ori.')
    elif '26107829180' in n:
        p.update(kwh=9471,value=-4261.95,current=0,pages='p. 2–3',note='EA prod: index 0 → 9.471. Linia curentă: 0 kWh / 0 lei; Total report loc livrare: 9.471 kWh / -4.261,95 lei. Același credit ca FX-26107829179.')
    else:
        p.update(kwh=0,value=0,current=0,pages='p. 2',note='Linia Energie Activă produsă și livrată în rețea: 0 kWh / 0 lei. Index EA prod 5.075 → 5.075 (citit).')
    rows.append(p)
d['production']=rows
(work/'report_data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def fmt(x):return 'Neînscris' if x is None else f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
title='ENERGIA PRODUSĂ ȘI LIVRATĂ ÎN REȚEA — PE FACTURĂ'
note='Valorile sunt cele înscrise în facturi pentru energia livrată în rețea; nu reprezintă producția totală a panourilor, care include autoconsumul. Semnul minus reprezintă creditul în document. Cantitatea este prezentată pozitiv ca volum livrat. Cele două facturi U10 prezintă aceeași energie: total distinct 9.471 kWh, credit 4.261,95 lei, nu dublu. Lipsa rubricii la Pallady nu dovedește producție zero.'
def report(rs):return '\n\n'+title+'\n'+note+'\n\n'+'\n\n'.join(f"{p['location']} | {p['number']} | {p['from']}–{p['to']}\nLivrat/report: {fmt(p['kwh'])} kWh; valoare energie: {fmt(p['value'])} lei; linie curentă energie în factură: {fmt(p['current'])} lei.\n{p['note']}\nSursa: {p['path']}, {p['pages']}" for p in rs)+'\n'
for dest,rs in [(root/'SITUATIE_HIDROELECTRICA_2026-10-07.txt',rows)]+[(root/l['base']/'SITUATIE_2026-10-07.txt',[p for p in rows if p['pod']==l['pod']]) for l in d['locations'] if l['pros']]:
    text=dest.read_text(encoding='utf-8').split('\n\n'+title)[0]
    dest.write_text(text+report(rs),encoding='utf-8')
table='<section id="productie"><h2>Energie produsă și livrată — fiecare factură</h2><p>'+html.escape(note)+'</p><table style="width:100%;border-collapse:collapse;font-size:14px"><tr><th>Locație / factură</th><th>Perioada</th><th>Livrat / report kWh</th><th>Valoare energie lei</th><th>Observație</th></tr>'
for p in rows:table+=f'<tr><td style="padding:12px;border-bottom:1px solid #ddd">{html.escape(p["location"])}<br><a href="{html.escape(p["path"])}">{p["number"]}</a> ({p["pages"]})</td><td>{p["from"]}<br>{p["to"]}</td><td>{fmt(p["kwh"])}</td><td>{fmt(p["value"])}</td><td style="max-width:340px;padding:10px">{html.escape(p["note"])}</td></tr>'
table+='</table></section>'
dest=root/'START_HIDROELECTRICA.html';t=dest.read_text(encoding='utf-8');t=t.replace('<section><h2>Alte documente</h2>',table+'<section><h2>Alte documente</h2>');dest.write_text(t,encoding='utf-8')
# Keep the original builder runnable from the workspace after archival.
for name in ['build_workbook.mjs','finalize_workbook.py']:
    f=work/name;t=f.read_text(encoding='utf-8-sig').replace('tmp/','99. Evidenta verificarii/Date de lucru/');f.write_text(t,encoding='utf-8')
print('Production data and reports updated: '+str(len(rows))+' invoices')
