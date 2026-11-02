from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import tomllib,json,shutil
root=Path.cwd();now=datetime.now(ZoneInfo('Europe/Bucharest'));stamp=now.isoformat(timespec='seconds');tag=now.strftime('%H-%M-%S');day='2026.10.29';base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');out=Path('08. Corespondenta/2026.10.29 Monitorizare Berger Pech');proof=out/(day+' Program verificari BERGER si PECH.json');backup=root/'folder map'/(day+' Istoric program monitorizare '+tag)
configs=[]
for aid in ('verificare-emailuri-berger-i-pech','verificare-emailuri-pech'):
 configs.append(tomllib.loads((Path.home()/'.codex/automations'/aid/'automation.toml').read_text(encoding='utf-8')))
b,p=configs;assert b['rrule']=='FREQ=DAILY;BYHOUR=10,13,17;BYMINUTE=0;BYSECOND=0' and p['rrule']=='FREQ=DAILY;BYHOUR=10,16;BYMINUTE=0;BYSECOND=0';assert all(c['status']=='ACTIVE' for c in configs)
def save(path,text):
 path=Path(path);dest=root/path
 if dest.exists():
  prior=backup/path;prior.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,prior)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf-8')
def prepend(path,text):
 path=Path(path);old=(root/path).read_text(encoding='utf-8-sig') if (root/path).exists() else '';save(path,text+'\n\nISTORIC PASTRAT\n\n'+old)
save(proof,json.dumps({'data':day,'verificat_la':stamp,'solicitare':'BERGER checklist zilnic la 10:00,13:00,17:00; PECH pastrat separat la 10:00,16:00','configuratii_originale_aplicatie':configs,'fus_orar_prompt':'Europe/Bucharest','fus_orar_client_curent':'UTC+02:00'},ensure_ascii=False,indent=2))
entry=f'''{day} | Program verificari BERGER si PECH
Verificat: {stamp}
Status scurt: BERGER separat, zilnic la 10:00,13:00,17:00; checklist cu sapte puncte: mesaje, contract/observatii, preturi/servicii, atasamente, draft/Sent/nelivrare, invitatii/calendar, termene si actiuni. PECH ramane separat zilnic la 10:00 si16:00. Fus orar indicat Europe/Bucharest; client curent UTC+02:00. Ambele automatizari sunt ACTIVE si readback TOML confirma programul.
Ultimul raspuns extern: nemodificat prin aceasta schimbare de program; se consulta cele mai recente surse si jurnale.
Urmatorul pas: verificarile programate; notificare numai pentru schimbari relevante, esec sau actiune noua. Statusurile in asteptare deja raportate nu se repeta. Checklistul complet se salveaza pe disc.
Sursa: {proof.as_posix()}; configuratii aplicatie {b['id']} si {p['id']}. Verificarea generala de la 08:00 ramane nemodificata. Niciun email/RSVP trimis, document comercial modificat, contract semnat sau plata efectuata.
'''
save(out/(day+' Program verificari BERGER si PECH.txt'),entry)
reg=base/(day+' Registru comunicatii.json');r=json.loads((root/reg).read_text(encoding='utf-8-sig'));before=(len(r['comunicatii']),len(r['drafturi']));r.setdefault('istoric_monitorizare_parteneri',[]).append({'data':day,'ora_iso':stamp,'configuratie_anterioara':r.get('monitorizare_parteneri')})
r['monitorizare_parteneri']={'status':'ACTIVE','fus_orar':'Europe/Bucharest','afisare':'in acest chat, numai noutati relevante','verificare_generala_08_passtrata':True,'sursa':proof.as_posix(),'BERGER':{'id':b['id'],'ore':['10:00','13:00','17:00'],'checklist':True},'PECH':{'id':p['id'],'ore':['10:00','16:00'],'program_preexistent_passtrat':True}}
r.setdefault('actualizari_punctuale',[]).append({'data':day,'ora_iso':stamp,'tip':'Program monitorizare BERGER modificat; PECH separat pastrat','sursa':proof.as_posix(),'mesaje_noi':0,'extinde_acoperirea_EVA':False});assert before==(len(r['comunicatii']),len(r['drafturi']));save(reg,json.dumps(r,ensure_ascii=False,indent=2))
for path in (Path(day+' Status proiect.txt'),Path(day+' Log progres proiect.txt'),base/'Parteneri'/(day+' Log discutii - Markus Berger.txt'),base/'Parteneri'/(day+' Log discutii - Pech.txt'),Path('folder map/README.md')):prepend(path,entry)
print(json.dumps({'berger':b['id'],'ore_berger':['10:00','13:00','17:00'],'pech':p['id'],'ore_pech':['10:00','16:00'],'status':'ACTIVE','proof':proof.as_posix()},ensure_ascii=False))
