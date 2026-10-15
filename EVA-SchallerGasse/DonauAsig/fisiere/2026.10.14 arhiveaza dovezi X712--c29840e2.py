from pathlib import Path
import json,shutil,hashlib
root=Path(__file__).resolve().parent.parent
insurance=root/'05. Asigurari/Asigurare cladire'
case=insurance/'2026.10.14 Analiza juridica Donau'
sources=case/'Surse'
records=[]
for p in [insurance/'20260526163520179.pdf',insurance/'Schalle_1080_DON_SHU_2044001194_2939905718.pdf']:
    dest=sources/('2026.10.14 Original verificat '+p.name)
    shutil.copy2(p,dest)
    records.append({'sursa':p.relative_to(root).as_posix(),'copie':dest.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for p in sources.glob('2026.10.14 Email verificat *.json'):
    d=json.loads(p.read_text(encoding='utf-8-sig'))
    text='Verificat: 2026.10.14\nStatut: PRIMIT\nData lizibilă: '+d['received_at'][:10].replace('-','.')+'\nData tehnică: '+d['received_at']+'\nID Eva-Mail: '+d['id']+'\nDe la: '+d['from_address']+'\nCătre: '+', '.join(d['to'])+'\nCC: '+', '.join(d['cc'])+'\nSubiect: '+d['subject']+'\n\nATAȘAMENTE ÎN MESAJ\n'+'\n'.join(a['name']+' | ID '+a['id'] for a in d['attachments'])+'\n\nTEXT ORIGINAL\n'+d['text']
    p.with_suffix('.txt').write_text(text,encoding='utf-8-sig')
(sources/'2026.10.14 Provenienta originale X712 si somatie mai.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
supplement=insurance/'2026.10.14 Situatie Donau/2026.10.14 Supliment cronologie martie si mai.txt'
supplement.write_text('2026.10.14 — Supliment la tabelul de 22 de comunicări\n\nDate | Tip | De la cine | Scurt cuprins | Documente anexate\n2026.03.19 | email primit | Bogdan Capra | Retransmite polița curentă primită de la Hofhans; documentul emis la 2026.02.03 are deja numărul 2044001194 și expirarea 2036.01.01. Nu este originalul X712. | Schalle_1080_DON_SHU_2044001194_2939905718.pdf; traducere română\n2026.05.27 | email primit | Bogdan Capra | Retransmite solicitarea Hofhans de informare a asigurătorului despre schimbarea proprietarului și de plată a restanței; atașează somația DONAU din 2026.05.20, cu termen de o lună. | 20260526163520179.pdf (două copii în email)\n\nSurse: JSON/TXT din ../2026.10.14 Analiza juridica Donau/Surse, ID 276acd1a-8709-473c-94ab-1d75e513a7f4 și cb505d08-3562-4ad6-a659-ed10ce34b02d. Originalele PDF au fost verificate vizual.\nTabelul Excel anterior reprezintă selecția verificată la prima întocmire; acest supliment adaugă mesajele relevante reverificate acum. Niciun mesaj nou nu a fost trimis.\nAnalizele juridice actuale din dosarul 2026.10.14, corectate pentru somația din mai, prevalează față de analiza 2026.10.07.\n',encoding='utf-8-sig')
print(json.dumps(records,ensure_ascii=False))
