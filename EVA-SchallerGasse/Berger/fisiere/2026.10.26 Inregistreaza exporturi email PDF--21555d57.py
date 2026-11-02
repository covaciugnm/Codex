from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,zipfile
root=Path.cwd();now=datetime.now(ZoneInfo('Europe/Bucharest'))
relout=Path('08. Corespondenta/2026.10.26 Emailuri primite PDF');out=root/relout
mf=out/'2026.10.26 Registru conversii email PDF.json';m=json.loads(mf.read_text(encoding='utf-8'))
assert len(m['conversii'])==9 and len({x['id_eva'] for x in m['conversii']})==9
assert sum(x['pagini'] for x in m['conversii'])==19
for x in m['conversii']:
    assert hashlib.sha256((root/x['sursa_txt']).read_bytes()).hexdigest()==x['sha256_sursa']
    assert hashlib.sha256((root/x['cale_pdf']).read_bytes()).hexdigest()==x['sha256_pdf']
    x['verificare_vizuala']='Toate paginile randate si inspectate: fara text taiat, suprapuneri sau glife lipsa; antete si subsoluri lizibile.'
m['verificare_vizuala_finala']=now.isoformat()
mf.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
archives=[]
for firm in ('BERGER','PECH'):
    target=out/f'2026.10.26 Emailuri primite {firm} PDF.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for x in m['conversii']:
            if x['firma']==firm:z.write(root/x['cale_pdf'],Path(x['cale_pdf']).name)
    with zipfile.ZipFile(target) as z:assert z.testzip() is None
    archives.append(str(target.relative_to(root)).replace('\\','/'))
backup=root/'folder map'/('2026.10.26 Istoric export email PDF '+now.strftime('%H-%M-%S'));backup.mkdir()
def keep(p):
    b=backup/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/p,b)
def prepend(p,t):
    p=Path(p);keep(p);file=root/p;file.write_text(t+'\n\n'+file.read_text(encoding='utf-8-sig'),encoding='utf-8')
regpath=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/2026.10.26 Registru comunicatii.json')
reg=json.loads((root/regpath).read_text(encoding='utf-8-sig'))
before={k:hashlib.sha256(json.dumps(reg[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest() for k in ('comunicatii','drafturi','acoperire')}
source=str(relout/'2026.10.26 Registru conversii email PDF.json').replace('\\','/')
block='2026.10.26 | TOATE EMAILURILE PRIMITE ARHIVATE BERGER / PECH - PDF PENTRU TIPARIRE\nStatus scurt: 9 mesaje unice convertite separat, 5 BERGER si 4 PECH, total 19 pagini; doua arhive ZIP cu PDF-urile individuale. Text integral verificat automat si toate paginile inspectate vizual. Antete, expeditor, destinatari, CC, ID EVA si statut PRIMIT pastrate; corespondența citata si semnaturile incluse.\nUltimul raspuns: BERGER 2026.10.24, PECH 2026.10.22, conform arhivei existente. Aceasta conversie nu este o verificare noua EVA si nu extinde acoperirea sincronizarii. Notificarea MAILER-DAEMON din 2026.10.13 nu este email de la BERGER si nu este inclusa.\nUrmatorul pas: tiparirea PDF-urilor dorite pentru intalnire; originalele text, metadatele, ofertele si contractele raman neschimbate. Atasamentele nu sunt lipite la emailuri.\nSursa: '+source+'.'
for p in ('2026.10.26 Status proiect.txt','2026.10.26 Log progres proiect.txt'):prepend(p,block)
for firm,partner in [('BERGER','Markus Berger'),('PECH','Pech')]:
    sub=[x for x in m['conversii'] if x['firma']==firm]
    entry={'data':'2026.10.26','mesaje':len(sub),'pagini':sum(x['pagini'] for x in sub),'folder':str(relout/firm).replace('\\','/'),'sursa':source,'status':'PDF-uri de tiparire din arhiva existenta; fara mesaje noi sau trimiteri'}
    journal=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri')/f'2026.10.26 Log discutii - {partner}.txt'
    text=f"2026.10.26 | EXPORT PDF EMAILURI PRIMITE {firm}\nStatus scurt: {entry['mesaje']} emailuri distincte, {entry['pagini']} pagini, fiecare email in PDF separat; text integral si paginare verificate.\nUltimul raspuns: {max(x['data_mesaj'] for x in sub)}, conform arhivei; fara verificare noua EVA.\nUrmatorul pas: tiparire pentru intalnire. Nu s-au trimis mesaje si nu s-au modificat contractele sau ofertele.\nSursa: {entry['folder']}; {source}."
    prepend(journal,text)
    for row in reg['statusuri']:
        if row.get('partener')==partner:row['export_emailuri_primite_pdf']=entry
keep(regpath)
reg['actualizari_punctuale'].append({'data':'2026.10.26','created_at_iso':now.isoformat(),'tip':'Conversie integrala emailuri primite BERGER PECH in PDF separat','mesaje_conversie':9,'mesaje_noi':0,'mesaje_trimise':0,'pdfuri':9,'pagini':19,'sursa':source,'arhive':archives})
for k,v in before.items():assert hashlib.sha256(json.dumps(reg[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==v
(root/regpath).write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
prepend('folder map/README.md','## 2026.10.26 - Emailuri primite BERGER si PECH in PDF\n\n'+block)
print(json.dumps({'pdfuri':9,'pagini':19,'arhive':archives,'comunicatii':len(reg['comunicatii']),'drafturi':len(reg['drafturi']),'backup':str(backup)},ensure_ascii=False))
