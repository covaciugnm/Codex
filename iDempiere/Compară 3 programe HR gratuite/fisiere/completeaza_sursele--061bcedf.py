import json,re,html,shutil
from pathlib import Path
from colecteaza_documentatia import ROOT,REG,fetch,run,CSS
d=json.loads((Path(__file__).parent/'arborescenta_idempiere_release13.json').read_text())
rows=[]; extra=[]
sha=d['sha']
for item in d['tree']:
    p=item['path']; fn=p.split('/')[-1]
    if p.startswith('org.adempiere.base/src/') and fn.startswith('I_') and fn.endswith('.java'):
        rows.append({'model':fn[2:-5],'cale':p,'url':'https://github.com/idempiere/idempiere/blob/'+sha+'/'+p})
        if '/org/eevolution/model/I_HR_' in p or re.search(r'/I_C_(Job|JobAssignment|JobCategory|JobRemuneration|Remuneration|UserRemuneration|BP_Employee_Acct)\.java$',p):
            extra.append(dict(id='CODE'+str(len(extra)+1).zfill(3),grup='02_iDempiere/Modele_HR_release13',titlu=fn,url='https://raw.githubusercontent.com/idempiere/idempiere/'+sha+'/'+p,tip='text',nota='Model generat; existența structurii nu certifică un flux operațional complet'))
extra += [dict(id='ID15B',grup='02_iDempiere',titlu='Licență iDempiere corectată',url='https://raw.githubusercontent.com/idempiere/idempiere/'+sha+'/LICENSE.md',tip='text',nota='Calea LICENSE.md este cea existentă în repository'),dict(id='PL18',grup='05_Extensii_HR_iDempiere',titlu='iDempiere Taiwan HR mobil',url='https://www.idempiere.tw/features/payroll/?lang=en',tip='html',nota='Pistă de furnizor; licență și distribuție de verificat'),dict(id='PL19',grup='05_Extensii_HR_iDempiere',titlu='Exvee ERP 17tek Vietnam',url='https://17tek.org/products/exvee-erp/',tip='html',nota='Ofertă comercială bazată pe iDempiere; nu este plugin gratuit verificat'),dict(id='ID16',grup='02_iDempiere',titlu='Poziții și atribuiri manual',url='https://wiki.idempiere.org/en/Position_%28Window_ID-351%29',tip='html',nota='Confirmare în codul release 13 disponibilă separat')]
res=json.loads((REG/'registru_surse.json').read_text(encoding='utf-8'))
res+=run(extra)
(REG/'registru_surse.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
tech=ROOT/'07_Anexe_tehnice';tech.mkdir(exist_ok=True)
(tech/'inventar_modele_release13.json').write_text(json.dumps({'commit':sha,'trunchiat':d.get('truncated'), 'precizare':'Inventar de interfețe de model, nu listă de funcții activate. Include modele istorice și auxiliare.','modele':rows},ensure_ascii=False,indent=2),encoding='utf-8')
body='<h1>Inventar tehnic iDempiere release 13</h1><p>Commit '+sha+'. '+str(len(rows))+' interfețe de model din org.adempiere.base. Acest inventar nu dovedește activarea meniurilor sau funcționarea proceselor în instalarea beneficiarului.</p><input id="q" placeholder="Caută modelul" style="font-size:18px;width:80%;padding:12px"><table><tr><th>Model</th><th>Cod oficial la commitul verificat</th></tr>'
for r in rows:body+='<tr><td>'+html.escape(r['model'])+'</td><td><a href="'+r['url']+'">'+html.escape(r['cale'])+'</a></td></tr>'
body+='</table><script>document.getElementById("q").oninput=function(){document.querySelectorAll("tr").forEach((r,i)=>{if(i)r.hidden=!r.textContent.toLowerCase().includes(this.value.toLowerCase())})}</script>'
(tech/'inventar_modele_release13.html').write_text('<!doctype html><html lang="ro"><meta charset="utf-8"><title>Inventar modele</title><style>'+CSS+'</style><body>'+body+'</body></html>',encoding='utf-8')
print('MODELE_BASE',len(rows))
