from pathlib import Path
import json, hashlib, html, csv, re
r=Path(__file__).resolve().parent
o=r/'7.1 Audit iterativ'; e=r/'7.6 Reevaluare punctaj'
replacements={'datelelor':'datelor','implementareaEcoWarriors':'implementarea EcoWarriors','înCSV':'în CSV','opinieEMCO':'opinie EMCO','arhivareaPDFîn':'arhivarea PDF în','înCF':'în CF','ConsiliuST':'Consiliu ST','plusdecalaj':'plus decalaj','suntn.a.':'sunt n.a.','peoperator':'pe operator','legea198':'Legea 198','surseUE':'surse UE','fațăde':'față de','CSVcomplet':'CSV complet','aleistoricului':'ale istoricului','Runda 3.csv':'Runda3.csv','eroriExcelmemorate':'erori Excel memorate','regimfărămodificare':'regim fără modificare','menținerean.a.pentru':'menținerea n.a. pentru','decalajnecunoscute':'decalaj necunoscute','OPEXintegral':'OPEX integral','necesarulcu':'necesarul cu','rămânn.a.':'rămân n.a.','Testelelimită':'Testele limită','inspecțiaformulelor':'inspecția formulelor','interactiveExcel':'interactive Excel','cuXLSXMIN/MAX':'cu XLSX MIN/MAX','salariullegal':'salariul legal','capacitateareală':'capacitatea reală','SensibilitateaF06 MAXși':'Sensibilitatea F06 MAX și','documenteUE/COM':'documente UE/COM','registrulvalidat':'registrul validat','inițialeFSE+2021':'inițiale FSE+ 2021','notelemodificării':'notele modificării','aprobămanualv 5 șiînlocuiește':'aprobă manualul v5 și înlocuiește','moduleleMySMISșiînlocuiește':'modulele MySMIS și înlocuiește','pentruSebeș':'pentru Sebeș','RPmax':'RP max','ziledupăperioadă':'zile după perioadă','zilelucrătoare':'zile lucrătoare','înainteCR':'înainte CR','CRfinalămax':'CR finală max','CPutilizatămax':'CP utilizată max','CRCPmax':'CRCP max','pânăla':'până la','dosareachiziții':'dosare achiziții','acteadiționale':'acte adiționale','FSE+modificăriînaceeașicategoriecuaprobare':'modificări FSE+ în aceeași categorie cu aprobare','personalpublic':'personal public','peclauza':'pe clauza','pentruCPnejustificate':'pentru CP nejustificate','ceAnexa':'ce Anexa','zileînainteadeciziei':'zile înaintea deciziei','GSCS/manualraportează':'GSCS/manual raportează','lafinalimplementare':'la finalul implementării','contractulFSE+art':'contractul FSE+ art','platafinală':'plata finală','șablonulOPEXinclude':'șablonul OPEX include','intervalulintermediar':'intervalul intermediar','lunifărăgol':'luni fără gol','subrezerva':'sub rezerva','clauzeisemnate':'clauzei semnate','separatminimum':'separat minimum','dela':'de la','anulultimeiplăți':'anul ultimei plăți','aprobareInstr':'aprobare Instr','șiInstr':'și Instr','dinmanual':'din manual','toateanexele':'toate anexele','strategicălocală':'strategică locală','interpretareAMrămân':'interpretare AM rămân','pentruEcoWarriors':'pentru EcoWarriors','selecțiapartenerului':'selecția partenerului','dateGT':'date GT','inventarePNRR':'inventare PNRR','puncte; 1.1,1.6 c,1.7 b,3.2 d=câte 1.4.2':'puncte; 1.1, 1.6c, 1.7b, 3.2d = câte 1 punct. Criteriul 4.2','3.3=2/2.4.2':'3.3=2/2. Criteriul 4.2','nu se atribuie fraudulos statutul':'nu i se atribuie statutul'}
def clean(s):
 for a,b in replacements.items(): s=s.replace(a,b)
 s=re.sub(r'(?<=[a-zăâîșț])(?=[A-ZĂÂÎȘȚ])',' ',s)
 s=re.sub(r'(?<=[a-zăâîșț])(?=\d)',' ',s)
 s=re.sub(r'(?<=\d)(?=[a-zăâîșț])',' ',s)
 return s
# Do not alter criterion identifiers, file names or source URLs in machine data.
for p in [o/'Runda3_Addendum.txt',e/'Runda3.txt']:
 s=p.read_text(encoding='utf-8')
 for a,b in replacements.items(): s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
style='<style>body{font:16px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 20px;color:#142b34}table{border-collapse:collapse;font-size:13px}td,th{border:1px solid #aac;padding:8px;vertical-align:top}p{margin:1.2em 0}</style>'
def render(t): return '<!doctype html><html lang="ro"><meta charset="utf-8">'+style+''.join('<p>'+html.escape(p).replace('\n','<br>')+'</p>' for p in t.split('\n\n'))
with (e/'Runda3.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f,delimiter=';'))
for row in rows:
 for key in ['Dovada_si_apreciere','Conditie_ramasa']: row[key]=clean(row[key])
with (e/'Runda3.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';'); w.writeheader();w.writerows(rows)
(o/'Runda3_Addendum.html').write_text(render((o/'Runda3_Addendum.txt').read_text(encoding='utf-8'))+'</html>',encoding='utf-8')
(e/'Runda3.html').write_text(render((e/'Runda3.txt').read_text(encoding='utf-8'))+'<table><tr>'+''.join('<th>'+html.escape(k)+'</th>'for k in rows[0])+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(v)+'</td>'for v in x.values())+'</tr>'for x in rows)+'</table></html>',encoding='utf-8')
paths=[p for d in [o,e] for p in sorted(d.glob('Runda3*')) if p.suffix in ['.txt','.html','.json','.csv'] and p.name not in ['Runda3_Manifest.json','Runda3_Pregatire.json']]
(o/'Runda3_Manifest.json').write_text(json.dumps([{'file':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths],ensure_ascii=False,indent=2),encoding='utf-8')
assert len(rows)==46
assert [sum(int(x[k])for x in rows)for k in ['Pilot_inferior','Pilot_superior','Extins_inferior','Extins_superior']]==[36,67,36,53]
print('QA OK: 46 criterii; 36–67 pilot; 36–53 extins; manifest '+str(len(paths))+' fisiere finale')
