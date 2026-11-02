import json,hashlib,shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
tz=ZoneInfo('Europe/Bucharest');now=datetime.now(tz);day='2026.10.26';stamp=now.isoformat();tag=now.strftime('%H-%M-%S')
assert now.strftime('%Y.%m.%d')==day
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');reg=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Verificare intalniri BERGER PECH')
proof=folder/(day+' '+tag+' Dovezi EVA.json');report=folder/(day+' '+tag+' Situatie intalniri.txt')
hist=Path('folder map')/(day+' Istoric intalniri '+tag)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,text):
 p=Path(p)
 if p.exists():
  h=hist/p;h.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,h)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
p=read('folder map/2026.10.26 Dovezi etapa intalniri.json');r=read(reg);known={x['id'] for x in r['comunicatii']}
assert len(known)==len(r['comunicatii'])==836
assert len(p['searches'])==22 and not p['errors']
found={e['id'] for s in p['searches'] for e in s['result']['items']}
assert len(found)==6 and found<=known
for s in p['searches']:assert s['args']['offset']+len(s['result']['items'])>=s['result']['total']
sources={}
for e in p['full_emails']:
 assert not e['truncated'] and not e['attachments']
 row=next(x for x in r['comunicatii'] if x['id']==e['id'])
 old=read(row['json'])['original_EVA']
 assert old['text']==e['text'] and old['received_at']==e['received_at']
 sources[row['partener']]=row['cale']
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'tip':'Verificare manuala la cererea utilizatorului: intalnirile 2026.10.27','parteneri':['Markus Berger','Pech'],'mesaje_noi':0,'query_count':22,'page_count':22,'paginare_completa':True,'perioada':'2026.10.22–2026.10.26; interval larg pentru recitirea invitatiilor si a raspunsurilor','sincronizari_originale':sync,'surse_mesaje':sources,'sursa':proof.as_posix()}
general=r['acoperire']['verificare_incrementala'].copy();bp=r['acoperire']['verificare_punctuala_BERGER_PECH'].copy()
r['acoperire']['verificare_manuala_intalniri_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
for s in r['statusuri']:
 if s.get('partener') in ('Markus Berger','Pech'):s['verificare_manuala_intalniri_2026_10_26']={'checked_at_iso':stamp,'sursa':proof.as_posix(),'mesaje_noi':0}
assert r['acoperire']['verificare_incrementala']==general and r['acoperire']['verificare_punctuala_BERGER_PECH']==bp
jsave(reg,r);jsave(proof,{'verificare':entry,'baseline_ID_count':836,'final_ID_count':836,'mesaje_noi':[],'dovezi_originale':p,'nota':'Ambele raspunsuri primite au fost recitite integral in EVA; textul este identic exporturilor originale arhivate. Fara atasamente noi. Niciun email sau eveniment calendar trimis/creat.'})
text=day+' '+now.strftime('%H:%M:%S')+' — Verificare manuala intalniri pentru 2026.10.27\n\nBERGER\nStatus scurt: in raspunsul primit 2026.10.24, ii convine marti 2026.10.27; propune 11:30 ora Vienei, in loc de 11:00, si invita beneficiarul la biroul din Schönbrunner Straße. Adresa din semnatura: Schönbrunner Straße 123 / 2, 1050 Wien.\nUltimul raspuns: email c9567bdd-b010-408f-b3a9-f0866958e7ba, recitit integral, fara raspuns mai nou identificat.\nUrmatorul pas: confirmarea orei 11:30 Viena (12:30 Romania) si a deplasarii la biroul BERGER. Nu s-a identificat confirmarea beneficiarului prin email.\nSursa: '+sources['Markus Berger']+'\n\nPECH\nStatus scurt: in raspunsul primit 2026.10.22, dl. Ployer poate confirma 2026.10.27 14:00 Viena daca beneficiarul vine la biroul PECH; adresa din semnatura Johann-Strauß-Gasse 32/6, 1040 Wien.\nUltimul raspuns: email c7338d5a-3f90-44e6-8843-17681af20732, recitit integral, fara raspuns mai nou identificat.\nUrmatorul pas: confirmarea disponibilitatii de a merge la biroul PECH la 14:00 Viena (15:00 Romania). Nu s-a identificat confirmarea beneficiarului prin email.\nSursa: '+sources['Pech']+'\n\nACOPERIRE\n22 cautari/22 pagini paginate integral, primite si trimise din office si Gmail, global dupa firme/adrese/referinte, inclusiv nelivrari, 2026.10.22–2026.10.26. Sase rezultate unice, toate deja arhivate; doua raspunsuri relevante recitite integral si identice surselor arhivate. Niciun email sau atasament relevant nou. Registru 836 ID-uri.\nOffice sincronizat 2026.10.26 09:00:18 Romania; Gmail 2026.10.26 06:38:15 Romania. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.\nNu s-au trimis emailuri, creat intalniri in calendar, modificat contracte, semnat ori efectuat plati. Orele/locurile propuse nu dovedesc o intalnire efectuata sau acceptarea contractelor.\nSursa verificarii: '+proof.as_posix()+'\n'
save(report,text)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt');save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
for partner in ('Markus Berger','Pech'):
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt');save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,text+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'register':reg.as_posix(),'sources':sources,'checked_at_iso':stamp,'unique_IDs':836,'general_and_BP_coverage_preserved':True},ensure_ascii=False))
