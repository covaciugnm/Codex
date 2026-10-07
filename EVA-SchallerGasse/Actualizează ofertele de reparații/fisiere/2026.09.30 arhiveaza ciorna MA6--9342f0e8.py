from pathlib import Path
import json,shutil
from email.message import EmailMessage
from email.policy import SMTP
from email.utils import format_datetime
from datetime import datetime
R=Path(__file__).resolve().parent.parent;D='2026.09.30';F=R/'08. Corespondenta'/f'{D} MA6 - Corectare aviz Q3'
d=json.loads((F/f'{D} DRAFT NETRIMIS - MA6.json').read_text(encoding='utf-8'))
assert d['status']=='pending' and d['to']==['kanzlei-b09@ma06.wien.gv.at']
j=json.loads((R/'10. Banci + Extrase de cont/2026.09.30 Audit facturi si plati/2026.09.30 Registru verificat.json').read_text(encoding='utf-8'))
source=R/next(x['Document local'] for x in j['documente'] if x['ID']=='F018')
att=F/'2026.07.10 MA6 aviz 480960377428.pdf';shutil.copy2(source,att)
header=f'{D} | DRAFT, NETRIMIS\nDe la: {d["account_email"]}\nCatre: '+', '.join(d['to'])+'\nSubiect: '+d['subject']+'\nID Eva-Mail: '+d['id']+'\nAtasament: '+att.name+'\n\n'
(F/f'{D} DRAFT NETRIMIS - MA6.txt').write_text(header+d['body'],encoding='utf-8-sig')
msg=EmailMessage(policy=SMTP);msg['From']=d['account_email'];msg['To']=', '.join(d['to']);msg['Subject']=d['subject'];msg['Date']=format_datetime(datetime.fromisoformat(d['created_at'].replace('Z','+00:00')));msg['X-Unsent']='1';msg['X-Eva-Draft-ID']=d['id'];msg.set_content(d['body']);msg.add_attachment(att.read_bytes(),maintype='application',subtype='pdf',filename=att.name)
(F/f'{D} DRAFT NETRIMIS - MA6.eml').write_bytes(msg.as_bytes())
note=f'{D} | MA6 — corectare aviz Q3\n\nStatus: ciorna germana salvata in Eva-Mail, NETRIMISA, ID {d["id"]}.\nCatre: kanzlei-b09@ma06.wien.gv.at\nSubiect: {d["subject"]}\n\nSolicita luarea in calcul a platii Q2 de 93,23 EUR din 2026.07.27, referinta 889970805056, confirmarea alocarii si un aviz/sold actualizat pentru Q3, cu referinta corecta a restului. Soldul de 93,23 EUR este calculul nostru, de confirmat de MA6. Avizul cumulativ original este anexat.\n\nUrmatorul pas: trimiterea ciornei din Eva-Mail, apoi urmarirea confirmarii si a documentului actualizat. Nu exista raspuns MA6 la aceasta solicitare si nici confirmare de trimitere. Sursa platii: AT13-021 din registrul financiar si extrasul personal, pagina 2; extrasul personal integral nu este anexat emailului.\n'
(F/f'{D} Jurnal MA6 - corectare Q3.txt').write_text(note,encoding='utf-8-sig')
p=R/'folder map'/f'{D} statusuri verificate.json';m=json.loads(p.read_text(encoding='utf-8'));v=m['MA6 - Taxe'];v['status']+=' 2026.09.30: ciorna germana pregatita in Eva-Mail pentru corectarea avizului Q3, tinand cont de plata Q2; NETRIMISA. ID '+d['id']+'.';v['urmatorul_pas']='Trimiterea ciornei din Eva-Mail, apoi obtinerea confirmarii alocarii Q2 si a avizului/soldului Q3 actualizat. Rest calculat 93,23 EUR, de confirmat de MA6.';v['surse'].append((F/f'{D} DRAFT NETRIMIS - MA6.txt').relative_to(R).as_posix());p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
p=R/'folder map/README.md';s=p.read_text(encoding='utf-8');entry='\n## 2026.09.30 — MA6, ciorna corectare Q3\n\nDosar: `../08. Corespondenta/2026.09.30 MA6 - Corectare aviz Q3/`. Email german catre `kanzlei-b09@ma06.wien.gv.at`, din `office@ac-wohnart.at`, DRAFT NETRIMIS in Eva-Mail, ID `'+d['id']+'`. Cere alocarea platii Q2 din 2026.07.27, 93,23 EUR, referinta 889970805056, si aviz/sold Q3 actualizat. Avizul original este anexat; text, JSON, EML cu atasament si jurnal sunt pe disc. Nu exista trimitere sau acceptare MA6 confirmata.\n';p.write_text(s+entry,encoding='utf-8')
print(json.dumps({'draft':d['id'],'status':'NETRIMIS','folder':str(F),'atasament_octeti':att.stat().st_size},ensure_ascii=False))
