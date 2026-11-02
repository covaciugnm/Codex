import json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone,timedelta
day='2026.10.24'
now=datetime.now(timezone(timedelta(hours=3)))
assert now.strftime('%Y.%m.%d')==day
tag=now.strftime('%H-%M-%S')
stamp=now.isoformat()
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
reg=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Verificare Berger Pech')
proof=folder/(day+' '+tag+' Dovezi verificare EVA.json')
report=folder/(day+' '+tag+' Raport verificare BERGER PECH.txt')
hist=Path('folder map')/(day+' Istoric BP '+tag)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,s):
 p=Path(p)
 if p.exists():
  h=hist/p
  h.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(p,h)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(s.encode('utf-8'))
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
p=read('folder map/2026.10.24 Dovezi etapa BP dupa-amiaza.json')
r=read(reg)
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==835
assert len(p['searches'])==22 and not p['errors']
for page in p['searches']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
e=p['full_emails'][0]
assert e['id']=='c9567bdd-b010-408f-b3a9-f0866958e7ba' and not e['truncated'] and not e['attachments']
assert not e['is_sent']
ep=folder/(day+' 13-33-22 PRIMIT Markus Berger c9567bdd.txt')
ej=ep.with_suffix('.json')
jsave(ej,{'data_lizibila':day,'statut':'PRIMIT','original_EVA':e,'sursa':'Eva-Mail get_email; text integral API, nu export MIME original'})
save(ep,'Data: '+day+'; ora Romania: 13:33:22; data tehnica originala: '+e['received_at']+'\nStatut: PRIMIT\nID Eva-Mail: '+e['id']+'\nCont: '+e['account_email']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e['cc'])+'\nSubiect original: '+e['subject']+'\nSursa: Eva-Mail; text API integral, nu MIME original\n\nTEXT ORIGINAL NEMODIFICAT\n\n'+e['text'])
r['comunicatii'].append({'data':day,'ora_utc':'10:33:22','partener':'Markus Berger','domeniu':'Constructii - Structura','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':ep.as_posix(),'json':ej.as_posix(),'atasamente':[],'trunchiat':False,'data_preluarii':day})
mb={m['email']:m for m in p['mailboxes']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger','Pech'],'mesaje_noi':1,'mesaje_trimise_noi':0,'mesaje_primite_noi':1,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':22,'page_count':22,'perioada':'2026.10.23–2026.10.24; suprapunere de o zi fata de verificarea punctuala 2026.10.24 11:02; comparatie inclusiv cu verificarea generala 08:59','paginare_completa':True,'acoperire_office_limitata':False,'sincronizare_office':mb['office@ac-wohnart.at']['last_sync'],'sincronizare_gmail':mb['covaciu.gnm@gmail.com']['last_sync'],'mesaje_incidentale_alti_parteneri':0,'sursa':proof.as_posix()}
status='BERGER, mesaj primit 2026.10.24 13:33:22 Romania: marti 2026.10.27 ii convine, dar propune 11:30 ora Vienei in loc de 11:00, deoarece anterior are o intalnire in Niederösterreich. Intreaba daca beneficiarul vine la biroul sau din Schönbrunner Straße. Adresa din semnatura: Schönbrunner Straße 123 / 2, 1050 Wien. Contrapropunere de ora si loc, fara confirmarea beneficiarului sau acceptarea contractului.'
nxt='Confirmarea disponibilitatii pentru 2026.10.27 11:30 Viena (12:30 Romania) si deplasarea la biroul BERGER, Schönbrunner Straße 123 / 2, 1050 Wien. Nu se considera intalnire bilateral fixata ori contract acceptat; in aceasta verificare nu se trimite raspuns.'
for s in r['statusuri']:
 if s.get('partener')=='Markus Berger':
  s.setdefault('istoric_status',[]).append({'data_preluarii':day,**{k:s.get(k) for k in ('status','ultimul_raspuns','ultima_comunicare','ultimul_primit','urmatorul_pas','sursa_status')}})
  s.update({'status':status,'ultimul_raspuns':status,'ultima_comunicare':day,'ultimul_primit':day,'subiect_ultimul_primit':e['subject'],'urmatorul_pas':nxt,'data_actualizarii':day,'sursa_status':[ep.as_posix(),proof.as_posix()],'sursa_ultimul_primit':ep.as_posix(),'mesaje':sum(x.get('partener')=='Markus Berger' for x in r['comunicatii'])})
 if s.get('partener') in ('Markus Berger','Pech'):
  s['verificare_punctuala_BERGER_PECH_2026_10_24']={'checked_at_iso':stamp,'mesaje_noi':1 if s['partener']=='Markus Berger' else 0,'sursa':proof.as_posix()}
general=r['acoperire']['verificare_incrementala'].copy()
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry
r['acoperire']['mesaje_salvate']=836
r['data_actualizarii']=day
r.setdefault('verificari_parteneri',[]).append(entry)
r.setdefault('actualizari_punctuale',[]).append({'data':day,'tip':'BERGER/PECH: raspuns primit BERGER privind intalnirea','mesaje_noi':1,'sursa':proof.as_posix()})
assert r['acoperire']['verificare_incrementala']==general
jsave(reg,r)
jsave(proof,{'verificare':entry,'baseline_unique_ids':835,'final_unique_ids':836,'new_BP_email_ids':[e['id']],'incidental_other_partner_email_ids':[],'attachments_verified':[],'dovezi_originale':p,'general_baseline':general,'nota':'Un raspuns primit BERGER, integral, fara atasamente, fara preturi/servicii sau acceptarea contractului. Propunerea de intalnire nu este eveniment efectuat. Fara email trimis, contract modificat/semnat sau plata efectuata.'})
cov='Acoperire: 2026.10.23–2026.10.24; 22 cautari/22 pagini paginate integral, mesaje primite si trimise in ambele conturi si global, inclusiv nelivrari si referinte contractuale. Un rezultat unic: mesajul nou BERGER citit integral; registrul creste de la 835 la 836 ID-uri. Fara atasamente noi.\nSincronizari Romania: office 2026.10.24 16:30:18; Gmail 2026.10.24 11:59:32. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.\n'
text=day+' '+now.strftime('%H:%M:%S')+' — Verificare BERGER/PECH\n\nNOUTATE BERGER\nStatus scurt: '+status+'\nUltimul raspuns: '+e['id']+'; primit, fara CC/atasamente.\nUrmatorul pas: '+nxt+'\nSursa: '+ep.as_posix()+'\n\nPECH\nNicio noutate fata de verificarile anterioare. Ultimul raspuns 2026.10.22, deja raportat: poate confirma 2026.10.27 14:00 Viena daca beneficiarul vine la biroul PECH. Confirmarea deplasarii si conditiile comerciale raman de clarificat; nu se repeta ca noutate.\n\n'+cov+'Sursa verificarii: '+proof.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati.\n'
save(report,text)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt')
 save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
for partner in ('Markus Berger','Pech'):
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt')
 save(path,text+'\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md')
save(path,text+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+path.read_text(encoding='utf-8-sig'))
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==836
assert ep.read_bytes().decode('utf-8').endswith(e['text'])
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'email':ep.as_posix(),'register':reg.as_posix(),'entry':entry,'unique_IDs':836,'general_coverage_preserved':True},ensure_ascii=False))
